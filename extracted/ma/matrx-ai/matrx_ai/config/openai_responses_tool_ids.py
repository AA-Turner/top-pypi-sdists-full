from __future__ import annotations

import hashlib
import re

_OPENAI_FC_ID_MAX_LEN = 64
_JOIN_KEY_PREFIXES = ("toolu_", "call_", "fc_", "gemini_")


def _join_suffix(join_key: str) -> str:
    for prefix in _JOIN_KEY_PREFIXES:
        if join_key.startswith(prefix):
            return join_key[len(prefix) :]
    return join_key


def _fc_item_id(raw_fc_id: str) -> str:
    candidate = raw_fc_id if raw_fc_id.startswith("fc") else f"fc_{raw_fc_id}"
    if len(candidate) <= _OPENAI_FC_ID_MAX_LEN and re.fullmatch(r"fc[_A-Za-z0-9-]+", candidate):
        return candidate
    digest = hashlib.sha256(candidate.encode()).hexdigest()[:48]
    return f"fc_{digest}"


def openai_responses_tool_call_wire_ids(
    join_key: str,
    *,
    openai_item_id: str | None = None,
) -> tuple[str, str]:
    """Map a stored tool-call join key to OpenAI Responses wire ids.

    ``join_key`` is the canonical id persisted in ``ToolCallContent.id`` /
    ``cx_tool_call.call_id``. Native OpenAI calls already carry a separate
    ``openai_item_id`` (``fc_…``) in metadata; foreign calls (``toolu_``,
    ``gemini_``, etc.) are remapped at serialization time only.
    """
    if not join_key:
        return "fc_missing_join_key", "call_missing_join_key"

    stored_fc = (openai_item_id or "").strip()
    if stored_fc.startswith("fc"):
        wire_call_id = (
            join_key if join_key.startswith("call_") else f"call_{_join_suffix(join_key)}"
        )
        return stored_fc, wire_call_id

    if join_key.startswith("call_"):
        suffix = join_key[len("call_") :]
        return _fc_item_id(f"fc_{suffix}"), join_key

    suffix = _join_suffix(join_key)
    return _fc_item_id(f"fc_{suffix}"), f"call_{suffix}"


def openai_responses_tool_result_call_id(join_key: str) -> str:
    """``function_call_output.call_id`` paired with a remapped ``function_call``."""
    _, wire_call_id = openai_responses_tool_call_wire_ids(join_key)
    return wire_call_id
