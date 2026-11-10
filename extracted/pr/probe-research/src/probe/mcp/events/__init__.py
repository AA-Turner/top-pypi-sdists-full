"""The MCP `events` tool's wait (`events.py`): live events since a cursor, awaited outside the tool slots.
Why and how: `sdk/events/DESIGN.md` ("The MCP `events` tool")."""

from .events import follow_events

__all__ = ["follow_events"]
