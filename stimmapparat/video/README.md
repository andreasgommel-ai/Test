# Erklärvideo „Der Stimmapparat“

Animiertes Trainingsvideo (1920 × 1080, 25 fps, etwa 6 Minuten) mit deutscher Sprecherstimme und eingeblendeten Untertiteln. Die Bilder stammen direkt aus dem 3D-Modell in `../index.html`, gesteuert von einer Zeitleiste.

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
| `build_audio.py` | Sprachsynthese (Piper), Hörbeispiele, Abmischung, `timeline.json`, Untertitel `.srt` und `.vtt` |
| `film.css`, `film.js` | Film-Ebene über dem 3D-Modell: Kapitelkopf, Infokarte mit Live-Diagrammen, Untertitel, Fortschritt |
| `render.mjs` | Rendert die Einzelbilder mit Playwright und Chromium, Bild für Bild mit fester Zeit |
| `make_video.py` | Fügt Bilder, Ton und Kapitelmarken zur MP4-Datei zusammen |

Die Ergebnisse landen in `out/` (nicht im Repository): `Stimmapparat_Erklaervideo.mp4`, `untertitel.srt`, `untertitel.vtt`, `tonspur.wav`.

## Neu erzeugen

Voraussetzungen: Python 3.10+, Node.js 18+, Playwright mit Chromium.

```bash
python -m venv venv && venv/bin/pip install piper-tts numpy scipy imageio-ffmpeg
# Deutsche Piper-Stimme (Kerstin, weiblich) herunterladen und entpacken:
curl -L -o kerstin.tgz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-kerstin-low.tar.gz
mkdir -p voices/kerstin-low && tar xzf kerstin.tgz -C voices/kerstin-low

venv/bin/python build_audio.py --voice-dir voices          # Ton, Zeitleiste, Untertitel
node render.mjs                                            # alle Bilder (dauert, CPU-Rendering)
node render.mjs --at 40,140,236                            # nur Kontrollbilder
venv/bin/python make_video.py                              # MP4 mit Kapitelmarken
```

`render.mjs` lädt Three.js und die Schriften normalerweise aus dem Netz. Ohne Netzzugang kannst du lokale Kopien übergeben: `--three pfad/three.min.js` (r128) und `--fonts ordner` mit den `@fontsource`-Paketen `bricolage-grotesque`, `atkinson-hyperlegible`, `jetbrains-mono` und `noto-sans`. Mit `--from` und `--to` lässt sich das Rendering auf mehrere Prozesse verteilen.

**Anpassen:** Text in `script.json` ändern und alle drei Schritte erneut ausführen. Für eine männliche Stimme `"voice": "de-thorsten-low"` setzen und die Stimme entsprechend herunterladen.

## Hinweise

- Die Sprecherstimme ist synthetisch (Piper, Stimme „Kerstin“). Formantwerte, Proportionen und Zeitabläufe des Modells sind für die Lehre vereinfacht.
- Die Stimmlippenschwingung wird verlangsamt gezeigt, wie bei einer Stroboskopie.
