"""UploadOpHandler: deliver a byte upload from its blob, and record a reference row when the server refuses it for good."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe.sdk.delivery.journal.journal import Journal


def _record_upload_fallback(journal: "Journal", client: Any, op: dict) -> bool:
    """Record a reference artifact for an upload the server refused for good; returns
    whether the row landed. The caller lets the op stop blocking the run's close only
    then: a recorded file is a resolved op, an unrecorded one is a real loss and stays
    blocking.

    The sync upload path already writes an `is_reference` row (local path,
    `meta.upload = "failed"`; `check_run` counts it as a capture gap) on a permanent
    rejection. It is the run's only record of the file, and the drainer had no
    equivalent: a rejected queued upload left an outbox dead letter and nothing else.

    Best effort: it runs while handling a failure so it may not raise. A dead letter with
    no fallback row still beats a drain that dies mid-pass.
    """
    shaped = _upload_fallback_request(op)
    if shaped is None:
        return False  # only runs carry the reference-artifact shape
    path, body = shaped
    try:
        client.transport.request("POST", path, json_body=body)
    except Exception:  # noqa: BLE001 -- a fallback may never break the drain
        return False
    return True


def _upload_fallback_request(op: dict) -> tuple[str, dict] | None:
    """(path, body) of the reference row `_record_upload_fallback` writes for
    an upload op, or None for an op that has no run to write it on."""
    upload = op.get("upload") or {}
    anchor, anchor_id = upload.get("anchor"), upload.get("anchor_id")
    if anchor != "run" or not anchor_id or not upload.get("name"):
        return None
    source = upload.get("src_path") or ""
    body = {
        "kind": upload.get("kind") or "file",
        "name": upload["name"],
        "uri": f"file://{source}" if source else None,
        "content_hash": upload.get("blob"),
        "size_bytes": upload.get("size_bytes"),
        "content_type": upload.get("content_type"),
        "is_reference": True,
        "span_id": upload.get("span_id"),
        "step_index": upload.get("step_index"),
        "meta": {
            **(upload.get("meta") or {}),
            "local_path": source,
            "upload": "failed",
            "upload_error": op.get("last_error"),
        },
    }
    # No `notes` (an older client's op may carry one): files carry none now, so it is
    # dropped here and in the upload replay (`_execute`).
    return f"/v1/runs/{anchor_id}/artifacts", {k: v for k, v in body.items() if v is not None}
