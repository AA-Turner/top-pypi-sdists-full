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


#: DECLARED STOP-GAP. The catalog is the authority on a model's dialect (its reasoning cell's
#: ``google_thinking`` mode); the id table above is a guess that stands in ONLY for cells that carry no
#: mode. Chair-step 20261109210000_gemini_3x_reasoning_cells_carry_their_processor.sql (now parked in db/held/) gives the five
#: live cells their mode; once it is applied, set this False and delete GEMINI_ALIAS_RESOLUTION's use
#: here. Guard I8 (scripts/check_unsupported_settings_never_reach_wire.py) fails while this is True and
#: no live Gemini 3.x offering relies on it.
MODEL_ID_FALLBACK_IN_USE = True

_PRE_GEMINI_3 = re.compile(r"^gemini-([0-2])(\.\d+)?-")  # gemini-1.5-…, gemini-2.5-…

#: ids the fallback has decided for, this process (each is named once in the log).
FALLBACK_DECIDED: set[str] = set()


def is_known_pre_gemini_3(provider_model_id: str | None) -> bool:
    """True only for an id we positively know is Gemini 1.x/2.x (aliases resolved)."""
    return bool(provider_model_id) and bool(_PRE_GEMINI_3.match(resolved_gemini_id(str(provider_model_id))))


def is_gemini_3_dialect(mode: str | None, provider_model_id: str | None) -> bool:
    """True when a request to this offering speaks the Gemini 3 dialect.

    The catalog's ``google_thinking`` mode is the authority. Five live Gemini 3.x offerings carry
    no mode on their ``reasoning_effort`` cell (PB-03 t, 2026-11-09), which made them look like
    2.5-class models and dropped Google Search beside function tools, which Gemini 3 accepts. Until
    the catalog is corrected, the model id (aliases resolved) decides for a cell with no mode, and
    SAYS SO in the log each time a new id is decided this way.
    """
    if mode == "gemini_3":
        return True
    if mode is not None or not MODEL_ID_FALLBACK_IN_USE or not provider_model_id:
        return False
    if not is_gemini_3x_or_newer(str(provider_model_id)):
        return False
    pid = str(provider_model_id)
    if pid not in FALLBACK_DECIDED:
        FALLBACK_DECIDED.add(pid)
        import logging

        logging.getLogger(__name__).warning(
            "[gemini-dialect-fallback] %s has no google_thinking mode in its catalog cell; the model id "
            "decided it is Gemini 3.x (%s). Fix the cell (chair-step "
            "20261109210000_gemini_3x_reasoning_cells_carry_their_processor.sql, held in db/held/) and retire this fallback.",
            pid,
            resolved_gemini_id(pid),
        )
    return True
