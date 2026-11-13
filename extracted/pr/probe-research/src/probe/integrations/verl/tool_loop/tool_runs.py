"""Whether one verl tool call worked (O4). `_call_tool` turns every failure into an ordinary `ToolResponse`
(`tool_agent_loop.py:457-494`), so "it returned" is not success: an unknown name or arguments that are not JSON are
decided by verl's own two checks before the call, an exception by verl's fixed prefix
`Error executing tool '<name>': ` (pinned); a response past both is the tool's own return. Anything else is None
(unknown), never True by default."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

#: verl's text for a tool that raised (`tool_agent_loop.py:492`), pinned by `tests/integrations/verl/pinned.py`.
ERROR_PREFIX = "Error executing tool '{name}': "


@dataclass
class ToolOutcome:
    is_ok: bool | None
    error: str | None = None


def get_tool_outcome(tool_call: Any, active_tools: Any, response: Any) -> ToolOutcome:
    """What `_call_tool` did with ``tool_call`` given the loop's ``active_tools`` and what it returned (its
    `ToolResponse`, the first of its tuple)."""
    name = getattr(tool_call, "name", None)
    text = getattr(response, "text", None)
    if not isinstance(name, str) or not hasattr(active_tools, "__contains__"):
        return ToolOutcome(None)
    if name not in active_tools:
        return ToolOutcome(False, text or f"unknown tool {name!r}")
    try:
        json.loads(getattr(tool_call, "arguments", None))
    except (json.JSONDecodeError, TypeError):
        return ToolOutcome(False, text or "the arguments are not JSON")
    prefix = ERROR_PREFIX.format(name=name)
    if isinstance(text, str) and text.startswith(prefix):
        return ToolOutcome(False, text[len(prefix):] or text)
    if not hasattr(response, "text"):
        return ToolOutcome(None)
    return ToolOutcome(True)
