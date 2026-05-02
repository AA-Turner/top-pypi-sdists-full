"""FlowTask Events.

Event System for Flowtask.
"""
from .events import LogEvent, LogError


def __getattr__(name: str):
    if name == "NotifyEvent":
        from .events import NotifyEvent
        globals()["NotifyEvent"] = NotifyEvent
        return NotifyEvent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    "NotifyEvent",
    "LogEvent",
    "LogError",
)
