"""The detached outbox drainer: wake on enqueue, drain until empty, exit.

Model (eng review 2026-07-29, 3A): the FIRST enqueue forks one detached worker; later
enqueues see the live flock lease and skip, so a loop queueing hundreds of writes forks once
per idle period, not per write. The worker loops with capped backoff until the journal is
empty, then exits: no daemon to install or forget.

Hard stops, so this never becomes the tap's zombie-uploader pitfall:
  * 401/403 -> the drain reports auth-blocked, ops stay queued untouched, and the worker
    EXITS (T2-A); it never retries with rejected credentials. EXCEPT a workspace-write
    refusal (403 `workspace_write_denied`), which is per-DESTINATION, not per-credential:
    that op dead-letters and the queue keeps flowing (`errors.WorkspaceLockedError` says why
    parking there is wrong). The suppression is a COOLDOWN, not a permanent stop: one
    re-probe every `_AUTH_RETRY_COOLDOWN_SECONDS`, so a rotated credential resumes on its
    own instead of needing `probe outbox retry`. One attempt per five minutes is not a
    zombie uploader; forever-silence with a growing queue was worse.
  * `probe outbox pause` -> exits at the next loop turn. The outbox's OWN switch, not the
    capture-consent killswitch.

A worker that dies (crash, reboot) is re-kicked by the next probe command of any kind;
`probe run end` remains the synchronous, run-scoped barrier.

When a Probe service runs on the machine the fork goes to it (plan Q5, `service_handoff`): it
starts this same module on the kicking process's interpreter as its own child; the lease, exit
guard and every hard stop are unchanged. Credential queues, processes holding a credential in
their environment, Windows and no service all fork as before.

Lives in the SDK (parity F1, docs/2026-08-04-outbox-miles-parity.md) so CLI commands and
``Client(async_writes=True)`` writers kick the same worker; ``probe.cli.outbox_worker`` stays
as a runnable shim because workers spawned by older releases exec that module path.
"""

from __future__ import annotations

import os
import sys
import time
from probe.foundation.compat.compat import StrEnum

from ...._shared import oscompat
from ....foundation.durable import durable
from probe.sdk.delivery.outbox.drainers.detached import _own_credential_queue, maybe_spawn
from probe.sdk.delivery.outbox.lease import _asked_to_stop, _drop_caps, _lease_path, _stop_path, _write_caps
from probe.sdk.delivery.outbox.linger import LingerEnd, _linger, _work_arrived
from probe.sdk.delivery.outbox.rescuer import rescue


class OutboxOutcome(StrEnum):
    """Why a drain episode ended — the worker's exit codes, given names.

    Lives here rather than in `cli.telemetry` (where the other event
    vocabularies sit) because the worker is the only producer, and the SDK must
    not import the CLI to name its own states. `emit_outbox_drained` takes it
    as a plain str, so there is exactly one definition either way.

    DRAINED is the only member that means the queue is empty. The other three
    all mean "ops are still queued", and they stay apart because they need
    different fixes: STALLED is the server or the network and heals itself,
    AUTH_BLOCKED needs a credential, PAUSED is someone's deliberate switch.
    Folding them into one "failed" would bury the state a human must act on
    behind the two that resolve on their own.
    """

    DRAINED = "drained"  # exit 0
    AUTH_BLOCKED = "auth_blocked"  # exit 3
    PAUSED = "paused"  # exit 4
    #: Not an exit code: the loop does not return while it is retrying, so this
    #: is reported from INSIDE the loop, once, when backoff reaches its cap.
    STALLED = "stalled"
    #: exit 0 with ops still queued: a newer producer asked for a worker that
    #: knows its op kinds (plan 1.11); its next kick spawns one.
    REPLACED = "replaced"


#: The one backoff shape for every durable retry in this SDK (a drain, an agent turn, a
#: backfill unit wait alike). Module names: this file reads them in several places.
_BACKOFF_START_SECONDS, _BACKOFF_CAP_SECONDS = durable.RETRY_BACKOFF
#: Between two looks at an upload still in the waiting room, or at ops held
#: back behind one.
_EXIT_GRACE_SECONDS = 1.5
#: How many looks, `_EXIT_GRACE_SECONDS` apart (~30 s in all), a worker takes at uploads in
#: the waiting room, or ops held behind one, before exiting and leaving them to the next
#: promoter.
_WAITING_PASSES = 20


def _promote_only(journal) -> None:
    """Promote waiting uploads under the promote lease, then return."""
    from ..journal.item_locks import _try_lock

    try:
        with _try_lock(journal.promote_lease) as held:
            if held:  # else another promoter is at it
                journal.promote_waiting()
    except OSError:
        return


def _pinned_base_url(journal, limit: int = 20) -> str | None:
    """The single base_url every queued op targets, or None if that is not provable. None
    (which disables the report) when the queue is empty, an op carries no pin, or two ops
    disagree: all mean "cannot prove which backend", and the egress contract makes that a
    no-send, not a guess. Bounded at `limit` ops: this runs at worker start, on the path a
    training loop kicks."""
    try:
        seen: set[str] = set()
        for _path, op in journal.pending()[:limit]:
            pinned = ((op or {}).get("context") or {}).get("base_url")
            if not pinned:
                return None
            seen.add(str(pinned).rstrip("/"))
            if len(seen) > 1:
                return None
        return next(iter(seen)) if seen else None
    except Exception:  # noqa: BLE001 -- an unreadable journal proves nothing
        return None


#: The pause between passes that delivered while some run is backing off.
_LANE_REPASS_SECONDS = 0.5

#: How often a worker whose remaining ops all belong to runs backing off looks for ops from
#: OTHER runs (plan 1.6): lists the queue's names, parses only unseen files.
_LANE_LOOK_SECONDS = 2.0


def _queued_names(journal) -> set:
    """Every queued op file name, per namespace. Names only."""
    names: set = set()
    for queue in journal.own_namespaces():
        try:
            names.update((str(queue.dir), n) for n in os.listdir(queue.ops_dir))
        except OSError:
            continue
    return names


def _wake_stamp(journal) -> float:
    """When `Journal.clear_auth_block` (a sign-in, `probe outbox
    resume`) last asked this queue's worker to look again, or 0."""
    try:
        return (journal.dir / ".wake").stat().st_mtime
    except OSError:
        return 0.0


def _sleep_until_new_work(journal, seen: set, lanes, seconds: float) -> None:
    """Sleep up to ``seconds``, waking early when an op of a run NOT backing off is queued
    (not in ``seen``, the names before the last pass) or when a sign-in asks
    (`_wake_stamp`: held writes may go now)."""
    import json

    from ..ops.ops import _lane_of

    deadline = time.monotonic() + seconds
    woken_at = _wake_stamp(journal)
    while True:
        left = deadline - time.monotonic()
        if left <= 0:
            return
        time.sleep(min(left, _LANE_LOOK_SECONDS))
        if journal.paused or _stop_path(journal).exists():
            return
        if _wake_stamp(journal) != woken_at:
            return
        skip = lanes.skip()
        for queue in journal.own_namespaces():
            try:
                names = os.listdir(queue.ops_dir)
            except OSError:
                continue
            for name in names:
                key = (str(queue.dir), name)
                if not name.endswith(".json") or key in seen:
                    continue
                seen.add(key)
                try:
                    op = json.loads((queue.ops_dir / name).read_text())
                except (OSError, ValueError):
                    return  # unreadable or gone: a pass will sort it out
                # By LANE, as the backoff is kept: a multipart upload waiting on the server's
                # verifier backs off in its own lane (plan (g)); a new op of its run must
                # still wake the loop.
                if not isinstance(op, dict) or _lane_of(op) not in skip:
                    return


def run(directory: str | None = None) -> int:
    """The worker loop. Exit codes: 0 empty (or asked to stop by a newer
    producer, plan 1.11), 3 auth-blocked, 4 paused."""
    from ..journal.journal import Journal

    journal = Journal(directory)
    journal._ensure()
    own = _own_credential_queue(journal)
    if own is not None:
        # The root's worker leaves credential queues to their own workers; this environment's
        # is one it can serve, beside the root (#2041 round 3).
        try:
            maybe_spawn(str(own))
        except Exception:  # noqa: BLE001 -- best-effort, like every kick
            pass
    lease = open(_lease_path(journal), "a+")
    try:
        oscompat.flock(lease.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    except BlockingIOError:
        lease.close()
        # Another worker owns delivery. Promote what waits for its credential scan (the owner
        # may be an older release that cannot) and leave delivery to it.
        _promote_only(journal)
        return 0
    _write_caps(journal)
    try:
        return _run_leased(journal)
    finally:
        _drop_caps(journal)


def _run_leased(journal) -> int:
    """`run`, while holding the lease (its handle stays open in `run`)."""
    from .. import journal as journal_module
    from ... import redaction
    from ..journal.journal import Journal
    from .drain.lanes import LaneBackoff
    from .drain.drain import drain

    # The scrub cache, as in the training process that spawned this worker. The drain
    # re-scrubs every op it sends; a fresh worker with the cache off rescanned each point's
    # constant keys and values ("key", "kind", "loss", ...): 180k scans, 7.1 s CPU for 2,002
    # coalesced one-step writes, waited out by `finish()` behind the drain lock (0.9 s with
    # it). Off in multi-tenant processes (redaction.py); this drains one OS user's outbox.
    redaction.enable_scrub_cache()

    # The backend this journal's ops target, resolved ONCE before the first drain pass while
    # the ops still exist. The worker delivers each op to the base_url pinned ON THAT OP
    # (journal.drain reads `context.base_url`), so gating the report on ambient config would
    # let a worker draining to a self-host endpoint report to the vendor. None disables the
    # report: outbox_context fails closed on an unknown backend.
    _gate_base_url = _pinned_base_url(journal)
    if not journal.receipt_enabled and journal.dir.parent.name != journal_module.CREDENTIAL_NAMESPACE:
        try:  # the root's worker tidies away idle credential queues (#2041 round 3)
            relocated = journal_module.DiscardCounts()
            journal_module.prune_credential_queues(journal.dir, counts=relocated)
            from .... import analytics as _telemetry

            _telemetry.emit_outbox_discarded(relocated, reason=_telemetry.DiscardReason.RELOCATED)
        except Exception:  # noqa: BLE001 -- housekeeping never stops delivery
            pass
    # Every wait comes from the ONE backoff helper (plan 0.6), restarted after
    # any pass that made progress.
    delays = durable.backoff_delays(None)
    # Per-run waits (plan 1.6): a run whose head op keeps failing backs off on
    # its own while every other run on the machine keeps delivering.
    lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
    woken_at = _wake_stamp(journal)
    started = time.monotonic()
    delivered = dead_lettered = passes = waiting_passes = 0
    #: The server's answer per dead letter, keyed as `sdk.delivery.summary` keys it, and how
    #: many were "run not found": a write naming no run is the sender's mistake, and the
    #: loss alert must tell it from ours.
    dead_lettered_by_status: dict[str, int] = {}
    dead_lettered_no_such_run = 0
    remaining = 0
    stalled_reported = False

    def _report(outcome: str) -> None:
        """Tell the fleet how this episode ended. Never raises or blocks the exit path:
        telemetry is a bystander to delivery."""
        try:
            from probe import analytics as telemetry

            telemetry.emit_outbox_drained(
                base_url=_gate_base_url,
                outcome=outcome,
                delivered=delivered,
                dead_lettered=dead_lettered,
                dead_lettered_by_status=dead_lettered_by_status,
                dead_lettered_no_such_run=dead_lettered_no_such_run,
                remaining=remaining,
                passes=passes,
                duration_s=time.monotonic() - started,
            )
        except Exception:  # noqa: BLE001 -- a broken pipe must not strand the queue
            pass

    while True:
        if _asked_to_stop(journal):
            # A newer SDK needs a worker that knows an op kind this one does
            # not (plan 1.11). Exit between passes; its next kick spawns one.
            print("stop requested by a newer producer; exiting", flush=True)
            _report(OutboxOutcome.REPLACED)
            return 0
        if journal.paused:
            if passes == 0:
                # Exiting before any drain pass: the tally is still 0 and a `remaining`
                # breakdown would show every paused queue as EMPTY, inverting the state a
                # human acts on. Read the depth already on disk, not a zero never measured.
                remaining = (Journal.read_status(str(journal.dir), credential_queues=False) or {}).get("pending") or 0
            _report(OutboxOutcome.PAUSED)
            return 4
        # Waits on the per-pass drain lock: a concurrent foreground `probe outbox drain`
        # finishes, then this pass sees what remains.
        before = _queued_names(journal)
        if _wake_stamp(journal) != woken_at:
            # A sign-in since the last pass: runs held for a credential are tried now, not
            # when their backoff ends (#2041 round 5: 57 s, up to 300 s).
            woken_at = _wake_stamp(journal)
            lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
        report = drain(journal, skip_runs=lanes.skip(), credential_queues=False)
        lanes.record(report)
        passes += 1
        delivered += report.delivered
        dead_lettered += report.dead_lettered
        for record in report.dead_letter_records:
            code = str(record.get("status") or "none")
            dead_lettered_by_status[code] = dead_lettered_by_status.get(code, 0) + 1
            dead_lettered_no_such_run += bool(record.get("no_such_run"))
        remaining = report.remaining
        if report.auth_stopped:
            # A refusal of an unstamped op (an older release queued it) stops
            # the queue: nothing tells its credential apart from the rest.
            print(
                f"auth-blocked; {report.remaining} op(s) kept queued ({journal_module.now_iso()})",
                flush=True,
            )
            _report(OutboxOutcome.AUTH_BLOCKED)
            return 3
        if report.remaining == 0:
            # Exit-race guard (red team): an enqueue in this final stretch saw our lease held
            # and skipped its spawn. Re-read status while holding the lease; anything new means
            # another pass, not an exit stranding the tail op until some future CLI command.
            fresh = Journal.read_status(str(journal.dir), credential_queues=False) or {}
            if _work_arrived(journal, fresh):
                continue
            if fresh.get("waiting") and waiting_passes < _WAITING_PASSES:
                # An upload mid-enqueue (item locked while it copies) or one not promotable
                # this pass. Look again shortly; never spin, never outlive a stuck item: the
                # next kick, barrier or CLI command promotes it.
                waiting_passes += 1
                time.sleep(_EXIT_GRACE_SECONDS)
                continue
            # Linger (_LINGER_SECONDS): a writer's LAST op can land after that re-read, and if
            # the writer dies there is no next command to re-kick (prod smoke 2026-08-06); a
            # live writer queues its next op in a second or two, which this worker takes
            # instead of exiting for the next kick to start another.
            ended = _linger(journal, waiting=waiting_passes < _WAITING_PASSES)
            if ended is None:
                _report(OutboxOutcome.DRAINED)
                return 0
            if ended == LingerEnd.WAITING:
                # An upload that arrived meanwhile, perhaps being scanned by a
                # promote-only child that will not deliver it.
                waiting_passes += 1
            continue
        if (
            (report.credential_held or report.credential_refused or report.close_held)
            and not (
                report.delivered
                or report.dead_lettered
                or report.held_back
                or report.stopped_transient
            )
            and lanes.next_wake() is None
        ):
            # Held ops of a RUN stall its lane; the branch below backs that run off while this
            # worker stays up for the rest (no fork per kick). What is left here names no run.
            # Everything left was queued with a credential this worker lacks (#2035; another
            # job's PROBE_TOKEN) or one the API refused (set aside until a new login or the
            # cooldown). Re-draining cannot change that: leave; the holder delivers them.
            print(
                f"{report.credential_held} op(s) wait for the credential that queued them "
                f"({journal_module.now_iso()})",
                flush=True,
            )
            _report(OutboxOutcome.STALLED)  # ops still queued; the next kick resumes
            return 0
        if report.held_back and not (report.delivered or report.dead_lettered):
            # Everything left waits on an upload another process is scanning. Look again
            # shortly, not in a tight loop, never outliving a stuck item. A pass that also
            # skipped runs backing off does not count: exiting would throw their backoff
            # away (review of #2051).
            if not lanes.skip():
                waiting_passes += 1
            if waiting_passes >= _WAITING_PASSES:
                _report(OutboxOutcome.STALLED)  # ops still queued; the next kick resumes
                return 0
            time.sleep(_EXIT_GRACE_SECONDS)
            continue
        if report.delivered or report.dead_lettered or report.in_progress:
            # Progress, a slice of a multipart upload's parts included (plan (g)): the worker
            # must not sleep to another lane's backoff or a 64-part upload crawls. Straight to
            # the next pass. Stalled runs wait out their own backoff via `skip_runs`; the rest
            # keep flowing, paced while some run backs off so a trickle of new writes cannot
            # make a pass per write (review of #2051).
            delays = durable.backoff_delays(None)
            if lanes.skip():
                time.sleep(_LANE_REPASS_SECONDS)
            continue
        wake = lanes.next_wake()
        if wake is not None and not report.unreachable:
            # Nothing moved, and what is left belongs to runs backing off:
            # sleep until the soonest of them may be tried again.
            backoff = min(wake, _BACKOFF_CAP_SECONDS)
            why = report.errors[-1] if report.errors else next(
                (stall.error for stall in report.stalled_runs.values()), "?"
            )
            print(
                f"{len(lanes.skip())} run(s) backing off, {report.remaining} left; "
                f"next try in {backoff:.0f}s: {why}",
                flush=True,
            )
            # ...unless another run queues something meanwhile: that must not
            # wait out a stalled run's backoff (up to five minutes).
            _sleep_until_new_work(journal, before, lanes, max(backoff, 0.05))
            if lanes.at_ceiling() and not stalled_reported:
                stalled_reported = True
                _report(OutboxOutcome.STALLED)
            continue
        if report.stopped_transient:
            # At least as long as the server asked (`Retry-After` on a 503 or
            # 429), never past the cap.
            backoff = durable.honor_retry_after(
                next(delays), report.retry_after, ceiling=_BACKOFF_CAP_SECONDS
            )
            print(
                f"transient failure, {report.remaining} left; retrying in "
                f"{backoff:.0f}s: {report.errors[-1] if report.errors else '?'}",
                flush=True,
            )
            time.sleep(backoff)
            # A worker retrying at the CAP has failed for minutes and may never exit, so it
            # would report nothing. Report once per worker, on the way INTO that state (each
            # capped pass would turn one wedged queue into a beacon).
            if backoff >= _BACKOFF_CAP_SECONDS and not stalled_reported:
                stalled_reported = True
                _report(OutboxOutcome.STALLED)
        else:
            # Progress was made (e.g. dead letters moved aside); reset backoff.
            delays = durable.backoff_delays(None)


def main(argv: list[str]) -> int:
    """The worker process: `python -m probe.sdk.outbox_worker [outbox]`, or `--rescue <outbox>`."""
    if len(argv) > 1 and argv[0] == "--rescue":
        return rescue(argv[1])
    return run(argv[0] if argv else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
