#!/usr/bin/env python3
"""Genera le fiabe in stories/ con la voce ElevenLabs 'fausto bedtime stories'."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import urllib.request
import urllib.error

BASE = Path(__file__).resolve().parent
AUDIO = BASE / "audio"
LANG = "it"
VOICE_ID = "ZcI3lqwa2V77372zvT4W"
MODEL = "eleven_multilingual_v2"
API = "https://api.elevenlabs.io/v1/text-to-speech"

STORIES = sorted((BASE / "stories").glob("0*.md"))

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]"
)

def clean_text(text: str) -> str:
    text = EMOJI_RE.sub("", text)
    text = re.sub(r"\*([^*\n]+)\*", r"\1", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def load_story(md_path: Path) -> str:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#") or s == "---":
            continue
        if s.startswith("*") and s.endswith("*"):
            continue
        out.append(s)
    return clean_text(" ".join(out))

def split_chunks(text: str, max_chars: int = 480) -> list[str]:
    """ElevenLabs handles long text well — bigger chunks than XTTS."""
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
            while len(s) > max_chars:
                cut = max(s.rfind(",", 0, max_chars), max_chars // 2)
                chunks.append(s[:cut].strip())
                s = s[cut:].strip()
            cur = s
    if cur:
        chunks.append(cur)
    return chunks

def generate_chunk(text: str, api_key: str, out_path: Path, voice_settings: dict) -> bool:
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": voice_settings,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{API}/{VOICE_ID}",
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            audio_data = resp.read()
            out_path.write_bytes(audio_data)
            return True
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {err_body[:200]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return False

def main():
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        # Try loading from .env
        env_file = BASE / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ELEVENLABS_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    if not api_key:
        print("ERROR: No ELEVENLABS_API_KEY found", file=sys.stderr)
        sys.exit(1)

    os.makedirs(AUDIO, exist_ok=True)

    # Bedtime storytelling voice settings
    voice_settings = {
        "stability": 0.55,
        "similarity_boost": 0.80,
        "style": 0.35,
        "use_speaker_boost": True,
    }

    for index, md in enumerate(STORIES, start=1):
        key = f"{index:02d}"
        fname = md.name
        text = load_story(md)
        chunks = split_chunks(text)
        name = re.sub(r"^\d+", "", md.stem)
        print(f"\n[{key}] {fname}: {len(chunks)} chunks, {len(text)} chars", flush=True)

        wav_files = []
        for i, ch in enumerate(chunks):
            out = AUDIO / f"chunk_{key}_{i:03d}.mp3"
            if out.exists() and out.stat().st_size > 1000:
                print(f"  [{key}] reuse chunk {i+1}/{len(chunks)}", flush=True)
            else:
                print(f"  [{key}] generating chunk {i+1}/{len(chunks)} ...", flush=True)
                ok = generate_chunk(ch, api_key, out, voice_settings)
                if not ok:
                    print(f"  [{key}] FAILED on chunk {i+1}, retrying once ...", flush=True)
                    ok = generate_chunk(ch, api_key, out, voice_settings)
                    if not ok:
                        print(f"  [{key}] FAILED permanently on chunk {i+1}", file=sys.stderr)
                        sys.exit(1)
            wav_files.append(out)

        # Concatenate chunks with ffmpeg, adding 0.6s silence between each
        concat_list = AUDIO / f"concat_{key}.txt"
        with open(concat_list, "w") as fh:
            for w in wav_files:
                fh.write(f"file '{w.resolve()}'\n")
                fh.write("file 'silence.wav'\n")

        # Generate silence file
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
             "-t", "0.6", "-c:a", "pcm_s16le", str(AUDIO / "silence.wav")],
            check=True,
        )

        # build.py cerca audio/11l-<NN>-*.mp3: generiamo già con quel nome
        final = AUDIO / f"11l-{key}-{name}.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "concat", "-safe", "0", "-i", str(concat_list),
             "-c:a", "libmp3lame", "-b:a", "192k",
             str(final)],
            check=True,
        )

        # Clean up chunks
        for w in wav_files:
            try:
                w.unlink()
            except OSError:
                pass
        try:
            concat_list.unlink()
        except OSError:
            pass

        # Verify
        dur = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_format", str(final)],
            capture_output=True, text=True,
        ).stdout
        dur_match = re.search(r"duration=(\S+)", dur)
        dur_val = float(dur_match.group(1)) if dur_match else 0
        size = final.stat().st_size
        print(f"  -> {final.name} ({dur_val:.1f}s, {size/1024:.0f} KB)", flush=True)

        # Copy to Desktop
        desktop = Path("/mnt/c/Users/Deckard/Desktop/fiabe-audio")
        desktop.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final, desktop / final.name)
        print(f"  -> copied to Desktop", flush=True)

    # Clean up silence file
    try:
        (AUDIO / "silence.wav").unlink()
    except OSError:
        pass

    print(f"\nDone. {len(STORIES)} stories generated.", flush=True)

    # Send via Telegram
    for index, md in enumerate(STORIES, start=1):
        key = f"{index:02d}"
        name = re.sub(r"^\d+", "", md.stem)
        mp3 = AUDIO / f"11l-{key}-{name}.mp3"
        if mp3.exists():
            for attempt in range(5):
                result = subprocess.run(
                    ["hermes", "send", "-t", "telegram:8375916874",
                     f"🌙 Fiaba {key} pronta: MEDIA:{mp3}"],
                    capture_output=True, text=True,
                )
                if result.returncode == 0:
                    print(f"  Sent {mp3.name} via Telegram", flush=True)
                    break
                print(f"  Telegram retry {attempt+1} ...", flush=True)
                import time; time.sleep(3)

if __name__ == "__main__":
    main()
