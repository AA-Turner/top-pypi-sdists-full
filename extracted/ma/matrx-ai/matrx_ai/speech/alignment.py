"""Word alignment from vendor character timestamps.

ElevenLabs returns per-character start/end times on its ``with-timestamps``
endpoints (and, for Text-to-Dialogue, voice segments per input turn). The audio
output part carries the WORD view — what a karaoke highlight, a caption track,
or a "jump to this line" control needs — plus the voice segments.

Inline performance markup (``[warm]`` audio tags, ``<break .../>`` SSML) is
spoken as nothing, so it never becomes a word.
"""

from __future__ import annotations

import re
from typing import Any

__all__ = ["alignment_to_words", "merge_timelines"]

_MARKUP = re.compile(r"\[[^\]]*\]|<[^>]*>")


def _alignment_of(response: Any) -> tuple[list[str], list[float], list[float]]:
    alignment = getattr(response, "alignment", None)
    if alignment is None:
        return [], [], []
    return (
        list(getattr(alignment, "characters", None) or []),
        [float(v) for v in getattr(alignment, "character_start_times_seconds", None) or []],
        [float(v) for v in getattr(alignment, "character_end_times_seconds", None) or []],
    )


def merge_timelines(segments: list[tuple[Any, str | None]]) -> dict[str, list[Any]]:
    """Concatenate several timestamped responses onto one timeline.

    Each later response is offset by where the previous one ended, matching the
    concatenated audio. ``voice_id`` names the voice of a single-voice response;
    a dialogue response brings its own voice segments.
    """
    characters: list[tuple[str, float, float]] = []
    voice_segments: list[dict[str, Any]] = []
    offset = 0.0
    for index, (response, voice_id) in enumerate(segments):
        chars, starts, ends = _alignment_of(response)
        for char, start, end in zip(chars, starts, ends, strict=False):
            characters.append((char, start + offset, end + offset))
        native = getattr(response, "voice_segments", None) or []
        if native:
            for seg in native:
                voice_segments.append(
                    {
                        "voice_id": getattr(seg, "voice_id", None),
                        "turn_index": getattr(seg, "dialogue_input_index", None),
                        "start_ms": round((float(seg.start_time_seconds) + offset) * 1000),
                        "end_ms": round((float(seg.end_time_seconds) + offset) * 1000),
                    }
                )
        elif ends:
            voice_segments.append(
                {
                    "voice_id": voice_id,
                    "turn_index": index,
                    "start_ms": round(offset * 1000),
                    "end_ms": round((ends[-1] + offset) * 1000),
                }
            )
        if ends:
            offset += ends[-1]
    return {"characters": characters, "voice_segments": voice_segments}


def alignment_to_words(characters: list[tuple[str, float, float]]) -> list[dict[str, Any]]:
    """Group a character timeline into words, dropping markup and whitespace."""
    text = "".join(c for c, _, _ in characters)
    hidden = [False] * len(text)
    for match in _MARKUP.finditer(text):
        for i in range(match.start(), match.end()):
            hidden[i] = True
    words: list[dict[str, Any]] = []
    current: list[int] = []

    def flush() -> None:
        if not current:
            return
        word = "".join(characters[i][0] for i in current)
        words.append(
            {
                "text": word,
                "start_ms": round(characters[current[0]][1] * 1000),
                "end_ms": round(characters[current[-1]][2] * 1000),
            }
        )
        current.clear()

    for i, (char, _, _) in enumerate(characters):
        if hidden[i] or char.isspace():
            flush()
            continue
        current.append(i)
    flush()
    return words
