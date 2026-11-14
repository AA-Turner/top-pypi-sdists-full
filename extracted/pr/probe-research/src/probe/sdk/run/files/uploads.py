"""UploadsMixin, Run's methods: choose how a file uploads -- multipart, queued in the outbox, or
now -- and record a refused upload as a pointer row."""

from __future__ import annotations
import os
import socket
import time
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ...secret_gate import (
    CredentialBlocked,
    freeze_upload,
    original_upload_path)
from ...artifact.storage_handlers import multipart as _multipart
from ...artifact.filetype import kind_to_send
from ...artifact.hashing import fingerprint, local_file_uri, reference_fields
from ....models import (
    ArtifactCreate,
    UploadRequest)


def _env_async_uploads(*, default: bool) -> bool:
    """`PROBE_ASYNC_UPLOADS` as a tri-state, mirroring `PROBE_ASYNC`.

    A separate knob from write mode on purpose: queueing a metric batch costs
    a few hundred bytes, queueing a checkpoint costs a copy of the checkpoint.
    Someone may reasonably want one and not the other.
    """
    raw = (os.environ.get("PROBE_ASYNC_UPLOADS") or "").strip().lower()
    if not raw:
        return default
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    _diagnostics.warn(f"ignoring unrecognised PROBE_ASYNC_UPLOADS={raw!r}; expected on or off")
    return default

#: Returned by `_maybe_queue_upload` when the upload was NOT queued and the
#: caller must fall through to the synchronous path. Distinct from None, which
#: is a legitimate "queued, no row yet" answer.
_NOT_QUEUED = object()
#: The server's 422 detail when a presign cites a span it has not stored yet (`app/files/artifacts/uploads/anchors/run.py`).
SPAN_NOT_FOUND = "span_id not found for this run"
#: Seconds between the retries of such a presign (7.75 s in all): long enough for a queued span another drain is
#: sending, or a backed-off lane's next try, to land; a file is lost only after the last one.
SPAN_PRESIGN_RETRY_DELAYS = (0.25, 0.5, 1.0, 2.0, 4.0)


class UploadsMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _maybe_multipart(
        self,
        name: str,
        path: str,
        *,
        kind: str,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        strict: bool,
        sync: bool | None,
        refused: Any,
    ):
        """An artifact over 64 MiB, in parts (plan item (g), `sdk/artifact/storage_handlers/multipart/multipart.py`).

        Returns ``_NOT_QUEUED`` when this server or this run cannot take one
        (the caller then refuses it as before: a warning and a reference row);
        None once it is staged and queued -- the call returns at once and the
        outbox sends it in the background, in a lane of its own; or the
        server's answer after a synchronous upload (``sync=True``, ``strict`` --
        which a fail-closed client (``fail_open=False``) is by default -- or a
        client with no queue), which blocks for the whole transfer.

        An offline run (plan 2.12) keeps the pointer: its queue never touches
        the network until `probe sync`, and D12's over-64-MiB rule holds. So
        does a client under ``PROBE_ARTIFACT_OPAQUE_POLICY=block``.
        """
        client = self._client
        if getattr(client, "_drains_by_hand", False):
            return _NOT_QUEUED
        from ... import secret_gate as _gate

        if not _gate.policy().allow_opaque:
            # `PROBE_ARTIFACT_OPAQUE_POLICY=block`: this user asked for nothing
            # that cannot be inspected to leave the machine, and a multipart
            # upload's bytes are stored before anything reads them.
            return _NOT_QUEUED
        try:
            supported = client.supports_feature(_multipart.FEATURE) is True
        except Exception:  # noqa: BLE001 -- unknown is not advertised
            supported = False
        if not supported:
            # Only a server that ADVERTISES `artifact_multipart` gets one --
            # prod ships the doors off (501, not declared) until its verifier
            # runs. Anything else, a features probe that failed included,
            # keeps today's path: the gate refuses the size, and 0.7's
            # warning and reference row stand.
            return _NOT_QUEUED
        fields = {
            "run_id": self.id,
            "name": name,
            "src": path,
            "kind": kind_to_send(kind),
            "content_type": content_type,
            "meta": meta or None,
            "span_id": span_id,
            "step_index": step_index,
        }
        queue = (
            sync is not True
            and not strict
            and getattr(client, "async_writes", False)
            and (sync is not None or _env_async_uploads(default=True))
            and os.path.isfile(path)
        )
        if queue:
            journal = client.journal
            try:
                op = _multipart.build_op(journal, **fields)
            except _multipart.StageRefused as refusal:
                return refused(f"Artifact upload refused: {refusal}")
            except OSError as exc:
                return refused(f"Artifact upload refused: it could not be staged ({exc.strerror})")
            try:
                _multipart.enqueue(journal, op)
            except Exception as exc:  # noqa: BLE001 -- a full outbox is not the loop's problem
                _multipart.release_staged(op["multipart"])
                return refused(f"Artifact upload refused: the outbox could not take it ({exc})")
            self._multipart_ops = [*getattr(self, "_multipart_ops", []), op["op_id"]]
            client._after_enqueue()
            return None
        try:
            return _multipart.upload_now(client, **fields)
        except errors.RosError as exc:
            if strict:
                raise
            return refused(f"Artifact upload refused: the multipart upload failed ({exc})")
        except (OSError, _multipart.StageRefused) as exc:
            if strict:
                raise
            return refused(f"Artifact upload refused: {exc}")

    def _multipart_still_uploading(self) -> list[str]:
        """This run's multipart uploads still queued (plan (g)), by op id."""
        ops = getattr(self, "_multipart_ops", None)
        journal = getattr(self._client, "journal", None) if ops else None
        if not ops or journal is None:
            return []
        try:
            return _multipart.still_uploading(journal, ops)
        except Exception:  # noqa: BLE001 -- a count for a message
            return []

    def _maybe_queue_upload(
        self,
        name: str,
        path: str,
        *,
        kind: str,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        strict: bool | None,
        sync: bool | None,
        verbatim: bool = False,
    ):
        """Queue an artifact upload, or return ``_NOT_QUEUED`` to upload now.

        STAGED-OR-SYNCHRONOUS. The queue is taken only when the outbox actually
        snapshots the bytes. `append_upload` would otherwise degrade to an
        UNSTAGED op that references the live file, which is right at a command
        line and wrong beside a training loop: checkpoint rotation -- write
        ckpt-1000, delete ckpt-900 -- is the normal shape of this workload, and
        an unstaged op whose source rotated either dead-letters or, above the
        inline-hash threshold, uploads different bytes under the caller's name.
        Falling back to the synchronous upload costs latency; the alternative
        costs correctness.

        Synchronous, always, when: the caller said so, `strict` demands a loud
        failure and a real row, the client is not async at all, or the file is
        not a regular file (a FIFO would block the snapshot forever, the guard
        `probe artifact log --async` already carries).
        """
        client = self._client
        if sync is True or not getattr(client, "async_writes", False):
            return _NOT_QUEUED
        if sync is None and not _env_async_uploads(default=True):
            return _NOT_QUEUED
        strict_resolved = (not client.fail_open) if strict is None else strict
        if strict_resolved:
            # strict means "raise, and hand back the row" -- neither of which a
            # queued write can do. Same resolution order as Client.write.
            return _NOT_QUEUED
        try:
            if not os.path.isfile(path):
                return _NOT_QUEUED
            from ...delivery.journal.headroom import INLINE_HASH_MAX_BYTES

            # `require_staged` asks and appends in ONE step. This used to be a
            # separate "is there headroom?" pre-check followed by an append,
            # which is check-then-act: the same free-space measurement is redone
            # inside `append_upload`, and between the two another writer on this
            # journal -- a neighbouring agent session, or this very training loop
            # writing the next checkpoint -- can take the headroom. The pre-check
            # then says yes, the append degrades to an UNSTAGED op referencing
            # the live file, and nothing reads the receipt that says so. That op
            # is precisely what the staged-or-synchronous rule exists to prevent.
            #
            # Atomic collapses the window: either the bytes are snapshotted, or
            # no op was written and we upload below.
            queued = client.journal.append_upload(
                anchor="run",
                anchor_id=self.id,
                name=name,
                src_path=path,
                inline_hash=os.path.getsize(path) <= INLINE_HASH_MAX_BYTES,
                content_type=content_type,
                kind=kind_to_send(kind),
                meta=meta or None,
                span_id=span_id,
                step_index=step_index,
                run_ref=self.id,
                require_staged=True,
                # The credential scan runs later, off this thread: the file is
                # copied into the waiting room and a promoter (the detached
                # worker, a barrier, this process at exit) scans, redacts and
                # fingerprints the copy before it can become an op.
                defer_scan=True,
                verbatim=verbatim,
            )
        except Exception:  # noqa: BLE001 -- a queue that cannot take it is not
            return _NOT_QUEUED  # a reason to lose the artifact; upload it now
        if not queued.get("staged"):
            # Refused for want of headroom, and nothing was appended. Upload it
            # now, while the source is still the only copy we are sure of.
            return _NOT_QUEUED
        if queued.get("waiting"):
            client._promote_waiting_at_exit(self.id)
        client._after_enqueue()
        # None, deliberately: the SDK-wide "this was journaled" answer. A
        # receipt-shaped dict would be worse than nothing here -- harbor reads
        # `is_reference` off the returned row to decide whether bytes landed,
        # so a dict missing that key would mark the capture confirmed with no
        # artifact id. None degrades pessimistically, which is correct.
        return None

    def _record_refused_upload(
        self,
        name: str,
        path: str,
        reason: str,
        *,
        withhold_path: bool,
        kind: str,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        coords: dict[str, Any] | None,
        labels: dict[str, Any] | None,
        allow_missing: bool,
        sync: bool | None,
    ):
        """The row for an upload the gate REFUSED, instead of an exception in
        the caller's training loop (plan 0.7).

        The same shape `_upload_file` writes when an upload fails: a pointer to
        the file (``file://`` uri, ``meta.local_path``, ``meta.host``), its size,
        ``meta.upload = "failed"`` so `check_run` counts the gap, and the
        refusal in ``meta.upload_error`` -- value-free by construction, the gate
        never interpolates a path or a byte into it. No hash: a 70 GB
        checkpoint must not be read to record that it was not uploaded.

        One exception to the pointer: a credential in the PATH
        (``withhold_path``). The path is the thing that must not be stored, so
        the row carries a placeholder instead of it (``CredentialInPath``'s
        whole contract).

        ``sync`` is the caller's: a caller that asked for the row in hand
        (harbor's capture ledger, `sync=True`) gets it back, with its reason,
        instead of a journaled write that returns None.
        """
        if withhold_path:
            fields: dict[str, Any] = {
                "uri": None,
                # NEVER EMPTY: the server refuses a reference with neither a
                # uri nor a meta.local_path (`_validate_reference_coherence`,
                # app/artifacts/schemas.py), and this row is the only record
                # that the file existed.
                "meta": {"local_path": "<withheld: the path looks like it holds a credential>"},
            }
            try:
                fields["size_bytes"] = os.path.getsize(path)
            except OSError:
                pass
        else:
            # `allow_missing` is the caller's own: a source that vanished
            # between the gate and here is as missing as one that never was.
            fields = reference_fields(path, allow_missing=allow_missing)
        row = ArtifactCreate(
            kind=kind,
            name=name,
            uri=fields.get("uri"),
            size_bytes=fields.get("size_bytes"),
            content_type=content_type,
            is_reference=True,
            span_id=span_id,
            step_index=step_index,
            meta={**meta, **fields["meta"], "upload": "failed", "upload_error": reason},
            coords=coords or None,
            labels=labels or None,
        )
        # Recorded BEFORE the warning, as in `_upload_file`: under `-W error` a
        # warning that raised first would lose the only record of the file.
        recorded = self._client.write(
            "POST",
            f"/v1/runs/{self.id}/artifacts",
            row.model_dump(mode="json", exclude_none=True),
            strict=False,
            sync=bool(sync),
        )
        # This method, log_artifact's `refused` closure, log_artifact, the caller.
        self._warn_not_uploaded(name, reason, stacklevel=4)
        return recorded

    def _warn_not_uploaded(self, name: str, reason: str, *, stacklevel: int) -> None:
        """THE warning for an upload that ended as a pointer row -- a gate
        refusal (`_record_refused_upload`) or a failed upload
        (`_upload_file`'s fallback). Once per run per reason: a checkpoint
        saved every N steps must not print the same line N times, and every
        row still carries its own ``meta.upload``/``meta.upload_error``.

        Silent while `_OWN_UPLOAD_WARNING` is set: that caller says what
        happened in its own words, once."""
        if _OWN_UPLOAD_WARNING.get() or reason in self._uploads_warned:
            return
        self._uploads_warned.add(reason)
        _diagnostics.warn(
            f"probe: artifact {name!r} was not uploaded ({reason}); recorded as a reference "
            "to the file instead, and the run continues. Later uploads that fail for the "
            "same reason on this run are recorded the same way without another warning. "
            "Pass strict=True to raise instead.",
            stacklevel=stacklevel + 1,
        )

    @freeze_upload
    def _upload_file(
        self,
        name: str,
        path: str,
        *,
        kind: str,
        content_hash: str,
        size_bytes: int,
        content_type: str | None,
        span_id: str | None,
        step_index: int | None,
        meta: dict,
        coords: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        strict: bool | None = None,
    ):
        """presign -> PUT -> confirm. Fail-open: on failure (and not strict) falls
        back to recording a hash+metadata reference so the training loop is unblocked.

        ``coords``/``labels`` (already merged with the ambient unit by the caller)
        ride only the fallback ``ArtifactCreate``: the presign ``UploadRequest``
        model has no coordinate fields server-side, so sending them there would be
        silently dropped at best and a 422 on a stricter model at worst."""
        strict_resolved = (not self._client.fail_open) if strict is None else strict
        # The upload presign goes straight to the network, but `Run.span` is
        # journaled -- so under async the artifact can reach the server before
        # the span it points at, and the server enforces the foreign key
        # (`span_id not found for this run`, 422). Deliver the queue first so
        # the reference cannot outrun its referent. Only when a span is actually
        # cited, and only on the direct-post path: the metadata-only branch goes
        # through the journal, where FIFO already orders it behind the span.
        self._flush_for_span(span_id)
        req = UploadRequest(
            name=name,
            content_hash=content_hash,
            size_bytes=size_bytes,
            content_type=content_type,
            span_id=span_id,
            step_index=step_index,
            kind=kind_to_send(kind),  # None preserves labels on restage
            meta=meta or None,
        )
        try:
            presign = self._presign_citing_span(req.model_dump(mode="json", exclude_none=True), span_id)
            if not presign.get("have"):
                # Stream the file (model weights fit here); never read it whole into
                # memory. size_bytes is the fingerprinted length the presign signed.
                self._client.transport.put_file(
                    presign["upload_url"],
                    path,
                    content_type=content_type or "application/octet-stream",
                    headers=presign.get("upload_headers") or presign.get("headers"),
                )
            return self._client.transport.post(
                f"/v1/artifacts/{presign['artifact_id']}/confirm", None
            )
        except (errors.RosError, AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
            # Broader than RosError on purpose. `presign` is None for an empty
            # 2xx (a proxy or CDN interstitial), so `.get`/`['artifact_id']`
            # raise AttributeError/KeyError; `put_file` re-opens the file per
            # attempt, so a checkpoint reaped mid-upload raises OSError; a
            # non-JSON 2xx body raises ValueError. Every one of those used to
            # sail past this handler into the training loop, which is precisely
            # what "fail-open" promised it would not do.
            if strict_resolved:
                raise
            # The recovery runs BEFORE the diagnostic. It used to be the other
            # way round, and under `-W error` the warn raised out of the handler
            # so the fallback row was never written -- the run lost the only
            # record of the file, and the message meant to explain the
            # degradation caused a worse one.
            local = os.path.abspath(original_upload_path(path))
            # THE URI NAMES THE ORIGINAL FILE, so the hash beside it must
            # describe that file. `content_hash`/`size_bytes` arrive from
            # `prepare_upload`, so after a redaction they describe bytes that
            # exist nowhere on disk: anyone resolving this pointer on a shared
            # volume and verifying the digest would get a mismatch and conclude
            # the file had been tampered with. Re-fingerprint what the uri
            # actually points at, and say in `meta` why the two differ.
            local_hash, local_size = content_hash, size_bytes
            redacted_hash = None
            try:
                if os.path.abspath(path) != local:
                    redacted_hash = content_hash
                    local_hash, local_size = _fingerprint(local)
            except OSError:
                # The source is gone; keep what we have rather than lose the row.
                local_hash, local_size = content_hash, size_bytes
            fallback = ArtifactCreate(
                kind=kind,
                name=name,
                uri=local_file_uri(local),
                content_hash=local_hash,
                size_bytes=local_size,
                content_type=content_type,
                is_reference=True,
                span_id=span_id,
                step_index=step_index,
                meta={
                    **meta,
                    "local_path": local,
                    "host": socket.gethostname(),
                    "upload": "failed",
                    # The transport's own gate refusing (a source that changed
                    # size mid-upload) says why; value-free by construction.
                    # Other failures keep their old shape: their text can quote
                    # a presigned URL.
                    **({"upload_error": str(exc)} if isinstance(exc, CredentialBlocked) else {}),
                    # Present only when the refused upload had been redacted:
                    # it names the digest of the bytes that WOULD have been
                    # stored, so the two hashes can be told apart later.
                    **({"redacted_content_hash": redacted_hash} if redacted_hash else {}),
                },
                coords=coords or None,
                labels=labels or None,
            )
            recorded = self._client.write(
                "POST",
                f"/v1/runs/{self.id}/artifacts",
                fallback.model_dump(mode="json", exclude_none=True),
                strict=False,
            )
            # The gate's reason is value-free; any other failure's text can
            # quote a presigned URL, so it is named, not quoted.
            self._warn_not_uploaded(
                name,
                str(exc) if isinstance(exc, CredentialBlocked) else "the upload did not complete",
                # _upload_file, its @freeze_upload wrapper, log_artifact, the caller.
                stacklevel=4,
            )
            return recorded

    def _presign_citing_span(self, body: dict, span_id: str | None) -> Any:
        """The presign POST. When it cites a span the server has not stored yet (422 "span_id not found for this
        run") while a span write of this run is still queued (another drain is sending it, its lane is backed off),
        flush the run's spans again and retry after each of `SPAN_PRESIGN_RETRY_DELAYS`. With nothing of the run
        queued the span just landed or never will: one last try at once, then its 422 stands (the caller falls back
        to a reference). Lost rollout files on the 11-13 verl run: 25 of 72."""
        path = f"/v1/runs/{self.id}/artifacts/uploads"
        for delay in SPAN_PRESIGN_RETRY_DELAYS if span_id and self._client.async_writes else ():
            try:
                return self._client.transport.post(path, body)
            except errors.ValidationError as exc:
                if SPAN_NOT_FOUND not in str(exc.detail or exc):
                    raise
            if not self._get_queued_span_ops():
                break
            time.sleep(delay)
            self._flush_for_span(span_id)
        return self._client.transport.post(path, body)


#: One definition, shared with the anchored-upload path in sdk/client/client.py — the hash
#: is part of the wire contract, so two copies could silently diverge.
_fingerprint = fingerprint
from probe.sdk.run.files.code_upload import _OWN_UPLOAD_WARNING  # noqa: E402 -- pieces need each other; the front door loads this one first
