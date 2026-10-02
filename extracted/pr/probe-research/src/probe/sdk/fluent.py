"""Module-level convenience: ``probe.init()`` / ``probe.log()`` / ``probe.finish()``.

W&B's defining ergonomic is that ``wandb.init()`` stashes a run somewhere global,
so ``wandb.log()`` works from anywhere without threading a handle down through
call frames. For a training script whose logging happens three libraries deep,
that is genuinely the right shape, and asking people to pass a ``run`` into code
they do not own is how instrumentation does not get added.

It is also W&B's worst failure mode. One process-wide global means two concurrent
runs clobber each other, a re-executed notebook cell logs into the previous run,
and a worker thread writes into whatever run some other thread started last.

So: the same ergonomic, with the binding in a :mod:`contextvars` variable backed
by a process default.

* :func:`init` sets both, so :func:`log` reaches the run from any thread — the
  common case, and what makes this a drop-in for the W&B shape (a plain
  contextvar would not: threads start with an empty context, so a DataLoader
  worker would silently find no run);
* an :func:`init` inside a thread, task, or block sets its own context too, and
  the context is consulted FIRST — so it shadows the default for that scope
  rather than replacing it everywhere. Two concurrent runs in one process stop
  being a silent-corruption bug and become a scoping question with an answer.

The process default is last-init-wins, matching W&B. If you genuinely run several
at once, scope them (or just use the explicit API, which has no ambient state at
all).

Nothing here is a second implementation: every function holds a real
:class:`~probe.sdk.client.Client` and :class:`~probe.sdk.run.Run` and forwards.
"""

from __future__ import annotations

import atexit
import contextvars
import os
import sys
import threading
import time
import warnings
import weakref
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from . import errors
from .client import Client
from .config import Mode, init_timeout_seconds, resolve_mode
from .transport import patience
from .unit_context import FailureContext

if TYPE_CHECKING:
    from collections.abc import Callable

    from .run import Run, SpanHandle


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

#: W&B's ``reinit`` values. ``default`` is ``finish_previous`` here (D16): W&B's
#: script default, ``return_previous``, leaves the first run open with nothing
#: bound to it, and an open run nobody closes is reaped ``crashed``.
_REINIT_MODES = ("default", "return_previous", "finish_previous", "create_new")
#: Longest a reinit waits on the previous run's writes before its close is
#: queued behind them: the caller is waiting for its NEW run.
_REINIT_FLUSH_CAP_S = 10.0
#: Held by a reinit from the moment it starts closing the old run until the new
#: one is bound. Another thread that finds no open run meanwhile waits on it
#: instead of raising "no active run" into a training loop that did nothing
#: wrong (`_reinit_in_progress` keeps that wait off the ordinary miss path) --
#: until `_reinit_wait_until`, `_REINIT_FLUSH_CAP_S` after the old run was let
#: go: opening the new run has no bound of its own (~122 s against an API that
#: is down), and that thread is someone's training loop (review of #2016).
_reinit_lock = threading.RLock()
_reinit_in_progress = False
_reinit_wait_until: "float | None" = None
#: Whether `log()` already said it is dropping rows while a reinit runs long.
_warned_reinit_drop = False
#: Writes dropped that way, and the run that replaced the closed one once it
#: is bound: they are counted on it (`probe_finish.dropped_writes` at its
#: close), since they were meant for it. Both under `_default_lock`.
_reinit_dropped = 0
_reinit_new_run: "Run | None" = None


class _ReinitStillOpening(errors.RosError):
    """No run to write to: another thread's :func:`init` is still opening the
    run that replaces the one it closed, past the wait `_binding` allows."""


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


def _binding(*, required: bool = True) -> "_Binding | None":
    found = _open_binding()
    if found is None and _reinit_in_progress:
        until = _reinit_wait_until
        wait = _REINIT_FLUSH_CAP_S if until is None else max(0.0, until - time.monotonic())
        if _reinit_lock.acquire(timeout=wait):
            try:
                found = _open_binding()
            finally:
                _reinit_lock.release()
        elif required:
            raise _ReinitStillOpening(
                "no active run: probe.init() on another thread closed the previous run "
                f"and is still opening the next one after {_REINIT_FLUSH_CAP_S:g}s"
            )
    if found is None and required:
        raise errors.RosError(
            "no active run — call probe.init() first, or use the explicit API: "
            "probe.Client().run(experiment=...)."
        )
    return found


def _drop_during_reinit(what: str) -> None:
    """A write found no run because a reinit is still opening one: drop it,
    count it on the run that opens (`_count_reinit_drop`), and say so once,
    instead of raising into a training loop."""
    global _warned_reinit_drop
    _count_reinit_drop()
    if _warned_reinit_drop:
        return
    _warned_reinit_drop = True
    from . import safe_warn

    safe_warn.warn(
        f"probe.{what}: dropped -- probe.init() on another thread closed the previous "
        f"run and is still opening the next one after {_REINIT_FLUSH_CAP_S:g}s; writes "
        "until it opens are dropped and counted on it as dropped_writes (said once)",
        stacklevel=3,
    )


def _count_reinit_drop() -> None:
    global _reinit_dropped
    with _default_lock:
        if _reinit_new_run is not None:
            # Bound after this write gave up waiting: count it there directly.
            _mark_dropped(_reinit_new_run, 1)
        else:
            _reinit_dropped += 1


def _mark_dropped(run: "Run", n: int) -> None:
    """Count ``n`` writes meant for ``run`` as dropped: its close reports
    ``dropped_writes`` as the rise over this baseline."""
    if n and hasattr(run, "_dropped_baseline"):
        run._dropped_baseline -= n


def active_run() -> "Run | None":
    """The run bound for this context, or None.

    Named ``active_run`` and not ``probe.run``: ``probe.run`` is already the
    compatibility module for :mod:`probe.sdk.run`, and shadowing a module with a
    value is how import order becomes load-bearing."""
    found = _binding(required=False)
    return found.run if found else None


def init(
    *,
    client: Client | None = None,
    mode: str | None = None,
    reinit: str | bool | None = "default",
    **kw: Any,
) -> "Run":
    """Open a run and bind it as the active one. Returns the run.

    Takes the same arguments as :meth:`~probe.sdk.client.Client.run`
    (``experiment``, ``question``, ``name``, ``project``, ``source``, ``tags``,
    …). Pass ``client=`` to reuse a configured one; otherwise a
    :class:`~probe.sdk.client.Client` is built from env / the stored login and
    closed by :func:`finish`.

    The returned run is an ordinary handle, so ``with probe.init(...) as run:``
    works and closes on the way out.

    ATTACHES INSTEAD OF CREATING when ``PROBE_RUN_ID`` is in the environment
    (0205). This is the wandb.init() shape: a launcher opens the run and exports
    the id, the job inside reads it and joins that run. Before this, the launcher
    exported ``PROBE_RUN_ID`` and nothing on earth read it, so ``probe exec``
    around a script that also called ``probe.init()`` produced TWO runs -- one
    wrapped with an exit code and no curves, one owned with curves and no exit
    code -- and neither was the run anyone meant.

    RECORDS WHAT THE RUN READS AND WRITES (lineage): every file this process
    opens for reading is noted with its hash and sent at ``finish()``, so the
    server can link this run to the run that wrote those bytes; every file it
    writes that is still there at ``finish()`` is sent with its final hash, so
    a later reader can be linked to THIS run. Python workers the process
    starts by spawn or forkserver (a DataLoader's, a Pool's, a ``python``
    subprocess) are recorded into the run too while it is the only run open
    here; the environment that binds them is restored at ``finish()``, and a
    persistent worker follows the process to its next run. Paths and hashes
    only, never contents. Opt out of both with ``capture_reads=False`` or
    ``PROBE_CAPTURE_READS=0``; of writes alone with ``capture_outputs=False``,
    ``PROBE_CAPTURE_OUTPUTS=0`` or ``PROBE_CAPTURE_WRITES=0``
    (:mod:`probe.sdk.inputs`).

    RETRIES FOR UP TO ``PROBE_INIT_TIMEOUT_SEC`` (default 90 s) when the API is
    unreachable or failing, then raises (plan 2.5, D9). ``0`` keeps the old
    few-quick-retries behaviour. A run create whose answer was lost is sent
    again only where the server replays it (``creation_key``), never twice.

    ``mode=`` (or ``PROBE_MODE``): ``"online"`` (default); ``"disabled"``,
    which returns a :class:`~probe.sdk.disabled.DisabledRun` that records
    nothing and touches neither the network nor the disk; or ``"offline"``
    (plan 2.12), which records the run with NO network call into a queue of its
    own for ``probe sync`` to deliver later (:mod:`probe.sdk.offline`).
    ``PROBE_INIT_FALLBACK=offline`` goes offline when an online init runs out
    of its budget, instead of raising.

    A SECOND ``init()`` while a run is open in this scope (this thread, or this
    task's context) does what ``reinit`` says, with W&B's values:

    * ``"finish_previous"`` (the default, and ``True``): close the open run
      ``completed`` -- the whole close takes at most 10 s, then whatever is
      left is queued with the close behind it -- and open the new one.
      Before, the first run was simply abandoned: nothing closed it and the
      reaper called it ``crashed``, and while both were open neither swept
      its outputs. Another thread's ``probe.log()`` meanwhile waits for the
      new run, for at most 10 s after the old one is let go, then drops its
      rows with one warning until the new run opens.
    * ``"return_previous"`` (``False``): return the open run; the arguments are
      ignored, with a warning.
    * ``"create_new"``: open another run and leave the first open and bound;
      the new one is returned but not bound, so ``probe.log()`` still reaches
      the first. Closing its handle releases the client built for it, and it
      is closed at exit if nothing closed it before.

    A run joined through ``PROBE_RUN_ID`` is never closed this way: its
    launcher owns it, so a second ``init()`` returns it. Only a run THIS scope
    opened is "previous": an ``init()`` in a worker thread, an asyncio task,
    ``asyncio.to_thread`` or a forked child opens its own run beside the one
    it can see.

    Differences from W&B: there ``reinit`` is process-wide, its script default
    is ``return_previous``, and ``finish_previous`` finishes every active run,
    ``create_new`` ones included. Here the default is ``finish_previous``
    (D16), each choice acts on the caller's own scope, and ``create_new`` runs
    close with their handle or at exit."""
    run_mode = resolve_mode(mode)
    reinit_mode = _reinit_mode(reinit)
    if run_mode is Mode.OFFLINE:
        # Replacing an open run follows `reinit`, as for every other mode.
        return _replace_previous(
            reinit_mode,
            {**kw, "client": client},
            lambda: _init_offline(kw, reinit_mode=reinit_mode),
        )
    if run_mode is Mode.DISABLED:
        # Replacing an open run follows `reinit` too: a disabled run bound
        # over an online one left that one open for the reaper (review of
        # #2016). Its arguments are all ignored, so all are named if unused.
        return _replace_previous(
            reinit_mode,
            {**kw, "client": client},
            lambda: _init_disabled(kw, bind=reinit_mode != "create_new"),
        )
    # Read capture (lineage): on by default for the run a script opens itself,
    # since this process IS the run's work. Popped before the attach check,
    # which names every other kwarg it has to ignore.
    capture_reads = kw.pop("capture_reads", None)
    # A researcher's run, created or attached: the scrubber may cache (plan
    # (k); off in every multi-tenant process, see redaction.py).
    from . import redaction as _redaction

    _redaction.enable_scrub_cache()
    outputs = kw.pop("outputs", None)
    capture_outputs = kw.pop("capture_outputs", None)
    # `.probeignore` patterns (plan (n)): they apply to an attached run's
    # capture too, so they are popped before the attach check drops extras.
    ignore = kw.pop("ignore", None)
    if ignore is not None:
        from . import ignore as _ignore

        try:
            ignore = _ignore.normalize(ignore)
        except ValueError as exc:
            raise errors.ValidationError(str(exc)) from None
    return _replace_previous(
        reinit_mode,
        {
            **kw,
            "client": client,
            "capture_reads": capture_reads,
            "outputs": outputs,
            "capture_outputs": capture_outputs,
            "ignore": ignore,
        },
        lambda: _open_and_bind(
            client, reinit_mode, kw, capture_reads, outputs, capture_outputs, ignore
        ),
    )


def _replace_previous(reinit_mode: str, given: dict, open_new: "Callable[[], Run]") -> "Run":
    """:func:`init`'s reinit decision, then ``open_new()`` for the new run.
    ``given`` is every argument the caller passed, named when a returned run
    ignores them."""
    global _reinit_in_progress, _reinit_wait_until, _warned_reinit_drop
    global _reinit_dropped, _reinit_new_run
    previous = _previous_in_scope()
    if previous is not None and (reinit_mode == "return_previous" or previous.attached):
        ignored = sorted(k for k, v in given.items() if v is not None)
        if ignored:
            why = (
                "it joined PROBE_RUN_ID, whose launcher owns the run"
                if previous.attached
                else 'reinit="return_previous"'
            )
            from . import safe_warn

            safe_warn.warn(
                f"probe.init() returned the run already open in this scope "
                f"({previous.run.slug or previous.run.id}) because {why}, and ignored "
                f"{', '.join(ignored)}. Call probe.finish() first to open a new run.",
                stacklevel=3,
            )
        return previous.run
    if previous is not None and reinit_mode == "finish_previous":
        with _reinit_lock:
            _reinit_in_progress = True
            _reinit_wait_until = None
            _warned_reinit_drop = False
            with _default_lock:
                _reinit_dropped, _reinit_new_run = 0, None
            try:
                # BEFORE the new run exists: its output sweep and read capture
                # skip while another run on this host is still open over the
                # same folder.
                _close_binding(previous, closed_by="reinit")
                # Other threads now find no run; they wait this long for the
                # new one (`_binding`), then `log()` drops instead of waiting.
                _reinit_wait_until = time.monotonic() + _REINIT_FLUSH_CAP_S
                run = open_new()
                with _default_lock:
                    # What was dropped meanwhile was meant for this run.
                    _mark_dropped(run, _reinit_dropped)
                    _reinit_dropped, _reinit_new_run = 0, run
                return run
            finally:
                _reinit_in_progress = False
                _reinit_wait_until = None
    return open_new()


def _open_and_bind(
    client: "Client | None",
    reinit_mode: str,
    kw: dict,
    capture_reads: Any,
    outputs: Any,
    capture_outputs: Any,
    ignore: Any = None,
) -> "Run":
    """Open (or attach) the run and bind it -- :func:`init` after the reinit
    decision."""
    owned: Client | None = None
    if client is None:
        client = Client()
        owned = client
    # What a create left for the offline fallback. A client passed in may carry
    # one from an EARLIER init; this init must never replay it.
    client._last_run_create = None
    try:
        # ONE budget for opening the run, attach or create (plan 2.5): the API
        # being down for a minute is not a reason to kill the training job.
        # Capture after the run is open is carved out (`without_patience`).
        with patience(init_timeout_seconds()):
            run = _attach_from_env(client, kw)
            attached = run is not None
            if not attached:
                run = client.run(outputs=outputs, capture_outputs=capture_outputs, ignore=ignore, **kw)
        if attached:
            # Joining a run a launcher opened. On this host the launcher
            # captures (unless we write elsewhere); on another machine -- a
            # forwarded Modal secret, `sbatch --export` -- only we can.
            run._set_ignore(ignore)
            # A launcher on this host collects our reads and sweeps our folder
            # with ITS rules: hand it ours (and say what code capture misses).
            run._hand_ignore_to_launcher()
            run._start_capture(outputs=outputs, capture_outputs=capture_outputs)
            if _nonzero_global_rank() is not None:
                # Interim rule until per-writer leases (plan 2.8): every rank of
                # a distributed job attaches to the SAME run, so whichever rank
                # exited first closed it for all of them, and a later rank's
                # `completed` overwrote an earlier one's `failed`. Rank 0 (and
                # the launcher that opened the run) own the verdict; this rank
                # still delivers everything it logged, and its crash evidence.
                run._sends_terminal_status = False
    except BaseException as exc:
        # A failed init must not leak the transport (and its heartbeat threads)
        # that only exists because init built it.
        if owned is not None:
            owned.close()
        if _falls_back_offline(exc):
            fallback = _fall_back_offline(
                kw,
                getattr(client, "_last_run_create", None),
                getattr(client, "settings", None),
                reinit_mode=reinit_mode,
                capture={
                    "capture_reads": capture_reads,
                    "capture_outputs": capture_outputs,
                    "ignore": ignore,
                },
            )
            if fallback is not None:
                return fallback
        raise
    binding = _Binding(run=run, close_client=owned, attached=attached)
    _bind_new(binding, reinit_mode)
    _install_exit_hooks()
    _install_sigterm_flush()
    _arm_ray_trial_exit(run)
    # What this process reads becomes the run's inputs (lineage). Never a
    # gate: a failure to start warns and the run goes on unrecorded.
    try:
        from . import inputs as _inputs

        if _inputs.start(
            run.id,
            capture_reads=capture_reads,
            capture_outputs=capture_outputs,
            client=run._client,
            ignore=run._ignore_rules(),
        ):
            # Python workers this process spawns (spawn/forkserver) record
            # into the run too, while it is the only one recording here (F5).
            _inputs.bind_workers(run.id)
            _inputs.start_recovery(run._client)
    except Exception:  # noqa: BLE001
        pass
    # Arm the hard-exit breadcrumb, and sweep whatever earlier processes left
    # behind. Both are best-effort and both are deliberately on the init path:
    # a run opening is the one moment we know a client, a journal and a run id
    # are all in hand, and a crash-looping job re-enters here every restart --
    # which is precisely when its predecessor's breadcrumb needs collecting.
    #
    # Under the SAME BaseException guard as the run creation above: diagnostics
    # swallows Exception but not KeyboardInterrupt, and an escape here would
    # leak the transport and its heartbeat threads that only exist because init
    # built them.
    try:
        from . import diagnostics

        diagnostics.sweep(run._client)
        diagnostics.arm(run._client, run.id)
    except BaseException:
        if owned is not None:
            owned.close()
        raise
    return run



def _bind_new(binding: _Binding, reinit_mode: str) -> None:
    """Bind a run :func:`init` just opened (online or offline) -- or, under
    ``reinit="create_new"``, keep it unbound and closed with its handle."""
    global _process_default, _exit_status, _exit_exception, _exit_code, _exit_via, _exit_recorded
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
            _exit_status = "completed"
            _exit_recorded = False
            _exit_exception = None
            _exit_code = None
            _exit_via = None


def _falls_back_offline(exc: BaseException) -> bool:
    """`PROBE_INIT_FALLBACK=offline` and the API, not the request, failed: a
    network failure or a 5xx after init's budget. Never a refusal (401/403/
    404/409/422: going offline would only defer the same refusal) and never
    an attach (PROBE_RUN_ID names a run only the server has)."""
    from .offline import fallback_enabled

    if not fallback_enabled() or os.environ.get("PROBE_RUN_ID", "").strip():
        return False
    return isinstance(exc, (errors.TransportError, errors.ServerError))


def _fall_back_offline(
    kw: dict,
    sent_create: dict | None,
    settings: Any = None,
    *,
    reinit_mode: str = "default",
    capture: dict | None = None,
) -> "Run | None":
    """`PROBE_INIT_FALLBACK=offline`: record offline what init could not open.

    ``sent_create`` is the last run create this init sent, if it got that far
    (`Client._create_idempotently`). One that did not land is recorded as an
    offline create UNDER ITS KEY, with the request kept beside it: `probe sync`
    sends the offline create first and replays the kept request only if the
    server says that key already made a run (its answer was lost), so a create
    that landed is found, not duplicated, and one that did not becomes a real
    offline run (offline, the real start time) -- whatever the failure looked
    like from here (a lost answer, a gateway 503, a refused connection).

    None -- and init raises its own failure -- when recording offline would be
    wrong: the create LANDED (init failed after it; a second, offline run would
    duplicate it), or offline cannot do what init was asked (an ``on_conflict``
    only the server can decide, including the default with an ``external_id``;
    see `offline.open_offline_run`)."""
    from . import safe_warn

    if sent_create is not None and sent_create.get("landed"):
        safe_warn.warn(
            "probe: PROBE_INIT_FALLBACK=offline did not record this run offline: its "
            "create reached the server before init failed, so an offline copy would be "
            "a second run; raising the failure that ended init"
        )
        return None
    try:
        # The online client's settings: the server this run was meant for, which
        # the queue records and `probe sync` checks it is delivered to.
        return _init_offline(
            kw,
            sent=sent_create,
            fallback=True,
            settings=settings,
            reinit_mode=reinit_mode,
            capture=capture,
        )
    except errors.ValidationError as why:
        safe_warn.warn(
            f"probe: PROBE_INIT_FALLBACK=offline could not record this run offline ({why}); "
            "raising the failure that ended init"
        )
        return None


def _init_offline(
    kw: dict,
    *,
    sent: dict | None = None,
    fallback: bool = False,
    settings: Any = None,
    reinit_mode: str = "default",
    capture: dict | None = None,
) -> "Run":
    """``PROBE_MODE=offline`` (or the init fallback): bind a run recorded with
    no network (unbound under ``reinit="create_new"``, as online). See
    :mod:`probe.sdk.offline`. The exit hooks close it (a queued close, no
    waiting). What the run reads and writes is recorded as online (F6) and
    queued with its other writes at the close, for ``probe sync`` to deliver;
    ``capture_reads`` / ``capture_outputs`` / ``ignore`` (popped from ``kw``, or
    handed over by the fallback in ``capture``) shape it. The crash breadcrumb
    is skipped: it needs the server."""
    if os.environ.get("PROBE_RUN_ID", "").strip():
        raise errors.ValidationError(
            "PROBE_MODE=offline cannot attach to PROBE_RUN_ID: that run exists only on "
            "the server. Unset PROBE_RUN_ID to record a new run offline."
        )
    from .offline import open_offline_run

    capture = dict(capture or {})
    for name in ("capture_reads", "capture_outputs", "ignore"):
        if name in kw:
            capture[name] = kw.pop(name)
    ignore = capture.get("ignore")
    if ignore is not None:
        from . import ignore as _ignore

        try:
            ignore = _ignore.normalize(ignore)
        except ValueError as exc:
            raise errors.ValidationError(str(exc)) from None
    run = open_offline_run(kw, sent=sent, fallback=fallback, settings=settings)
    _bind_new(_Binding(run=run, close_client=run._client), reinit_mode)
    _install_exit_hooks()
    _install_sigterm_flush()
    # Never a gate, as online. No recovery from here: an offline client has
    # no server to send other runs' leftovers to.
    try:
        from . import inputs as _inputs

        run._set_ignore(ignore)
        if _inputs.start(
            run.id,
            capture_reads=capture.get("capture_reads"),
            capture_outputs=capture.get("capture_outputs"),
            client=run._client,
            ignore=run._ignore_rules(),
            offline_dir=run.offline_dir,
        ):
            _inputs.bind_workers(run.id)
    except Exception:  # noqa: BLE001
        pass
    return run


def _init_disabled(kw: dict, *, bind: bool = True) -> "Run":
    """``PROBE_MODE=disabled``: bind a run that records nothing.

    No Client (so no network and no outbox directory), no exit hooks, no
    capture. Bound like a real run so ``probe.log()`` and ``probe.finish()``
    work unchanged from anywhere in the script -- unless ``bind`` is False
    (``reinit="create_new"``, whose runs are never bound)."""
    global _process_default
    from .disabled import DisabledRun

    run = DisabledRun(name=kw.get("name"), config=kw.get("config"), tags=kw.get("tags"))
    # Open beside a recording run, it still makes that run's worker binding
    # unsafe: its own workers' reads are not the other run's (F5). In memory.
    from . import _open_runs

    _open_runs.opened(run)
    if not bind:
        return run  # type: ignore[return-value]
    binding = _Binding(run=run, close_client=None)  # type: ignore[arg-type]
    _current.set(binding)
    with _default_lock:
        _process_default = binding
    return run  # type: ignore[return-value]


#: Kwargs that CHOOSE or DESCRIBE a run at creation. When PROBE_RUN_ID already
#: chose one, passing these is a contradiction, not a refinement: silently
#: preferring either side is how telemetry lands on a run nobody was looking at.
_IDENTITY_KWARGS = ("experiment", "project", "name", "slug", "question", "hypothesis")


def _attach_from_env(client: Client, kw: dict) -> "Run | None":
    """Attach to the run named by PROBE_RUN_ID, or None if there is none.

    The epoch rides along when the launcher exported one: a run id names a ROW,
    not an execution attempt, and without the epoch a stale process holding an
    old id would attach to a row a newer attempt had already reopened and
    inherit its write authority.

    A conflicting kwarg RAISES rather than being ignored or honoured. The
    environment has already chosen the run; a caller who also passes
    ``experiment=`` either does not know that or is running the wrong script,
    and both deserve to find out at import rather than at read time.
    """
    run_id = os.environ.get("PROBE_RUN_ID", "").strip()
    if not run_id:
        return None
    conflicting = sorted(k for k in _IDENTITY_KWARGS if kw.get(k) is not None)
    if conflicting:
        raise errors.ValidationError(
            f"probe.init() received {', '.join(conflicting)} while PROBE_RUN_ID="
            f"{run_id} is set. The run is already chosen by the environment -- a "
            "launcher opened it and handed it to this process. Drop those "
            "arguments to join that run, or unset PROBE_RUN_ID to create a new "
            "one; doing both would write this job's telemetry onto whichever run "
            "happened to win."
        )
    # Everything else a caller passed is DROPPED -- attach_run has no use for
    # it. Silence there is its own failure: `probe.init(hw=True)` would stop
    # collecting hardware metrics with no sign, and tags/description would
    # simply not arrive. Name them. `config` is the exception (plan (c)): it
    # merges into the joined run below, from global rank 0 only.
    config = kw.get("config")
    dropped = sorted(k for k, v in kw.items() if v is not None and k != "config")
    if dropped:
        warnings.warn(
            f"probe.init() ignored {', '.join(dropped)} while attaching to "
            f"PROBE_RUN_ID={run_id}: an attach joins a run that already exists, "
            "so creation-time arguments have nothing to apply to. Set them on "
            "the launcher that opened the run, or with run.set_* afterwards.",
            stacklevel=3,
        )
    raw_epoch = os.environ.get("PROBE_RUN_EPOCH", "").strip()
    try:
        write_epoch = int(raw_epoch) if raw_epoch else None
    except ValueError:
        # An unreadable epoch is not a reason to refuse the attach: the server
        # still fences on its own copy. Warn and attach unfenced.
        warnings.warn(
            f"PROBE_RUN_EPOCH={raw_epoch!r} is not an integer; attaching without "
            "the writer-epoch fence",
            stacklevel=3,
        )
        write_epoch = None
    run = client.attach_run(
        run_id,
        heartbeat=True,
        # Beats from here say "the job itself is reporting", which is what
        # stamps attached_at. The launcher's own beats deliberately do not.
        attached=True,
        # A queued job can reach its run after the created-sweep already ended
        # it. Reopening is how a late start rejoins instead of beating into a
        # silent no-op for the rest of its life.
        reopen_if_dead=True,
        write_epoch=write_epoch,
    )
    # One line, because the alternative is a researcher wondering why their
    # curves are on a run they did not create.
    print(f"probe: attached to run {run.slug or run.id} via PROBE_RUN_ID", flush=True)
    if config is not None and _nonzero_global_rank() is None:
        # Under `probe exec` the launcher created the run without the script's
        # config, so this is the only place it can arrive. One rank is enough:
        # every rank of a job passes the same config.
        run.update_config(config)
    return run


def finish(status: str = "completed", **kw: Any):
    """Close the active run, flush its spool, and release the client init built.

    A no-op when nothing is active, so calling it twice (or in a ``finally``
    beside a ``with``) is safe."""
    binding = _binding(required=False)
    if binding is None:
        return None
    result = None
    try:
        result = binding.run.finish(status, **kw)
        return result
    finally:
        # NB: disarming lives in Run.finish, not here. This wrapper is only one
        # of the paths that close a run -- `with probe.init(...) as run:` goes
        # through Run.__exit__ -> Run.finish and never reaches this function, so
        # a breadcrumb disarmed only here stayed armed for the ergonomic the
        # docs actually advertise.
        #
        # A close still running on this same thread (a signal handler calling
        # probe.finish() mid-close) is using the client: releasing it here
        # made that close's terminal write fail. The running close's caller
        # releases it.
        if not (isinstance(result, dict) and result.get("finish_in_progress")):
            _release(binding)


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


def _reinit_bound(run: "Run") -> float:
    """A reinit's close deadline: ``PROBE_FINISH_TIMEOUT_SEC`` (600 s unset),
    never more than `_REINIT_FLUSH_CAP_S`. The caller waits for a new run."""
    return min(run._resolve_finish_timeout(None), _REINIT_FLUSH_CAP_S)


def _retire(binding: _Binding) -> None:
    """Let go of a run closed through its handle. Never raises.

    After a ``finish()`` this is a release. After a bare ``set_status`` --
    ``run.execute()`` closes its run that way -- ``finish()`` (idempotent)
    first does the rest of the close, bounded like a reinit: crumb, lineage,
    the drain, never a second verdict. A close still RUNNING (another thread's
    ``finish()``) is left alone: releasing closed the client it was sending
    through, and waiting could hold this caller for its whole deadline. Its
    own caller lets go of it, or the next look here does."""
    from .run import _FINISHING

    run = binding.run
    if getattr(run, "_finish_result", None) is _FINISHING:
        return
    started = time.monotonic()
    bound = _REINIT_FLUSH_CAP_S
    try:
        bound = _reinit_bound(run)
        run.finish(flush_timeout=bound)
    except Exception:  # noqa: BLE001 -- the run already has its verdict
        pass
    # Its client too, within the same bound (see `_close_binding`).
    _release_quietly(binding, timeout=max(0.0, bound - (time.monotonic() - started)))


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


def _reinit_mode(reinit: object) -> str:
    """W&B's ``reinit`` values; the booleans are W&B's (deprecated) spelling."""
    if reinit is True:
        return "finish_previous"
    if reinit is False:
        return "return_previous"
    if reinit is None or reinit == "default":
        return "finish_previous"  # D16
    if reinit not in _REINIT_MODES:
        raise errors.ValidationError(
            f"reinit must be one of {', '.join(_REINIT_MODES)} (or True/False), not {reinit!r}"
        )
    return str(reinit)


def _close_binding(binding: _Binding, *, closed_by: str) -> None:
    """Close a run because something else replaces it. Never raises.

    ``completed``, with ``probe_finish.closed_by`` in its summary so the run
    says why it ended. The close is BOUNDED -- at most
    ``min(PROBE_FINISH_TIMEOUT_SEC, 10)`` seconds (`_reinit_bound`), letting go
    of its client included -- and whatever is left is queued with the close
    behind it for the detached worker, because the caller is waiting for a new
    run, not for this one's backlog. One line says what happened: printed when
    the close landed, a warning when it is queued or failed. Ctrl-C (or a
    SystemExit) during it queues ``canceled`` behind the data instead of
    leaving the run for the reaper to call ``crashed`` -- unless the terminal
    write was already on its way, which the server may have applied: then that
    same status is queued again (`Run._close`). The interrupt then propagates.

    The marker is merged over the summary this handle last saw, because a
    summary write REPLACES the whole field on the server -- as a metadata
    write does. ``summary`` is where the close's own accounting
    (``probe_finish``) already lives, and the SDK writes a summary only when
    it closes a run, so what this handle saw is what the server has unless a
    caller queued a summary write of their own."""
    from . import safe_warn

    run = binding.run
    if getattr(run, "disabled", False):
        # PROBE_MODE=disabled recorded nothing, so there is nothing to close
        # or say: its handle finishes and lets go.
        try:
            run.finish("completed")
        except Exception:  # noqa: BLE001 -- the new run must still open
            pass
        _release_quietly(binding)
        return
    label = run.slug or run.id
    bound = _REINIT_FLUSH_CAP_S
    started = time.monotonic()
    try:
        existing = run.data.get("summary_metrics") or run.data.get("summary") or {}
        if not isinstance(existing, dict):
            existing = {}
        accounting = existing.get("probe_finish")
        summary = {
            **existing,
            "probe_finish": {**(accounting if isinstance(accounting, dict) else {}), "closed_by": closed_by},
        }
        bound = _reinit_bound(run)
        # Not the caller's choice to close it, so an interrupt is not a
        # `completed` it asked for. `Run._close` queues it on an interrupt in
        # either window, the finalizers or the drain and terminal write.
        run._status_on_interrupt = "canceled"
        # Never strict: a reinit never raises, and a strict close refuses
        # rather than queueing the verdict behind what it could not deliver.
        result = run.finish("completed", summary=summary, flush_timeout=bound, strict=False)
    except Exception as exc:  # noqa: BLE001 -- the new run must still open
        try:
            run.stop_heartbeat()
        except Exception:  # noqa: BLE001
            pass
        safe_warn.warn(
            f"probe: run {label} did not close cleanly when probe.init() replaced it "
            f"({safe_warn.describe(exc)}); see `probe outbox status`",
            stacklevel=3,
        )
    else:
        if isinstance(result, dict) and (result.get("close_rejected") or result.get("close_unrecorded")):
            safe_warn.warn(
                f"probe: run {label} did not close cleanly when probe.init() replaced it "
                "(the close was rejected or could not be recorded); see `probe outbox status`",
                stacklevel=3,
            )
        elif isinstance(result, dict) and result.get("offline"):
            pass  # an offline close always queues; its own line says where
        elif isinstance(result, dict) and result.get("finish_queued"):
            safe_warn.warn(
                f"probe: closed run {label} because probe.init() opened another; "
                f"{result.get('remaining', 0)} write(s) could not be delivered in "
                f"{bound:g}s and are queued, with the close behind them",
                stacklevel=3,
            )
        else:
            print(
                f"probe: closed run {label} (completed) because probe.init() opened "
                'another; pass reinit="create_new" to keep both open',
                flush=True,
            )
    finally:
        # Closing the client joins its exporter, which a hung API holds
        # mid-request: within what is left of the bound, not 5 s past it.
        _release_quietly(binding, timeout=max(0.0, bound - (time.monotonic() - started)))


# -- forwarding surface --------------------------------------------------------
# Deliberately small. These are the calls that happen deep inside a training loop
# where threading a handle through is the actual friction; anything rarer is one
# `probe.active_run().<verb>()` away and does not need ambient state.
def log(metrics: dict[str, Any], **kw: Any):
    """Append metric points to the active run. See :meth:`probe.sdk.run.Run.log`."""
    try:
        binding = _binding()
    except _ReinitStillOpening:
        _drop_during_reinit("log")
        return None
    return binding.run.log(metrics, **kw)


def expect(ranges: dict[str, Any], **kw: Any):
    """Declare where metrics should stay; Probe emails you when one leaves.

    ::

        probe.init(project="my-project")
        probe.expect({"val/acc": (0.5, 1.0), "train/loss": (None, 20)})

    Optional, and it never raises into your script: with no active run it
    warns and does nothing. See :meth:`probe.sdk.run.Run.expect`."""
    binding = _binding(required=False)
    if binding is None:
        from . import safe_warn

        safe_warn.warn("probe.expect: no active run, nothing recorded -- call probe.init() first")
        return None
    return binding.run.expect(ranges, **kw)


def update_config(values: Any, **kw: Any):
    """Merge ``values`` into the active run's config (plan (c)): shallow, new
    wins. See :meth:`probe.sdk.run.Run.update_config`."""
    return _binding().run.update_config(values, **kw)


def log_hw(metrics: dict[str, Any], **kw: Any):
    """Hardware metrics with dimensions. See :meth:`probe.sdk.run.Run.log_hw`."""
    try:
        binding = _binding()
    except _ReinitStillOpening:
        _drop_during_reinit("log_hw")
        return None
    return binding.run.log_hw(metrics, **kw)


def log_artifact(name: str, **kw: Any):
    """Record an artifact on the active run. See :meth:`probe.sdk.run.Run.log_artifact`."""
    try:
        binding = _binding()
    except _ReinitStillOpening:
        _drop_during_reinit("log_artifact")
        return None
    return binding.run.log_artifact(name, **kw)


def span(span_type: str, **kw: Any) -> "SpanHandle":
    """Open a span on the active run. See :meth:`probe.sdk.run.Run.span` — the
    returned handle is a context manager."""
    return _binding().run.span(span_type, **kw)


def context(**ids: Any) -> FailureContext:
    """Name the batch/sample the block is processing, for crash reports ONLY::

        for epoch in range(epochs):
            for i, batch in enumerate(loader):
                with probe.context(batch_id=i, epoch=epoch):   # or sample_id= / task_id=
                    train_step(batch)   # its probe.log() calls are unchanged

    A crash inside the block reaches the crash email as ``Batch: 17`` /
    ``Epoch: 3``; metrics logged inside are sent exactly as they would be
    outside it (unlike ``run.unit(labels=...)``, which would stop the curve
    plotting). See :meth:`probe.sdk.run.Run.context` for the keys.

    Unlike the other forwarders this one never raises: with no active run it
    is a no-op context manager, so it is safe in library code that may or may
    not run under ``probe.init()``."""
    found = _binding(required=False)
    return FailureContext(getattr(found.run, "id", None) if found is not None else None, ids)


# -- exit hooks ----------------------------------------------------------------
# How the process ends decides how the run ends, and Python announces it in
# three places, none of which sees the others:
#
#   * an uncaught exception reaches ``sys.excepthook`` (never a SystemExit);
#   * ``sys.exit(code)`` raises a SystemExit no hook ever sees -- Hydra and
#     Lightning both end a failed or interrupted job this way, from INSIDE their
#     own ``except`` blocks, so the traceback is swallowed and the exit is all
#     that is left;
#   * atexit runs after both and is the only place a run can still be closed.
#
# So the first two RECORD and atexit ACTS. The sys.exit wrapper is W&B's
# (`wandb/sdk/lib/exit_hooks.py`): replace ``sys.exit``, remember the code, call
# the previous one. Code-less exits a library raises itself (Lightning's
# SIGTERMException) reach none of them; the integration says so through
# :func:`note_exit`.
#
# KNOWN LIMITS, shared with W&B: an exit that never calls the wrapper is not
# seen -- ``raise SystemExit(2)``, the ``exit()`` builtin, a ``from sys import
# exit`` taken before ``probe.init()``, and above all ``sys.exit(main())`` with
# ``probe.init()`` inside ``main()``, where ``sys.exit`` is looked up before
# ``main()`` runs. With no launcher such a run closes ``completed``. Under
# ``probe exec`` it is right: with nothing recorded the child leaves the close to
# the launcher, which has the real exit code (``EXEC_FINALIZES_ENV``). A
# ``sys.exit(2)`` the script catches and survives still records ``failed``.
#
#: The chain lives on ``sys``, not in this module, like ``sys._probe_reads_state``
#: in inputs.py: ``importlib.reload(fluent)`` re-runs this file in the SAME module
#: dict while ``sys.exit`` is still the wrapper whose globals ARE that dict. With
#: the chain in module globals, a reload reset "the previous sys.exit" to None
#: (every exit raised TypeError) and a re-install captured the wrapper as its own
#: predecessor (RecursionError). Keys: ``exit`` and ``excepthook`` -- what was
#: installed before us -- and ``pid``, the process whose exit is the bound run's.
#: A forked child inherits all of it together with the parent's binding, so
#: without the pid a child's exit closed the PARENT's run with its own verdict.
_HOOKS_ATTR = "_probe_exit_hooks"
_exit_status = "completed"
#: Whether a hook saw how the process is ending (sys.exit, the excepthook,
#: note_exit). When none did, the status at exit is a guess -- see
#: :func:`_finish_at_exit`.
_exit_recorded = False
#: The exception that ended the process, held for :func:`_finish_at_exit` to
#: report. This hook is the only place in the client where a dying run's
#: traceback is in scope; until it was kept, the sole evidence a crash left
#: behind was ``_exit_status``, which says THAT the run broke and never why.
_exit_exception: BaseException | None = None
#: The non-zero code the process is exiting with, and what reported it
#: (``sys.exit`` or ``excepthook``). Written as the run's ``exit`` process span,
#: which is where the crash email reads an exit code from (`_EXIT_SQL`).
_exit_code: int | None = None
_exit_via: str | None = None

_EXIT_STATUSES = ("completed", "failed", "canceled")

#: (rank, world size) environment variables naming a GLOBAL rank, most specific
#: first: under `srun` + `torchrun`, SLURM_PROCID numbers the node while RANK
#: numbers the worker. LOCAL_RANK is absent on purpose -- it repeats per node.
_GLOBAL_RANK_VARS = (
    ("RANK", "WORLD_SIZE"),
    ("SLURM_PROCID", "SLURM_NTASKS"),
    ("OMPI_COMM_WORLD_RANK", "OMPI_COMM_WORLD_SIZE"),
)


def _int_env(name: str) -> int | None:
    try:
        return int((os.environ.get(name) or "").strip())
    except ValueError:
        return None


def _nonzero_global_rank() -> int | None:
    """The global rank of this process when it is above 0, else None.

    ANY advertised rank above 0 counts: a worker is rank 0 only if every
    scheme that numbers it agrees. A rank whose own world size says the job is
    one process (``RANK=3 WORLD_SIZE=1``, a left-over export) does not count,
    and neither does a negative one (``RANK=-1``, "not distributed")."""
    for rank_var, size_var in _GLOBAL_RANK_VARS:
        rank = _int_env(rank_var)
        if rank is None or rank <= 0:
            continue
        size = _int_env(size_var)
        if size is not None and size <= 1:
            continue
        return rank
    return None


def _hooks() -> dict | None:
    state = getattr(sys, _HOOKS_ATTR, None)
    return state if isinstance(state, dict) else None


def _in_hooks_process() -> bool:
    state = _hooks()
    return state is not None and state.get("pid") == os.getpid()


def _record_exit(
    status: str,
    *,
    exc: BaseException | None = None,
    code: int | None = None,
    via: str | None = None,
) -> None:
    """Remember how the process is ending, for :func:`_finish_at_exit`.

    Last word wins: a Lightning Ctrl-C reports through :func:`note_exit` and
    then through its own ``sys.exit(1)``, and both say ``canceled``."""
    global _exit_status, _exit_exception, _exit_code, _exit_via, _exit_recorded
    _exit_recorded = True
    _exit_status = status
    # Only a failure is diagnosed. Ctrl-C is a decision, not a defect, and a
    # process that chose to exit 0 has declared the exception handled.
    _exit_exception = exc if status == "failed" else None
    _exit_code = code or None
    _exit_via = via if code else None


def note_exit(status: str, exc: BaseException | None = None) -> None:
    """Tell the close at exit how this process is ending. For integrations.

    Some endings reach no process hook at all. Lightning turns SIGTERM into
    ``SIGTERMException``, a code-less SystemExit: the process exits 0, the
    excepthook never runs, and the run would close ``completed``. A trainer's
    ``on_exception`` sees it, so the integration calls this from there:
    KeyboardInterrupt -> ``"canceled"``; ``SIGTERMException`` or anything else
    -> ``"failed"``, passing the exception so it is reported as the run's
    diagnostic. The run is closed with this status when the process exits.

    Not a signal handler itself. The SIGTERM handler `init` installs
    (:mod:`probe.sdk.preempt`) runs AFTER a framework's own -- Lightning's
    composes with it -- and a close on the way out of a SIGTERM is
    ``failed`` whatever is noted here.
    """
    if status not in _EXIT_STATUSES:
        raise errors.ValidationError(
            f"note_exit status must be one of {', '.join(_EXIT_STATUSES)}, not {status!r}"
        )
    if not _in_hooks_process():
        # No probe.init() in this process -- or a forked child, whose ending
        # is not the parent's run's.
        return
    _record_exit(status, exc=exc)
    binding = _binding(required=False)
    if binding is not None:
        # Also on the run itself: inside `with probe.init()`, the block closes
        # the run before any exit hook runs, and a code-less SystemExit
        # (Lightning's SIGTERMException) alone reads as success there.
        binding.run._noted_exit = (status, exc)


def _forget_noted_exit(run: "Run") -> None:
    """Take back a :func:`note_exit` the process outlived. For integrations.

    A sweep loop caught the error one trainer noted, and a new trainer is now
    starting on the same run (the script's, or a launcher's): that ending was
    not the process's, and it must not close the run ``failed`` at exit. The
    process-wide record is cleared only while it is still the one ``note_exit``
    made -- anything recorded since (a ``sys.exit`` wrapper) stands."""
    global _exit_status, _exit_exception, _exit_code, _exit_via, _exit_recorded
    noted = getattr(run, "_noted_exit", None)
    if noted is None:
        return
    run._noted_exit = None
    if not _in_hooks_process():
        return
    status, exc = noted
    if (
        _exit_recorded
        and _exit_status == status
        and _exit_code is None
        and _exit_exception is (exc if status == "failed" else None)
    ):
        _exit_status = "completed"
        _exit_recorded = False
        _exit_exception = None
        _exit_via = None


def _exit(code: object = None) -> None:
    """``sys.exit``, recording the code first, then the previous one -- which
    raises the SystemExit, so whatever was installed before still decides."""
    try:
        _note_system_exit(code)
    except Exception:  # noqa: BLE001 -- nothing may stand between a script and its exit
        pass
    try:
        _close_ending_ray_trial(code)
    except Exception:  # noqa: BLE001 -- as above
        pass
    previous = (_hooks() or {}).get("exit")
    if previous is None or previous is _exit:
        raise SystemExit(code)
    previous(code)


# -- Ray Tune: the trial's thread ends, then Ray kills the process -------------
# A Ray Tune function trainable runs on Ray's `RunnerThread` in the trial's
# actor, and Tune ends it there: when it stops the trial -- a scheduler's early
# stop (ASHA, median stopping), or after the function returned, which Ray
# reports as one last result -- the `tune.report()` the thread waits in calls
# ``sys.exit(0)`` (`_TrainSession._report_training_result`). The actor's
# `stop()` does not wait for the thread; Tune removes the trial's placement
# group, and the raylet SIGTERMs the actor's process group and SIGKILLs it
# 200 ms later (hard-coded, Ray 2.58 `NodeManager::DisconnectClient`). Ray's
# SIGTERM handler ends the main thread, so the atexit close started only after
# Ray's own shutdown (15-80 ms in, measured): over a real network it was killed
# mid-request, and the run stayed `running` with its lease held -- the output
# helper, in the same group, died too, so nothing reported it gone.
#
# So a ``sys.exit`` on that thread closes the run the thread opened, THERE, with
# no budget: ``flush_timeout=0`` sends nothing, it queues the verdict (the lease
# release) behind the run's data and hands the queue to the detached outbox
# worker -- milliseconds of local work. That worker is started again at exit,
# past Ray's kill of the actor's children (`_arm_ray_trial_exit`). The
# verdict is the exit code's, as for any ``sys.exit``: Ray's stop is 0, so
# `completed` -- Tune records the trial TERMINATED, as one that ran every
# iteration; `canceled` means a person's Ctrl-C. A `tune.Trainable` class needs
# none of this: Tune runs its `cleanup()` and waits for it, so `probe.finish()`
# there closes the run in full.


def _ray_trial_thread() -> bool:
    """Whether this thread runs a Ray Tune function trainable: Ray's
    ``RunnerThread``, which a ``SystemExit`` ends (it never reaches the process).
    By the thread's class, never through Ray's session: the actor's `stop()`
    clears that session (``shutdown_session()``) as it releases the thread, so
    by the time the thread's ``sys.exit(0)`` runs it is already gone. Never
    imports Ray: a process that has not loaded it has no trial."""
    util = sys.modules.get("ray.air._internal.util")
    runner = getattr(util, "RunnerThread", None)
    return isinstance(runner, type) and isinstance(threading.current_thread(), runner)


def _close_ending_ray_trial(code: object) -> None:
    """A ``sys.exit`` is ending the Ray Tune trial function on this thread:
    close the run this thread opened now, queue-only (see above). Not on the
    main thread, where the process's own exit hooks close it."""
    global _ray_closes
    if threading.current_thread() is threading.main_thread():
        return
    if not _in_hooks_process() or not _ray_trial_thread():
        return
    binding = _binding(required=False)
    if binding is None or binding.owner[:2] != (os.getpid(), threading.get_ident()):
        return
    from .run import _status_for_system_exit

    status, _ = _status_for_system_exit(code, sys.exc_info()[1])
    with _ray_closing:
        _ray_closes += 1
    try:
        finish(status, flush_timeout=0)
    except Exception as exc:  # noqa: BLE001 -- the trial ends either way; say so
        _warn_not_closed_at_exit(binding.run, exc)
    finally:
        with _ray_closing:
            _ray_closes -= 1
            _ray_closing.notify_all()


#: Ray-trial closes running now (`_close_ending_ray_trial`), which the exit
#: kick waits out; and the outboxes it kicks at exit.
_ray_closing = threading.Condition()
_ray_closes = 0
_ray_exit_kicks: set[str] = set()
#: The longest the exit kick waits for a trial close still running. Ray's
#: SIGKILL ends the wait far sooner; outside a teardown nothing is running.
_RAY_EXIT_KICK_WAIT_S = 5.0
#: The longest the exit kick waits for the outbox worker Ray's shutdown just
#: SIGKILLed to let go of its lease (`outbox_worker.spawn_past_a_kill`): a few
#: ms normally, and Ray's group SIGKILL at 200 ms ends a teardown's wait
#: anyway. Only a live worker's lease -- a sibling trial's -- waits it out.
_RAY_KILLED_WORKER_WAIT_S = 0.5


def _arm_ray_trial_exit(run: "Run") -> None:
    """A run opened on a Ray trial's thread: start the outbox worker again at
    interpreter exit. Ray's core worker, shutting down on the SIGTERM,
    SIGKILLs the actor's direct children (``kill_child_processes_on_worker_exit``,
    on by default) -- the detached outbox worker this process started among
    them, however far it had got with the queue and the queued close. atexit
    runs after that sweep and before the group's SIGKILL: a worker started
    there is past the sweep, and in a session of its own the group's SIGKILL
    misses it. Armed at the open, not at the close: that close may still be
    running when the main thread reaches atexit, and a handler registered then
    never runs -- so the kick waits for it instead. Never raises."""
    try:
        client = run._client
        if not _ray_trial_thread() or not getattr(client, "_default_transport", False):
            return
        journal_dir = str(client.journal.dir)
    except Exception:  # noqa: BLE001 -- a run's open never fails over this
        return
    with _ray_closing:
        if journal_dir in _ray_exit_kicks:
            return
        _ray_exit_kicks.add(journal_dir)

    def kick() -> None:
        try:
            with _ray_closing:
                _ray_closing.wait_for(lambda: _ray_closes == 0, timeout=_RAY_EXIT_KICK_WAIT_S)
            from . import outbox_worker

            # Past the worker Ray just killed, whose lease outlives the kill
            # by the time the kernel takes to tear it down.
            outbox_worker.spawn_past_a_kill(journal_dir, wait=_RAY_KILLED_WORKER_WAIT_S)
        except Exception:  # noqa: BLE001 -- best effort, like every kick
            pass

    atexit.register(kick)


def _note_system_exit(code: object) -> None:
    if threading.current_thread() is not threading.main_thread():
        # sys.exit in a worker thread ends that thread, not the process: the
        # script goes on, and so does the run.
        return
    if not _in_hooks_process():
        return
    if "ipykernel" in sys.modules:
        # A notebook: IPython catches the SystemExit and the kernel carries on,
        # so the cell stopping says nothing about how the run ends. The same
        # heuristic outputs.py uses to keep fd capture out of notebooks.
        return
    from .run import _status_for_system_exit

    in_flight = sys.exc_info()[1]
    # Lightning's Ctrl-C (`except KeyboardInterrupt: ... sys.exit(1)`) is
    # canceled: the person stopped it, the 1 is the framework's. The code is
    # what the OS will report -- `sys.exit(-1)` exits 255, never "a signal".
    status, exit_code = _status_for_system_exit(code, in_flight)
    _record_exit(
        status,
        # Hydra: `except Exception as e: ... sys.exit(1)` -- the traceback it
        # swallowed is the in-flight exception, and it is the crash report.
        exc=in_flight if isinstance(in_flight, Exception) else None,
        code=exit_code,
        via="sys.exit",
    )


def _excepthook(exc_type, exc, tb) -> None:
    if _in_hooks_process():
        # KeyboardInterrupt is a real lifecycle outcome in this vocabulary, and
        # it is the common way a training run ends early. Calling it 'failed'
        # would lose the distinction between "I stopped it" and "it broke" --
        # and Ctrl-C is a decision, not a defect: diagnosing it would file a
        # report on every interactive session anyone ever interrupts.
        if issubclass(exc_type, KeyboardInterrupt):
            _record_exit("canceled")
        else:
            # An uncaught exception exits 1.
            _record_exit("failed", exc=exc, code=1, via="excepthook")
    previous = (_hooks() or {}).get("excepthook")
    if previous is None or previous is _excepthook:
        previous = sys.__excepthook__
    previous(exc_type, exc, tb)


def _write_exit_span(
    run: "Run",
    code: int,
    via: str | None,
    status: str,
    *,
    extra: dict | None = None,
    direct: bool = False,
) -> None:
    """The exit code, as a ``process`` span named ``exit``. Never raises.

    The crash email reads a run's exit code from its latest process span
    (`_EXIT_SQL`); without this an in-process run that ended with
    ``sys.exit(2)`` and no traceback could only say it "was marked failed".
    Non-blocking, like the diagnostic: it must never hold the close. The id is
    derived, so writing it twice addresses one row; the epoch keeps a reopened
    run's exit apart from the first attempt's, and a non-zero rank writes its
    own rather than overwriting rank 0's. ``direct``: sent now, never queued
    (a SIGTERMed run's close on a throwaway disk, whose queue is stuck behind
    data that will not arrive); a queued copy that lands too is the same row."""
    try:
        from .run import _now

        rank = _nonzero_global_rank()
        key = f"exit:{run.write_epoch}" + (f":rank{rank}" if rank is not None else "")
        attributes: dict[str, Any] = {**(extra or {}), "exit_code": code, "via": via}
        if rank is not None:
            attributes["rank"] = rank
        now = _now()
        run.span(
            "process",
            name="exit",
            external_key=key,
            parent_span_id=None,
            status=status,
            started_at=now,
            ended_at=now,
            attributes=attributes,
            strict=direct,
            blocking=False,
        )
    except Exception:  # noqa: BLE001 -- evidence never gates a close
        pass


def _finish_at_exit() -> None:
    """Close a run the script never closed.

    Without this, a script that simply ends leaves its run ``running`` until the
    server's reaper marks it ``crashed`` — the wrong answer for one that
    succeeded. atexit still runs after an unhandled exception (the traceback
    prints first), so guessing ``completed`` for every exit would be a lie;
    :func:`_excepthook` and the ``sys.exit`` wrapper are what tell them apart."""
    if not _in_hooks_process():
        # A forked child inherits this registration AND the parent's binding;
        # its exit must not close the parent's run.
        return
    binding = _binding(required=False)
    if binding is not None and binding.owner[0] == os.getpid():
        # A forked child that opened its own run with create_new is still
        # BOUND to the parent's run it inherited; its exit must not close it.
        _close_bound_at_exit(binding)
    _finish_unbound_at_exit()


def _close_bound_at_exit(binding: _Binding) -> None:
    run = binding.run
    if getattr(run, "_closed_status", None) is not None or _finish_called(run):
        # The script closed it -- `run.finish(...)`, `with probe.init()`
        # ending, `run.execute()` -- and that verdict stands. Closing again
        # overwrote it: a `with` block that completed, then `sys.exit(2)` from
        # a gate check after it, turned a finished run `failed` and mailed a
        # crash notice. So no exit code and no crash report on it.
        # Still finish() it -- idempotent: the first close's answer, or a wait
        # for one still running, or the rest of the close a bare `set_status`
        # left (the crumb, lineage, the drain; review of #2016) -- and let go
        # of it: closing the client init() built is what makes the last export
        # pass, hands leftovers to the background uploader and seals the
        # outbox producer.
        try:
            finish(_exit_status)
        except Exception:  # noqa: BLE001 -- its verdict is already out
            _release_quietly(binding)
        return
    if not _exit_recorded and _launcher_finalizes(run):
        # No hook saw how this process ends, so `completed` would be a guess,
        # and it used to land first: `sys.exit(main())` looks sys.exit up
        # before main() calls probe.init(), and the launcher's own verdict,
        # from the real exit code, then deferred to it. Deliver the data and
        # leave the close to the launcher.
        run._sends_terminal_status = False
    # BEFORE finish(), never after: finish() flips the run terminal and owns
    # the delivery barrier, so a span written behind it races a closed run.
    # Both swallow unconditionally -- neither can stop the run being closed.
    if _exit_code:
        _write_exit_span(run, _exit_code, _exit_via, _exit_status)
    if _exit_exception is not None:
        from . import diagnostics

        diagnostics.report_exception(run, _exit_exception)
    try:
        finish(_exit_status)
    except Exception as exc:
        # Never raise from here -- it would only obscure whatever is ending the
        # process -- but never be silent either: a bare `pass` here is how one
        # busy-server 503 at exit left runs `running` until the reaper called
        # them `crashed`, with nothing on screen to say why.
        _warn_not_closed_at_exit(run, exc)


def _warn_not_closed_at_exit(run: "Run", exc: BaseException) -> None:
    """One line on stderr through the SDK's non-raising warning channel."""
    from . import safe_warn

    try:
        detail = f"{type(exc).__name__}: {exc}"
    except Exception:  # noqa: BLE001 -- a hostile __str__ must not stop the report
        detail = safe_warn.describe(exc)
    try:
        label = run.slug or run.id
    except Exception:  # noqa: BLE001
        label = "?"
    safe_warn.warn(
        f"probe: run {label} was not closed at exit ({detail[:300]}); it will be reaped "
        "as crashed -- see `probe outbox status`",
        stacklevel=2,
    )


def _finish_unbound_at_exit() -> None:
    """Close what ``reinit="create_new"`` opened and nothing closed since."""
    with _default_lock:
        # This process's own: a forked child inherits the parent's list, and
        # its exit must not close the parent's runs.
        pending = [b for b in _unbound if not b.closed and b.owner[0] == os.getpid()]
        _unbound.clear()
    for binding in pending:
        was_open = _is_open(binding)
        try:
            # Idempotent, like the bound run's: a run a bare `set_status`
            # closed (`run.execute()`) keeps its verdict and gets the rest.
            binding.run.finish(_exit_status)
        except Exception as exc:  # noqa: BLE001 -- interpreter teardown, as above
            if was_open:
                _warn_not_closed_at_exit(binding.run, exc)
        finally:
            _release_quietly(binding)


def _launcher_finalizes(run: "Run") -> bool:
    """A `probe exec` launcher runs this process and will close THIS run from
    its real exit code (`Run.execute(finalize=True)` names the run it closes;
    another run this process attached to has no such launcher)."""
    from .run import EXEC_FINALIZES_ENV

    return (os.environ.get(EXEC_FINALIZES_ENV) or "").strip() == run.id


def _install_sigterm_flush() -> None:
    """The run is open: put the SIGTERM flush in front of SIGTERM
    (:mod:`probe.sdk.preempt`; main thread only, never raises)."""
    from . import preempt

    preempt.install()


def _uninstall_sigterm_flush_if_idle() -> None:
    """No run of this process is open any more: give SIGTERM back what it had
    -- unless a handler installed after ours now holds it."""
    try:
        if _has_open_run():
            return
        from . import preempt

        preempt.uninstall()
    except Exception:  # noqa: BLE001 -- a close never fails over this
        pass


def _has_open_run() -> bool:
    """Whether this process has a run of its own still open (a close in
    progress counts). Lock-free: the SIGTERM handler calls it, and the frame it
    interrupted may hold `_default_lock`."""
    pid = os.getpid()
    for binding in (_current.get(), _process_default, *list(_unbound)):
        if binding is not None and not binding.closed and binding.owner[0] == pid:
            return True
    return False


def _close_for_preemption() -> None:
    """A SIGTERM is ending this process (:mod:`probe.sdk.preempt`, on its
    worker thread): close what :func:`_finish_at_exit` would close, ``failed``.
    `Run.finish` adds the preemption's facts and holds each close to the
    budget."""
    if not _in_hooks_process():
        return
    # Recorded, so a finalizing launcher's child still speaks (the launcher
    # never learns the SIGTERM), and no exit span from here: `Run.finish`
    # writes the preemption's own.
    _record_exit("failed")
    _finish_at_exit()


def _install_exit_hooks() -> None:
    """Install once per interpreter, under the lock.

    Unsynchronised, two threads calling :func:`init` concurrently — which this
    module explicitly supports — can both pass the check; the second then
    captures ``sys.excepthook`` AFTER the first replaced it, so the
    "previous" hook becomes :func:`_excepthook` itself and any later uncaught
    exception recurses until the stack blows. ``sys.exit`` is chained the same
    way, and for the same reason captured only once -- keyed on ``sys``, so a
    reloaded module does not capture its own wrapper either."""
    with _default_lock:
        state = _hooks()
        if state is None:
            state = {"exit": sys.exit, "excepthook": sys.excepthook}
            setattr(sys, _HOOKS_ATTR, state)
            sys.excepthook = _excepthook
            sys.exit = _exit
            atexit.register(_finish_at_exit)
        # A forked child that opens a run of its own adopts the hooks it
        # inherited (re-wrapping would chain them to themselves); from then on
        # its exit is ITS run's, and the parent's pid no longer matches.
        state["pid"] = os.getpid()
