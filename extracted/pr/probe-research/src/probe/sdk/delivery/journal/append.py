"""AppendMixin: append ops in FIFO order -- op file names, producer sequence stamps, the locked append, http and catalog-manifest ops."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import time
import uuid

from probe.foundation.durable.durable import SYNC_FILE, SYNC_FULL, SYNC_NONE, file_lock, fsync_directory, now_iso, write_text_atomic
from probe.foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk import errors
from probe.sdk.agent_session import queued_event_at, queued_session, run_write_origin
# At module load, not in the drain: a module first imported while a script exits clears its
# pending KeyboardInterrupt (tests/test_ctrlc_exit_code.py).
from probe.sdk.values import unstorable


class AppendMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    # -- append -------------------------------------------------------------
    def _op_filename(self, op_id: str, *, sync: str = SYNC_FULL) -> str:
        """FIFO name: per-journal sequence first, wall clock second, so a clock step cannot reorder ops.
        Under the append lock; starts above the highest sequence queued (`.seq` is not fsynced)."""
        seq_file = self.dir / ".seq"
        try:
            seq = int(seq_file.read_text().strip() or 0)
        except (OSError, ValueError):
            seq = 0
        if not self._seq_recovered:
            floor = self._seq_floor
            if floor is None:
                floor = self._queued_seq_high_water()
            seq = max(seq, floor)
            self._seq_recovered = True
            self._seq_floor = None
        seq += 1
        write_text_atomic(seq_file, f"{seq}\n", mode=0o600, sync=sync)
        return f"{seq:012d}-{time.time_ns():020d}-{op_id}.json"

    def _queued_seq_high_water(self) -> int:
        """The highest queue sequence any op still holds: queued, dead-lettered (a retry puts it
        back in line) or reserved by a waiting upload. Op files are read by NAME only; waiting
        records are few and parsed.

        Safe WITHOUT the append lock (the `log()` path takes none, so a deep queue's listing does
        not hold every other writer): it exists to lift `.seq` above ops that survived a machine
        crash, which were on disk before any process of this boot appended. An op another process
        adds meanwhile took its number from `.seq`, which the lock-holder reads."""
        high = 0
        for directory in (self.ops_dir, self.failed_dir):
            try:
                names = os.listdir(directory)
            except OSError:
                continue
            for name in names:
                head = name.split("-", 1)[0]
                if head.isdigit():
                    high = max(high, int(head))
        for position, *_ in self._waiting_items():
            head = str(position).split("-", 1)[0]
            if head.isdigit():
                high = max(high, int(head))
        return high

    def _stamp_producer_locked(self, op: dict, *, sync: str = SYNC_FULL) -> None:
        if self._producer_id is None:
            return
        # Sequence allocation reads the registry INSIDE the lock, not an in-memory counter: a
        # producer_id shared across processes (the CLI's per-host one) must never mint the same
        # sequence twice (parity F4).
        record = self._read_producer_locked(self._producer_id)
        sequence = int(record.get("last_sequence") or 0) + 1
        op["producer_id"] = self._producer_id
        op["producer_sequence"] = sequence
        # `sync`: the `log()` path does not fsync this (plan 1.3). A power loss can regress
        # `last_sequence` and a later op reuse a number; the sequence is this machine's own
        # accounting (gaps name it), never sent.
        self._update_producer_locked(
            self._producer_id, record, role=self._producer_role, last_sequence=sequence,
            sync=sync,
        )

    def _unstamp_producer_locked(self, op: dict, path: Path | None) -> None:
        """Give back the sequence `_stamp_producer_locked` took for an op whose file never landed
        (a Ctrl-C mid-append, #2055 lets it through; a full disk). Kept, it read as a write handed
        to the journal that nothing accounts for: `last_sequence` one above what could ever be
        delivered, with no gap (a drop then burned a SECOND number for its gap). Under the append
        lock, so no later op holds a higher number; the op loses its stamp so a retry (`_append`)
        stamps it afresh. An op whose file DID land keeps both. Never raises."""
        producer_id = op.get("producer_id")
        sequence = op.get("producer_sequence")
        if producer_id is None or sequence is None:
            return
        try:
            if path is not None and path.exists():
                return
            op.pop("producer_id", None)
            op.pop("producer_sequence", None)
            record = self._read_producer_locked(producer_id)
            if int(record.get("last_sequence") or 0) == int(sequence):
                record["last_sequence"] = int(sequence) - 1
                self._update_producer_locked(producer_id, record, sync=SYNC_NONE)
        except Exception:  # noqa: BLE001 -- best effort: the caller's error is what matters
            pass

    def _base_op(self, kind: str, run_ref: str | None) -> dict:
        session = queued_session()
        op = {
            "schema": SCHEMA,
            "op_id": uuid.uuid4().hex,
            "kind": kind,
            "run_ref": run_ref,
            "context": self.context,
            "attribution": self.attribution,
            "enqueued_at": now_iso(),
            # The session that queued it, sent at delivery whoever drains it, (a daemon command's)
            # when its work happened, and (a run process's) that a run made it: `_delivery_scope`.
            "agent_session": session,
            "attempts": 0,
            "last_error": None,
        }
        event_at = queued_event_at()
        if event_at:
            op["event_at"] = event_at
        origin = run_write_origin(session)
        if origin:
            op["write_origin"] = origin
        return op

    def _append(
        self,
        op: dict,
        *,
        before_write=None,
        unstaged_low_disk: int = 0,
        headroom_checked: bool = False,
        write_op=None,
        admitted: bool = False,
        sync: str = SYNC_FULL,
    ) -> str:
        # The ENVELOPE only: every op carrying a `body` got it from `append_http`, which scrubbed it
        # (or was handed one `Client.write` had just scrubbed). Scrubbing the whole op again was a
        # second full pass over every metric point of every `log()` (plan 1.3).
        # scanning disabled: op.update(scrub_envelope(op))
        try:
            return self._append_locked(
                op,
                before_write=before_write,
                unstaged_low_disk=unstaged_low_disk,
                headroom_checked=headroom_checked,
                write_op=write_op,
                admitted=admitted,
                sync=sync,
            )
        except OutboxFull:
            # A deliberate refusal, not a broken layout. Re-asserting the directories would not
            # create room, and retrying would double-count the capture gap already recorded.
            raise
        except OSError:
            # The layout may have gone (a tmpdir reaped, a mount that came back empty). Re-assert
            # it once and retry before giving up, so the cached-`_ensure` fast path cannot turn a
            # recoverable state into a dropped write.
            self._layout_ready = False
            self._ensure_layout()
            return self._append_locked(
                op,
                before_write=before_write,
                unstaged_low_disk=unstaged_low_disk,
                headroom_checked=headroom_checked,
                write_op=write_op,
                admitted=admitted,
                sync=sync,
            )

    def _append_locked(
        self,
        op: dict,
        *,
        before_write=None,
        unstaged_low_disk: int = 0,
        headroom_checked: bool = False,
        write_op=None,
        admitted: bool = False,
        sync: str = SYNC_FULL,
    ) -> str:
        """``sync`` is the op file's durability (`durable.write_text_atomic`). The rare paths
        (uploads, receipts, promotions) keep ``"full"`` for everything. The `log()` path passes
        ``"file"``: the op file is fsynced (by `JournalFlusher` within ~2 s by default, plan T6;
        at once under `PROBE_OUTBOX_FSYNC=each` or past its backlog cap), so a process killed
        after this returns loses nothing and a power cut at most those ~2 s, a torn op going to
        `failed/` (`torn`);
        the bookkeeping beside it (`.seq`, the producer record, status.json) is not fsynced at all.
        The drain rebuilds the status counts and the sequence is recovered from op filenames.
        That took `log()` from eight fsyncs to one (plan 1.3, D5)."""
        bookkeeping = SYNC_FULL if sync == SYNC_FULL else SYNC_NONE
        self._ensure()
        if not self._seq_recovered and self._seq_floor is None:
            self._seq_floor = self._queued_seq_high_water()  # outside the lock
        if self._pending_estimate is None:
            self._refresh_pending_estimate()
        refusal = None if admitted else self._append_headroom(check_free=not headroom_checked)
        if refusal is not None:
            # Refuse the NEW write rather than evicting an old one: dropping an op under a
            # concurrent drain is a race, and the oldest entries are what a barrier waits on. The
            # loss is recorded as a numbered gap in the producer registry, a hole in the record
            # rather than silence. A best-effort op (hardware) is not the user's data: its loss
            # is neither.
            refused = OutboxFull(refusal)
            if not op.get("best_effort"):
                self.note_capture_gap(refusal)
                # The client's drop handler records gaps too; once is enough.
                refused.gap_recorded = True
                if not self._headroom_warned:
                    self._headroom_warned = True
                    _diagnostics.warn(f"probe: dropping queued writes — {refusal}")
            raise refused
        with file_lock(self.append_lock):
            # A waiting upload was stamped when it was QUEUED, by the producer that queued it; its
            # promoter is someone else.
            stamping = "producer_id" not in op
            path = None
            flusher, deferred = None, False
            try:
                if stamping:
                    self._stamp_producer_locked(op, sync=bookkeeping)
                if before_write is not None:
                    # Runs INSIDE the lock, before the op file exists: append_upload publishes its
                    # staged blob atomically with the op that references it, so gc_blobs (same lock)
                    # never sees the blob as unreferenced garbage.
                    before_write()
                path = self.ops_dir / (
                    op.get("queue_filename") or self._op_filename(op["op_id"], sync=bookkeeping)
                )
                if write_op is not None:
                    write_op(path, op)
                elif sync == SYNC_FULL:
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                else:
                    # The `log()` path's one fsync goes to the flusher (plan T6, D1 = A) unless
                    # `PROBE_OUTBOX_FSYNC=each`, its thread died or it is behind: a process death
                    # loses nothing either way, a power cut at most the last ~2 s.
                    flusher = get_journal_flusher() if sync == SYNC_FILE else None
                    deferred = flusher is not None and flusher.can_defer_fsync()
                    # Compact: `indent=` takes json's pure-Python encoder.
                    write_text_atomic(
                        path,
                        json.dumps(op, separators=(",", ":")) + "\n",
                        mode=0o600,
                        sync=SYNC_NONE if deferred else sync,
                    )
            except BaseException:
                if stamping:
                    self._unstamp_producer_locked(op, path)
                raise
            if deferred:
                # Outside the `try`: the op is on disk and queued, so nothing here may count it
                # dropped (review of #3785, C5); `record` never raises.
                flusher.record(path)
            # The count this status write just stored: status.json's previous value (which another
            # process's drain may have lowered) plus one. The op file is ON DISK here: the write is
            # queued whatever the bookkeeping does next. A volume full but for the few KB the op
            # needed fails this status rewrite with ENOSPC; raising made the caller count a drop
            # for a write the drain later delivered, made `_append` queue the op a second time,
            # and left the run's lane non-empty so every later write was dropped instead of sent
            # directly (lane S soak, 0.195.0). The drain rebuilds the counts.
            try:
                self._pending_estimate = self._write_status_locked(
                    unstaged_low_disk=unstaged_low_disk,
                    recount=False,
                    pending_delta=1,
                    enqueued_at=op.get("enqueued_at"),
                    pending_bytes_delta=int((op.get("upload") or {}).get("size_bytes") or 0),
                    sync=bookkeeping,
                )
            except OSError:
                self._pending_estimate = (self._pending_estimate or 0) + 1
        return op["op_id"]

    def append_http(
        self,
        method: str,
        path: str,
        body: dict | None,
        *,
        run_ref: str | None = None,
        blocking: bool = True,
        correlation: str | None = None,
        validation_error: str | None = None,
        best_effort: bool = False,
        admitted: bool = False,
        tag: str | None = None,
        _prepared: bool = False,
    ) -> str:
        """Journal one HTTP op; returns its op id.

        ``tag``: what the op is, for a later reader (`"late_hash"`); never sent. ``_prepared``: the
        body was normalized, NUL-checked and scrubbed already (`Client.write`). ``admitted``: skips the
        cap and the free-space floor (a run's terminal status). ``best_effort``: not the user's data, so
        a refusal for room drops it quietly. ``blocking=False``: does not hold the run's close."""
        # An experiment's child write is journaled by its EXPERIMENT, never the project it sat in
        # when queued: the drain places it (`_placed`), so a move between the two cannot
        # dead-letter it, and its correlation digest is the same whichever project answered.
        path = routes.unplaced_experiment_path(path)

        if not _prepared:
            body = unstorable.normalize_json(body)
            # The same door as `Client.write` (review of #2053): the hardware rail and other
            # direct appends reach the queue here.
            body, unstorable_reasons = unstorable.drop_unstorable_points(method, path, body)
            if unstorable_reasons and not body.get("points"):
                return ""
            try:
                unstorable.validate_nuls(body, path=path, method=method)
            except errors.ValidationError as exc:
                validation_error = str(exc)
            # scanning disabled: body = scrub_body(body)
        if validation_error is not None and correlation is not None:
            raise errors.ValidationError(validation_error, status=422)
        if correlation is not None:
            if not self.receipt_enabled:
                return self.for_receipts(
                    self.dir, context=self.context, attribution=self.attribution
                ).append_http(
                    method, path, body, run_ref=run_ref, blocking=blocking, correlation=correlation
                )
            if (
                method.upper() != "POST"
                or not body
                or body.get("is_reference") is not True
                or not re.fullmatch(
                    r"/v1/(runs|experiments|projects)/[^/]+(/experiments/[^/]+)?/artifacts", path
                )
            ):
                raise ValueError("correlated HTTP operations must create an artifact reference")
            self._receipt_dirs()
            key = self._correlation_key(correlation)
            request = {
                "kind": "http",
                "method": method,
                "path": path,
                "body": body,
                "context": self.context,
                "attribution": self.attribution,
            }
            with self._correlation_lock(key):
                prior = self._replay_correlation(correlation, request)
                if prior is not None:
                    return prior["op_id"]
                op = self._base_op("http", run_ref or routes.run_ref_of(path))
                op.update({"method": method, "path": path, "body": body})
                return self._publish_receipt_op(correlation, request, op)["op_id"]
        if self.receipt_enabled:
            raise ValueError("delivery-v1 requires an explicit correlation")
        # An unknown kind makes older drainers refuse this too; a new field on kind=http would be
        # ignored and could upload a scrubbed identity alias.
        kind = "rejected_http" if validation_error is not None else "http"
        op = self._base_op(kind, run_ref or routes.run_ref_of(path))
        op.update({"method": method, "path": path, "body": body})
        if validation_error is not None:
            op["validation_error"] = validation_error
        if not blocking:
            op["blocking"] = False
        if best_effort:
            op["best_effort"] = True
        if tag is not None:
            op["tag"] = tag
        if not admitted and validation_error is None:
            # The writer's collect window (plan T2): a drainer may hold this run's telemetry
            # until then and send it in one POST. Optional on disk: older drainers send at once.
            stamp_send_after(op, cap=self.window_cap)
        # The `log()` path: one fsync, of the op file (`_append_locked`). An admitted op (a run's
        # terminal status, once per run) keeps them all.
        return self._append(op, admitted=admitted, sync=SYNC_FULL if admitted else SYNC_FILE)

    def catalog_manifest_path(self, op_id: str) -> Path:
        """Where a queued catalog manifest's gzip bytes wait (`CATALOG_MANIFEST`)."""
        return self.dir / "catalog" / f"{op_id}.json.gz"

    def append_catalog_manifest(self, digest: str, gz: bytes) -> str:
        """Queue `PUT /v1/catalog/manifests/{digest}` with ``gz`` as its body. The bytes are
        written (and synced) before the op naming them, so no op points at a missing file.
        Returns the op id."""
        if not re.fullmatch(r"[0-9a-f]{64}", digest or ""):
            raise errors.ValidationError(f"not a manifest digest: {digest!r}", status=422)
        op = self._base_op(CATALOG_MANIFEST, None)
        op["digest"] = digest
        path = self.catalog_manifest_path(op["op_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(bytes(gz))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        except BaseException:
            Path(temporary).unlink(missing_ok=True)
            raise
        fsync_directory(path.parent)
        try:
            from .. import outbox as outbox_worker

            outbox_worker.ready_for(CATALOG_MANIFEST, str(self.dir))
        except Exception:  # noqa: BLE001 -- a nudge, never a condition
            pass
        return self._append(op)

    # -- legacy spool import -------------------------------------------------
    def import_spool(self, spool=None) -> int:
        """Fold a surviving pre-journal spool into the journal, in order. The spool's two-file
        protocol is honored by reading inflight first, the order ``Spool.flush`` would replay.
        Records import with the CURRENT context pin (the spool never recorded one) and the spool
        files are removed, so this runs once per machine, ever.
        """
        from ..spool import Spool

        spool = spool or Spool()
        if not (spool.file.exists() or spool.inflight_file.exists()):
            return 0
        if self.context is None:
            # Stamp the records with the context current AT IMPORT TIME (red team: a null pin
            # resolves at drain time, so a context switch in between would deliver the old spool's
            # writes to a different tenant than the one that captured them).
            from ...settings.settings import current_context_name, resolve

            self.context = {
                "name": current_context_name() or None,
                "base_url": resolve().base_url,
            }
        imported = 0
        with file_lock(spool.lock_file):
            # NOT spool.pending(): it takes the same lock we hold and flock is not reentrant across
            # file handles.
            records = spool._read_records(spool.inflight_file) + spool._read_records(
                spool.file
            )
            for record in records:
                self.append_http(record.method, record.path, record.json_body)
                imported += 1
            spool.file.unlink(missing_ok=True)
            spool.inflight_file.unlink(missing_ok=True)
        return imported
from probe.sdk.delivery.ops.ops import CATALOG_MANIFEST  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.headroom import OutboxFull  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk import routes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.flusher import get_journal_flusher  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.window import stamp_send_after  # noqa: E402 -- pieces need each other; the front door loads this one first
