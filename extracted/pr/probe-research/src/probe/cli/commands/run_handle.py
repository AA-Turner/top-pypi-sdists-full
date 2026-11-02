"""the Run handle a run-scoped write goes through: read-first (`_run_handle`) or enqueue-only (`_async_run`)."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ...sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None


def _async_run(client: Client, run_ref: str):
    """A Run handle that does NOT read the run first: async enqueue must not
    block on (or fail without) the network; the server validates the ref at
    replay (eng review D20-1).

    Its writer epoch is whatever can be known OFFLINE (SDK reliability 1.10):
    the generation `run start` pinned in the bracket's lease, the same pin
    `_run_handle` applies, and otherwise none at all. It used to default to 1,
    which the server fences on any reopened run: every queued point
    dead-lettered, and a queued `run end` would have been refused."""
    from ...sdk.run.run import Run

    handle = Run(client, {"id": run_ref})
    try:
        from probe.foundation.durable import run_lock

        pinned = run_lock.lease_write_epoch(run_ref)
        if pinned is not None:
            handle.write_epoch = pinned
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        pass
    return handle


def _run_handle(client: Client, run_id: str, *, owns_process: bool = False):
    """A handle for a run-scoped CLI write.

    `owns_process` (0205) splits the two very different things this returns.

    The DEFAULT is the lease tier: `probe log`, `probe artifact`, `probe run
    set` -- one short write inside a detached `run start`...`run end` bracket
    with no process of ours alive in between. Such a handle must not beat: it
    would assert ownership for a second and then go silent, and the reaper reads
    that as a process that died.

    `owns_process=True` is the flock tier: `probe exec`, which lives for exactly
    as long as the child it wraps. That process CAN honestly beat for the run's
    whole life, and before 0205 it did not -- so a wrapped child that logged
    nothing for fifteen minutes was reaped mid-flight, which is the failure the
    wrapper existed to prevent. Its beats carry no `attached` flag: holding a
    run open is not the same as the job inside it reporting.
    """
    from ...sdk.run.run import Run

    # Every run-scoped CLI write funnels through here, which makes it the one
    # place a detached run's auto-update lease can be renewed without anyone
    # having to remember to. A bare `probe run start` ... `probe run end`
    # bracket has no process of ours alive in between, so its claim on the box
    # is a lease -- and this is the traffic that keeps it alive.
    #
    # No-ops for a run holding an flock (SDK, `probe exec`) and skips the write
    # until the lease is half spent, so `probe log` in a training loop does not
    # pay for it. See run_lock.renew_lease_if_stale.
    try:
        from probe.foundation.durable import run_lock

        run_lock.renew_lease_if_stale(run_id)
    except Exception:  # noqa: BLE001 -- a lock refresh must never break a write
        pass
    if owns_process:
        # Through the SDK's construction boundary so the beat thread, the
        # process-bound flock and the finalizer all come with it.
        handle = client.attach_run(run_id, heartbeat=True, attached=False)
    else:
        handle = Run(client, client.get_run(run_id))
    try:
        from probe.foundation.durable import run_lock

        # A live lease pins the bracket's writer generation (0185): stamp the
        # epoch `run start` opened under, not the row's current one, so a
        # bracket superseded by a reopen elsewhere fences instead of splicing.
        pinned = run_lock.lease_write_epoch(run_id)
        if pinned is not None:
            handle.write_epoch = pinned
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        pass
    return handle
from probe.cli.commands.refs import run_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
