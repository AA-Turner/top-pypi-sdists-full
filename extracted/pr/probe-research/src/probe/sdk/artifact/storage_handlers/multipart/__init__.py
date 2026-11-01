"""Multipart artifact uploads: stage, queue, open doors, send parts, finish.
One front door; names are served live, so a patch on a piece reaches every caller."""

from __future__ import annotations

import importlib

# Every piece loads here; names are served live below (see module docstring).
for _piece in (
    "probe.sdk.artifact.storage_handlers.multipart.doors",
    "probe.sdk.artifact.storage_handlers.multipart.parts",
    "probe.sdk.artifact.storage_handlers.multipart.queue",
    "probe.sdk.artifact.storage_handlers.multipart.staging",
    "probe.sdk.delivery.ops.op_handlers.multipart_upload",
    "probe.sdk.artifact.storage_handlers.multipart.multipart",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    # probe.sdk.artifact.storage_handlers.multipart.doors
    "_anchor_of": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_open": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_grant": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_status": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_finish": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_abort": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_fields": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_create": "probe.sdk.artifact.storage_handlers.multipart.doors",
    "_Busy": "probe.sdk.artifact.storage_handlers.multipart.doors",
    # probe.sdk.artifact.storage_handlers.multipart.parts
    "PARALLEL_PARTS": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_MAX_REFUSED_SLICES": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_PART_URL_BATCH": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_HASHING": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_HASHING_LOCK": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_hash_staged": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_hash_in_background": "probe.sdk.artifact.storage_handlers.multipart.parts",
    "_send_parts": "probe.sdk.artifact.storage_handlers.multipart.parts",
    # probe.sdk.artifact.storage_handlers.multipart.queue
    "KIND": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "ops_dir": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "failed_dir": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "build_op": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "enqueue": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "pending": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "_live_op_ids": "probe.sdk.artifact.storage_handlers.multipart.queue",
    "still_uploading": "probe.sdk.artifact.storage_handlers.multipart.queue",
    # probe.sdk.artifact.storage_handlers.multipart.staging
    "_ORPHAN_GRACE_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "staged_dir": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "_private": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "_identity": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "_free_bytes": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "_floor": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "_pinned": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "StageRefused": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "stage": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "gc_staging": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "release_staged": "probe.sdk.artifact.storage_handlers.multipart.staging",
    "_check_staged": "probe.sdk.artifact.storage_handlers.multipart.staging",
    # probe.sdk.delivery.ops.op_handlers.multipart_upload
    "SLICE_SECONDS": "probe.sdk.delivery.ops.op_handlers.multipart_upload",
    "execute_op": "probe.sdk.delivery.ops.op_handlers.multipart_upload",
    # probe.sdk.artifact.storage_handlers.multipart.multipart
    "FEATURE": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "ANCHORED_FEATURE": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "STAGED_TTL_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "VERIFY_POLL_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "BUSY_RETRY_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "BUSY_MAX_WAIT_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "HASH_POLL_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "_RESTARTABLE": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "_MAX_RESTARTS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "_SYNC_BUSY_WAIT_SECONDS": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "threshold_bytes": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "over_threshold": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "on_dead_letter": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "advance": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "settle_reason": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "settle_for_close": "probe.sdk.artifact.storage_handlers.multipart.multipart",
    "upload_now": "probe.sdk.artifact.storage_handlers.multipart.multipart",
}


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
