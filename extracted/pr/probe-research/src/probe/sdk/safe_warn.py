"""The SDK's one non-raising warning channel.

Telemetry may never become a training run's cause of death. That rule was
learned expensively: a live campaign disabled Probe mid-flight after SDK writes
killed worker processes, and three successive fixes each reopened the wound from
a new direction -- the last one in the very line written to close it, because it
used ``warnings.warn`` to report that a close had failed.

``warnings.warn`` RAISES under ``-W error``, ``PYTHONWARNINGS=error``, or any
``filterwarnings("error")`` -- settings several ML harnesses turn on by default.
So every diagnostic the SDK emits from a write path, a close path, or an
``except`` block is a live exception waiting for the right environment. Two of
those were worse than noise: one made a SUCCESSFUL twelve-hour run die at its
closing brace, and one sat ahead of a fail-open recovery and ate it.

Separate from :mod:`probe.sdk.diagnostics`, which is the crash REPORTER (it
captures a traceback into a run-scoped span). This module is the far smaller
thing underneath: making the SDK's own warnings incapable of killing a caller.
Kept apart because it is imported on the enqueue path, which runs beside a
training loop -- it is stdlib-only and imports nothing else in the package when
it loads, so it costs a training loop nothing to pull in.

Deliberately still ``warnings.warn`` underneath rather than ``logging``: users
already filter and capture Probe's warnings that way, and ``pytest.warns`` keeps
working. The ONLY thing taken away is the ability of a warning to terminate the
caller.

Nor to HANG it. A SIGTERM close (:mod:`probe.sdk.preempt`) runs on a worker
thread while the main thread sits parked in the signal handler, and CPython
runs that handler INSIDE a ``print``: ``BufferedWriter``'s flush checks for
signals between writes with the stream's lock held. The main thread then holds
``sys.stdout``'s or ``sys.stderr``'s lock until the process dies, and the
close -- flushing the streams before it stops the log capture, or printing a
warning -- waited on it for the whole budget, so the run never closed (release
gate 36503631939). On a thread inside :func:`streams_off_limits` a warning goes
straight to file descriptor 2 instead, as preempt's own notes do, and the log
capture skips that flush.
"""

from __future__ import annotations

import contextlib
import os
import sys
import threading
import warnings

#: What a diagnostic must never swallow: the user's Ctrl-C and a deliberate
#: exit. Everything else -- a filter turning warnings into errors, a broken
#: hook, a torn-down interpreter -- is ours to absorb.
_STOPS = (KeyboardInterrupt, SystemExit)

_thread = threading.local()


@contextlib.contextmanager
def streams_off_limits():
    """While inside, this thread's warnings (and :func:`streams_allowed`'s
    callers) never touch ``sys.stdout``/``sys.stderr``: another thread may
    hold their locks for good. For the SIGTERM close's worker thread."""
    before = getattr(_thread, "off_limits", False)
    _thread.off_limits = True
    try:
        yield
    finally:
        _thread.off_limits = before


def streams_allowed() -> bool:
    """False on a thread inside :func:`streams_off_limits`."""
    return not getattr(_thread, "off_limits", False)


def warn(message: str, *, stacklevel: int = 2) -> None:
    """Emit a warning that cannot raise, whatever the warning filters say.

    ``stacklevel`` is counted from the CALLER of this function, matching the
    convention of the ``warnings.warn`` calls this replaces -- the extra frame
    this wrapper introduces is added back internally.

    The broad ``except BaseException`` is the entire point, not an oversight:
    a filter turning warnings into errors, a broken ``showwarning`` hook, and a
    ``__del__``-time call after the warnings module has been torn down are all
    ways this can throw, and none of them may reach the caller.

    Except a Ctrl-C or a ``sys.exit`` (`_STOPS`), which propagate: a
    KeyboardInterrupt that lands while a warning prints -- a delivery notice
    beside a training loop, a DDP worker's death signal mid-close -- is the
    user stopping the process, and swallowing it let training carry on.
    """
    try:
        if not streams_allowed():
            _write_fd2(message, stacklevel + 1)
            return
        warnings.warn(message, stacklevel=stacklevel + 1)
    except _STOPS:
        raise
    except BaseException:  # noqa: BLE001 -- a diagnostic may never be fatal
        pass


def _write_fd2(message: str, stacklevel: int) -> None:
    """The warning as ``warnings`` would print it, straight to fd 2: no stream
    object, so no lock another thread can hold. The filters are not
    consulted -- that path takes the same stream."""
    try:
        frame = sys._getframe(stacklevel)
        where = (frame.f_code.co_filename, frame.f_lineno)
    except (AttributeError, ValueError):
        where = ("sys", 1)
    text = f"{where[0]}:{where[1]}: UserWarning: {message}\n"
    os.write(2, text.encode("utf-8", "replace"))


def describe(value: object, *, limit: int = 200) -> str:
    """``repr(value)``, truncated, and safe against a raising ``__repr__``.

    Diagnostics routinely interpolate caller-supplied objects, and in ML code
    those are tensors, dataclasses and framework handles whose ``__repr__`` can
    touch a released CUDA context or a closed file. A message about a dropped
    metric must not become an exception about formatting one.
    """
    try:
        text = repr(value)
    except _STOPS:
        raise
    except BaseException:  # noqa: BLE001
        try:
            text = f"<unrepresentable {type(value).__name__}>"
        except _STOPS:
            raise
        except BaseException:  # noqa: BLE001
            return "<unrepresentable>"
    if len(text) > limit:
        return text[: limit - 1] + "…"
    return text


def join(values: object, *, separator: str = ", ") -> str:
    """``separator.join`` over anything, coercing members and never raising.

    ``", ".join(result.get("missing", []))`` was a real fatal path: a backend
    returning objects (or nulls) instead of strings made ``str.join`` raise
    TypeError from inside a completion warning, killing the run at close.
    """
    try:
        return separator.join(str(v) for v in (values or ()))  # type: ignore[union-attr]
    except _STOPS:
        raise
    except BaseException:  # noqa: BLE001
        return describe(values)


class _Trouble:
    """One kind of delivery trouble, as `DeliveryNotices` tracks it."""

    __slots__ = ("total", "printed", "printed_at", "detail", "what", "prints")

    def __init__(self, what: str) -> None:
        self.prints = 0
        self.total = 0
        self.printed = 0
        self.printed_at: float | None = None
        self.detail: str | None = None
        self.what = what


class DeliveryNotices:
    """Delivery trouble, said in the TRAINING process while it happens (plan 1.7).

    The detached worker writes only to `drainer.log`, and a dead letter or an
    auth block used to surface at `finish()` -- hours later -- while a dropped
    write warned once per call (44 lines for 50 drops). Each KIND of trouble
    now prints one line when it first happens, then at most once per
    `INTERVAL` seconds with the running count, each naming its fix;
    `summary()` prints what was held back since, for `finish()`.

    A no-op in the detached worker (``PROBE_OUTBOX_WORKER=1``): its clients are
    synchronous and nobody reads its stderr. Stdlib-only, like this module.
    """

    INTERVAL = 300.0
    DEAD_LETTER = "dead_letter"
    AUTH_BLOCK = "auth_block"
    DROP = "drop"
    STALLED = "stalled"

    _FIX = {
        DEAD_LETTER: "see `probe outbox status`, fix the cause, then `probe outbox retry`",
        DROP: "free disk space next to the outbox, or see `probe outbox status`",
        STALLED: "they stay on disk; see `probe outbox status`",
    }

    def __init__(self, *, prefix: str = "probe", clock=None) -> None:
        import os
        import threading
        import time

        self._lock = threading.Lock()  # writes come from any thread (review of #2055)
        self.prefix = prefix
        #: Monotonic seconds; the client's poller keeps time by it too.
        self.clock = clock or time.monotonic
        self._off = os.environ.get("PROBE_OUTBOX_WORKER") == "1"
        self._kinds: dict[str, _Trouble] = {}

    def note(self, kind: str, what: str, *, count: int = 1, detail: str | None = None) -> None:
        """Record ``count`` more of ``kind``. ``what`` describes them, with
        ``{n}`` for the running total ("{n} write(s) dropped")."""
        if self._off:
            return
        try:
            with self._lock:
                self._note(kind, what, count, detail)
        except Exception:  # noqa: BLE001 -- a notice may never be fatal
            # Not BaseException: a Ctrl-C or a worker's death signal landing
            # while a notice prints must still stop the process.
            pass

    def _note(self, kind: str, what: str, count: int, detail: str | None) -> None:
        now = self.clock()
        trouble = self._kinds.setdefault(kind, _Trouble(what))
        trouble.total += count
        trouble.what = what
        if detail is not None:
            trouble.detail = detail
        if trouble.printed_at is None or now - trouble.printed_at >= self.INTERVAL:
            self._print(kind, trouble, now)

    def summary(self) -> None:
        """Print, once, each kind with trouble recorded since its last line."""
        if self._off:
            return
        try:
            with self._lock:
                for kind, trouble in self._kinds.items():
                    if trouble.total > trouble.printed:
                        self._print(kind, trouble, self.clock(), closing=True)
        except Exception:  # noqa: BLE001 -- see `note`
            pass

    def _fix(self, kind: str) -> str:
        if kind == self.AUTH_BLOCK:
            # Read at print time, not import time: this module imports nothing
            # else in the package when it loads (see the module docstring), and
            # session_marker is stdlib-only, so the late import costs a line.
            from .session_marker import WIZARD_HINT

            return f"{WIZARD_HINT}; the queued writes deliver once it is fixed"
        return self._FIX.get(kind, "see `probe outbox status`")

    def _print(self, kind: str, trouble: _Trouble, now: float, *, closing: bool = False) -> None:
        trouble.printed, trouble.printed_at = trouble.total, now
        line = f"{self.prefix}: {trouble.what.format(n=trouble.total)}"
        if trouble.detail:
            line += f" ({trouble.detail})"
        line += f"; {self._fix(kind)}."
        if closing:
            line += " (at close)"
        trouble.prints += 1
        if trouble.prints > 1:
            # Python's default warning filter shows an identical message from
            # one place only once: a reminder must never repeat an earlier
            # message's exact text (review of #2055).
            line = f"{line} (reminder {trouble.prints})"
        warn(line, stacklevel=5)
