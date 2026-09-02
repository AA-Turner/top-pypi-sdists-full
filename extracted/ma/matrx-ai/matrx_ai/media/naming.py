"""Filename generation for AI-produced media.

UUIDs make terrible filenames — they tell the user nothing about what's
in the file and break any "download → see this in your file manager"
flow. This module produces descriptive filenames from the prompt that
generated the media, with a short uniquifier to prevent collisions.

Two tiers of naming:

1. :func:`slugify_prompt` — deterministic, dependency-free, fast.
   Takes the first 4–6 meaningful words from the prompt, kebab-cases
   them. ALWAYS works (no LLM call, no network). The default.

2. :func:`ai_filename_async` — optional LLM-driven naming. Uses a small
   fast model (gpt-4o-mini or whatever the host configures) to produce
   a more semantically meaningful filename. Costs ~$0.0001 per call +
   ~500ms latency. Falls back to the deterministic slugifier on any
   error so we never break a generation flow because the namer hiccuped.

Both produce paths in the form ``<slug>-<8-char-uniquifier>.<ext>``.
The uniquifier is a content-hash prefix (deterministic for the same
bytes) so retries of the same generation collapse to the same filename.
"""

from __future__ import annotations

import hashlib
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# Tokens stripped from prompts before slugifying — common conversational
# scaffolding that shouldn't make it into a filename.
_STOP_WORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "the",
        "of",
        "in",
        "on",
        "at",
        "to",
        "for",
        "with",
        "and",
        "or",
        "but",
        "if",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "shall",
        "can",
        "this",
        "that",
        "these",
        "those",
        "i",
        "you",
        "he",
        "she",
        "it",
        "we",
        "they",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "their",
        "me",
        "him",
        "us",
        "them",
        "please",
        "create",
        "generate",
        "make",
        "draw",
        "show",
        "render",
        "produce",
        "give",
        "output",
        "image",
        "picture",
        "photo",
        "photograph",
        "illustration",
        "video",
        "clip",
        "audio",
        "sound",
        "voice",
    }
)


_MAX_WORDS = 6
_UNIQUIFIER_LEN = 8


def _strip_to_words(text: str) -> list[str]:
    """Lowercase + strip → meaningful word tokens (no punctuation, no stops)."""
    if not text:
        return []
    # Replace non-alphanumeric with spaces; collapse whitespace.
    cleaned = re.sub(r"[^a-zA-Z0-9]+", " ", text.lower()).strip()
    if not cleaned:
        return []
    return [w for w in cleaned.split() if w and w not in _STOP_WORDS]


def _uniquifier(content: bytes | None, *, fallback_seed: str = "") -> str:
    """8-char content-hash prefix for filename uniqueness.

    Deterministic for the same bytes — retries of the same generation
    collapse to the same filename, which plays nicely with
    content-hash dedup.
    """
    if content is not None:
        return hashlib.sha256(content).hexdigest()[:_UNIQUIFIER_LEN]
    seed = (fallback_seed or "").encode("utf-8", errors="ignore")
    return hashlib.sha256(seed).hexdigest()[:_UNIQUIFIER_LEN]


def slugify_prompt(
    prompt: str | None,
    *,
    content_bytes: bytes | None = None,
    fallback: str = "ai-media",
    max_words: int = _MAX_WORDS,
) -> str:
    """Deterministic prompt → kebab-case filename slug.

    Returns ``<slug>-<8-char-hash>`` (extension is added by the caller
    based on mime type). When the prompt is empty/None, returns
    ``<fallback>-<8-char-hash>``.

    Examples:
        >>> slugify_prompt("A sunset over the Rocky Mountains")
        'sunset-over-rocky-mountains-a1b2c3d4'
        >>> slugify_prompt(None)
        'ai-media-xxxxxxxx'
    """
    words = _strip_to_words(prompt or "")
    slug_words = words[:max_words] if words else [fallback]
    slug = "-".join(slug_words)
    if not slug:
        slug = fallback
    unique = _uniquifier(content_bytes, fallback_seed=prompt or "")
    return f"{slug}-{unique}"


async def ai_filename_async(
    prompt: str | None,
    *,
    content_bytes: bytes | None = None,
    fallback: str = "ai-media",
    naming_callable=None,
) -> str:
    """LLM-driven filename — falls back to ``slugify_prompt`` on failure.

    ``naming_callable`` is an optional async callable
    ``async (prompt: str) -> str | None`` the host injects to produce a
    semantically-richer filename (e.g. wraps the conversation-labeler
    agent or a dedicated small-prompt agent). When None or any error,
    we use the deterministic slugifier.

    The LLM result is sanitized through the same slug rules so a
    misbehaving model can't produce a path-traversal payload.
    """
    if not prompt:
        return slugify_prompt(None, content_bytes=content_bytes, fallback=fallback)

    raw: str | None = None
    if naming_callable is not None:
        try:
            raw = await naming_callable(prompt)
        except Exception:
            raw = None

    if raw:
        words = _strip_to_words(raw)
        if words:
            slug = "-".join(words[:_MAX_WORDS])
            unique = _uniquifier(content_bytes, fallback_seed=prompt)
            return f"{slug}-{unique}"

    return slugify_prompt(prompt, content_bytes=content_bytes, fallback=fallback)


__all__ = [
    "slugify_prompt",
    "ai_filename_async",
]
