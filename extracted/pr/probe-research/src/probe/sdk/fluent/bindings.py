"""Which run is bound to this process, thread or asyncio task, and letting it go."""

from __future__ import annotations
import contextvars
import os
import sys
import threading
import weakref
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from ..client.client import Client

if TYPE_CHECKING:

    from ..run.run import Run


def _current_task():
    """The running asyncio task, or None. Free when asyncio was never imported:
    then no task can be running."""
    if "asyncio" not in sys.modules:
        return None
    import asyncio

    try:
        return asyncio.current_task()
    except RuntimeError:  # no running event loop in this thread
        return None


def _here() -> tuple:
    """(pid, thread, weakref to the asyncio task or None): the scope a binding
    belongs to."""
    task = _current_task()
    return (os.getpid(), threading.get_ident(), weakref.ref(task) if task is not None else None)


@dataclass(eq=False)
class _Binding:
    run: "Run"
    #: The client to close on finish, set only when :func:`init` built it. A
    #: caller-supplied client is theirs to close; closing it here would kill a
    #: transport (and any other run's heartbeat) they are still using.
    close_client: Client | None
    #: Set by :func:`finish`. A binding can be observed by more contexts than the
    #: one that closes it — a worker thread calling finish() cannot reach into the
    #: main thread's contextvar — so "is this run still open" has to live on the
    #: binding itself. Without it, the initiating thread keeps logging into a
    #: completed run.
    closed: bool = False
    #: Joined through ``PROBE_RUN_ID`` rather than created here. The launcher
    #: that opened the run owns its close, so a second :func:`init` returns it
    #: instead of finishing it.
    attached: bool = False
    #: The scope that bound it (:func:`_here`). A context variable is COPIED
    #: into every asyncio task, ``asyncio.to_thread`` call and forked child, so
    #: "visible here" does not mean "opened here": a task's ``init()`` used to
    #: take the parent's run for its own previous run and close it.
    owner: tuple = field(default_factory=_here)


_current: contextvars.ContextVar["_Binding | None"] = contextvars.ContextVar(
    "probe_active_binding", default=None
)

_process_default: "_Binding | None" = None
_default_lock = threading.Lock()
#: Runs opened with ``reinit="create_new"``: never bound, so no forwarder
#: reaches them, but still closed at exit like the bound one (W&B's exit closes
#: every run it has) instead of being left for the reaper.
_unbound: "list[_Binding]" = []


def _open_binding() -> "_Binding | None":
    current = _current.get()
    if current is not None and not current.closed:
        return current
    default = _process_default
    if default is None or default.closed:
        return None
    if current is not None and default.owner[:2] != (os.getpid(), threading.get_ident()):
        # This context's own run was closed from elsewhere. Falling through to
        # the process default is right in a notebook -- a run opened in a
        # top-level-await cell sets its context variable in a copy that dies
        # with the cell, and the sync cells after it, on the SAME thread,
        # reach the run only through the default -- but another thread's run
        # is not this context's: a script's worker would log into it (review
        # of #2016). So only a default bound on this thread.
        return None
    return default


def _mark_dropped(run: "Run", n: int) -> None:
    """Count ``n`` writes meant for ``run`` as dropped: its close reports
    ``dropped_writes`` as the rise over this baseline."""
    if n and hasattr(run, "_dropped_baseline"):
        run._dropped_baseline -= n



def _bind_new(binding: _Binding, reinit_mode: str) -> None:
    """Bind a run :func:`init` just opened (online or offline) -- or, under
    ``reinit="create_new"``, keep it unbound and closed with its handle."""
    global _process_default
    run = binding.run
    if reinit_mode == "create_new":
        # Not bound (W&B: create_new never becomes `wandb.run`), so the run
        # already bound here -- and every forwarder -- is left as it was. Only
        # its handle can close it, so its close lets go of the client init
        # built: a sweep of `create_new` + `run.finish()` kept every client
        # (and its connection pool) open until exit (review of #2016).
        run._after_finish = lambda: _drop_unbound(binding)
        with _default_lock:
            done = [b for b in _unbound if not _is_open(b)]
            _unbound[:] = [b for b in _unbound if _is_open(b)]
            _unbound.append(binding)
        for stale in done:
            # Closed without finish() (a bare set_status: `run.execute()`).
            _retire(stale)
    else:
        _current.set(binding)
        with _default_lock:
            _process_default = binding
            # Per-run, not per-process: a new run must not inherit the exit
            # status a previous one's exception set -- nor its exception, which
            # would be filed as THIS run's crash report, nor its exit code.
            _reset_exit_record()


def _init_disabled(kw: dict, *, bind: bool = True) -> "Run":
    """``PROBE_MODE=disabled``: bind a run that records nothing.

    No Client (so no network and no outbox directory), no exit hooks, no
    capture. Bound like a real run so ``probe.log()`` and ``probe.finish()``
    work unchanged from anywhere in the script -- unless ``bind`` is False
    (``reinit="create_new"``, whose runs are never bound)."""
    global _process_default
    from ..run.disabled import DisabledRun

    run = DisabledRun(name=kw.get("name"), config=kw.get("config"), tags=kw.get("tags"))
    from ..capture.logs import early as _early

    _early.end_held_window()  # records nothing: the tee `import probe` started stops too
    # Open beside a recording run, it still makes that run's worker binding
    # unsafe: its own workers' reads are not the other run's (F5). In memory.
    from ..run.launch import open_runs as _open_runs

    _open_runs.opened(run)
    if not bind:
        return run  # type: ignore[return-value]
    binding = _Binding(run=run, close_client=None)  # type: ignore[arg-type]
    _current.set(binding)
    with _default_lock:
        _process_default = binding
    return run  # type: ignore[return-value]


def _release(binding: _Binding, *, timeout: float | None = None) -> None:
    """Unbind a closed run everywhere it is visible, and close the client init
    built for it. Once: a second call is a no-op. ``timeout`` bounds that
    client's close (`Client.close`)."""
    global _process_default
    already = binding.closed
    # Mark the binding first: every context that can still see it (including
    # threads whose contextvar we cannot reach) reads this flag.
    binding.closed = True
    with _default_lock:
        if _process_default is binding:
            _process_default = None
    if _current.get() is binding:
        _current.set(None)
    # Never another process's client: a forked child holds a COPY of the
    # parent's, and closing it seals the parent's outbox producer.
    try:
        if not already and binding.close_client is not None and binding.owner[0] == os.getpid():
            if timeout is None:
                binding.close_client.close()
            else:
                binding.close_client.close(timeout=timeout)
    finally:
        if not already:
            _uninstall_sigterm_flush_if_idle()


def _release_quietly(binding: _Binding, *, timeout: float | None = None) -> None:
    try:
        _release(binding, timeout=timeout)
    except Exception:  # noqa: BLE001 -- letting go of a closed run never raises
        pass


def _is_open(binding: _Binding) -> bool:
    """Nobody has closed it: not unbound by :func:`finish`, no ``finish()`` on
    its handle (run, or running), no verdict sent by ``set_status``."""
    run = binding.run
    return (
        not binding.closed
        and getattr(run, "_closed_status", None) is None
        and not _finish_called(run)
    )


def _finish_called(run: "Run") -> bool:
    """`Run._finish_called`, and the same question of a ``PROBE_MODE=disabled``
    run, which has no private surface: its ``finish()`` sets its ``status``."""
    called = getattr(run, "_finish_called", None)
    if callable(called):
        return bool(called())
    return getattr(run, "status", "running") != "running"


def _drop_unbound(binding: _Binding) -> None:
    """A ``create_new`` run's close is over: forget it and close its client."""
    with _default_lock:
        if binding in _unbound:
            _unbound.remove(binding)
    _release_quietly(binding)


def _owned_here(binding: _Binding, *, ended_task_counts: bool) -> bool:
    """The caller is in the scope that bound it: the same process, thread and
    asyncio task. With ``ended_task_counts``, a binding from a task that has
    finished counts too -- how a notebook runs cells (a task per cell, one
    thread, one context kept across them)."""
    pid, thread, task_ref = binding.owner
    if pid != os.getpid() or thread != threading.get_ident():
        return False
    current = _current_task()
    if task_ref is None:
        return current is None
    owner_task = task_ref()
    if owner_task is current:
        return True
    return ended_task_counts and (owner_task is None or owner_task.done())


def _previous_in_scope() -> "_Binding | None":
    """The run a second :func:`init` here replaces, or None.

    Visible is not enough. A worker thread sees the main thread's run through
    the process default, and an asyncio task, an ``asyncio.to_thread`` call or
    a forked child sees its parent's through a copied context variable; each
    of those opens its own run beside it, as before reinit existed. Only a run
    this very scope opened is "previous".

    A finished task's run counts only when it is in THIS context -- a notebook
    keeps its context across cells, each cell a task that has ended by the
    next. Through the process default alone it would be a sibling task's
    (``asyncio.gather``), whose run is still that caller's to use."""
    for candidate, ended_task_counts in ((_current.get(), True), (_process_default, False)):
        if candidate is None or candidate.owner[0] != os.getpid():
            continue  # another process's: never ours to close or release
        if not _is_open(candidate):
            # Closed through its own handle (`with probe.init()`, run.finish(),
            # `run.execute()`) and never unbound: finish that close, and let go
            # of the client init built for it.
            _retire(candidate)
            continue
        if _owned_here(candidate, ended_task_counts=ended_task_counts):
            return candidate
    return None


def _has_open_run() -> bool:
    """Whether this process has a run of its own still open (a close in
    progress counts). Lock-free: the SIGTERM handler calls it, and the frame it
    interrupted may hold `_default_lock`."""
    pid = os.getpid()
    for binding in (_current.get(), _process_default, *list(_unbound)):
        if binding is not None and not binding.closed and binding.owner[0] == pid:
            return True
    return False
from probe.sdk.fluent.exit import _reset_exit_record, _uninstall_sigterm_flush_if_idle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.reinit import _retire  # noqa: E402 -- pieces need each other; the front door loads this one first
