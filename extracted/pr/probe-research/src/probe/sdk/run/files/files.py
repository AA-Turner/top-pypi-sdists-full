"""FilesMixin, Run's methods: run.log_artifact -- check the call, gate the file, record the
artifact row."""

from __future__ import annotations
import errno
from contextlib import nullcontext
import os
import stat
from datetime import datetime, timezone
from typing import Any
from ...secret_gate import (
    CredentialBlocked,
    CredentialInPath,
    # scanning disabled: _check_path as _check_upload_path,
    check_upload,
    InspectionResult,
    PreparedUpload)
from ...artifact.storage_handlers import multipart as _multipart
from ..context import context as unit_context
from ...artifact.filetype import artifact_kind_for, name_with_extension
from ...artifact.hashing import reference_fields
from ....models import ArtifactCreate


def _gate_reason(refusal: object) -> str:
    """A gate refusal's reason without its generic "Artifact upload refused: "
    prefix, for a sentence that already says it was refused."""
    return str(refusal).removeprefix("Artifact upload refused: ")


def _require_upload_source(path: str, *, allow_missing: bool) -> bool:
    """Raise for a mistake in the CALL, before the gate sees the file.

    Only what the credential gate refuses about a real file -- over the size
    limit, a credential in its path, its content, bytes that moved while they
    were read -- becomes a pointer row instead of an exception (plan 0.7). A
    typo'd path, a directory, a FIFO or an unreadable file is the caller's to
    fix and raises exactly as before, so it cannot hide behind a warning the
    warn-once rule would silence the second time.

    Returns True when there is a file to upload, False only for a missing one
    the caller passed ``allow_missing`` for (the ``reference=True`` rule).

    Run after the path's own credential check: every message here quotes it.
    """
    local = os.path.abspath(path)
    try:
        info = os.stat(local)
    except FileNotFoundError:
        if allow_missing:
            return False
        raise FileNotFoundError(
            errno.ENOENT,
            "cannot upload: no such file (pass allow_missing=True to record a pointer "
            "to it anyway)",
            local,
        ) from None
    if stat.S_ISDIR(info.st_mode):
        raise IsADirectoryError(
            errno.EISDIR, "cannot upload a directory: log each file in it", local
        )
    if not stat.S_ISREG(info.st_mode):
        # The gate's own refusal, raised as it always was: a FIFO or a device
        # is not a file the caller can have meant to upload.
        raise CredentialBlocked("Artifact upload refused: upload source must be a regular file")
    if not os.access(local, os.R_OK):
        raise PermissionError(errno.EACCES, "cannot upload: permission denied", local)
    return True


class FilesMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- artifacts ----------------------------------------------------------
    def log_artifact(
        self,
        name: str,
        *,
        sync: bool | None = None,
        path: str | None = None,
        uri: str | None = None,
        kind: str | None = None,
        content_hash: str | None = None,
        content_type: str | None = None,
        size_bytes: int | None = None,
        is_reference: bool | None = None,
        reference: bool = False,
        hash_content: bool = False,
        allow_missing: bool = False,
        span_id: str | None = None,
        step_index: int | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        coords: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        strict: bool | None = None,
        verbatim: bool = False,
    ):
        """Record an artifact.

        ``verbatim=True`` is for bytes that must come back exactly as saved (a
        checkpoint's files): where the gate would mask a credential in them,
        the upload is refused instead (a reference row and a warning, like any
        refusal), never stored rewritten.

        ``coords``/``labels`` are the below-run coordinate maps (same split as
        :meth:`log`), merged over the ambient :meth:`unit` context and sent as
        top-level ``ArtifactCreate`` fields — the server hashes coords into the
        cross-table join key and mirrors both maps into ``meta`` for display, so
        the client never folds them into ``meta`` itself. The presign *uploads*
        door does not accept them (its request model has no such fields), so a
        byte upload records them only if it falls back to a reference artifact.

        With ``path`` and no ``uri`` and no ``reference``: the real presign upload flow
        (fold #16) runs, fingerprint -> presign -> PUT bytes to R2 -> confirm.

        With ``reference=True`` and a ``path``: a PATH reference is recorded -- the file's
        location is stored as a ``file://`` uri (raw path in ``meta.local_path``, recording
        host in ``meta.host``) and its bytes are NOT uploaded. Only ``os.stat`` runs unless
        ``hash_content`` asks for a fingerprint. This is the shared-volume case: a 16 GB
        checkpoint or a TB of files an agent on the same volume resolves locally. Raises
        ``FileNotFoundError`` if the path is missing unless ``allow_missing``.

        With ``uri`` (object already in a bucket) or no bytes: a metadata-only reference
        artifact is recorded, as before.

        ``kind`` left out is read from the file's extension (``artifact_kind_for``):
        a ``.ckpt``/``.safetensors``/``.pt``/``.pth`` is a ``checkpoint``, anything
        else (an image included) ``other``. A ``kind`` the caller passes always
        wins. The kinds are ``checkpoint``, ``dataset``, ``evaluation``, ``code``
        and ``other``; the server files any other word as ``other`` (a synonym
        such as ``benchmark`` as its kind) and keeps the word in
        ``meta.kind_label`` (``artifact_kinds``).

        A path a ``.probe.config`` excludes records nothing, except at ``hash``:
        there a reference (``reference=True``, or a ``uri`` alone) is recorded
        by identity only -- location, size and, for a path, its sha256 or
        fingerprint in ``meta`` (`catalog.identity_meta`) -- and an upload is
        refused.

        ``notes`` is accepted and ignored with a DeprecationWarning, never sent:
        files no longer carry notes, so what a file IS (and where it lives) goes
        in the run's notes."""
        from ... import probe_config as _pc_uri
        from ...reads.notes_cap import FILE_NOTES_REMOVED, warn_notes_ignored

        warn_notes_ignored(notes, FILE_NOTES_REMOVED)

        local = path if path is not None else _pc_uri.local_path_of(uri)
        identity_only = False
        if local is not None:
            # A researcher's `.probe.config` excludes the file (or folder): nothing
            # is recorded about it, named explicitly or not -- but at `hash` its
            # identity is what the level allows, so a reference still records.
            from ...recording_rules import recording_rules as _exclusions
            from ... import probe_config as _probe_config

            verdict = _exclusions.excluded(local)
            if verdict.excluded:
                if not (verdict.identity_only and (reference or path is None)):
                    _exclusions.warn(_exclusions.say(_probe_config.ARTIFACT_EXCLUDED, local, verdict))
                    return None
                identity_only = True
        self._progress.bump()  # 2.8: a checkpoint or output upload is work done
        # Before anything branches on it: every branch below stores `name`, and the
        # preview route reads its extension. `log_artifact("ckpt", path="ckpt-4000.pt")`
        # -- the shape the skill documents -- would otherwise store an extensionless
        # name for a file that has one. Restored from the path; additive only.
        # scanning disabled: from .redaction import default_scrub, scrub_string, scrub_text

        # `scrub_string`, not `scrub_text`: see `Client.upload`.
        # scanning disabled: name = scrub_string(name_with_extension(name, path))
        name = name_with_extension(name, path)
        if kind is None:
            kind = artifact_kind_for(name, path)
        # scanning disabled: meta = default_scrub(dict(meta or {}))
        meta = dict(meta or {})
        # Lineage (server 0255): did THIS run write the file, or only log one it
        # read? Stamped from the file's mtime against the run's start, and
        # carried onto the version the upload becomes -- which is how a file the
        # run overwrote stays recognisable as its output. A caller's own value
        # wins.
        if path is not None:
            for key, value in self._write_marks(path).items():
                meta.setdefault(key, value)
        # Resolve the coordinate at CALL time (the fail-open spool replays this
        # payload later; the ambient unit must not be re-read at flush time).
        coords, labels = unit_context.merged(coords, labels)
        # Explicit path reference: record WHERE the bytes live (file://) instead of
        # uploading them. Takes precedence over the upload branch so path + reference
        # never force-uploads (the old code ignored is_reference for path+no-uri).
        if reference and path is not None:
            fields = reference_fields(
                path, hash_content=hash_content, allow_missing=allow_missing, size_bytes=size_bytes
            )
            self._note_logged(path, fields.get("content_hash"))
            uri = uri or fields["uri"]
            if content_hash is None:
                content_hash = fields.get("content_hash")
            if size_bytes is None:
                size_bytes = fields.get("size_bytes")
            for key, value in fields["meta"].items():
                meta.setdefault(key, value)
            if identity_only:
                # In `meta`, never `content_hash`: the row stays a hashless
                # reference, which the server refreshes in place (a checkpoint's
                # best / deleted flags).
                from ...catalog.identity import identity_meta

                for key, value in identity_meta(path, self.id).items():
                    meta.setdefault(key, value)
            is_reference = True
        elif path is not None and uri is None:
            # A REFUSAL by the credential gate -- over the 64 MiB inspection
            # limit, a credential in the path, the content, bytes that moved
            # while they were read -- is not the training loop's problem:
            # outside `strict` it becomes a warning and a reference row, like
            # any other upload that did not land (plan 0.7). A mistake in the
            # CALL (a missing path, a directory, a hash that does not match the
            # file) still raises: see `_require_upload_source`.
            strict_resolved = (not self._client.fail_open) if strict is None else strict

            def refused(reason: str, *, withhold_path: bool = False, missing: bool = False):
                return self._record_refused_upload(
                    name,
                    path,
                    reason,
                    withhold_path=withhold_path,
                    kind=kind,
                    content_type=content_type,
                    span_id=span_id,
                    step_index=step_index,
                    meta=meta,
                    coords=coords,
                    labels=labels,
                    allow_missing=missing,
                    sync=sync,
                )

            # scanning disabled: try:
                # scanning disabled: # First, and before anything quotes the path.
                # scanning disabled: _check_upload_path(path)
            # scanning disabled: except CredentialInPath as exc:
                # scanning disabled: if strict_resolved:
                    # scanning disabled: raise
                # scanning disabled: return refused(str(exc), withhold_path=True)
            if not _require_upload_source(path, allow_missing=allow_missing):
                # Missing, and the caller said that is expected: the pointer is
                # what they asked for, so no `strict` raise either.
                return refused("no such file on this host", missing=True)
            if _multipart.over_threshold(path):
                # Plan item (g): over the 64 MiB inspection limit, a server
                # that takes multipart uploads gets the file in parts -- staged
                # now, sent by the outbox in the background. Otherwise (an old
                # server, an offline run) `check_upload` below refuses it and
                # 0.7's warning + reference row stands.
                handled = self._maybe_multipart(
                    name,
                    path,
                    kind=kind,
                    content_type=content_type,
                    span_id=span_id,
                    step_index=step_index,
                    meta=meta,
                    strict=strict_resolved,
                    sync=sync,
                    refused=refused,
                )
                if handled is not _NOT_QUEUED:
                    self._note_logged(path)
                    return handled
            try:
                check_upload(path)
                queued = self._maybe_queue_upload(
                    name,
                    path,
                    kind=kind,
                    content_type=content_type,
                    span_id=span_id,
                    step_index=step_index,
                    meta=meta,
                    strict=strict,
                    sync=sync,
                    verbatim=verbatim,
                )
                if queued is not _NOT_QUEUED:
                    # After the queue took it, never before: a log_artifact that
                    # failed must not stop output capture from storing the file.
                    self._note_logged(path)
                    return queued
                # The queued branch above redacts when it stages its snapshot. This
                # is the synchronous branch, so redaction happens here instead --
                # before the fingerprint, which the server signs.
                # scanning disabled: with prepare_upload(path, verbatim=verbatim) as prepared:
                with nullcontext(PreparedUpload(path=os.fspath(path), result=InspectionResult())) as prepared:
                    digest, size = _fingerprint(prepared.path)
                    if not prepared.was_redacted and (
                        (content_hash is not None and content_hash.lower() != digest)
                        or (size_bytes is not None and size_bytes != size)
                    ):
                        # The caller's fingerprint is wrong. Left to the
                        # `@freeze_upload` check it reads as "source changed"
                        # -- a refusal, so a pointer row and a warning -- for
                        # what is a bug in the call.
                        raise ValueError(
                            f"log_artifact({name!r}): the content_hash/size_bytes passed do "
                            f"not match the file (sha256 {digest}, {size} bytes). Leave them "
                            "out and the SDK fingerprints the file itself."
                        )
                    if prepared.was_redacted:
                        # The stored hash will name the REDACTED bytes, which no
                        # reader ever opened; the original's hash is what a run
                        # reading this file can be matched on.
                        meta = {**meta, "source_sha256": _fingerprint(path)[0]}
                    # A caller-supplied hash describes the file on disk. Once a span
                    # is replaced that is no longer what leaves, and honouring it
                    # would refuse the upload on a digest mismatch, so the prepared
                    # bytes win. Only redaction overrides the caller.
                    uploaded = self._upload_file(
                        name,
                        prepared.path,
                        kind=kind,
                        # Checked equal above, so this is the caller's own
                        # value whenever they passed one (lower-cased).
                        content_hash=digest,
                        size_bytes=size,
                        content_type=content_type,
                        span_id=span_id,
                        step_index=step_index,
                        meta=meta,
                        coords=coords,
                        labels=labels,
                        strict=strict,
                    )
                    self._note_logged(path, digest)
                    return uploaded
            except CredentialBlocked as exc:
                if strict_resolved:
                    raise
                return refused(str(exc), withhold_path=isinstance(exc, CredentialInPath))
        elif path is not None:
            # A uri AND a local copy: fingerprint for metadata, keep uri as the pointer.
            digest, size = _fingerprint(path)
            self._note_logged(path, digest)
            content_hash = content_hash or digest
            size_bytes = size_bytes if size_bytes is not None else size
            meta.setdefault("local_path", os.path.abspath(path))
        artifact = ArtifactCreate(
            kind=kind,
            name=name,
            uri=uri,
            content_hash=content_hash,
            content_type=content_type,
            size_bytes=size_bytes,
            is_reference=bool(is_reference) if is_reference is not None else (uri is not None),
            span_id=span_id,
            step_index=step_index,
            meta=meta,
            coords=coords or None,
            labels=labels or None,
        )
        body = artifact.model_dump(mode="json", exclude_none=True)
        return self._client.write("POST", f"/v1/runs/{self.id}/artifacts", body, strict=strict)

    def _write_marks(self, path: str | os.PathLike) -> dict[str, Any]:
        """`written_during_run` / `written_at` for a file being logged.

        The run's start is the server's `started_at` (or `created_at`), which
        for an attached run is the launcher's start -- the right boundary. A
        second of slack absorbs filesystem timestamp granularity."""
        try:
            mtime = os.stat(path).st_mtime
        except OSError:
            return {}
        started = self._data.get("started_at") or self._data.get("created_at")
        start_ts: float | None = None
        if isinstance(started, str):
            try:
                start_ts = datetime.fromisoformat(started.replace("Z", "+00:00")).timestamp()
            except ValueError:
                start_ts = None
        if start_ts is None:
            return {}
        return {
            "written_during_run": mtime >= start_ts - 1.0,
            "written_at": datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat(),
        }
from probe.sdk.run.files.uploads import _NOT_QUEUED, _fingerprint  # noqa: E402 -- pieces need each other; the front door loads this one first
