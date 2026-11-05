"""The outbox worker: started by the first enqueue (or the Probe service), it drains until the queue
is empty, then exits; run as `python -m probe.sdk.outbox_worker`, a path kept for good (DESIGN.md)."""

from __future__ import annotations

import os
import sys
import time
from probe.foundation.compat.compat import StrEnum

from ....foundation.os_backend import os_backend as oscompat
from ....foundation.durable import durable
from probe.sdk.delivery.outbox.drainers.detached import _own_credential_queue, maybe_spawn
from probe.sdk.delivery.outbox.lease import _asked_to_stop, _drop_caps, _lease_path, _stop_path, _write_caps
from probe.sdk.delivery.outbox.linger import LingerEnd, _linger, _work_arrived
from probe.sdk.delivery.outbox.rescuer import rescue
from probe.sdk.delivery.status_fields import StatusField


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


def _sleep_until_new_work(journal, seen: set, lanes, seconds: float, also_skip: frozenset = frozenset()) -> None:
    """Sleep up to ``seconds``, waking early when an op of a run NOT backing off (nor in
    ``also_skip``, lanes held after a stall) is queued (not in ``seen``, the names before the
    last pass) or when a sign-in asks (`_wake_stamp`: held writes may go now)."""
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
        skip = lanes.skip() | also_skip
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
    from ... import redaction
    from .drain.drain import SenderClients, drain

    # The scrub cache, as in the training process that spawned this worker. The drain
    # re-scrubs every op it sends; a fresh worker with the cache off rescanned each point's
    # constant keys and values ("key", "kind", "loss", ...): 180k scans, 7.1 s CPU for 2,002
    # coalesced one-step writes, waited out by `finish()` behind the drain lock (0.9 s with
    # it). Off in multi-tenant processes (redaction.py); this drains one OS user's outbox.
    redaction.enable_scrub_cache()
    # The clients every pass sends with, kept for this worker's life (I13): one TLS handshake
    # per credential, not one per pass.
    senders = SenderClients()
    episode = _WorkerEpisode(journal, senders=senders)
    try:
        return _run_episode(journal, episode, drain)
    finally:
        senders.close()
        # The last word: a waiter tells this clean exit from a worker that died.
        episode.tracker.publish(exiting=True)


def _run_episode(journal, episode: "_WorkerEpisode", drain) -> int:
    """The worker's passes until one of them ends the episode."""
    while True:
        ended = episode.end_before_pass()
        if ended is not None:
            return ended
        # Waits on the per-pass drain lock: a concurrent foreground `probe outbox drain`
        # finishes, then this pass sees what remains.
        before = _queued_names(journal)
        episode.restart_lanes_after_sign_in()
        episode.let_out_due_held()
        report = drain(
            journal,
            skip_runs=episode.lanes.skip(),
            credential_queues=False,
            window=episode.window,
            priority_runs=episode.waited_runs(),
            set_best_effort_aside=True,
            senders=episode.senders,
        )
        episode.count(report)
        released = episode.release_held_on_recovery(report)
        episode.handle_stalls(report)
        if released and not report.auth_stopped:
            continue  # what came back goes out in the next pass, not after a wait
        ended = episode.handle_report(report, before)
        if ended is not None:
            return ended


class _WorkerEpisode:
    """One worker's run of passes over a queue: its backoff, its tally, and what each pass's
    report makes it do next (another pass, a wait, or an exit code)."""

    def __init__(self, journal, *, senders=None) -> None:
        from .. import journal as journal_module
        from .drain.lanes import LaneBackoff
        from .drain.window import CollectWindow

        self.journal = journal
        # The backend this journal's ops target, resolved ONCE before the first drain pass while
        # the ops still exist. The worker delivers each op to the base_url pinned ON THAT OP
        # (journal.drain reads `context.base_url`), so gating the report on ambient config would
        # let a worker draining to a self-host endpoint report to the vendor. None disables the
        # report: outbox_context fails closed on an unknown backend.
        self.gate_base_url = _pinned_base_url(journal)
        if not journal.receipt_enabled and journal.dir.parent.name != journal_module.CREDENTIAL_NAMESPACE:
            try:  # the root's worker tidies away idle credential queues (#2041 round 3)
                relocated = journal_module.DiscardCounts()
                journal_module.prune_credential_queues(journal.dir, counts=relocated)
                from .... import analytics as _telemetry

                _telemetry.emit_outbox_discarded(relocated, reason=_telemetry.DiscardReason.RELOCATED,
                                                 surface=_telemetry.get_worker_surface())
            except Exception:  # noqa: BLE001 -- housekeeping never stops delivery
                pass
        # Every wait comes from the ONE backoff helper (plan 0.6), restarted after
        # any pass that made progress.
        self.delays = durable.backoff_delays(None)
        # Per-run waits (plan 1.6): a run whose head op keeps failing backs off on
        # its own while every other run on the machine keeps delivering.
        self.lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
        # Each writer's collect window (plan T2), stamped on its ops as `send_after`.
        self.window = CollectWindow()
        #: The worker's `SenderClients` (I13); None: each pass builds and closes its own.
        self.senders = senders
        #: Servers (`held.get_server_key`) that failed a pass with nothing landing: the first
        #: write landing on one again lets its held writes out (I14). Seeded from what an earlier
        #: worker held, so a restart does not leave those writes to their hour.
        from .held import get_held_servers

        try:
            self.servers_down: set = get_held_servers(journal.dir)
        except OSError:
            self.servers_down = set()
        self.woken_at = _wake_stamp(journal)
        self.started = time.monotonic()
        self.delivered = self.dead_lettered = self.passes = self.waiting_passes = 0
        #: The server's answer per dead letter, keyed as `sdk.delivery.summary` keys it, and how
        #: many were "run not found": a write naming no run is the sender's mistake, and the
        #: loss alert must tell it from ours.
        self.dead_lettered_by_status: dict[str, int] = {}
        self.dead_lettered_no_such_run = 0
        self.remaining = 0
        self.stalled_reported = False
        from .progress import ProgressTracker

        # The per-run progress record a waiting `finish()` reads (R1), and the stall clock (R12).
        self.tracker = ProgressTracker(journal)
        self.priority: list[str] = []

    def send_report(self, outcome: str) -> None:
        """Tell the fleet how this episode ended. Never raises or blocks the exit path:
        telemetry is a bystander to delivery."""
        self.tracker.publish(force=True)
        try:
            from probe import analytics as telemetry

            telemetry.emit_outbox_drained(
                base_url=self.gate_base_url,
                surface=telemetry.get_worker_surface(),
                outcome=outcome,
                delivered=self.delivered,
                dead_lettered=self.dead_lettered,
                dead_lettered_by_status=self.dead_lettered_by_status,
                dead_lettered_no_such_run=self.dead_lettered_no_such_run,
                remaining=self.remaining,
                passes=self.passes,
                duration_s=time.monotonic() - self.started,
            )
        except Exception:  # noqa: BLE001 -- a broken pipe must not strand the queue
            pass

    def end_before_pass(self) -> int | None:
        """The exit code when a newer producer asked this worker to stop or the outbox is paused."""
        from ..journal.journal import Journal

        journal = self.journal
        if _asked_to_stop(journal):
            # A newer SDK needs a worker that knows an op kind this one does
            # not (plan 1.11). Exit between passes; its next kick spawns one.
            print("stop requested by a newer producer; exiting", flush=True)
            self.send_report(OutboxOutcome.REPLACED)
            return 0
        if journal.paused:
            if self.passes == 0:
                # Exiting before any drain pass: the tally is still 0 and a `remaining`
                # breakdown would show every paused queue as EMPTY, inverting the state a
                # human acts on. Read the depth already on disk, not a zero never measured.
                fresh = Journal.read_status(str(journal.dir), credential_queues=False) or {}
                self.remaining = fresh.get(StatusField.PENDING) or 0
            self.send_report(OutboxOutcome.PAUSED)
            return 4
        return None

    def restart_lanes_after_sign_in(self) -> None:
        """A sign-in since the last pass: runs held for a credential are tried now, not
        when their backoff ends (#2041 round 5: 57 s, up to 300 s)."""
        if _wake_stamp(self.journal) != self.woken_at:
            self.woken_at = _wake_stamp(self.journal)
            self.lanes.forget_all()

    def waited_runs(self) -> list[str]:
        """The runs a `finish()` waits on (R2): their writes go first this pass."""
        from .waiter import waited_runs

        try:
            self.priority = waited_runs(self.journal.outbox_root)
        except Exception:  # noqa: BLE001 -- an unreadable marker only loses the priority
            self.priority = []
        return self.priority

    def let_out_due_held(self) -> None:
        """Held writes whose hour is up go back in line (R9). A listing when none is held."""
        from .held import release_held

        try:
            release_held(self.journal.dir)
        except OSError:
            pass

    def release_held_on_recovery(self, report) -> int:
        """Held writes of a server that answers again go back in line now, not at their hour
        (I14): a 503 storm's set-aside writes land with the first write after it. A server counts
        as back only after a pass it failed with nothing landing, and a let-out write failing again
        does not count as failing (`DrainReport.failing_servers`), so a write held while its
        server answered waits its hour (`HELD_RETRY_SECONDS`, the backstop). Returns how many
        writes and lanes came back."""
        from .held import release_held

        answered = report.answered_servers
        recovered = self.servers_down & answered
        self.servers_down = (self.servers_down - answered) | (report.failing_servers - answered)
        if not recovered:
            return 0
        try:
            return release_held(self.journal.dir, due_only=False, servers=recovered)
        except OSError:
            return 0

    def handle_stalls(self, report) -> None:
        """After a pass: set aside what stalled (R12) and tell the server what it must hear (D5).
        Never raises: the next pass delivers either way."""
        from .stall import report_new_stalls, set_aside_stalled

        try:
            report_new_stalls(self.tracker, report)
            set_aside_stalled(self.journal, self.tracker, self.lanes)
        except Exception:  # noqa: BLE001 -- bookkeeping never stops delivery
            pass
        self.tracker.publish()

    def count(self, report) -> None:
        """Add one pass's report to the episode's tally."""
        self.tracker.record(report, priority=self.priority)
        self.lanes.record(report)
        self.passes += 1
        self.delivered += report.delivered
        self.dead_lettered += report.dead_lettered
        for record in report.dead_letter_records:
            code = str(record.get("status") or "none")
            self.dead_lettered_by_status[code] = self.dead_lettered_by_status.get(code, 0) + 1
            self.dead_lettered_no_such_run += bool(record.get("no_such_run"))
        self.remaining = report.remaining

    def handle_report(self, report, before: set) -> int | None:
        """What a pass's report makes the worker do: an exit code, or None for another pass
        (after any wait it takes here)."""
        from .. import journal as journal_module

        if report.auth_stopped:
            # A refusal of an unstamped op (an older release queued it) stops
            # the queue: nothing tells its credential apart from the rest.
            print(
                f"auth-blocked; {report.remaining} op(s) kept queued ({journal_module.now_iso()})",
                flush=True,
            )
            self.send_report(OutboxOutcome.AUTH_BLOCKED)
            return 3
        if report.remaining == 0:
            return self.handle_empty_queue()
        if self.is_waiting_for_windows(report):
            self.wait_for_windows(report, before)
            return None
        if self.is_held_for_credentials(report):
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
            self.send_report(OutboxOutcome.STALLED)  # ops still queued; the next kick resumes
            return 0
        if report.held_back and not (report.delivered or report.dead_lettered):
            return self.wait_for_held_back()
        if self.is_waiting_for_held_lanes(report):
            self.wait_for_held(before)
            return None
        if report.delivered or report.dead_lettered or report.in_progress:
            # Progress, a slice of a multipart upload's parts included (plan (g)): the worker
            # must not sleep to another lane's backoff or a 64-part upload crawls. Straight to
            # the next pass. Stalled runs wait out their own backoff via `skip_runs`; the rest
            # keep flowing, paced while some run backs off so a trickle of new writes cannot
            # make a pass per write (review of #2051).
            self.delays = durable.backoff_delays(None)
            if self.lanes.skip():
                time.sleep(_LANE_REPASS_SECONDS)
            return None
        wake = self.lanes.next_wake()
        if wake is not None and not report.unreachable:
            self.wait_for_backed_off_runs(report, before, wake)
            return None
        if report.stopped_transient:
            self.wait_out_transient(report)
        else:
            # Progress was made (e.g. dead letters moved aside); reset backoff.
            self.delays = durable.backoff_delays(None)
        return None

    def handle_empty_queue(self) -> int | None:
        """The queue looked empty: exit once nothing new arrived and lingering found nothing."""
        from ..journal.journal import Journal

        journal = self.journal
        # Exit-race guard (red team): an enqueue in this final stretch saw our lease held
        # and skipped its spawn. Re-read status while holding the lease; anything new means
        # another pass, not an exit stranding the tail op until some future CLI command.
        fresh = Journal.read_status(str(journal.dir), credential_queues=False) or {}
        if _work_arrived(journal, fresh):
            return None
        if fresh.get(StatusField.WAITING) and self.waiting_passes < _WAITING_PASSES:
            # An upload mid-enqueue (item locked while it copies) or one not promotable
            # this pass. Look again shortly; never spin, never outlive a stuck item: the
            # next kick, barrier or CLI command promotes it.
            self.waiting_passes += 1
            time.sleep(_EXIT_GRACE_SECONDS)
            return None
        # Linger (_LINGER_SECONDS): a writer's LAST op can land after that re-read, and if
        # the writer dies there is no next command to re-kick (prod smoke 2026-08-06); a
        # live writer queues its next op in a second or two, which this worker takes
        # instead of exiting for the next kick to start another.
        from .held import has_held

        if has_held(journal.dir):
            # Held writes are let out by a worker at their hour (R9): stay for them, never exit
            # leaving them to a producer that may never come back.
            self.wait_for_held(_queued_names(journal))
            return None
        self.tracker.publish(force=True)  # nothing left: a waiter reads it now, not after the linger
        ended = _linger(journal, waiting=self.waiting_passes < _WAITING_PASSES)
        if ended is None:
            self.send_report(OutboxOutcome.DRAINED)
            return 0
        if ended == LingerEnd.WAITING:
            # An upload that arrived meanwhile, perhaps being scanned by a
            # promote-only child that will not deliver it.
            self.waiting_passes += 1
        return None

    def is_waiting_for_held_lanes(self, report) -> bool:
        """Everything that could go went; the rest is in lanes held after a stall."""
        return bool(
            report.lane_held
            and not (
                report.delivered
                or report.dead_lettered
                or report.in_progress
                or report.stopped_transient
                or report.deferred
            )
            and self.lanes.next_wake() is None
        )

    def wait_for_held(self, before: set) -> None:
        """Sleep until the soonest held write or lane is let out, waking for new work of a run
        that is not held (a stall window, if one runs, cuts it short too)."""
        from .held import held_lanes, next_release_in

        self.tracker.publish(force=True)  # a waiter sees where things stand while this sleeps
        left = next_release_in(self.journal.dir)
        if left is None:
            return
        stall = self.tracker.seconds_to_next_stall()
        seconds = max(0.05, min(left, stall) if stall is not None else left)
        _sleep_until_new_work(
            self.journal, before, self.lanes, seconds, also_skip=frozenset(held_lanes(self.journal.dir))
        )

    @staticmethod
    def is_waiting_for_windows(report) -> bool:
        """Everything that may go now went; the rest waits for its run's collect window (plan T2)."""
        return bool(report.deferred and not (
            report.delivered
            or report.dead_lettered
            or report.in_progress
            or report.unreachable
            or (report.stopped_transient and not report.stalled_runs)
        ))

    def wait_for_windows(self, report, before: set) -> None:
        """Sleep until the soonest collect window or run backoff ends, waking for a write that must
        go now (another writer's at window 0, a close, an upload, a full POST), never for each
        `log()`: a pass per write is the cost the window removes."""
        journal = self.journal
        self.tracker.publish(force=True)  # a waiter sees where things stand while this sleeps
        soonest = min(
            w
            for w in (report.send_in, self.lanes.next_wake(), self.tracker.seconds_to_next_stall())
            if w is not None
        )
        woke_from = self.woken_at
        self.window.wait(
            journal,
            seconds=max(soonest, 0.05),
            seen=before,
            skip=self.lanes.skip(),
            loads=report.deferred_loads,
            asked=lambda: journal.paused
            or _stop_path(journal).exists()
            or _wake_stamp(journal) != woke_from,
        )

    def is_held_for_credentials(self, report) -> bool:
        """Everything left waits for a credential this worker lacks or the API refused."""
        return bool(
            (report.credential_held or report.credential_refused or report.close_held)
            and not (
                report.delivered
                or report.dead_lettered
                or report.held_back
                or report.stopped_transient
            )
            and self.lanes.next_wake() is None
        )

    def wait_for_held_back(self) -> int | None:
        """Everything left waits on an upload another process is scanning. Look again
        shortly, not in a tight loop, never outliving a stuck item. A pass that also
        skipped runs backing off does not count: exiting would throw their backoff
        away (review of #2051)."""
        if not self.lanes.skip():
            self.waiting_passes += 1
        if self.waiting_passes >= _WAITING_PASSES:
            self.send_report(OutboxOutcome.STALLED)  # ops still queued; the next kick resumes
            return 0
        time.sleep(_EXIT_GRACE_SECONDS)
        return None

    def wait_for_backed_off_runs(self, report, before: set, wake: float) -> None:
        """Nothing moved, and what is left belongs to runs backing off:
        sleep until the soonest of them may be tried again."""
        self.tracker.publish(force=True)  # a waiter sees where things stand while this sleeps
        backoff = min(wake, _BACKOFF_CAP_SECONDS, self.tracker.seconds_to_next_stall() or wake)
        why = report.errors[-1] if report.errors else next(
            (stall.error for stall in report.stalled_runs.values()), "?"
        )
        print(
            f"{len(self.lanes.skip())} run(s) backing off, {report.remaining} left; "
            f"next try in {backoff:.0f}s: {why}",
            flush=True,
        )
        # ...unless another run queues something meanwhile: that must not
        # wait out a stalled run's backoff (up to five minutes).
        _sleep_until_new_work(self.journal, before, self.lanes, max(backoff, 0.05))
        if self.lanes.at_ceiling() and not self.stalled_reported:
            self.stalled_reported = True
            self.send_report(OutboxOutcome.STALLED)

    def wait_out_transient(self, report) -> None:
        """At least as long as the server asked (`Retry-After` on a 503 or
        429), never past the cap."""
        self.tracker.publish(force=True)  # a waiter sees where things stand while this sleeps
        step = next(self.delays)
        # Full jitter (I14): every worker of a fleet that failed in one second must not retry in it.
        backoff = durable.honor_retry_after(
            durable.pick_jittered_wait(step), report.retry_after, ceiling=_BACKOFF_CAP_SECONDS
        )
        print(
            f"transient failure, {report.remaining} left; retrying in "
            f"{backoff:.0f}s: {report.errors[-1] if report.errors else '?'}",
            flush=True,
        )
        time.sleep(backoff)
        # A worker retrying at the CAP has failed for minutes and may never exit, so it
        # would report nothing. Report once per worker, on the way INTO that state (each
        # capped pass would turn one wedged queue into a beacon). The ladder's step, not the
        # jittered wait, says it got there.
        if step >= _BACKOFF_CAP_SECONDS and not self.stalled_reported:
            self.stalled_reported = True
            self.send_report(OutboxOutcome.STALLED)


def main(argv: list[str]) -> int:
    """The worker process: `python -m probe.sdk.outbox_worker [outbox]`, or `--rescue <outbox>`."""
    if len(argv) > 1 and argv[0] == "--rescue":
        return rescue(argv[1])
    return run(argv[0] if argv else None)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
