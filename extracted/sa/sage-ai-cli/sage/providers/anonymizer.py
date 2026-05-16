"""Cloud-AI request anonymizer.

Sage's privacy posture: when a user's prompt is sent to a cloud AI provider
(OpenRouter, Groq, Together, etc.), the provider must NEVER receive anything
that could identify the end user.

This module is the chokepoint. Every payload going to a non-local provider
passes through `anonymize_payload()`, which:

  1. Strips any top-level field that could carry user identity
     (`user`, `metadata`, `identity`, `email`, `uid`, `customer_id`, etc.).
     OpenAI's API supports a `user` field for end-user tracking — we
     deliberately drop it so providers can't correlate prompts to a person.

  2. Scrubs message content of obvious PII (email addresses, US-format
     phone numbers) before transmission. Best-effort — code-heavy prompts
     stay legible because we only target strict formats, not bare digits.

  3. Local providers (ollama, llama-cpp) skip ALL of this. Local inference
     never leaves the machine, so there's nothing to anonymize.

The transparency page at /privacy/cloud-ai documents the exact rules.
"""

from __future__ import annotations

import logging
import re
from typing import Iterable

logger = logging.getLogger("sage.providers.anonymizer")


# Top-level payload keys we forbid for cloud providers. Lowercased.
# OpenAI's API uses `user`; some providers use `metadata`; we strip both
# plus anything else that smells identifying.
FORBIDDEN_TOP_LEVEL_KEYS: frozenset[str] = frozenset({
    "user",
    "user_id",
    "userid",
    "end_user",
    "end_user_id",
    "customer",
    "customer_id",
    "client_id",
    "uid",
    "email",
    "identity",
    "metadata",
    "fingerprint",
    "session_id",
    "request_id",
})


# Providers that run on the user's own machine. These bypass anonymization
# because nothing leaves the device.
LOCAL_PROVIDERS: frozenset[str] = frozenset({
    "ollama",
    "llama-cpp",
    "llama_cpp",
    "local",
})


# Email regex — RFC-5322 simplified. We replace with the literal token
# `[email redacted]` so the model still understands an address belongs
# here without seeing the actual value.
_EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)

# US-format phone with explicit separators. We deliberately do NOT match
# bare 10-digit strings — too many false positives in code (e.g., timestamps,
# port numbers, large constants).
_PHONE_RE = re.compile(
    r"\b(?:\+?1[\s.\-]?)?\(?([2-9]\d{2})\)?[\s.\-]([2-9]\d{2})[\s.\-](\d{4})\b"
)


def is_local_provider(provider_name: str) -> bool:
    """True if `provider_name` runs on the end-user's machine."""
    return (provider_name or "").lower() in LOCAL_PROVIDERS


def scrub_text(text: str) -> str:
    """Mask obvious PII in a free-form string.

    Only formats with explicit separators are matched — keeps false-positive
    rate low on code-heavy prompts. Order matters: phone before email is
    safer because some emails embed digits.
    """
    if not text:
        return text
    text = _PHONE_RE.sub("[phone redacted]", text)
    text = _EMAIL_RE.sub("[email redacted]", text)
    return text


def _scrub_message_content(content):
    """Recursively scrub a message's `content` field.

    OpenAI-compatible APIs accept either a plain string or a list of content
    parts (`{"type": "text", "text": "..."}`). We handle both.
    """
    if isinstance(content, str):
        return scrub_text(content)
    if isinstance(content, list):
        scrubbed = []
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                scrubbed.append({**part, "text": scrub_text(part["text"])})
            else:
                scrubbed.append(part)
        return scrubbed
    return content


def anonymize_payload(payload: dict, *, provider_name: str) -> dict:
    """Return a sanitized copy of `payload` safe to send to `provider_name`.

    Local providers pass through unchanged. Cloud providers get:
      - Forbidden top-level keys removed (with a warning logged so leaks
        get caught in dev)
      - `messages[].content` PII-scrubbed

    Never mutates the input.
    """
    if is_local_provider(provider_name):
        return payload

    # Shallow copy — we'll rebuild the messages list below.
    clean: dict = {}
    leaked_keys: list[str] = []
    for key, value in payload.items():
        if key.lower() in FORBIDDEN_TOP_LEVEL_KEYS:
            leaked_keys.append(key)
            continue
        clean[key] = value

    if leaked_keys:
        # Deliberately log key NAMES only, never values — values may contain
        # the very PII we're trying to keep out of logs.
        logger.warning(
            "anonymizer stripped forbidden field(s) before sending to %s: %s",
            provider_name, sorted(leaked_keys),
        )

    # OpenAI-style: `messages[].content` (string OR list of content parts)
    messages = clean.get("messages")
    if isinstance(messages, list):
        clean["messages"] = [
            {**m, "content": _scrub_message_content(m.get("content"))}
            if isinstance(m, dict) else m
            for m in messages
        ]

    # Gemini-style: `contents[].parts[].text` and `systemInstruction.parts[].text`
    contents = clean.get("contents")
    if isinstance(contents, list):
        clean["contents"] = [_scrub_gemini_turn(t) for t in contents]
    system_instr = clean.get("systemInstruction")
    if isinstance(system_instr, dict) and isinstance(system_instr.get("parts"), list):
        clean["systemInstruction"] = {
            **system_instr,
            "parts": [_scrub_gemini_part(p) for p in system_instr["parts"]],
        }

    return clean


def _scrub_gemini_part(part):
    """Scrub a single Gemini `part` (e.g. `{"text": "..."}`)."""
    if isinstance(part, dict) and isinstance(part.get("text"), str):
        return {**part, "text": scrub_text(part["text"])}
    return part


def _scrub_gemini_turn(turn):
    """Scrub all parts inside a Gemini `contents[]` entry."""
    if isinstance(turn, dict) and isinstance(turn.get("parts"), list):
        return {**turn, "parts": [_scrub_gemini_part(p) for p in turn["parts"]]}
    return turn


__all__ = [
    "anonymize_payload",
    "is_local_provider",
    "scrub_text",
    "FORBIDDEN_TOP_LEVEL_KEYS",
    "LOCAL_PROVIDERS",
]
