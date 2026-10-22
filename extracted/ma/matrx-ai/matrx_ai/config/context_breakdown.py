"""What a request's context is made of, measured on the config about to be sent.

The provider reports how many input tokens a call cost, never what they were
spent on. This splits the SAME config the send boundary hands the provider
(after the trim) into the parts a person can reason about — the system prompt,
each family of tool definitions, the conversation's messages, and the tool
calls/results inside them — in characters. A reader multiplies each share by
the provider's real input-token count to get an honest per-part estimate (the
total is exact; only the split is estimated, and it says so).

Pure and best-effort: it never raises into the send path (the caller wraps it),
and an unreadable part is counted as zero rather than guessed.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

BREAKDOWN_VERSION = 1

# Category keys, in display order. Labels are short UI text.
LABELS: dict[str, str] = {
    "system_prompt": "System prompt",
    "system_tools": "System tools",
    "mcp_tools": "MCP tools",
    "agent_tools": "Agent tools",
    "messages": "Messages",
    "tool_activity": "Tool calls & results",
}


def _chars(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value)
    try:
        return len(json.dumps(value, default=str, ensure_ascii=False))
    except Exception:  # noqa: BLE001 — unreadable counts as nothing, never a guess
        return 0


def _system_text(config: Any) -> str:
    raw = getattr(config, "system_instruction", None)
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw
    for attr in ("text", "content", "value"):
        val = getattr(raw, attr, None)
        if isinstance(val, str):
            return val
    if isinstance(raw, dict):
        return json.dumps(raw, default=str)
    return str(raw)


def _tool_family(name: str) -> str:
    if name.startswith(("mcp.", "mcp__", "mcp:")):
        return "mcp_tools"
    if name.startswith("custom_tool_"):
        return "agent_tools"
    return "system_tools"


def _declaration_name(declaration: Any) -> str:
    """The tool name a declaration carries. A declaration that is not a dict (a bare name, a
    pydantic model, an SDK object) is read for the same fields and never raises."""
    if isinstance(declaration, str):
        return declaration
    if isinstance(declaration, dict):
        function = declaration.get("function")
        inner = function.get("name") if isinstance(function, dict) else None
        return str(declaration.get("name") or inner or "")
    function = getattr(declaration, "function", None)
    return str(
        getattr(declaration, "name", None) or getattr(function, "name", None) or ""
    )


def _tool_definitions(config: Any) -> list[tuple[str, int]]:
    """(name, chars) for every tool definition this call declares."""
    out: list[tuple[str, int]] = []
    declared = getattr(config, "tool_declarations", None)
    if isinstance(declared, dict) and declared:
        # The stabilized per-provider declarations ARE what goes on the wire.
        decls = next(iter(declared.values())) or []
        if isinstance(decls, (str, dict)):
            decls = [decls]
        for d in decls:
            out.append((_declaration_name(d), _chars(d)))
        if out:
            return out
    try:
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
    except Exception:  # noqa: BLE001
        registry = None
    for tool in getattr(config, "tools", None) or []:
        name = tool if isinstance(tool, str) else str(getattr(tool, "name", "") or "")
        if not name:
            continue
        definition = registry.get(name) if registry is not None else None
        if definition is None:
            out.append((name, _chars(name)))
            continue
        out.append(
            (
                name,
                _chars(getattr(definition, "description", "") or "")
                + _chars(getattr(definition, "parameters", None) or {}),
            )
        )
    return out


def _message_parts(message: Any) -> tuple[int, int]:
    """(conversation chars, tool-activity chars) for one message."""
    content = (
        message.get("content") if isinstance(message, dict) else getattr(message, "content", None)
    )
    if isinstance(content, str):
        return len(content), 0
    convo = tool = 0
    for part in content or []:
        kind = type(part).__name__.lower()
        ptype = str(
            (part.get("type") if isinstance(part, dict) else getattr(part, "type", "")) or ""
        ).lower()
        is_tool = "tool" in kind or "tool" in ptype
        text = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)
        size = (
            len(text)
            if isinstance(text, str)
            else _chars(part.model_dump() if hasattr(part, "model_dump") else part)
        )
        if is_tool:
            tool += size
        else:
            convo += size
    return convo, tool


def measure(config: Any) -> dict[str, Any]:
    """The breakdown of ``config`` as a JSON-ready dict (``unit: chars``)."""
    totals = dict.fromkeys(LABELS, 0)
    items = dict.fromkeys(LABELS, 0)

    system = _system_text(config)
    totals["system_prompt"] = len(system)

    for name, size in _tool_definitions(config):
        family = _tool_family(name)
        totals[family] += size
        items[family] += 1

    messages = getattr(config, "messages", None) or []
    for message in messages:
        role = message.get("role") if isinstance(message, dict) else getattr(message, "role", None)
        role = str(getattr(role, "value", role) or "")
        if role in ("system", "developer"):
            totals["system_prompt"] += sum(_message_parts(message))
            continue
        convo, tool = _message_parts(message)
        totals["messages"] += convo
        totals["tool_activity"] += tool
        items["messages"] += 1

    total = sum(totals.values())
    return {
        "version": BREAKDOWN_VERSION,
        "unit": "chars",
        "measured_at": datetime.now(UTC).isoformat(),
        "model": getattr(config, "model", None),
        "total_chars": total,
        "categories": [
            {"key": key, "label": label, "chars": totals[key], "items": items[key]}
            for key, label in LABELS.items()
        ],
    }


__all__ = ["BREAKDOWN_VERSION", "LABELS", "measure"]
