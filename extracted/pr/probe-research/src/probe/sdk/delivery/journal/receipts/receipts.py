"""ReceiptsMixin: delivery-v1 receipts -- correlate a write, replay it, record its receipt, recover interrupted appends."""

from __future__ import annotations

from contextlib import closing, contextmanager
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from typing import Any

from probe.foundation.os_backend import os_backend as oscompat
from probe.foundation.durable.durable import file_lock, fsync_directory, now_iso, write_text_atomic
from probe.sdk import errors
from probe.sdk.artifact.hashing import fingerprint
from probe.sdk.secret_gate import check_upload


class ReceiptsMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

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
from probe.sdk.delivery.ops.ops import CREDENTIAL_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import DELIVERY_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import DELIVERY_SCHEMA  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.headroom import OutboxFull  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.receipts.index import RECEIPT_INDEX_VERSION  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.uploads import snapshot_file  # noqa: E402 -- pieces need each other; the front door loads this one first
