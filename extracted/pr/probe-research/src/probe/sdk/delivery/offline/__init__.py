"""Offline runs and `probe sync`, and the old `probe.sdk.offline` as one front door over its pieces.
Names are served live, so a patch on the defining piece reaches callers here; code imports pieces."""

from __future__ import annotations

import importlib

# Every piece loads here, as `probe.sdk.offline` loaded whole: a piece first imported at interpreter
# exit would exec there (CPython 3.12 then loses an uncaught Ctrl-C's exit code).
for _piece in (
    "probe.sdk.delivery.offline.lineage",
    "probe.sdk.delivery.offline.queue",
    "probe.sdk.delivery.offline.sync",
    "probe.sdk.delivery.ops.op_handlers.create_run",
    "probe.sdk.delivery.sinks.offline",
    "probe.sdk.delivery.offline.offline",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    # probe.sdk.delivery.offline.lineage
    "_lineage_feature": "probe.sdk.delivery.offline.lineage",
    "_GATED": "probe.sdk.delivery.offline.lineage",
    "_take_gated": "probe.sdk.delivery.offline.lineage",
    "lineage_gate": "probe.sdk.delivery.offline.lineage",
    "_OBSERVATIONS_FEATURE": "probe.sdk.delivery.offline.lineage",
    "_LATE": "probe.sdk.delivery.offline.lineage",
    "_unobserved": "probe.sdk.delivery.offline.lineage",
    "_drop_untaken_lineage": "probe.sdk.delivery.offline.lineage",
    # probe.sdk.delivery.offline.queue
    "OFFLINE_DIRNAME": "probe.sdk.delivery.offline.queue",
    "MAPPING_NAME": "probe.sdk.delivery.offline.queue",
    "_OFFLINE_CONFLICT": "probe.sdk.delivery.offline.queue",
    "read_manifest": "probe.sdk.delivery.offline.queue",
    "read_mapping": "probe.sdk.delivery.offline.queue",
    "_write_mapping": "probe.sdk.delivery.offline.queue",
    "search_places": "probe.sdk.delivery.offline.queue",
    "find_offline_dirs": "probe.sdk.delivery.offline.queue",
    "describe": "probe.sdk.delivery.offline.queue",
    "_create_ops": "probe.sdk.delivery.offline.queue",
    "amend": "probe.sdk.delivery.offline.queue",
    # probe.sdk.delivery.offline.sync
    "_origin": "probe.sdk.delivery.offline.sync",
    "check_origin": "probe.sdk.delivery.offline.sync",
    "check_tenant": "probe.sdk.delivery.offline.sync",
    "require_server": "probe.sdk.delivery.offline.sync",
    "sync_dir": "probe.sdk.delivery.offline.sync",
    # probe.sdk.delivery.ops.op_handlers.create_run
    "bind_local_refs": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_replace": "probe.sdk.delivery.ops.op_handlers.create_run",
    "deliver_create": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_key_made_a_run": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_post": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_home_path": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_create_with_policy": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_conflict_message": "probe.sdk.delivery.ops.op_handlers.create_run",
    "_mark_supersede": "probe.sdk.delivery.ops.op_handlers.create_run",
    # probe.sdk.delivery.sinks.offline
    "LINEAGE_ROUTES": "probe.sdk.delivery.sinks.offline",
    "OfflineTransport": "probe.sdk.delivery.sinks.offline",
    "OfflineClient": "probe.sdk.delivery.sinks.offline",
    # probe.sdk.delivery.offline.offline
    "MANIFEST_NAME": "probe.sdk.delivery.offline.offline",
    "MANIFEST_SCHEMA": "probe.sdk.delivery.offline.offline",
    "LOCAL_PREFIX": "probe.sdk.delivery.offline.offline",
    "CREATE_KIND": "probe.sdk.delivery.offline.offline",
    "FALLBACK_ENV": "probe.sdk.delivery.offline.offline",
    "UNKNOWN_OWNER": "probe.sdk.delivery.offline.offline",
    "SKIPPED_CAPTURE": "probe.sdk.delivery.offline.offline",
    "_CREATE_FIELDS": "probe.sdk.delivery.offline.offline",
    "_HOME_FIELDS": "probe.sdk.delivery.offline.offline",
    "_SKIPPED_FIELDS": "probe.sdk.delivery.offline.offline",
    "offline_root": "probe.sdk.delivery.offline.offline",
    "local_ref": "probe.sdk.delivery.offline.offline",
    "OfflineRun": "probe.sdk.delivery.offline.offline",
    "cached_identity": "probe.sdk.delivery.offline.offline",
    "open_offline_run": "probe.sdk.delivery.offline.offline",
    "_offline_body": "probe.sdk.delivery.offline.offline",
    "_note_in_manifest": "probe.sdk.delivery.offline.offline",
    "_context_name": "probe.sdk.delivery.offline.offline",
    "fallback_enabled": "probe.sdk.delivery.offline.offline",
    # imported by the old module: the same objects, read through a piece that imports them
    "hashlib": "probe.sdk.delivery.ops.op_handlers.create_run",
    "json": "probe.sdk.delivery.offline.queue",
    "os": "probe.sdk.delivery.offline.lineage",
    "time": "probe.sdk.delivery.offline.sync",
    "uuid": "probe.sdk.delivery.offline.offline",
    "Path": "probe.sdk.delivery.offline.lineage",
    "Any": "probe.sdk.delivery.offline.queue",
    "httpx": "probe.sdk.delivery.sinks.offline",
    "errors": "probe.sdk.delivery.offline.lineage",
    "_diagnostics": "probe.sdk.delivery.ops.op_handlers.create_run",
    "Client": "probe.sdk.delivery.offline.offline",
    "Settings": "probe.sdk.delivery.sinks.offline",
    "resolve_settings": "probe.sdk.delivery.offline.offline",
    "now_iso": "probe.sdk.delivery.offline.queue",
    "write_text_atomic": "probe.sdk.delivery.offline.queue",
    "Journal": "probe.sdk.delivery.offline.lineage",
    "default_root": "probe.sdk.delivery.offline.queue",
    "Run": "probe.sdk.delivery.offline.offline",
    "_now": "probe.sdk.delivery.offline.offline",
    "_summary_wire": "probe.sdk.delivery.offline.offline",
    "_UNSET": "probe.sdk.delivery.offline.offline",
    "Transport": "probe.sdk.delivery.sinks.offline",
}
#: `from <old path> import *` takes what the old module's did: every public name.
__all__ = [name for name in _HOMES if not name.startswith("_")]


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
