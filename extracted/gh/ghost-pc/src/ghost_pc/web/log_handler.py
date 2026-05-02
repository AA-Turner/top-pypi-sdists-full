"""Dashboard log handler — ring buffer for real-time log streaming."""

from __future__ import annotations

import asyncio
import logging
from collections import deque
from typing import Any


class DashboardLogHandler(logging.Handler):
    """Logging handler that stores recent records in a ring buffer.

    Dashboard WebSocket clients subscribe to receive new records in real time.
    REST clients can poll ``get_recent()`` for the latest entries.
    """

    def __init__(self, max_records: int = 500) -> None:
        super().__init__()
        self._buffer: deque[dict[str, Any]] = deque(maxlen=max_records)
        self._subscribers: list[asyncio.Queue[dict[str, Any]]] = []

    def emit(self, record: logging.LogRecord) -> None:
        """Store a log record and push to subscribers."""
        entry = {
            "timestamp": record.created,
            "level": record.levelname,
            "name": record.name,
            "message": self.format(record),
        }
        self._buffer.append(entry)

        # Non-blocking push to subscribers
        dead: list[asyncio.Queue[dict[str, Any]]] = []
        for queue in self._subscribers:
            try:
                queue.put_nowait(entry)
            except asyncio.QueueFull:
                # Drop oldest if queue is full
                try:
                    queue.get_nowait()
                    queue.put_nowait(entry)
                except (asyncio.QueueEmpty, asyncio.QueueFull):
                    dead.append(queue)
        for q in dead:
            if q in self._subscribers:
                self._subscribers.remove(q)

    def subscribe(self) -> asyncio.Queue[dict[str, Any]]:
        """Create a new subscriber queue for real-time log push."""
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=100)
        self._subscribers.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[dict[str, Any]]) -> None:
        """Remove a subscriber queue."""
        if queue in self._subscribers:
            self._subscribers.remove(queue)

    def get_recent(self, count: int = 50) -> list[dict[str, Any]]:
        """Return the most recent log entries."""
        entries = list(self._buffer)
        return entries[-count:]
