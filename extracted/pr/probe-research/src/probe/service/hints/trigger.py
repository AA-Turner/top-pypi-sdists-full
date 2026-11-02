"""the TriggerDetector interface (does this event ask for a lookup: trigger, text, senders) and the ordered registry."""

from __future__ import annotations
from probe.service.hints.triggers.command import launches_run
from probe.service.hints.triggers.peer import sender_of
from probe.service.hints.triggers.prompt import _NOT_PROMPTS
from probe.service.hints.triggers.search import WEB_FETCH, WEB_SEARCH
MAIN_STREAM = "main"


class Trigger:
    PROMPT = "prompt"
    PEER = "peer"
    SEARCH = "search"
    COMMAND = "command"
    WINDOW = "window"


#: The triggers a waiting lookup is never replaced by a search or a command for
#: (the server's `prompt` class: the one shown before the others are calibrated).
_ASKED_FIRST = frozenset({Trigger.PROMPT, Trigger.PEER})


def trigger_of(event) -> tuple[str, str, list[str]] | None:
    """`(trigger, text, its senders)` for an event that asks for a lookup, else
    None. A sender is an address the lane resolves to a session to exclude
    (`Senders`)."""
    from probe.shared.harness.events import PEER_TOOL, Kind

    if event.stream != MAIN_STREAM:
        return None
    if event.kind == Kind.PROMPT:
        text = event.text or ""
        return None if text.lstrip().startswith(_NOT_PROMPTS) else (Trigger.PROMPT, text, [])
    if event.kind == Kind.META and event.tool == PEER_TOOL:
        sender = sender_of(event)
        return Trigger.PEER, event.text or "", [sender] if sender else []
    if event.kind != Kind.TOOL_CALL:
        return None
    args = event.tool_input or {}
    if event.tool == WEB_SEARCH:
        query = args.get("query")
        return (Trigger.SEARCH, query, []) if isinstance(query, str) else None
    if event.tool == WEB_FETCH:
        parts = [v for v in (args.get("url"), args.get("prompt")) if isinstance(v, str) and v.strip()]
        return (Trigger.SEARCH, "\n".join(parts), []) if parts else None
    command = args.get("command") if isinstance(args.get("command"), str) else args.get("cmd")
    if isinstance(command, str) and launches_run(command):
        return Trigger.COMMAND, command, []
    return None
