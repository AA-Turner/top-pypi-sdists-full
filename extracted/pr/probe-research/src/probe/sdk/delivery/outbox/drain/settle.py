"""DrainSettleMixin: settle each op a pass attempted -- landed, held, in progress, or failed per classify()."""

from __future__ import annotations

import json
import os
from pathlib import Path
import time
from typing import Any

from probe.foundation.durable.durable import fsync_directory, now_iso, write_text_atomic
from probe.sdk import errors
from probe.sdk.secret_gate import CredentialBlocked


_DEAD_LETTER_ERROR_CHARS = 300

#: ...AND at least this many attempts. Time alone would dead-letter a laptop's whole queue on
#: the first blip after a day asleep; attempts alone let the poll rate decide. Both must be
#: spent. Cost, until per-run lanes (plan 1.6) stop one run's head holding the others: a
#: poison op the server always answers 5xx blocks the machine's FIFO for a day.
MIN_TRANSIENT_ATTEMPTS = 50
#: How soon a pass looks again at a run another drain is sending (holds its lock): a ceiling
#: on that run's backoff, not a failure.
_RUN_BUSY_RECHECK_SECONDS = 5.0


class DrainSettleMixin:
    """Part of DrainPass: its methods run with `self` the DrainPass; fold_parts() copies them into DrainPass."""

    def _record_in_progress(self, progress: OpInProgress, lane: Any, op: dict | None = None) -> None:
        """Plan (g): the long op moved (or waits on the server) and saved where it is;
        nothing failed, so no attempt is charged."""
        if progress.retry_after is not None:
            # Waiting (server verifying, its own hash in the background, another upload
            # of the same bytes): this lane backs off, at least `retry_after`, growing.
            self.stalled[lane] = LaneStall(
                str(progress), progress.retry_after, wake_by=progress.wake_by
            )
        else:
            # A slice of parts went: that IS progress (the worker must not sleep to
            # another lane's backoff after it); the next pass takes the next slice.
            self.report.in_progress += 1
            self.report.progressed_runs.add(lane)
            self.report.note_run_progress(op, delivered=False)
            if lane is not None:
                self.held_runs.add(lane)

    def _settle_landed(self, path: Path, op: dict, lane: Any, went_away: int) -> None:
        """A delivered op leaves the queue, durably, and is counted."""
        report = self.report
        if self.drain_hold.let_go != went_away and not path.exists():
            report.delivered += 1  # it landed; another drain settled its file
            report.progressed_runs.add(lane)
            report.note_run_progress(op, delivered=True)
            return
        path.unlink(missing_ok=True)
        # fsync so a post-delivery crash cannot resurrect the op file and replay a write
        # the server already committed (codex: replay is at-least-once; keep the window
        # as small as disk semantics allow).
        fsync_directory(self.journal.ops_dir)
        self.count_delivered(op)
        report.delivered += 1
        report.progressed_runs.add(lane)
        report.note_run_progress(op, delivered=True)
        self.notify_delivered(op)
        self.settled_upload = self.settled_upload or op.get("kind") == "upload"

    # -- settling -------------------------------------------------------------------------------
    def count_delivered(self, op: dict) -> None:
        """Credit one landed op to the producer that enqueued it. Runs AFTER the op file is gone
        (see ``note_delivered``) and never fails a delivery: accounting is diagnostics, the
        write already happened."""
        producer_id = op.get("producer_id")
        if not producer_id:
            return
        try:
            self.journal.note_delivered(producer_id)
        except Exception:  # noqa: BLE001 -- accounting must never break the drain
            pass

    def notify_delivered(self, op: dict) -> None:
        on_delivered = self.options.on_delivered
        if on_delivered is not None:
            try:
                on_delivered(op.get("correlation"))
            except Exception:  # noqa: BLE001 -- observers cannot fail a committed delivery
                pass

    def hold(self, lane: Any, ops: list, held: OpHeldHere) -> None:
        """Where every `OpHeldHere` lands, for a lone op or a batch: each op stays queued as
        it is and its run's later ops (its close) wait out the pass behind it. An op naming
        no run holds only itself. #2041 counts `credential_held` and its reasons here."""
        report = self.report
        if lane is not None:
            self.held_runs.add(lane)
        if isinstance(held, CredentialNotHere):
            # Not this drainer's to send (#2035): untouched, no attempt counted, nothing
            # dead-lettered, every op this drainer CAN send still goes. Its run's lane STALLS
            # as well as parks: a worker backs that run off and stays up instead of exiting
            # and being forked again on the next kick (#2041 round 3, MED-2).
            note = self.held_note = str(held)
            report.credential_held += len(ops)
            if held.permanent:
                report.permanently_held += len(ops)
            self.held_paths.update(item[0] for item in ops)
            if lane is not None:
                self.credential_lanes[lane] = self.credential_lanes.get(lane, False) or held.permanent
            if note not in report.held_reasons:
                report.held_reasons.append(note)
            if lane is not None:
                self.stalled[lane] = LaneStall(note, held=True)
        log.debug("outbox: %d op(s) of run %s held: %s", len(ops), lane, held)

    def mark_run_busy(self, lane: Any) -> None:
        """Another drain is sending ``lane`` (it let go of the drain lock for that run's
        upload, #3618): the run waits out this pass, its later ops with it. Not a failure:
        looked at again soon."""
        reason = f"another drain is sending the writes of run {lane}"
        self.stalled[lane] = LaneStall(reason, held=True, wake_by=_RUN_BUSY_RECHECK_SECONDS)
        self.report.busy_runs.add(lane)

    def settle_batch(self, batch: list, landed: list, failed: list, lane: Any) -> str:
        """Credit what a coalesced POST delivered, settle each op that did not land as if
        sent alone, and put the ops the batch never reached back in line for this pass."""
        journal = self.journal
        report = self.report
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
                report.note_run_progress(landed_op, delivered=True)
                self.notify_delivered(landed_op)
                landed_fp = _stamp_fingerprint(landed_op)
                if landed_fp is not None:
                    self.delivered_fps.add(landed_fp)
                    self.record_token_account(landed_op)
            report.progressed_runs.add(lane)
        settled = {item[0] for item in landed} | {item[0] for item, _ in failed}
        for item_path, _ in batch:
            if item_path not in settled:
                self.consumed.discard(item_path)
        for (failed_path, failed_op), exc in failed:
            if self.settle_failure(failed_path, failed_op, exc, lane) == "break":
                return "break"
        return "continue"

    def settle_window(self, items: list, landed: dict) -> dict:
        """Credit the uploads a window sent (`_prefetch_uploads`), now: each leaves the queue
        (one fsync for all) and is counted as the serial pass counts one. Returns what could
        not be settled (a receipt the server's answer cannot make) for the serial pass."""
        journal = self.journal
        report = self.report
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
            self.consumed.add(landed_path)
            gone.append(landed_path)
        if not gone:
            return left
        fsync_directory(journal.ops_dir)
        for landed_path in gone:
            landed_op = ops_of[landed_path]
            journal._scan_forget(landed_path.name)
            self.count_delivered(landed_op)
            report.delivered += 1
            report.progressed_runs.add(_lane_of(landed_op))
            report.note_run_progress(landed_op, delivered=True)
            self.notify_delivered(landed_op)
            landed_fp = _stamp_fingerprint(landed_op)
            if landed_fp is not None:
                self.delivered_fps.add(landed_fp)
                self.record_token_account(landed_op)
        self.settled_upload = True
        return left

    def settle_failure(self, path: Path, op: dict, exc: Exception, lane: Any) -> str:
        """What one op's failure does to it and the pass: ``"continue"`` or ``"break"``. The
        single path and a coalesced batch (plan 1.2) both come here, so a merged op fails
        as it would alone."""
        report = self.report
        if isinstance(exc, errors.OfflineRunNotCreated) or getattr(exc, "offline", False):
            # An offline run's op ahead of its run (plan 2.12: its create was refused or is
            # queued behind a transient stop), or an in-process drain of the run's own queue
            # (`flush()`) meeting its refusing transport. Not this op's fault:
            # no attempt charged, it keeps its place; `probe sync` delivers it.
            report.stopped_transient = True
            report.errors.append(_redact(str(exc)))
            return "break"
        if isinstance(exc, errors.DeadlineExceeded):
            return self._settle_deadline(path, op, exc)
        if self.options.on_error is not None:
            self.options.on_error(exc)
        if errors.names_stale_write_epoch(exc) and not _is_multipart(op):
            return self._set_aside_superseded(path, op, exc, lane)
        verdict = classify(exc)
        if _edge_already_there(op, exc) or (
            verdict == "idempotent"
            and _attempts(op) > 0
            and not op.get("correlation")
        ):
            return self._settle_already_there(path, op, exc, lane)
        op["attempts"] = _attempts(op) + 1
        op["last_error"] = _redact(f"{type(exc).__name__}: {exc}")
        verdict = self._apply_transient_budget(verdict, exc, op)
        if verdict == "auth":
            return self._settle_refusal(path, op, exc, lane)
        if verdict in ("permanent", "idempotent"):
            return self._move_to_failed(path, op, exc, lane, verdict)
        return self._hold_transient(path, op, exc, lane)

    def _settle_deadline(self, path: Path, op: dict, exc: Exception) -> str:
        """The CALLER's clock ran out (finish()'s close budget), not the op: nothing was
        learned about the server, so no error is recorded, the failure clock does not
        start, and the op keeps its place for the detached worker. Exception: when the
        request had fully left (`sent`) the server may have applied it, so the ATTEMPT
        is recorded; a replayed create whose 409 names `existing_id` is then read as
        its own earlier delivery, not a first-attempt conflict."""
        if getattr(exc, "sent", False):
            op["attempts"] = _attempts(op) + 1
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
            self.known[path.name] = _meta_of(op)  # the recount's cache follows
        self.report.deadline_reached = True
        return "break"

    def _set_aside_superseded(self, path: Path, op: dict, exc: Exception, lane: Any) -> str:
        """A newer attempt owns the run (the op's write epoch is past): the server refuses
        it every time, so it is set aside in discarded/ (kept, never sent) instead of
        dead-lettered, where it nagged every session start and `probe outbox retry`
        could never deliver it (#3629, T24). Before the idempotent check: the
        heartbeat's refusal names `existing_id`."""
        op["attempts"] = _attempts(op) + 1
        op["last_error"] = _redact(f"{type(exc).__name__}: {exc}")
        write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
        target = self.journal._discard_dir()
        target.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.replace(path, target / path.name)
        fsync_directory(target)
        fsync_directory(path.parent)
        self.report.superseded.add(op)
        self.report.progressed_runs.add(lane)
        self.report.note_run_progress(op, delivered=False)
        self.settled_upload = self.settled_upload or op.get("kind") == "upload"
        return "continue"

    def _settle_already_there(self, path: Path, op: dict, exc: Exception, lane: Any) -> str:
        """A 409-with-existing_id on a RETRY plausibly names our own earlier
        half-delivered attempt. On a FIRST attempt it is a genuine natural-key conflict:
        treating it as success would silently discard the queued write (codex), so it
        falls to the permanent path. Exception: an edge that already exists IS the
        write done."""
        extra = sorted(k for k in ("reason", "meta", "provenance") if (op.get("body") or {}).get(k))
        if extra and _edge_already_there(op, exc):
            log.info("outbox: edge op %s already existed; its %s was not applied",
                     op.get("op_id"), ", ".join(extra))
        path.unlink(missing_ok=True)
        fsync_directory(self.journal.ops_dir)
        self.count_delivered(op)
        self.report.delivered += 1
        self.report.progressed_runs.add(lane)
        self.report.note_run_progress(op, delivered=True)
        self.notify_delivered(op)
        self.settled_upload = self.settled_upload or op.get("kind") == "upload"
        return "continue"

    @staticmethod
    def _apply_transient_budget(verdict: str, exc: Exception, op: dict) -> str:
        """``"permanent"`` for a transient failure that has spent its patience, else ``verdict``."""
        if (
            verdict == "transient"
            # This computer's workspace limit refused (e.g. it names a deleted workspace):
            # every op fails alike until a person runs `probe workspace limit`, so none may
            # run out of patience meanwhile. Ordinary lane backoff, never a hot loop.
            and not isinstance(exc, errors.WorkspaceLimitError)
            # A write the stall rule set aside goes back to held/, never to failed/ (R9).
            and not was_held(op)
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
        return verdict

    def _settle_refusal(self, path: Path, op: dict, exc: Exception, lane: Any) -> str:
        """The API refused the op's credential: a stamped op stops that credential's writes for
        the pass, an unstamped one the whole queue."""
        from ....settings.key_refusal import credential_refused

        report = self.report
        if _stamp_fingerprint(op) in self.adopted_login:
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
        self.known[path.name] = _meta_of(op)  # a hashed upload now has a size
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
            self.refused_now[refused_fp] = now_iso()
            self.delivered_fps.discard(refused_fp)
            login_fp = self.adopted_login.get(refused_fp)
            if login_fp:
                self.refused_now[login_fp] = self.refused_now[refused_fp]
                self.delivered_fps.discard(login_fp)
            if lane is not None:
                self.stalled[lane] = LaneStall(op["last_error"], status=getattr(exc, "status", None))
            report.credential_refused += 1
            return "continue"
        report.queue_auth_stopped = True
        return "break"

    def _move_to_failed(self, path: Path, op: dict, exc: Exception, lane: Any, verdict: str) -> str:
        """A permanent failure: the op moves to failed/ (an upload keeps a reference row first,
        a multipart upload drops its staged bytes) and the queue flows on."""
        report = self.report
        if (
            verdict == "permanent"
            and op.get("kind") in ("upload", "multipart_upload")
            and not op.get("correlation")
            # An adopted credential's refused upload: nothing may write for it with the
            # adopting login, a fallback row included.
            and not isinstance(exc, (CredentialBlocked, AdoptedRouteRefused))
        ):
            self._record_fallback_row(op)
        if _is_multipart(op) and not isinstance(exc, AdoptedRouteRefused):
            # Plan (g): a dead multipart upload keeps no bytes (one refused on the adopted
            # route keeps them, for a retry with its own credential, and is never aborted
            # with the adopting login: that is a DELETE). Its staged copy goes and the
            # server's upload is aborted (best-effort: the server sweeps an idle one).
            try:
                multipart_storage("multipart").on_dead_letter(self.journal, self.choose_client, op)
            except Exception:  # noqa: BLE001 -- cleanup never breaks the drain
                pass
        # Update in place, then MOVE atomically: writing a failed/ copy before unlinking
        # the original leaves the op in both queues across a crash (codex).
        write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
        # A multipart op dead-letters into its own queue's failed/, never the shared one,
        # where an older release's `probe outbox retry` would move it into ops/ for a
        # worker that cannot send it.
        failed_dir = path.parent.parent / "failed" if _is_multipart(op) else self.journal.failed_dir
        failed_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.replace(path, failed_dir / path.name)
        fsync_directory(failed_dir)
        fsync_directory(path.parent)
        report.dead_lettered += 1
        report.progressed_runs.add(lane)
        report.note_run_progress(op, delivered=False)
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
        self.settled_upload = self.settled_upload or op.get("kind") == "upload"
        return "continue"

    def _set_best_effort_aside(self, path: Path, op: dict, lane: Any) -> bool:
        with holding_run_lock(self.journal, lane) as locked:
            if not locked:
                return False
            if hold_op(path, op, cause=HeldCause.STALLED, retry_seconds=best_effort_retry(op)) is None:
                return False
        self.report.note_run_progress(op, delivered=False)
        return True

    def _hold_again(self, path: Path, op: dict, lane: Any) -> bool:
        """Set a write let out of held/ aside again: a metric, step or upload alone (the rest of
        its run goes on), anything else by holding its run's lane, so nothing passes it."""
        if not is_set_aside_alone(op):
            if lane is None or not hold_lane(
                self.journal.dir, lane, path, run_ref=op.get("run_ref"), error=op.get("last_error")
            ):
                return False
            self.held_lanes.add(lane)
            return True
        with holding_run_lock(self.journal, lane) as locked:
            if not locked or hold_op(path, op, cause=HeldCause.STALLED) is None:
                return False
        self.report.note_run_progress(op, delivered=False)
        return True

    def _record_fallback_row(self, op: dict) -> None:
        """A permanently rejected UPLOAD must still leave a record. The sync path degrades
        to a reference artifact (`meta.upload = "failed"`), which `check_run` counts as
        a capture gap. The drainer had no such path: a rejected queued upload left NO
        artifact row, only an outbox dead letter nobody reads. A capability regression
        inside the async upload, closed BEFORE uploads may be queued at all."""
        # BUILDING the fallback client resolves credentials, which can itself fail
        # (always, for an unroutable endpoint). Evaluated bare as an argument it
        # raised out of this `except`, the loop and drain(), stranding every op
        # behind it: the wedge the permanent verdict exists to remove. A fallback may
        # never break the drain.
        try:
            fallback = self.choose_client(op.get("context"))
        except Exception:
            fallback = None
        with _delivery_scope(op):
            recorded = fallback is not None and _record_upload_fallback(
                self.journal, fallback, op
            )
        if recorded:
            # THE FALLBACK IS THE RESOLUTION, so this op stops holding the run open.
            # The sync upload path degrades to exactly this row and leaves no failure
            # state; a queued upload reaching the same end must not be why
            # `Run.finish` refuses to close. The dead letter is still written (the
            # audit trail `probe outbox status` shows), no longer counting as
            # blocking (`Run._queued_ops`).
            op["blocking"] = False

    def _hold_transient(self, path: Path, op: dict, exc: Exception, lane: Any) -> str:
        """Transient: park in place, order preserved; its run waits, or the pass ends when the
        server is unreachable for everyone."""
        report = self.report
        write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
        self.known[path.name] = _meta_of(op)  # a hashed upload now has a size
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
            self.lost_responses += 1
            if self.lost_responses >= 2:
                report.unreachable = True
                return "break"
        if (
            self.options.set_best_effort_aside
            and is_best_effort(op)
            and not self.journal.receipt_enabled
            and self._set_best_effort_aside(path, op, lane)
        ):
            # Best-effort (lineage, captured outputs, the exit span): never holds its run's line,
            # its close included. Aside at once, tried again in a minute, doubling (R9).
            report.held_again += 1
            return "continue"
        if was_held(op) and not self.journal.receipt_enabled and self._hold_again(path, op, lane):
            # Let out of held/ and still failing: straight back for another hour, not another
            # stall window (R9).
            report.held_again += 1
            return "continue"
        self.stalled[lane] = LaneStall(
            op["last_error"], retry_after, getattr(exc, "status", None), failing=True, path=path
        )
        return "continue"
from probe.sdk.delivery.outbox.drain.adoption import AdoptedRouteRefused  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import CredentialNotHere  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import LaneStall  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import OpHeldHere  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import OpInProgress  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _attempts  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.coalesce import _count_producers  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _delivery_scope  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _edge_already_there  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _failing_for_seconds  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _is_multipart  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _lane_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _meta_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import _record_upload_fallback  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _redact  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _stamp_fingerprint  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _transient_budget_seconds  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.op_handler import multipart_storage  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.held import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    HeldCause,
    best_effort_retry,
    hold_lane,
    hold_op,
    is_best_effort,
    is_set_aside_alone,
    was_held,
)
from probe.sdk.delivery.outbox.drain.lock import holding_run_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
