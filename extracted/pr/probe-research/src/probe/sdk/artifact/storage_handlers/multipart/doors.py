"""MultipartDoors: the server's per-anchor multipart endpoints -- open/create, grant part URLs, status, finish, abort."""

from __future__ import annotations
from typing import Any

from .... import errors
from ...anchors import Anchor


def _anchor_of(upload: dict) -> str:
    """The op's anchor; an op without one is a run's (only runs had these)."""
    return str(upload.get("anchor") or Anchor.RUN.value)


# The doors: one literal path per anchor (the parity guard reads call sites).
# An experiment's live under the project it is filed in NOW, resolved per call.


def _open(client: Any, upload: dict, body: dict) -> Any:
    anchor, ref = _anchor_of(upload), upload.get("anchor_id")
    if anchor == Anchor.RUN.value:
        return client.transport.post(f"/v1/runs/{ref}/artifacts/multipart", body, idempotent=True)
    if anchor == Anchor.PROJECT.value:
        return client.transport.post(
            f"/v1/projects/{ref}/artifacts/multipart", body, idempotent=True
        )
    if anchor == Anchor.EXPERIMENT.value:
        return client._on_experiment(
            lambda p, e: client.transport.post(
                f"/v1/projects/{p}/experiments/{e}/artifacts/multipart", body, idempotent=True
            ),
            str(ref),
        )
    if anchor == Anchor.WORKSPACE.value:
        return client.transport.post(
            f"/v1/workspaces/{ref}/files/multipart", body, idempotent=True
        )
    if anchor == Anchor.SHARED.value:
        return client.transport.post("/v1/shared/files/multipart", body, idempotent=True)
    raise errors.ValidationError(f"a multipart upload has no {anchor!r} anchor", status=422)


def _grant(client: Any, upload: dict, upload_id: str, body: dict) -> Any:
    anchor, ref = _anchor_of(upload), upload.get("anchor_id")
    if anchor == Anchor.RUN.value:
        return client.transport.post(
            f"/v1/runs/{ref}/artifacts/multipart/{upload_id}/parts", body, idempotent=True
        )
    if anchor == Anchor.PROJECT.value:
        return client.transport.post(
            f"/v1/projects/{ref}/artifacts/multipart/{upload_id}/parts", body, idempotent=True
        )
    if anchor == Anchor.EXPERIMENT.value:
        return client._on_experiment(
            lambda p, e: client.transport.post(
                f"/v1/projects/{p}/experiments/{e}/artifacts/multipart/{upload_id}/parts",
                body,
                idempotent=True,
            ),
            str(ref),
        )
    if anchor == Anchor.WORKSPACE.value:
        return client.transport.post(
            f"/v1/workspaces/{ref}/files/multipart/{upload_id}/parts", body, idempotent=True
        )
    if anchor == Anchor.SHARED.value:
        return client.transport.post(
            f"/v1/shared/files/multipart/{upload_id}/parts", body, idempotent=True
        )
    raise errors.ValidationError(f"a multipart upload has no {anchor!r} anchor", status=422)


def _status(client: Any, upload: dict, upload_id: str) -> Any:
    anchor, ref = _anchor_of(upload), upload.get("anchor_id")
    if anchor == Anchor.RUN.value:
        return client.transport.get(f"/v1/runs/{ref}/artifacts/multipart/{upload_id}")
    if anchor == Anchor.PROJECT.value:
        return client.transport.get(f"/v1/projects/{ref}/artifacts/multipart/{upload_id}")
    if anchor == Anchor.EXPERIMENT.value:
        return client._on_experiment(
            lambda p, e: client.transport.get(
                f"/v1/projects/{p}/experiments/{e}/artifacts/multipart/{upload_id}"
            ),
            str(ref),
        )
    if anchor == Anchor.WORKSPACE.value:
        return client.transport.get(f"/v1/workspaces/{ref}/files/multipart/{upload_id}")
    if anchor == Anchor.SHARED.value:
        return client.transport.get(f"/v1/shared/files/multipart/{upload_id}")
    raise errors.ValidationError(f"a multipart upload has no {anchor!r} anchor", status=422)


def _finish(client: Any, upload: dict, upload_id: str) -> Any:
    anchor, ref = _anchor_of(upload), upload.get("anchor_id")
    if anchor == Anchor.RUN.value:
        return client.transport.post(
            f"/v1/runs/{ref}/artifacts/multipart/{upload_id}/complete", idempotent=True
        )
    if anchor == Anchor.PROJECT.value:
        return client.transport.post(
            f"/v1/projects/{ref}/artifacts/multipart/{upload_id}/complete", idempotent=True
        )
    if anchor == Anchor.EXPERIMENT.value:
        return client._on_experiment(
            lambda p, e: client.transport.post(
                f"/v1/projects/{p}/experiments/{e}/artifacts/multipart/{upload_id}/complete",
                idempotent=True,
            ),
            str(ref),
        )
    if anchor == Anchor.WORKSPACE.value:
        return client.transport.post(
            f"/v1/workspaces/{ref}/files/multipart/{upload_id}/complete", idempotent=True
        )
    if anchor == Anchor.SHARED.value:
        return client.transport.post(
            f"/v1/shared/files/multipart/{upload_id}/complete", idempotent=True
        )
    raise errors.ValidationError(f"a multipart upload has no {anchor!r} anchor", status=422)


def _abort(client: Any, upload: dict, upload_id: str) -> Any:
    anchor, ref = _anchor_of(upload), upload.get("anchor_id")
    if anchor == Anchor.RUN.value:
        return client.transport.delete(f"/v1/runs/{ref}/artifacts/multipart/{upload_id}")
    if anchor == Anchor.PROJECT.value:
        return client.transport.delete(f"/v1/projects/{ref}/artifacts/multipart/{upload_id}")
    if anchor == Anchor.EXPERIMENT.value:
        return client._on_experiment(
            lambda p, e: client.transport.delete(
                f"/v1/projects/{p}/experiments/{e}/artifacts/multipart/{upload_id}"
            ),
            str(ref),
        )
    if anchor == Anchor.WORKSPACE.value:
        return client.transport.delete(f"/v1/workspaces/{ref}/files/multipart/{upload_id}")
    if anchor == Anchor.SHARED.value:
        return client.transport.delete(f"/v1/shared/files/multipart/{upload_id}")
    raise errors.ValidationError(f"a multipart upload has no {anchor!r} anchor", status=422)


def _fields(op: dict) -> tuple[dict, dict]:
    upload, state = op.get("upload"), op.get("multipart")
    if (
        not isinstance(upload, dict)
        or not isinstance(state, dict)
        or not (upload.get("anchor_id") or _anchor_of(upload) == Anchor.SHARED.value)
        or not upload.get("name")
        or not state.get("staged_path")
        or not isinstance(state.get("identity"), dict)
    ):
        raise errors.ValidationError(
            f"multipart op {op.get('op_id')} is missing its upload or staging fields", status=422
        )
    return upload, state


def _create(client: Any, upload: dict) -> dict:
    if upload.get("hosted"):
        # A hosted dataset blob (`.probe/datasets/<sha256>`): only the hosting door may
        # stage that name; the generic create below refuses it (422).
        from ....catalog.hosting import reopen_hosted

        return reopen_hosted(client, upload)
    body = {
        "name": upload["name"],
        "content_hash": upload["blob"],
        "size_bytes": upload["size_bytes"],
        "content_type": upload.get("content_type"),
        # No `notes`: an older client's op may carry one; files no longer do.
    }
    if _anchor_of(upload) == Anchor.RUN.value:
        # Run-only: every other door forbids them (`extra=forbid`).
        body.update(
            span_id=upload.get("span_id"),
            step_index=upload.get("step_index"),
            kind=upload.get("kind"),
            meta=upload.get("meta"),
        )
    body = {k: v for k, v in body.items() if v is not None}
    try:
        # Idempotent: the same (anchor, name, bytes) gets its active upload back.
        return _open(client, upload, body) or {}
    except errors.ConflictError as exc:
        detail = exc.detail if isinstance(exc.detail, dict) else {}
        if detail.get("state") in ("uploading", "verifying"):
            # Another upload of these bytes is in progress in this team; when it ends
            # (verified: this becomes a HAVE; or failed/aborted) this create goes through.
            # The server bounds the wait (~10 min idle after the other process died,
            # e.g. a preempted job re-logging a checkpoint); the lane retries meanwhile.
            raise _Busy("another upload of these bytes is in progress") from None
        raise


class _Busy(Exception):
    pass
