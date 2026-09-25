"""Bounded process-local runtime diagnostics, independent of file logging."""

import threading
import traceback
import typing as t
from collections import deque
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

MAX_MESSAGE_CHARS = 8192
MAX_QUERY_ENTRIES = 200
_LEVELS = {
    "TRACE": 5,
    "DEBUG": 10,
    "INFO": 20,
    "SUCCESS": 25,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


class RuntimeLogEntry(BaseModel):
    """A captured record; sequence numbers are scoped to one process instance."""

    model_config = ConfigDict(frozen=True)
    sequence: int
    timestamp: datetime
    level: str
    level_no: int
    source: str
    message: str
    truncated: bool


class RuntimeLogPage(BaseModel):
    """A bounded query result with an explicit replay cursor."""

    instance_id: str
    next_cursor: int
    reset: bool
    gap: bool
    entries: list[RuntimeLogEntry]


class RuntimeLogBuffer:
    """Thread-safe diagnostic history shared by HTTP and agent consumers."""

    def __init__(self, maxlen: int = 2000) -> None:
        self.instance_id = str(uuid4())
        self._entries: deque[RuntimeLogEntry] = deque(maxlen=maxlen)
        self._sequence = 0
        self._lock = threading.Lock()

    def capture(self, message: t.Any) -> None:
        """Capture loguru records without formatting exception local variables."""
        record = message.record
        text = record["message"]
        exc = record.get("exception")
        if exc and exc.value:
            text += "\n" + "".join(traceback.format_exception(exc.type, exc.value, exc.traceback))
        with self._lock:
            self._sequence += 1
            self._entries.append(
                RuntimeLogEntry(
                    sequence=self._sequence,
                    timestamp=record["time"],
                    level=record["level"].name,
                    level_no=record["level"].no,
                    source=(record["name"] or "loguru")[:256],
                    message=text[:MAX_MESSAGE_CHARS],
                    truncated=len(text) > MAX_MESSAGE_CHARS,
                )
            )

    def query(
        self,
        *,
        after: int | None = None,
        instance_id: str | None = None,
        limit: int = 100,
        level: str = "DEBUG",
        text: str = "",
    ) -> RuntimeLogPage:
        """Tail initially, then page forward. Filters never stall the cursor."""
        level_no = _LEVELS.get(level.upper())
        if level_no is None or not 1 <= limit <= MAX_QUERY_ENTRIES:
            raise ValueError("Invalid log level or limit")
        if (after is not None and after < 0) or len(text) > 256:
            raise ValueError("Invalid cursor or search text")
        with self._lock:
            entries = list(self._entries)
            latest = self._sequence
        reset = (instance_id is not None and instance_id != self.instance_id) or (
            after is not None and after > latest
        )
        if reset:
            after = None
        gap = bool(after is not None and entries and after < entries[0].sequence - 1)
        needle = text.casefold()
        matches = [
            entry
            for entry in entries
            if (after is None or entry.sequence > after)
            and entry.level_no >= level_no
            and (needle in entry.message.casefold() or needle in entry.source.casefold())
        ]
        selected = matches[-limit:] if after is None else matches[:limit]
        cursor = selected[-1].sequence if after is not None and len(matches) > limit else latest
        return RuntimeLogPage(
            instance_id=self.instance_id, next_cursor=cursor, reset=reset, gap=gap, entries=selected
        )


runtime_log_buffer = RuntimeLogBuffer()
