"""Filename generation for AI-produced media.

The deterministic slugifier lives in :mod:`matrx_files.naming` (the placement
registry's ``prompt_slug_hash`` strategy) and is re-exported here.
:func:`ai_filename_async` takes a host-injected naming callable; the platform's
AI naming runs through the ``files.name_generated_file`` mandate once approved.
"""

from __future__ import annotations

from matrx_files.naming import _MAX_WORDS, slugify_prompt
from matrx_files.naming import strip_to_words as _strip_to_words
from matrx_files.naming import uniquifier as _uniquifier


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
