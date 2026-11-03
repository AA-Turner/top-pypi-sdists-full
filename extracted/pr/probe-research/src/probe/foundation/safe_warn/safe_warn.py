"""The SDK's one non-raising warning channel: ``warnings.warn`` that cannot kill or hang a caller.

Stdlib-only, importing nothing else from the package at load (the enqueue path). DESIGN.md.
"""

from __future__ import annotations

import contextlib
import os
import sys
import threading
import warnings

#: Never swallowed: Ctrl-C and a deliberate exit. Anything else (a warnings-as-errors filter, a
#: broken hook, a torn-down interpreter) is ours to absorb.
_STOPS = (KeyboardInterrupt, SystemExit)
#: How a person fixes a missing or rejected credential. A copy of `probe.sdk.session_marker.WIZARD_HINT`,
#: which the hooks vendor stdlib-only; tests/test_wizard_hint_sync.py keeps the two equal.
WIZARD_HINT = "run the Probe wizard: probe wizard or npx probe-research"

_thread = threading.local()


@contextlib.contextmanager
def streams_off_limits():
    """While inside, this thread's warnings (and :func:`streams_allowed`'s callers) never touch
    ``sys.stdout``/``sys.stderr``: another thread may hold their locks for good (SIGTERM close)."""
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

    ``stacklevel`` counts from this function's CALLER, as ``warnings.warn`` did. The broad
    ``except BaseException`` is the point (warnings-as-errors, a broken ``showwarning``, a
    ``__del__``-time call after teardown). Ctrl-C and ``sys.exit`` (`_STOPS`) still
    propagate: swallowing one mid-warning (a DDP worker's death signal) let training carry on.
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
    """The warning as ``warnings`` would print it, straight to fd 2: no stream object, so no
    lock another thread can hold. Filters are not consulted (that path takes the same stream)."""
    try:
        frame = sys._getframe(stacklevel)
        where = (frame.f_code.co_filename, frame.f_lineno)
    except (AttributeError, ValueError):
        where = ("sys", 1)
    text = f"{where[0]}:{where[1]}: UserWarning: {message}\n"
    os.write(2, text.encode("utf-8", "replace"))


def describe(value: object, *, limit: int = 200) -> str:
    """``repr(value)``, truncated to ``limit`` chars, safe against a raising ``__repr__`` (a
    tensor's can touch a released CUDA context or a closed file)."""
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
    """``separator.join`` over anything, coercing members and never raising: a backend
    returning nulls once made ``str.join`` raise inside a completion warning and kill the run."""
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

    Each KIND prints one line when it first happens, then at most once per `INTERVAL`
    seconds with the running count and its fix; `summary()` prints the rest for `finish()`.
    A no-op in the detached worker (``PROBE_OUTBOX_WORKER=1``): nobody reads its stderr.
    Why: DESIGN.md (DeliveryNotices).
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
            # Not BaseException: a Ctrl-C or worker death signal mid-notice must still stop it.
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
            # The default filter shows an identical message from one place once: a reminder
            # must never repeat an earlier one's exact text (review of #2055).
            line = f"{line} (reminder {trouble.prints})"
        warn(line, stacklevel=5)
