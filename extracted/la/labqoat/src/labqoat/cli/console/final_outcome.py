"""Authoritative final status with measured duration and retained failure evidence."""

from datetime import datetime

from labqoat.json_document import JsonDocument


class FinalOutcome:
    """Keep outcome metadata independent from transient display and child failures."""

    @staticmethod
    def document(run: JsonDocument) -> JsonDocument:
        """Build a final record from the run's own timestamps: time executing, and time since submission.

        Its elapsed origin is the run's start, like the stream's records, and is used only when no stream
        record supplied one; the observer otherwise keeps the origin it has been printing against.
        """
        raw = run.get("failure_detail")
        data = JsonDocument(raw) if isinstance(raw, dict) else JsonDocument()
        end = run.get("ended_at")
        ran = FinalOutcome.span(run.get("started_at"), end)
        total = FinalOutcome.span(run.get("inserted_at"), end)
        if ran is not None:
            data["duration"] = ran
        if total is not None and total != ran:
            data["total"] = f"total {total}"
        return JsonDocument(
            content="",
            event_type=f"run.{run['status']}",
            stream="lifecycle",
            data=data,
            final=True,
            run_id=run.get("id"),
            status=run["status"],
            inserted_at=run.get("ended_at"),
            run_started_at=run.get("started_at") or run.get("inserted_at"),
        )

    @staticmethod
    def span(start: object, end: object) -> str | None:
        """Whole minutes and seconds between two retained instants, when both exist."""
        if not isinstance(start, str) or not isinstance(end, str):
            return None
        duration = datetime.fromisoformat(end.replace("Z", "+00:00")) - datetime.fromisoformat(
            start.replace("Z", "+00:00")
        )
        minutes, seconds = divmod(max(0, round(duration.total_seconds())), 60)
        return f"{minutes}m{seconds:02d}s"
