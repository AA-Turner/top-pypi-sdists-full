"""CatalogResource (client.catalog, typed reads) and CatalogMixin, Client's methods: checkpoints,
sources, manifests, datasets, provenance, versions, pin impact, upload gc (twin: app/catalog)."""

from __future__ import annotations
from ....generated.models import ArtifactPinImpact, ArtifactVersionOut, SourceListOut, SourceOut
from ..resource import Resource
import os
import warnings
from pathlib import Path
from typing import Any
from ....models import (
    ArtifactVersionCreate,
    UploadGcRequest)
from ...run.readback import readback as _checkpoints
# scanning disabled: from .secret_gate import ArtifactRedactedWarning, check_upload, freeze_upload, prepare_upload
from ...secret_gate import ArtifactRedactedWarning


class CatalogMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- checkpoints (probe.sdk.run.readback.readback) ----------------------------------
    def checkpoint(
        self,
        run_id: str,
        which: str = "latest",
        *,
        callback: str | None = None,
        recoverable: bool = True,
    ) -> dict | None:
        """The run's ``"latest"`` (highest step) or ``"best"`` (``meta.best``)
        checkpoint row, or None. ``recoverable=True`` skips one whose bytes are
        gone: an upload with a file not (yet) stored, or a location known to be
        gone, so ``"latest"`` is the newest save that can be had. A save from a
        range a rewind abandoned (``meta.rewound``) is never picked. Two
        Lightning callbacks each marking a best raise ``AmbiguousCheckpoint``
        unless ``callback=`` names one."""
        row, _files = _checkpoints.find(self, run_id, which, callback=callback, recoverable_only=recoverable)
        return row

    def download_checkpoint(self, checkpoint: dict | str, dest: str | os.PathLike) -> dict:
        """Write a checkpoint's stored files under the folder ``dest`` (a row
        from :meth:`checkpoint`, or its id), each checked against its sha256.
        Raises ``CheckpointNotStored`` naming what is missing, or where a
        location-only checkpoint is, before writing anything."""
        row = self.get_artifact(checkpoint) if isinstance(checkpoint, str) else checkpoint
        result = _checkpoints.download(self, row, dest)
        if result.get("redacted"):
            warnings.warn(
                f"probe: checkpoint {result.get('checkpoint')} has files stored with a credential "
                f"masked, so they differ from what was saved: {', '.join(result['redacted'])}",
                ArtifactRedactedWarning,
                stacklevel=2,
            )
        return result

    # -- the data catalog (plan data-catalog C1-C11; probe.sdk.catalog) -------
    # Datasets, checkpoints and sources as first-class things. These are the
    # plain HTTP calls: they RAISE, for the CLI. The SDK's training-side verbs
    # (`probe.source`, `Run.use_dataset`, `Run.log_dataset`, ...) live in
    # `probe.sdk.catalog`, which warns once and never raises into a job.

    def create_source(self, body: dict) -> dict:
        """``POST /v1/sources``: register an external source (a Hub dataset, a
        bucket, a URL, a base model) or get the one already registered for the
        same canonical uri and revision. ``{id, ref, canonical_key, provider,
        kind, revision, created}``."""
        return self.transport.post("/v1/sources", body)

    def get_source(self, ref: str) -> dict:
        """``GET /v1/sources/{ref}``: one source with its use counts."""
        return self.transport.get(f"/v1/sources/{catalog_path_ref(ref)}")

    def list_sources(self, **params: Any) -> dict:
        """``GET /v1/catalog/sources`` (``q``, ``provider``, ``kind``, ``cursor``, ``limit``)."""
        return self.transport.get("/v1/catalog/sources", params=_present(params))

    def use_in_run(self, run_id: str, body: dict) -> dict:
        """``POST /v1/runs/{run}/uses``: what a run used, with its roles --
        ``{target, roles, share?}`` -- or a training mixture that replaces the
        run's train shares in one transaction, ``{mixture: [{target, share}],
        role}`` (V12)."""
        return self.transport.post(f"/v1/runs/{run_id}/uses", body)

    def put_manifest(self, digest: str, gz: bytes) -> None:
        """``PUT /v1/catalog/manifests/{sha256}``: a folder dataset's manifest,
        gzip JSON, keyed by its identity hash (idempotent: 204 either way)."""
        self.transport.request(
            "PUT",
            f"/v1/catalog/manifests/{digest}",
            content=gz,
            content_headers={"Content-Type": "application/json", "Content-Encoding": "gzip"},
            idempotent=True,
        )

    def host_dataset_uploads(self, name: str, manifest_hash: str) -> dict:
        """``POST /v1/catalog/datasets/uploads`` (C8): which of a manifest's
        files Probe already hosts (``have``) and an upload for each of the rest
        (``uploads: [{content_hash, artifact_id, size_bytes, url + headers +
        confirm | multipart}]``), at most 1,000 per call: ``deferred`` counts the
        ones still to send after these (`catalog.host` asks again). Safe to
        retry: asking again re-answers the same rows and resumes the same
        multipart uploads."""
        return self.transport.post(
            "/v1/catalog/datasets/uploads", {"name": name, "manifest_hash": manifest_hash}, idempotent=True
        )

    def confirm_hosted_blob(self, artifact_id: str, *, shared: bool = False) -> dict:
        """Confirm one hosted blob PUT through the existing confirm doors: the
        Shared folder's own when the upload names it, else the generic one
        (both delegate to the same core)."""
        if shared:
            return self.transport.post(f"/v1/shared/files/{artifact_id}/confirm", None)
        return self.transport.post(f"/v1/artifacts/{artifact_id}/confirm", None)

    def register_dataset(self, body: dict) -> dict:
        """``POST /v1/catalog/datasets``: the next version of a team dataset,
        from a run's file, a reference or hosted bytes, in one request (Q9)."""
        return self.transport.post("/v1/catalog/datasets", body)

    def dataset(self, ref: str) -> dict:
        """``GET /v1/catalog/datasets/{ref}``: one dataset and every version."""
        return self.transport.get(f"/v1/catalog/datasets/{catalog_path_ref(ref)}")

    def list_datasets(self, **params: Any) -> dict:
        """``GET /v1/catalog/datasets`` (``q``, ``project``, ``registered``, ``cursor``, ``limit``)."""
        return self.transport.get("/v1/catalog/datasets", params=_present(params))

    def dataset_files(self, ref: str, *, cursor: str | None = None) -> dict:
        """``GET /v1/catalog/datasets/{ref}/files``: one version's files
        (``{relpath, artifact_id | null, size_bytes, rows, content_hash,
        fingerprint, preview_artifact_id, download: {artifact_id, version} |
        null}``). Bytes come by ``artifact_id`` through
        :meth:`presign_download_batch`, else by ``download`` through
        :meth:`presign_version_download` (an older version of a one-file team
        dataset); a file with neither is kept outside Probe."""
        return self.transport.get(
            f"/v1/catalog/datasets/{catalog_path_ref(ref)}/files", params=_present({"cursor": cursor})
        )

    def list_checkpoints(self, **params: Any) -> dict:
        """``GET /v1/catalog/checkpoints`` (``project``, ``experiment``, ``run``,
        ``best``, ``stored``, ``cursor``, ``limit``): every checkpoint team-wide."""
        return self.transport.get("/v1/catalog/checkpoints", params=_present(params))

    def provenance(self, ref: str, direction: str = "upstream", depth: int = 4) -> dict:
        """``GET /v1/provenance``: the bounded graph up to the sources, or down
        to everything that used ``ref``."""
        return self.transport.get(
            "/v1/provenance", params={"ref": ref, "direction": str(direction), "depth": int(depth)}
        )

    def provenance_steps(self, ref: str) -> dict:
        """``GET /v1/provenance?format=steps``: the methods view, source first."""
        return self.transport.get("/v1/provenance", params={"ref": ref, "format": "steps"})

    # -- artifact versions (an artifact's content history) ------------------
    def list_artifact_versions(self, artifact_id: str) -> list[dict]:
        """The artifact's version chain, newest first.

        An artifact is a named thing in a container; this is the chain of immutable,
        content-addressed versions behind that name. Immutability lives on the version,
        never the artifact, so renames and moves do not break a pin."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/versions")

    def create_artifact_version(
        self,
        artifact_id: str,
        *,
        from_artifact_id: str | None = None,
        uri: str | None = None,
        content_hash: str | None = None,
        size_bytes: int | None = None,
        content_type: str | None = None,
        label: str | None = None,
        meta: dict | None = None,
    ) -> dict:
        """Append the next version. Exactly one source: promote an existing artifact
        (``from_artifact_id``, zero-copy -- pins its hash + uri + size, the R2 object is
        shared, never re-uploaded) or name a pointer directly (``uri``).

        Re-sending content identical to the artifact's current live content is a no-op
        that returns the existing version, so this is safe to retry."""
        if bool(from_artifact_id) == bool(uri):
            raise ValueError("create_artifact_version needs exactly one of from_artifact_id or uri")
        model = ArtifactVersionCreate(
            from_artifact_id=from_artifact_id,
            uri=uri,
            content_hash=content_hash,
            size_bytes=size_bytes,
            content_type=content_type,
            label=label,
            meta=meta,
        )
        return self.transport.post(
            f"/v1/artifacts/{artifact_id}/versions",
            model.model_dump(mode="json", exclude_none=True),
        )

    def presign_version_download(self, artifact_id: str, version: int) -> str:
        """Presigned GET for one version's bytes -- the pin-resolution path.

        The one home for this route literal, mirroring :meth:`presign_download`, so the
        parity guard sees a single reachable call site. A force-deleted version raises
        410 WITH its deletion metadata, so a manifest can tell "deliberately destroyed"
        apart from "never existed"."""
        return self.transport.post(
            f"/v1/artifacts/{artifact_id}/versions/{version}/download", None
        )["download_url"]

    def download_artifact_version(self, artifact_id: str, version: int) -> bytes:
        """Fetch one version's bytes into memory. Use
        :meth:`download_artifact_version_to` for anything large -- this holds the whole
        blob at once."""
        return self.transport.get_url(self.presign_version_download(artifact_id, version))

    def download_artifact_version_to(self, artifact_id: str, version: int, dest: str) -> dict:
        """Stream one version's bytes to ``dest``, hashing as they land. Same partial-file
        guarantee as :meth:`download_artifact_to`: a mid-stream failure removes the file
        rather than leaving a truncated blob that looks like the artifact."""
        url = self.presign_version_download(artifact_id, version)
        ok = False
        try:
            size, digest = self.transport.download_to(url, dest)
            ok = True
        finally:
            if not ok:
                Path(dest).unlink(missing_ok=True)
        return {
            "artifact_id": artifact_id,
            "version": version,
            "dest": str(dest),
            "size_bytes": size,
            "sha256": digest,
        }

    def artifact_pin_impact(self, artifact_id: str) -> dict:
        """Which projects -- and which experiments within them -- pin this artifact's
        versions. What a delete confirmation should show a human before destroying
        something reproducible: not a count, but the work that would break."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/pin-impact")

    def delete_artifact(self, artifact_id: str) -> None:
        """Delete an artifact row."""
        self.transport.delete(f"/v1/artifacts/{artifact_id}")

    def gc_uploads(self, older_than: str) -> dict:
        """Sweep abandoned (never-confirmed) artifact uploads older than
        ``older_than``. Only ever touches pending rows; confirmed artifacts are
        untouched."""
        model = UploadGcRequest(older_than=older_than)
        return self.transport.post("/v1/artifacts/uploads/gc", model.model_dump(mode="json"))


class CatalogResource(Resource):
    """`client.catalog`: typed source and artifact-version reads. Datasets, checkpoints and
    provenance stay dicts: their routes declare no response model."""

    __slots__ = ()

    def get_source(self, ref: str) -> SourceOut:
        """`Client.get_source` as a `SourceOut`."""
        return self._to_model(SourceOut, self._client.get_source(ref))

    def list_sources(self, **params: Any) -> SourceListOut:
        """`Client.list_sources` as a `SourceListOut`."""
        return self._to_model(SourceListOut, self._client.list_sources(**params))

    def list_artifact_versions(self, artifact_id: str) -> list[ArtifactVersionOut]:
        """`Client.list_artifact_versions` as `ArtifactVersionOut`s."""
        return self._to_models(ArtifactVersionOut, self._client.list_artifact_versions(artifact_id))

    def get_pin_impact(self, artifact_id: str) -> ArtifactPinImpact:
        """`Client.artifact_pin_impact` as an `ArtifactPinImpact`."""
        return self._to_model(ArtifactPinImpact, self._client.artifact_pin_impact(artifact_id))

from probe.sdk.client.ids import _present, catalog_path_ref  # noqa: E402 -- pieces need each other; the front door loads this one first
