"""UploadQueueMixin: queue byte uploads (staged, fingerprinted) and keep the content-addressed blob store."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import time
from typing import Callable

from probe.foundation.durable.durable import file_lock, fsync_directory
from probe.sdk.artifact.hashing import fingerprint
from probe.sdk.secret_gate import check_upload, read_source, strict_policy


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


class UploadQueueMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

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
        lane: str | None = None,
    ) -> dict:
        """Queue a byte upload; returns ``{op_id, blob, size_bytes, staged, unstaged_reason}``.

        ``stage`` snapshots the file into the blob store (``inline_hash`` hashes the snapshot, never the
        live file); short of space it degrades to referencing the source, unless ``require_staged``:
        then nothing is queued and ``op_id`` is None. ``defer_scan`` copies into the waiting room and
        returns (``waiting`` True). ``verbatim`` refuses, never masks, a credential. ``blocking=False``
        does not hold the run's close. ``lane`` (optional on disk; an older drainer uses the run's)
        keeps an upload nothing is ordered after out of the run's lane, so its failures never hold
        the run's other writes. DESIGN.md says why each exists."""
        # scanning disabled: meta = default_scrub(meta)
        # `scrub_string`, not `scrub_text`: see `Client.upload`.
        # scanning disabled: name = scrub_string(name)
        if correlation is not None:
            return self._append_correlated_upload(
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
        if lane:
            op["lane"] = lane
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
        staged, publish, digest, size_bytes = self._stage_upload(
            op, src_path, stage=stage, inline_hash=inline_hash, verbatim=verbatim
        )
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

    def _append_correlated_upload(self, **upload) -> dict:
        """A correlated upload goes through the receipt queue (delivery-v1)."""
        queue = (
            self
            if self.receipt_enabled
            else self.for_receipts(self.dir, context=self.context, attribution=self.attribution)
        )
        return queue._receipt_upload(**upload)

    def _stage_upload(
        self, op: dict, src_path: str, *, stage: bool, inline_hash: bool, verbatim: bool
    ) -> tuple[bool, Callable[[], None] | None, str | None, int | None]:
        """Snapshot the file into a staging blob (hashed from the snapshot with ``inline_hash``), or,
        unstaged, hash the file as it sits. Returns (staged, publish, digest, size): ``publish``
        renames the staging blob to its address under the append lock."""
        staged = False
        publish = None
        digest: str | None = None
        size_bytes: int | None = None
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
        return staged, publish, digest, size_bytes

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
            # held/: a write set aside after its run stalled keeps its bytes (outbox/held, R9).
            for _, op in self.pending() + self.failed() + self._read_dir(self.dir / "held"):
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
