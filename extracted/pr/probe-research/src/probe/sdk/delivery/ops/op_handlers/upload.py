"""UploadOpHandler: deliver a byte upload from its blob, and record a reference row when the server refuses it for good."""

from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe.sdk.delivery.journal.journal import Journal


def _record_upload_fallback(journal: "Journal", client: Any, op: dict) -> bool:
    """Record a reference artifact for an upload the server refused for good, as the sync path does;
    returns whether the row landed (only then does the op stop holding the run's close). Best
    effort: it runs while handling a failure."""
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
