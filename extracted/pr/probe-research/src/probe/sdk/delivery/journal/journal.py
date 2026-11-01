"""The durable outbox journal: ONE ordered queue for every deferred write (eng review
2026-07-29, T1-C). Every async operation (metric batch, span, note, reference-add, artifact
upload, run end) is one op file in `<dir>/ops/<time_ns>-<op_id>.json` (atomic write, FIFO by
filename); file-bearing ops reference a content-addressed `blobs/` store. Dirs 0o700, files
0o600 (research data, maybe on shared storage).

Ops never carry credentials: they pin a context NAME + base_url (5A) and the drain resolves
tokens fresh via ``config.resolve``. Importing this module must stay httpx-free (enqueue runs
beside training loops); the network stack loads only inside :func:`drain`.

Failure policy (7A + T2-A): permanent rejection (4xx except 408/429/auth) -> op moves to
failed/, queue keeps flowing (`retry_failed` puts it back); transient (network, 5xx, 408, 429,
unexpected) -> drain stops in place and retries with backoff; 401/403 -> drain halts as a
CREDENTIAL-level blocker, ops stay queued untouched; 409 with ``existing_id`` -> idempotent
replay already landed, counted delivered.

DESIGN.md holds the directory layout, the op schema (``probe.outbox/1``) and the policy in full.
"""

from __future__ import annotations
import json
import hashlib
import logging
import os
import re
import shutil
import time
import uuid
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Any, Callable

from ...._shared import oscompat
from ... import errors
from ....foundation.safe_warn import safe_warn as _diagnostics
from ....foundation.durable.durable import (
    SYNC_FILE,
    SYNC_FULL,
    SYNC_NONE,
    file_lock,
    fsync_directory,
    now_iso,
    write_text_atomic)
from ...agent_session import queued_event_at, queued_session, run_write_origin
from ...artifact.hashing import fingerprint
# At module load, not in the drain: a module first imported while a script exits clears its
# pending KeyboardInterrupt (tests/test_ctrlc_exit_code.py).
from ...values import unstorable
from ...secret_gate import (
    CredentialBlocked,
    check_upload,
    read_source,
    # scanning disabled: redact_quick_bytes,
    refuse_rewrite,
    # scanning disabled: safe_snapshot_file as snapshot_file,
    InspectionResult,
    strict_policy)
from probe.sdk.delivery.journal.failures.pause import (
    DEFAULT_PAUSE_HOURS,
    PAUSE_SCHEMA,
    _pause_in_effect,
    _pause_marker,
    _unlink_pause,
)
from probe.sdk.delivery.journal.receipts.index import RECEIPT_COMPACTION_BATCH, RECEIPT_INDEX_VERSION
# scanning disabled: from .redaction import default_scrub, scrub_string, scrub_text
# scanning disabled: from .stamp_scrub import scrub_body, scrub_envelope, scrub_op


def snapshot_file(source, destination, *, verbatim: bool = False) -> str:
    """`secret_gate.safe_snapshot_file` with its redaction pass removed (scanning disabled):
    copy `source` to `destination` byte for byte and return the sha256 of the bytes read."""
    del verbatim  # only steered the redaction pass
    raw = read_source(source)
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return hashlib.sha256(raw).hexdigest()

log = logging.getLogger(__name__)


class Journal:
    def __init__(
        self,
        directory: str | Path | None = None,
        *,
        context: dict | None = None,
        attribution: str = "ambient",
    ):
        self.dir = Path(directory).expanduser() if directory else default_dir()
        self.ops_dir = self.dir / "ops"
        self.failed_dir = self.dir / "failed"
        self.blobs_dir = self.dir / "blobs"
        #: Uploads queued before their credential scan (see `promote_waiting`). No earlier
        #: release reads it, so an older drainer sharing this journal never picks up
        #: unscanned bytes.
        self.waiting_dir = self.dir / "waiting"
        #: Held by whoever is promoting (a promote-only worker or a drain's promotion pass), so
        #: a kick does not fork another promoter; separate from the drain lease an OLDER worker
        #: may hold.
        self.promote_lease = self.dir / ".promote.lock"
        self.status_file = self.dir / "status.json"
        self.paused_file = self.dir / "paused"
        self.append_lock = self.dir / ".append.lock"
        self.drain_lock = self.dir / ".drain.lock"
        #: Held shared by a run's close while it waits for the drain lock, so a
        #: pass gives the lock up at its next op (`_DrainHold`, #3618).
        self.drain_want = self.dir / ".drain.want"
        #: One flock per run slot, held while a pass sends that run's upload
        #: with the drain lock let go (`_DrainHold`, #3618).
        self.run_locks_dir = self.dir / ".run-locks"
        #: Present while a takeover barrier (SDK reliability 2.3) holds queued status ops aside in
        #: `failed/`: the cheap test telling every drain pass and new client whether to look for
        #: abandoned holds.
        self.holds_marker = self.dir / "takeover-holds"
        self.producers_dir = self.dir / "producers"
        #: default {"name", "base_url"} pin stamped onto appended ops.
        self.context = context
        if attribution not in ("ambient", "backfill"):
            raise ValueError("invalid outbox attribution")
        self.attribution = attribution
        self.receipt_enabled = self.dir.name == DELIVERY_NAMESPACE
        self.intents_dir = self.dir / "intents"
        self.receipts_dir = self.dir / "receipts"
        self.receipt_index = self.dir / "receipts-v1.sqlite3"
        self.correlation_locks = self.dir / "correlation-stripes"
        self.recovery_file = self.dir / ".recover"
        #: parity F4: set via register_producer; None = unstamped ops.
        self._producer_id: str | None = None
        self._producer_role: str | None = None
        #: Backpressure state for `_append_headroom`. `_pending_estimate` is the pending count
        #: this process last saw in status.json: read on the first append, then taken from
        #: every status write the append makes (so another process's drain lowers it free), and
        #: re-read before any refusal. A drain pass rewrites status.json from a real count only
        #: when it ENDS, so a write that would still be refused also counts the queue directory,
        #: at most once per `_RECOUNT_EVERY_SECONDS`.
        #:
        #: It was read ONCE and only incremented: the detached worker delivers in another
        #: process, so a long-lived process refused every write after its MAX_PENDING_OPS-th
        #: append while the queue sat empty (plan 0.1: live, cap 150, 150 of 450 writes arrived).
        self._pending_estimate: int | None = None
        self._recounted_at = float("-inf")
        self._appends_since_statvfs = _STATVFS_EVERY
        self._last_free_ok = True
        self._headroom_warned = False
        #: The queue's sequence high-water mark, taken once per Journal before its first
        #: sequence (see `_op_filename`); None until then, and again once applied.
        self._seq_floor: int | None = None
        self._seq_recovered = False
        #: The sibling namespace's pending count, re-read with the free-space
        #: sample rather than on every append (plan 1.3); `None` = not yet read.
        self._sibling_pending: int | None = None
        self._appends_since_sibling = 0
        #: This queue's op-count ceiling: None is `MAX_PENDING_OPS`, 0 is none. An OFFLINE run's
        #: queue (plan 2.12) sets 0: nothing drains it until `probe sync`, so a ceiling meant to
        #: catch a stalled drainer would drop every point after the 500,000th and the close with
        #: them. The free-space floor still applies.
        self.op_ceiling: int | None = None

    @classmethod
    def for_receipts(cls, directory=None, *, context=None, attribution="backfill") -> Journal:
        """New operations live outside every pre-receipt worker's ops directory."""
        base = Path(directory).expanduser() if directory else default_dir()
        if base.name != DELIVERY_NAMESPACE:
            base = base / DELIVERY_NAMESPACE
        return cls(base, context=context, attribution=attribution)

    @classmethod
    def for_credential(
        cls, directory=None, fingerprint: str = "", *, context=None, attribution="ambient"
    ) -> Journal:
        """The queue of one credential (see `CREDENTIAL_NAMESPACE`)."""
        base = Path(directory).expanduser() if directory else default_dir()
        if not fingerprint or not re.fullmatch(r"[0-9a-f]{16}", fingerprint):
            raise ValueError("a credential queue needs a 16-hex fingerprint")
        return cls(base / CREDENTIAL_NAMESPACE / fingerprint, context=context, attribution=attribution)

    @property
    def outbox_root(self) -> Path:
        """The outbox directory this queue lives in (itself, for the root)."""
        path = self.dir
        if path.name == DELIVERY_NAMESPACE:
            path = path.parent
        if path.parent.name == CREDENTIAL_NAMESPACE:
            path = path.parent.parent
        return path

    def namespaces(self) -> list[Journal]:
        """This queue and the queues under it, each once: the root, its receipt namespace, and
        every credential queue with its own receipt namespace."""
        if self.receipt_enabled:
            return [self]
        out = [self]
        child = self.for_receipts(self.dir, context=self.context, attribution=self.attribution)
        if child.dir.exists():
            out.append(child)
        if self.dir.parent.name != CREDENTIAL_NAMESPACE:
            for path in _credential_queue_dirs(self.dir):
                queue = Journal(path, context=self.context, attribution=self.attribution)
                out.append(queue)
                receipts = self.for_receipts(path, context=self.context, attribution=self.attribution)
                if receipts.dir.exists():
                    out.append(receipts)
        return out

    @staticmethod
    def _correlation_key(correlation: str) -> str:
        if not isinstance(correlation, str) or not correlation or len(correlation) > 4096:
            raise ValueError("correlation must be a nonempty string of at most 4096 characters")
        return hashlib.sha256(correlation.encode()).hexdigest()

    @staticmethod
    def _request_digest(request: dict) -> str:
        """The request's identity for correlation replays. Leaves out the credential stamp
        (#2035): the same request re-queued after a re-login is the same request and must replay,
        not raise.

        So a correlation names ONE request whoever queues it: the same correlation, anchor and
        body queued under another credential (same team; another team's anchor id differs)
        replays the first op, which goes out with the credential that queued it first. Callers
        mint correlations per request (backfill's are content-addressed), so two people never
        share one by accident (#2041 re-review, decided)."""
        context = request.get("context")
        if isinstance(context, dict) and "principal" in context:
            request = {**request, "context": {k: v for k, v in context.items() if k != "principal"}}
        return hashlib.sha256(
            json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()

    @staticmethod
    def _read_record(path: Path) -> dict | None:
        try:
            data = json.loads(path.read_text())
        except FileNotFoundError:
            return None
        if not isinstance(data, dict) or data.get("schema") != DELIVERY_SCHEMA:
            raise ValueError(f"invalid delivery record: {path.name}")
        return data

    def receipt(self, correlation: str) -> dict | None:
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).receipt(correlation)
        found = self._own_receipt(correlation)
        if found is None and self.dir.parent.parent.name == CREDENTIAL_NAMESPACE:
            # A credential queue's receipts start empty; what was delivered before the stamp
            # (#2035) is recorded in the root's. Read-only.
            legacy = Journal(self.outbox_root / DELIVERY_NAMESPACE)
            if legacy.dir.exists():
                return legacy._own_receipt(correlation)
        return found

    def _own_receipt(self, correlation: str) -> dict | None:
        key = self._correlation_key(correlation)
        # JSON first is essential: compaction commits the index before unlink, so a reader that
        # misses the file cannot miss the committed row.
        legacy = self._read_record(self.receipts_dir / f"{key}.json")
        if legacy is not None:
            return legacy
        if not self.receipt_index.exists():
            return None
        with closing(sqlite3.connect(self.receipt_index.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version == 0 and not conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone():
                return None  # interrupted before the first schema transaction
            if version != RECEIPT_INDEX_VERSION:
                raise ValueError("unsupported terminal receipt index version")
            row = conn.execute("SELECT payload FROM receipts WHERE key=?", (key,)).fetchone()
        result = json.loads(row[0]) if row else None
        if result is not None and (result.get("schema") != DELIVERY_SCHEMA
                                   or result.get("correlation") != correlation):
            raise ValueError("invalid indexed delivery receipt")
        return result

    @contextmanager
    def _correlation_lock(self, key: str, *, blocking: bool = True):
        """Stable stripes fence both writers and legacy-lock retirement. The 256 stripe inodes
        are NEVER unlinked. A waiter acquires its stripe BEFORE opening any legacy per-key
        inode; cleanup holds that same stripe, so no new writer can retain a deleted lock inode
        while another opens a replacement. Active legacy locks are retained on a nonblocking
        cleanup attempt. Pre-index delivery-v1 binaries must be upgraded before compaction;
        production pre-receipt workers never enter this namespace.
        """
        self.correlation_locks.mkdir(parents=True, exist_ok=True, mode=0o700)
        flags = oscompat.LOCK_EX | (0 if blocking else oscompat.LOCK_NB)
        with (self.correlation_locks / f"{key[:2]}.lock").open("a+") as stripe:
            oscompat.flock(stripe, flags)
            legacy = None
            try:
                try:
                    legacy = (self.dir / "correlations" / f"{key}.lock").open("r+")
                except FileNotFoundError:
                    pass
                if legacy is not None:
                    oscompat.flock(legacy, flags)
                yield
            finally:
                if legacy is not None:
                    legacy.close()
                oscompat.flock(stripe, oscompat.LOCK_UN)

    @staticmethod
    def _commit_receipt_index(conn) -> None:
        """The terminal durability boundary; operation removal happens later."""
        conn.commit()

    def _index_receipts(self, receipts: list[dict], *, timeout: float = 5.0) -> None:
        """Commit immutable identities in one indexed, FULL-synchronous transaction."""
        self._receipt_dirs()
        # Reserve a private inode before sqlite opens it (its default mode is 644).
        descriptor = os.open(self.receipt_index, os.O_CREAT | os.O_RDWR, 0o600)
        os.close(descriptor)
        with closing(sqlite3.connect(self.receipt_index, timeout=timeout)) as conn, conn:
            conn.execute("PRAGMA synchronous=FULL")
            conn.execute("BEGIN IMMEDIATE")
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, RECEIPT_INDEX_VERSION):
                raise ValueError("unsupported terminal receipt index version")
            conn.execute("CREATE TABLE IF NOT EXISTS receipts (key TEXT PRIMARY KEY, "
                         "payload TEXT NOT NULL, cleanup INTEGER NOT NULL DEFAULT 1) WITHOUT ROWID")
            conn.execute("CREATE INDEX IF NOT EXISTS receipt_cleanup ON receipts(cleanup) WHERE cleanup=1")
            conn.execute(f"PRAGMA user_version={RECEIPT_INDEX_VERSION}")
            for receipt in receipts:
                if (receipt.get("schema") != DELIVERY_SCHEMA or receipt.get("state") != "delivered"
                        or receipt.get("status") != "complete" or not receipt.get("artifact_id")
                        or not receipt.get("request_digest")):
                    raise ValueError("cannot compact an unverified terminal receipt")
                key = self._correlation_key(receipt["correlation"])
                payload = json.dumps(receipt, separators=(",", ":"), sort_keys=True)
                previous = conn.execute("SELECT payload FROM receipts WHERE key=?", (key,)).fetchone()
                if previous and json.loads(previous[0]) != receipt:
                    raise ValueError("terminal receipt identity is immutable")
                conn.execute("INSERT OR IGNORE INTO receipts(key,payload) VALUES (?,?)", (key, payload))
                conn.execute("UPDATE receipts SET cleanup=1 WHERE key=?", (key,))
            self._commit_receipt_index(conn)
        fsync_directory(self.dir)

    def compact_receipts(self, *, max_records: int = RECEIPT_COMPACTION_BATCH,
                         max_seconds: float = 1.0) -> dict:
        """Bounded explicit checkpoint; preserves all terminal identities forever. Imports legacy
        JSON into the index before deleting any copy. Cleanup is indexed, so a crash after the
        index commit or JSON unlink resumes without scanning historical identities. Does not
        VACUUM or erase receipts. One filesystem operation/SQLite commit may overrun the time
        budget; lock waits are nonblocking and DB admission uses that budget.
        """
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).compact_receipts(max_records=max_records, max_seconds=max_seconds)
        if not 1 <= max_records <= 4096 or not 0 < max_seconds <= 10:
            raise ValueError("receipt compaction requires 1..4096 records and 0 < seconds <= 10")
        deadline = time.monotonic() + max_seconds
        report = {"indexed": 0, "json_removed": 0, "locks_removed": 0,
                  "compacted": 0, "deferred": 0, "remaining": False}
        receipts = []
        if self.receipts_dir.exists():
            with os.scandir(self.receipts_dir) as entries:
                for entry in entries:
                    if len(receipts) >= max_records or time.monotonic() >= deadline:
                        break
                    if entry.name.endswith(".json") and entry.is_file(follow_symlinks=False):
                        receipt = self._read_record(Path(entry.path))
                        if receipt is not None:
                            if entry.name != self._correlation_key(receipt["correlation"]) + ".json":
                                raise ValueError("legacy receipt name differs from correlation")
                            receipts.append(receipt)
        if receipts:
            self._index_receipts(receipts, timeout=max(0.001, deadline - time.monotonic()))
            report["indexed"] = len(receipts)
        if not self.receipt_index.exists():
            return report
        with closing(sqlite3.connect(self.receipt_index, timeout=max(0.001, deadline - time.monotonic()))) as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version == 0 and not conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone():
                return report
            if version != RECEIPT_INDEX_VERSION:
                raise ValueError("unsupported terminal receipt index version")
            keys = conn.execute("SELECT key FROM receipts WHERE cleanup=1 LIMIT ?", (max_records,)).fetchall()
            cleaned = []
            for (key,) in keys:
                if time.monotonic() >= deadline:
                    break
                try:
                    with self._correlation_lock(key, blocking=False):
                        for directory, suffix, field in (
                            (self.receipts_dir, ".json", "json_removed"),
                            (self.dir / "correlations", ".lock", "locks_removed"),
                        ):
                            path = directory / f"{key}{suffix}"
                            if path.exists():
                                path.unlink()
                                fsync_directory(directory)
                                report[field] += 1
                        cleaned.append((key,))
                except BlockingIOError:
                    report["deferred"] += 1
            if cleaned:
                conn.executemany("UPDATE receipts SET cleanup=0 WHERE key=?", cleaned)
                conn.commit()
            report["compacted"] = len(cleaned)
            report["remaining"] = bool(conn.execute("SELECT 1 FROM receipts WHERE cleanup=1 LIMIT 1").fetchone())
        if self.receipts_dir.exists():
            with os.scandir(self.receipts_dir) as entries:
                report["remaining"] |= next(entries, None) is not None
        return report

    def delivery_state(self, correlation: str) -> dict:
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).delivery_state(correlation)
        receipt = self.receipt(correlation)
        if receipt is not None:
            return receipt
        intent = self._read_record(self.intents_dir / f"{self._correlation_key(correlation)}.json")
        if intent is None:
            return {"state": "unknown", "correlation": correlation}
        op = intent["op"]
        filename = op["queue_filename"]
        failed = self.failed_dir / filename
        discarded = self.dir / "discarded" / filename
        state = (
            "discarded"
            if discarded.exists()
            else (
                "failed"
                if failed.exists()
                else ("queued" if (self.ops_dir / filename).exists() else "pending")
            )
        )
        error = None
        if failed.exists():
            error = json.loads(failed.read_text()).get("last_error")
        return {
            "state": state,
            "correlation": correlation,
            "op_id": op["op_id"],
            "blob": (op.get("upload") or {}).get("blob"),
            "size_bytes": (op.get("upload") or {}).get("size_bytes"),
            "staged": bool((op.get("upload") or {}).get("staged")),
            # The name the request froze, as a receipt reports the delivered one: a caller can tell
            # a request that went out under a name it never meant from one still in flight under
            # the right name.
            "name": (op.get("upload") or {}).get("name") or (op.get("body") or {}).get("name"),
            "error": error,
        }

    def _receipt_dirs(self) -> None:
        self._ensure()
        for path in (self.intents_dir, self.receipts_dir, self.dir / "correlations"):
            path.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _replay_correlation(self, correlation: str, request: dict) -> dict | None:
        digest = self._request_digest(request)
        done = self.receipt(correlation)
        key = self._correlation_key(correlation)
        intent = self._read_record(self.intents_dir / f"{key}.json")
        previous = done or intent
        if previous is None:
            return None
        if previous["request_digest"] != digest:
            raise ValueError("correlation already belongs to a different immutable request")
        if done is not None:
            return done
        op = intent["op"]
        filename = op["queue_filename"]
        if not any(
            (directory / filename).exists()
            for directory in (
                self.ops_dir,
                self.failed_dir,
                self.dir / "discarded",
            )
        ):
            # The intent committed but the operation did not. Its staged bytes,
            # not the current source file, are the only valid retry input.
            blob = self.blob_path(op)
            if op["kind"] == "upload" and (blob is None or not blob.is_file()):
                raise OSError("receipt upload's immutable staged bytes are missing")
            self._restore_intent_op(op)
        return self.delivery_state(correlation)

    def _restore_intent_op(self, op: dict) -> None:
        # This request was admitted before the crash. Restoring its small queue record must not
        # compete for admission with new snapshots: its existing bytes may be what draining needs
        # to release under disk pressure.
        with file_lock(self.append_lock):
            path = self.ops_dir / op["queue_filename"]
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
            self._write_status_locked()

    def _publish_receipt_op(self, correlation: str, request: dict, op: dict, publish=None) -> dict:
        key = self._correlation_key(correlation)
        op.update(
            {
                "schema": DELIVERY_SCHEMA,
                "correlation": correlation,
                "request_digest": self._request_digest(request),
            }
        )

        def before_write():
            if publish is not None:
                publish()
            if "queue_filename" not in op:
                op["queue_filename"] = self._op_filename(op["op_id"])
            # Marker precedes intent: restart must see even an append interrupted before
            # status.json or the op file exists.
            write_text_atomic(self.recovery_file, op["op_id"] + "\n", mode=0o600)
            write_text_atomic(
                self.intents_dir / f"{key}.json",
                json.dumps(
                    {
                        "schema": DELIVERY_SCHEMA,
                        "correlation": correlation,
                        "request_digest": op["request_digest"],
                        "op": op,
                    }
                )
                + "\n",
                mode=0o600,
            )

        self._append(op, before_write=before_write)
        return self.delivery_state(correlation)

    def _receipt_upload(
        self, *, correlation: str, expected_content_hash: str | None, **fields
    ) -> dict:
        self._receipt_dirs()
        key = self._correlation_key(correlation)
        fields["src_path"] = os.path.abspath(fields["src_path"])
        request = {
            "kind": "upload",
            # `notes` stays in the DIGESTED request as an always-empty slot: a correlation recorded
            # before files stopped carrying notes was digested with `"notes": null`, and
            # re-enqueueing it must replay, not fail as "a different immutable request". The
            # queued upload (`fields`) carries none.
            "fields": {**fields, "notes": None},
            "context": self.context,
            "attribution": self.attribution,
            "expected_content_hash": expected_content_hash,
        }
        with self._correlation_lock(key):
            existing = self._replay_correlation(correlation, request)
            if existing is not None:
                return existing
            # A retry refers to the admitted immutable snapshot/receipt, not today's source.
            # Inspect only a genuinely new upload request.
            check_upload(fields["src_path"])
            self._refresh_pending_estimate()
            refusal = self._append_headroom() or self._staging_headroom(fields["src_path"])
            if refusal:
                raise OutboxFull(refusal)
            op = self._base_op("upload", fields.get("run_ref"))
            staging = self.blobs_dir / f".staging-{op['op_id']}"
            source = Path(fields["src_path"])
            try:
                before = source.stat()
                if not source.is_file():
                    raise ValueError("receipt upload source is not a regular file")
                source_digest = snapshot_file(source, staging)
                digest, size = fingerprint(str(staging))
                after = source.stat()

                def observed(stat):
                    return (
                        stat.st_dev,
                        stat.st_ino,
                        stat.st_size,
                        stat.st_mtime_ns,
                        stat.st_ctime_ns,
                    )

                if observed(before) != observed(after):
                    raise ValueError("source changed while its snapshot was staged")
                if expected_content_hash is not None and expected_content_hash not in (
                    digest,
                    source_digest,
                ):
                    # The caller's hash describes the file it censused and the snapshot is
                    # redacted, so the two legitimately differ. A backfill whose approved file
                    # carried a credential failed delivery permanently here; matching EITHER keeps
                    # the tamper check while letting a redacted upload through.
                    raise ValueError("staged bytes do not match expected_content_hash")
                upload = {k: v for k, v in fields.items() if k != "run_ref"}
                upload.update(
                    {"blob": digest, "size_bytes": size, "staged": True, "unstaged_reason": None}
                )
                if expected_content_hash is not None:
                    # The source this snapshot was read from, taken from that same read. The receipt
                    # carries it, so a caller holding the source's hash can tell its own file,
                    # redacted, from other bytes; a receipt without it predates the stamp.
                    upload["source_content_hash"] = source_digest
                op["upload"] = upload

                def publish():
                    final = self.blobs_dir / digest
                    if final.exists():
                        staging.unlink(missing_ok=True)
                    else:
                        os.replace(staging, final)
                    fsync_directory(self.blobs_dir)

                return self._publish_receipt_op(correlation, request, op, publish)
            finally:
                staging.unlink(missing_ok=True)

    def recover_intents(self) -> int:
        """Repair interrupted local appends without rereading a live source."""
        if not self.receipt_enabled or not self.intents_dir.exists():
            return 0
        try:
            generation = self.recovery_file.read_text()
        except FileNotFoundError:
            generation = None
        recovered = 0
        for path in sorted(self.intents_dir.glob("*.json")):
            intent = self._read_record(path)
            if intent is None:
                continue
            correlation = intent["correlation"]
            with self._correlation_lock(self._correlation_key(correlation)):
                if self.receipt(correlation) is not None:
                    path.unlink(missing_ok=True)
                    continue
                op = intent["op"]
                filename = op["queue_filename"]
                if not any(
                    (directory / filename).exists()
                    for directory in (
                        self.ops_dir,
                        self.failed_dir,
                        self.dir / "discarded",
                    )
                ):
                    self._restore_intent_op(op)
                    recovered += 1
        with file_lock(self.append_lock):
            try:
                current_generation = self.recovery_file.read_text()
            except FileNotFoundError:
                current_generation = None
            # A newer append may have died after our directory snapshot. Its marker belongs to
            # the next pass, even when status still says zero.
            if current_generation == generation:
                self.recovery_file.unlink(missing_ok=True)
                fsync_directory(self.dir)
        return recovered

    def _save_delivery_receipt(self, op: dict, result: Any) -> None:
        if not op.get("correlation"):
            return
        if not isinstance(result, dict) and hasattr(result, "json"):
            result = result.json()
        if (
            not isinstance(result, dict)
            or not result.get("id")
            or result.get("status") != "complete"
        ):
            raise errors.TransportError("delivery returned no complete artifact identity")
        upload = op.get("upload") or {}
        body = op.get("body") or {}
        reference = op["kind"] == "http"
        if bool(result.get("is_reference")) != reference or not result.get("uri"):
            raise errors.TransportError("delivery returned no readable artifact or reference URI")
        if result.get("name") != (upload.get("name") or body.get("name")):
            raise errors.TransportError("delivered artifact name differs from requested name")
        if reference and result["uri"] != body["uri"]:
            raise errors.TransportError("delivered reference URI differs from requested URI")
        if upload and (
            result.get("content_hash") != upload["blob"]
            or result.get("size_bytes") != upload["size_bytes"]
        ):
            raise errors.TransportError(
                "delivered artifact digest or size differs from staged bytes"
            )
        for attribute in ("content_hash", "size_bytes"):
            if (
                reference
                and body.get(attribute) is not None
                and result.get(attribute) != body[attribute]
            ):
                raise errors.TransportError(
                    f"delivered reference {attribute} differs from requested value"
                )
        correlation = op["correlation"]
        receipt = {
            "schema": DELIVERY_SCHEMA,
            "correlation": correlation,
            "op_id": op["op_id"],
            "request_digest": op["request_digest"],
            "state": "delivered",
            "status": "complete",
            "artifact_id": str(result["id"]),
            "content_hash": result.get("content_hash"),
            "size_bytes": result.get("size_bytes"),
            "is_reference": reference,
            "blob": result.get("content_hash") if not reference else None,
            "staged": not reference,
            "mode": "reference" if reference else "upload",
            "readable": not reference,
            "uri": result["uri"],
            "name": result.get("name") or upload.get("name") or body.get("name"),
            "anchor": upload.get("anchor") or op.get("path", "").split("/")[2].removesuffix("s"),
            "anchor_id": upload.get("anchor_id") or op.get("path", "").split("/")[3],
            "delivered_at": now_iso(),
        }
        if upload.get("source_content_hash"):
            receipt["source_content_hash"] = upload["source_content_hash"]
        key = self._correlation_key(correlation)
        with self._correlation_lock(key):
            existing = self.receipt(correlation)
            if existing is None:
                self._index_receipts([receipt])
            elif existing["request_digest"] != op["request_digest"]:
                raise ValueError("terminal receipt belongs to a different request")
            (self.intents_dir / f"{key}.json").unlink(missing_ok=True)
            fsync_directory(self.intents_dir)

    # -- layout -------------------------------------------------------------
    def usable(self) -> str | None:
        """None when this queue can take appends, else why it cannot (plan 1.5). Checked once,
        when a `Client` builds its journal, WITHOUT creating the queue (a read-only command must
        not leave an outbox behind): a file is created and `flock`-ed, then removed, in the
        nearest existing directory of the queue's path. A read-only or chmod-500 HOME, a volume
        out of inodes, or a filesystem without `flock` (ENOSYS: Lustre without ``-o flock``, some
        overlays) dropped EVERY write, a warning apiece. The lock is a fresh file's, never the
        queue's own, so a busy queue (another process appending) cannot read as unusable (Codex,
        round 2)."""
        import tempfile

        probe_dir = self.ops_dir
        while not probe_dir.exists() and probe_dir.parent != probe_dir:
            probe_dir = probe_dir.parent
        try:
            with tempfile.TemporaryFile(dir=probe_dir, prefix=".probe-usable-") as handle:
                try:
                    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                    oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
                except OSError as exc:
                    if exc.errno in _UNUSABLE_LOCK_ERRNOS:
                        return f"{probe_dir} does not support file locks ({exc.strerror or exc})"
        except OSError as exc:
            return f"{probe_dir} is not writable ({exc.strerror or exc})"
        return None

    @staticmethod
    def discover(environ=None) -> list[Path]:
        """Every outbox directory of this user on this machine: the default root and its
        ``rank-*`` children, and the ``$TMPDIR`` fallback and its. Only directories holding a
        queue, their own or a per-credential one under ``credential-v1/`` (plan 1.5: `probe
        outbox status` saw only the default one, so a distributed job's ranks and a fallen-back
        queue were invisible).

        ``rank-*`` only, deliberately: an offline run's queue (plan 2.12, ``<root>/offline/``) is
        delivered by `probe sync` alone, so `probe outbox drain --all` must never find it; and
        #2041's per-credential queues (``<dir>/credential-v1/<fingerprint>/``) are reached
        through each directory's own `namespaces()`, never as roots.

        A ``$TMPDIR`` fallback is listed only when it is a `trusted_dir`, and so each of its
        ``rank-*`` children: a directory another user made there must never be drained with this
        user's credential (review of #2054). ``environ``: another process's variables, as
        `default_root` takes them."""
        found: list[Path] = []
        roots = [(default_root(environ), False)] + [(root, True) for root in _fallback_roots(environ)]
        for root, untrusted_place in roots:
            candidates = [root]
            try:
                candidates += sorted(
                    child for child in root.iterdir() if child.name.startswith("rank-")
                )
            except OSError:
                pass
            for candidate in candidates:
                if candidate in found:
                    continue
                if untrusted_place and not trusted_dir(candidate):
                    continue
                if os.path.islink(candidate):
                    continue
                if (
                    (candidate / "ops").is_dir()
                    or (candidate / "status.json").exists()
                    # Every write of it queued under a stamped credential (#2041): the directory
                    # holds no queue of its own.
                    or (candidate / CREDENTIAL_NAMESPACE).is_dir()
                ):
                    found.append(candidate)
        return found

    def _ensure(self) -> None:
        # Once per Journal, not per append: this ran 4 mkdir + 4 chmod on EVERY write; chmod is a
        # SETATTR write RPC on NFS, not a cached stat, so on a shared $HOME it was eight round
        # trips per metric point. `_ensure_again` clears the flag whenever a write actually fails,
        # so a directory deleted underneath us is still recreated.
        if getattr(self, "_layout_ready", False):
            return
        self._ensure_layout()

    def _ensure_layout(self) -> None:
        for directory in (self.dir, self.ops_dir, self.failed_dir, self.blobs_dir, self.waiting_dir):
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            # mkdir mode is masked by umask; queue contents are research data, so re-assert (codex
            # finding: primitives default to umask).
            try:
                os.chmod(directory, 0o700)
            except OSError:
                pass
        self._layout_ready = True
        if not getattr(self, "_spool_checked", False):
            # One-time fold of a surviving pre-journal spool (T1-C). Two stats when there is
            # nothing to import. ONLY the default journal auto-imports: a custom/temporary journal
            # directory must never steal (and delete) the machine's global spool (codex).
            self._spool_checked = True
            if self.dir == default_dir():
                try:
                    self.import_spool()
                except Exception:  # noqa: BLE001 -- legacy debris must not block a write
                    pass

    # -- append -------------------------------------------------------------
    def _op_filename(self, op_id: str, *, sync: str = SYNC_FULL) -> str:
        """FIFO name: monotonic per-journal sequence first, wall clock second. Runs under the
        append lock. The sequence file makes ordering immune to backwards clock steps (red team:
        an NTP correction between enqueues could sort a run-end PATCH before the metrics it must
        follow).

        The `log()` path writes `.seq` without an fsync (plan 1.3), so a power loss can leave it
        BEHIND an op file that survived: the next append would take a sequence below a queued op
        and sort ahead of it (a terminal PATCH jumping the data it closes). So the first sequence
        this Journal hands out is at least the highest one the queue holds
        (`_queued_seq_high_water`, names only)."""
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
        ``"file"``: the op file is fsynced before its rename (a process killed after this returns
        loses nothing; a power loss can lose only the last renames, never leave a torn op) and the
        bookkeeping beside it (`.seq`, the producer record, status.json) is not fsynced at all.
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
                    # Compact: `indent=` takes json's pure-Python encoder.
                    write_text_atomic(
                        path, json.dumps(op, separators=(",", ":")) + "\n", mode=0o600, sync=sync
                    )
            except BaseException:
                if stamping:
                    self._unstamp_producer_locked(op, path)
                raise
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

    def _refresh_pending_estimate(self) -> int:
        """Re-seed `_pending_estimate` from status.json. One small file read."""
        status = self.read_status(self.dir, include_receipts=False) or {}
        try:
            pending = int(status.get("pending") or 0)
        except (TypeError, ValueError):
            pending = 0
        self._pending_estimate = pending
        return pending

    def _recount_pending(self) -> int | None:
        """The REAL queue length from a directory listing, at most once per
        `_RECOUNT_EVERY_SECONDS` (None when too soon). Only the refusal path calls it, so the
        common append never lists the queue."""
        now = time.monotonic()
        if now - self._recounted_at < _RECOUNT_EVERY_SECONDS:
            return None
        self._recounted_at = now
        # Counted OUTSIDE the append lock, names only and unsorted: a sorted listing of a queue at
        # the cap (500k names) held every other writer's `log()` for its whole length. Each append
        # landing during the listing is missing from the stored count (at the cap, a few per
        # second), so the estimate can read low until the next drain pass recounts: it can admit a
        # few writes over the cap, never refuse one under it.
        try:
            count = sum(1 for name in os.listdir(self.ops_dir) if name.endswith(".json"))
        except FileNotFoundError:
            count = 0
        with file_lock(self.append_lock):
            # Store it, or the next append's delta would rebuild the stale number from status.json
            # and refuse again.
            self._write_status_locked(recount=False, set_pending=count)
        self._pending_estimate = count
        return count

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
        """Journal one HTTP op.

        ``tag`` names what kind of op this is for a later reader of the queue (`probe sync`'s
        gate: a late hash re-send, ``"late_hash"``). Never sent; a drainer that does not know it
        ignores it.

        ``_prepared=True`` is `Client.write`'s: the body was normalized, NUL-checked and scrubbed
        on the way in (a failed NUL check arrives as ``validation_error``), so this skips all
        three on every `log()` (plan 1.3). Every other caller hands a raw body and keeps them.

        ``admitted=True`` skips the queue-length cap and the free-space floor, for the ONE op that
        must not be refused by them: a run's terminal status, queued behind data that filled the
        queue.

        ``best_effort=True`` marks an op that is not the user's data (the hardware rail): a
        refusal for room drops it without a capture gap or the "dropping queued writes" notice,
        both of which mean the user's own writes are being lost.

        ``blocking=False`` marks an op that must NOT hold a run's close. `Run.finish` refuses to
        mark a run terminal while any of its ops are undelivered or dead-lettered: right for data,
        wrong for a best-effort write. A diagnostic that dead-letters would leave the run
        `running` for the reaper instead of `failed`: the report changing the outcome it reports.
        """
        # An experiment's child write is journaled by its EXPERIMENT, never the project it sat in
        # when queued: the drain places it (`_placed`), so a move between the two cannot
        # dead-letter it, and its correlation digest is the same whichever project answered.
        path = unplaced_experiment_path(path)

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
                op = self._base_op("http", run_ref or run_ref_for_path(path))
                op.update({"method": method, "path": path, "body": body})
                return self._publish_receipt_op(correlation, request, op)["op_id"]
        if self.receipt_enabled:
            raise ValueError("delivery-v1 requires an explicit correlation")
        # An unknown kind makes older drainers refuse this too; a new field on kind=http would be
        # ignored and could upload a scrubbed identity alias.
        kind = "rejected_http" if validation_error is not None else "http"
        op = self._base_op(kind, run_ref or run_ref_for_path(path))
        op.update({"method": method, "path": path, "body": body})
        if validation_error is not None:
            op["validation_error"] = validation_error
        if not blocking:
            op["blocking"] = False
        if best_effort:
            op["best_effort"] = True
        if tag is not None:
            op["tag"] = tag
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

    def append_upload(
        self,
        *,
        anchor: str,
        anchor_id: str | None,
        name: str,
        src_path: str,
        stage: bool = True,
        inline_hash: bool = False,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
        run_ref: str | None = None,
        require_staged: bool = False,
        correlation: str | None = None,
        expected_content_hash: str | None = None,
        blocking: bool = True,
        defer_scan: bool = False,
        verbatim: bool = False,
    ) -> dict:
        """Queue a byte upload; returns ``{op_id, blob, size_bytes}``.

        ``verbatim`` (a checkpoint's files): a credential the gate would mask refuses the upload
        instead (here, or as a dead letter when the scan is deferred), so the stored file is never
        a rewritten copy.

        ``blocking=False`` marks an upload that must NOT hold its run's close, like
        ``append_http``'s flag: `Run.finish` still drains it first but an undeliverable one (an R2
        outage) cannot keep the run open. Output capture uses it; an explicit `log_artifact` not.

        With ``stage`` the file is snapshotted into the blob store, and with ``inline_hash`` the
        digest is taken FROM THE SNAPSHOT, never the live source whose bytes can change between a
        hash pass and a copy pass (codex: a same-size rewrite in that window would poison the
        content address). Without ``inline_hash`` the drainer hashes later (11A). The snapshot
        lands under a dot-prefixed staging name (gc ignores dotfiles); the publish rename +
        op-file write happen together under the append lock, so gc never sees an unreferenced
        blob to delete.

        A requested ``stage`` can come back false: staging is refused when the snapshot would
        drive the blob store's filesystem under :data:`MIN_FREE_BYTES`. The returned
        ``staged``/``unstaged_reason`` (also on the op) say so.

        ``require_staged`` REFUSES that degrade: nothing is appended and ``op_id`` comes back None
        (the only case where it is not a string), with ``staged``/``unstaged_reason`` saying why;
        the caller is expected to upload synchronously. Why: an unstaged op records ``src_path``
        and the drainer reads the LIVE FILE at delivery. Under an opt-in ``--async`` the caller
        chose that; as a DEFAULT it is a footgun: `probe artifact add ckpt.pt` beside a training
        loop rotating checkpoints would upload step-1100 bytes under the step-1000 name, or 422 on
        a file that is gone. Staging cannot be predicted from outside (free space is a race), so
        attempt it and be told. Default False keeps every existing caller byte-identical.

        ``defer_scan`` (with ``stage``) takes the credential scan off the caller's thread: the file
        is copied into the waiting room and the call returns; `promote_waiting` scans, redacts and
        fingerprints the copy and only then queues it. ``blob`` comes back None, ``waiting`` True.
        """
        # scanning disabled: meta = default_scrub(meta)
        # `scrub_string`, not `scrub_text`: see `Client.upload`.
        # scanning disabled: name = scrub_string(name)
        if correlation is not None:
            queue = (
                self
                if self.receipt_enabled
                else self.for_receipts(self.dir, context=self.context, attribution=self.attribution)
            )
            return queue._receipt_upload(
                correlation=correlation,
                expected_content_hash=expected_content_hash,
                anchor=anchor,
                anchor_id=anchor_id,
                name=name,
                src_path=src_path,
                content_type=content_type,
                kind=kind,
                meta=meta,
                span_id=span_id,
                step_index=step_index,
                run_ref=run_ref,
            )
        if self.receipt_enabled:
            raise ValueError("delivery-v1 requires an explicit correlation")
        check_upload(src_path)
        self._ensure()
        upload = {
            "anchor": anchor,
            "anchor_id": anchor_id,
            "name": name,
            "content_type": content_type,
            "kind": kind,
            "meta": meta,
            "span_id": span_id,
            "step_index": step_index,
            "src_path": os.path.abspath(src_path),
        }
        if verbatim:
            upload["verbatim"] = True
        # The strict policy keeps the full scan on the caller's thread, where it always was
        # (`read_upload_redacted`); only the quick check waits.
        if stage and defer_scan and not strict_policy():
            waiting = self._enqueue_waiting(
                upload, run_ref=run_ref, inline_hash=inline_hash, require_staged=require_staged,
                blocking=blocking,
            )
            if waiting is not None:
                return waiting
        op = self._base_op("upload", run_ref)
        if not blocking:
            op["blocking"] = False
        staged = False
        publish = None
        digest: str | None = None
        size_bytes: int | None = None
        unstaged_reason: str | None = None
        if stage:
            unstaged_reason = self._staging_headroom(src_path)
            if unstaged_reason is not None:
                if require_staged:
                    # Refuse rather than degrade. No op is appended, so the caller's synchronous
                    # fallback is the ONLY writer: a queued op would upload the file twice and the
                    # drainer's later read of a rotated src_path would win.
                    return {
                        "op_id": None,
                        "blob": None,
                        "size_bytes": None,
                        "staged": False,
                        "unstaged_reason": unstaged_reason,
                    }
                # Degrade to referencing the source rather than refusing: enqueue is fail-open by
                # contract (it runs beside a training loop), so the op goes in and the drainer
                # reads the original bytes. If the source is gone the drain raises a 422: a dead
                # letter with a message, never a lost write nobody was told about, never a full disk.
                stage = False
        if stage:
            staging = self.blobs_dir / f".staging-{op['op_id']}"
            snapshot_file(src_path, staging, verbatim=verbatim)
            if inline_hash:
                digest, size_bytes = fingerprint(str(staging))
            final = (
                self.blobs_dir / digest
                if digest is not None
                else self.blobs_dir / f"incoming-{op['op_id']}"
            )

            def publish() -> None:
                if digest is not None and final.exists():
                    staging.unlink(missing_ok=True)  # dedup: bytes already staged
                else:
                    os.replace(staging, final)
                fsync_directory(self.blobs_dir)

            staged = True
        elif inline_hash:
            # UNSTAGED, so nothing redacts (as it never did): the drainer re-reads this path and
            # sends it as it sits (inspected first only under the block policy). The digest must
            # describe the file as it sits, or the guard refuses the very upload this policy exists
            # to save. (An earlier version fingerprinted the redacted bytes here and every such op
            # dead-lettered.) The server records what it finds.
            digest, size_bytes = fingerprint(src_path)
        op["upload"] = {
            **upload,
            "blob": digest,
            "staged": staged,
            "size_bytes": size_bytes,
            "unstaged_reason": unstaged_reason,
        }
        self._append(
            op,
            before_write=publish,
            unstaged_low_disk=1 if unstaged_reason is not None else 0,
            # `_staging_headroom` above already priced this write's disk cost and degraded to an
            # unstaged reference if there was no room. Re-checking the floor here would refuse the
            # very op that degrade produced.
            headroom_checked=True,
        )
        return {
            "op_id": op["op_id"],
            "blob": digest,
            "size_bytes": size_bytes,
            "staged": staged,
            "unstaged_reason": unstaged_reason,
        }

    # -- the waiting room: uploads queued before their credential scan ------
    #
    # WHY. `log_artifact` scanned the file three times on the caller's thread before returning
    # (205 s for an 11.5 MB zip). Now the call copies the file here and returns; `promote_waiting`
    # (detached worker, a barrier, or `drain`) scans, redacts and fingerprints the copy, and only
    # then does it become an op in `ops/`.
    #
    # WHY A SEPARATE DIRECTORY. Every released drainer reads every `*.json` in `ops/` (hidden
    # names included) and an old one sharing this journal would upload whatever it found.
    # Nothing unscanned may ever sit in `ops/`.
    #
    # THE COMMIT ORDER, per item `<id>` (item flock held throughout):
    #   enqueue: `<id>.bytes` (plain copy, fsync), then `<id>.json` (the record; its existence
    #            is what "queued" means).
    #   promote: redact into a staging blob; then under the append lock --
    #            (1) publish the blob  (2) write the final op to `<id>.op.json`
    #            (3) unlink `<id>.json`  (4) RENAME `<id>.op.json` into `ops/`;
    #            then (5) unlink `<id>.bytes`.
    #   recover: `<id>.json` present -> promote again (the op was never visible);
    #            only `<id>.op.json` -> roll forward, re-deriving the blob from `<id>.bytes`
    #            (a GC may have taken the published one); only `<id>.bytes` -> delete it.
    # So each item becomes exactly one visible op, never zero, never two.
    #
    # ORDER. Items promote in queue order, and a run's items never pass its earliest one that
    # cannot be promoted right now (another process holds it, a disk error): two versions of one
    # artifact must reach the server in the order logged. `drain` holds a run's later ops back
    # the same way (`waiting_positions`).

    def _waiting_paths(self, op_id: str) -> tuple[Path, Path, Path, Path]:
        base = self.waiting_dir / op_id
        return (
            base.with_suffix(".json"),
            self.waiting_dir / f"{op_id}.op.json",
            base.with_suffix(".bytes"),
            base.with_suffix(".lock"),
        )

    def _enqueue_waiting(
        self,
        upload: dict,
        *,
        run_ref: str | None,
        inline_hash: bool,
        require_staged: bool,
        blocking: bool = True,
    ) -> dict | None:
        # Two copies until promotion ends: the waiting one and the clean blob.
        refusal = self._staging_headroom(upload["src_path"], copies=2)
        if refusal is not None:
            if require_staged:
                return {"op_id": None, "blob": None, "size_bytes": None, "staged": False,
                        "unstaged_reason": refusal}
            return None  # the ordinary path degrades to an unstaged reference
        # The op ceiling counts what waits as well as what is queued: a stalled promoter must not
        # let an upload-only producer grow this without bound.
        refusal = self._append_headroom(check_free=False, extra=self.count_waiting(self.dir))
        if refusal is not None:
            raise OutboxFull(refusal)
        op = self._base_op("upload", run_ref)
        if not blocking:
            op["blocking"] = False  # see `append_upload`; it rides into the op
        op["upload"] = {**upload, "blob": None, "staged": True, "size_bytes": None,
                        "unstaged_reason": None}
        record, _, data, lock = self._waiting_paths(op["op_id"])
        with _item_lock(lock):
            # The queue position is the CALL's, reserved now: a run's terminal status queued after
            # this upload must still sort after it. So is the producer's sequence: its promoter
            # is someone else.
            with file_lock(self.append_lock):
                op["queue_filename"] = self._op_filename(op["op_id"])
                self._stamp_producer_locked(op)
            raw = read_source(upload["src_path"])
            _write_private(data, raw)
            write_text_atomic(
                record, json.dumps({"op": op, "inline_hash": bool(inline_hash)}) + "\n", mode=0o600
            )
            fsync_directory(self.waiting_dir)
        return {"op_id": op["op_id"], "blob": None, "size_bytes": len(raw), "staged": True,
                "unstaged_reason": None, "waiting": True}

    def _waiting_items(self) -> list[tuple[str, str, str | None, bool, bool]]:
        """`(queue position, op id, run_ref, readable, blocking)` per waiting item, in queue
        order. An unreadable record sorts first, so it is dealt with before anything it might be
        holding up."""
        try:
            names = os.listdir(self.waiting_dir)
        except OSError:
            return []
        items: dict[str, tuple[str, str, str | None, bool, bool]] = {}
        for op_id in {name.split(".", 1)[0] for name in names if name.endswith(".json")}:
            # The record, then the committed op: a promotion between the listing and this read has
            # replaced one with the other (steps 2-3), and only when both are gone is the op in
            # `ops/` (step 4), which a reader looking at `ops/` AFTER this one then sees.
            record, prepared, _, _ = self._waiting_paths(op_id)
            for path in (record, prepared):
                try:
                    body = json.loads(path.read_text())
                    op = body.get("op") or body
                    items[op_id] = (str(op["queue_filename"]), op_id, op.get("run_ref"), True,
                                    op.get("blocking", True) is not False)
                except FileNotFoundError:
                    continue
                except (OSError, ValueError, KeyError, TypeError, AttributeError):
                    items[op_id] = ("", op_id, None, False, True)
                break
        return sorted(items.values())

    def waiting(self, *, run_ref: str | None = None) -> list[str]:
        """Op ids still in the waiting room (queued, or promoted halfway), in
        the order they were queued."""
        return [
            op_id for _, op_id, ref, readable, _ in self._waiting_items()
            if run_ref is None or ref == run_ref or not readable
        ]

    def waiting_positions(self) -> dict[str | None, str]:
        """Per run, the queue position of its earliest waiting upload: `drain` delivers none of
        that run's ops queued after it. A non-blocking upload
        (`append_upload(blocking=False)`) holds nothing back."""
        positions: dict[str | None, str] = {}
        for position, _, ref, readable, blocking in self._waiting_items():
            if readable and blocking and ref is not None:
                positions.setdefault(ref, position)
        return positions

    @staticmethod
    def count_waiting(directory: str | Path) -> int:
        """Waiting items, by LISTING the directory, never status.json (an older worker rewrites
        it from `ops/` alone)."""
        try:
            names = os.listdir(Path(directory) / "waiting")
        except OSError:
            return 0
        return len({name.split(".", 1)[0] for name in names if name.endswith(".json")})

    def promote_waiting(
        self, *, run_ref: str | None = None, wait: bool = False, timeout: float | None = None
    ) -> int:
        """Scan, redact and fingerprint waiting uploads; queue each as an op. Returns how many
        became ops. Items go in queue order and a run stops at its first item that cannot go now:
        another process holds it (with ``wait``, waited for) or a disk error. Outbox full stops
        the pass. An item that can never go (unreadable record, missing copy, failing scan) is
        dead-lettered with the reason. ``timeout`` bounds the call: no scan starts and no wait
        continues after it.
        """
        if self.receipt_enabled or not self.waiting_dir.is_dir():
            return 0
        deadline = None if timeout is None else time.monotonic() + timeout
        promoted = 0
        while True:
            busy = False
            stopped: set[str | None] = set()  # runs held at an earlier item
            for _, op_id, ref, readable, _ in self._waiting_items():
                if deadline is not None and time.monotonic() >= deadline:
                    return promoted
                # An unreadable item belongs to no run we can name: taken whatever `run_ref` asks
                # for, and dead-lettered.
                if (run_ref is not None and ref != run_ref and readable) or ref in stopped:
                    continue
                with _try_lock(self._waiting_paths(op_id)[3]) as held:
                    if not held:
                        busy = True
                        stopped.add(ref)
                        continue
                    try:
                        promoted += self._promote_locked(op_id)
                    except OutboxFull:
                        return promoted
                    except OSError:
                        stopped.add(ref)  # left waiting; the next pass retries
                    except Exception as exc:  # noqa: BLE001 -- one item must not wedge the rest
                        self._dead_letter_waiting(
                            op_id, None, f"promotion failed ({type(exc).__name__})"
                        )
            self._sweep_waiting_orphans()
            if not (wait and busy):
                return promoted
            if deadline is not None and time.monotonic() >= deadline:
                return promoted
            time.sleep(0.05)

    def promote_for_close(self, run_ref: str, *, timeout: float) -> list[str]:
        """Before a run's close is queued: promote its waiting uploads, waiting up to ``timeout``
        for any another process is scanning. Returns the op ids still waiting that hold the close
        (a non-blocking upload does not); the caller decides whether that refuses the close."""
        try:
            self.promote_waiting(run_ref=run_ref, wait=True, timeout=timeout)
        except Exception:  # noqa: BLE001 -- judged by what is still waiting
            pass
        return self.waiting_for_close(run_ref)

    def waiting_for_close(self, run_ref: str) -> list[str]:
        """This run's waiting uploads that hold its close: all but those queued non-blocking, plus
        any unreadable item (it may be this run's)."""
        return [
            op_id for _, op_id, ref, readable, blocking in self._waiting_items()
            if (ref == run_ref and blocking) or not readable
        ]

    def _promote_locked(self, op_id: str) -> int:
        record, prepared, data, lock = self._waiting_paths(op_id)
        if not record.exists() and not prepared.exists():
            data.unlink(missing_ok=True)
            return 0
        starting_over = record.exists()
        try:
            body = json.loads((record if starting_over else prepared).read_text())
            op = dict(body["op"] if starting_over else body)
            inline_hash = bool(body.get("inline_hash"))
            if "op_id" not in op or not isinstance(op.get("upload"), dict):
                raise KeyError("op")  # not the shape promotion relies on
        except FileNotFoundError:
            return 0  # promoted meanwhile
        except (ValueError, KeyError, TypeError, AttributeError):
            self._dead_letter_waiting(op_id, None, "the queued upload's record is unreadable")
            return 0
        try:
            raw = data.read_bytes()
        except FileNotFoundError:
            self._dead_letter_waiting(op_id, op, "the queued copy of the upload is missing")
            return 0
        if starting_over:
            prepared.unlink(missing_ok=True)  # a half-made promotion; start over
            try:
                # scanning disabled: clean, result = redact_quick_bytes(raw)
                clean, result = raw, InspectionResult()
                if (op.get("upload") or {}).get("verbatim"):
                    refuse_rewrite(result)
            except CredentialBlocked as exc:
                self._dead_letter_waiting(op_id, op, str(exc))
                return 0
            if result.rewritten:
                # The artifact row records this too (the server reads the markers); this line is
                # for whoever reads the worker's log.
                print(
                    f"redacted {', '.join(sorted(set(result.rewritten)))} in queued upload "
                    f"{(op.get('upload') or {}).get('name')!r} ({now_iso()})",
                    flush=True,
                )
            digest = hashlib.sha256(clean).hexdigest() if inline_hash else None
            op["upload"]["blob"] = digest
            op["upload"]["size_bytes"] = len(clean) if inline_hash else None
            publish = self._staged_publisher(op, clean)
        else:
            # Roll forward: the op was committed and never made visible. Its blob may have gone to
            # a GC (it was unreferenced), so the blob is derived again from the scanned source
            # (deleted last) and published under the append lock like any other: whether it still
            # exists is only knowable there.
            try:
                # scanning disabled: clean, result = redact_quick_bytes(raw)
                clean, result = raw, InspectionResult()
                if (op.get("upload") or {}).get("verbatim"):
                    refuse_rewrite(result)
            except CredentialBlocked as exc:
                self._dead_letter_waiting(op_id, op, str(exc))
                return 0
            publish = self._staged_publisher(op, clean)

        def write_op(path: Path, final_op: dict) -> None:
            # (2) the committed op, (3) retire the record, (4) make it visible.
            write_text_atomic(prepared, json.dumps(final_op, indent=2) + "\n", mode=0o600)
            record.unlink(missing_ok=True)
            fsync_directory(self.waiting_dir)
            os.replace(prepared, path)
            fsync_directory(self.ops_dir)

        # `admitted`: the op ceiling counted this upload when queued (`_enqueue_waiting`).
        # Refusing it now could deadlock: drain holds the run's later ops, which fill the queue,
        # behind this very upload.
        self._append(op, before_write=publish, headroom_checked=True, write_op=write_op, admitted=True)
        data.unlink(missing_ok=True)  # (5)
        # Safe while held: a promoter that opened the old lock finds nothing left to do, and one
        # locking it after this unlink is told it holds nothing (`_same_file`).
        _retire_lock(lock)
        return 1

    def _staged_publisher(self, op: dict, clean: bytes):
        """Write `clean` to a staging blob now; return the publish step that moves it into place
        inside the append lock (gc takes the same lock)."""
        staging = self.blobs_dir / f".staging-{op['op_id']}"
        staging.unlink(missing_ok=True)
        _write_private(staging, clean)
        digest = op["upload"].get("blob")
        final = self.blobs_dir / digest if digest else self.blobs_dir / f"incoming-{op['op_id']}"

        def publish() -> None:
            if digest is not None and final.exists():
                staging.unlink(missing_ok=True)  # dedup: these bytes are already staged
            else:
                os.replace(staging, final)
            fsync_directory(self.blobs_dir)

        return publish

    def _dead_letter_waiting(self, op_id: str, op: dict | None, reason: str) -> None:
        """Refuse a waiting upload as the sync path refuses one: with the reason, nothing sent.
        Its copy goes: a retry has nothing scanned to deliver (fails again, never sends unscanned
        bytes)."""
        record, prepared, data, lock = self._waiting_paths(op_id)
        if op is None:
            # Keep whatever attribution survives: a run-scoped close checks its run's dead
            # letters and one filed under no run is missed.
            try:
                body = json.loads((record if record.exists() else prepared).read_text())
                found = body.get("op") or body
                op = dict(found) if isinstance(found, dict) and found.get("run_ref") else None
            except (OSError, ValueError, AttributeError, TypeError):
                op = None
        if op is None:
            op = {**self._base_op("upload", None), "op_id": op_id, "upload": {"staged": True}}
        op["last_error"] = f"{reason}; nothing was sent -- log the artifact again"
        op["attempts"] = int(op.get("attempts") or 0) + 1
        name = op.get("queue_filename") or self._op_filename(op_id)
        with file_lock(self.append_lock):
            write_text_atomic(self.failed_dir / name, json.dumps(op, indent=2) + "\n", mode=0o600)
            record.unlink(missing_ok=True)
            prepared.unlink(missing_ok=True)
            data.unlink(missing_ok=True)
            self._write_status_locked()
        _retire_lock(lock)

    def _sweep_waiting_orphans(self) -> None:
        """Delete `.bytes` with neither record nor committed op: an enqueue that died before
        returning, or a promotion that finished. Locked ones are an enqueue in progress, left
        alone."""
        try:
            names = os.listdir(self.waiting_dir)
        except OSError:
            return
        live = {name.split(".", 1)[0] for name in names if name.endswith(".json")}
        for name in names:
            if not name.endswith((".bytes", ".lock")) or name.split(".", 1)[0] in live:
                continue
            record, prepared, data, lock = self._waiting_paths(name.split(".", 1)[0])
            with _try_lock(lock) as held:
                if held and not record.exists() and not prepared.exists():
                    data.unlink(missing_ok=True)
                    _retire_lock(lock)

    def _append_headroom(self, *, check_free: bool = True, extra: int = 0) -> str | None:
        """``None`` when there is room for one more queued op, else WHY not.

        The disk floor and op ceiling existed only for UPLOAD staging ("a producer that outruns
        delivery grows the queue without bound: filling the disk is the STEADY STATE of that
        shape"). That is what a metric-logging loop does in an outage, and `append_http` had no
        free-space floor, count cap or backpressure: a long outage filled the state partition,
        and on a shared $HOME everyone's.

        The free-space stat is sampled, not per-append (disk pressure builds over thousands of
        writes; a statvfs per metric point repeats the listdir mistake this class just dropped).
        The op-count ceiling is free: the delta counter tracks it.
        """
        ceiling = MAX_PENDING_OPS if self.op_ceiling is None else self.op_ceiling
        pending = self._pending_estimate
        other = self._sibling_pending_count()
        if pending is None and extra:
            pending = self._refresh_pending_estimate()
        if pending is not None:
            pending += other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            # Re-read before refusing: a refusal is a dropped datapoint, and another process's
            # drain may have lowered the count since.
            other = self._sibling_pending_count(fresh=True)
            pending = self._refresh_pending_estimate() + other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            # status.json can still say "full" mid-drain-pass after most of the queue was
            # delivered: count it for real.
            real = self._recount_pending()
            if real is not None:
                pending = real + other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            return (
                f"outbox full: {pending} ops queued, at the {ceiling} "
                "ceiling (PROBE_OUTBOX_MAX_PENDING). Delivery is not keeping up "
                "— see `probe outbox status`"
            )
        if not check_free:
            # The caller already made its own headroom decision. `append_upload` asks
            # `_staging_headroom` first and DEGRADES to an unstaged op (a small reference, not a
            # byte copy): the path that must keep working when the disk is tight. Blocking it here
            # would refuse the write the degrade exists to preserve. The op-count ceiling above
            # still applies.
            return None
        return self.below_floor()

    def below_floor(self) -> str | None:
        """Why the queue's volume is under its free-space floor, or None. Sampled, not per call
        (disk pressure builds over thousands of writes): the statvfs runs every
        `_STATVFS_EVERY` calls, and on every call while the last sample was low, so recovery is
        seen at once. `Client` asks before it queues (plan 1.5: below the floor it may send
        directly) and every append asks again."""
        floor = self._free_floor()
        if floor <= 0:
            return None
        self._appends_since_statvfs += 1
        if self._appends_since_statvfs < _STATVFS_EVERY and self._last_free_ok:
            return None
        self._appends_since_statvfs = 0
        try:
            free = shutil.disk_usage(self.ops_dir if self.ops_dir.exists() else self.dir).free
        except OSError:
            self._last_free_ok = True
            return None  # unmeasurable is not a breach; enqueue is fail-open
        self._last_free_ok = free >= floor
        if self._last_free_ok:
            return None
        return (
            f"low disk: {free} bytes free on {self.ops_dir}, under the "
            f"{floor}-byte floor (PROBE_OUTBOX_MIN_FREE_BYTES). Queued writes "
            "are sent directly while nothing is queued, else dropped rather "
            "than filling the filesystem"
        )

    def _free_floor(self) -> int:
        """`free_floor` for this journal's volume, measured once (a volume's size does not
        change under a running process; an override needs no measuring)."""
        if MIN_FREE_BYTES is not None:
            return MIN_FREE_BYTES
        floor = getattr(self, "_floor_cached", None)
        if floor is None:
            where = self.dir if self.dir.exists() else self.dir.parent
            floor = self._floor_cached = free_floor(where)
        return floor

    def _sibling_pending_count(self, *, fresh: bool = False) -> int:
        """The other namespace's (`delivery-v1` <-> the root) pending count, which the op ceiling
        counts too. Re-read every `_STATVFS_EVERY` appends and before any refusal (``fresh``), not
        each append: it was a status.json open per `log()` for a namespace nearly always empty
        for a training loop (plan 1.3)."""
        self._appends_since_sibling += 1
        if (
            fresh
            or self._sibling_pending is None
            or self._appends_since_sibling >= _STATVFS_EVERY
        ):
            self._appends_since_sibling = 0
            sibling = self.dir.parent if self.receipt_enabled else self.dir / DELIVERY_NAMESPACE
            other = self.read_status(sibling, include_receipts=False) or {}
            try:
                self._sibling_pending = int(other.get("pending") or 0)
            except (TypeError, ValueError):
                self._sibling_pending = 0
        return self._sibling_pending

    def _staging_headroom(self, src_path: str | Path, *, copies: int = 1) -> str | None:
        """``None`` when there is room to stage ``src_path``, else WHY not. Two stat-class
        syscalls, no read of the file: this runs on every upload enqueue beside a training loop
        and must not scale with the bytes queued. Unmeasurable is NOT a breach (no evidence to
        degrade on; enqueue is fail-open).
        """
        floor = self._free_floor()
        if floor <= 0:
            return None
        try:
            size = os.path.getsize(src_path)
            free = shutil.disk_usage(self.blobs_dir).free
        except OSError:
            return None
        if free - copies * size >= floor:
            return None
        return (
            f"low disk: staging {size} bytes would leave {free - copies * size} bytes "
            f"free on {self.blobs_dir}, under the {floor}-byte floor "
            "(PROBE_OUTBOX_MIN_FREE_BYTES); the op references the source "
            "instead and the drainer reads its original bytes"
        )

    # -- producer registry (parity F4) --------------------------------------
    def _producer_file(self, producer_id: str) -> Path:
        return self.producers_dir / f"{_safe_component(producer_id)}.json"

    def _ensure_producers_dir(self) -> None:
        self.producers_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            os.chmod(self.producers_dir, 0o700)
        except OSError:
            pass

    def _read_producer_locked(self, producer_id: str) -> dict:
        try:
            return json.loads(self._producer_file(producer_id).read_text())
        except (OSError, json.JSONDecodeError, ValueError):
            return {}

    def _update_producer_locked(
        self,
        producer_id: str,
        record: dict,
        *,
        role: str | None = None,
        last_sequence: int | None = None,
        delivered: int | None = None,
        gap: dict | None = None,
        state: str | None = None,
        sync: str = SYNC_FULL,
    ) -> None:
        record.setdefault("schema", SCHEMA)
        record.setdefault("producer_id", producer_id)
        record.setdefault("role", role)
        record.setdefault("registered_at", now_iso())
        record.setdefault("last_sequence", 0)
        record.setdefault("delivered", 0)
        record.setdefault("gaps", [])
        record.setdefault("gap_count", len(record["gaps"]))
        record.setdefault("closed_at", None)
        if last_sequence is not None:
            record["last_sequence"] = max(int(record["last_sequence"]), last_sequence)
        if delivered is not None:
            # Additive, and re-read from disk under the lock by every caller: the drainer and a
            # live writer touch the same record from different processes, so an in-memory counter
            # would clobber.
            record["delivered"] = int(record.get("delivered") or 0) + int(delivered)
        if gap is not None:
            # A count plus the most recent few: the full list grew by one per dropped write and
            # is rewritten with every drop.
            record["gap_count"] = int(record.get("gap_count") or 0) + 1
            record["gaps"] = [*record["gaps"], gap][-_GAPS_KEPT:]
        if state is not None:
            record["state"] = state
            record["closed_at"] = now_iso() if state == "closed" else None
        else:
            record.setdefault("state", "open")
        write_text_atomic(
            self._producer_file(producer_id),
            json.dumps(record, indent=2) + "\n",
            mode=0o600,
            sync=sync,
        )

    def register_producer(self, producer_id: str, *, role: str = "sdk") -> None:
        """Join this journal's producer registry. Sequences make silent capture loss VISIBLE:
        every later append stamps ``producer_id`` + a per-producer sequence and the registry
        records the high-water mark. A registry saying N with no op (queued, dead-lettered or
        delivered) ever stamped N is a write lost between caller and journal; ``note_capture_gap``
        records those the caller catches itself. Re-registering an existing id resumes its
        sequence (restarts, and ids shared across short-lived processes, continue the same line).
        """
        self._ensure()
        self._ensure_producers_dir()
        self._producer_id = producer_id
        self._producer_role = role
        with file_lock(self.append_lock):
            record = self._read_producer_locked(producer_id)
            self._update_producer_locked(
                producer_id, record, role=role, state="open"
            )

    def note_capture_gap(self, reason: str) -> None:
        """Burn a sequence for a write that never reached the journal, so the loss is a visible
        hole, not silence (Miles' capture_gaps)."""
        if self._producer_id is None:
            return
        with file_lock(self.append_lock):
            record = self._read_producer_locked(self._producer_id)
            sequence = int(record.get("last_sequence") or 0) + 1
            self._update_producer_locked(
                self._producer_id,
                record,
                role=self._producer_role,
                last_sequence=sequence,
                # scanning disabled: gap={"sequence": sequence, "reason": scrub_text(reason), "at": now_iso()},
                gap={"sequence": sequence, "reason": reason, "at": now_iso()},
            )

    def note_delivered(self, producer_id: str, count: int = 1) -> None:
        """Add ``count`` LANDED ops to one producer's tally.

        ``last_sequence`` says what a producer handed the journal; this says how much reached the
        server, so "of what I enqueued, how much is there" is answerable without correlating two
        machines (``DrainReport.delivered`` is per-pass and machine-wide).

        Called by :func:`drain` per delivered op, NOT batched at the end of a pass: a pass that
        dies mid-flight (SIGKILL, OOM, dead laptop) is when the number matters. It takes a
        producer id, not this journal's own, because the drainer delivers for every producer,
        usually including ones with no live process.

        The tally is a FLOOR: written after the op file is unlinked, so a crash in that window
        under-counts by at most one op per crash; writing first would over-count, and a producer
        reporting more delivered than enqueued reads as a bug, not as the at-least-once delivery
        it is.
        """
        if not producer_id or count <= 0:
            return
        self._ensure_producers_dir()
        with file_lock(self.append_lock):
            record = self._read_producer_locked(producer_id)
            self._update_producer_locked(producer_id, record, delivered=count)

    def seal_producer(self) -> None:
        """Mark this producer cleanly closed. A producer left "open" whose process is gone is a
        crashed writer: the report shows exactly that."""
        if self._producer_id is None or not self.producers_dir.exists():
            return
        with file_lock(self.append_lock):
            record = self._read_producer_locked(self._producer_id)
            self._update_producer_locked(
                self._producer_id, record, role=self._producer_role, state="closed"
            )

    def producer_report(self) -> list[dict]:
        """Every producer this journal knows: sequence high-water, ``delivered`` tally, capture
        gaps, open/closed state. Unparseable records are skipped, not raised: diagnostics, never a
        blocker."""
        if not self.producers_dir.exists():
            return []
        out: list[dict] = []
        for path in sorted(self.producers_dir.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                out.append(json.loads(path.read_text()))
            except (OSError, json.JSONDecodeError, ValueError):
                continue
        return out

    # -- reads --------------------------------------------------------------
    @staticmethod
    def _read_dir(directory: Path) -> list[tuple[Path, dict]]:
        if not directory.exists():
            return []
        out: list[tuple[Path, dict]] = []
        for path in sorted(directory.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                out.append((path, json.loads(path.read_text())))
            except (OSError, json.JSONDecodeError):
                continue
        return out

    def pending(self) -> list[tuple[Path, dict]]:
        return self._read_dir(self.ops_dir)

    def failed(self) -> list[tuple[Path, dict]]:
        return self._read_dir(self.failed_dir)

    def run_ops(self, run_ref: str) -> "RunOps":
        """A counter of ONE run's blocking ops that parses each op file once."""
        return RunOps(self, run_ref)

    def outbox_queues(self) -> "list[Journal]":
        """Every queue of the outbox this one belongs to: the root, its receipt
        namespace, and each credential queue (#2035) with its own."""
        root = Journal(self.outbox_root, context=self.context, attribution=self.attribution)
        return root.namespaces()

    def worker_alive(self) -> bool:
        """Whether a worker holds this queue's lease right now (non-blocking)."""
        try:
            handle = (self.dir / ".worker.lock").open("a+")
        except OSError:
            return False
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except (BlockingIOError, OSError):
            return True
        else:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            return False
        finally:
            handle.close()

    def own_namespaces(self) -> "list[Journal]":
        """`namespaces` without the credential queues under a root: what the
        root's own worker serves."""
        return [
            queue
            for queue in self.namespaces()
            if queue.dir == self.dir or queue.dir == self.dir / DELIVERY_NAMESPACE
        ]

    def other_queues(self) -> "list[Journal]":
        """`outbox_queues` minus this queue and its own receipt namespace."""
        mine = {self.dir, self.dir / DELIVERY_NAMESPACE}
        return [queue for queue in self.outbox_queues() if queue.dir not in mine]

    def run_ops_elsewhere(self, run_ref: str, *, min_epoch: int | None = None) -> "RunOps":
        """ONE run's blocking ops in the outbox's OTHER queues: writes of the
        same run queued under another credential (#2035), which this queue's
        order cannot see and a close queued here could overtake. ``min_epoch``
        leaves out an older attempt's (round 5)."""
        return RunOps(self, run_ref, queues=self.other_queues(), min_epoch=min_epoch)

    @property
    def paused(self) -> bool:
        """Paused here, or in any queue above this one (`probe outbox pause` pauses the root and
        every namespace under it), by a pause that has not run out (`DEFAULT_PAUSE_HOURS`)."""
        return _pause_in_effect(self.dir) is not None

    def pause(self, hours: float | None = DEFAULT_PAUSE_HOURS) -> dict:
        """Hold delivery for ``hours``, or until `resume` when None. Returns the marker. Written
        under the append lock, so `lift_stale_pause` never removes a pause written while it looked."""
        from datetime import datetime, timedelta, timezone

        self._ensure()
        at = datetime.now(timezone.utc)
        until = None if hours is None else (at + timedelta(hours=hours)).isoformat()
        marker = {"schema": PAUSE_SCHEMA, "at": at.isoformat(), "until": until}
        with file_lock(self.append_lock):
            write_text_atomic(self.paused_file, json.dumps(marker) + "\n", mode=0o600)
            self._write_status_locked()
        return marker

    def lift_stale_pause(self, *, wait: bool = True) -> bool:
        """Delete this queue's pause marker once it no longer holds: its end passed, or it is an
        older CLI's endless one. An older release reads only whether the marker EXISTS (an SDK
        pinned in a job's venv), so it stays paused until the file is gone. An older CLI's `pause`
        writes outside the append lock, so one typed in the microseconds between this check and
        the unlink is lost. ``wait`` False: when another process holds the append lock, lift
        nothing now (for a caller that must never hang on a stopped writer's lock: the Probe
        service). True when one was lifted."""
        if not os.path.lexists(self.paused_file) or _pause_marker(self.dir) is not None:
            return False
        lock = file_lock(self.append_lock) if wait else _try_lock(self.append_lock)
        with lock as held:
            if held is False:
                return False
            if not os.path.lexists(self.paused_file) or _pause_marker(self.dir) is not None:
                return False
            _unlink_pause(self.paused_file)
            self._write_status_locked()
        return True

    def resume(self) -> None:
        for child in self.namespaces()[1:]:
            child.resume()
        _unlink_pause(self.paused_file)
        if self.dir.exists():
            with file_lock(self.append_lock):
                self._write_status_locked()

    def quarantine_corrupt(self) -> int:
        """Move unparseable op files to failed/ so they stay VISIBLE. Silently skipping them
        (codex) let status count files the drain never saw: the worker exited 'empty' while the
        banner re-kicked it forever. Quarantined files keep their names: they count as failed in
        status.json while the (parse-skipping) readers ignore them. The queue is parsed OUTSIDE the
        append lock (plan 1.9); only the corrupt files are re-checked under it
        (`quarantine_paths`).
        """
        ops, corrupt = self._scan_ops()
        return self.quarantine_paths(corrupt, known=op_meta(ops))

    def _scan_ops(
        self, stamps: dict | None = None
    ) -> tuple[list[tuple[Path, dict]], list[Path]]:
        """ONE parse of ``ops/``, taken outside every lock: the ops in FIFO order and the paths
        that did not parse (for `quarantine_paths`). Op files appear by atomic rename, so one that
        does not parse is corrupt, not half-written. One vanished between listing and read was
        delivered or moved by someone else and is skipped. ``stamps`` gets each parsed op's
        (inode, size, mtime): how a pass that let go of the drain lock tells an op another drain
        changed (#3618).
        """
        if not self.ops_dir.exists():
            return [], []
        ops: list[tuple[Path, dict]] = []
        corrupt: list[Path] = []
        # Plan 1.6 review: a worker delivering one run while another sits in backoff re-scanned
        # the parked run's ops every pass; at 20k parked ops that held a core for the whole
        # outage. An op file unchanged since the last pass (same inode, size, mtime) and not
        # attempted by the drain (`_scan_forget`) is not parsed again. Only the first
        # `SCAN_CACHE_MAX_BYTES` of op files are kept: the cache outlives the pass and unbounded
        # held 58 MB at 20k ops.
        cache = self.__dict__.setdefault("_scan_cache", {})
        seen: dict = {}
        kept = 0
        for name in sorted(n for n in os.listdir(self.ops_dir) if n.endswith(".json")):
            path = self.ops_dir / name
            try:
                stat = os.stat(path)
                stamp = (stat.st_ino, stat.st_size, stat.st_mtime_ns)
                cached = cache.get(name)
                if cached is not None and cached[0] == stamp:
                    op = cached[1]
                else:
                    op = json.loads(path.read_text())
                if kept + stat.st_size <= SCAN_CACHE_MAX_BYTES:
                    seen[name] = (stamp, op)
                    kept += stat.st_size
                if stamps is not None:
                    stamps[name] = stamp
                ops.append((path, op))
            except FileNotFoundError:
                continue
            except (OSError, json.JSONDecodeError, ValueError):
                corrupt.append(path)
        self._scan_cache = seen
        return ops, corrupt

    def _scan_forget(self, name: str) -> None:
        """The drain is about to attempt this op (it may change it in memory): the next pass reads
        it from disk again."""
        cache = self.__dict__.get("_scan_cache")
        if cache is not None:
            cache.pop(name, None)

    def quarantine_paths(self, paths: list[Path], *, known: dict | None = None) -> int:
        """Move the given op files to failed/ if they STILL do not parse, re-checking only them
        under the append lock. ``known`` (from `op_meta`) lets the status recount skip re-parsing
        the rest."""
        if not paths:
            return 0
        moved = 0
        with file_lock(self.append_lock):
            for path in paths:
                try:
                    json.loads(path.read_text())
                    continue  # parses now: not ours to move
                except FileNotFoundError:
                    continue
                except (OSError, json.JSONDecodeError, ValueError):
                    os.replace(path, self.failed_dir / path.name)
                    moved += 1
            if moved:
                fsync_directory(self.failed_dir)
                fsync_directory(self.ops_dir)
                self._write_status_locked(known=known)
        return moved

    def sweep_stale_temps(self, *, older_than: float = 3600.0) -> int:
        """Remove ``.<name>.<uuid>.tmp`` siblings `write_text_atomic` left when a writer was killed
        mid-write, once older than an hour (a live write lasts milliseconds). Blob staging has its
        own sweep in `gc_blobs`. Never raises."""
        removed = 0
        cutoff = time.time() - older_than
        for directory in (self.ops_dir, self.failed_dir, self.dir):
            try:
                names = [n for n in os.listdir(directory) if n.startswith(".") and n.endswith(".tmp")]
            except OSError:
                continue
            for name in names:
                try:
                    path = directory / name
                    if path.stat().st_mtime < cutoff:
                        path.unlink()
                        removed += 1
                except OSError:
                    continue
        return removed

    def discard_failed(self, op_id: str | None = None) -> int:
        """Move dead letters (one, or all) to ``discarded/``: an audit-safe tombstone, not
        deletion. Covers quarantined-corrupt files too (matched by name when they cannot be
        parsed), which retry can never requeue (red team: without a discard verb they nagged
        forever). Returns how many moved (`discard_failed_counts` says what)."""
        return self.discard_failed_counts(op_id).writes

    def discard_failed_counts(self, op_id: str | None = None) -> DiscardCounts:
        """`discard_failed`, returning what moved (`DiscardCounts`). A credential queue's go to
        the root's ``discarded/``, which no cleanup deletes."""
        counts = DiscardCounts()
        for child in self.namespaces()[1:]:
            counts.merge(child.discard_failed_counts(op_id))
        target = self._discard_dir()
        moved = 0
        with file_lock(self.append_lock):
            if self.failed_dir.exists():
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path in sorted(self.failed_dir.iterdir()):
                    op = _read_op_file(path)
                    if op_id is not None:
                        if isinstance(op, dict):
                            if op.get("op_id") != op_id:
                                continue
                        elif op_id not in path.name:
                            continue
                    os.replace(path, target / path.name)
                    counts.add(op)
                    moved += 1
            if moved:
                fsync_directory(target)
                fsync_directory(self.failed_dir)
                self._write_status_locked()
                self._record_dead_letters()
        if moved:
            self.gc_blobs()
        return counts

    def drop_unrecoverable(
        self, *, run_exists: "Callable[[dict], bool | None] | None" = None
    ) -> DiscardCounts:
        """Move to ``discarded/`` the dead letters no retry can ever deliver (`probe doctor --fix`,
        #3629): a write a newer attempt of its run superseded (refused for a past write epoch; a
        run's epoch only grows), and a write whose run the server said does not exist, asked again
        now with the write's own credential. ``run_exists(op)`` answers: False only on the
        server's own "run not found", None when it cannot tell (no credential here, server away):
        then the letter stays, as does every other letter, for `probe outbox retry`. A close a
        takeover set aside stays too. Returns what moved (`DiscardCounts`)."""
        check = run_exists if run_exists is not None else _run_exists_now()
        counts = DiscardCounts()
        for queue in self.namespaces():
            if queue.receipt_enabled or not queue.failed_dir.exists():
                continue
            doomed: dict[Path, str] = {}
            for path in sorted(queue.failed_dir.glob("*.json")):
                op = _read_op_file(path)
                if not isinstance(op, dict) or op.get(TAKEOVER_HOLD_KEY) is not None:
                    continue
                error = str(op.get("last_error") or "")
                if _STALE_EPOCH_LETTER.match(error) or (
                    error == _NO_SUCH_RUN_LETTER and op.get("run_ref") and check(op) is False
                ):
                    doomed[path] = error
            if not doomed:
                continue
            target = queue._discard_dir()
            moved = 0
            with file_lock(queue.append_lock):
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path, error in doomed.items():
                    op = _read_op_file(path)
                    if not isinstance(op, dict) or str(op.get("last_error") or "") != error:
                        continue  # retried, discarded or failed again meanwhile
                    os.replace(path, target / path.name)
                    counts.add(op)
                    moved += 1
                if moved:
                    fsync_directory(target)
                    fsync_directory(queue.failed_dir)
                    queue._write_status_locked()
                    queue._record_dead_letters()
        if counts.writes:
            self.gc_blobs()
        return counts

    def _discard_dir(self) -> Path:
        """Where this queue's discards go: its own ``discarded/``, or for a credential queue the
        root's (a credential queue is deleted once idle, by older releases too, and its discards
        with it: `_move_discards`). A receipt namespace keeps its own: `recover_intents` reads it
        there."""
        if self.dir.parent.name == CREDENTIAL_NAMESPACE and not self.receipt_enabled:
            return self.dir.parent.parent / "discarded"
        return self.dir / "discarded"

    def discard_request(self, correlation: str, *, timeout: float = 5.0) -> dict:
        """Tombstone one receipt request wherever it waits (queued, dead-lettered, or an intent
        whose op never landed) so neither a drain nor a retry sends it again. A delivered request
        is left. Returns the state afterwards.

        Taken under the drain lock, so no pass is mid-way through the op; when another drain holds
        it past ``timeout`` nothing moves and the state still says where the request waits. One
        file is moved by name, nothing recounted, blobs left for the next drain to collect:
        `discard_failed` re-reads every dead letter and then all of the queue in `gc_blobs`, which
        made a repair of 1,200 requests take 166 s under the append lock."""
        waiting = WAITING_STATES
        state = self.delivery_state(correlation)
        if state["state"] not in waiting:
            return state
        handle = self.drain_lock.open("a+")
        try:
            if not _take_drain_lock(handle, wait_for_lock=True, timeout=timeout):
                return state
            key = self._correlation_key(correlation)
            with self._correlation_lock(key):
                state = self.delivery_state(correlation)
                if state["state"] not in waiting:
                    return state
                op = self._read_record(self.intents_dir / f"{key}.json")["op"]
                filename = op["queue_filename"]
                target = self.dir / "discarded"
                with file_lock(self.append_lock):
                    target.mkdir(parents=True, exist_ok=True, mode=0o700)
                    source = next(
                        (
                            directory / filename
                            for directory in (self.ops_dir, self.failed_dir)
                            if (directory / filename).exists()
                        ),
                        None,
                    )
                    if source is None:
                        # Pending: the intent committed and its op did not. The tombstone keeps
                        # `recover_intents` from restoring it.
                        write_text_atomic(
                            target / filename, json.dumps(op, indent=2) + "\n", mode=0o600
                        )
                    else:
                        os.replace(source, target / filename)
                        fsync_directory(source.parent)
                        self._scan_forget(filename)
                    fsync_directory(target)
                    # A delta, as an append writes one: a recount re-reads every queued op, per
                    # request. A dead letter's count is the drain's to rewrite, like every status number.
                    if source is not None and source.parent == self.ops_dir:
                        self._write_status_locked(
                            recount=False,
                            pending_delta=-1,
                            pending_bytes_delta=-int((op.get("upload") or {}).get("size_bytes") or 0),
                        )
                    elif source is not None:
                        self._record_dead_letters()
                return self.delivery_state(correlation)
        finally:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            finally:
                handle.close()

    def discard_held(self, *, credential: str | None = None) -> int:
        """`discard_held_counts`, returning how many moved."""
        return self.discard_held_counts(credential=credential).writes

    def discard_held_counts(self, *, credential: str | None = None) -> DiscardCounts:
        """Move to ``discarded/`` the PENDING ops, in this queue and those under it, that no
        credential on this machine will send as things stand: a stored login's write whose account
        is unknown or another account's, or one whose own login the API refused while still the
        stored one (#2041 round 3/4). Nothing a live process could still deliver is touched:
        another job's `PROBE_TOKEN` or in-code writes stay (that job sends them) and a login whose
        account `/v1/me` cannot confirm now is not "held". ``credential`` names a fingerprint (as
        `probe outbox drain` prints it): then that credential's queued writes go too, which is how
        a stranded job's writes are dropped on purpose. An unstamped op is never touched. Returns
        what moved (`DiscardCounts`). Each queue's drain lock is taken, so no pass is mid-way
        through them, and a run a pass is sending with that lock let go (#3618) is left. A
        credential queue's writes go to the root's ``discarded/`` (`_discard_dir`), and a
        credential whose writes all went no longer reads as refused."""
        counts = DiscardCounts()
        for queue in self.namespaces():
            counts.merge(queue._discard_held_here(credential))
        return counts

    def _discard_held_here(self, credential: str | None) -> DiscardCounts:
        from ...settings.settings import load_context

        counts = DiscardCounts()
        if not self.ops_dir.exists():
            return counts
        status = Journal.read_status(self.dir, include_receipts=False) or {}
        refused = status.get("refused_fingerprints") or {}
        handle = self.drain_lock.open("a+")
        try:
            if not _take_drain_lock(handle, wait_for_lock=True, timeout=30.0):
                return counts
            held: list[Path] = []
            adopted_here: dict = {}
            queued = self._read_dir(self.ops_dir)
            # One token is one account, as in `drain`.
            accounts: dict[str, tuple[str, str]] = {}
            for _path, queued_op in queued:
                queued_stamp = (queued_op.get("context") or {}).get("principal")
                queued_as = stamp_identity(queued_stamp) if isinstance(queued_stamp, dict) else None
                if queued_as is not None:
                    accounts.setdefault(str(queued_stamp.get("fingerprint")), queued_as)
            for path, op in queued:
                stamp = (op.get("context") or {}).get("principal")
                if not isinstance(stamp, dict) or not stamp.get("fingerprint"):
                    continue
                if credential and credential in (stamp.get("fingerprint"), stamp.get("ingest_fingerprint")):
                    held.append(path)  # named by the user
                    continue
                fingerprint, ingest = op_credential(op)
                if fingerprint not in adopted_here:
                    adopted_here[fingerprint] = adopted_account(fingerprint) is not None
                adopted = not ingest and adopted_here[fingerprint]
                if stamp.get("source") != CredentialSource.CONFIG and not adopted:
                    continue  # another job's: that job sends it
                if ingest:
                    continue
                if fingerprint in refused and not adopted:
                    try:
                        stored = load_context((op.get("context") or {}).get("name"))
                    except Exception:  # noqa: BLE001
                        stored = {}
                    if credential_fingerprint(stored.get("token"), None) == fingerprint:
                        held.append(path)  # its login was refused and is still the stored one
                    continue
                try:
                    _settings_for_op(
                        op.get("context"),
                        ingest=False,
                        account=accounts.get(fingerprint) or recorded_account(fingerprint),
                    )
                except CredentialNotHere as absent:
                    if absent.permanent:
                        held.append(path)
                except Exception:  # noqa: BLE001 -- logged out, unroutable: not "held"
                    continue
            # A run a drain is sending now, its drain lock let go for an upload (#3618), stays:
            # that drain settles its files after.
            lanes = {path: _lane_of(op) for path, op in queued}
            probe = _DrainHold(self, handle, urgent=False)
            try:
                held = [path for path in held if not probe.busy(lanes.get(path))]
            finally:
                probe.close()
            if not held:
                return counts
            by_path = dict(queued)
            target = self._discard_dir()
            with file_lock(self.append_lock):
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path in held:
                    try:
                        os.replace(path, target / path.name)
                    except FileNotFoundError:
                        continue  # delivered meanwhile
                    self._scan_forget(path.name)
                    counts.add(by_path.get(path))
                fsync_directory(target)
                fsync_directory(self.ops_dir)
                gone = set(held)
                emptied = {op_credential(op)[0] for path, op in queued if path in gone and isinstance(op, dict)}
                emptied -= {op_credential(op)[0] for path, op in queued if path not in gone and isinstance(op, dict)}
                try:
                    written = json.loads(self.status_file.read_text()).get("refused_fingerprints") or {}
                except (OSError, ValueError, AttributeError):
                    written = {}
                self._write_status_locked(
                    held=0,
                    close_held=0,
                    held_at=None,
                    # A credential with nothing left here is refused nothing.
                    refused_fingerprints={fp: at for fp, at in dict(written).items() if fp not in emptied},
                )
        finally:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            finally:
                handle.close()
        self.gc_blobs()
        return counts

    def clear_auth_block(self) -> None:
        """Forget a recorded auth block (after re-login / explicit retry) so the wake-on-enqueue
        drainer spawns again (codex: nothing cleared it, so delivery stayed stopped forever after
        one 401)."""
        for child in self.namespaces()[1:]:
            child.clear_auth_block()
        self.write_status(auth_blocked_since=None, refused_fingerprints={}, held=0, close_held=0, held_at=None)
        try:  # a worker sleeping on held runs looks again now (outbox_worker._wake_stamp)
            write_text_atomic(self.dir / ".wake", now_iso() + "\n", mode=0o600)
        except OSError:
            pass

    def retry_failed(
        self, op_id: str | None = None, *, run_ref: str | None = None
    ) -> int:
        """Requeue dead letters (one op, one run's, or all). Files keep their names, so a retried
        op re-enters at its original FIFO position."""
        children_moved = sum(
            child.retry_failed(op_id, run_ref=run_ref) for child in self.namespaces()[1:]
        )
        moved = 0
        with file_lock(self.append_lock):
            for path, op in self._read_dir(self.failed_dir):
                if op_id is not None and op.get("op_id") != op_id:
                    continue
                if run_ref is not None and op.get("run_ref") != run_ref:
                    continue
                if "first_failed_at" in op:
                    # A human asked for another try: the transient budget's clock restarts, or an op
                    # dead-lettered by the budget would be dead-lettered again by its first failure.
                    op.pop("first_failed_at", None)
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                os.replace(path, self.ops_dir / path.name)
                moved += 1
            if moved:
                fsync_directory(self.ops_dir)
                fsync_directory(self.failed_dir)
                self._write_status_locked()
                self._record_dead_letters()
        return moved + children_moved

    # -- status -------------------------------------------------------------
    @staticmethod
    def _count_dir(directory: Path) -> tuple[int, str | None]:
        """(count, first filename) without parsing op bodies. Runs on EVERY append, so it must
        stay O(directory listing), not O(total bytes queued) (perf review: a training loop
        enqueuing offline was O(N^2))."""
        if not directory.exists():
            return 0, None
        names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
        return len(names), names[0] if names else None

    def _write_status_locked(
        self,
        *,
        unstaged_low_disk: int = 0,
        recount: bool = True,
        pending_delta: int = 0,
        pending_bytes_delta: int = 0,
        enqueued_at: str | None = None,
        set_pending: int | None = None,
        known: dict | None = None,
        sync: str = SYNC_FULL,
        new_dead_letters: list | None = None,
        **extra: Any,
    ) -> int:
        """Rewrite status.json; returns the pending count it wrote. ``recount=False`` is the
        APPEND path. ``set_pending`` (with ``recount=False``) stores a count the caller just took
        from a directory listing, without re-parsing any op body.

        A recount lists the directories (names only) and parses only the op files ``known``
        (`op_meta`: name -> (size_bytes, enqueued_at), taken by the caller OUTSIDE the lock) does
        not cover: the tail appended since (plan 1.9). A drain pass re-parsed the whole queue here
        holding the append lock, so every `log()` waited: 3.3 s at 20k ops.

        Counts used to come from ``_count_dir`` on every append, and that listdir made N enqueues
        O(N^2 log N): 1.19ms/append at depth 1 rising to 6.50ms at 8k, the queue slower to write
        as the outage it survives got longer. ``_count_dir`` claimed O(1) because it stopped
        PARSING bodies; the LISTING was still O(N).

        So an append carries its own delta forward instead of recounting, and the DRAIN (which
        already walks both directories) writes the authoritative numbers. status.json is
        banner-grade (see ``read_status``): a count briefly off after a hard kill is acceptable;
        a training loop slowing under backlog is not.
        """
        previous: dict = {}
        try:
            previous = json.loads(self.status_file.read_text())
        except (OSError, json.JSONDecodeError):
            pass
        if recount:
            names = (
                sorted(n for n in os.listdir(self.ops_dir) if n.endswith(".json"))
                if self.ops_dir.exists()
                else []
            )
            pending_count = len(names)
            failed_count, _ = self._count_dir(self.failed_dir)
            pending_bytes = 0
            oldest = None
            for index, name in enumerate(names):
                meta = (known or {}).get(name)
                if meta is None:
                    try:
                        meta = _meta_of(json.loads((self.ops_dir / name).read_text()))
                    except (OSError, json.JSONDecodeError, ValueError, AttributeError):
                        meta = (0, None)
                pending_bytes += meta[0]
                if index == 0:
                    oldest = meta[1]
        else:
            pending_count = (
                max(0, set_pending)
                if set_pending is not None
                else max(0, int(previous.get("pending") or 0) + pending_delta)
            )
            failed_count = int(previous.get("failed") or 0)
            pending_bytes = max(0, int(previous.get("pending_bytes") or 0) + pending_bytes_delta)
            oldest = previous.get("oldest_pending")
            if pending_count == 0:
                oldest = None
            elif not oldest and pending_delta > 0:
                # First op onto an empty queue: this append IS the oldest.
                oldest = enqueued_at
        status = {
            "schema": SCHEMA,
            "updated_at": now_iso(),
            "pending": pending_count,
            "pending_bytes": pending_bytes,
            "failed": failed_count,
            "oldest_pending": oldest,
            "paused": self.paused,
            "auth_blocked_since": previous.get("auth_blocked_since"),
            # Per-credential refusals (#2041 review): fingerprint -> when the API last refused it.
            # Carried like the block above.
            "refused_fingerprints": previous.get("refused_fingerprints") or {},
            # Ops the last drain pass had to leave held (another credential, a refused one, a close
            # waiting on another queue) and when: a kick adding nothing deliverable need not fork a
            # worker (#2041 round 3). Carried like the fields around it.
            "held": int(previous.get("held") or 0),
            # Of those, closes waiting on their run's writes in another queue
            # (at most CLOSE_HOLD_MAX_SECONDS): held, but not stuck.
            "close_held": int(previous.get("close_held") or 0),
            "held_at": previous.get("held_at"),
            "last_error": previous.get("last_error"),
            # Monotonic tally of uploads that DEGRADED to unstaged for want of disk headroom,
            # carried forward like the fields above. Counting by scanning ops would make every
            # append O(queue), the regression the O(1) status rewrite fixed.
            "unstaged_low_disk": (
                int(previous.get("unstaged_low_disk") or 0) + int(unstaged_low_disk)
            ),
        }
        status.update(extra)
        # scanning disabled: if recount or extra:
            # An APPEND's status carries only numbers, timestamps this module minted and fields
            # copied from the previous status.json, scrubbed when written: scrubbing again was one
            # of four full scrubs per `log()` (plan 1.3). New text arrives only through `extra` or
            # a drain's recount.
            # scanning disabled: status = default_scrub(status)
        if new_dead_letters:
            self._record_dead_letters(new_dead_letters)
        # Compact: `indent=` takes json's pure-Python encoder and every append rewrites this
        # file (review of #2055).
        write_text_atomic(
            self.status_file, json.dumps(status, separators=(",", ":")) + "\n", mode=0o600,
            sync=sync
        )
        return pending_count

    @property
    def dead_letters_file(self) -> Path:
        return self.dir / "dead_letters.json"

    def recent_dead_letters(self) -> list[dict]:
        """The last `_RECENT_DEAD_LETTERS` dead letters (`{run_ref, op_id, error, status}`, errors
        redacted at the source) for a training process to say so while it runs (plan 1.7). Their
        own file, written only by the drain and the dead-letter commands: in status.json every
        append re-read and rewrote them (review of #2055: 15 KB, 179 -> 511 us)."""
        try:
            records = json.loads(self.dead_letters_file.read_text())
        except (OSError, ValueError):
            return []
        return [r for r in records if isinstance(r, dict)] if isinstance(records, list) else []

    def _record_dead_letters(self, new: list[dict] | None = None) -> None:
        """Append ``new`` and forget entries whose op is no longer a dead letter (retried or
        discarded). Under the append lock."""
        try:
            present = {
                name for name in os.listdir(self.failed_dir) if name.endswith(".json")
            } if self.failed_dir.exists() else set()
        except OSError:
            present = None
        kept = self.recent_dead_letters() + list(new or [])
        if present is not None:
            # A record names its op, not its file: keep those whose op id still names a file in
            # failed/ (the name ends in "-<op_id>.json").
            ids = {name.rsplit("-", 1)[-1][: -len(".json")] for name in present}
            kept = [r for r in kept if str(r.get("op_id")) in ids]
        kept = kept[-_RECENT_DEAD_LETTERS:]
        try:
            if kept:
                write_text_atomic(
                    self.dead_letters_file,
                    json.dumps(kept, separators=(",", ":")) + "\n",
                    mode=0o600,
                    sync=SYNC_NONE,
                )
            else:
                self.dead_letters_file.unlink(missing_ok=True)
        except OSError:
            pass

    def write_status(self, **extra: Any) -> None:
        self._ensure()
        with file_lock(self.append_lock):
            self._write_status_locked(**extra)

    @staticmethod
    def read_status(
        directory: str | Path | None = None,
        *,
        include_receipts: bool = True,
        credential_queues: bool = True,
        keep_idle_refusals: bool = False,
        _pause: bool = True,
    ) -> dict | None:
        """Banner-grade counts, including the fenced delivery namespace and (``credential_queues``)
        every credential queue under this root. A queue holding no writes reads with no refusal and
        nothing held (`_forget_idle_refusals`), each judged on its own before any is folded in.
        ``keep_idle_refusals``: the file as written, for the drain, whose cooldowns count from
        those stamps. ``_pause``: read the pause marker (outermost call only; folded queues' copy
        is never used)."""
        root = Path(directory).expanduser() if directory else default_dir()
        path = root / "status.json"
        try:
            status = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError, ValueError):
            status = None
        if isinstance(status, dict):
            if not keep_idle_refusals:
                _forget_idle_refusals(status, root)
            status.update(_blocked_marker(status))
        if include_receipts and root.name != DELIVERY_NAMESPACE:
            child = Journal.read_status(root / DELIVERY_NAMESPACE, include_receipts=False, _pause=False)
            if child:
                status = dict(status or {})
                for field in ("pending", "pending_bytes", "failed", "held"):
                    status[field] = int(status.get(field) or 0) + int(child.get(field) or 0)
                status.update(_older_block(status, child))
                status["delivery_pending"] = int(child.get("pending") or 0)
                status["delivery_failed"] = int(child.get("failed") or 0)
                status["delivery_pending_bytes"] = int(child.get("pending_bytes") or 0)
                status["delivery_paused"] = _pause and _pause_marker(root / DELIVERY_NAMESPACE) is not None
                status["delivery_last_error"] = child.get("last_error")
                status["auth_blocked_since"] = status.get("auth_blocked_since") or child.get(
                    "auth_blocked_since"
                )
        if root.name != DELIVERY_NAMESPACE:
            waiting = Journal.count_waiting(root)
            if waiting or status is not None:
                status = dict(status or {})
                status["waiting"] = waiting
        if (
            include_receipts
            and credential_queues
            and root.name != DELIVERY_NAMESPACE
            and root.parent.name != CREDENTIAL_NAMESPACE
        ):
            # The credential queues (#2035) count toward the root's banner.
            for path in _credential_queue_dirs(root):
                child = Journal.read_status(path, include_receipts=True, _pause=False)
                if not child:
                    continue
                status = dict(status or {})
                # `held`: writes a drain set aside for a credential nothing here can send; a held
                # queue under an empty root is still a backlog.
                for field in ("pending", "pending_bytes", "failed", "waiting", "held"):
                    status[field] = int(status.get(field) or 0) + int(child.get(field) or 0)
                oldest = [v for v in (status.get("oldest_pending"), child.get("oldest_pending")) if v]
                status["oldest_pending"] = min(oldest) if oldest else None
                status.update(_older_block(status, child))
                status["auth_blocked_since"] = status.get("auth_blocked_since") or child.get(
                    "auth_blocked_since"
                )
                child_refused = child.get("refused_fingerprints")
                if isinstance(child_refused, dict) and child_refused:
                    # A refused credential's queue is the one holding its writes: the root's banner
                    # must see it (`auth_blocked_since`).
                    merged = dict(status.get("refused_fingerprints") or {})
                    for fp, at in child_refused.items():
                        merged[fp] = min(str(at), str(merged[fp])) if merged.get(fp) else at
                    status["refused_fingerprints"] = merged
                status["last_error"] = status.get("last_error") or child.get("last_error")
        if status is not None and _pause:
            # From the marker, never status.json: a pause that ran out is over, whatever the last
            # status write saw.
            pause = _pause_in_effect(root)
            status["paused"] = pause is not None
            status["paused_until"] = pause["until"] if pause else None
            if "delivery_paused" in status:
                status["delivery_paused"] = bool(status["delivery_paused"] or pause)
        return status

    # -- blob store ---------------------------------------------------------
    def blob_path(self, op: dict) -> Path | None:
        upload = op.get("upload") or {}
        if not upload.get("staged"):
            return None
        if upload.get("blob"):
            return self.blobs_dir / upload["blob"]
        return self.blobs_dir / f"incoming-{op['op_id']}"

    def gc_blobs(self, *, staging_grace_seconds: float = 86_400.0) -> int:
        """Drop blobs no live or dead op references. Liveness is computed, not counted:
        crash-safe by construction. The reference scan runs INSIDE the append lock (codex: a stale
        reference set computed before the lock could delete a blob published while gc waited).
        Crash-orphaned ``.staging-*`` files older than the grace window are swept too, so an
        interrupted enqueue cannot leak a multi-GB snapshot forever."""
        children_removed = sum(
            child.gc_blobs(staging_grace_seconds=staging_grace_seconds)
            for child in self.namespaces()[1:]
        )
        if not self.blobs_dir.exists():
            return children_removed
        removed = 0
        with file_lock(self.append_lock):
            referenced: set[str] = set()
            for _, op in self.pending() + self.failed():
                upload = op.get("upload") or {}
                if upload.get("staged"):
                    # BOTH possible names stay referenced: mid-drain, an op whose digest was just
                    # persisted may still hold its bytes under the incoming staging name (red team).
                    referenced.add(f"incoming-{op['op_id']}")
                    if upload.get("blob"):
                        referenced.add(upload["blob"])
            # An interrupted append can publish the intent before the op file. Preserve that
            # immutable snapshot until a terminal receipt exists.
            if self.receipt_enabled:
                for intent_path in self.intents_dir.glob("*.json"):
                    intent = self._read_record(intent_path)
                    if (
                        intent
                        and not (self.dir / "discarded" / intent["op"]["queue_filename"]).exists()
                    ):
                        upload = intent["op"].get("upload") or {}
                        if upload.get("blob"):
                            referenced.add(upload["blob"])
            cutoff = time.time() - staging_grace_seconds
            for path in self.blobs_dir.iterdir():
                # `in`, not `startswith`: snapshot_file writes its temp as `.{dst.name}.{uuid}.tmp`,
                # so staging a blob named `.staging-<op>` yields `..staging-<op>.<uuid>.tmp`, a
                # DOUBLED dot the prefix test missed and the dotfile skip below swallowed. A SIGKILL
                # mid-copy leaked a checkpoint-sized file nothing would collect, the case the grace
                # sweep exists for. Blob names are hex digests, so they cannot collide with this.
                if ".staging-" in path.name:
                    try:
                        if path.stat().st_mtime < cutoff:
                            path.unlink(missing_ok=True)
                            removed += 1
                    except OSError:
                        pass
                    continue
                if path.name.startswith("."):
                    continue
                if path.name not in referenced:
                    path.unlink(missing_ok=True)
                    removed += 1
        return removed + children_removed

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
from probe.sdk.delivery.journal.failures.discards import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    DiscardCounts,
    WAITING_STATES,
    _NO_SUCH_RUN_LETTER,
    _STALE_EPOCH_LETTER,
)
from probe.sdk.delivery.journal.failures.failures import SCAN_CACHE_MAX_BYTES, _RECENT_DEAD_LETTERS  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.headroom import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    MAX_PENDING_OPS,
    MIN_FREE_BYTES,
    OutboxFull,
    _RECOUNT_EVERY_SECONDS,
    _STATVFS_EVERY,
    free_floor,
)
from probe.sdk.delivery.journal.item_locks import _item_lock, _retire_lock, _try_lock, _write_private  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.paths import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _UNUSABLE_LOCK_ERRNOS,
    _credential_queue_dirs,
    _fallback_roots,
    default_dir,
    default_root,
    trusted_dir,
)
from probe.sdk.delivery.journal.producers import _GAPS_KEPT  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.run_ops import RunOps  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.status_file import _blocked_marker, _forget_idle_refusals, _older_block  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _run_exists_now  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import unplaced_experiment_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CATALOG_MANIFEST,
    CREDENTIAL_NAMESPACE,
    DELIVERY_NAMESPACE,
    DELIVERY_SCHEMA,
    SCHEMA,
    TAKEOVER_HOLD_KEY,
    _lane_of,
    _meta_of,
    _read_op_file,
    _safe_component,
    op_meta,
    run_ref_for_path,
)
from probe.sdk.delivery.outbox.drain.accounts import recorded_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import adopted_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CredentialSource,
    _settings_for_op,
    credential_fingerprint,
    op_credential,
    stamp_identity,
)
from probe.sdk.delivery.outbox.drain.lock import _DrainHold, _take_drain_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.report import CredentialNotHere  # noqa: E402 -- pieces need each other; the front door loads this one first
