#!/usr/bin/env python3
"""Erzeugt die Tonspur des Erklärvideos.

- Sprechertext mit Piper (offline, neuronale deutsche Stimme)
- Klangbeispiele (Rohklang, Vokale, Silben) per Quelle-Filter-Synthese
- Abmischung zu einer WAV-Datei (48 kHz, mono)
- timeline.json (Szenen, Untertitel, Regieanweisungen für das Rendering)
- Untertitel als .srt und .vtt

Aufruf: python build_audio.py --voice-dir VOICES --out OUT
"""
import argparse, hashlib, json, math, os, wave
import numpy as np
from scipy.signal import lfilter, butter, sosfilt, resample_poly

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- Sprecher
def tts_lines(script, voice_dir, cache_dir):
    from piper import PiperVoice, SynthesisConfig
    name = script["voice"]
    model = os.path.join(voice_dir, name.replace("de-", "", 1), f"{name}.onnx")
    voice = PiperVoice.load(model)
    # espeak liefert [ç] zerlegt als c + Cedille; das Stimmmodell kennt nur das ganze Zeichen
    orig = voice.phonemize
    def phonemize(text):
        out = []
        for sent in orig(text):
            merged = []
            for p in sent:
                if p == "\u0327" and merged and merged[-1] == "c":
                    merged[-1] = "ç"
                else:
                    merged.append(p)
            out.append(merged)
        return out
    voice.phonemize = phonemize
    cfg = SynthesisConfig(length_scale=script.get("lengthScale", 1.0), noise_scale=0.6, noise_w_scale=0.7)
    os.makedirs(cache_dir, exist_ok=True)
    out = {}
    for sc in script["scenes"]:
        for ln in sc["lines"]:
            key = hashlib.sha1(f'v2|{name}|{cfg.length_scale}|{ln["text"]}'.encode()).hexdigest()[:16]
            path = os.path.join(cache_dir, key + ".wav")
            if not os.path.exists(path):
                with wave.open(path, "wb") as wf:
                    voice.synthesize_wav(ln["text"], wf, syn_config=cfg)
            with wave.open(path, "rb") as wf:
                sr = wf.getframerate()
                x = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float64) / 32768
            g = math.gcd(sr, SR)
            x = resample_poly(x, SR // g, sr // g)
            out[ln["text"]] = trim(x)
    return out

def trim(x, thr=0.004):
    idx = np.where(np.abs(x) > thr)[0]
    if not len(idx):
        return x
    a = max(0, idx[0] - int(0.03 * SR)); b = min(len(x), idx[-1] + int(0.08 * SR))
    return x[a:b]

# --------------------------------------------------------------------------- Klangbeispiele
VOW = {  # Männerwerte, werden mit dem Stimmfaktor skaliert
    "a": [750, 1300, 2550, 3500], "i": [280, 2250, 2950, 3500], "u": [300, 700, 2300, 3500],
}
BW = [80, 100, 140, 200]
VOICE = {"f": (210, 1.17, 0.06), "m": (115, 1.0, 0.02), "c": (300, 1.3, 0.05)}  # f0, Formantfaktor, Behauchung

def rosenberg(phase, oq=0.62):
    p = phase % 1.0; tp = oq * 0.6
    g = np.where(p < tp, 0.5 * (1 - np.cos(np.pi * p / tp)),
        np.where(p < oq, np.cos(np.pi / 2 * (p - tp) / (oq - tp)), 0.0))
    return g

def source(n, f0, rng, vib=0.006):
    t = np.arange(n) / SR
    f = f0 * (1 + vib * np.sin(2 * np.pi * 5.2 * t) + 0.003 * np.convolve(rng.standard_normal(n), np.ones(2400) / 2400, "same"))
    ph = np.cumsum(f) / SR
    g = rosenberg(ph)
    return np.diff(g, prepend=0.0) * SR / f0 / 6  # Ableitung ≈ Abstrahlung an den Lippen

def resonator_coeffs(F, B):
    C = -math.exp(-2 * math.pi * B / SR); Bc = 2 * math.exp(-math.pi * B / SR) * math.cos(2 * math.pi * F / SR)
    return [1 - Bc - C], [1, -Bc, -C]

def cascade(x, tracks, block=240):
    """Kaskade aus 4 Resonatoren mit zeitveränderlichen Formanten (tracks: n x 4)."""
    y = x.copy(); n = len(x)
    for i in range(4):
        zi = np.zeros(2); out = np.empty(n)
        for s in range(0, n, block):
            e = min(n, s + block); F = float(np.mean(tracks[s:e, i]))
            b, a = resonator_coeffs(F, BW[i] if F > 400 else BW[i] * 1.2)
            out[s:e], zi = lfilter(b, a, y[s:e], zi=zi)
        y = out
    return y

def env(n, pts):
    """Stückweise lineare Hüllkurve, pts = [(t, v), ...]"""
    t = np.arange(n) / SR; ts, vs = zip(*pts)
    return np.interp(t, ts, vs)

def band(x, lo, hi, order=4):
    sos = butter(order, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], btype="band", output="sos")
    return sosfilt(sos, x)

def norm(x, rms=0.1):
    r = np.sqrt(np.mean(x ** 2)) + 1e-12
    return x * rms / r

def demo_sound(name, rng):
    if name == "buzz":
        f0, k, _ = VOICE["f"]; n = int(1.9 * SR)
        x = source(n, f0, rng) * env(n, [(0, 0), (0.08, 1), (1.75, 1), (1.9, 0)])
        return norm(band(x, 60, 9000, 2), 0.08)
    if name.startswith("a_") or name.startswith("v_"):
        vt = "a" if name.startswith("a_") else name[2:]
        vc = name[2:] if name.startswith("a_") else "f"
        f0, k, br = VOICE[vc]; n = int(1.0 * SR)
        x = source(n, f0, rng) * env(n, [(0, 0), (0.05, 1), (0.85, 1), (1.0, 0)])
        x += br * rng.standard_normal(n) * env(n, [(0, 0), (0.05, 1), (0.85, 1), (1.0, 0)])
        tracks = np.tile(np.array(VOW[vt]) * k, (n, 1))
        return norm(cascade(x, tracks), 0.08)
    return syllable(name, rng)

SYL = {  # Konsonant, Art, Stelle
    "pa": ("p", "plosiv", "bilabial"), "ta": ("t", "plosiv", "alveolar"), "ka": ("k", "plosiv", "velar"),
    "fa": ("f", "frikativ", "labiodental"), "sa": ("s", "frikativ", "alveolar"), "scha": ("ʃ", "frikativ", "postalveolar"),
    "ma": ("m", "nasal", "bilabial"), "na": ("n", "nasal", "alveolar"),
}
MDUR = {"plosiv": 0.11, "nasal": 0.17, "frikativ": 0.2}
LOCUS = {"bilabial": 800, "labiodental": 1000, "alveolar": 1800, "postalveolar": 1900, "velar": 1900}
BURST = {"bilabial": (500, 1500, 0.35), "alveolar": (3000, 6000, 0.6), "velar": (1500, 2600, 0.6)}
FRIC = {"f": (1600, 7000, 0.18), "s": (5000, 8500, 0.9), "ʃ": (2300, 4200, 0.8)}
NASF = {"bilabial": [250, 1100, 2300, 3500], "alveolar": [250, 1600, 2600, 3500]}

def syllable(name, rng):
    """Silbe Konsonant + [a] mit denselben Zeiten wie im 3D-Modell (Vorlauf 0,08 s + Konsonantdauer)."""
    c, m, pl = SYL[name]; f0, k, br = VOICE["f"]
    lead = 0.08; tr = lead + MDUR[m]; vend = tr + 0.45; total = vend + 0.15
    n = int(total * SR); t = np.arange(n) / SR
    va = np.array(VOW["a"]) * k
    tracks = np.tile(va, (n, 1)).astype(float)
    loc = va.copy(); loc[1] = (va[1] + (LOCUS[pl] * k - va[1]) * 0.65); loc[0] = min(va[0], 320 * k)
    if m == "nasal":
        loc = np.array(NASF[pl]) * k
    trans = 0.06
    for i in range(4):
        tracks[:, i] = np.where(t < tr, loc[i], np.where(t < tr + trans, loc[i] + (va[i] - loc[i]) * (t - tr) / trans, va[i]))
    src = source(n, f0, rng)
    noise = rng.standard_normal(n)
    if m == "plosiv":
        av = env(n, [(0, 0), (tr + 0.065, 0), (tr + 0.085, 1), (vend, 1), (total, 0)])
        ah = env(n, [(0, 0), (tr, 0), (tr + 0.005, 0.5), (tr + 0.065, 0.3), (tr + 0.08, 0), (total, 0)])
        voiced = cascade(src * av + noise * (ah + br * av), tracks)
        lo, hi, g = BURST[pl]; b = np.zeros(n); i0 = int(tr * SR); L = int(0.012 * SR)
        b[i0:i0 + L] = noise[i0:i0 + L] * np.exp(-np.arange(L) / (0.004 * SR))
        out = norm(voiced, 0.08) + band(b, lo, hi) * g * 0.9
    elif m == "frikativ":
        av = env(n, [(0, 0), (tr - 0.01, 0), (tr + 0.02, 1), (vend, 1), (total, 0)])
        voiced = cascade(src * av + noise * br * av, tracks)
        lo, hi, g = FRIC[c]
        af = env(n, [(0, 0), (lead, 0), (lead + 0.04, 1), (tr - 0.02, 1), (tr + 0.01, 0), (total, 0)])
        out = norm(voiced, 0.08) + band(noise, lo, hi) * af * g * 0.12
    else:  # nasal
        av = env(n, [(0, 0), (lead, 0), (lead + 0.03, 0.55), (tr, 0.55), (tr + 0.03, 1), (vend, 1), (total, 0)])
        voiced = cascade(src * av + noise * br * av, tracks)
        # Nasalmurmel: höhere Formanten gedämpft
        mur = np.where(t < tr, 1.0, 0.0)
        lp = sosfilt(butter(2, 700 / (SR / 2), output="sos"), voiced)
        out = norm(voiced * (1 - mur) + lp * mur * 1.6, 0.08)
    return out

# --------------------------------------------------------------------------- Zeitleiste
def at_time(spec, start, dur):
    s = str(spec)
    return start + (float(s[:-1]) / 100 * dur if s.endswith("%") else float(s))

def build(script, voice_dir, outdir):
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(7)
    narr = tts_lines(script, voice_dir, os.path.join(outdir, "tts_cache"))
    demos = {}
    gap = script.get("gap", 0.45); pad0, pad1 = script.get("scenePad", [0.6, 0.9])
    chapters = {c["id"]: c for c in script["chapters"]}
    placed, subs, cues, scenes = [], [], [], []
    t = 0.4
    for si, sc in enumerate(script["scenes"]):
        ch = chapters[sc["chapter"]]
        s0 = t
        cues.append({"t": round(s0, 3), "a": "reset", "v": dict(sc["reset"], scene=si, chapter=sc["chapter"], label=ch["label"], color=ch.get("color"), num=sc.get("num"), role=sc.get("role"))})
        t += pad0
        for ln in sc["lines"]:
            x = narr[ln["text"]]; d = len(x) / SR
            placed.append((t, x))
            for c in ln.get("cues", []):
                cues.append({"t": round(at_time(c[0], t, d), 3), "a": c[1], "v": c[2]})
            end = t + d
            for dm in ln.get("demo", []):
                if dm["sound"] not in demos:
                    demos[dm["sound"]] = demo_sound(dm["sound"], rng)
                y = demos[dm["sound"]]; ts = t + d + 0.35 + dm["at"]
                placed.append((ts, y * 1.41))  # Klangbeispiele +3 dB
                for c in dm.get("cues", []):
                    cues.append({"t": round(at_time(c[0], ts, len(y) / SR), 3), "a": c[1], "v": c[2]})
                end = max(end, ts + len(y) / SR)
            subs.append({"start": round(t - 0.05, 3), "end": round(max(end, t + d + 0.25), 3), "text": ln["text"]})
            t = end + gap
        t += pad1 - gap
        scenes.append({"start": round(s0, 3), "end": round(t, 3), "chapter": sc["chapter"], "label": ch["label"], "num": sc.get("num")})
    total = t + 1.6
    cues.append({"t": round(t + 0.1, 3), "a": "outro", "v": True})
    cues.sort(key=lambda c: c["t"])

    # Mischung
    n = int(math.ceil(total * SR)); mix = np.zeros(n)
    for ts, x in placed:
        i = int(ts * SR); mix[i:i + len(x)] += x[: max(0, n - i)]
    # Pegel: Sprache auf etwa -18,5 dBFS RMS, Spitzen weich begrenzen
    speech = np.concatenate([narr[l["text"]] for sc in script["scenes"] for l in sc["lines"]])
    gain = 10 ** ((-18.5 - 20 * np.log10(np.sqrt(np.mean(speech ** 2)) + 1e-9)) / 20)
    mix = mix * gain
    a = np.abs(mix); knee = 0.8
    mix = np.where(a > knee, np.sign(mix) * (knee + (1 - knee) * np.tanh((a - knee) / (1 - knee))), mix) * 0.97
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(outdir, "tonspur.wav"), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())

    tl = {"title": script["title"], "subtitle": script["subtitle"], "duration": round(total, 3),
          "chapters": script["chapters"], "scenes": scenes, "subs": subs, "cues": cues}
    with open(os.path.join(outdir, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(tl, f, ensure_ascii=False, indent=1)
    write_subs(subs, os.path.join(outdir, "untertitel"))
    print(f"Dauer {total:.1f} s, {len(subs)} Untertitel, {len(cues)} Regieanweisungen")

def ts_fmt(t, sep):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{int(round((s - int(s)) * 1000)):03d}"

def write_subs(subs, base):
    with open(base + ".srt", "w", encoding="utf-8") as f:
        for i, s in enumerate(subs, 1):
            f.write(f"{i}\n{ts_fmt(s['start'], ',')} --> {ts_fmt(s['end'], ',')}\n{s['text']}\n\n")
    with open(base + ".vtt", "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for s in subs:
            f.write(f"{ts_fmt(s['start'], '.')} --> {ts_fmt(s['end'], '.')}\n{s['text']}\n\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice-dir", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--script", default=os.path.join(HERE, "script.json"))
    a = ap.parse_args()
    build(json.load(open(a.script, encoding="utf-8")), a.voice_dir, a.out)
