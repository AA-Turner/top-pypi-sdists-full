"""Immutable transport identity for structured application output."""

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import ClassVar, Literal

from labqoat.json_document import JsonDocument, JsonValue


@dataclass(frozen=True)
class RunLogRecord:
    """Validate metadata before it joins the assignment's replayable telemetry queue.

    A log line is evidence, not work: one that is too long is shortened and oversized data is replaced by a
    note of what was dropped, so a diagnostic can never be what fails a run.
    """

    limit: ClassVar[int] = 16384

    content: str
    level: Literal["debug", "info", "progress", "warning", "error", "critical"] = "info"
    stream: Literal["stdout", "stderr", "logging", "milestone", "progress"] = "stdout"
    produced_at: datetime | None = None
    logger: str | None = None
    data: dict[str, JsonValue] = field(default_factory=dict)

    def to_dict(self) -> JsonDocument:
        """Snapshot bounded JSON metadata and assign UTC producer time before delivery."""
        stamp = self.produced_at or datetime.now(UTC)
        if stamp.utcoffset() is None:
            raise ValueError("Log producer timestamps must include a timezone")
        if not self.content:
            raise ValueError("Log content must not be empty")
        if self.logger is not None and len(self.logger) > 256:
            raise ValueError("Logger names must not exceed 256 characters")
        encoded = json.dumps(self.data, allow_nan=False, ensure_ascii=False)
        size = len(encoded.encode("utf-8"))
        if size > self.limit:
            encoded = json.dumps({"truncated": True, "bytes": size, "keys": sorted(self.data)[:32]})
        document = JsonDocument(
            content=self.content if len(self.content) <= self.limit else self.content[: self.limit - 1] + "…",
            level=self.level,
            stream=self.stream,
            produced_at=stamp.astimezone(UTC).isoformat(),
            data=JsonDocument.expect_dict(json.loads(encoded)),
        )
        if self.logger is not None:
            document["logger"] = self.logger
        return document
