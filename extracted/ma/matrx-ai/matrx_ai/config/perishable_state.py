"""Perishable state — what a tool SAW of a live machine goes stale between turns.

The defect (measured on the Personal Staff thread, 2026-09-26 and 2026-09-28)
-----------------------------------------------------------------------------
A Personal Staff thread never ends: every text, call and app visit continues the
same conversation. On it, asked "what files are in my workspace?", the Chief of
Staff answered from an ``fs_list`` result three turns back — five old marker
files — and missed the file it had created in the turn before. Asked to "run
``uname -a``", it recited an earlier ``shell_execute`` output without running
anything. About 2 of every 12 turns. It gets worse as the history grows, because
there is more old workspace state to copy from.

A listing, a command's output, a page the browser read: each is a photograph of
a live system at one instant. In the turn it arrived in it is the truth; in any
later turn it is a memory of the truth, and the model has no way to tell the two
apart — both are just text in its history. The world's best coding agents
(Claude Code, Cursor) treat file and terminal state as perishable and re-read
before they assert. This module makes the history SAY which results are
photographs from an earlier turn, with the time they were taken.

What it does
------------
``mark_perishable_state`` walks the message list the resolver hands the send
boundary and, for every ``tool_result`` block from a PERISHABLE tool (see
:func:`is_perishable_tool`) that sits BEFORE the current turn — i.e. before the
last message the person sent — prefixes its content with::

    [STALE — this is what fs_list returned at 2026-09-28 02:40 UTC, in an
    earlier turn. The workspace, its files, processes and browser may have
    changed since. Never state it as current; run the tool again.]

Results from the current turn are never touched: they are this turn's truth.

Properties the send boundary depends on
---------------------------------------
* In-memory only. The database row is never written; the original output stays
  authoritative and replays unmarked to every human surface.
* Deterministic and cache-stable: the stamp is the tool message's OWN timestamp
  (``UnifiedMessage.timestamp``, its ``created_at``), never "now", so a result
  marked once is byte-identical on every later turn and the prompt-cache prefix
  moves exactly once — the turn after the result arrived.
* Idempotent: a block already carrying the marker is left alone.
* Pairing-safe: only ``content`` changes; ids, names and ``is_error`` stay.
* Media-bearing results (typed image/audio/video block lists) are never touched.

Who turns it on
---------------
The HOST decides which conversations are permanent (``_ext``
``perishable_state_marker``), because only the host knows what a staff thread
is. Unconfigured, nothing is marked and matrx-ai behaves exactly as before.
It is a send-boundary step (``send_boundary.prepare_for_send``, resolve stage)
and may be called from nowhere else — ``tests/test_send_boundary_guard.py``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

#: The marker every stale block opens with — also the idempotence key.
STALE_MARKER = "[STALE — "

#: Tools whose output is a reading of a live machine: files, processes, the
#: terminal, a browser. An ACTION's receipt (fs_write "wrote 12 bytes",
#: fs_mkdir, fs_delete) is a record of what was done, not a reading of state,
#: and stays as it is.
PERISHABLE_TOOL_NAMES: frozenset[str] = frozenset(
    {
        "fs_list",
        "fs_read",
        "fs_read_forced",
        "fs_search",
        "shell_execute",
        "shell_exec",
        "shell_python",
        "desktop_capabilities",
    }
)

#: Whole families that read a live surface (every browser / computer-use tool).
PERISHABLE_TOOL_PREFIXES: tuple[str, ...] = ("browser_", "cloud_browser", "computer_")


def is_perishable_tool(name: str | None) -> bool:
    """True when this tool's output describes live machine state."""
    if not name:
        return False
    tool = str(name).strip()
    return tool in PERISHABLE_TOOL_NAMES or tool.startswith(PERISHABLE_TOOL_PREFIXES)


@dataclass
class PerishableReport:
    """Audit of one pass — logged by the send boundary."""

    blocks_marked: int = 0
    tools: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"blocks_marked": self.blocks_marked, "tools": list(self.tools)}


def _get(obj: Any, attr: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(attr)
    return getattr(obj, attr, None)


def _set_content(block: Any, value: Any) -> None:
    if isinstance(block, dict):
        block["content"] = value
    else:
        block.content = value


def _role(message: Any) -> str:
    role = _get(message, "role")
    return str(getattr(role, "value", role) or "")


def _is_tool_result(block: Any) -> bool:
    return _get(block, "type") == "tool_result"


def _is_person_turn(message: Any) -> bool:
    """A message the PERSON sent — a user row that is not a tool-result carrier."""
    if _role(message) != "user":
        return False
    content = _get(message, "content") or []
    if isinstance(content, list) and content and all(_is_tool_result(b) for b in content):
        return False
    return True


def _is_media_list(content: Any) -> bool:
    return isinstance(content, list) and any(
        hasattr(item, "to_anthropic") or hasattr(item, "to_openai") or hasattr(item, "to_google")
        for item in content
    )


def stamp_for(timestamp: Any) -> str:
    """``2026-09-28 02:40 UTC`` from an ISO string / datetime / epoch — or "an earlier turn"."""
    moment: datetime | None = None
    if isinstance(timestamp, datetime):
        moment = timestamp
    elif isinstance(timestamp, (int, float)) and timestamp > 0:
        seconds = timestamp / 1000 if timestamp > 10**11 else timestamp
        moment = datetime.fromtimestamp(seconds, tz=UTC)
    elif isinstance(timestamp, str) and timestamp:
        try:
            moment = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            moment = None
    if moment is None:
        return "an unrecorded time"
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC")


def stale_prefix(tool_name: str, timestamp: Any) -> str:
    return (
        f"{STALE_MARKER}this is what {tool_name} returned at {stamp_for(timestamp)}, in an "
        "earlier turn. The workspace, its files, processes and browser may have changed "
        "since. Never state it as current; run the tool again to see it now.]\n"
    )


def _already_marked(content: Any) -> bool:
    return isinstance(content, str) and content.startswith(STALE_MARKER)


def mark_perishable_state(messages: list[Any]) -> PerishableReport:
    """Mark every perishable tool result from an earlier turn as stale, in place.

    The current turn begins at the LAST message the person sent; everything
    before it is an earlier turn. A list with no person message marks nothing
    (there is no "earlier" to speak of).
    """
    report = PerishableReport()
    current_turn_start: int | None = None
    for index in range(len(messages) - 1, -1, -1):
        if _is_person_turn(messages[index]):
            current_turn_start = index
            break
    if current_turn_start is None:
        return report

    for message in messages[:current_turn_start]:
        blocks = _get(message, "content")
        if not isinstance(blocks, list):
            continue
        timestamp = _get(message, "timestamp")
        for block in blocks:
            if not _is_tool_result(block):
                continue
            name = _get(block, "name") or ""
            if not is_perishable_tool(name):
                continue
            content = _get(block, "content")
            if _already_marked(content) or _is_media_list(content):
                continue
            if isinstance(content, str):
                body = content
            elif content is None:
                body = ""
            else:
                try:
                    body = json.dumps(content, default=str)
                except (TypeError, ValueError):
                    body = str(content)
            _set_content(block, stale_prefix(str(name), timestamp) + body)
            report.blocks_marked += 1
            report.tools.append(str(name))
    return report


__all__ = [
    "PERISHABLE_TOOL_NAMES",
    "PERISHABLE_TOOL_PREFIXES",
    "PerishableReport",
    "STALE_MARKER",
    "is_perishable_tool",
    "mark_perishable_state",
    "stale_prefix",
    "stamp_for",
]
