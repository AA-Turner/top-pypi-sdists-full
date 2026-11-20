"""
The robot's stream over each of its uplinks - a Starlink terminal and a cellular modem, say (connect(..., lines=[...])):
a WorkerStream by each line, its connection bound to the line's interface; each request goes on every line that is
open, and its first answer is the one used.

In one sentence: each line opens a stream of its own (worker_stream.open_stream, bind=) → an observation post goes on
every open line with room, and counts as taken once the first line's server took it (a server keeps a number once:
StreamStore.put) → an act goes on every open line not still carrying the act before, under its one request id, which
the server runs once and answers on each line → the first answer is returned, the others read as they come and how much
later counted → a line that ended opens again in the background while the others carry everything; the stream ends
only when every line has.

WHY every observation on every line: an act waits at the server for the observations before it, so posted on one line
alone, an act that went on another would wait for that line.
WHY an act is never given a line still carrying the act before: a line that stopped answering would collect a queue of
acts behind it.

The cost: every observation and every act is sent on each line - two lines, twice the upload.
"""
from __future__ import annotations

import concurrent.futures
import statistics
import threading
import time
from collections import deque
from typing import Any, Callable, Optional, Sequence

import httpx

from . import worker_stream as _stream


REOPEN_S = 1.0

LATER_KEPT = 64


class _Line:
    """One uplink: its name (a network interface), its stream while it is open, and what it carried."""

    __slots__ = ("name", "stream", "opening", "acts", "first", "errors", "busy", "later_ms", "why")

    def __init__(self, name: str) -> None:
        self.name = name
        self.stream: Optional[_stream.WorkerStream] = None
        self.opening = False
        self.acts = 0
        self.first = 0
        self.errors = 0
        self.busy = 0
        self.later_ms: deque = deque(maxlen=LATER_KEPT)
        self.why: Optional[str] = None

    @property
    def alive(self) -> bool:
        stream = self.stream
        return stream is not None and stream.alive


class LinesStream:
    """
    The robot's stream over two or more lines (the module's docstring), as one WorkerStream to the transport that keeps
    it (worker_link.StreamLink): `said`, `alive`, `why_closed`, `submit`, `handle`, `room`, `ping`, `send_message`,
    `close`, and each line's numbers in `stats()`.

    names       the lines, by their network interface, in order: the first one's opening answer is `said`
    open_line   open_line(name, timeout_s, on_quiet) -> the WorkerStream of the line `name`, its connection bound to
                it; `on_quiet` is what the line's stream calls when it went silent
    timeout_s   how long the lines have to open: the first that does makes the stream; the others open meanwhile and
                after it. What the first line met is raised when none did
    on_reopen   on_reopen(name), called once a line that ended has opened again (a GPU's allow list told of it)
    """

    def __init__(self, names: Sequence[str], open_line: Callable[[str, float, Callable[[], None]], Any], *,
                 timeout_s: float, on_reopen: Optional[Callable[[str], None]] = None,
                 reopen_s: float = REOPEN_S) -> None:
        if len(names) < 2:
            raise ValueError(f"lines are two or more, and {list(names)} is {len(names)}")
        self._lines = [_Line(name) for name in names]
        self._open_line, self._on_reopen, self._reopen_s, self._timeout_s = open_line, on_reopen, reopen_s, timeout_s
        self._lock = threading.Lock()
        self._closed: Optional[str] = None
        self._pool = concurrent.futures.ThreadPoolExecutor(max_workers=4 * len(names), thread_name_prefix="seq-line")
        self.said: dict = {}
        opened, left, first_error = threading.Event(), [len(self._lines)], []

        def tried(line: _Line, error: Optional[BaseException]) -> None:
            with self._lock:
                left[0] -= 1
                if error is not None:
                    first_error.append(error)
                if line.alive or left[0] == 0:
                    opened.set()

        for line in self._lines:
            self._open(line, timeout_s, then=tried)
        opened.wait(timeout_s)
        if not any(line.alive for line in self._lines):
            self._end("no line opened")
            if first_error:
                raise first_error[0]
            raise _stream.NotOpened(f"no line of {self.names} opened in {timeout_s:.1f} s")
        threading.Thread(target=self._keep, daemon=True, name="seq-lines").start()

    @property
    def names(self) -> list:
        return [line.name for line in self._lines]


    def _open(self, line: _Line, timeout_s: float, *,
              then: Optional[Callable[[_Line, Optional[BaseException]], None]] = None) -> None:
        """Open `line` on a thread of its own; `then(line, error)` once it opened (error None) or failed."""
        with self._lock:
            if self._closed is not None or line.opening:
                return
            line.opening = True
        again = line.stream is not None or line.why is not None

        def run() -> None:
            error: Optional[BaseException] = None
            try:
                stream = self._open_line(line.name, timeout_s, lambda: self._silent(line))
            except Exception as exc:
                error = exc
                line.why = f"{type(exc).__name__}: {exc}"[:200]
            else:
                with self._lock:
                    closed = self._closed
                    if closed is None:
                        line.stream, line.why = stream, None
                        if not self.said:
                            self.said = stream.said
                if closed is not None:
                    stream.close(closed)
                elif again and self._on_reopen is not None:
                    try:
                        self._on_reopen(line.name)
                    except Exception:
                        pass
            finally:
                with self._lock:
                    line.opening = False
                if then is not None:
                    then(line, error)

        threading.Thread(target=run, daemon=True, name=f"seq-line-{line.name}").start()

    def _keep(self) -> None:
        """Every REOPEN_S: each line that ended, or did not open, opened again - until the stream ends."""
        while self._closed is None:
            time.sleep(self._reopen_s)
            if not self.alive:
                return
            for line in self._lines:
                if not line.alive and not line.opening:
                    if line.stream is not None and line.why is None:
                        line.why = line.stream.why_closed
                    self._open(line, self._timeout_s)

    def _silent(self, line: _Line) -> None:
        """A line's stream that went silent: closed, so it opens again (_keep), the others carrying meanwhile."""
        stream = line.stream
        if stream is not None:
            stream.close(f"line {line.name} went silent")

    def _open_lines(self) -> list:
        return [line for line in self._lines if line.alive]


    @property
    def alive(self) -> bool:
        """Whether a line is open. Once none is, the stream has ended, its lines closed - a line opening again included:
        the transport opens it anew, as a stream that ended, and what was on its way goes again as after any."""
        if self._closed is not None:
            return False
        if any(line.alive for line in self._lines):
            return True
        self._end("every line ended: " + "; ".join(
            f"{line.name}: {line.why or (line.stream.why_closed if line.stream is not None else None) or 'ended'}"
            for line in self._lines))
        return False

    @property
    def why_closed(self) -> Optional[str]:
        return self._closed

    def submit(self, method: str, path: str, headers: list, body: bytes, trace: Any = None, *, control: bool = False,
               silent: bool = False, on_done: Optional[Callable[[Any], None]] = None, key: Optional[str] = None,
               after: Optional[str] = None) -> Any:
        """One request queued on every open line (an observation post on those with room, where any has), never
        waiting: a pending done as the first line's is done well - an observation post its server took, an answer -
        or, once every line's is done and none was, with the first line's refusal, else its error. StreamClosed with no
        line open."""
        lines = self._open_lines()
        if not lines:
            raise _stream.StreamClosed(self._closed or "no line is open")
        if not control:
            lines = [line for line in lines if line.stream.room(0.0)] or lines
        merged = _stream._Pending(0, trace, control, silent, on_done)
        merged.begun = True
        state = {"left": len(lines), "refused": None, "error": None, "done": False}

        def done(pending: Any, line: _Line) -> None:
            well = pending.error is None and (pending.answer is None or not silent)
            with self._lock:
                if state["done"]:
                    return
                if not well:
                    line.errors += pending.error is not None
                    if pending.error is None and state["refused"] is None:
                        state["refused"] = pending
                    elif pending.error is not None and state["error"] is None:
                        state["error"] = pending.error
                    state["left"] -= 1
                    if state["left"] > 0:
                        return
                    pending = state["refused"]
                state["done"] = True
                merged.answer = pending.answer if pending is not None else None
                merged.error = state["error"] if pending is None else None
                if pending is not None:
                    merged.began_at, merged.sent_at = pending.began_at, pending.sent_at
            merged.sent.set()
            merged._finish()

        taken, closed = 0, []
        for line in lines:
            try:
                line.stream.submit(method, path, headers, body, None, control=control, silent=silent,
                                   on_done=lambda pending, line=line: done(pending, line), key=key, after=after)
                taken += 1
            except _stream.StreamClosed as exc:
                closed.append((line, exc))
        if not taken:
            raise _stream.StreamClosed(self._closed or "no line took it")
        for line, exc in closed:
            failed = _stream._Pending(0, None, control, silent, None)
            failed.error = exc
            done(failed, line)
        return merged

    def handle(self, request: httpx.Request) -> httpx.Response:
        """One httpx request on every open line - an act on those not still carrying the act before -, each on a thread
        of its own: the first answer, the others read as they come and how much later counted. What the first line met
        when every line failed."""
        act = request.method == "POST" and request.url.path == "/act"
        with self._lock:
            lines = self._open_lines()
            if act:
                lines = [line for line in lines if not line.busy] or lines
                for line in lines:
                    line.busy += 1
                    line.acts += 1
        if not lines:
            raise _stream.Unwritten(self._closed or "no line is open")
        request.read()
        asked: dict = {}
        for line in lines:
            try:
                asked[self._pool.submit(self._one, line, request, act)] = line
            except RuntimeError:
                if act:
                    with self._lock:
                        line.busy -= 1
        if not asked:
            raise _stream.Unwritten(self._closed or "the stream ended")
        first_error: Optional[BaseException] = None
        for future in concurrent.futures.as_completed(asked):
            try:
                response = future.result()
            except Exception as exc:
                first_error = first_error or exc
                continue
            line, came = asked[future], time.monotonic()
            if act:
                with self._lock:
                    line.first += 1
            for other, behind in asked.items():
                if other is not future:
                    other.add_done_callback(lambda f, behind=behind, came=came: self._later(behind, came, f))
            return response
        assert first_error is not None
        raise first_error

    def _one(self, line: _Line, request: httpx.Request, act: bool) -> httpx.Response:
        stream = line.stream
        try:
            if stream is None:
                raise _stream.Unwritten(f"line {line.name} is not open")
            return stream.handle(request)
        except Exception:
            with self._lock:
                line.errors += 1
            raise
        finally:
            if act:
                with self._lock:
                    line.busy -= 1

    def _later(self, line: _Line, came: float, future: Any) -> None:
        if future.exception() is None:
            with self._lock:
                line.later_ms.append((time.monotonic() - came) * 1000.0)

    def room(self, timeout_s: float = 0.0) -> bool:
        """Whether an open line has room for another observation post, waited for up to `timeout_s`; True with none
        open, so a caller goes on to meet that."""
        end = time.monotonic() + timeout_s
        while True:
            lines = self._open_lines()
            if not lines or any(line.stream.room(0.0) for line in lines):
                return True
            left = end - time.monotonic()
            if left <= 0:
                return False
            lines[0].stream.room(min(left, 0.005))

    def ping(self) -> None:
        for line in self._open_lines():
            line.stream.ping()

    def send_message(self, message: dict) -> None:
        """`message` on every open line. StreamClosed when no line took it."""
        sent = False
        for line in self._open_lines():
            try:
                line.stream.send_message(message)
                sent = True
            except _stream.StreamClosed:
                pass
        if not sent:
            raise _stream.StreamClosed(self._closed or "no line is open")

    def close(self, why: str = "the robot's side closed the stream") -> None:
        self._end(why)

    def _end(self, why: str) -> None:
        with self._lock:
            if self._closed is not None:
                return
            self._closed = why
            streams = [line.stream for line in self._lines if line.stream is not None]
        for stream in streams:
            stream.close(why)
        self._pool.shutdown(wait=False)

    def stats(self) -> list:
        """Each line's numbers, in order: its interface, whether it is open (and why not), the acts sent on it, how
        many it answered first, its failed requests, and how much later than the first its other answers came."""
        with self._lock:
            return [{"line": line.name, "open": line.alive, **({} if line.alive else {"why": line.why}),
                     "acts": line.acts, "first": line.first, "errors": line.errors,
                     "later_ms_p50": round(statistics.median(line.later_ms), 1) if line.later_ms else None}
                    for line in self._lines]
