"""Fold a run's wait for a machine into a few lines, however long it lasts."""

from collections import Counter
from datetime import UTC, datetime, timedelta

from labqoat.cli.console.console_entry import ConsoleEntry
from labqoat.json_document import JsonDocument


class CapacityWait:
    """The first placement line, a summary every ten minutes, and one line when the run gets its worker.

    Placement cycles through regions, shapes and launch refusals for as long as capacity is short, which can be
    hours; each line differs, so plain repeat folding keeps none of them out. JSON output keeps every record.
    """

    interval = timedelta(minutes=10)

    def __init__(self) -> None:
        """Start outside any wait."""
        self.seen: datetime | None = None
        self.reset()

    def reset(self) -> None:
        """Forget the wait that ended."""
        self.started: datetime | None = None
        self.noted: datetime | None = None
        self.refusals: Counter[str] = Counter()
        self.booted = 0
        self.shapes: dict[str, None] = {}
        self.regions: dict[str, None] = {}

    def fold(self, entry: ConsoleEntry) -> list[ConsoleEntry] | None:
        """Lines to print instead of ``entry``, or None when ``entry`` is not part of a wait and prints itself."""
        if entry.document.get("run_path") or not entry.kind:
            return None
        if not entry.kind.startswith("capacity.") or entry.kind == "capacity.worker.started":
            return self.ended(entry)
        at = self.time(entry)
        self.count(entry)
        if self.started is None:
            self.started = self.noted = at
            return [entry]
        if self.noted is not None and at - self.noted >= self.interval:
            self.noted = at
            return [self.line(entry, f"Still waiting for a machine after {self.span(at)}: {self.tally()}")]
        return []

    def ended(self, entry: ConsoleEntry) -> list[ConsoleEntry] | None:
        """Close an open wait with how long it took, then let ``entry`` print as usual."""
        if self.started is None:
            return None
        summary = self.line(entry, f"Placement took {self.span(self.time(entry))}: {self.tally()}")
        self.reset()
        return [summary, entry]

    def count(self, entry: ConsoleEntry) -> None:
        """Remember refusals by cause and where placement looked."""
        raw = entry.document.get("data")
        data = JsonDocument.expect_dict(raw) if isinstance(raw, dict) else JsonDocument()
        self.booted += entry.kind == "capacity.machine.booting"
        if data.get("code") == "launch_failed":
            self.refusals[str(data.get("error") or "refused")] += 1
        types = data.get("instance_types")
        self.shapes.update(dict.fromkeys(str(name) for name in types) if isinstance(types, list) else {})
        if data.get("location_id"):
            self.regions[str(data["location_id"])] = None

    def tally(self) -> str:
        """Refusals by cause and the places tried, short enough for one line."""
        refusals = sum(self.refusals.values())
        causes = ", ".join(f"{cause} {count}" for cause, count in self.refusals.most_common(3))
        refused = f"{refusals} launch refusals ({causes})" if refusals else "no launch refusals"
        if self.booted:
            refused = f"{self.booted} machines booted, {refused}"
        if not self.regions:
            return refused
        shapes = ", ".join(list(self.shapes)[:4]) or "machines"
        return f"{refused}; tried {shapes} in {', '.join(self.regions)}"

    def span(self, at: datetime) -> str:
        """The wait so far in hours and minutes."""
        minutes = int((at - (self.started or at)).total_seconds() // 60)
        return f"{minutes // 60}h{minutes % 60:02d}m" if minutes >= 60 else f"{minutes}m"

    @staticmethod
    def line(entry: ConsoleEntry, text: str) -> ConsoleEntry:
        """A summary carrying ``entry``'s time and identity, rendered as plain progress."""
        document = {key: value for key, value in entry.document.items() if key not in ("event_type", "data")}
        return ConsoleEntry(JsonDocument(document, stream="progress", level="progress", content=text))

    def time(self, entry: ConsoleEntry) -> datetime:
        """When the event happened; a record without a time happened when the last timed one did."""
        stamp = (
            entry.document.get("produced_at") or entry.document.get("timestamp") or entry.document.get("inserted_at")
        )
        try:
            at = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        except ValueError:
            return self.seen or datetime.now(UTC)
        self.seen = at if at.tzinfo else at.replace(tzinfo=UTC)
        return self.seen
