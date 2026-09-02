"""
LLM-to-TTS streaming pipeline.

Consumes an async stream of (token, voice_id) tagged tuples — e.g. from an
LLM that emits both reasoning tokens and content tokens — buffers them into
sentence-sized chunks per voice, and plays each chunk through ElevenLabs TTS
in real time (exactly like direct_dialogue.py), while also saving the full
audio to temp/audio/.

A voice change always forces a flush so the previous speaker finishes cleanly
before the next one begins.

Architecture:
  - The async LLM loop runs on the main asyncio event loop.
  - TTS conversion + playback runs in a dedicated background thread using the
    synchronous ElevenLabs client + elevenlabs.stream (play_stream), which is
    a blocking call that plays audio as bytes arrive.
  - A thread-safe queue.Queue bridges the two worlds.  The async side puts
    (text, voice_id) sentence chunks onto it; the thread drains it.

Usage:

    path = await play_and_save_tagged_stream(tagged_token_stream())
"""

from __future__ import annotations

import asyncio
import queue
import re
import threading
from collections.abc import AsyncGenerator, AsyncIterator
from datetime import datetime
from pathlib import Path

from elevenlabs import stream as play_stream
from elevenlabs.client import ElevenLabs

from matrx_ai._ext import get_ext
from matrx_ai.catalog.resolve import (
    resolve_tts_call_profile,
    resolve_tts_voice,
    validate_tts_voices,
)

_SENTENCE_ENDINGS = re.compile(r"[.!?…]\s*")
MIN_FLUSH_CHARS = 100  # don't flush until at least this many chars are buffered
MAX_BUFFER_CHARS = 300  # force-flush even without punctuation above this limit


def _audio_dir() -> Path:
    """The host's audio temp dir, resolved LAZILY at first use.

    Reading ``get_ext("settings")`` at import time made this module
    un-importable on a standalone install (ExtNotConfiguredError before any
    capability was requested). The package must import cleanly with no host.
    """
    path = get_ext("settings").temp_dir / "audio"
    path.mkdir(parents=True, exist_ok=True)
    return path

_SENTINEL = object()  # signals the TTS thread that the stream is done


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_sync_client() -> ElevenLabs:
    from dotenv import load_dotenv

    from matrx_ai.providers.keys import resolve_api_key

    load_dotenv()
    return ElevenLabs(api_key=resolve_api_key("ELEVENLABS_API_KEY"))


def _unique_audio_path(stem: str = "tts") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return _audio_dir() / f"{stem}_{timestamp}.mp3"


def _split_on_sentence_boundary(text: str, min_chars: int = MIN_FLUSH_CHARS) -> tuple[str, str]:
    """
    Return (chunk_to_flush, remainder), splitting at the last sentence-end
    that falls at or after ``min_chars``.  Returns ("", text) if no qualifying
    boundary exists yet.
    """
    matches = list(_SENTENCE_ENDINGS.finditer(text))
    # Only consider boundaries that end at or beyond the minimum
    qualifying = [m for m in matches if m.end() >= min_chars]
    if not qualifying:
        return "", text
    last = qualifying[-1]
    return text[: last.end()], text[last.end() :]


# ---------------------------------------------------------------------------
# TTS worker thread
# ---------------------------------------------------------------------------


def _tts_worker(
    chunk_queue: queue.Queue,
    model_id: str,
    collected: list[bytes],
) -> None:
    """
    Runs in a background thread.  Drains chunk_queue, calls ElevenLabs TTS
    for each (text, voice_id) pair, plays audio in real time via play_stream,
    and appends all bytes to `collected` for saving later.
    """
    client = _get_sync_client()

    while True:
        item = chunk_queue.get()
        if item is _SENTINEL:
            break

        text, voice_id = item
        text = text.strip()
        if not text:
            continue

        # print(f"  [TTS] converting {len(text)} chars (voice={voice_id[:8]}...)", flush=True)

        audio_stream = client.text_to_speech.stream(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
            optimize_streaming_latency=3,
        )

        chunk_bytes: list[bytes] = []

        def tee(source):
            for chunk in source:
                if isinstance(chunk, bytes) and chunk:
                    chunk_bytes.append(chunk)
                    yield chunk

        play_stream(tee(audio_stream))
        collected.extend(chunk_bytes)


# ---------------------------------------------------------------------------
# Primary pipeline
# ---------------------------------------------------------------------------


async def play_and_save_tagged_stream(
    tagged_stream: AsyncIterator[str | tuple[str, str]],
    *,
    model_ref: str,
    voice_id: str | None = None,
    cycle_voices: list[str] | None = None,
    stem: str = "tts",
) -> Path:
    """
    Consume a tagged token stream, play audio in real time, and save to file.

    Each item from ``tagged_stream`` may be either:
      - a plain ``str`` token          →  uses the next voice in the cycle
      - a ``(token, voice_id)`` tuple  →  uses the next voice in the cycle

    ``cycle_voices`` is an optional list of catalog-linked voice IDs to rotate
    through for every sentence chunk. If omitted, the catalog default voice
    for ``model_ref`` is used.

    Flushes to TTS at sentence boundaries and when the buffer exceeds
    MAX_BUFFER_CHARS.

    Returns the Path where the complete audio was saved.
    """
    profile = await resolve_tts_call_profile(model_ref)
    if profile.vendor != "elevenlabs":
        raise ValueError(
            f"ElevenLabs streaming requires an ElevenLabs catalog model; "
            f"{model_ref!r} resolved to vendor={profile.vendor!r}"
        )
    if cycle_voices:
        validate_tts_voices(profile, cycle_voices)
        voices = cycle_voices
    else:
        voices = [resolve_tts_voice(profile, voice_id)]
    cycle_index = 0

    def _current_voice() -> str:
        return voices[cycle_index % len(voices)]

    def _advance() -> None:
        nonlocal cycle_index
        cycle_index += 1

    chunk_queue: queue.Queue = queue.Queue()
    collected: list[bytes] = []

    worker = threading.Thread(
        target=_tts_worker,
        args=(chunk_queue, profile.provider_model_id, collected),
        daemon=True,
    )
    worker.start()

    loop = asyncio.get_running_loop()

    def enqueue(text: str, vid: str) -> None:
        if text.strip():
            chunk_queue.put((text, vid))

    buffer = ""

    async for item in tagged_stream:
        token = item[0] if isinstance(item, tuple) else item
        buffer += token

        chunk, remainder = _split_on_sentence_boundary(buffer)
        if not chunk and len(buffer) >= MAX_BUFFER_CHARS:
            chunk, remainder = buffer, ""

        if chunk:
            enqueue(chunk, _current_voice())
            _advance()
            buffer = remainder

    if buffer.strip():
        enqueue(buffer, _current_voice())

    chunk_queue.put(_SENTINEL)
    await loop.run_in_executor(None, worker.join)

    all_audio = b"".join(collected)
    path = _unique_audio_path(stem)
    path.write_bytes(all_audio)
    print(f"\nSaved {len(all_audio):,} bytes to {path}")
    return path


# ---------------------------------------------------------------------------
# Alias kept for backwards compat with test_huggingface.py
# ---------------------------------------------------------------------------


async def save_streamed_audio(
    tagged_stream: AsyncIterator[str | tuple[str, str]],
    *,
    model_ref: str,
    voice_id: str | None = None,
    cycle_voices: list[str] | None = None,
    stem: str = "tts",
) -> Path:
    return await play_and_save_tagged_stream(
        tagged_stream,
        model_ref=model_ref,
        voice_id=voice_id,
        cycle_voices=cycle_voices,
        stem=stem,
    )


# ---------------------------------------------------------------------------
# Demo helpers
# ---------------------------------------------------------------------------


async def _mock_tagged_stream(
    reasoning: str,
    content: str,
    voice_id: str,
    token_delay: float = 0.03,
) -> AsyncGenerator[tuple[str, str]]:
    for word in reasoning.split():
        yield (word + " ", voice_id)
        await asyncio.sleep(token_delay)
    for word in content.split():
        yield (word + " ", voice_id)
        await asyncio.sleep(token_delay)


if __name__ == "__main__":
    from matrx_utils import clear_terminal

    clear_terminal()

    async def _demo() -> None:
        reasoning = "Let me think about this carefully. The answer involves several steps."
        content = "The final answer is forty-two. I hope that helps!"
        model_ref = input("Catalog model or alias: ").strip()
        voice_id = input("Catalog-linked voice ID (blank for default): ").strip() or None
        profile = await resolve_tts_call_profile(model_ref)
        resolved_voice = resolve_tts_voice(profile, voice_id)
        path = await play_and_save_tagged_stream(
            _mock_tagged_stream(reasoning, content, resolved_voice),
            model_ref=model_ref,
            voice_id=resolved_voice,
            stem="demo_multi_voice",
        )
        print(f"Demo saved to: {path}")

    asyncio.run(_demo())
