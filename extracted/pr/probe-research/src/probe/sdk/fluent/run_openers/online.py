"""Open or attach the run through the client and bind it, falling back offline when PROBE_INIT_FALLBACK=offline and the API failed."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any

from ... import errors
from ...client.client import Client
from ...settings.settings import init_timeout_seconds
from ...delivery.transport.deadlines import patience

if TYPE_CHECKING:

    from ...run.run import Run


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
        from ...capture import lineage as _inputs

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
        from ... import diagnostics

        diagnostics.sweep(run._client)
        diagnostics.arm(run._client, run.id)
    except BaseException:
        if owned is not None:
            owned.close()
        raise
    return run


def _falls_back_offline(exc: BaseException) -> bool:
    """`PROBE_INIT_FALLBACK=offline` and the API, not the request, failed: a
    network failure or a 5xx after init's budget. Never a refusal (401/403/
    404/409/422: going offline would only defer the same refusal) and never
    an attach (PROBE_RUN_ID names a run only the server has)."""
    from ...settings.settings import env_run_id
    from ...delivery.offline.offline import fallback_enabled

    if not fallback_enabled() or env_run_id():
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
    from ....foundation.safe_warn import safe_warn

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
from probe.sdk.fluent.attach import _attach_from_env, _nonzero_global_rank  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.bindings import _Binding, _bind_new  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.exit import _install_exit_hooks, _install_sigterm_flush  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.ray import _arm_ray_trial_exit  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.fluent.run_openers.offline import _init_offline  # noqa: E402 -- pieces need each other; the front door loads this one first
