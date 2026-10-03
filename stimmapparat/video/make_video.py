#!/usr/bin/env python3
"""Fügt Einzelbilder, Tonspur und Kapitelmarken zu einer MP4-Datei zusammen.

Aufruf: python make_video.py [--out OUT] [--name Stimmapparat_Erklaervideo]
Benötigt imageio-ffmpeg (bringt ein ffmpeg mit libx264 mit) oder ein ffmpeg im PATH.
"""
import argparse, json, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return shutil.which("ffmpeg")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--name", default="Stimmapparat_Erklaervideo")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--crf", type=int, default=20)
    a = ap.parse_args()
    tl = json.load(open(os.path.join(a.out, "timeline.json"), encoding="utf-8"))

    meta = os.path.join(a.out, "kapitel.ffmeta")
    with open(meta, "w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        f.write(f"title={tl['title']} – {tl['subtitle']}\nlanguage=deu\n")
        for s in tl["scenes"]:
            start = 0 if s is tl["scenes"][0] else s["start"]
            f.write(f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(start * 1000)}\nEND={int(s['end'] * 1000)}\n")
            label = f"{s['num']}. {s['label']}" if s.get("num") else s["label"]
            f.write(f"title={label}\n")

    mp4 = os.path.join(a.out, a.name + ".mp4")
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-stats",
           "-framerate", str(a.fps), "-i", os.path.join(a.out, "frames", "%05d.jpg"),
           "-i", os.path.join(a.out, "tonspur.wav"),
           "-i", meta, "-map_metadata", "2", "-map_chapters", "2",
           "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-tune", "animation",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
           "-metadata:s:a:0", "language=deu", "-movflags", "+faststart", "-shortest", mp4]
    subprocess.run(cmd, check=True)
    poster = os.path.join(a.out, a.name + "_Vorschau.jpg")
    subprocess.run([ffmpeg_exe(), "-y", "-loglevel", "error", "-ss", "21", "-i", mp4, "-frames:v", "1", "-q:v", "2", poster], check=True)
    print(f"{mp4}  ({os.path.getsize(mp4) / 1e6:.1f} MB)")

if __name__ == "__main__":
    main()
