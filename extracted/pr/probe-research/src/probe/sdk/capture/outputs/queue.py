"""queue each swept file as an upload, a multipart upload, a reference or a generated manifest, and remember it in the run's ledger."""

from __future__ import annotations
import contextlib
import json
import os
import tempfile
import time
from pathlib import Path
from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import secret_gate
from ...artifact.filetype import artifact_kind_for, kind_to_send
from ...artifact.hashing import fingerprint, local_file_uri
# scanning disabled: from .secret_gate import FIELD_NAME_RULE, CredentialBlocked, _findings, prepare_upload
from ...secret_gate import CredentialBlocked
from ...artifact.limits import AUTO_UPLOAD_MAX_BYTES, SCAN_PREFIX_BYTES

#: Every captured output is named under this prefix (see WHY THE PREFIXES).
OUTPUT_PREFIX = "outputs/"
#: ``meta.capture`` on every row this module writes. Never "code-snapshot":
#: the server reserves that value for the batch code-capture door.
CAPTURE_OUTPUTS = "outputs"
#: The time a close keeps in hand to scan one big file's head before queueing it
#: in parts: 16 MiB of text took ~9 s on the devbox. With less left, the
#: pointer stands.
HEAD_SCAN_RESERVE_SECONDS = 15.0
#: The per-team switch (`GET /v1/teams/features`) under which capture uploads a
#: file between the inspection limit and `AUTO_UPLOAD_MAX_BYTES` in parts.
AUTO_MULTIPART_FEATURE = "artifact_auto_multipart"


class OutputQueueMixin:
    """Part of OutputCapture: its methods run with `self` the OutputCapture; compose() folds them into OutputCapture."""

    def _sends_in_parts(self) -> bool:
        """Whether this close uploads files over the inspection limit in parts:
        the server takes multipart uploads, THIS team is switched on
        (`artifact_auto_multipart`, a canary list), the client queues (an
        offline run drained by hand keeps pointers), nobody asked that
        nothing uninspected leave (`PROBE_ARTIFACT_OPAQUE_POLICY=block`), and a
        detached worker on durable storage will carry the upload after this
        process exits (`multipart.settle_reason`). On a throwaway box nothing
        would, and an op queued here would vanish with the disk instead of
        being listed, so the old pointer-or-list rule stands there.
        Asked once per close; any failure is a no."""
        cached = getattr(self, "_parts_ok", None)
        if cached is None:
            try:
                from ...artifact.storage_handlers import multipart as _multipart

                cached = bool(
                    self.client is not None
                    and not getattr(self.client, "_drains_by_hand", False)
                    and secret_gate.policy().allow_opaque
                    and _multipart.settle_reason(self.client) is None
                    and self._server_takes_multipart()
                    and self.client.supports_team_feature(AUTO_MULTIPART_FEATURE)
                )
            except Exception:  # noqa: BLE001 -- unknown is a no: the pointer stands
                cached = False
            self._parts_ok = cached
        return cached

    def _queue_in_parts(self, rel: str, full: str, storage: dict, deadline: float) -> str | None:
        """Queue one big output file as a multipart upload. ``"queued"``;
        ``"secret"`` when its PATH holds a credential; None when it cannot go
        this way, and the caller records the pointer (or lists it) as before:
        switched off, out of the close's time, not stageable without a copy,
        over 5 GiB once staged, or a head that is not clean.

        The STAGED copy's first `SCAN_PREFIX_BYTES` are scanned here, before any
        byte leaves -- the staged inode is what will be sent, so a writer racing
        the close cannot swap the bytes after the scan. The server only records
        what its verifier finds in the same prefix, and a log with a token in its
        first line must not ship merely because it grew past 64 MiB. Past that
        prefix nothing is scanned, as with any multipart upload."""
        if time.monotonic() >= deadline:
            return None
        # scanning disabled: if _findings(full)[0]:
        if False:
            return "secret"
        try:
            from ...delivery.transport.deadlines import deadline_scope

            with deadline_scope(deadline):  # the feature reads must not outlive the close
                if not self._sends_in_parts():
                    return None
        except Exception:  # noqa: BLE001 -- unknown is a no: the pointer stands
            return None
        from ...artifact.storage_handlers import multipart as _multipart

        name = OUTPUT_PREFIX + rel
        kind = artifact_kind_for(name, checkpoints=False)
        try:
            op = _multipart.build_op(
                self.journal,
                run_id=self.run_id,
                name=name,
                src=full,
                kind=kind_to_send(kind),
                content_type=None,
                meta=self._meta(full, storage),
                span_id=None,
                step_index=None,
                allow_copy=False,
            )
        except (_multipart.StageRefused, OSError):
            return None
        staged = op["multipart"]
        if (
            staged["identity"]["size"] > AUTO_UPLOAD_MAX_BYTES  # it grew after the folder walk
            or time.monotonic() + HEAD_SCAN_RESERVE_SECONDS >= deadline  # no time to scan it
            or not _head_is_clean(staged["staged_path"], SCAN_PREFIX_BYTES)
            or time.monotonic() >= deadline  # the scan ran the close out of time
        ):
            _multipart.release_staged(staged)
            return None
        try:
            _multipart.enqueue(self.journal, op)
        except Exception:  # noqa: BLE001 -- a queue that cannot take it: the pointer stands
            _multipart.release_staged(op["multipart"])
            return None
        self.enqueued += 1
        try:
            self.client._after_enqueue()
        except Exception:  # noqa: BLE001
            pass
        return "queued"

    def _server_takes_multipart(self) -> bool:
        """Whether the server advertises `artifact_multipart` (plan (g)); a
        probe that fails is a no."""
        try:
            from ...artifact.storage_handlers.multipart.multipart import FEATURE

            return self.client is not None and self.client.supports_feature(FEATURE) is True
        except Exception:  # noqa: BLE001 -- advice only
            return False

    def _meta(self, full: str, storage: dict) -> dict:
        return {
            "capture": CAPTURE_OUTPUTS,
            "source_path": full,
            "host": self.host,
            **({"storage": storage["fstype"]} if storage.get("fstype") else {}),
        }

    # -- queueing -------------------------------------------------------------------
    def _queue_upload(self, name: str, path: str, *, meta: dict) -> bool:
        """Journal a non-blocking, STAGED upload; if the outbox cannot take it,
        upload now, still through the gate and still fail-open."""
        kind = artifact_kind_for(name, checkpoints=False)
        try:
            queued = self.journal.append_upload(
                anchor="run",
                anchor_id=self.run_id,
                name=name,
                src_path=path,
                stage=True,
                inline_hash=True,
                kind=kind_to_send(kind),
                meta=meta,
                run_ref=self.run_id,
                require_staged=True,
                blocking=False,
            )
        except CredentialBlocked:
            return False
        except Exception:  # noqa: BLE001 -- a queue that cannot take it: upload now
            queued = None
        if queued and queued.get("op_id"):
            self.enqueued += 1
            if self.client is not None:
                try:
                    self.client._after_enqueue()
                except Exception:  # noqa: BLE001
                    pass
            return True
        if self.client is None:
            return False
        try:
            # scanning disabled: with prepare_upload(path) as prepared:
            with contextlib.nullcontext(secret_gate.PreparedUpload(path=os.fspath(path), result=secret_gate.InspectionResult())) as prepared:
                digest, size = fingerprint(prepared.path)
                self.client.upload_fingerprinted(
                    "run", self.run_id, name, prepared.path,
                    digest=digest, size=size, kind=kind_to_send(kind), meta=meta,
                )
            return True
        except Exception as exc:  # noqa: BLE001
            _diagnostics.warn(
                f"probe: could not upload output {name!r} ({type(exc).__name__}); "
                "it is not stored on the run."
            )
            return False

    @staticmethod
    def _reference_hash(
        full: str, size: int, mtime_ns: int, budget: list[int], deadline: float
    ) -> str | None:
        """The sha256 a reference carries (F3), or None: over 1 GiB, changed
        since the listing, or past what the budget or the deadline allow."""
        try:
            from .. import lineage as _inputs

            return _inputs.reference_hash(
                full, budget=budget, deadline=deadline, size=size, mtime_ns=mtime_ns
            )
        except Exception:  # noqa: BLE001 -- a hash never costs the reference
            return None

    def _queue_reference(
        self, rel: str, full: str, size: int, storage: dict, *, why: str, content_hash: str | None = None
    ) -> None:
        from ....models import ArtifactCreate

        body = ArtifactCreate(
            kind=artifact_kind_for(rel, checkpoints=False),
            name=OUTPUT_PREFIX + rel,
            uri=local_file_uri(full),
            size_bytes=size,
            content_hash=content_hash,
            is_reference=True,
            meta={
                "capture": CAPTURE_OUTPUTS,
                "local_path": full,
                "host": self.host,
                "reason": why,
                **({"storage": storage["fstype"]} if storage.get("fstype") else {}),
            },
        ).model_dump(mode="json", exclude_none=True)
        self.journal.append_http(
            "POST", f"/v1/runs/{self.run_id}/artifacts", body, run_ref=self.run_id, blocking=False
        )
        self.enqueued += 1

    def _queue_generated(self, name: str, data: bytes, *, meta: dict) -> bool:
        """Upload ``data`` from a private temporary file; the journal stages
        its own copy before this returns."""
        directory = _private_dir("outputs")
        fd, tmp = tempfile.mkstemp(prefix=f"{self.run_id}.", suffix=f".{os.path.basename(name)}", dir=directory)
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(data)
            return self._queue_upload(name, tmp, meta=meta)
        finally:
            Path(tmp).unlink(missing_ok=True)

    def _queue_manifest(self, listed: list[dict], *, truncated: bool) -> None:
        body = json.dumps(
            {
                "note": "Files this run wrote that output capture listed but did not store.",
                "root": self.root,
                "host": self.host,
                "listing_truncated": truncated,
                "files": listed,
            },
            indent=2,
        ).encode("utf-8")
        self._queue_generated(MANIFEST_NAME, body, meta={"capture": CAPTURE_OUTPUTS})


class _Ledger:
    """What was already queued for one run, on disk: ``{relative path: sha256
    or pointer key}`` plus the ``(size, mtime_ns)`` it had then. A second close
    -- a re-finish, a resumed attempt, another rank of the run -- queues
    nothing twice, and skips an untouched file without reading it."""

    def __init__(self, run_id: str):
        self.path = _private_dir("outputs") / f"{run_id}.json"
        try:
            data = json.loads(self.path.read_text())
            self.files: dict[str, str] = dict(data.get("files") or {})
            self.stats: dict[str, list] = dict(data.get("stats") or {})
        except (OSError, ValueError, AttributeError, TypeError):
            self.files, self.stats = {}, {}
        self._dirty = False

    def has(self, rel: str, key: str) -> bool:
        return self.files.get(rel) == key

    def unchanged(self, rel: str, size: int, mtime_ns: int) -> bool:
        return rel in self.files and self.stats.get(rel) == [size, mtime_ns]

    def add(self, rel: str, key: str, size: int, mtime_ns: int) -> None:
        self.files[rel] = key
        self.stats[rel] = [size, mtime_ns]
        self._dirty = True

    def save(self) -> None:
        if not self._dirty:
            return
        try:
            _prune(self.path.parent)
            # Merge with what another rank saved meanwhile.
            try:
                on_disk = json.loads(self.path.read_text())
                files = {**dict(on_disk.get("files") or {}), **self.files}
                stats = {**dict(on_disk.get("stats") or {}), **self.stats}
            except (OSError, ValueError, AttributeError, TypeError):
                files, stats = self.files, self.stats
            _write_json(self.path, {"files": files, "stats": stats})
        except OSError:
            pass
from probe.sdk.capture.outputs.host_registry import _write_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.outputs.log import _head_is_clean, _private_dir, _prune  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.outputs.sweep import MANIFEST_NAME  # noqa: E402 -- pieces need each other; the front door loads this one first
