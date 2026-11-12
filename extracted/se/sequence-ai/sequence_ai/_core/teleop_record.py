"""
What a robot connected to "teleop" alone keeps while its Record is on: no worker sees its steps,
so it writes them itself, the same JSONL lines a worker's capture writes, so `seq data export` and the Storage page read
them alike.

In one sentence: its link says Record is on and brings signed upload URLs → each step it observes and each chunk of a
person's it played becomes one JSON line in a buffer → the buffer goes, an object at a time, straight to storage, at
FLUSH_LINES lines or every FLUSH_S, on a thread of its own, one URL always kept back and the link's next round a short one
when only that is left → as its connect closes, every line it holds is written before close() returns, its link going on
for the URLs that takes: the episode whole, as the docs say - or Unavailable, saying how many steps are not.
WHY best-effort: a full buffer (a robot's uplink behind its cameras) drops lines and counts them, and never slows its
loop - as a worker's capture does.

WHY a person's played chunks alone: a chunk never played is no step the robot took, and the kept episodes are what it
did.
"""
from __future__ import annotations

import base64
import collections
import json
import logging
import threading
import time
from typing import Any, Callable, Optional

from ..errors import Unavailable

FLUSH_LINES = 50
FLUSH_S = 30.0
MAX_BUFFER_BYTES = 64 * 1024 * 1024



OBJECT_MOST_BYTES = 8 * 1024 * 1024

_SAY_DROPS_S = 10.0


_BACKOFF_S = 0.5
_BACKOFF_MOST_S = 8.0




WANT_URLS = 16
URL_GOOD_S = 45 * 60.0
_PUT_S = 60.0




_STALL_S = 60.0
_CLOSING_MOST_S = 600.0
_log = logging.getLogger("sequence_ai.teleop")


def _jsonable(value: Any) -> Any:
    """`value` as JSON carries it: an array as {"__ndarray__": base64, "dtype", "shape"}, bytes as {"__bytes__": base64}, a
    numpy scalar as its number, a tuple as a list, a map's keys as strings (harness/capture.py's, line for line)."""
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (bytes, bytearray, memoryview)):
        return {"__bytes__": base64.b64encode(bytes(value)).decode()}
    if type(value).__module__ == "numpy":
        if hasattr(value, "shape") and hasattr(value, "tobytes") and getattr(value, "ndim", 0) > 0:
            import numpy as np

            a = np.ascontiguousarray(value)
            return {"__ndarray__": base64.b64encode(a.tobytes()).decode(), "dtype": a.dtype.str, "shape": list(a.shape)}
        return value.item()
    return value


def _http_put(url: str, data: bytes, timeout_s: float) -> bool:
    import httpx

    try:
        r = httpx.put(url, content=data, timeout=timeout_s)
    except Exception:
        return False
    return r.status_code in (200, 201)


class Recording:
    """One connect()'s recording (module docstring)."""

    def __init__(self, put: Optional[Callable[[str, bytes, float], bool]] = None) -> None:
        self._lock = threading.Lock()
        self.on = False
        self._put = put or _http_put
        self._urls: collections.deque = collections.deque()
        self._lines: list = []
        self._bytes = 0
        self._last = time.monotonic()
        self._flushing = False
        self._writer: Optional[threading.Thread] = None
        self._closing = False
        self._urls_came = threading.Event()
        self.failed_writes = 0
        self.dropped_steps = 0
        self._said_drops = 0.0
        self._said_fails = 0.0
        self._backoff = 0.0
        self._wake = threading.Event()
        self.written = 0
        self.dropped = 0
        self._full = False

    def configure(self, on: Any, urls: Any = (), full: Any = False) -> None:
        """What a round of its link says: whether Record is on, upload URLs, and whether the account's storage is full -
        said here once each time it fills, or what it records would go in silence. Off, what is buffered goes: it was to
        be kept only while it is on."""
        now = time.monotonic()
        with self._lock:
            newly_full, self._full = bool(full) and not self._full, bool(full)
            self.on = bool(on)
            if not self.on:
                self._lines, self._bytes = [], 0
            came = [(url, now) for url in urls or () if isinstance(url, str)]
            self._urls.extend(came)
            while self._urls and now - self._urls[0][1] > URL_GOOD_S:
                self._urls.popleft()
        if came:
            self._urls_came.set()
        if newly_full:
            _log.warning("this robot's Record is on, but its account's storage is at its limit: nothing new is kept until "
                         "the limit is raised or something is deleted")
        self._flush_soon()

    def wanted(self) -> int:
        """How many upload URLs its next round asks for."""
        with self._lock:
            return max(0, WANT_URLS - len(self._urls)) if self.on else 0

    def needs_urls(self) -> bool:
        """Record is on and its writes wait on a URL - none in hand, or only the one kept back for the closing write with
        lines waiting - and one is to come: a round's end is when URLs arrive, so the next is a short one, or a recording
        that closed before a whole round had passed would have written nothing, and one whose URLs ran out piled its steps
        up for a round."""
        with self._lock:
            if not self.on or self._full:
                return False
            return not self._urls or (len(self._urls) <= WANT_URLS // 2 and bool(self._lines))

    def observed(self, episode: str, step: int, observation: Any, driver: str, by: Optional[str]) -> None:
        """One step it observed, as it goes: its Video, Depth and Tactile items already their encoders' maps."""
        self._push({"ts": round(time.time(), 3), "kind": "observe", "episode_id": episode, "step": step,
                    "observation": observation, "driver": driver, "operator": by})

    def played(self, said: dict) -> None:
        """A person's chunk the robot played (teleop_robot.Driven's say of it)."""
        self._push({"ts": round(time.time(), 3), "kind": "act", "episode_id": said.get("episode"), "step": said.get("step"),
                    "outputs": said.get("chunk"), "driver": "human", "operator": said.get("by"), "path": "direct"})

    def label(self, episode: str, success: bool, notes: str) -> None:
        """How the robot said its episode went."""
        self._push({"ts": round(time.time(), 3), "kind": "label", "episode_id": episode, "success": bool(success),
                    "notes": notes})

    def _push(self, record: dict) -> None:
        if not self.on:
            return
        try:
            line = json.dumps(_jsonable(record), separators=(",", ":")).encode() + b"\n"
        except (TypeError, ValueError):
            self.dropped += 1
            return
        say = None
        with self._lock:
            if not self.on:
                return
            if self._bytes + len(line) > MAX_BUFFER_BYTES:
                self.dropped += 1
                self.dropped_steps += int(record.get("kind") == "observe")
                now = time.monotonic()
                if now - self._said_drops >= _SAY_DROPS_S:
                    self._said_drops, say = now, self.dropped_steps
            else:
                self._lines.append(line)
                self._bytes += len(line)
            due = len(self._lines) >= FLUSH_LINES or time.monotonic() - self._last >= FLUSH_S
        if say is not None:
            _log.warning("this robot's recording is dropping steps: its uplink is behind its cameras and its buffer "
                         "(%d MiB) is full; steps dropped so far: %d", MAX_BUFFER_BYTES // (1024 * 1024), say)
        if due:
            self._flush_soon()

    def _flush_soon(self) -> None:
        """A write on a thread of its own, one at a time: a write takes as long as the robot's uplink does. One URL is kept
        back for the last write, as the robot closes (close)."""
        with self._lock:
            if self._flushing or self._closing or not self._lines or len(self._urls) <= 1:
                return
            self._flushing = True
            self._writer = writer = threading.Thread(target=self._flush_all, daemon=True, name="seq-teleop-record")
        writer.start()

    def _a_whole_object_waits(self) -> bool:
        with self._lock:
            return (len(self._lines) >= FLUSH_LINES or self._bytes >= OBJECT_MOST_BYTES
                    or (bool(self._lines) and time.monotonic() - self._last >= FLUSH_S))

    def _flush_all(self) -> None:
        """Writes on its thread while a whole object's worth waits: what is left of a backlog goes with the next, or the
        closing write - not as one object a write, which a robot written to without pause made of every few steps."""
        try:
            while self._a_whole_object_waits() and self._write(_PUT_S, keep=1):
                with self._lock:
                    wait = self._backoff
                if wait and self._wake.wait(wait):
                    break
        finally:
            with self._lock:
                self._flushing = False

    def _write(self, timeout_s: float, keep: int = 0) -> bool:
        """One object written - the oldest lines, up to OBJECT_MOST_BYTES (one at least) - with one URL, `keep` of them left
        in hand: whether there may be more to write."""
        with self._lock:
            if not self._lines or len(self._urls) <= keep:
                return False
            url, _ = self._urls.popleft()
            take, size = 0, 0
            for line in self._lines:
                if take and size + len(line) > OBJECT_MOST_BYTES:
                    break
                take, size = take + 1, size + len(line)
            lines = self._lines[:take]
            del self._lines[:take]
            self._bytes -= size
            data, n = b"".join(lines), take
            self._last = time.monotonic()
        if self._put(url, data, timeout_s):
            with self._lock:
                self.written += n
                self._backoff = 0.0
        else:
            with self._lock:
                self._lines[:0] = lines
                self._bytes += len(data)
                self.failed_writes += 1
                self._backoff = min(_BACKOFF_MOST_S, self._backoff * 2 or _BACKOFF_S)
                now = time.monotonic()
                say = now - self._said_fails >= _SAY_DROPS_S
                if say:
                    self._said_fails = now
                failed, waiting = self.failed_writes, len(self._lines)
            if say:
                _log.warning("this robot's recording could not write to storage (%d tries failed so far): its %d lines "
                             "wait, and go as storage takes them", failed, waiting)
        return True

    def close(self) -> None:
        """Every line it holds written before its connect goes - the episode whole: the write under way waited for, then
        the rest, a URL at a time as its link brings them (the link goes on until this returns), a write that failed made
        again with the next. Unavailable, saying how many steps and lines are not written - counted dropped - where
        storage took none of it for _STALL_S, or _CLOSING_MOST_S went by."""
        with self._lock:
            self._closing = True
            writer, waiting = self._writer, len(self._lines)
        self._wake.set()
        if waiting > FLUSH_LINES:
            _log.info("writing the last %d lines of this robot's recording before it closes", waiting)
        began = progressed = time.monotonic()
        if writer is not None:
            writer.join(_STALL_S)
        while True:
            with self._lock:
                if not self._lines or not self.on:
                    break
                have = bool(self._urls)
                if not have:
                    self._urls_came.clear()
            now = time.monotonic()
            if now - progressed > _STALL_S or now - began > _CLOSING_MOST_S:
                break
            if have:
                before = self.written
                self._write(min(_PUT_S, max(1.0, _STALL_S - (now - progressed))))
                if self.written > before:
                    progressed = time.monotonic()
                else:
                    with self._lock:
                        wait = self._backoff
                    time.sleep(min(wait, max(0.0, _STALL_S - (time.monotonic() - progressed))))
            else:
                self._urls_came.wait(0.5)
        with self._lock:
            left = self._lines
            self._lines, self._bytes, self.on = [], 0, False
            self.dropped += len(left)
            dropped_before, dropped = self.dropped_steps, self.dropped
        steps = sum(1 for line in left if b'"kind":"observe"' in line)
        if left or dropped:
            said = []
            if left:
                stalled = time.monotonic() - progressed > _STALL_S
                said.append(f"could not write its last {steps} steps ({len(left)} lines) before it closed: "
                            + (f"storage took none of it in {_STALL_S:.0f} s" if stalled
                               else f"{_CLOSING_MOST_S:.0f} s were not enough"))
            if dropped_before:
                said.append(f"dropped {dropped_before} steps while it recorded, its uplink behind its cameras and its "
                            f"buffer ({MAX_BUFFER_BYTES // (1024 * 1024)} MiB) full")
            raise Unavailable(f"this robot's recording {'; and '.join(said)}",
                              details={"reason": "recording_unwritten", "steps": steps + dropped_before, "lines": dropped})
