"""Pinned tool arguments — a person's per-request limit on what a tool call may ask for.

A host stamps ``AppContext.metadata[PINNED_TOOL_ARGS_KEY] = {tool_name: {arg: value}}``
(aidream: the chat's "the AI may search all of my Notes" pin, ``user.search_types`` →
``knowledge_search.types``). ``ToolExecutor.execute`` applies the pins to the call's
arguments BEFORE the durable tool row, the trace and validation, so every record of the
call carries what actually ran, and the model is told on the result.

Rules, per pinned argument:
  * a LIST pin limits: the model's list narrowed to the pinned values; nothing left (or
    nothing asked) → the pin itself.
  * any other pin replaces the model's value.
"""

from __future__ import annotations

from typing import Any

PINNED_TOOL_ARGS_KEY = "pinned_tool_args"


def pins_for(tool_name: str, metadata: dict[str, Any] | None) -> dict[str, Any]:
    """The pins a request set for ``tool_name`` ({} when none)."""
    raw = (metadata or {}).get(PINNED_TOOL_ARGS_KEY)
    if not isinstance(raw, dict):
        return {}
    pins = raw.get(tool_name)
    return dict(pins) if isinstance(pins, dict) else {}


def apply_arg_pins(arguments: dict[str, Any], pins: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """``(pinned arguments, one sentence per argument the pin changed)``. Never mutates."""
    if not pins:
        return arguments, []
    out = dict(arguments or {})
    changes: list[str] = []
    for name, pinned in pins.items():
        asked = out.get(name)
        if isinstance(pinned, list | tuple):
            allowed = list(pinned)
            narrowed = [v for v in asked if v in allowed] if isinstance(asked, list) else []
            value = narrowed or allowed
        else:
            value = pinned
        if asked != value:
            changes.append(
                f"{name}={value!r} (this chat limits it; the call asked for {asked!r})"
                if asked is not None
                else f"{name}={value!r} (set by this chat)"
            )
        out[name] = value
    return out, changes


__all__ = ["PINNED_TOOL_ARGS_KEY", "apply_arg_pins", "pins_for"]
