"""Descendant progress as periodic counts rather than one line per transition."""

from collections import Counter
from datetime import datetime

from labqoat.cli.console.console_entry import ConsoleEntry
from labqoat.cli.console.lifecycle_message import LifecycleMessage


class ChildDigest:
    """Let an agent follow a fan-out of any size in a bounded number of lines."""

    named = 4
    spacing = 10.0

    def __init__(self, *, enabled: bool) -> None:
        """Track the latest state of each descendant; only an enabled digest replaces their lines."""
        self.enabled = enabled
        self.states: dict[str, str] = {}
        self.reported: Counter[str] = Counter()
        self.last: datetime | None = None

    def replaces(self, entry: ConsoleEntry) -> bool:
        """Absorb descendant stages and successes, and the root's per-child acceptances.

        Failures keep their own line, and so do groups: they are few, and they are how a reader follows the work.
        A warning about a descendant is also its own line and leaves that descendant's counted state alone.
        """
        path = entry.path()
        if not entry.kind or entry.level == "debug":
            return False
        if not path:
            return self.enabled and entry.kind.endswith("child.accepted")
        if entry.group() or entry.kind in LifecycleMessage.advisories:
            return False
        self.states[path] = self.state(entry)
        return self.enabled and (entry.level == "progress" or entry.kind == "completed")

    def due(self, entry: ConsoleEntry) -> str | None:
        """A count line when the picture changed and the last one is at least ten seconds of run time old."""
        stamp = entry.document.get("inserted_at") or entry.document.get("produced_at")
        if not isinstance(stamp, str):
            return None
        time = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if self.last is not None and (time - self.last).total_seconds() < self.spacing:
            return None
        line = self.flush()
        if line is not None:
            self.last = time
        return line

    def flush(self) -> str | None:
        """Each child by name while there are few, counts by state beyond that; nothing when unchanged."""
        counts = Counter(self.states.values())
        if not counts or counts == self.reported:
            return None
        self.reported = counts
        if len(self.states) <= self.named:
            parts = ", ".join(f"{path} {state}" for path, state in self.states.items())
        else:
            parts = ", ".join(f"{count} {state}" for state, count in sorted(counts.items()))
        return f"children {len(self.states)}: {parts}"

    @staticmethod
    def state(entry: ConsoleEntry) -> str:
        """Outcomes keep their name; everything before execution is waiting."""
        if entry.terminal:
            return entry.kind.replace("_", " ")
        return "running" if entry.kind in ("running", "finalizing") else "waiting"
