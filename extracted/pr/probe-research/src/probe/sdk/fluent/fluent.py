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
:class:`~probe.sdk.client.client.Client` and :class:`~probe.sdk.run.run.Run` and forwards.
"""

from __future__ import annotations
import os
from typing import TYPE_CHECKING, Any

from .. import errors
from ..client.client import Client
from ..settings.settings import Mode, resolve_mode
from ..run.context.context import FailureContext

if TYPE_CHECKING:

    from ..run.run import Run
    from ..run.metrics.spans import SpanHandle


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

    Takes the same arguments as :meth:`~probe.sdk.client.client.Client.run`
    (``experiment``, ``question``, ``name``, ``project``, ``source``, ``tags``,
    …). Pass ``client=`` to reuse a configured one; otherwise a
    :class:`~probe.sdk.client.client.Client` is built from env / the stored login and
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
    (:mod:`probe.sdk.capture.lineage`).

    RETRIES FOR UP TO ``PROBE_INIT_TIMEOUT_SEC`` (default 90 s) when the API is
    unreachable or failing, then raises (plan 2.5, D9). ``0`` keeps the old
    few-quick-retries behaviour. A run create whose answer was lost is sent
    again only where the server replays it (``creation_key``), never twice.

    ``mode=`` (or ``PROBE_MODE``): ``"online"`` (default); ``"disabled"``,
    which returns a :class:`~probe.sdk.run.disabled.DisabledRun` that records
    nothing and touches neither the network nor the disk; or ``"offline"``
    (plan 2.12), which records the run with NO network call into a queue of its
    own for ``probe sync`` to deliver later (:mod:`probe.sdk.delivery.offline`).
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
    if run_mode is Mode.ONLINE and _names_offline_run():
        # An offline `execute()` hands its child its `local:<key>` id: a run only this
        # machine's queue holds, so the child joins it offline (no server knows it yet).
        run_mode = Mode.OFFLINE
    reinit_mode = _reinit_mode(reinit)
    if run_mode is not Mode.DISABLED:
        # A researcher's `.probe.config` excludes where this runs: no run, and
        # the script runs exactly as it would with `mode="disabled"`.
        from ..recording_rules import recording_rules as _exclusions
        from .. import probe_config as _probe_config

        hit = _exclusions.run_excluded()
        if hit is not None and hit[1].identity_only:
            # `hash`: the run opens (V9) and records metrics, config and file
            # identities; no bytes, and no console log (`outputs.log_enabled`).
            _exclusions.warn(_exclusions.say(_probe_config.INIT_HASH_ONLY, *hit))
        elif hit is not None:
            _exclusions.warn(_exclusions.say(_probe_config.INIT_EXCLUDED, *hit))
            run_mode = Mode.DISABLED
    if run_mode is not Mode.DISABLED:
        # This process does a run's work from here on, offline too: what it
        # writes is the run's, never its agent being active (R41).
        from .. import agent_session as _agent_session

        _agent_session.mark_run_process()
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
    from .. import redaction as _redaction

    _redaction.enable_scrub_cache()
    outputs = kw.pop("outputs", None)
    capture_outputs = kw.pop("capture_outputs", None)
    # `.probeignore` patterns (plan (n)): they apply to an attached run's
    # capture too, so they are popped before the attach check drops extras.
    ignore = kw.pop("ignore", None)
    if ignore is not None:
        from ..recording_rules import ignore as _ignore

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


def _names_offline_run() -> bool:
    named = os.environ.get("PROBE_RUN_ID", "").strip()
    if not named:
        return False
    from ..delivery.offline import LOCAL_PREFIX

    return named.startswith(LOCAL_PREFIX)


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


# -- forwarding surface --------------------------------------------------------
# Deliberately small. These are the calls that happen deep inside a training loop
# where threading a handle through is the actual friction; anything rarer is one
# `probe.active_run().<verb>()` away and does not need ambient state.
def log(metrics: dict[str, Any], **kw: Any):
    """Append metric points to the active run. See :meth:`probe.sdk.run.run.Run.log`."""
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
    warns and does nothing. See :meth:`probe.sdk.run.run.Run.expect`."""
    binding = _binding(required=False)
    if binding is None:
        from ...foundation.safe_warn import safe_warn

        safe_warn.warn("probe.expect: no active run, nothing recorded -- call probe.init() first")
        return None
    return binding.run.expect(ranges, **kw)


def update_config(values: Any, **kw: Any):
    """Merge ``values`` into the active run's config (plan (c)): shallow, new
    wins. See :meth:`probe.sdk.run.run.Run.update_config`."""
    return _binding().run.update_config(values, **kw)


def log_hw(metrics: dict[str, Any], **kw: Any):
    """Hardware metrics with dimensions. See :meth:`probe.sdk.run.run.Run.log_hw`."""
    try:
        binding = _binding()
    except _ReinitStillOpening:
        _drop_during_reinit("log_hw")
        return None
    return binding.run.log_hw(metrics, **kw)


def log_artifact(name: str, **kw: Any):
    """Record an artifact on the active run. See :meth:`probe.sdk.run.run.Run.log_artifact`."""
    try:
        binding = _binding()
    except _ReinitStillOpening:
        _drop_during_reinit("log_artifact")
        return None
    return binding.run.log_artifact(name, **kw)


def span(span_type: str, **kw: Any) -> "SpanHandle":
    """Open a span on the active run. See :meth:`probe.sdk.run.run.Run.span` — the
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
    plotting). See :meth:`probe.sdk.run.run.Run.context` for the keys.

    Unlike the other forwarders this one never raises: with no active run it
    is a no-op context manager, so it is safe in library code that may or may
    not run under ``probe.init()``."""
    found = _binding(required=False)
    return FailureContext(getattr(found.run, "id", None) if found is not None else None, ids)
from probe.sdk.fluent.bindings import _init_disabled, _release  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.reinit import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _ReinitStillOpening,
    _binding,
    _drop_during_reinit,
    _reinit_mode,
    _replace_previous,
)
from probe.sdk.fluent.run_openers.offline import _init_offline  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.run_openers.online import _open_and_bind  # noqa: E402 -- pieces need each other; the front door loads this one first
