"""each file's delivery: approve, intend, reissue, accept the receipt, reconcile, dead letters and exclusions."""

from __future__ import annotations


def own_names(intent: dict) -> set[str]:
    """The artifact names that are this intent's file: the scrubbed name the
    uploader sends, and the raw path a legacy adoption (`backfill_legacy`)
    matched an artifact already stored under.

    The SDK scrubs credentials out of every name (`scrub_string`), so a path
    carrying one is delivered under its redacted form; comparing a receipt with
    the raw path alone would fail that file on every run."""
    from .....sdk.redaction import scrub_string

    return {scrub_string(intent["artifact_name"]), intent["artifact_name"]}


def delivers_approved_bytes(intent: dict, receipt: dict) -> bool:
    """True when the receipt's bytes are the approved file's, or its redaction.

    Uploads are redacted before they are hashed (`secret_gate.prepare_upload`),
    so an approved file with a credential-shaped span lands under the redacted
    digest and size. The journal stages a request that names an
    `expected_content_hash` (`backfill_delivery.enqueue` always sets the
    approved hash) only when the source or the snapshot matches it, and stamps
    the source digest of that same read on the receipt as `source_content_hash`.
    Every such receipt carries the stamp, so one without it predates the stamp
    (CLI 0.281.0 and before); its request was held to the same check, so it is
    accepted as the approved file redacted.
    """
    from .....sdk.delivery.ops.ops import DELIVERY_SCHEMA

    if (receipt.get("content_hash") == intent["content_hash"]
            and receipt.get("size_bytes") == intent["size_bytes"]):
        return True
    if intent["mode"] != "upload":
        return False
    if "source_content_hash" in receipt:
        return receipt["source_content_hash"] == intent["content_hash"]
    return receipt.get("schema") == DELIVERY_SCHEMA and bool(receipt.get("request_digest"))
