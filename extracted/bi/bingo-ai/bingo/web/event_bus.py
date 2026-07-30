"""Thread-safe event bridge: sync AgentLoop ↔ async FastAPI/WebSocket."""
from __future__ import annotations

import json
import queue
import threading
from typing import Any


class EventBus:
    """Publish/subscribe bridge.

    AgentLoop (sync thread) → push_event() / push_hint()
    FastAPI WS handlers (async thread) → subscribe() / drain_hints()
    """

    def __init__(self) -> None:
        self._subscribers: list[queue.Queue] = []
        self._hint_queue: queue.Queue = queue.Queue(maxsize=100)
        self._lock = threading.Lock()
        self._findings_snapshot: list[dict] = []
        self._stats_snapshot: dict[str, Any] = {}

    # ── publish ──────────────────────────────────────────────────────────────

    def push_event(self, type: str, data: dict) -> None:
        """Emit JSON event to all WebSocket subscribers."""
        msg = json.dumps({"type": type, "data": data}, ensure_ascii=False, default=str)
        with self._lock:
            dead: list[queue.Queue] = []
            for sub in self._subscribers:
                try:
                    sub.put_nowait(msg)
                except queue.Full:
                    dead.append(sub)
            for d in dead:
                try:
                    self._subscribers.remove(d)
                except ValueError:
                    pass
        if type == "finding":
            self._findings_snapshot.append(data)
        elif type == "stats":
            self._stats_snapshot = data

    def push_hint(self, text: str) -> None:
        """Queue a hint string for AgentLoop to inject."""
        try:
            self._hint_queue.put_nowait(text)
        except queue.Full:
            pass

    # ── subscribe ────────────────────────────────────────────────────────────

    def subscribe(self) -> queue.Queue:
        q: queue.Queue = queue.Queue(maxsize=500)
        with self._lock:
            self._subscribers.append(q)
        return q

    def unsubscribe(self, q: queue.Queue) -> None:
        with self._lock:
            try:
                self._subscribers.remove(q)
            except ValueError:
                pass

    def drain_hints(self) -> list[str]:
        """Consume and return all pending hints (called by AgentLoop)."""
        hints: list[str] = []
        while True:
            try:
                hints.append(self._hint_queue.get_nowait())
            except queue.Empty:
                break
        return hints

    # ── snapshots ─────────────────────────────────────────────────────────────

    def get_findings(self) -> list[dict]:
        return list(self._findings_snapshot)

    def get_stats(self) -> dict[str, Any]:
        return dict(self._stats_snapshot)
