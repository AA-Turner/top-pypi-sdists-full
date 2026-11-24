"""TOOL BRIEFINGS — a short block every run that holds a family of tools is handed, unasked.

A tool family can be useless until the model knows what it is working on: an agent with the
``records`` tools spent its first calls (and often guessed instead) finding out which tables exist.
A briefing is the small answer to that first question, attached to every run that holds any of the
family's tools, so the first call is already the right one.

The host registers one briefing per family at boot (``register_tool_briefing``): a slot name, the
tool names that make it apply, and an async source ``(AppContext) -> block | None``. This package
only places the block. No briefing registered → nothing staged (standalone posture).

ONE PATH, AND THE CACHE GATE HOLDS. The block rides the per-turn context channel
(``MessageList.attach_turn_context``, its own slot) and is staged by the send boundary alone
(``send_boundary._stage_tool_briefings``), on every loop send. That channel is the cache-safe one:
the turn's FIRST send freezes what it placed, later sends of the turn place that exact text, an
earlier turn replays the block its own sends cached, and what changed since rides the tail after
the cache line. So a briefing never rewrites a cached prefix, and it is rendered once per turn
(memo by ``request_id`` and slot) so a long tool loop asks the source once.

A run that holds none of a briefing's tools gets its slot cleared, so a tool removed mid-loop takes
its briefing with it.
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from typing import Any

#: ``async (AppContext | None) -> block | None``.
ToolBriefingSource = Callable[[Any], Awaitable["str | None"]]


@dataclass(frozen=True)
class ToolBriefing:
    """One family's briefing: applies when the run holds ANY of ``tools``."""

    slot: str
    tools: frozenset[str]
    source: ToolBriefingSource


_BRIEFINGS: dict[str, ToolBriefing] = {}
_MAX_MEMO = 512
_MEMO: OrderedDict[tuple[str, str], str] = OrderedDict()


def register_tool_briefing(slot: str, tools: Iterable[str], source: ToolBriefingSource) -> None:
    """Install (or replace) the briefing staged in ``slot`` for runs holding any of ``tools``."""
    names = frozenset(str(t) for t in tools if t)
    if not slot or not names:
        raise ValueError("register_tool_briefing: a briefing needs a slot name and at least one tool name.")
    _BRIEFINGS[slot] = ToolBriefing(slot=slot, tools=names, source=source)
    for key in [k for k in _MEMO if k[1] == slot]:
        del _MEMO[key]


def unregister_tool_briefing(slot: str) -> None:
    _BRIEFINGS.pop(slot, None)


def registered_tool_briefings() -> dict[str, ToolBriefing]:
    return dict(_BRIEFINGS)


def tool_names_of(config: Any) -> frozenset[str]:
    """Every tool name this run holds: preloaded, discovered mid-conversation, and custom."""
    names: set[str] = set()
    for attr in ("tools", "dynamic_tools", "custom_tools"):
        for tool in getattr(config, attr, None) or ():
            name = tool if isinstance(tool, str) else getattr(tool, "name", None)
            if name:
                names.add(str(name))
    return frozenset(names)


async def stage_tool_briefings(config: Any, ctx: Any) -> tuple[list[str], list[tuple[str, BaseException]]]:
    """Attach (or clear) every registered briefing for this send.

    Answers ``(slots that went out, [(slot, failure)])``. A failing source clears its own slot and
    is handed back to the caller to announce; it never costs the other briefings or the send.
    """
    attach = getattr(getattr(config, "messages", None), "attach_turn_context", None)
    if attach is None or not _BRIEFINGS:
        return [], []
    held = tool_names_of(config)
    request = str(getattr(ctx, "request_id", "") or "")
    staged: list[str] = []
    failed: list[tuple[str, BaseException]] = []
    for slot, briefing in list(_BRIEFINGS.items()):
        if not (held & briefing.tools):
            attach("", slot=slot)
            continue
        key = (request, slot)
        if request and key in _MEMO:
            block = _MEMO[key]
        else:
            try:
                block = (await briefing.source(ctx)) or ""
            except Exception as exc:  # noqa: BLE001 — handed to the caller, which announces it
                attach("", slot=slot)
                failed.append((slot, exc))
                continue
            if request:
                _MEMO[key] = block
                while len(_MEMO) > _MAX_MEMO:
                    _MEMO.popitem(last=False)
        attach(block, slot=slot)
        if block:
            staged.append(slot)
    return staged, failed


__all__ = [
    "ToolBriefing",
    "ToolBriefingSource",
    "register_tool_briefing",
    "registered_tool_briefings",
    "stage_tool_briefings",
    "tool_names_of",
    "unregister_tool_briefing",
]
