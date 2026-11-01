"""The team note as one local file per machine: push/pull, parking, render, audit (twin: app/team_notes).
Names are served live, so a patch on the defining piece reaches callers here."""

from __future__ import annotations

import importlib

# Every piece loads here, as the module did whole; names are served live below.
for _piece in (
    "probe.shared.notes.team_note.audit",
    "probe.shared.notes.team_note.team_note",
    "probe.shared.notes.team_note.parking",
    "probe.shared.notes.team_note.push_pull",
    "probe.shared.notes.team_note.render",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    "HEALTH_FILE": "probe.shared.notes.team_note.audit",
    "note_health_path": "probe.shared.notes.team_note.audit",
    "AUDIT_STAMP_RE": "probe.shared.notes.team_note.audit",
    "_audit_baseline": "probe.shared.notes.team_note.audit",
    "AUDIT_HORIZON_DAYS": "probe.shared.notes.team_note.audit",
    "AUDIT_SIZE_PCT": "probe.shared.notes.team_note.audit",
    "AUDIT_INTERVAL_DAYS": "probe.shared.notes.team_note.audit",
    "INTERACTIVE_ENTRYPOINTS": "probe.shared.notes.team_note.audit",
    "session_is_automated": "probe.shared.notes.team_note.audit",
    "_audit_env": "probe.shared.notes.team_note.audit",
    "_stamp_age_days": "probe.shared.notes.team_note.audit",
    "_untouched_since_audit": "probe.shared.notes.team_note.audit",
    "AuditDue": "probe.shared.notes.team_note.audit",
    "audit_due": "probe.shared.notes.team_note.audit",
    "audit_advisory": "probe.shared.notes.team_note.audit",
    "_local_note_state": "probe.shared.notes.team_note.audit",
    "advisory_for_source": "probe.shared.notes.team_note.audit",
    "audit_due_for_source": "probe.shared.notes.team_note.audit",
    "AUDIT_LEASE_SECONDS": "probe.shared.notes.team_note.audit",
    "AUDIT_SESSION_ENV": "probe.shared.notes.team_note.audit",
    "audit_lease_path": "probe.shared.notes.team_note.audit",
    "_LEASE_MAX_BYTES": "probe.shared.notes.team_note.audit",
    "_read_lease": "probe.shared.notes.team_note.audit",
    "_lease_time": "probe.shared.notes.team_note.audit",
    "claim_audit_dispatch": "probe.shared.notes.team_note.audit",
    "_record_health": "probe.shared.notes.team_note.audit",
    "_merge_into_file": "probe.shared.notes.team_note.team_note",
    "DOCUMENT_NAME": "probe.shared.notes.team_note.team_note",
    "paths": "probe.shared.notes.team_note.team_note",
    "paths_for": "probe.shared.notes.team_note.team_note",
    "owner_key": "probe.shared.notes.team_note.team_note",
    "reconcile": "probe.shared.notes.team_note.team_note",
    "PARKED_KINDS": "probe.shared.notes.team_note.parking",
    "PARKED_GLOB": "probe.shared.notes.team_note.parking",
    "PARKED_SIDECARS": "probe.shared.notes.team_note.parking",
    "LEGACY_SOURCES": "probe.shared.notes.team_note.parking",
    "park": "probe.shared.notes.team_note.parking",
    "_copy_ancestor": "probe.shared.notes.team_note.parking",
    "_move_stamp": "probe.shared.notes.team_note.parking",
    "parked_kind": "probe.shared.notes.team_note.parking",
    "parked_copies": "probe.shared.notes.team_note.parking",
    "adopt": "probe.shared.notes.team_note.parking",
    "migrate_legacy_documents": "probe.shared.notes.team_note.parking",
    "push": "probe.shared.notes.team_note.push_pull",
    "pull": "probe.shared.notes.team_note.push_pull",
    "INSTRUCTION_FILE_MAX_BYTES": "probe.shared.notes.team_note.render",
    "RENDER_FAILURE_FILE": "probe.shared.notes.team_note.render",
    "_render_sources": "probe.shared.notes.team_note.render",
    "RENDER_SOURCES": "probe.shared.notes.team_note.render",
    "RenderReport": "probe.shared.notes.team_note.render",
    "hidden_by_limit": "probe.shared.notes.team_note.render",
    "HIDDEN_DETAIL": "probe.shared.notes.team_note.render",
    "remove_blocks": "probe.shared.notes.team_note.render",
    "instruction_lock_path": "probe.shared.notes.team_note.render",
    "render_failure_path": "probe.shared.notes.team_note.render",
    "_record_failures": "probe.shared.notes.team_note.render",
    "pending_render_failures": "probe.shared.notes.team_note.render",
    "_utf8_len": "probe.shared.notes.team_note.render",
    "_fits": "probe.shared.notes.team_note.render",
    "render_blocks": "probe.shared.notes.team_note.render",
    "Paths": "probe.shared.notes.sync",
    "Report": "probe.shared.notes.sync",
    "Unreadable": "probe.shared.notes.sync",
    # Imported by the module before the split: served for its callers too.
    "Path": "probe.shared.notes.team_note.audit",
    "SYNC_NONE": "probe.shared.notes.team_note.audit",
    "_dt": "probe.shared.notes.team_note.audit",
    "dataclass": "probe.shared.notes.team_note.audit",
    "datetime": "probe.shared.notes.team_note.parking",
    "errors": "probe.shared.notes.team_note.push_pull",
    "file_lock": "probe.shared.notes.team_note.audit",
    "hashlib": "probe.shared.notes.team_note.audit",
    "json": "probe.shared.notes.team_note.audit",
    "math": "probe.shared.notes.team_note.audit",
    "merge3": "probe.shared.notes.team_note.team_note",
    "os": "probe.shared.notes.team_note.audit",
    "re": "probe.shared.notes.team_note.audit",
    "state_dir": "probe.shared.notes.team_note.audit",
    "superseded": "probe.shared.notes.team_note.render",
    "time": "probe.shared.notes.team_note.audit",
    "timezone": "probe.shared.notes.team_note.parking",
    "write_text_atomic": "probe.shared.notes.team_note.audit",
}

# Re-exported under another name: bound here, not served live.
from ..sync import (  # noqa: E402, F401
    Merged as _Merged,
    commit as _commit,
    merge_into_file as _merge_into_file_core,
    one_trailing_newline as _one_trailing_newline,
    read_meta as _read_meta,
    read_text as _read,
    stamp_matches as _stamp_matches,
)


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
