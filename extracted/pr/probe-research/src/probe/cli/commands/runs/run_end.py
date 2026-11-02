"""probe run end: close a run (status, queued or direct) and apply an update deferred to its end."""

from __future__ import annotations
import time
from enum import Enum
from typing import Optional

import typer
from probe.cli.commands.refs import run_ref
from probe.cli.commands.runs.runs import run_app
from probe.cli.connection import (
    _async_client,
    _client,
    _journal,
    _kick_drainer,
    _resolve_write_mode,
    write_mode_opt,
)


class EndStatus(str, Enum):
    completed = "completed"
    failed = "failed"
    crashed = "crashed"
    canceled = "canceled"
    # 0106: uniform with the server enum (any client may set any status). The
    # honest use from a CLI is closing a run you registered but never attached
    # a live logger to -- e.g. a mirror that imported history for a run whose
    # real telemetry lives elsewhere.
    untracked = "untracked"


@run_app.command("end")
def run_end(
    run: str = run_ref(),
    status: EndStatus = typer.Option(EndStatus.completed, "--status"),
    flush_timeout: Optional[float] = typer.Option(
        None,
        "--flush-timeout",
        envvar="PROBE_FINISH_TIMEOUT_SEC",
        help="Bounded barrier (F3): keep draining this run's ops up to N "
        "seconds, then queue the close BEHIND whatever remains and exit 0 -- "
        "for jobs that must not hold hardware on a dead API. Dead letters "
        "and auth blocks still exit 2.",
    ),
    write_mode: Optional[bool] = write_mode_opt(),
) -> None:
    """Close a run.

    Synchronous mode is a RUN-SCOPED barrier (T3-A): this run's queued outbox
    ops are delivered first, and the run is not closed while any of them cannot
    be -- unrelated runs' stuck items never block it. Async mode enqueues the
    close as a journal op ORDERED BEHIND everything the run already queued, so
    the run only closes after its data lands; nothing blocks.

    THIS VERB DOES NOT FOLLOW THE ASYNC DEFAULT, and that is the point of it.
    `log`, `span add` and run-anchored `artifact add` queue unless told not to;
    `run end` blocks unless told to queue. It is the only command that verifies
    delivery -- drain this run's ops, refuse to close while any of them cannot
    land, exit 2 -- so a job that ends with it cannot exit 0 with data stuck on
    a disk that is about to be torn down. It also runs ONCE per run, so it was
    never on the hot path the default flip exists to speed up.

    f073194c is why this is spelled out: replacing set_status's strict=True with
    sync= let strict resolve to False for the CLI, and a typo'd run ref then
    journaled, printed success and exited 0 -- the exact opposite of a barrier.
    Making async the default here would reopen that from the other side.
    """
    if _resolve_write_mode(write_mode) is True:
        from ....foundation.durable.durable import now_iso

        with _async_client() as c:
            # set_status, not finish(): finish() flushes synchronously, which is
            # exactly what async mode must not do. Ordering is the barrier here.
            _async_run(c, run).set_status(status.value, ended_at=now_iso())
        _kick_drainer()
        print(f"queued end for {run} -> {status.value} (async)")
        # The run page is already live and shows the close landing, so the link
        # is worth handing back even though the status is still in flight.
        _print_link("run", run)
        return
    from ....sdk.delivery.outbox.drain.drain import drain
    from ....sdk.run.closing.drain import WAITING_PROMOTE_TIMEOUT

    journal = _journal()
    # Every queue: a PROBE_TOKEN or in-code writer's ops live in their own
    # credential queue (#2035), and the barrier is about the run's RESULT.
    queues = journal.namespaces()
    # This attempt's write epoch, when `run start` pinned one: a write an OLDER
    # attempt queued is refused by the server as superseded, so it never holds
    # this close (#2041 round 5, a rotated PROBE_TOKEN's leftovers).
    try:
        from probe.foundation.durable import run_lock

        epoch = run_lock.lease_write_epoch(run)
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        epoch = None

    def of_run(listing) -> list[dict]:
        return [op for queue in queues for _, op in listing(queue) if op.get("run_ref") == run]

    def queued_of_run() -> list[dict]:
        from ....sdk.delivery.ops.ops import _write_epoch_of

        def current(op: dict) -> bool:
            theirs = _write_epoch_of(op)
            return epoch is None or theirs is None or theirs >= epoch

        return [op for op in of_run(lambda q: q.pending()) if current(op)]

    # This run's uploads still waiting for their credential scan must become
    # ops BEFORE the barrier drain, or the drain would pass without them and
    # the close would land ahead of them. Local CPU; seconds.
    for queue in queues:
        if not queue.receipt_enabled:
            queue.promote_for_close(run, timeout=WAITING_PROMOTE_TIMEOUT)
    if flush_timeout is None:
        report = drain(journal, run_ref=run)
    else:
        deadline = time.monotonic() + max(flush_timeout, 0.0)
        while True:
            report = drain(journal, run_ref=run)
            left = queued_of_run()
            newly_dead = of_run(lambda q: q.failed())
            if not left or newly_dead or report.auth_blocked or time.monotonic() >= deadline:
                break
            time.sleep(min(0.25, max(deadline - time.monotonic(), 0.0)))
    dead = of_run(lambda q: q.failed())
    # Anything of this run's still queued after the drain (paused journal, a
    # skipped pass, any future skip condition) also blocks the close -- the
    # barrier promise is about the RESULT, not about which flag tripped.
    still_queued = queued_of_run()
    still_waiting = [
        item for queue in queues if not queue.receipt_enabled for item in queue.waiting_for_close(run)
    ]
    if still_waiting:
        typer.echo(
            f"run {run} NOT closed: {len(still_waiting)} queued upload(s) could not be "
            "prepared for delivery (credential scan). See `probe outbox status`, then "
            "re-run `probe run end`.",
            err=True,
        )
        raise typer.Exit(2)
    if flush_timeout is not None and still_queued and not dead and not report.auth_blocked:
        # Bounded barrier expired on retryable ops only: queue the close
        # BEHIND them (F3) and let the detached worker land everything. Dead
        # letters and auth blocks fall through to exit 2 -- deferring cannot
        # heal a permanent rejection, and a worker never runs auth-blocked.
        with _client() as c:
            _async_run(c, run)._queue_deferred_finish(status.value, None, len(still_queued))
        typer.echo(
            f"end queued for {run} -> {status.value} behind "
            f"{len(still_queued)} pending op(s); the background worker keeps "
            "retrying — `probe outbox watch` to follow",
            err=True,
        )
        _print_link("run", run)
        # The local writer is done even though the close rides the queue; a
        # held lease would only delay an upgrade (the cheap failure mode).
        try:
            from probe.foundation.durable import run_lock

            run_lock.clear_lease(run)
        except Exception:  # noqa: BLE001 -- an expiring lease is the backstop
            pass
        return
    if report.auth_blocked or report.stopped_transient or dead or still_queued:
        detail = "; ".join(
            report.errors[-3:]
            or [op.get("last_error") or "?" for op in dead[:3]]
            # Held, not failed: queued under a credential this shell does not
            # have (another job's PROBE_TOKEN, #2035) -- that job delivers them.
            or list(getattr(report, "held_reasons", None) or [])[:3]
            or [f"{len(still_queued)} still queued"]
        )
        typer.echo(
            f"run {run} NOT closed: its outbox items could not all be delivered "
            f"({detail}). Fix (see `probe outbox status`), retry dead letters "
            "with `probe outbox retry`, then re-run `probe run end`.",
            err=True,
        )
        raise typer.Exit(2)
    from ....foundation.durable.durable import now_iso as _now_iso

    with _client() as c:
        # set_status, not finish(): the run-scoped barrier above already
        # delivered THIS run's ops; finish() would foreground-drain the whole
        # machine-wide journal — other runs' queued gigabytes — inside this
        # command (red team: 'unrelated runs never block it' held for
        # correctness but not for time).
        # strict=True: `probe run end` without --async is the delivery barrier
        # (mcp/server.py documents it as "delivers that run's queued items or
        # fails loudly"). Without it the CLI client's fail_open=True resolves
        # strict to False, so a TransportError -- or a typo'd run ref's 404 --
        # would journal, print success and exit 0, which is the opposite of a
        # barrier. The lease clear and deferred update below both assume the
        # run really is terminal, so they must not be reached on a failure.
        _run_handle(c, run).set_status(status.value, ended_at=_now_iso(), strict=True)
    # The run is terminal, so release its claim on the box immediately rather
    # than waiting out the lease. Done AFTER set_status and outside the client
    # block: a lease that outlives its run only delays an upgrade, while one
    # dropped before the run actually closed would let an upgrade land on it.
    try:
        from probe.foundation.durable import run_lock

        run_lock.clear_lease(run)
    except Exception:  # noqa: BLE001 -- an expiring lease is the backstop
        pass
    # The run is terminal and its lease is gone: this is one of exactly two
    # moments where an update that `_version_notice` found and refused can be
    # applied. NOT the queued path above -- that one returns with a detached
    # outbox worker still delivering this run's close, and upgrading the tree
    # under it is the lazy-import hazard the whole design avoids.
    _apply_deferred_update()
    print(f"{run} -> {status.value}")
    # The run just became terminal: this is the moment its page is worth opening,
    # and the last one at which anything is printed about it.
    _print_link("run", run)
from probe.cli.commands.json_print import _print_link  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _async_run, _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.lifecycle.update_spawn import _apply_deferred_update  # noqa: E402 -- pieces need each other; the front door loads this one first
