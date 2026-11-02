"""A run's stages as a checklist: each finished stage with how long it lasted."""

from datetime import datetime
from typing import ClassVar

import click

from labqoat.cli.console.console_entry import ConsoleEntry


class StageBoard:
    """Remember the open stage and close it when the next one, or the outcome, arrives."""

    width = 22
    quiet: ClassVar[frozenset[str]] = frozenset(
        (
            "submission.finalized",
            "submission.build.succeeded",
            "submission.worker.assigned",
            "submission.child.accepted",
            "compute.child.accepted",
            "finalizing",
            "capacity.machine.booting",
            "capacity.machine.ready",
        )
    )
    notes: ClassVar[frozenset[str]] = frozenset(("capacity.worker.started",))

    def __init__(self) -> None:
        """No stage is open until the first lifecycle record."""
        self.label = ""
        self.aside = ""
        self.opened: datetime | None = None

    @classmethod
    def role(cls, entry: ConsoleEntry) -> str:
        """Outcomes end the list, waits and work are stages, bookkeeping is silent and reports stay plain lines."""
        if entry.terminal:
            return "end"
        if entry.kind in cls.quiet:
            return "quiet"
        if entry.kind in cls.notes:
            return "note"
        return "stage" if entry.level == "progress" else "line"

    def advance(self, entry: ConsoleEntry) -> str | None:
        """Open a stage and return the finished line of the one it replaces."""
        finished = self.close(entry, succeeded=True)
        self.label, _, self.aside = entry.content.partition(" · ")
        self.opened = self.instant(entry)
        return finished

    def annotate(self, entry: ConsoleEntry) -> None:
        """Attach a report, such as how the worker container started, to the stage it happened in."""
        detail = entry.content.partition(" · ")[2]
        self.aside = " · ".join(part for part in (self.aside, detail) if part)

    def close(self, entry: ConsoleEntry, *, succeeded: bool) -> str | None:
        """Mark the open stage done, or failed when the run ended in it, timed by the record that ended it."""
        if not self.label:
            return None
        mark = click.style("  ✓", fg="green", bold=True) if succeeded else click.style("  ✗", fg="red", bold=True)
        ended = self.instant(entry)
        seconds = (ended - self.opened).total_seconds() if self.opened is not None and ended is not None else 0.0
        lasted = self.span(seconds) if seconds >= 0.05 else ""
        line = f"{mark} {self.label.ljust(self.width)}{lasted.rjust(7)}"
        line = f"{line}  {click.style(self.aside, dim=True)}" if self.aside else line.rstrip()
        self.label = ""
        return line

    @staticmethod
    def instant(entry: ConsoleEntry) -> datetime | None:
        """When the service retained the record, if it says."""
        stamp = entry.document.get("inserted_at") or entry.document.get("produced_at")
        return StageBoard.instant_of(stamp) if isinstance(stamp, str) else None

    @staticmethod
    def instant_of(stamp: str) -> datetime:
        """Parse a retained UTC instant."""
        return datetime.fromisoformat(stamp.replace("Z", "+00:00"))

    @staticmethod
    def span(seconds: float) -> str:
        """Tenths below ten seconds, whole seconds below a minute, then minutes and seconds."""
        if seconds < 10:
            return f"{max(0.0, seconds):.1f}s"
        if seconds < 60:
            return f"{seconds:.0f}s"
        minutes, rest = divmod(int(seconds), 60)
        return f"{minutes}m{rest:02d}s"
