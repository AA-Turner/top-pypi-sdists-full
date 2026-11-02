"""Bounded, per-attempt summaries of retained scalar metrics."""

from collections import OrderedDict
from datetime import datetime
from fnmatch import fnmatchcase

from labqoat.cli.console.metric_cadence import MetricCadence
from labqoat.cli.console.metric_progress import MetricProgress
from labqoat.json_document import JsonDocument


class MetricSummary:
    """Group adjacent step points while always showing validation, evaluation, and final samples."""

    def __init__(self, every: str = "auto", patterns: tuple[str, ...] = ()) -> None:
        """Keep at most four display columns for each of 256 recently observed series groups."""
        self.cadence = MetricCadence(every)
        self.patterns = patterns
        self.pending: OrderedDict[str, JsonDocument] = OrderedDict()
        self.previous: OrderedDict[str, tuple[int, float]] = OrderedDict()
        self.progress = MetricProgress()
        self.totals: OrderedDict[str, int] = OrderedDict()

    def accept(self, document: JsonDocument) -> list[JsonDocument]:
        """Flush step boundaries and milestones without relying on observer wall-clock speed."""
        if document.get("stream") != "metric":
            return self.non_metric(document)
        data = JsonDocument.expect_dict(document.get("data", {}))
        name = str(data.get("name", ""))
        if self.patterns and not any(fnmatchcase(name, pattern) for pattern in self.patterns):
            return []
        phase = self.phase(name)
        key = self.owner(document) + phase
        emitted = self.boundary(key, data.get("step"))
        self.retain(key, document, data, phase)
        return emitted

    @staticmethod
    def owner(document: JsonDocument) -> str:
        """Separate attempt coordinates and descendant paths."""
        return f"{document.get('run_id') or document.get('run_path', '')}:{document.get('attempt_id', '')}:"

    def non_metric(self, document: JsonDocument) -> list[JsonDocument]:
        """Explicit milestones finish summaries; incidental stdout cannot reset sampling."""
        if document.get("stream") == "progress" and self.declare(document):
            return []
        kind = str(document.get("event_type", ""))
        if (
            document.get("stream") == "milestone"
            or kind in ("run.completed", "run.failed", "run.cancelled", "run.completed_with_errors")
            or document.get("type") == "run.logs.complete"
        ):
            return [*self.flush(), document]
        return [document]

    def declare(self, document: JsonDocument) -> bool:
        """A total survives later metric steps and applies only to this invocation."""
        data = JsonDocument.expect_dict(document.get("data", {}))
        total = data.get("total")
        if not isinstance(total, int) or total <= 0:
            return False
        owner = self.owner(document)
        self.totals[owner] = total
        self.totals.move_to_end(owner)
        if len(self.totals) > 256:
            self.totals.popitem(last=False)
        selected = [row for key, row in self.pending.items() if key.startswith(owner)]
        for row in selected:
            row["total"] = total
        return bool(selected)

    def boundary(self, key: str, step: object) -> list[JsonDocument]:
        """Changing steps completes the previous immutable sample."""
        previous = self.pending.get(key)
        if previous is None or previous["step"] == step:
            return []
        result = self.emit(key, force=False)
        self.pending.pop(key)
        return result

    def retain(self, key: str, document: JsonDocument, data: JsonDocument, phase: str) -> None:
        """Retain source attribution and a bounded set of scalar columns."""
        if key not in self.pending:
            self.pending[key] = JsonDocument(document)
            self.pending[key].update(step=data.get("step", 0), phase=phase, metrics={})
            self.pending[key]["total"] = self.totals.get(self.owner(document))
        row = self.pending[key]
        metrics = JsonDocument.expect_dict(row["metrics"])
        if len(metrics) < 4:
            metrics[str(data["name"])] = data["value"]
        row["metrics"] = metrics
        self.pending.move_to_end(key)
        if len(self.pending) > 256:
            oldest, _entry = self.pending.popitem(last=False)
            self.previous.pop(oldest, None)

    def emit(self, key: str, *, force: bool) -> list[JsonDocument]:
        """Training spacing never suppresses validation or evaluation milestones."""
        row = self.pending[key]
        step = int(str(row["step"]))
        raw = str(row.get("produced_at") or row.get("inserted_at") or "1970-01-01T00:00:00Z")
        timestamp = datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp()
        total = int(str(row["total"])) if row.get("total") else None
        if (
            not force
            and row["phase"] == "training"
            and not self.cadence.due(self.previous.get(key), step, timestamp, total)
        ):
            return []
        self.previous[key] = (step, timestamp)
        self.previous.move_to_end(key)
        if len(self.previous) > 256:
            self.previous.popitem(last=False)
        metrics = JsonDocument.expect_dict(row["metrics"])
        columns = "  ".join(f"{name} {float(str(value)):.4g}" for name, value in metrics.items())
        progress = self.progress.describe(key, step, timestamp, total)
        return [JsonDocument(row, content=f"{row['phase']}  {progress}  {columns}")]

    def flush(self) -> list[JsonDocument]:
        """Keep the last available sample before a milestone, outcome, or observer completion."""
        rows = [row for key in self.pending for row in self.emit(key, force=True)]
        self.pending.clear()
        return rows

    @staticmethod
    def phase(name: str) -> str:
        """Treat only explicit metric namespaces as phase evidence."""
        prefix = name.partition("/")[0]
        if prefix in ("val", "validation"):
            return "validation"
        if prefix in ("eval", "evaluation", "test"):
            return "evaluation"
        return "training"
