"""Optional UTC or elapsed producer timestamps with explicit legacy fallback."""

from datetime import UTC, datetime

from labqoat.json_document import JsonDocument


class ConsoleTimestamp:
    """Anchor elapsed timestamps to the observed run start, never to network arrival.

    Every line of one observation shares that origin, the final outcome included; what happened before the
    run started (submission, build, queueing) is shown as time before it.
    """

    def __init__(self, mode: str) -> None:
        """Retain one observer's timestamp mode and optional start time."""
        self.mode = mode
        self.start: datetime | None = None

    def prefix(self, entry: JsonDocument) -> str:
        """Prefer producer time while tolerating legacy lines with no timestamp."""
        stamp = entry.get("produced_at") or entry.get("timestamp") or entry.get("inserted_at")
        if self.mode == "off" or not isinstance(stamp, str):
            return ""
        time = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if time.tzinfo is None:
            time = time.replace(tzinfo=UTC)
        origin = entry.get("run_started_at")
        if isinstance(origin, str) and not (entry.get("final") and self.start is not None):
            self.start = datetime.fromisoformat(origin.replace("Z", "+00:00"))
        self.start = self.start or time
        if self.mode == "abs":
            return time.astimezone(UTC).isoformat().replace("+00:00", "Z") + " "
        seconds = int((time - self.start).total_seconds())
        minutes, seconds = divmod(abs(seconds), 60)
        return f"{'-' if time < self.start and (minutes or seconds) else '+'}{minutes:02d}:{seconds:02d} "
