"""Normalize retained log evidence for text and JSON without dropping metadata."""

from labqoat.cli.console.lifecycle_message import LifecycleMessage
from labqoat.json_document import JsonDocument
from typing import ClassVar


class ConsoleEntry:
    """Separate source, severity, event time, and rendering identity."""

    levels: ClassVar[dict[str, int]] = {
        "debug": 10,
        "info": 20,
        "progress": 25,
        "warning": 30,
        "error": 40,
        "critical": 50,
    }
    symbols: ClassVar[dict[str, str]] = {
        "debug": "·",
        "info": " ",
        "progress": "▸",
        "warning": "⚠",
        "error": "✗",
        "critical": "✗",
    }

    def __init__(self, document: JsonDocument) -> None:
        """Preserve raw fields and supply defaults for older worker output."""
        self.document = document
        self.source = str(document.get("stream", "stdout"))
        self.source = {"lifecycle": "system", "execution": "stdout", "runtime": "system"}.get(self.source, self.source)
        self.kind = LifecycleMessage.kind(document)
        fallback = LifecycleMessage.level(document) if self.kind else "info"
        self.level = str(document.get("level", "debug" if self.source == "build" else fallback))
        self.content = LifecycleMessage.describe(document) if self.kind else str(document.get("content", ""))
        if "LABQOAT_TIMING " in self.content and "level" not in document:
            self.level = "debug"  # the platform's own stage timings, read with --level debug
        if self.source == "milestone":
            self.content = self.milestone(document)
        self.terminal = self.kind in LifecycleMessage.outcomes

    def group(self) -> bool:
        """Whether this record comes from a group: a node that organizes children and runs nothing itself."""
        source = self.document.get("source")
        return isinstance(source, dict) and source.get("workload_kind") == "group"

    def path(self) -> str:
        """The descendant this record belongs to, with operation-key separators shown as written."""
        return str(self.document.get("run_path") or "").replace("~1", "/").replace("~0", "~")

    def symbol(self) -> str:
        """Use outcome and milestone symbols independently from severity."""
        special = {"completed": "✓", "cancelled": "■", "queued": "…"}
        if self.source in ("milestone", "progress"):
            return "◆" if self.source == "milestone" else "▸"
        if self.source == "metric" and self.document.get("phase") in ("validation", "evaluation"):
            return "◆"
        return special.get(self.kind, self.symbols.get(self.level, "·"))

    @staticmethod
    def milestone(document: JsonDocument) -> str:
        """Display caller-authored scalar fields alongside the milestone's message."""
        data = document.get("data")
        if not isinstance(data, dict):
            return str(document.get("content", ""))
        fields = [
            f"{key} {value:.4g}" if isinstance(value, float) else f"{key} {value}"
            for key, value in data.items()
            if not isinstance(value, (dict, list))
        ]
        return "  ".join([str(document.get("content", "")), *fields])

    def json(self) -> JsonDocument:
        """Retain original evidence while adding the normalized console vocabulary."""
        result = JsonDocument(self.document)
        result.update(level=self.level, stream=self.source, message=self.content)
        return result
