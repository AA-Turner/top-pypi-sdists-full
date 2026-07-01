"""Incremental reader for local spans.jsonl files."""

from __future__ import annotations

import json
import typing as t
from dataclasses import dataclass
from json import JSONDecodeError

if t.TYPE_CHECKING:
    from pathlib import Path


@dataclass(slots=True, frozen=True)
class SpanLineSummary:
    """Lightweight summary for one JSONL span record."""

    index: int
    offset: int
    timestamp: str
    name: str
    kind: str
    status: str
    trace_id: str
    span_id: str
    error: str | None = None


class RawSpansReader:
    """Incrementally index and parse a local JSONL spans file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._offsets: list[int] = []
        self._summaries: list[SpanLineSummary] = []
        self._file_size = 0

    @property
    def summaries(self) -> tuple[SpanLineSummary, ...]:
        return tuple(self._summaries)

    def _reset(self) -> None:
        self._offsets.clear()
        self._summaries.clear()
        self._file_size = 0

    def refresh(self) -> bool:
        """Refresh the line index, appending new rows when possible."""
        if not self.path.exists():
            changed = bool(self._offsets or self._summaries or self._file_size)
            self._reset()
            return changed

        size = self.path.stat().st_size
        old_count = len(self._summaries)
        old_size = self._file_size
        offset = 0
        if size < self._file_size:
            self._reset()

        with self.path.open("rb") as handle:
            if self._file_size and size >= self._file_size:
                handle.seek(self._file_size)
                offset = self._file_size

            while True:
                line_offset = offset
                line = handle.readline()
                if not line:
                    break
                offset = handle.tell()
                self._offsets.append(line_offset)
                self._summaries.append(self._parse_summary(len(self._summaries), line_offset, line))

        self._file_size = size
        return len(self._summaries) != old_count or size != old_size

    def _parse_summary(self, index: int, offset: int, line: bytes) -> SpanLineSummary:
        raw_line = line.decode("utf-8", errors="replace").rstrip("\r\n")
        try:
            data = json.loads(raw_line)
        except JSONDecodeError as exc:
            return SpanLineSummary(
                index=index,
                offset=offset,
                timestamp="",
                name="<invalid json>",
                kind="",
                status="invalid",
                trace_id="",
                span_id="",
                error=str(exc),
            )

        if not isinstance(data, dict):
            return SpanLineSummary(
                index=index,
                offset=offset,
                timestamp="",
                name="<invalid span>",
                kind="",
                status="invalid",
                trace_id="",
                span_id="",
                error="Span row is not a JSON object",
            )

        return SpanLineSummary(
            index=index,
            offset=offset,
            timestamp=str(data.get("start_time") or ""),
            name=str(data.get("name") or "<unnamed span>"),
            kind=str(data.get("kind") or ""),
            status=str(data.get("status") or ""),
            trace_id=str(data.get("trace_id") or ""),
            span_id=str(data.get("span_id") or ""),
            error=None,
        )

    def read_raw_line(self, index: int) -> str:
        """Read the raw JSONL line for one indexed row."""
        offset = self._offsets[index]
        with self.path.open("rb") as handle:
            handle.seek(offset)
            return handle.readline().decode("utf-8", errors="replace").rstrip("\r\n")

    def read_record(self, index: int) -> dict[str, t.Any] | None:
        """Parse and return the full JSON object for a row, if valid."""
        raw_line = self.read_raw_line(index)
        try:
            data = json.loads(raw_line)
        except JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
