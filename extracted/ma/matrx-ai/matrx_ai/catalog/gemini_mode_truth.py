"""Which thinking mode a Gemini id runs in, as Google answers it (probed, not guessed).

A Gemini 3.x model takes ``thinking_level`` (the ``gemini_3`` mode of the ``google_thinking``
processor); only 2.x and earlier take the raw ``thinking_budget`` (``legacy``). A ``*-latest``
alias is a moving pointer, so the table below pins what each resolved to on the probe date:
``generateContent`` with the alias returns ``modelVersion`` = the real id.

Guards: ``packages/matrx-ai/tests/test_gemini_3x_never_legacy_mode.py`` (pinned cells) and
``scripts/check_unsupported_settings_never_reach_wire.py`` (I6, every live offering).
"""

from __future__ import annotations

import re

# alias -> the concrete model it answered as (probe 2026-10-18, modelVersion of a tiny call).
GEMINI_ALIAS_RESOLUTION: dict[str, str] = {
    "gemini-flash-latest": "gemini-3.8-flash",
    "gemini-flash-lite-latest": "gemini-3.5-flash-lite",
    "gemini-pro-latest": "gemini-3.1-pro-preview",
}

_GEMINI_3X = re.compile(r"^gemini-([3-9])(\.\d+)?-")  # gemini-3-…, gemini-3.5-…, gemini-4-…
_NOT_THINKING = ("-tts", "-image", "-embedding", "-live", "-audio")


def resolved_gemini_id(provider_model_id: str) -> str:
    return GEMINI_ALIAS_RESOLUTION.get(provider_model_id, provider_model_id)


def is_gemini_3x_or_newer(provider_model_id: str) -> bool:
    rid = resolved_gemini_id(provider_model_id)
    return bool(_GEMINI_3X.match(rid)) and not any(t in rid for t in _NOT_THINKING)


def mode_mismatch(provider_model_id: str, mode: str | None) -> str | None:
    """A sentence when a Gemini 3.x-or-newer id is not in ``gemini_3`` mode, else None."""
    if is_gemini_3x_or_newer(provider_model_id) and mode != "gemini_3":
        rid = resolved_gemini_id(provider_model_id)
        return (
            f"{provider_model_id} runs as {rid}, a Gemini 3.x-or-newer model that takes thinking_level, "
            f"but the catalog has it in {mode!r} mode"
        )
    return None
