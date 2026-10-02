"""SIGTERM: send what is queued, close the run ``failed``, then die of SIGTERM.

Managed jobs (SageMaker, Vertex, Kubernetes, a spot reclaim, ``docker stop``)
end with SIGTERM and destroy the container about 30 s later. Python's default
action for SIGTERM ends the process at once -- no ``finally``, no atexit -- so a
run's queued writes died with the container's disk and the run stayed
``running`` until the server's reaper called it ``crashed`` 15 minutes later
(lane E3's managed-job test: 0 of 900 queued points, the config and the
artifact lost).

So :func:`fluent.init` installs a SIGTERM handler, on the main thread, when the
run opens. On SIGTERM it spends up to ``PROBE_SIGTERM_FLUSH_SECONDS`` (default
20; ``0`` turns all of this off) delivering what is queued and closing every
run this process has open ``failed``, with ``probe_finish.reason =
"preempted"``, ``signal = "SIGTERM"`` and ``exit_code = 143`` on it, and an
``exit`` process span whose ``exit_code`` is ``-15`` -- the server's "died on
that signal", which its crash email reads. Then it puts SIGTERM's default action
back and raises it again, so the process still ends killed by SIGTERM (a PID 1,
which the kernel will not kill that way, exits 143 instead).

ANOTHER HANDLER FIRST. A handler already installed when the run opens
(Lightning's, torchrun's agent, the script's own) runs FIRST, and ours after
it -- as does ours under a handler that composes the one it found (Lightning
installs its own after ``probe.init``, calling ours after its notifier; the
first ``Run.log`` after that moves ours to the front of Lightning's list,
`run_first`, because that notifier can block for good: see below). Either way
the grace below is armed before theirs runs.

* It RETURNS: it has a stop of its own to make -- Lightning raises
  ``SIGTERMException`` at the next step, Hugging Face's JIT checkpoint saves
  one -- so ours does not cut it short. The run is marked preempted, and the
  process's own way out (a ``with probe.init()`` exit, a ``finally``, atexit)
  closes it ``failed``/``preempted`` within the budget. If the process is
  still running when all but `_close_reserve` of the budget is spent, ours
  closes the run and ends the process as above.
* It RAISES (a SystemExit, a KeyboardInterrupt, torchrun's SignalException):
  the exception goes through, and the process's way out closes the run
  ``failed``/``preempted`` within what is left of the budget (never less than
  `LATE_CLOSE_FLOOR_SECONDS`), however that exception would have closed it.
* It calls ``os._exit``: nothing of ours runs; the run is left to the server's
  reaper, as before.
* It NEVER RETURNS, stuck in a C call: Lightning 2.6's notifier broadcasts to
  the other ranks from inside the handler, and a node preempted alone (its
  pod deleted) has no peer in that collective, so rank 0's main thread
  blocks in gloo until torchrun SIGKILLs it (the 7-day soak's F2). When the
  grace runs out, the worker re-signals the main thread; one inside a C call
  runs no handler, so after `_ANSWER_SECONDS` without an answer the worker
  closes the run itself and ends the process (`_close_unanswered`, exit code
  143).

A handler installed AFTER the run opened that replaces ours (rather than
composing it) is left alone: at close ours is taken down only while it is still
the one installed. Only the main thread can install a signal handler; a run
opened on another thread gets none.

RE-ENTRANCY -- the hard part. A signal handler runs on the main thread at
whatever bytecode it interrupted, so it may land inside the SDK while that
frame holds a lock (the journal's append flock, the outbox status write, a run
lock, the transport's pool). Anything the handler waited on could be one of
those, and the interrupted frame can never release it while the handler runs.
Two rules keep that from hanging the process:

* The close runs on a WORKER thread, started when the handler was installed
  (starting a thread inside a handler takes ``threading``'s own lock, which the
  interrupted frame may hold). The handler only asks it through a
  ``queue.SimpleQueue`` -- reentrant by contract -- and waits for it at most
  until the budget's deadline. Whatever it is blocked on, the process then dies
  on time. Another signal meanwhile (a parent's death signal, a Ctrl-C) does
  not cut the wait short.
* When the interrupted frame is INSIDE the SDK (a ``probe.log`` in a training
  loop, the likeliest place of all), the handler first lets it finish: it
  returns at once, and a profile hook takes over the moment control leaves the
  SDK, holding none of its locks. If it has not left within
  `_SDK_GRACE_SECONDS` (a sync write stuck on a dead network, a hung fsync),
  the worker re-signals the main thread and the close goes ahead anyway,
  bounded as above. A close already running on the main thread is instead let
  run to the deadline: it is doing exactly what the handler would.
* The interrupted frame may hold ``sys.stdout``'s or ``sys.stderr``'s lock
  with NO frame on the stack to show it: CPython's ``BufferedWriter`` checks
  for signals between the writes of a flush, the lock held, so a handler runs
  inside a ``print`` (or a progress bar's redraw). The close's worker thread
  keeps off both streams (`safe_warn.streams_off_limits`): its warnings go to
  fd 2, and the log capture stops without flushing them. Waiting on that lock
  spent the whole budget and left the run ``running`` (release gate
  36503631939: a SIGTERM right after the script's own ``print``).

A main thread inside a long C call (a CUDA sync, a big numpy op) runs no Python
signal handler until the call returns. When a grace or a deferral runs out
first, the worker closes without it (`_close_unanswered`).

ON A THROWAWAY DISK (``ephemeral``: a container's overlay, tmpfs, a disposable
machine's local disk) the queue dies with the machine, so a close that could
not deliver everything in time is sent DIRECTLY, marking what is lost
(``probe_finish.undelivered``), instead of being queued behind that data for a
worker that dies with the container (`Run._close_preempted_directly`); on
durable storage it is queued as any close is, for the worker or the next
process to deliver.

A forked child inherits the handler but not the run: there it acts as the
handler it replaced (the default action, or the one it chained), unless the
child opens a run of its own.
"""

from __future__ import annotations

import contextvars
import os
import queue
import signal
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any

ENV = "PROBE_SIGTERM_FLUSH_SECONDS"
DEFAULT_SECONDS = 20.0
#: What a shell reports for a process killed by SIGTERM, and what a PID 1 --
#: which the kernel will not kill with a default-action signal -- exits with.
EXIT_CODE = 128 + int(signal.SIGTERM)
REASON = "preempted"
#: The least a close that starts after the budget is spent still gets (the
#: late close of a chained handler that raised), so its status write can go.
LATE_CLOSE_FLOOR_SECONDS = 2.0
#: Kept back from the budget by the close on the worker thread, for the main
#: thread to put the default action back and die on time.
_EXIT_MARGIN_SECONDS = 0.5
#: The longest the handler lets an interrupted SDK call run on before closing
#: anyway (a quarter of the budget when that is less).
_SDK_GRACE_SECONDS = 2.0
#: How long the main thread has to answer the worker's re-signal before the
#: worker closes without it (`_close_unanswered`): running Python, it answers
#: within milliseconds; inside a C call it runs no handler until that returns.
_ANSWER_SECONDS = 0.5

_IDLE = "idle"
#: Another handler ran first and returned: its own stop is under way.
_GRACE = "grace"
#: The handler returned to let an interrupted SDK call finish first.
_DEFERRED = "deferred"
#: The close is running on the worker; the main thread waits for it.
_FLUSHING = "flushing"
#: A chained handler raised (or a grace's own stop closed every run): the
#: process ends its own way.
_UNWINDING = "unwinding"
_DYING = "dying"


@dataclass(frozen=True)
class Ending:
    """This process is ending because of a SIGTERM."""

    signum: int
    deadline: float
    #: 143 when this module ends the process; None while the process ends its
    #: own way (another handler raised, or is making its own stop).
    exit_code: int | None

    def facts(self) -> dict[str, Any]:
        """What the close records on the run (``probe_finish``)."""
        facts: dict[str, Any] = {"reason": REASON, "signal": _signal_name(self.signum)}
        if self.exit_code is not None:
            facts["exit_code"] = self.exit_code
        return facts

    def close_timeout(self, requested: float) -> float:
        """A close's deadline under this ending: what it asked for, never past
        the budget -- except a close the process makes its own way, which keeps
        `LATE_CLOSE_FLOOR_SECONDS` for its status write."""
        left = self.deadline - time.monotonic()
        if self.exit_code is not None:
            bound = left - _EXIT_MARGIN_SECONDS
        else:
            bound = max(left, LATE_CLOSE_FLOOR_SECONDS)
        # Tenths: the close prints its timeout ("not delivered within 9.5s").
        return max(0.0, int(min(requested, bound) * 10) / 10)


class _State:
    def __init__(self) -> None:
        self.pid: int | None = None
        #: What SIGTERM did before ours: SIG_DFL, or a callable to chain.
        self.previous: Any = signal.SIG_DFL
        self.budget = DEFAULT_SECONDS
        self.phase = _IDLE
        self.ending: Ending | None = None
        #: Set while ours calls the chained handler: a chain that holds ours in
        #: turn (Lightning's composed handler, ours re-wrapped by a later
        #: `init`) must not recurse into it.
        self.in_previous = False
        self.commands: queue.SimpleQueue | None = None
        self.worker: threading.Thread | None = None
        self.main_ident: int | None = None
        #: The handler installed when the grace began: the worker re-signals
        #: only through it (or ours), never into a handler set since.
        self.grace_handler: Any = None
        self.defer_frame: Any = None
        self.defer_until = 0.0
        self.saved_profile: Any = None
        #: The worker re-signalled the main thread (not a signal from outside).
        self.forced = False
        self.ctx: contextvars.Context | None = None
        self.done = threading.Event()
        self.close_finished = False


_state = _State()


def _signal_name(signum: int) -> str:
    try:
        return signal.Signals(signum).name
    except ValueError:
        return str(signum)


def budget_seconds() -> float:
    """``PROBE_SIGTERM_FLUSH_SECONDS``: the default when unset or unreadable,
    0 (off) when zero or negative."""
    raw = (os.environ.get(ENV) or "").strip()
    if not raw:
        return DEFAULT_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_SECONDS
    if value != value:  # NaN
        return DEFAULT_SECONDS
    return max(0.0, value)


def _close_reserve(budget: float) -> float:
    """What a grace leaves for ours to close in, if the process's own stop
    has not closed the run by then: a quarter of the budget, at least the
    smaller of 5 s and half of it."""
    return max(0.25 * budget, min(5.0, 0.5 * budget))


def ending() -> Ending | None:
    """How this process is ending, when a SIGTERM decided it; else None."""
    st = _state
    if st.pid != os.getpid():
        return None
    return st.ending


# -- install / take down ---------------------------------------------------------


def install() -> bool:
    """Put ours in front of SIGTERM for the run that just opened. Main thread
    only; never raises. True when ours is the handler afterwards.

    Ours goes in when SIGTERM has its default action, or a Python handler to
    chain (it runs first). An ignored SIGTERM (SIG_IGN) stays ignored, and a
    handler set outside Python (``getsignal`` is None) cannot be chained, so
    both are left alone."""
    try:
        return _install()
    except Exception:  # noqa: BLE001 -- a run's open never fails over this
        return False


def _install() -> bool:
    budget = budget_seconds()
    if budget <= 0 or os.name != "posix":
        return False
    if threading.current_thread() is not threading.main_thread():
        return False
    pid = os.getpid()
    if _state.pid != pid:
        # A forked child opening a run of its own: nothing of the parent's
        # state (its worker thread did not survive the fork) is ours, except
        # what an inherited handler of ours chains to.
        inherited = signal.getsignal(signal.SIGTERM) is _on_sigterm
        previous = _state.previous
        _reset(pid)
        if inherited:
            _state.previous = previous
    st = _state
    if st.phase != _IDLE:
        return False
    current = signal.getsignal(signal.SIGTERM)
    if current is not _on_sigterm and (current is None or current == signal.SIG_IGN):
        return False
    _prepare()
    if current is not _on_sigterm:
        st.previous = current  # SIG_DFL, or theirs to run first
    st.budget = budget
    st.main_ident = threading.main_thread().ident
    if st.worker is None or not st.worker.is_alive():
        st.commands = queue.SimpleQueue()
        st.worker = threading.Thread(
            target=_worker, args=(st.commands,), name="probe-sigterm", daemon=True
        )
        st.worker.start()
    if current is not _on_sigterm:
        signal.signal(signal.SIGTERM, _on_sigterm)
    return True


def uninstall() -> None:
    """The last open run closed: give SIGTERM back what it had -- only while
    ours is still the handler (one installed after the run opened stays).
    Main thread only; never raises."""
    try:
        st = _state
        if st.pid != os.getpid() or st.phase != _IDLE:
            return
        if threading.current_thread() is not threading.main_thread():
            return
        if signal.getsignal(signal.SIGTERM) is _on_sigterm:
            previous = st.previous
            signal.signal(signal.SIGTERM, previous if previous is not None else signal.SIG_DFL)
        # `previous` is kept: a handler that composed ours (Lightning) may put
        # ours back, and a SIGTERM then still reaches what ours chains to.
        if st.commands is not None:
            st.commands.put(("stop",))
        st.worker = None
        st.commands = None
    except Exception:  # noqa: BLE001 -- a close never fails over this
        pass


def run_first() -> None:
    """Put ours FIRST in a handler that composed ours after its own.

    Lightning installs its SIGTERM handler after ``probe.init`` and composes
    the one it found -- ours -- LAST, behind its notifier (``_HandlersCompose``,
    whose ``signal_handlers`` it calls in order). Lightning 2.6's notifier
    BROADCASTS from inside the handler, a collective the other ranks join only
    if they got SIGTERM too: when one node alone is preempted (its pod
    deleted), rank 0's main thread blocks in it for good, and ours never ran
    (the 7-day soak's finding F2: the run stayed ``running``). First in that
    list, ours starts the budget and arms the worker before theirs runs, and
    `_close_unanswered` closes the run when theirs never returns.

    Called on every `Run.log` (the first SDK code to run once a fit is under
    way), so it must stay cheap: one ``getsignal`` when ours is the handler or
    nothing composed it. Main thread only (a handler runs there, so the list
    is never reordered under it); never raises."""
    try:
        current = signal.getsignal(signal.SIGTERM)
        if current is _on_sigterm or current is None:
            return
        handlers = getattr(current, "signal_handlers", None)
        if type(handlers) is not list or not handlers or handlers[0] is _on_sigterm:
            return
        st = _state
        if (
            _on_sigterm not in handlers
            or st.phase != _IDLE
            or st.pid != os.getpid()
            or threading.get_ident() != st.main_ident
        ):
            return
        handlers[:] = [_on_sigterm, *(h for h in handlers if h is not _on_sigterm)]
    except Exception:  # noqa: BLE001 -- a log never fails over this
        pass


def _reset(pid: int | None = None) -> None:
    """Fresh state (a forked child, or a test)."""
    global _state
    _state = _State()
    _state.pid = pid


def _prepare() -> None:
    """Import now what the close imports later: a first import inside a
    handler, or at interpreter exit, is where the #2083 regression came from."""
    from . import diagnostics, ephemeral, fluent, run, safe_warn, transport  # noqa: F401

    global _CLOSE_CODES, _fluent
    _fluent = fluent
    if not _CLOSE_CODES:
        _CLOSE_CODES = frozenset({run.Run.finish.__code__})


# -- the handler -----------------------------------------------------------------


def _on_sigterm(signum: int, frame: Any) -> None:
    st = _state
    # Directly from the signal, `frame` is our caller; from a composing
    # handler (Lightning's, which calls the one it found), that handler is.
    composed = sys._getframe(1) is not frame
    if st.pid != os.getpid():
        # A forked child that opened no run: the handler we replaced decides.
        _as_before(signum, frame, composed)
        return
    if st.in_previous:
        # Called back by the chained handler itself (a composed handler that
        # holds ours): ours runs once, after it returns.
        return
    phase = st.phase
    if phase in (_FLUSHING, _DYING):
        return  # already ending; the deadline bounds it
    if phase == _UNWINDING:
        _as_before(signum, frame, composed)
        return
    if phase == _DEFERRED:
        if st.forced or time.monotonic() >= st.defer_until:
            st.forced = False
            _take_over()
        return
    if phase == _GRACE:
        if not st.forced:
            # Another SIGTERM from outside while their stop is under way:
            # theirs hears it again, as it would without us.
            if callable(st.previous):
                _call_previous(signum, frame)
            return
        st.forced = False
        _close_now(frame)
        return
    fluent = _fluent
    if fluent is None or not fluent._has_open_run():
        _as_before(signum, frame, composed)
        return
    deadline = time.monotonic() + st.budget
    if callable(st.previous) or composed:
        # Theirs has a stop of its own to make: the one we chain (about to
        # run), or the one that composed ours (it ran, or runs after ours).
        # Mark the run preempted and give that stop until our reserve --
        # armed BEFORE theirs runs, so a handler of theirs that never returns
        # (stuck in a C call) still ends in our close (`_close_unanswered`).
        _grace(signum, deadline)
        if callable(st.previous):
            try:
                _call_previous(signum, frame)
            except BaseException:
                # Theirs ends the process its own way; the close on the way out
                # (with-block exit, a finally, atexit) makes it failed/preempted.
                st.phase = _UNWINDING
                raise
        return
    st.ending = Ending(signum, deadline, EXIT_CODE)
    _close_now(frame)


def _grace(signum: int, deadline: float) -> None:
    st = _state
    st.ending = Ending(signum, deadline, None)
    st.phase = _GRACE
    st.grace_handler = signal.getsignal(signal.SIGTERM)
    # This thread's context, for a close the worker makes without it.
    st.ctx = contextvars.copy_context()
    if st.commands is not None:
        st.commands.put(("wake", deadline - _close_reserve(st.budget)))


def _call_previous(signum: int, frame: Any) -> None:
    st = _state
    st.in_previous = True
    try:
        st.previous(signum, frame)
    finally:
        st.in_previous = False


def _as_before(signum: int, frame: Any, composed: bool) -> None:
    """What SIGTERM did before ours: the chained handler, else the default --
    unless a composing handler called ours, which is then what handles it
    (the default was never its to run)."""
    if callable(_state.previous):
        _call_previous(signum, frame)
        return
    if not composed:
        _die(quiet=True)


def _close_now(frame: Any) -> None:
    """Close and die -- once the main thread is out of the SDK."""
    st = _state
    if not _fluent._has_open_run():
        # A grace whose own stop already closed everything: theirs goes on.
        st.phase = _UNWINDING
        return
    if st.ending is None:
        st.ending = Ending(signal.SIGTERM, time.monotonic() + st.budget, EXIT_CODE)
    elif st.ending.exit_code is None:
        # The grace ran out: from here this module ends the process.
        st.ending = Ending(st.ending.signum, st.ending.deadline, EXIT_CODE)
    boundary, closing = _sdk_boundary(frame)
    if boundary is not None:
        _defer(boundary, closing)
        return
    _take_over()


# -- let an interrupted SDK call finish first ------------------------------------

_SDK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
_CLOSE_CODES: frozenset = frozenset()
#: `probe.sdk.fluent`, bound by `_prepare` so the handler imports nothing.
_fluent: Any = None


def _sdk_boundary(frame: Any) -> tuple[Any, bool]:
    """The OUTERMOST frame of the ``probe`` package on the main thread's
    stack, and whether a close (`Run.finish`) is among them; (None, False)
    when the SDK is nowhere on it.

    The whole stack, not only its top: the frame the signal interrupted may be
    a library the SDK called (httpx, json, os) or a user's object it is
    converting, with the lock-holding SDK frame below it. Once the outermost
    SDK frame returns, no SDK frame is left to hold anything."""
    boundary = None
    closing = False
    f = frame
    while f is not None:
        code = f.f_code
        if code.co_filename.startswith(_SDK_ROOT):
            boundary = f
            if code in _CLOSE_CODES:
                closing = True
        f = f.f_back
    return boundary, closing


def _defer(boundary: Any, closing: bool) -> None:
    st = _state
    now = time.monotonic()
    deadline = st.ending.deadline if st.ending is not None else now
    # A close already running is doing what we would: it gets the budget.
    grace = (deadline - now) if closing else min(_SDK_GRACE_SECONDS, 0.25 * st.budget)
    st.phase = _DEFERRED
    st.defer_frame = boundary
    st.defer_until = now + grace
    st.saved_profile = sys.getprofile()
    sys.setprofile(_profile_hook)
    if st.commands is not None:
        st.commands.put(("wake", st.defer_until))


def _profile_hook(frame: Any, event: str, arg: Any) -> None:
    st = _state
    if event != "return" or frame is not st.defer_frame:
        return
    st.defer_frame = None
    sys.setprofile(st.saved_profile)
    st.saved_profile = None
    if st.phase == _DEFERRED:
        _take_over()


# -- close on the worker, then die -----------------------------------------------


def _take_over() -> None:
    """On the main thread, outside any SDK frame (or out of time for one):
    close on the worker, wait at most until the deadline, then die."""
    st = _state
    if st.phase not in (_IDLE, _GRACE, _DEFERRED):
        return
    st.phase = _FLUSHING
    if st.defer_frame is not None:
        st.defer_frame = None
        try:
            sys.setprofile(st.saved_profile)
        except Exception:  # noqa: BLE001
            pass
    deadline = st.ending.deadline if st.ending is not None else time.monotonic()
    if st.commands is not None and deadline - time.monotonic() > _EXIT_MARGIN_SECONDS:
        st.ctx = contextvars.copy_context()
        st.commands.put(("close",))
        # Every other signal meanwhile -- a parent's death signal (SIGINT
        # under torch), a Ctrl-C -- is absorbed: the deadline bounds the wait.
        while not st.done.is_set():
            left = deadline - time.monotonic()
            if left <= 0:
                break
            try:
                st.done.wait(left)
            except BaseException:  # noqa: BLE001
                continue
    if not st.close_finished:
        _note(
            f"probe: SIGTERM: the run could not be closed within {st.budget:g}s "
            f"({ENV}); exiting -- what did not go out is left to the outbox and the "
            "server's reaper\n"
        )
    _die()


def _worker(commands: queue.SimpleQueue) -> None:
    """Pre-started at install: the handler may not start a thread. Wakes the
    main thread when a grace or a deferral runs out, and runs the close --
    by itself when the main thread does not answer that wake."""
    wake_at: float | None = None
    asked = False
    while True:
        timeout = None if wake_at is None else max(0.0, wake_at - time.monotonic())
        try:
            command = commands.get(timeout=timeout)
        except queue.Empty:
            wake_at = None
            if asked:
                asked = False
                if _unanswered():
                    _close_unanswered()
                    return
            elif _wake_main():
                asked = True
                wake_at = time.monotonic() + _ANSWER_SECONDS
            continue
        kind = command[0]
        if kind == "stop":
            return
        if kind == "wake":
            wake_at, asked = command[1], False
            continue
        if kind == "close":
            _close()
            return


def _wake_main() -> bool:
    """Re-signal the main thread so the handler runs again -- a real signal,
    so a blocking call there is interrupted. Only into ours, or the handler
    that composed ours when the grace began. True when it re-signalled."""
    st = _state
    if st.phase not in (_GRACE, _DEFERRED) or not st.main_ident:
        return False
    try:
        current = signal.getsignal(signal.SIGTERM)
        if current is _on_sigterm or (st.phase == _GRACE and current is st.grace_handler):
            st.forced = True
            signal.pthread_kill(st.main_ident, signal.SIGTERM)
            return True
    except Exception:  # noqa: BLE001
        pass
    return False


def _unanswered() -> bool:
    """The main thread has not run the handler since the worker re-signalled
    it: the handler clears ``forced`` and moves the phase on."""
    st = _state
    return st.forced and st.phase in (_GRACE, _DEFERRED)


def _close_unanswered() -> None:
    """The main thread did not answer: it is inside a C call -- a collective
    whose peers never join (Lightning 2.6 broadcasts from its SIGTERM handler,
    and a node preempted alone has no peer in it), a hung syscall -- and runs
    no Python handler until that returns. So the close goes ahead here, and
    this thread ends the process when it is done or out of time: nothing on
    the main thread can."""
    st = _state
    st.phase = _FLUSHING
    st.forced = False
    ending_ = st.ending
    if ending_ is not None and ending_.exit_code is None:
        st.ending = Ending(ending_.signum, ending_.deadline, EXIT_CODE)
    _close()
    _note(
        "probe: SIGTERM: the main thread is stuck in a call that runs no signal handler; "
        + ("closed the run from another thread" if st.close_finished else
           f"the run could not be closed within {st.budget:g}s ({ENV})")
        + "; exiting\n"
    )
    # No flush, no default action: the main thread may hold the streams'
    # locks, and only the main thread may set a signal's action.
    os._exit(EXIT_CODE)


def _close() -> None:
    st = _state
    try:
        ctx = st.ctx if st.ctx is not None else contextvars.copy_context()
        ctx.run(_close_runs)
        st.close_finished = True
    except BaseException:  # noqa: BLE001 -- the main thread dies on time regardless
        pass
    finally:
        st.done.set()


def _close_runs() -> None:
    from . import safe_warn
    from .transport import fresh_deadline_scope

    ending_ = _state.ending
    deadline = ending_.deadline if ending_ is not None else time.monotonic()
    # The main thread's context may carry a deadline of its own (a close it
    # was in): ours replaces it. And the main thread may hold sys.stdout's or
    # sys.stderr's lock (see RE-ENTRANCY): this thread keeps off both.
    with fresh_deadline_scope(deadline), safe_warn.streams_off_limits():
        _fluent._close_for_preemption()


def _note(message: str) -> None:
    """Straight to fd 2: the interrupted frame may hold ``sys.stderr``'s lock."""
    try:
        os.write(2, message.encode("utf-8", "replace"))
    except Exception:  # noqa: BLE001
        pass


def _die(*, quiet: bool = False) -> None:
    """End the process as SIGTERM's default action would."""
    st = _state
    st.phase = _DYING
    try:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
    except Exception:  # noqa: BLE001
        pass
    if not quiet:
        for stream in (sys.stdout, sys.stderr):
            try:
                stream.flush()
            except Exception:  # noqa: BLE001 -- its lock may be the interrupted frame's
                pass
    try:
        signal.raise_signal(signal.SIGTERM)
    except Exception:  # noqa: BLE001
        pass
    # Still here: a PID 1 (the kernel drops a default-action signal it sends
    # itself) or SIGTERM blocked. Exit with what a shell reports for it.
    os._exit(EXIT_CODE)
