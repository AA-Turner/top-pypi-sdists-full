"""Deterministic file naming — the ``prompt_slug_hash`` strategy of the placement registry.

Moved down from ``matrx_ai.media.naming`` (2026-10-30) so the one resolver
(:mod:`matrx_files.placement`) can name files without importing matrx-ai, which
depends on this package. ``matrx_ai.media.naming`` re-exports :func:`slugify_prompt`.

Names have the shape ``<slug>-<8-char-uniquifier>``; the uniquifier is a
content-hash prefix, so retries of the same bytes collapse to the same name.
"""

from __future__ import annotations

import hashlib
import re

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


__all__ = ["slugify_prompt", "strip_to_words", "uniquifier"]

strip_to_words = _strip_to_words
uniquifier = _uniquifier
