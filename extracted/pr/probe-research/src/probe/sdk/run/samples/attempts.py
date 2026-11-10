"""In-flight attempts: each one's task and whole progress snapshot, and which beats go now (an attempt's first progress
and each new phase at once, the rest one per attempt per 30 s; a held beat goes when its window opens).
`last_progress_at` moves only on a change (rl-next B.4)."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Mapping
from typing import Any

from ....generated.samples import PartRole

#: At most one beat per attempt per this many seconds (an attempt's first progress and a new phase go at once).
HEARTBEAT_MIN_SECONDS = 30.0
#: Attempts remembered at once; the oldest is forgotten past it (a beat then goes at once).
ATTEMPTS_REMEMBERED = 100_000
#: How often the flusher looks for held beats whose window opened.
FLUSH_EVERY_SECONDS = 5.0
#: The snapshot's fields whose change is real progress (a model call, a tool call, a phase change).
PROGRESS_FIELDS = ("phase", "turns", "tokens", "activity")


class AttemptBeats:
    """Which beats go now, and each attempt's progress snapshot. ``clock`` is monotonic seconds (a test pins it);
    ``send_held(key, fields)`` sends a held beat once its window opens (from the flusher's thread)."""

    def __init__(self, clock: Callable[[], float] = time.monotonic,
                 send_held: Callable[[str, dict], None] | None = None) -> None:  # fmt: skip
        self._clock = clock
        self._send_held = send_held
        self._last_sent: dict[str, float] = {}
        self._held: dict[str, dict] = {}
        self._tasks: dict[str, dict] = {}
        self._snapshots: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._flusher: threading.Thread | None = None
        self._stopped = threading.Event()

    def record_start(self, key: str, task: dict | None = None) -> None:
        """An attempt started (its start part went): its first beat waits a window; ``task`` (its
        `task_key` and `scenario`) rides every beat."""
        with self._lock:
            self._remember(key, self._clock())
            if task:
                self._tasks[key] = dict(task)

    def update_progress(self, key: str, changes: Mapping[str, Any], at: str) -> bool:
        """Merge ``changes`` (phase, turns, tokens, activity) into the snapshot; a value that changed is progress and
        moves `last_progress_at` to ``at`` (the producer's clock). True when the beat is news that goes at once: the
        attempt's first progress, or a new phase (a 4 s rollout otherwise ended before its first beat)."""
        with self._lock:
            snapshot = self._snapshots.setdefault(key, {})
            is_first = not any(snapshot.get(name) is not None for name in PROGRESS_FIELDS)
            moved = [name for name in PROGRESS_FIELDS
                     if changes.get(name) is not None and snapshot.get(name) != changes[name]]  # fmt: skip
            snapshot.update({name: changes[name] for name in moved})
            given = changes.get("last_progress_at")
            if given is not None and given != snapshot.get("last_progress_at"):
                snapshot["last_progress_at"] = given  # when it happened, as the framework saw it
            elif moved:
                snapshot["last_progress_at"] = at
            return bool(moved) and (is_first or "phase" in moved)

    def get_snapshot(self, key: str) -> dict:
        with self._lock:
            return dict(self._snapshots.get(key, {}))

    def take_beat(self, key: str, fields: dict, *, is_news: bool = False) -> dict | None:
        """The beat to send now (held fields merged under these), or None to hold it (the flusher sends it when
        the window opens). ``is_news`` (`update_progress`'s answer) sends it now whatever the window."""
        now = self._clock()
        with self._lock:
            last = self._last_sent.get(key)
            if not is_news and last is not None and now - last < HEARTBEAT_MIN_SECONDS:
                self._held[key] = {**self._held.get(key, {}), **fields}
                self._start_flusher()
                return None
            merged = {**self._held.pop(key, {}), **fields}
            self._remember(key, now)
            return merged

    def take_due(self) -> list[tuple[str, dict]]:
        """Held beats whose window has opened, taken (each to send with its snapshot)."""
        now = self._clock()
        with self._lock:
            due = [key for key in self._held
                   if now - self._last_sent.get(key, now - HEARTBEAT_MIN_SECONDS) >= HEARTBEAT_MIN_SECONDS]  # fmt: skip
            taken = []
            for key in due:
                taken.append((key, self._held.pop(key)))
                self._remember(key, now)
            return taken

    def fill_task(self, part: Any, role: str) -> Any:
        """An attempt part (a beat, an error, the end) that names no task gets its start's: a newest part
        without one left the attempt unlisted. Other parts are returned as they are."""
        if not isinstance(part, Mapping) or (part.get("role") or role) != PartRole.ATTEMPT or part.get("task_key"):
            return part
        with self._lock:
            task = self._tasks.get(str(part.get("key")))
        return {**task, **part} if task else part

    def forget(self, key: str) -> None:
        """The attempt finished: its held beat and snapshot are dropped (its end or sample replaces them)."""
        with self._lock:
            self._last_sent.pop(key, None)
            self._held.pop(key, None)
            self._tasks.pop(key, None)
            self._snapshots.pop(key, None)

    def stop(self) -> None:
        """The flusher ends (held beats are dropped: the run is closing)."""
        self._stopped.set()

    def _remember(self, key: str, at: float) -> None:
        self._last_sent.pop(key, None)
        self._last_sent[key] = at
        while len(self._last_sent) > ATTEMPTS_REMEMBERED:
            oldest = next(iter(self._last_sent))
            self._last_sent.pop(oldest)
            self._held.pop(oldest, None)
            self._tasks.pop(oldest, None)
            self._snapshots.pop(oldest, None)

    def _start_flusher(self) -> None:
        """Under the lock: one daemon thread while beats are held; it ends when none are."""
        if self._send_held is None or self._stopped.is_set():
            return
        if self._flusher is not None and self._flusher.is_alive():
            return
        self._flusher = threading.Thread(target=self._flush_held, name="probe-sample-beats", daemon=True)
        self._flusher.start()

    def _flush_held(self) -> None:
        while not self._stopped.wait(FLUSH_EVERY_SECONDS):
            for key, fields in self.take_due():
                try:
                    self._send_held(key, fields)  # type: ignore[misc]
                except Exception:  # noqa: BLE001 -- fail open: a held beat that cannot go is dropped
                    pass
            with self._lock:
                if not self._held:
                    self._flusher = None
                    return
