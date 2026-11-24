"""What a customer's sentence may never contain: a model id, a model family, or a provider name.

THE ONE LIST (Arman, 2026-11-18: a free-plan customer read "gemini-2.5-pro-preview-tts needs a paid plan").
Every ``user_message`` we build is fixed text of ours; the model, the provider and the raw server words ride the
developer fields (``RetryableError.message`` / ``details``, the log, the admin record). This module only DETECTS
a leak, so a guard and the HTTP envelope backstop share one definition:

* :data:`PROVIDER_WORDS` - every provider name and model-family brand, defined once (the routing-key display
  table in ``errors.py`` feeds it, so a provider added there is covered here).
* :data:`MODEL_ID_SHAPE` - what a catalog model id looks like (``gpt-4o``, ``gemini-2.5-pro-preview-tts``).
* :func:`names_a_model_or_provider` - what the guards and the envelope backstop ask.

Guard: ``tests/test_server_messages_never_name_a_model_or_provider.py``.
"""

from __future__ import annotations

import re

from matrx_ai.providers.errors import _PROVIDER_DISPLAY_NAMES

#: Brands a person must not read in an error sentence: every provider's key and display name, plus the model
#: families and products they are known by.
PROVIDER_WORDS: tuple[str, ...] = tuple(
    sorted(
        {
            *(k for k in _PROVIDER_DISPLAY_NAMES),
            *(v for v in _PROVIDER_DISPLAY_NAMES.values()),
            "gemini", "claude", "gpt", "chatgpt", "llama", "mistral", "mixtral", "deepseek", "qwen", "grok",
            "kimi", "sonnet", "opus", "haiku", "vertex", "bedrock", "azure", "perplexity", "sonar", "whisper",
            "imagen", "veo", "lyria", "sora", "flux", "dall-e", "hume", "deepgram", "assemblyai", "gpt-oss",
        },
        key=str.lower,
    )
)

_WORDS = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(w) for w in PROVIDER_WORDS) + r")(?![A-Za-z])", re.I)

#: ``family-2.5-pro-preview``, ``gpt-4o``, ``o1-mini``, ``llama-3.1-70b-instruct``, ``org/model-name``.
MODEL_ID_SHAPE = re.compile(
    r"\b(?:[A-Za-z][A-Za-z0-9]*[-_/])+[A-Za-z0-9.]*\d[A-Za-z0-9.]*(?:[-_][A-Za-z0-9.]+)*\b"
    r"|\b(?:gpt|claude|gemini|llama|grok|sonar)[-_ ]?\d[\w.\-]*\b"
    r"|\bo\d(?:-(?:mini|pro|preview|high|low))?\b",
    re.I,
)


def names_a_model_or_provider(text: str | None) -> str | None:
    """The first model id or provider word in ``text`` (for a guard to quote), or None when it is clean."""
    if not text:
        return None
    hit = _WORDS.search(text) or MODEL_ID_SHAPE.search(text)
    return hit.group(0) if hit else None
