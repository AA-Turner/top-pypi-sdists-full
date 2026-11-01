"""Drain: one drain pass over a queue and its namespaces, FIFO within each run, settling each op."""

from __future__ import annotations
import json
import os
import time
from contextlib import nullcontext
from pathlib import Path
from typing import Any, Callable

from ....._shared import oscompat
from .... import errors
from .....foundation.durable.durable import (
    file_lock,
    fsync_directory,
    now_iso,
    write_text_atomic)
from ....session_marker import WIZARD_HINT
from ....secret_gate import CredentialBlocked
_DEAD_LETTER_ERROR_CHARS = 300

#: ...AND at least this many attempts. Time alone would dead-letter a laptop's whole queue on
#: the first blip after a day asleep; attempts alone let the poll rate decide. Both must be
#: spent. Cost, until per-run lanes (plan 1.6) stop one run's head holding the others: a
#: poison op the server always answers 5xx blocks the machine's FIFO for a day.
MIN_TRANSIENT_ATTEMPTS = 50


#: Ops looked at per parallel window, as a multiple of the worker count. Bounded because a
#: window is read into memory and the serial loop behind it decides everything: a larger
#: window buys nothing once the link is saturated and costs re-work when the pass stops early.
UPLOAD_WINDOW_FACTOR = 4
#: Ops a window may look past to fill itself, as a multiple of its size. A run queue of
#: metric points holds no upload to find; scanning the rest at every window cost a drain of
#: 6,000 such ops 565,504 op reads.
UPLOAD_WINDOW_SCAN_FACTOR = 4
#: How soon a pass looks again at a run another drain is sending (holds its lock): a ceiling
#: on that run's backoff, not a failure.
_RUN_BUSY_RECHECK_SECONDS = 5.0


def drain(
    journal: Journal,
    *,
    run_ref: str | None = None,
    client_factory: Callable[[dict | None], Any] | None = None,
    wait_for_lock: bool = True,
    lock_timeout: float | None = None,
    promote_timeout: float | None = None,
    on_error: Callable[[Exception], None] | None = None,
    on_delivered: Callable[[str | None], None] | None = None,
    skip_runs: "set | frozenset | None" = None,
    credential_queues: bool = True,
    long_ops: bool = True,
    only_ops: "set | frozenset | None" = None,
    _include_receipts: bool = True,
) -> DrainReport:
    """Deliver queued ops, FIFO WITHIN each run. Foreground and background drains share this;
    the drainer loop wraps it in backoff.

    Per-run lanes (plan 1.6): the queue is split by ``run_ref`` and lanes are visited
    round-robin, one op per turn, so a deep backlog no longer delays other runs. A transient
    failure (503, timeout) parks that op in place and stops only ITS run for the pass
    (`DrainReport.stalled_runs`); one run's poison op used to hold the whole machine's queue
    for the 24 h to dead-letter. Order across runs was never promised; a run's own ops, its
    close last, go in queue order. An auth block, a connect failure (server unreachable for
    everyone) and the caller's deadline still end the pass. ``skip_runs`` names lanes the
    caller is backing off: not attempted this pass. Ops naming no run share one lane (None).

    ``lock_timeout`` bounds the wait for the drain lock (another drainer, e.g. the detached
    worker, may be mid-pass): polled, never blocked on; a pass that cannot take it in time
    attempts nothing and reports ``lock_busy``. None keeps ``wait_for_lock``'s behaviour.
    `Run.finish()` passes what is left of its deadline, so a worker's long pass cannot hold a
    close past it (plan 0.6). ``promote_timeout`` likewise bounds promotion of uploads still
    waiting for their credential scan (None: no bound).

    ``run_ref`` scopes a barrier drain (T3-A): only that run's ops are attempted, the rest is
    left for the machine-wide drainer. A barrier never runs a multipart upload (plan (g)), nor
    does a pass with ``long_ops=False`` (a closing process's last pass must not spend a slice
    of seconds on one). ``only_ops`` (op ids) attempts those ops only, multipart uploads
    included: a `finish()` seeing its own uploads through (`multipart.settle_for_close`).
    ``client_factory(context)`` is for tests; production resolves a client per pinned context,
    tokens fresh (5A).
    ``on_error`` may raise before an error changes the queued operation: an approved import
    retains its receipts and owns a longer network retry policy without treating unknown
    failures as temporary connection problems.
    ``on_delivered(correlation)`` runs after the receipt and queue removal are durable,
    including recovery after a receipt-before-removal crash. A best-effort observer; its
    failures cannot undo or interrupt delivery.
    """
    if _include_receipts and not journal.receipt_enabled:
        namespaces = journal.namespaces()
        if len(namespaces) > 1:
            combined = DrainReport()
            for queue in namespaces:
                if queue.dir.parent.parent.name == CREDENTIAL_NAMESPACE or (
                    queue.dir.parent.name == CREDENTIAL_NAMESPACE
                ):
                    if not credential_queues:
                        # The root's detached worker: each credential queue has its own,
                        # started by a writer holding that credential (#2041 round 3). This one
                        # could only hold their writes, and keep its lease doing it.
                        continue
                if queue.dir.parent.name == CREDENTIAL_NAMESPACE and _queue_is_empty(queue.dir):
                    # An idle credential queue: nothing to lock, scan or rewrite status for
                    # (#2041 round 3: hundreds of them made every pass slow).
                    continue
                part = drain(
                    queue,
                    run_ref=run_ref,
                    client_factory=client_factory,
                    wait_for_lock=wait_for_lock,
                    lock_timeout=lock_timeout,
                    promote_timeout=promote_timeout,
                    on_error=on_error,
                    on_delivered=on_delivered,
                    skip_runs=skip_runs,
                    long_ops=long_ops,
                    only_ops=only_ops,
                    _include_receipts=False,
                )
                combined.delivered += part.delivered
                combined.dead_lettered += part.dead_lettered
                combined.remaining += part.remaining
                if part.auth_blocked and not combined.auth_blocked:
                    combined.auth_status = part.auth_status
                    combined.auth_message = part.auth_message
                    combined.auth_context = part.auth_context
                combined.auth_blocked |= part.auth_blocked
                combined.queue_auth_stopped |= part.queue_auth_stopped
                combined.credential_refused += part.credential_refused
                combined.close_held += part.close_held
                combined.permanently_held += part.permanently_held
                combined.auth_refusals.extend(part.auth_refusals)
                combined.held_reasons.extend(
                    r for r in part.held_reasons if r not in combined.held_reasons
                )
                combined.stopped_transient |= part.stopped_transient
                combined.held_back += part.held_back
                combined.credential_held += part.credential_held
                combined.errors.extend(part.errors)
                combined.deadline_reached |= part.deadline_reached
                combined.lock_busy |= part.lock_busy
                combined.unreachable |= part.unreachable
                if part.queued_runs is not None:
                    combined.queued_runs = (combined.queued_runs or set()) | part.queued_runs
                combined.unknown_kinds += part.unknown_kinds
                combined.in_progress += part.in_progress
                combined.coalesced += part.coalesced
                combined.skipped += part.skipped
                combined.dead_letter_records.extend(part.dead_letter_records)
                combined.progressed_runs |= part.progressed_runs
                combined.busy_runs |= part.busy_runs
                combined.superseded.merge(part.superseded)
                for lane, stall in part.stalled_runs.items():
                    combined.stalled_runs.setdefault(lane, stall)
                if part.retry_after is not None:
                    combined.retry_after = max(combined.retry_after or 0.0, part.retry_after)
            return combined
    report = DrainReport()
    journal._ensure()
    if journal.receipt_enabled:
        journal._receipt_dirs()
    try:
        journal.sweep_stale_temps()
    except Exception:  # noqa: BLE001 -- hygiene is best-effort
        pass
    if journal.paused:
        report.remaining = journal._count_dir(journal.ops_dir)[0]
        return report
    if not journal.receipt_enabled:
        # Uploads queued before their credential scan become ops first: every new-version drain
        # (worker, barrier, `probe outbox drain`) is a promoter. An item another process holds
        # is left to it.
        try:
            # The lease says "someone is promoting", so a kick meanwhile forks no promote-only
            # worker; items have their own locks, so this promotes with or without the lease.
            with _try_lock(journal.promote_lease):
                journal.promote_waiting(run_ref=run_ref, timeout=promote_timeout)
        except Exception:  # noqa: BLE001 -- items stay waiting; the next pass retries
            pass

    Client = delivery_client()  # loaded here, not at import: enqueue paths must not import httpx

    clients: dict[tuple, Any] = {}
    constructed: list[Any] = []  # only clients WE built get closed

    # Credentials the API refused (#2041 review): fingerprint -> when. Earlier passes' come
    # from status.json, so a refused credential is re-tried once per cooldown, not per pass;
    # this pass's refusals apply to every later op of that credential, the writer's own too.
    cooling = _cooling_refusals(journal)
    refused_now: dict[str, str] = {}
    # Fingerprint -> adopted (`probe outbox adopt`), read once per pass.
    adoptions: dict[str, bool] = {}
    # Adopted fingerprint -> the fingerprint of the login its writes go out with this pass. A
    # refusal of THAT login is recorded under it too, so the banner names it and its cooldown
    # holds the adopted writes back as well.
    adopted_login: dict[str, str] = {}

    def is_adopted(fingerprint: str) -> bool:
        if fingerprint not in adoptions:
            adoptions[fingerprint] = adopted_account(fingerprint) is not None
        return adoptions[fingerprint]

    delivered_fps: set[str] = set()
    # One token is one account: what any of a token's writes recorded vouches for all of them
    # (#2041 re-review). Filled from the queue below.
    accounts: dict[str, tuple[str, str]] = {}
    learned: set[str] = set()

    def learn_account(op: dict) -> None:
        """After a stored-login write went out with ITS OWN token: remember which account that
        token is, once per token (`record_account`), so its other writes can follow a
        same-account re-login (a login saved by the setup wizard or an older CLI records none,
        #2041 round 3)."""
        stamp = (op.get("context") or {}).get("principal")
        if not isinstance(stamp, dict) or stamp.get("source") != CredentialSource.CONFIG:
            return
        fp = stamp.get("fingerprint")
        if not fp or op_credential(op)[1] or fp in learned or stamp_identity(stamp) or fp in accounts:
            return
        learned.add(fp)
        try:
            if recorded_account(fp) is not None:
                return
            sender = client_for(op.get("context"))
            settings = getattr(sender, "settings", None)
            if settings is None or credential_fingerprint(settings.token, None) != fp:
                return  # went out with a later login (the account was known): nothing to learn
            record_account(
                fp,
                _identity_of(settings, getattr(sender, "transport", None)),
                login_of=_login_base_of(op.get("context"), settings.base_url),
            )
        except Exception:  # noqa: BLE001 -- evidence for later, never a delivery step
            return

    def client_for(context: dict | None, ingest: bool = False, op: dict | None = None):
        stamp = (context or {}).get("principal")
        stamped_fp = None
        if isinstance(stamp, dict):
            stamped_fp = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
        key = ((context or {}).get("name"), (context or {}).get("base_url"), stamped_fp, ingest)
        # What a client_factory is told: the route, so it matches the right key.
        asked = {**context, "route": "ingest"} if (ingest and isinstance(context, dict)) else context
        refused_at = refused_now.get(stamped_fp) if stamped_fp else None
        if (
            refused_at is None
            and stamped_fp in cooling
            and (ingest or not is_adopted(stamped_fp))
            and (client_factory is None or client_factory(asked) is None)
        ):
            # Refused in an earlier pass. The writer itself (client_factory) may still try: a
            # re-login it picked up is how its writes recover. So may an adopted credential's
            # writes, which go out with the stored login now: the refusal on record is of the
            # dead token, which a job still running with it re-records every cooldown.
            refused_at = cooling[stamped_fp]
        if refused_at is not None:
            # Set aside with every other write of that credential: no re-asking the API, no
            # holding anyone else's writes up.
            raise CredentialNotHere(
                f"its credential was refused by the API at {refused_at}; it waits for a "
                f"new sign-in ({WIZARD_HINT}), or for the process that holds that credential"
            )
        if (
            op is not None
            and stamped_fp
            and not ingest
            and is_adopted(stamped_fp)
            and (client_factory is None or client_factory(asked) is None)
        ):
            refused_here = adopted_route_refuses(op)
            if refused_here is not None:
                raise AdoptedRouteRefused(
                    f"queued with a revoked credential that was adopted, but {refused_here} "
                    "(`probe outbox retry` requeues it if that credential comes back)",
                    status=422,
                )
        if isinstance(clients.get(key), CredentialNotHere):
            # A fresh instance: re-raising one object grows its traceback per op.
            raise CredentialNotHere(str(clients[key]), permanent=clients[key].permanent)
        if key not in clients:
            supplied = client_factory(asked) if client_factory is not None else None
            if supplied is not None:
                clients[key] = supplied
            else:
                try:
                    if stamped_fp and not ingest and is_adopted(stamped_fp):
                        # Before `_settings_for_op`, whose account check is the
                        # login's first request and may be what is refused.
                        login_fp = _stored_login_fingerprint(context)
                        if login_fp:
                            adopted_login[stamped_fp] = login_fp
                        login_refused = refused_now.get(login_fp or "") or cooling.get(
                            login_fp or ""
                        )
                        if login_refused:
                            raise CredentialNotHere(
                                f"adopted by the login stored here, which the API refused at "
                                f"{login_refused}; it waits for a new sign-in ({WIZARD_HINT})"
                            )
                    account = accounts.get((stamp or {}).get("fingerprint") or "")
                    settings = _settings_for_op(context, ingest=ingest, account=account)
                except CredentialNotHere as absent:
                    clients[key] = absent  # asked once per pass, not once per op
                    raise
                if not settings.token and not settings.ingest_token:
                    raise errors.AuthError(
                        f"no credentials for context {key[0] or '<default>'} ({WIZARD_HINT})"
                    )
                # async_writes=False because THIS is the drainer: an async client mints a
                # producer record (`sdk:{host}:{pid}:{uuid4}`) per construction, the detached
                # worker builds one per pass, and a long outage would litter producers/ with
                # thousands of single-use entries in the registry that makes capture loss
                # visible. NOT because replay would re-journal: replay never goes through
                # `Client.write`, it uses `transport.request` and `upload_fingerprinted`
                # directly; write mode does not govern the drain path.
                client = Client(settings=settings, async_writes=False)
                constructed.append(client)
                clients[key] = client
        return clients[key]

    def tally_delivered(op: dict) -> None:
        """Credit one landed op to the producer that enqueued it. Runs AFTER the op file is gone
        (see ``note_delivered``) and never fails a delivery: accounting is diagnostics, the
        write already happened."""
        producer_id = op.get("producer_id")
        if not producer_id:
            return
        try:
            journal.note_delivered(producer_id)
        except Exception:  # noqa: BLE001 -- accounting must never break the drain
            pass

    def notify_delivered(op: dict) -> None:
        if on_delivered is not None:
            try:
                on_delivered(op.get("correlation"))
            except Exception:  # noqa: BLE001 -- observers cannot fail a committed delivery
                pass

    lock_handle = journal.drain_lock.open("a+")
    # A run's close (its barrier, or the uploads it must see through) says it is waiting, so a
    # pass holding the lock gives it up at its next op (#3618).
    urgent = run_ref is not None or only_ops is not None
    if not _take_drain_lock(
        lock_handle,
        wait_for_lock=wait_for_lock,
        timeout=lock_timeout,
        want=journal.drain_want if urgent and not journal.receipt_enabled else None,
    ):
        lock_handle.close()
        report.remaining = journal._count_dir(journal.ops_dir)[0]
        report.lock_busy = True
        report.errors.append("another drain holds the lock")
        return report
    drain_hold = _DrainHold(journal, lock_handle, urgent=urgent)

    # Whether an upload LEFT the queue this pass (delivered or dead-lettered): only then can a
    # blob have lost its last reference. `gc_blobs` re-reads the whole queue under the append
    # lock; after a pass that merely TRIED an upload (head of the queue during an outage, every
    # pass) it blocked `log()` ~1 s per pass at 20k ops (review of #2038).
    settled_upload = False
    # Petname -> uuid, for this drain only. See _resolved_run_id.
    run_ids: dict[str, str] = {}
    # What the closing status recount may reuse instead of re-parsing under the append lock
    # (plan 1.9); filled by the one scan below.
    known: dict[str, tuple[int, str | None]] = {}
    held_note: str | None = None
    # Per run: queued-at of each blocking op in the outbox's OTHER queues. Read once, only
    # when this pass meets a run's close.
    elsewhere: dict | None = None

    def writes_elsewhere(run: str, before: str | None, epoch: Any = None) -> int:
        """How many blocking writes of ``run`` queued no later than ``before`` sit in the
        outbox's other queues. A write stamped with an OLDER write epoch than the close's is
        left out: the server refuses it as stale, so holding the close for it only delays the
        close (#2041 round 5: a takeover's close sat behind the dead attempt's writes)."""
        nonlocal elsewhere
        if elsewhere is None:
            elsewhere = {}
            for queue in journal.other_queues():
                for _other_path, other in Journal._read_dir(queue.ops_dir):
                    if isinstance(other, dict) and other.get("run_ref") and other.get("blocking", True):
                        elsewhere.setdefault(other["run_ref"], []).append(
                            (str(other.get("enqueued_at") or ""), _write_epoch_of(other))
                        )
                if not queue.receipt_enabled:
                    # Uploads still waiting for their credential scan count too: they become
                    # ops of that queue shortly (#2041 round 4).
                    for _position, _op_id, ref, readable, blocking in queue._waiting_items():
                        if readable and blocking and ref:
                            elsewhere.setdefault(ref, []).append(("", None))
        return sum(
            1
            for at, their_epoch in elsewhere.get(run, ())
            if (not before or at <= before)
            and not (epoch is not None and their_epoch is not None and their_epoch < epoch)
        )
    try:
        if journal.receipt_enabled:
            journal.recover_intents()
        # 2.3: a close a dead relaunch held aside goes back in the queue, so this pass delivers
        # it (a stat when nothing is held).
        try:
            restore_abandoned_holds(journal)
        except Exception:  # noqa: BLE001 -- a hold left in place is the old behaviour
            pass
        # Plan (g): multipart uploads live in a queue of their own (`<outbox>/multipart/ops/`)
        # that no earlier release reads, so an older worker holding this outbox never meets one.
        # Only a pass that may run them (not a run's barrier, not a closing exporter) reads it.
        multipart_queue: list = []
        if not journal.receipt_enabled and (only_ops is not None or (run_ref is None and long_ops)):
            try:
                _multipart = multipart_storage()

                # A staged copy nothing will read again (op finished or dead-lettered, a copy
                # cut short by a kill) goes first.
                _multipart.gc_staging(journal)
                multipart_queue = _multipart.pending(journal)
            except Exception:  # noqa: BLE001 -- multipart waits for the next pass
                multipart_queue = []
        # A run's ops queued after an upload still being scanned wait for it: its close must not
        # reach the server first (see `promote_waiting`). Read BEFORE the queue: an upload
        # promoted in between is then both "waiting" and queued, holding successors back one
        # pass; the other order would miss it in both and let its close go first.
        held_back = {} if journal.receipt_enabled else journal.waiting_positions()
        # ONE parse of the queue, outside the append lock (plan 1.9): this pass's work list,
        # quarantine list and the recount's cache.
        queued, corrupt = journal._scan_ops(stamps=drain_hold.stamps)
        known = op_meta(queued)
        report.queued_runs = {
            _lane_of(op) for _, op in [*queued, *multipart_queue] if isinstance(op, dict)
        }
        # Each run's ops in queue order, for coalescing (plan 1.2): a metric op rides in one
        # POST with the ones queued right behind it in its run.
        lanes: dict[Any, list[tuple[Path, dict]]] = {}
        for item in queued:
            lanes.setdefault(_lane_of(item[1]), []).append(item)
        lane_index = {item[0]: n for ops in lanes.values() for n, item in enumerate(ops)}
        consumed: set[Path] = set()
        if run_ref is None:
            queued = _round_robin(queued)
        # Plan (g): a multipart upload spends up to a slice of seconds per visit, so every other
        # lane goes first each pass (a metric behind a 10 GB checkpoint is delivered before its
        # next slice). ONE upload at a time sends or hashes (the oldest not waiting on the
        # server); the next starts only when it is verifying, so an earlier checkpoint finishes
        # and releases its staged bytes before a later one pins more.
        queued = [*queued, *multipart_queue]
        multipart_turn = next(
            (p for p, o in multipart_queue if not _multipart_waiting(o)), None
        )
        skip = set(skip_runs or ())
        stalled = report.stalled_runs
        # Runs parked for the pass behind an op this drainer must not send.
        held_runs: set = set()
        # Of those, the runs held for a credential (#2035): their later ops count as kept too.
        credential_lanes: dict = {}
        held_paths: set = set()

        def hold(lane: Any, ops: list, held: OpHeldHere) -> None:
            """Where every `OpHeldHere` lands, for a lone op or a batch: each op stays queued as
            it is and its run's later ops (its close) wait out the pass behind it. An op naming
            no run holds only itself. #2041 counts `credential_held` and its reasons here."""
            nonlocal held_note
            if lane is not None:
                held_runs.add(lane)
            if isinstance(held, CredentialNotHere):
                # Not this drainer's to send (#2035): untouched, no attempt counted, nothing
                # dead-lettered, every op this drainer CAN send still goes. Its run's lane STALLS
                # as well as parks: a worker backs that run off and stays up instead of exiting
                # and being forked again on the next kick (#2041 round 3, MED-2).
                note = held_note = str(held)
                report.credential_held += len(ops)
                if held.permanent:
                    report.permanently_held += len(ops)
                held_paths.update(item[0] for item in ops)
                if lane is not None:
                    credential_lanes[lane] = credential_lanes.get(lane, False) or held.permanent
                if note not in report.held_reasons:
                    report.held_reasons.append(note)
                if lane is not None:
                    stalled[lane] = LaneStall(note, held=True)
            log.debug("outbox: %d op(s) of run %s held: %s", len(ops), lane, held)

        for _path, queued_op in queued:
            queued_stamp = (queued_op.get("context") or {}).get("principal")
            queued_as = stamp_identity(queued_stamp) if isinstance(queued_stamp, dict) else None
            if queued_as is not None:
                accounts.setdefault(str(queued_stamp.get("fingerprint")), queued_as)
        try:
            journal.quarantine_paths(corrupt, known=known)
        except Exception:  # noqa: BLE001 -- quarantine is best-effort hygiene
            pass
        workers = _upload_workers()
        parallel = workers > 1
        prefetched: dict = {}

        def window_skips(path: Path, op: dict) -> bool:
            """What the serial pass below would not attempt now, for `_run_window`: such an op
            ends its run's parallel window."""
            lane = _lane_of(op)
            return (
                (only_ops is not None and op.get("op_id") not in only_ops)
                or lane in skip
                or lane in stalled
                or lane in held_runs
                or lane in credential_lanes
                or path.name > held_back.get(lane, path.name)
                or drain_hold.busy(lane)
            )

        def run_busy(lane: Any) -> None:
            """Another drain is sending ``lane`` (it let go of the drain lock for that run's
            upload, #3618): the run waits out this pass, its later ops with it. Not a failure:
            looked at again soon."""
            reason = f"another drain is sending the writes of run {lane}"
            stalled[lane] = LaneStall(reason, held=True, wake_by=_RUN_BUSY_RECHECK_SECONDS)
            report.busy_runs.add(lane)

        # The window REFILLS as the serial loop advances. A single fetch took the first
        # `workers * FACTOR` operations and every one after went back to being uploaded alone:
        # a hundred-thousand-file import parallelised sixteen files and serialised the rest,
        # the latency this exists to remove, hidden behind a test that never staged over eight.
        cursor = 0
        lost_responses = 0
        def settle_batch(batch: list, landed: list, failed: list, lane: Any) -> str:
            """Credit what a coalesced POST delivered, settle each op that did not land as if
            sent alone, and put the ops the batch never reached back in line for this pass."""
            for landed_path, _ in landed:
                landed_path.unlink(missing_ok=True)
            if landed:
                # One fsync for the batch, as the single path does per op.
                fsync_directory(journal.ops_dir)
                for producer_id, count in _count_producers(landed).items():
                    try:
                        journal.note_delivered(producer_id, count)
                    except Exception:  # noqa: BLE001 -- accounting never breaks the drain
                        pass
                for _, landed_op in landed:
                    report.delivered += 1
                    notify_delivered(landed_op)
                    landed_fp = _stamp_fingerprint(landed_op)
                    if landed_fp is not None:
                        delivered_fps.add(landed_fp)
                        learn_account(landed_op)
                report.progressed_runs.add(lane)
            settled = {item[0] for item in landed} | {item[0] for item, _ in failed}
            for item_path, _ in batch:
                if item_path not in settled:
                    consumed.discard(item_path)
            for (failed_path, failed_op), exc in failed:
                if settle_failure(failed_path, failed_op, exc, lane) == "break":
                    return "break"
            return "continue"

        def still_queued(item_path: Path, item_op: dict) -> bool:
            """For `_coalesce` once this pass let go of the drain lock: an op another drain sent
            meanwhile does not ride again (#3618)."""
            if item_path in consumed:
                return False
            if drain_hold.fresh(item_path, item_op):
                return True
            consumed.add(item_path)
            return False

        def settle_window(items: list, landed: dict) -> dict:
            """Credit the uploads a window sent (`_prefetch_uploads`), now: each leaves the queue
            (one fsync for all) and is counted as the serial pass counts one. Returns what could
            not be settled (a receipt the server's answer cannot make) for the serial pass."""
            nonlocal settled_upload
            ops_of = {item_path: item_op for item_path, item_op in items}
            left: dict = {}
            gone: list = []
            for landed_path, result in landed.items():
                try:
                    journal._save_delivery_receipt(ops_of[landed_path], result)
                except Exception:  # noqa: BLE001 -- settled by the serial pass, as before
                    left[landed_path] = result
                    continue
                landed_path.unlink(missing_ok=True)
                consumed.add(landed_path)
                gone.append(landed_path)
            if not gone:
                return left
            fsync_directory(journal.ops_dir)
            for landed_path in gone:
                landed_op = ops_of[landed_path]
                journal._scan_forget(landed_path.name)
                tally_delivered(landed_op)
                report.delivered += 1
                report.progressed_runs.add(_lane_of(landed_op))
                notify_delivered(landed_op)
                landed_fp = _stamp_fingerprint(landed_op)
                if landed_fp is not None:
                    delivered_fps.add(landed_fp)
                    learn_account(landed_op)
            settled_upload = True
            return left

        def settle_failure(path: Path, op: dict, exc: Exception, lane: Any) -> str:
            """What one op's failure does to it and the pass: ``"continue"`` or ``"break"``. The
            single path and a coalesced batch (plan 1.2) both come here, so a merged op fails
            as it would alone."""
            nonlocal settled_upload, lost_responses

            if isinstance(exc, errors.OfflineRunNotCreated):
                # An offline run's op ahead of its run (plan 2.12: its create was refused or is
                # queued behind a transient stop). Not this op's fault: no attempt charged, it
                # keeps its place; `probe sync` names the fix.
                report.stopped_transient = True
                report.errors.append(_redact(str(exc)))
                return "break"
            if isinstance(exc, errors.DeadlineExceeded):
                # The CALLER's clock ran out (finish()'s close budget), not the op: nothing was
                # learned about the server, so no error is recorded, the failure clock does not
                # start, and the op keeps its place for the detached worker. Exception: when the
                # request had fully left (`sent`) the server may have applied it, so the ATTEMPT
                # is recorded; a replayed create whose 409 names `existing_id` is then read as
                # its own earlier delivery, not a first-attempt conflict.
                if getattr(exc, "sent", False):
                    op["attempts"] = _attempts(op) + 1
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                    known[path.name] = _meta_of(op)  # the recount's cache follows
                report.deadline_reached = True
                return "break"
            if on_error is not None:
                on_error(exc)
            if errors.names_stale_write_epoch(exc) and not _is_multipart(op):
                # A newer attempt owns the run (the op's write epoch is past): the server refuses
                # it every time, so it is set aside in discarded/ (kept, never sent) instead of
                # dead-lettered, where it nagged every session start and `probe outbox retry`
                # could never deliver it (#3629, T24). Before the idempotent check: the
                # heartbeat's refusal names `existing_id`.
                op["attempts"] = _attempts(op) + 1
                op["last_error"] = _redact(f"{type(exc).__name__}: {exc}")
                write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                target = journal._discard_dir()
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                os.replace(path, target / path.name)
                fsync_directory(target)
                fsync_directory(path.parent)
                report.superseded.add(op)
                report.progressed_runs.add(lane)
                settled_upload = settled_upload or op.get("kind") == "upload"
                return "continue"
            verdict = classify(exc)
            if _edge_already_there(op, exc) or (
                verdict == "idempotent"
                and _attempts(op) > 0
                and not op.get("correlation")
            ):
                # A 409-with-existing_id on a RETRY plausibly names our own earlier
                # half-delivered attempt. On a FIRST attempt it is a genuine natural-key conflict:
                # treating it as success would silently discard the queued write (codex), so it
                # falls to the permanent path. Exception: an edge that already exists IS the
                # write done.
                extra = sorted(k for k in ("reason", "meta", "provenance") if (op.get("body") or {}).get(k))
                if extra and _edge_already_there(op, exc):
                    log.info("outbox: edge op %s already existed; its %s was not applied",
                             op.get("op_id"), ", ".join(extra))
                path.unlink(missing_ok=True)
                fsync_directory(journal.ops_dir)
                tally_delivered(op)
                report.delivered += 1
                report.progressed_runs.add(lane)
                notify_delivered(op)
                settled_upload = settled_upload or op.get("kind") == "upload"
                return "continue"
            op["attempts"] = _attempts(op) + 1
            op["last_error"] = _redact(f"{type(exc).__name__}: {exc}")
            if (
                verdict == "transient"
                # This computer's workspace limit refused (e.g. it names a deleted workspace):
                # every op fails alike until a person runs `probe workspace limit`, so none may
                # run out of patience meanwhile. Ordinary lane backoff, never a hot loop.
                and not isinstance(exc, errors.WorkspaceLimitError)
                and _failing_for_seconds(op, time.time()) >= _transient_budget_seconds()
                and op["attempts"] >= MIN_TRANSIENT_ATTEMPTS
            ):
                # Out of patience, not politeness. Parking is right for a blip and ruinous for a
                # permanent fault: the queue behind this op never moves and the run never closes.
                # Past the budget (WALL-CLOCK since the first failure, so no loop's poll rate
                # decides it, AND a floor of attempts, so one blip after a day asleep cannot
                # either) we stop calling it transient and let the permanent path record what it
                # can and move on.
                verdict = "permanent"
            if verdict == "auth":
                from ....settings.key_refusal import credential_refused

                if _stamp_fingerprint(op) in adopted_login:
                    # Refused while going out with the ADOPTING login: what that login may do
                    # says nothing about the credential that queued it (`op_refusal`).
                    op["refused_via_adoption"] = True
                elif isinstance(exc, errors.ScopeError) and not credential_refused(403, str(exc)):
                    # Sticky: a later 401 (token revoked) rewrites `last_error` and must not
                    # erase that this write asked for more than its credential may do
                    # (`op_refusal`).
                    op["refused_for_scope"] = True
                    op.pop("refused_via_adoption", None)
                write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                known[path.name] = _meta_of(op)  # a hashed upload now has a size
                refused_context = op.get("context")
                if not report.auth_blocked:
                    report.auth_status = getattr(exc, "status", None)
                    report.auth_message = str(exc)
                    report.auth_context = refused_context
                report.auth_blocked = True
                refused_fp = _stamp_fingerprint(op)
                report.auth_refusals.append(
                    {
                        "status": getattr(exc, "status", None),
                        "message": str(exc),
                        "context": refused_context,
                        "fingerprint": refused_fp,
                    }
                )
                report.errors.append(op["last_error"])
                if refused_fp is not None:
                    # A stamped op names its credential, so only that credential's writes stop;
                    # the rest (a PROBE_TOKEN job's own, say) keeps going. It used to stop the
                    # whole pass and block the box (#2041 review).
                    refused_now[refused_fp] = now_iso()
                    delivered_fps.discard(refused_fp)
                    login_fp = adopted_login.get(refused_fp)
                    if login_fp:
                        refused_now[login_fp] = refused_now[refused_fp]
                        delivered_fps.discard(login_fp)
                    if lane is not None:
                        stalled[lane] = LaneStall(op["last_error"], status=getattr(exc, "status", None))
                    report.credential_refused += 1
                    return "continue"
                report.queue_auth_stopped = True
                return "break"
            if verdict in ("permanent", "idempotent"):
                # A permanently rejected UPLOAD must still leave a record. The sync path degrades
                # to a reference artifact (`meta.upload = "failed"`), which `check_run` counts as
                # a capture gap. The drainer had no such path: a rejected queued upload left NO
                # artifact row, only an outbox dead letter nobody reads. A capability regression
                # inside the async upload, closed BEFORE uploads may be queued at all.
                if (
                    verdict == "permanent"
                    and op.get("kind") in ("upload", "multipart_upload")
                    and not op.get("correlation")
                    # An adopted credential's refused upload: nothing may write for it with the
                    # adopting login, a fallback row included.
                    and not isinstance(exc, (CredentialBlocked, AdoptedRouteRefused))
                ):
                    # BUILDING the fallback client resolves credentials, which can itself fail
                    # (always, for an unroutable endpoint). Evaluated bare as an argument it
                    # raised out of this `except`, the loop and drain(), stranding every op
                    # behind it: the wedge the permanent verdict exists to remove. A fallback may
                    # never break the drain.
                    try:
                        fallback = client_for(op.get("context"))
                    except Exception:
                        fallback = None
                    with _delivery_scope(op):
                        recorded = fallback is not None and _record_upload_fallback(
                            journal, fallback, op
                        )
                    if recorded:
                        # THE FALLBACK IS THE RESOLUTION, so this op stops holding the run open.
                        # The sync upload path degrades to exactly this row and leaves no failure
                        # state; a queued upload reaching the same end must not be why
                        # `Run.finish` refuses to close. The dead letter is still written (the
                        # audit trail `probe outbox status` shows), no longer counting as
                        # blocking (`Run._queued_ops`).
                        op["blocking"] = False
                if _is_multipart(op) and not isinstance(exc, AdoptedRouteRefused):
                    # Plan (g): a dead multipart upload keeps no bytes (one refused on the adopted
                    # route keeps them, for a retry with its own credential, and is never aborted
                    # with the adopting login: that is a DELETE). Its staged copy goes and the
                    # server's upload is aborted (best-effort: the server sweeps an idle one).
                    try:
                        multipart_storage("multipart").on_dead_letter(journal, client_for, op)
                    except Exception:  # noqa: BLE001 -- cleanup never breaks the drain
                        pass
                # Update in place, then MOVE atomically: writing a failed/ copy before unlinking
                # the original leaves the op in both queues across a crash (codex).
                write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                # A multipart op dead-letters into its own queue's failed/, never the shared one,
                # where an older release's `probe outbox retry` would move it into ops/ for a
                # worker that cannot send it.
                failed_dir = path.parent.parent / "failed" if _is_multipart(op) else journal.failed_dir
                failed_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
                os.replace(path, failed_dir / path.name)
                fsync_directory(failed_dir)
                fsync_directory(path.parent)
                report.dead_lettered += 1
                report.progressed_runs.add(lane)
                report.errors.append(op["last_error"])
                report.dead_letter_records.append(
                    {
                        "run_ref": op.get("run_ref"),
                        "op_id": op.get("op_id"),
                        "error": str(op["last_error"])[:_DEAD_LETTER_ERROR_CHARS],
                        "status": getattr(exc, "status", None),
                        # The server's own "run not found", told apart from every other 404 (a run
                        # token's refusal, a swept upload, R2): those lose writes for our reasons.
                        "no_such_run": errors.names_no_such_run(exc),
                    }
                )
                settled_upload = settled_upload or op.get("kind") == "upload"
                return "continue"
            # transient: park in place, order preserved
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
            known[path.name] = _meta_of(op)  # a hashed upload now has a size
            report.stopped_transient = True
            report.errors.append(op["last_error"])
            retry_after = getattr(exc, "retry_after", None)
            if retry_after is not None:
                report.retry_after = max(report.retry_after or 0.0, float(retry_after))
            if getattr(exc, "unreachable", False):
                # Nobody's op can land: stop the pass, as before lanes.
                report.unreachable = True
                return "break"
            if (
                isinstance(exc, errors.TransportError)
                and getattr(exc, "status", None) is None
                and not isinstance(exc, errors.DeadlineExceeded)
            ):
                # Sent, and no answer came. Once may be this op; twice in one pass is a server
                # that accepts and hangs, and trying every run's head would hold the drain lock
                # (`finish()` waits on it) for one read timeout per run (review of #2051).
                lost_responses += 1
                if lost_responses >= 2:
                    report.unreachable = True
                    return "break"
            stalled[lane] = LaneStall(op["last_error"], retry_after, getattr(exc, "status", None))
            return "continue"

        for position, (path, op) in enumerate(queued):
            if path in consumed:
                continue  # delivered inside an earlier op's batch
            if parallel and path not in prefetched and cursor <= position:
                ahead = queued[
                    position : position + workers * UPLOAD_WINDOW_FACTOR * UPLOAD_WINDOW_SCAN_FACTOR
                ]
                if drain_hold.let_go:
                    # Another drain may have sent or changed some of these while this pass was
                    # away: only what is still queued may go.
                    ahead = [
                        item for item in ahead
                        if item[0] in consumed or drain_hold.fresh(*item)
                    ]
                try:
                    landed = _prefetch_uploads(
                        journal,
                        ahead,
                        client_for,
                        workers,
                        run_ref,
                        skips=window_skips,
                        already=prefetched.keys() | consumed,
                        away=drain_hold.away,
                    )
                except _LockNotBack:
                    # Its uploads stay queued (results unrecorded) for the next drain, which
                    # sends them again: a file the server holds gets its row back, no bytes move
                    # twice.
                    report.deadline_reached = True
                    break
                if drain_hold.yields:
                    # Settled NOW, not when the serial pass reaches each: this pass lets go of
                    # the drain lock again and another drain would send a landed upload whose op
                    # file is still queued a second time (`_DrainHold.away`).
                    prefetched.update(settle_window(ahead, landed))
                else:
                    prefetched.update(landed)
                if landed or not any(
                    isinstance(o, dict)
                    and o.get("kind") == "upload"
                    and p not in prefetched
                    and p not in consumed
                    for p, o in ahead
                ):
                    cursor = position + workers * UPLOAD_WINDOW_FACTOR
                else:
                    # Uploads ahead, none free to go yet: an op in front of them (a run's
                    # metadata, a span) goes first. Look again right after it, not a window
                    # later (a run's first 30 uploads went one by one behind its first write).
                    cursor = position + 1
            if only_ops is not None and op.get("op_id") not in only_ops:
                continue
            if run_ref is not None and op.get("run_ref") != run_ref:
                continue
            if _is_multipart(op) and path != multipart_turn and not _multipart_waiting(op):
                continue  # not its turn: one upload at a time (plan (g))
            lane = _lane_of(op)
            if lane in credential_lanes and path not in held_paths:
                # A later op of a run held for its credential (or a close held behind another
                # queue): kept too and counted, so "N kept" says how many writes wait, not how
                # many runs (#2041 round 4), and how many `discard --held` would drop (round 5).
                report.credential_held += 1
                if credential_lanes[lane]:
                    report.permanently_held += 1
                continue
            if lane in skip:
                report.skipped += 1
                continue  # backed off: its run waits; the other runs do not
            if lane in stalled or lane in held_runs:
                continue  # its run waits; the other runs do not
            if path.name > held_back.get(lane, path.name):
                report.held_back += 1
                continue
            # Between two ops: a close waiting for the drain lock gets it now
            # (#3618). Whatever another drain did meanwhile is on disk.
            try:
                drain_hold.between_ops()
            except _LockNotBack:
                report.deadline_reached = True
                break
            if not drain_hold.fresh(path, op):
                consumed.add(path)
                continue  # another drain sent it, or set it aside, while this pass was away
            if drain_hold.busy(lane):
                run_busy(lane)
                continue
            kind = op.get("kind")
            if isinstance(kind, str) and kind not in OP_KINDS:
                # A newer SDK's op. Not attempted: no attempt charged, the 24 h budget never
                # starts; it waits, in its run's order, for a worker that can deliver it (plan
                # 1.11). A kind that is not even a string is not a newer SDK's: `_execute`
                # refuses it (dead letter), as always (review of #2052: a list here raised
                # TypeError and failed every pass machine-wide).
                reason = f"op kind {kind!r} needs a newer probe-research to deliver it"
                report.unknown_kinds += 1
                if reason not in report.errors:
                    report.errors.append(reason)
                if lane is not None:
                    stalled[lane] = LaneStall(reason)
                # An op naming no run holds only itself: the run-less lane has no order to keep
                # and stalling it would hold every other run-less write behind a newer SDK's op.
                continue
            if lane is not None and _is_run_close(op) and not _close_hold_expired(op):
                waiting = writes_elsewhere(lane, op.get("enqueued_at"), _write_epoch_of(op))
                if waiting:
                    # The close must not land before its data: writes of this run queued earlier
                    # under another credential are in another queue, which this queue's order
                    # cannot see (#2041 round 3). Held, at most CLOSE_HOLD_MAX_SECONDS.
                    reason = (
                        f"the close of run {lane} waits for {waiting} of its write(s) queued "
                        "under another credential"
                    )
                    stalled[lane] = LaneStall(reason, held=True, wake_by=_close_hold_left(op))
                    report.close_held += 1
                    if reason not in report.held_reasons:
                        report.held_reasons.append(reason)
                    continue
            journal._scan_forget(path.name)  # attempted: read it fresh next pass
            batch = (
                []
                if journal.receipt_enabled
                else _coalesce(
                    lanes.get(lane) or [],
                    lane_index.get(path, 0),
                    held_back.get(lane),
                    still_queued=still_queued if drain_hold.let_go else None,
                )
            )
            for item_path, _ in batch:
                journal._scan_forget(item_path.name)

            if batch:
                # Plan 1.2: this op and the metric ops queued right behind it in its run, as ONE
                # POST (see `_deliver_batch`). Settled OUTSIDE the per-op `try`: an error while
                # settling must not send the head through `settle_failure` again after it landed
                # (review of #2053).
                try:
                    client = client_for(op.get("context"), op=op)
                except OpHeldHere as held:
                    # Every op of the batch shares the head's context (it is in
                    # `_merge_key`), so none of them is this drainer's to send.
                    hold(lane, batch, held)
                    continue
                except Exception as exc:  # noqa: BLE001 -- the head's failure, as alone
                    if settle_failure(path, op, exc, lane) == "break":
                        break
                    continue
                consumed.update(item[0] for item in batch)
                with _delivery_scope(op):
                    landed, failed, merged = _deliver_batch(journal, client, batch, run_ids)
                report.coalesced += merged
                try:
                    action = settle_batch(batch, landed, failed, lane)
                except Exception as exc:  # noqa: BLE001 -- e.g. ENOSPC recording a failure
                    # What landed may be sent again next pass (the insert keeps the first write
                    # of a point); nothing is lost or resent now. The run waits for the rest of the
                    # pass: an unsettled op of it is still queued and its later ops (its close)
                    # must not go ahead of it (review of #2053).
                    log.warning("outbox: settling a coalesced batch failed", exc_info=True)
                    stalled[lane] = LaneStall(_redact(f"{type(exc).__name__}: {exc}"))
                    action = "continue"
                if action == "break":
                    break
                continue
            went_away = drain_hold.let_go  # the count before this op's attempt
            try:
                if journal.receipt_enabled and op.get("schema") != DELIVERY_SCHEMA:
                    raise errors.ValidationError(
                        "unsupported delivery operation schema", status=422
                    )
                if op.get("correlation") and journal.receipt(op["correlation"]) is not None:
                    # Receipt committed before a crash prevented op deletion.
                    result = None
                elif path in prefetched:
                    # Its bytes already moved, in parallel with its neighbours. The receipt is
                    # still written here, in order, on this thread (`_prefetch_uploads`).
                    journal._save_delivery_receipt(op, prefetched[path])
                else:
                    with _delivery_scope(op):
                        sender = client_for(op.get("context"), op_credential(op)[1], op=op)
                        # An upload's bytes go with the drain lock let go and its run's lock held
                        # (#3618): a 30 MiB file no longer holds every other run's close for the
                        # length of its PUT.
                        sending = (
                            drain_hold.away({lane})
                            if op.get("kind") == "upload" and not op.get("correlation")
                            else nullcontext()
                        )
                        with sending:
                            result = _execute(journal, sender, path, op, run_ids)
                    journal._save_delivery_receipt(op, result)
                delivered_fp = _stamp_fingerprint(op)
                if delivered_fp is not None:
                    delivered_fps.add(delivered_fp)
                    learn_account(op)
            except OpInProgress as progress:
                # Plan (g): the long op moved (or waits on the server) and saved where it is;
                # nothing failed, so no attempt is charged.
                if progress.retry_after is not None:
                    # Waiting (server verifying, its own hash in the background, another upload
                    # of the same bytes): this lane backs off, at least `retry_after`, growing.
                    stalled[lane] = LaneStall(
                        str(progress), progress.retry_after, wake_by=progress.wake_by
                    )
                else:
                    # A slice of parts went: that IS progress (the worker must not sleep to
                    # another lane's backoff after it); the next pass takes the next slice.
                    report.in_progress += 1
                    report.progressed_runs.add(lane)
                    if lane is not None:
                        held_runs.add(lane)
                continue
            except OpHeldHere as held:
                hold(lane, [(path, op)], held)
                continue
            except Exception as exc:  # noqa: BLE001 -- classified in settle_failure
                if (
                    not isinstance(exc, _LockNotBack)
                    and drain_hold.let_go != went_away
                    and not path.exists()
                ):
                    # Sent with the lock let go, and meanwhile a drain that knows no run locks (an
                    # older release, `probe outbox discard`) delivered it or set it aside: writing
                    # the op back would bring it back into the queue (#3618).
                    continue
                if settle_failure(path, op, exc, lane) == "break":
                    break
                continue
            else:
                if drain_hold.let_go != went_away and not path.exists():
                    report.delivered += 1  # it landed; another drain settled its file
                    report.progressed_runs.add(lane)
                    continue
                path.unlink(missing_ok=True)
                # fsync so a post-delivery crash cannot resurrect the op file and replay a write
                # the server already committed (codex: replay is at-least-once; keep the window
                # as small as disk semantics allow).
                fsync_directory(journal.ops_dir)
                tally_delivered(op)
                report.delivered += 1
                report.progressed_runs.add(lane)
                notify_delivered(op)
                settled_upload = settled_upload or op.get("kind") == "upload"
    finally:
        for client in constructed:
            try:
                client.close()
            except Exception:  # noqa: BLE001
                pass
        if settled_upload:  # no upload left the queue: no blob can be unreferenced
            try:
                journal.gc_blobs()
            except Exception:  # noqa: BLE001
                pass
        # Counted from the recount itself: names under the lock, parsing only what this pass's
        # scan did not see (plan 1.9).
        journal._ensure()
        with file_lock(journal.append_lock):
            # Merged with what is on disk NOW, under the append lock: a `probe login` during
            # this pass cleared the list (clear_auth_block) and writing back the one read at
            # the start undid it (#2041 re-review).
            previous = Journal.read_status(journal.dir, include_receipts=False, keep_idle_refusals=True) or {}
            on_disk = previous.get("refused_fingerprints") or {}
            if not isinstance(on_disk, dict):
                on_disk = {}
            # A held run the caller backs off is skipped next pass; not recounting its holds
            # wrote `held: 0` while they still waited and the stuck signal flickered. The last
            # count stands for the ops this pass did not look at.
            carried = min(_status_count(previous.get("held")), report.skipped)
            carried_close = min(_status_count(previous.get("close_held")), carried)
            cleared = set(cooling) - set(on_disk)
            report.remaining = journal._write_status_locked(
                known=known,
                auth_blocked_since=(now_iso() if report.queue_auth_stopped else None),
                held=report.credential_held + report.credential_refused + report.close_held + carried,
                close_held=report.close_held + carried_close,
                held_at=now_iso(),
                refused_fingerprints={
                    **{fp: at for fp, at in on_disk.items() if fp not in delivered_fps},
                    **{fp: at for fp, at in refused_now.items() if fp not in cleared},
                },
                last_error=(report.errors[-1] if report.errors else held_note),
                new_dead_letters=report.dead_letter_records,
            )
        if not journal.receipt_enabled:
            # Plan (g): an upload still in its own queue is still work, so a worker does not
            # exit with one half-sent (status.json's count, which older releases read, stays
            # the shared queue's).
            report.remaining += _multipart_pending_count(journal)
        drain_hold.close()
        oscompat.flock(lock_handle.fileno(), oscompat.LOCK_UN)
        lock_handle.close()
        if report.superseded.writes:
            # Set aside, not lost by us: a newer attempt owns those runs (T24). Every drain
            # says so (a `finish()`'s, a flush's, the worker's), as a dead letter used to reach
            # `probe outbox status`.
            try:
                from ..... import analytics as _telemetry

                _telemetry.emit_outbox_discarded(
                    report.superseded, reason=_telemetry.DiscardReason.SUPERSEDED
                )
            except Exception:  # noqa: BLE001 -- telemetry never stops delivery
                pass
    return report
from probe.sdk.delivery.journal.item_locks import _try_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import Journal, log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.paths import _queue_is_empty  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.status_file import _status_count  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _edge_already_there,
    _failing_for_seconds,
    _redact,
    _transient_budget_seconds,
    classify,
)
from probe.sdk.delivery.ops.op_handler import (  # noqa: E402 -- pieces need each other
    _delivery_scope,
    _execute,
    _record_upload_fallback,
    multipart_storage,
)
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CREDENTIAL_NAMESPACE,
    DELIVERY_SCHEMA,
    OP_KINDS,
    _attempts,
    _is_multipart,
    _is_run_close,
    _lane_of,
    _meta_of,
    _write_epoch_of,
    delivery_client,
    op_meta,
)
from probe.sdk.delivery.outbox.drain.accounts import record_account, recorded_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import AdoptedRouteRefused, adopted_account, adopted_route_refuses  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.coalesce import _coalesce, _count_producers, _deliver_batch  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CredentialSource,
    _cooling_refusals,
    _identity_of,
    _login_base_of,
    _settings_for_op,
    _stamp_fingerprint,
    _stored_login_fingerprint,
    credential_fingerprint,
    op_credential,
    stamp_identity,
)
from probe.sdk.delivery.outbox.drain.holds import _close_hold_expired, _close_hold_left, restore_abandoned_holds  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lanes import _multipart_pending_count, _multipart_waiting, _round_robin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lock import _DrainHold, _LockNotBack, _take_drain_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import CredentialNotHere, DrainReport, LaneStall, OpHeldHere, OpInProgress  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.upload_windows import _prefetch_uploads, _upload_workers  # noqa: E402 -- pieces need each other; the front door loads this one first
