# Stimmapparat 3D

Interaktives Lernmodell, das zeigt, wie Stimme und Sprechen beim Menschen entstehen. Die Datei `index.html` läuft ohne Build-Schritt direkt im Browser. Three.js r128 wird von cdnjs geladen.

## Die vier Stufen

| Stufe | Rolle | Was das Modell zeigt |
|---|---|---|
| 1 Atmung | Energiequelle | Lungen, Zwerchfell und Brustkorb bewegen sich im Atemzyklus. Umschaltbar zwischen Ruhe- und Sprechatmung. Diagramm von Lungenvolumen und subglottischem Druck. |
| 2 Stimmlippen | Schallquelle | Verformbare Stimmlippen mit Randkantenverschiebung (untere Kante eilt voraus), Stellknorpel öffnen und schließen die Glottis. Stroboskopische Zeitlupe, Kehlkopfspiegel-Ansicht und Glottis-Luftstrom (Rosenberg-Puls). |
| 3 Resonanz | Filter | Ansatzrohr als Röhre mit veränderlicher Querschnittsfläche. Spektrum aus Quelle × Filter = Ergebnis, Formanten F1–F3, Vokalviereck, stehende Wellen im Rohr (Näherung als gleichförmiges Rohr, Resonanzen je nach Rohrlänge der gewählten Stimme). |
| 4 Artikulation | Lautbildung | Zunge, Lippen, Unterkiefer und Gaumensegel. Alle Vokale und Konsonanten des Deutschen als IPA-Tabelle, jeweils mit 3D-Stellung und hörbarer Silbe. |

## Bedienung

- Ziehen dreht das Modell, Mausrad oder Pinch zoomt, ein Klick auf ein Organ zeigt eine Erklärung.
- **Ton an** startet die Klangsynthese (Quelle-Filter-Modell mit Web Audio). Tonhöhe und Lautstärke (subglottischer Druck) wirken live auf Modell, Diagramme und Klang.
- **Stimme** ist standardmäßig eine Frauenstimme (Grundfrequenz um 210 Hz, Formanten etwa 17 % höher als bei Männern, entsprechend einem Ansatzrohr von rund 15 cm, etwas behauchter Klang). Umschaltbar auf Mann (115 Hz) oder Kind (300 Hz).
- Tasten 1–4 wechseln die Stufe, die Leertaste hält die Animation an.

## Vereinfachungen

Proportionen, Formantwerte (deutsche Vokale, Männerwerte als Basis, für Frauen- und Kinderstimme hochskaliert) und Zeitabläufe sind gerundet. Die Stimmlippenschwingung wird verlangsamt dargestellt, der Klang ist synthetisch.
