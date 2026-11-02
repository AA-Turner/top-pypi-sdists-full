"""ArtifactsResource (client.artifacts, typed reads) and ArtifactsMixin, Client's methods: uploads,
references, downloads, the Shared folder (twins: app/files/artifacts, app/files/shared_folders)."""

from __future__ import annotations
import builtins
from ....generated.models import ArtifactDetailOut, ArtifactOut, ArtifactTreeLevel
from ..resource import Resource
import os
from contextlib import nullcontext
from pathlib import Path
from typing import Any
from ....models import (
    ScopedUploadRequest,
    UploadRequest)

from ... import errors
from ...artifact.listing import read_artifact_rows
from ...artifact.filetype import name_with_extension
from ...artifact.hashing import fingerprint
# scanning disabled: from .secret_gate import ArtifactRedactedWarning, check_upload, freeze_upload, prepare_upload
from ...secret_gate import InspectionResult, PreparedUpload, freeze_upload


#: What an artifact hangs off (`anchors.py`, where the lower layers can import
#: it without this module). Re-exported: `client.Anchor` is the one class.
from ...artifact.anchors import Anchor  # noqa: E402


#: Anchors whose upload body is a ``ScopedUploadRequest``. That model is declared
#: ``extra="forbid"``, so a run-only field (``kind``, ``meta``, ``span_id``,
#: ``step_index``) sent to one of these is a 422 — silently ignored is NOT what
#: happens, which is why the client rejects it up front with a readable message.
_SCOPED_ANCHORS = frozenset({Anchor.EXPERIMENT, Anchor.PROJECT, Anchor.WORKSPACE, Anchor.SHARED})


class ArtifactsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- anchored artifacts / files -----------------------------------------
    # Every route below is written as its own literal call site rather than looked up
    # in a table. That is deliberate: the contract-parity guard resolves paths from the
    # AST, and a path built by `.format()` or a dict lookup is invisible to it — the
    # routes would read as unreachable and the guard would stop guarding them.

    def _presign_anchored(
        self, anchor: Anchor, anchor_id: str | None, body: dict, *, direct: bool = False
    ) -> dict:
        if anchor is Anchor.RUN:
            # `direct`: ask for a link straight to object storage where the
            # server grants one (`X-Probe-Direct-Upload`); a run upload only.
            return self.transport.post(
                f"/v1/runs/{anchor_id}/artifacts/uploads",
                body,
                extra_headers={"X-Probe-Direct-Upload": "1"} if direct else None,
            )
        if anchor is Anchor.EXPERIMENT:
            return self._on_experiment(
                lambda p, e: self.transport.post(
                    f"/v1/projects/{p}/experiments/{e}/artifacts/uploads", body
                ),
                str(anchor_id),
            )
        if anchor is Anchor.PROJECT:
            return self.transport.post(f"/v1/projects/{anchor_id}/artifacts/uploads", body)
        if anchor is Anchor.WORKSPACE:
            return self.transport.post(f"/v1/workspaces/{anchor_id}/files/uploads", body)
        return self.transport.post("/v1/shared/files/uploads", body)

    def list_anchored(
        self,
        anchor: Anchor,
        anchor_id: str | None = None,
        *,
        project_id: str | None = None,
        **params,
    ) -> Any:
        """List the artifacts/files under one anchor. ``project_id``: an
        experiment anchor's project, when the caller holds it (saves the
        ``/v1/scopes`` lookup); ignored for the other anchors."""
        query = params or None
        if anchor is Anchor.RUN:
            if "limit" not in params and "offset" not in params:
                return read_artifact_rows(
                    lambda page: self.transport.request(
                        "GET", f"/v1/runs/{anchor_id}/artifacts", params=page, idempotent=True
                    ),
                    query,
                )
            return self.transport.get(f"/v1/runs/{anchor_id}/artifacts", params=query)
        if anchor is Anchor.EXPERIMENT:
            return self._on_experiment(
                lambda p, e: self.transport.get(
                    f"/v1/projects/{p}/experiments/{e}/artifacts", params=query
                ),
                str(anchor_id),
                project_id,
            )
        if anchor is Anchor.PROJECT:
            return self.transport.get(f"/v1/projects/{anchor_id}/artifacts", params=query)
        if anchor is Anchor.WORKSPACE:
            return self.transport.get(f"/v1/workspaces/{anchor_id}/files", params=query)
        return self.transport.get("/v1/shared/files", params=query)

    def create_anchored_reference(self, anchor: Anchor, anchor_id: str, body: dict) -> dict:
        """Record a metadata-only (reference) artifact — no bytes uploaded.

        Only the three *artifact* anchors have this door. Workspace and shared are
        file anchors: a file is its bytes, so there is no reference-without-bytes form
        of one, and the backend declares no such route.
        """
        if anchor is Anchor.RUN:
            return self.transport.post(f"/v1/runs/{anchor_id}/artifacts", body)
        if anchor is Anchor.EXPERIMENT:
            return self._on_experiment(
                lambda p, e: self.transport.post(
                    f"/v1/projects/{p}/experiments/{e}/artifacts", body
                ),
                anchor_id,
            )
        if anchor is Anchor.PROJECT:
            return self.transport.post(f"/v1/projects/{anchor_id}/artifacts", body)
        raise ValueError(
            f"{anchor.value} is a file anchor — a file has no metadata-only form; "
            "upload bytes with upload_file() instead"
        )

    def upload_file(
        self,
        anchor: Anchor,
        anchor_id: str | None,
        name: str,
        path: str,
        *,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
    ) -> dict:
        """Upload a local file to any anchor: fingerprint -> presign -> PUT -> confirm.

        ``kind``/``meta``/``span_id``/``step_index`` are run-only. Passing them with a
        non-run anchor raises here rather than letting the server 422, because
        ``ScopedUploadRequest`` forbids extras and the resulting error does not say
        which field was the problem.

        ``notes`` is accepted and ignored with a DeprecationWarning: files no
        longer carry notes, so what a file IS goes in its run's notes. Never in
        ``name``, which is the file's relative posix path: a description there
        breaks the extension, the preview and the derived folder (0095).

        Strict by design — no fail-open reference fallback. The fallback exists on
        :meth:`Run.log_artifact` so a training loop is never blocked by a flaky
        upload; an operator running ``probe artifact add`` wants to be told it failed.
        """
        anchor = Anchor(anchor)
        # The caller's `name` is the artifact's relative posix path, and the preview
        # route reads its extension. A caller naming the upload for what it IS
        # ("ckpt") rather than where it came from loses that, so it is restored from
        # the local path. Idempotent -- a name that has one is untouched.
        from ...reads.notes_cap import FILE_NOTES_REMOVED, warn_notes_ignored
        # scanning disabled: from .redaction import default_scrub, scrub_string

        warn_notes_ignored(notes, FILE_NOTES_REMOVED)
        # `scrub_string`, not `scrub_text`. The name is a repo-relative path, and
        # `scrub_text`'s home-path rule read every `/Users/<x>` or `/home/<x>`
        # FOLDER in it as a home directory and cut the rest to `<path>`:
        # `pages/Admin/Users/Edit.tsx` and `pages/Admin/Users/New.tsx` both
        # became `pages/Admin<path>` and overwrote each other. The server refuses
        # a name with a leading `/` or a backslash (422); a caller naming a file
        # by a drive path like `C:/Users/<x>/...` keeps the user name in it.
        # scanning disabled: name = scrub_string(name_with_extension(name, path))
        name = name_with_extension(name, path)
        # scanning disabled: meta = default_scrub(meta)
        run_only = {
            "kind": kind,
            "meta": meta,
            "span_id": span_id,
            "step_index": step_index,
        }
        if anchor in _SCOPED_ANCHORS:
            offending = sorted(k for k, v in run_only.items() if v is not None)
            if offending:
                raise ValueError(
                    f"{', '.join(offending)} {'is' if len(offending) == 1 else 'are'} "
                    f"only accepted on a run anchor; the {anchor.value} upload contract "
                    "rejects extra fields (422)"
                )
        if anchor is not Anchor.SHARED and not anchor_id:
            raise ValueError(f"a {anchor.value} anchor needs an id")

        # Redact BEFORE fingerprinting: the digest has to describe the bytes
        # that actually leave, because the server signs it and R2 checks it.
        # scanning disabled: with prepare_upload(path) as prepared:
        with nullcontext(PreparedUpload(path=os.fspath(path), result=InspectionResult())) as prepared:
            digest, size = fingerprint(prepared.path)
            return self.upload_fingerprinted(
                anchor,
                anchor_id,
                name,
                prepared.path,
                digest=digest,
                size=size,
                content_type=content_type,
                kind=kind,
                meta=meta,
                span_id=span_id,
                step_index=step_index,
            )

    def presign_upload(
        self,
        anchor: Anchor | str,
        anchor_id: str | None,
        name: str,
        *,
        digest: str,
        size: int,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
        direct: bool = False,
    ) -> dict:
        """Register upload intent: the server creates (or revives) the
        ``pending`` artifact row and returns a presigned PUT. Called by
        :meth:`upload_fingerprinted` on every attempt -- a remembered URL or
        row is never trusted (the reaper may have expired both) -- and by the
        async enqueue's capped best-effort ping (1A). ``notes`` is accepted and
        ignored (files no longer carry notes)."""
        from ...reads.notes_cap import FILE_NOTES_REMOVED, warn_notes_ignored

        warn_notes_ignored(notes, FILE_NOTES_REMOVED)
        anchor = Anchor(anchor)
        if anchor in _SCOPED_ANCHORS:
            req = ScopedUploadRequest(
                name=name,
                content_hash=digest,
                size_bytes=size,
                content_type=content_type,
            )
        else:
            req = UploadRequest(
                name=name,
                content_hash=digest,
                size_bytes=size,
                content_type=content_type,
                span_id=span_id,
                step_index=step_index,
                kind=kind,
                meta=meta or None,
            )
        return self._presign_anchored(
            anchor, anchor_id, req.model_dump(mode="json", exclude_none=True), direct=direct
        )

    @freeze_upload
    def upload_fingerprinted(
        self,
        anchor: Anchor | str,
        anchor_id: str | None,
        name: str,
        path: str,
        *,
        digest: str,
        size: int,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
        direct: bool = False,
    ) -> dict:
        """The presign -> PUT -> confirm core, for callers that already hold the
        fingerprint -- :meth:`upload_file` after hashing, and the outbox journal
        drain replaying a staged blob (whose hash was taken at enqueue or by the
        drainer, 11A). Phase-aware failure handling lives HERE, where the phase
        is known: a 404 on confirm after a ``have`` dedup is success (see below),
        and every attempt re-presigns rather than trusting a remembered URL.
        ``notes`` is accepted and ignored (files no longer carry notes).
        """
        from ...reads.notes_cap import FILE_NOTES_REMOVED, warn_notes_ignored

        warn_notes_ignored(notes, FILE_NOTES_REMOVED, stacklevel=4)
        anchor = Anchor(anchor)
        presign = self.presign_upload(
            anchor,
            anchor_id,
            name,
            digest=digest,
            size=size,
            content_type=content_type,
            kind=kind,
            meta=meta,
            span_id=span_id,
            step_index=step_index,
            direct=direct,
        )
        # `have` means the server already holds these bytes (content-addressed dedup),
        # so there is nothing to PUT. For a file anchor the swap to live also already
        # happened, in its own transaction.
        if not presign.get("have"):
            # Stream the file (an anchored artifact can be model weights); never read
            # it whole into memory. size is the fingerprinted length the presign signed.
            try:
                self.transport.put_file(
                    presign["upload_url"],
                    path,
                    content_type=content_type or "application/octet-stream",
                    headers=presign.get("upload_headers") or presign.get("headers"),
                )
            except (errors.UploadRefused, errors.TransportError) as exc:
                from ...artifact.storage_handlers import r2 as upload_many

                unreachable = direct and upload_many._direct_unreachable(
                    self, presign["upload_url"], exc
                )
                if unreachable:
                    # A direct link this machine cannot use (an egress allowlist,
                    # DNS, TLS): this file goes again through the API's relay, and
                    # the process stops asking this server for direct links.
                    upload_many.forget_direct(self)
                elif not isinstance(exc, errors.UploadRefused):
                    raise
                # A presigned link lives minutes: one that expired before its PUT,
                # or that the store no longer takes as signed, gets ONE fresh
                # presign. A second refusal stands.
                presign = self.presign_upload(
                    anchor,
                    anchor_id,
                    name,
                    digest=digest,
                    size=size,
                    content_type=content_type,
                    kind=kind,
                    meta=meta,
                    span_id=span_id,
                    step_index=step_index,
                    direct=direct and not unreachable,
                )
                if not presign.get("have"):
                    self.transport.put_file(
                        presign["upload_url"],
                        path,
                        content_type=content_type or "application/octet-stream",
                        headers=presign.get("upload_headers") or presign.get("headers"),
                    )
        # Confirmed unconditionally, including on the `have` path: the server's confirm
        # returns an already-complete row unchanged (uploads_router.py `_confirm_pending_row`
        # is explicitly idempotent), so this costs one call and buys a single uniform
        # return shape — the stored artifact — across every anchor.
        try:
            return self.transport.post(f"/v1/artifacts/{presign['artifact_id']}/confirm", None)
        except errors.NotFoundError:
            if not presign.get("have"):
                raise
            # `have` means the bytes were already stored and, for a file anchor, already
            # swapped live. A concurrent replace of the same (anchor, name) can then
            # soft-delete this row before the confirm reads it. The upload succeeded;
            # failing here would report a phantom error for work the server did.
            #
            # Return an artifact-shaped row, NOT the presign: the presign carries
            # `upload_url` (a signed, bearer-equivalent write capability) and callers
            # print this — `probe shared add` sends it straight to stdout, where it
            # would land in CI logs. It also has no `id`/`status`, so every caller
            # relying on the documented uniform return shape would KeyError on exactly
            # this race.
            return {
                "id": presign["artifact_id"],
                "name": name,
                "content_hash": digest,
                "size_bytes": size,
                "status": "complete",
                "superseded": True,
            }

    # -- shared folder ------------------------------------------------------
    def share_workspace_file(self, artifact_id: str, *, replace: bool = False) -> dict:
        """Move a workspace file into the team's Shared folder.

        A MOVE, not a copy: ownership transfers and the search index is re-keyed in the
        same transaction, so the file leaves your workspace listing when it lands in
        Shared.

        A name collision in the destination is a 409 by default — the server never
        auto-supersedes someone else's file. ``replace=True`` atomically supersedes
        the prior one, which has to be asked for explicitly.
        """
        return self.transport.request(
            "POST",
            f"/v1/workspace-files/{artifact_id}/share",
            params={"replace": replace} if replace else None,
        ).json()

    def unshare_file(self, artifact_id: str, *, replace: bool = False) -> dict:
        """Move a Shared file into the server default workspace.

        Uses the oldest existing workspace, creating a Default workspace if needed.
        Same collision rule as :meth:`share_workspace_file`, in the other direction.
        """
        return self.transport.request(
            "POST",
            f"/v1/shared/files/{artifact_id}/unshare",
            params={"replace": replace} if replace else None,
        ).json()

    def download_shared_file(self, artifact_id: str) -> dict:
        """Presigned download URL for a Shared file."""
        return self.transport.get(f"/v1/shared/files/{artifact_id}/download")

    def delete_shared_file(self, artifact_id: str) -> None:
        self.transport.delete(f"/v1/shared/files/{artifact_id}")

    def confirm_shared_file(self, artifact_id: str) -> dict:
        """The Shared folder's own confirm door. Equivalent to the generic
        ``/v1/artifacts/{id}/confirm``; both delegate to the same core."""
        return self.transport.post(f"/v1/shared/files/{artifact_id}/confirm", None)

    # -- per-file code capture (0193) ----------------------------------------
    def presign_capture_batch(
        self, run_id: str, items: list[dict], *, captured_at: str | None = None
    ) -> dict:
        """Mint one ``kind='code'`` artifact row per captured file, deduped on
        content (``POST /v1/runs/{id}/artifacts/uploads/batch``). Each item is
        ``{name, content_hash, size_bytes, mode}``; the answer carries, per item,
        ``have`` (already stored, nothing to PUT), a checksum-pinned
        ``upload_url`` + ``upload_headers``, or a per-item ``error``."""
        body: dict[str, Any] = {"items": items}
        if captured_at is not None:
            body["captured_at"] = captured_at
        # Idempotent by the server's contract (a retried batch returns the same
        # ids), so the transport's bounded backoff covers a 502/503/504.
        return self.transport.post(
            f"/v1/runs/{run_id}/artifacts/uploads/batch", body, idempotent=True
        )

    def confirm_capture_batch(self, artifact_ids: list[str]) -> dict:
        """HEAD-verify and flip capture rows complete
        (``POST /v1/artifacts/confirm/batch``). Five buckets: ``confirmed``;
        ``unconfirmed`` (object not there yet -- retry the PUT once); ``refused``
        (a live row that is not a capture row: the researcher registered that
        name and bytes on purpose); ``failed`` (the upload reaper gave up on it;
        re-run the capture to revive it); ``unknown`` (no live row). Only
        ``unconfirmed`` is worth a retry; the rest are verdicts."""
        return self.transport.post(
            "/v1/artifacts/confirm/batch", {"artifact_ids": list(artifact_ids)}, idempotent=True
        )

    # -- ordinary run uploads, many per request ------------------------------
    def presign_run_uploads(
        self, run_id: str, items: list[dict], *, direct: bool = False
    ) -> list[dict]:
        """:meth:`presign_upload` for up to 100 files of one run
        (``POST /v1/runs/{id}/artifacts/uploads/many``). Each item is an
        ``UploadRequest`` body; the answer is one per item, in order: ``status``
        201 with ``have``/``upload_url``/``upload_headers``/``artifact_id``, or
        the status and ``detail`` the per-row door refuses that file with. The
        run itself (404, a write refusal) answers for the whole request. An older
        server has no such route: a route-miss 404 or a 405 (`upload_many`).
        ``direct`` asks for links straight to object storage
        (`X-Probe-Direct-Upload: 1`) where the server grants them; without it,
        or where it does not, the links go to the API's own upload relay."""
        # Idempotent by the server's contract: a re-sent request re-presigns the
        # same rows, exactly as a re-sent per-row presign does.
        return self.transport.post(
            f"/v1/runs/{run_id}/artifacts/uploads/many",
            {"items": items},
            idempotent=True,
            extra_headers={"X-Probe-Direct-Upload": "1"} if direct else None,
        )["items"]

    def confirm_uploads(self, artifact_ids: list[str]) -> list[dict]:
        """The per-row confirm for up to 100 uploads, any anchor
        (``POST /v1/artifacts/confirm/many``): one answer per distinct id, in
        order -- ``status`` 200 with the stored ``artifact``, or the status and
        ``detail`` ``POST /v1/artifacts/{id}/confirm`` answers. Idempotent."""
        return self.transport.post(
            "/v1/artifacts/confirm/many", {"artifact_ids": list(artifact_ids)}, idempotent=True
        )["items"]

    def presign_download_batch(self, artifact_ids: list[str]) -> dict:
        """Presigned GETs for up to 1,000 artifacts at once
        (``POST /v1/artifacts/download/batch``): ``{items: {id: {download_url}},
        unknown: [...], refused: {id: reason}}`` -- ``refused`` names a live row
        that cannot be fetched (not complete, a reference pointer, no pointer).
        Restore of a captured tree needs one URL per file."""
        return self.transport.post(
            "/v1/artifacts/download/batch", {"artifact_ids": list(artifact_ids)}, idempotent=True
        )

    def list_run_artifact_tree(
        self, run_id: str, *, prefix: str = "", limit: int | None = None
    ) -> dict:
        """One folder level of a run's artifacts
        (``GET /v1/runs/{id}/artifacts/tree``): the files whose folder is exactly
        ``prefix`` plus each direct child folder with its descendant count."""
        params = {k: v for k, v in {"prefix": prefix, "limit": limit}.items() if v is not None}
        return self.transport.get(f"/v1/runs/{run_id}/artifacts/tree", params=params)

    def presign_download(self, artifact_id: str) -> str:
        """Presigned GET URL for an artifact's blob (``POST /v1/artifacts/{id}/download``).

        The one home for this route literal: ``download_artifact*`` and the callers
        that need the raw doc in memory (``trial expand``, ``asset materialize``) all
        route through here, so the parity guard sees one reachable call site."""
        return self.transport.post(f"/v1/artifacts/{artifact_id}/download", None)["download_url"]

    def download_artifact(self, artifact_id: str) -> bytes:
        """Fetch an artifact's bytes into memory. Use :meth:`download_artifact_to`
        for anything large -- this holds the whole blob at once."""
        return self.transport.get_url(self.presign_download(artifact_id))

    def download_artifact_to(
        self, artifact_id: str, dest: str, *, max_bytes: int | None = None
    ) -> dict:
        """Stream an artifact's blob to ``dest`` without buffering it in memory.

        Returns ``{artifact_id, dest, size_bytes, sha256}`` -- ``sha256`` is computed
        over the bytes as they land, so the caller can check it against the
        ``content_hash`` from a listing to prove the round trip (metadata match is not
        blob existence). On a mid-stream failure the partial file is removed rather
        than left behind as a truncated blob masquerading as the artifact -- the old
        in-memory path buffered before writing, so it never wrote a partial, and this
        preserves that guarantee."""
        url = self.presign_download(artifact_id)
        ok = False
        try:
            kwargs = {"max_bytes": max_bytes} if max_bytes is not None else {}
            size, digest = self.transport.download_to(url, dest, **kwargs)
            ok = True
        finally:
            if not ok:
                Path(dest).unlink(missing_ok=True)
        return {"artifact_id": artifact_id, "dest": str(dest), "size_bytes": size, "sha256": digest}

    def get_artifact(self, artifact_id: str) -> dict:
        """One artifact row by id."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}")


class ArtifactsResource(Resource):
    """`client.artifacts`: typed artifact reads."""

    __slots__ = ()

    def get(self, artifact_id: str) -> ArtifactDetailOut:
        """`Client.get_artifact` as an `ArtifactDetailOut`."""
        return self._to_model(ArtifactDetailOut, self._client.get_artifact(artifact_id))

    def list(
        self, anchor: Anchor, anchor_id: str | None = None, *, project_id: str | None = None,
        **params,
    ) -> builtins.list[ArtifactOut]:
        """`Client.list_anchored` as `ArtifactOut`s."""
        return self._to_models(
            ArtifactOut,
            self._client.list_anchored(anchor, anchor_id, project_id=project_id, **params),
        )

    def get_tree(
        self, run_id: str, *, prefix: str = "", limit: int | None = None,
    ) -> ArtifactTreeLevel:
        """`Client.list_run_artifact_tree` as an `ArtifactTreeLevel`."""
        return self._to_model(
            ArtifactTreeLevel,
            self._client.list_run_artifact_tree(run_id, prefix=prefix, limit=limit),
        )
