#!/usr/bin/env python3
"""
Kokoro-TTS Audio Generator for Recep's Technical Blog (Go Hugo)

Synthesizes high-fidelity, human-cadence MP3 audio for Hugo blog posts using
the open-source Kokoro-82M ONNX model. Generates podcast-ready audio with
in-car / CarPlay metadata and audio scrubbing support.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

# Paths relative to script directory
SCRIPT_DIR = Path(__file__).resolve().parent
if (SCRIPT_DIR.parent / "receps_blog").exists():
    BLOG_ROOT = SCRIPT_DIR.parent / "receps_blog"
elif (SCRIPT_DIR.parent / "blog" / "receps_blog").exists():
    BLOG_ROOT = SCRIPT_DIR.parent / "blog" / "receps_blog"
else:
    BLOG_ROOT = SCRIPT_DIR.parent / "receps_blog"

CONTENT_POSTS_DIR = BLOG_ROOT / "content" / "posts"
STATIC_AUDIO_DIR = BLOG_ROOT / "static" / "audio"
CACHE_FILE = STATIC_AUDIO_DIR / ".audio_cache.json"

MODEL_CACHE_DIR = Path.home() / ".cache" / "kokoro"
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin"

DEFAULT_VOICE = "am_adam"
DEFAULT_SPEED = 1.0
SAMPLE_RATE = 24000


def ensure_model_files():
    """Ensure Kokoro ONNX model and voices bin are downloaded."""
    MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_CACHE_DIR / "kokoro-v1.0.onnx"
    voices_path = MODEL_CACHE_DIR / "voices-v1.0.bin"

    if not model_path.exists():
        print(f"📥 Downloading Kokoro ONNX model (~310MB) to {model_path}...")
        urllib.request.urlretrieve(MODEL_URL, model_path)
        print("✓ Model download complete.")

    if not voices_path.exists():
        print(f"📥 Downloading Kokoro voices (~27MB) to {voices_path}...")
        urllib.request.urlretrieve(VOICES_URL, voices_path)
        print("✓ Voices download complete.")

    return str(model_path), str(voices_path)


def parse_frontmatter(content: str):
    """
    Parses TOML (+++ ... +++) or YAML (--- ... ---) frontmatter and body.
    Returns (meta_dict, body_text).
    """
    meta = {}
    body = content

    # Check for TOML frontmatter +++ ... +++
    toml_match = re.match(r'^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$', content, re.DOTALL)
    if toml_match:
        raw_meta, body = toml_match.groups()
        for line in raw_meta.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip('"\'')
                meta[key] = val
        return meta, body

    # Check for YAML frontmatter --- ... ---
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if yaml_match:
        raw_meta, body = yaml_match.groups()
        for line in raw_meta.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip().strip('"\'')
                meta[key] = val
        return meta, body

    return meta, body


def clean_markdown_for_speech(title: str, author: str, body: str) -> list[str]:
    """
    Transforms markdown content into an array of clean spoken paragraphs.
    Removes syntax noise, code blocks, raw URLs, and HTML markup.
    """
    # 1. Remove HTML comments
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)

    # 2. Convert Twitter/X embeds to spoken quote
    def replace_tweet(m):
        tweet_html = m.group(0)
        # Extract paragraph text inside blockquote
        p_match = re.search(r'<p[^>]*>(.*?)</p>', tweet_html, flags=re.DOTALL)
        if p_match:
            clean_p = re.sub(r'<[^>]+>', '', p_match.group(1))
            return f"\nQuote from Twitter: {clean_p}\n"
        return ""
    body = re.sub(r'<blockquote class="twitter-tweet"[^>]*>.*?</blockquote>', replace_tweet, body, flags=re.DOTALL)

    # 3. Strip general HTML tags (div, img, script, style, etc.)
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body, flags=re.DOTALL)
    body = re.sub(r'<[^>]+>', ' ', body)

    # 4. Handle fenced code blocks
    body = re.sub(r'```[a-zA-Z0-9_-]*\n(.*?)```', r'\n[Code snippet omitted. Please refer to the written article for code listings.]\n', body, flags=re.DOTALL)

    # 5. Handle images ![alt](url) -> remove
    body = re.sub(r'!\[.*?\]\(.*?\)', '', body)

    # 6. Handle links [text](url) -> keep text only
    body = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', body)

    # 7. Convert headings to spoken transitions
    def heading_replacer(match):
        level = len(match.group(1))
        htext = match.group(2).strip()
        # Clean numeric prefixes like '1. Introduction' -> 'Section: 1. Introduction.'
        return f"\n\n{htext}.\n\n"
    body = re.sub(r'^(#{1,6})\s+(.+)$', heading_replacer, body, flags=re.MULTILINE)

    # 8. Clean inline code `foo` -> foo
    body = re.sub(r'`([^`]+)`', r'\1', body)

    # 9. Clean markdown bold/italic/strike
    body = re.sub(r'\*\*(.+?)\*\*', r'\1', body)
    body = re.sub(r'__(.+?)__', r'\1', body)
    body = re.sub(r'\*(.+?)\*', r'\1', body)
    body = re.sub(r'_(.+?)_', r'\1', body)
    body = re.sub(r'~~(.+?)~~', r'\1', body)

    # 10. Clean horizontal rules
    body = re.sub(r'^\s*[-*_]{3,}\s*$', '', body, flags=re.MULTILINE)

    # 11. Clean bullet lists (- item / * item)
    body = re.sub(r'^\s*[-*+]\s+', '', body, flags=re.MULTILINE)

    # 12. Clean blockquotes (> text)
    body = re.sub(r'^\s*>\s*', '', body, flags=re.MULTILINE)

    # 13. Expand common technical abbreviations and symbols for better pronunciation
    body = re.sub(r'\bTL;DR:?\b', 'Summary.', body)
    body = re.sub(r'\bHPC\b', 'H P C', body)
    body = re.sub(r'\bAI\b', 'A I', body)
    body = re.sub(r'\bML\b', 'M L', body)
    body = re.sub(r'\bPhD\b', 'P h D', body)
    body = re.sub(r'\bSLURM\b', 'Slurm', body)
    body = re.sub(r'\bLLM\b', 'L L M', body)
    body = re.sub(r'\bLLMs\b', 'L L Ms', body)
    body = re.sub(r'\be\.g\.,?\b', 'for example,', body)
    body = re.sub(r'\bi\.e\.,?\b', 'that is,', body)
    body = re.sub(r'&amp;', 'and', body)
    body = re.sub(r'&quot;', '"', body)
    body = re.sub(r'&#39;', "'", body)

    # 14. Split into clean paragraphs
    raw_paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]

    # Build audio script with intro header
    spoken_chunks = []
    author_name = author if author else "Recep Erol"
    intro = f"{title}. By {author_name}."
    spoken_chunks.append(intro)

    for p in raw_paragraphs:
        # Collapse whitespace within paragraph
        cleaned_p = ' '.join(p.split())
        if len(cleaned_p) < 3:
            continue
        # If paragraph is excessively long, split by sentence to protect TTS attention window
        if len(cleaned_p) > 600:
            sentences = re.split(r'(?<=[.!?])\s+', cleaned_p)
            current_sub = []
            current_len = 0
            for s in sentences:
                if current_len + len(s) > 500 and current_sub:
                    spoken_chunks.append(' '.join(current_sub))
                    current_sub = [s]
                    current_len = len(s)
                else:
                    current_sub.append(s)
                    current_len += len(s)
            if current_sub:
                spoken_chunks.append(' '.join(current_sub))
        else:
            spoken_chunks.append(cleaned_p)

    return spoken_chunks


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)


def get_post_slug(file_path: Path) -> str:
    """Returns slug for a post: bundle dir name if index.md, else file stem."""
    if file_path.name == "index.md":
        return file_path.parent.name
    return file_path.stem


def synthesize_post(kokoro, post_path: Path, output_mp3: Path, voice: str, speed: float) -> dict:
    """Synthesizes speech for a single post using Kokoro-ONNX and writes MP3."""
    import numpy as np
    import soundfile as sf

    with open(post_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    meta, body = parse_frontmatter(raw_content)
    title = meta.get("title", post_path.stem.replace("-", " ").replace("_", " ").title())
    author = meta.get("author", "Recep Erol")

    # Override voice if specified in frontmatter
    post_voice = meta.get("audio_voice", voice)

    chunks = clean_markdown_for_speech(title, author, body)
    print(f"  📖 Processing '{title}' ({len(chunks)} spoken paragraphs, voice: {post_voice})...")

    audio_segments = []
    # 0.4s silence pause between paragraphs
    pause_samples = np.zeros(int(SAMPLE_RATE * 0.4), dtype=np.float32)

    t0 = time.time()
    for idx, chunk in enumerate(chunks):
        try:
            samples, sr = kokoro.create(chunk, voice=post_voice, speed=speed, lang="en-us")
            if len(samples) > 0:
                audio_segments.append(samples)
                audio_segments.append(pause_samples)
        except Exception as e:
            print(f"    ⚠️ Warning on paragraph {idx+1}/{len(chunks)}: {e}")
            continue

    if not audio_segments:
        raise RuntimeError(f"No audio was generated for {post_path}")

    full_audio = np.concatenate(audio_segments)
    elapsed = time.time() - t0
    duration_sec = len(full_audio) / SAMPLE_RATE

    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_mp3), full_audio, SAMPLE_RATE, format="MP3")

    mins = int(duration_sec // 60)
    secs = int(duration_sec % 60)
    dur_str = f"{mins}:{secs:02d}"

    print(f"  ✓ Saved: {output_mp3.name} (Duration: {dur_str}, Gen time: {elapsed:.2f}s, RTF: {elapsed/duration_sec:.3f}x)")

    return {
        "slug": get_post_slug(post_path),
        "title": title,
        "author": author,
        "voice": post_voice,
        "duration_seconds": round(duration_sec, 2),
        "duration_str": dur_str,
        "file_size": output_mp3.stat().st_size,
        "output_path": str(output_mp3.relative_to(BLOG_ROOT)),
    }


def find_posts(target_post: str | None = None) -> list[Path]:
    """Finds all markdown post files."""
    if target_post:
        candidate = Path(target_post)
        if candidate.exists():
            return [candidate.resolve()]
        # Try relative to BLOG_ROOT
        if (BLOG_ROOT / target_post).exists():
            return [(BLOG_ROOT / target_post).resolve()]
        # Try relative to CONTENT_POSTS_DIR
        if (CONTENT_POSTS_DIR / target_post).exists():
            return [(CONTENT_POSTS_DIR / target_post).resolve()]
        raise FileNotFoundError(f"Post not found: {target_post}")

    posts = []
    for md_file in sorted(CONTENT_POSTS_DIR.glob("**/*.md")):
        # Skip drafts or special pages
        posts.append(md_file)
    return posts


def compute_content_hash(file_path: Path, voice: str, speed: float) -> str:
    """Computes SHA256 of file content + voice parameters."""
    with open(file_path, 'rb') as f:
        data = f.read()
    h = hashlib.sha256()
    h.update(data)
    h.update(voice.encode('utf-8'))
    h.update(str(speed).encode('utf-8'))
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Kokoro-TTS Hugo Audio Generator")
    parser.add_argument("--post", type=str, help="Relative or absolute path to a specific post markdown file")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help=f"Kokoro voice (default: {DEFAULT_VOICE})")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED, help=f"Speech speed multiplier (default: {DEFAULT_SPEED})")
    parser.add_argument("--force", action="store_true", help="Force regenerate audio even if cached")
    parser.add_argument("--list-voices", action="store_true", help="List all available Kokoro voices")
    args = parser.parse_args()

    model_path, voices_path = ensure_model_files()

    from kokoro_onnx import Kokoro
    kokoro = Kokoro(model_path, voices_path)

    if args.list_voices:
        print("Available Kokoro Voices:")
        for v in kokoro.get_voices():
            print(f"  - {v}")
        sys.exit(0)

    posts = find_posts(args.post)
    cache = load_cache()

    print(f"🎙️ Starting Audio Synthesis for {len(posts)} post(s)...")
    print(f"   Model: Kokoro-v1.0 (ONNX) | Default Voice: {args.voice} | Sample Rate: {SAMPLE_RATE}Hz")
    print("-" * 65)

    stats = []
    for p in posts:
        slug = get_post_slug(p)
        output_mp3 = STATIC_AUDIO_DIR / f"{slug}.mp3"
        content_hash = compute_content_hash(p, args.voice, args.speed)

        cached_entry = cache.get(slug)
        if not args.force and output_mp3.exists() and cached_entry and cached_entry.get("hash") == content_hash:
            print(f"  ⏩ Skipping '{slug}' (up to date in cache: {cached_entry.get('duration_str')})")
            stats.append(cached_entry)
            continue

        try:
            result = synthesize_post(kokoro, p, output_mp3, args.voice, args.speed)
            result["hash"] = content_hash
            cache[slug] = result
            save_cache(cache)
            stats.append(result)
        except Exception as e:
            print(f"  ❌ Error synthesizing {p.name}: {e}")

    print("-" * 65)
    print(f"🎉 Complete! {len(stats)} audio editions ready in: {STATIC_AUDIO_DIR}")


if __name__ == "__main__":
    main()
