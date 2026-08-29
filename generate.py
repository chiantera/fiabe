#!/usr/bin/env python3
"""Genera le fiabe in stories/ con la voce clonata (Coqui XTTS-v2)."""
import re
import shutil
import subprocess
import sys
import os
from pathlib import Path

from TTS.api import TTS

REF_WAV = "ref/reference.wav"
BASE = Path(__file__).resolve().parent
AUDIO = BASE / "audio"
TMP = BASE / "chunks"
LANG = "it"

STORIES = sorted((BASE / "stories").glob("0*.md"))

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]"
)

def clean_text(text: str) -> str:
    # rimuove emoji
    text = EMOJI_RE.sub("", text)
    # rimuove i marcatori corsivo *parola*
    text = re.sub(r"\*([^*\n]+)\*", r"\1", text)
    # rimuove spazi doppi residui
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def load_story(md_path: Path) -> str:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("*") and s.endswith("*"):
            continue  # sottotitolo corsivo
        if s == "---":
            continue
        out.append(s)
    return clean_text(" ".join(out))

def split_chunks(text: str, max_chars: int = 190) -> list[str]:
    # spezza in frasi, poi raggruppa in chunk <= max_chars
    sentences = re.split(r"(?<=[.!?…])\s+", text)
    sentences = [s for s in sentences if s.strip()]
    chunks = []
    cur = ""
    for s in sentences:
        if len(cur) + len(s) + 1 <= max_chars:
            cur = (cur + " " + s).strip() if cur else s
        else:
            if cur:
                chunks.append(cur)
            # se una singola frase eccede, taglia sulle virgole
            while len(s) > max_chars:
                cut = max(s.rfind(",", 0, max_chars), max_chars // 2)
                chunks.append(s[:cut].strip())
                s = s[cut:].strip()
            cur = s
    if cur:
        chunks.append(cur)
    return chunks

def main():
    os.makedirs(AUDIO, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)

    print("Caricamento modello XTTS-v2 ...", flush=True)
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    print("Modello caricato.", flush=True)

    for index, md in enumerate(STORIES, start=1):
        key = f"{index:02d}"
        fname = md.name
        text = load_story(md)
        chunks = split_chunks(text)
        print(f"[{key}] {fname}: {len(chunks)} chunk, {len(text)} char", flush=True)

        wav_files = []
        for i, ch in enumerate(chunks):
            out = TMP / f"{key}_{i:03d}.wav"
            tts.tts_to_file(
                text=ch,
                speaker_wav=REF_WAV,
                language=LANG,
                file_path=str(out),
                speed=1.0,
            )
            wav_files.append(out)
            if (i + 1) % 10 == 0:
                print(f"  [{key}] {i+1}/{len(chunks)}", flush=True)

        # concatena i chunk con 0.35s di pausa
        concat = TMP / f"{key}_concat.txt"
        with open(concat, "w", encoding="utf-8") as fh:
            for w in wav_files:
                fh.write(f"file '{w.resolve()}'\n")
                fh.write("file 'silence.wav'\n")

        # genera un silenzio di 0.35s
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", "0.35", "-c:a", "pcm_s16le", str(TMP / "silence.wav")],
            check=True,
        )

        name = re.sub(r"^\d+", "", md.stem)
        final = AUDIO / f"11l-{key}-{name}.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "concat", "-safe", "0", "-i", str(concat),
             "-ar", "44100", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "160k",
             str(final)],
            check=True,
        )
        print(f"  -> {final}", flush=True)

    # copia anche sul Desktop Windows
    desktop = Path("/mnt/c/Users/Deckard/Desktop/fiabe-audio")
    desktop.mkdir(parents=True, exist_ok=True)
    for mp3 in sorted(AUDIO.glob("*.mp3")):
        shutil.copy2(mp3, desktop / mp3.name)
    print(f"Copiati anche in {desktop}", flush=True)

    print("Fatto.")


if __name__ == "__main__":
    main()
