# Erklärvideo „Der Stimmapparat“

Animiertes Trainingsvideo (1920 × 1080, 25 fps, etwa 6½ Minuten) mit männlicher deutscher Sprecherstimme und eingeblendeten Untertiteln. Die Bilder stammen direkt aus dem 3D-Modell in `../index.html`, gesteuert von einer Zeitleiste.

## Inhalt

| Kapitel | Thema |
|---|---|
| Einführung | Weg der Luft, die vier beteiligten Systeme |
| 1 Atmung | Zwerchfell, Brustkorb, Lunge, Ruhe- und Sprechatmung, Atemstütze, subglottischer Druck |
| 2 Kehlkopf | Ring-, Schild- und Stellknorpel, Kehldeckel, Stimmlippen und Glottis, Öffnen und Schließen |
| 3 Stimmlippen | Schwingungszyklus, Bernoulli-Effekt, Schleimhautwelle, Rohklang, Tonhöhe von Frau, Mann und Kind |
| 4 Resonanz | Ansatzrohr, Formanten, Quelle-Filter-Prinzip, Vokale a, i, u |
| 5 Artikulation | Zunge, Lippen, Kiefer, Gaumensegel, Plosive, Frikative, Nasale, stimmhaft und stimmlos |
| Zusammenfassung | Zusammenspiel der vier Systeme |

Hörbeispiele im Video (synthetisch nach dem Quelle-Filter-Prinzip): Rohklang der Stimmlippen, [a] in drei Stimmlagen, die Vokale [a], [i], [u] sowie die Silben pa, ta, ka, fa, sa, scha, ma und na.

## Dateien

| Datei | Zweck |
|---|---|
| `script.json` | Drehbuch: Sprechertext je Satz, Kamera, Hervorhebungen, Einblendungen, Hörbeispiele |
| `build_audio.py` | Sprachsynthese (Coqui-TTS mit der Stimme Thorsten, alternativ Piper), Hörbeispiele, Abmischung, `timeline.json`, Untertitel `.srt` und `.vtt` |
| `film.css`, `film.js` | Film-Ebene über dem 3D-Modell: Kapitelkopf, Infokarte mit Live-Diagrammen, Untertitel, Fortschritt |
| `render.mjs` | Rendert die Einzelbilder mit Playwright und Chromium, Bild für Bild mit fester Zeit |
| `make_video.py` | Fügt Bilder, Ton und Kapitelmarken zur MP4-Datei zusammen |

Die Ergebnisse landen in `out/` (nicht im Repository): `Stimmapparat_Erklaervideo.mp4`, `untertitel.srt`, `untertitel.vtt`, `tonspur.wav`.

## Neu erzeugen

Voraussetzungen: Python 3.10+, Node.js 18+, Playwright mit Chromium.

```bash
python -m venv venv
venv/bin/pip install coqui-tts torchcodec "gruut[de]" "transformers>=4.57,<4.58" scipy imageio-ffmpeg
# Männliche deutsche Stimme Thorsten (Coqui VITS, 22 kHz) herunterladen und entpacken:
curl -L -o thorsten.zip https://github.com/coqui-ai/TTS/releases/download/v0.7.0_models/tts_models--de--thorsten--vits.zip
mkdir -p voices && (cd voices && python -m zipfile -e ../thorsten.zip .)

venv/bin/python build_audio.py --voice-dir voices          # Ton, Zeitleiste, Untertitel
node render.mjs                                            # alle Bilder (dauert, CPU-Rendering)
node render.mjs --at 40,140,236                            # nur Kontrollbilder
venv/bin/python make_video.py                              # MP4 mit Kapitelmarken
```

`render.mjs` lädt Three.js und die Schriften normalerweise aus dem Netz. Ohne Netzzugang kannst du lokale Kopien übergeben: `--three pfad/three.min.js` (r128) und `--fonts ordner` mit den `@fontsource`-Paketen `bricolage-grotesque`, `atkinson-hyperlegible`, `jetbrains-mono` und `noto-sans`. Mit `--from` und `--to` lässt sich das Rendering auf mehrere Prozesse verteilen.

**Anpassen:** Text in `script.json` ändern und alle drei Schritte erneut ausführen.

- `text` ist der Untertitel. `say` ist eine optionale Sprechfassung, zum Beispiel „Peh, Teh und Kah“ für „p, t und k“.
- `respell` ersetzt Wörter, die der Phonemizer gruut sonst falsch ausspricht, etwa „Quelle“ durch „Kwelle“ oder „Frauenstimme“ durch „Frauen Stimme“. Das gilt nur für die Sprachsynthese.
- `prosody` steuert die Lebendigkeit der Stimme: `noise` für die Tonhöhenvariation, `noiseDuration` für die Variation der Lautlängen.
- Für die frühere weibliche Piper-Stimme setzt du `"engine": "piper"` und `"voice": "de-kerstin-low"`.

## Hinweise

- Die Sprecherstimme ist synthetisch (Coqui-TTS, Stimme „Thorsten“, Datensatz von Thorsten Müller, CC0). Formantwerte, Proportionen und Zeitabläufe des Modells sind für die Lehre vereinfacht.
- Die Stimmlippenschwingung wird verlangsamt gezeigt, wie bei einer Stroboskopie.
