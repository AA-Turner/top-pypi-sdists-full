"""Front door: every name the module had before it was split into this folder."""

from __future__ import annotations

import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.imports.folder.flow.auto_import",
    "probe.cli.imports.folder.flow.background_job",
    "probe.cli.imports.folder.flow.deliver",
    "probe.cli.imports.folder.flow.review",
    "probe.cli.imports.folder.flow.scoped",
    "probe.cli.imports.folder.upload.flush",
    "probe.cli.imports.folder.flow.flow",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "asdict": "probe.cli.imports.folder.flow.auto_import",
    "nullcontext": "probe.cli.imports.folder.flow.review",
    "contextmanager": "probe.cli.imports.folder.flow.deliver",
    "hashlib": "probe.cli.imports.folder.flow.auto_import",
    "json": "probe.cli.imports.folder.flow.auto_import",
    "os": "probe.cli.imports.folder.upload.flush",
    "Path": "probe.cli.imports.folder.flow.auto_import",
    "shlex": "probe.cli.imports.folder.flow.background_job",
    "time": "probe.cli.imports.folder.flow.deliver",
    "uuid": "probe.cli.imports.folder.flow.auto_import",
    "write_text_atomic": "probe.cli.imports.folder.flow.auto_import",
    "fsync_directory": "probe.cli.imports.folder.flow.auto_import",
    "file_lock": "probe.cli.imports.folder.flow.auto_import",
    "delivery": "probe.cli.imports.folder.flow.deliver",
    "evidence": "probe.cli.imports.folder.flow.background_job",
    "github": "probe.cli.imports.folder.flow.background_job",
    "legacy": "probe.cli.imports.folder.flow.flow",
    "agent_session": "probe.cli.imports.folder.flow.review",
    "plans": "probe.cli.imports.folder.flow.deliver",
    "projects_mod": "probe.cli.imports.folder.flow.review",
    "structure": "probe.cli.imports.folder.flow.deliver",
    "wandb": "probe.cli.imports.folder.flow.auto_import",
    "ledger_mod": "probe.cli.imports.folder.flow.deliver",
    "skipped_folders": "probe.cli.imports.folder.flow.background_job",
    "Scope": "probe.cli.imports.folder.flow.auto_import",
    "CoverageError": "probe.cli.imports.folder.flow.auto_import",
    "Coverage": "probe.cli.imports.folder.flow.auto_import",
    "UnitState": "probe.cli.imports.folder.flow.deliver",
    "UnitKind": "probe.cli.imports.folder.flow.review",
    "Unit": "probe.cli.imports.folder.flow.deliver",
    "Ledger": "probe.cli.imports.folder.flow.background_job",
    "_Stopped": "probe.cli.imports.folder.flow.flow",
    "_BackToImport": "probe.cli.imports.folder.flow.flow",
    "BACKGROUND_SCHEMA": "probe.cli.imports.folder.flow.background_job",
    "AUTO_BACKGROUND_SCHEMA": "probe.cli.imports.folder.flow.auto_import",
    "enqueue_auto_import": "probe.cli.imports.folder.flow.auto_import",
    "_enqueue_reviewed_import": "probe.cli.imports.folder.flow.scoped",
    "_auto_checkpoint": "probe.cli.imports.folder.flow.auto_import",
    "_read_auto_checkpoint": "probe.cli.imports.folder.flow.auto_import",
    "_verify_auto_folder": "probe.cli.imports.folder.flow.auto_import",
    "_run_auto_import": "probe.cli.imports.folder.flow.auto_import",
    "_approval_snapshot": "probe.cli.imports.folder.flow.background_job",
    "_unit_snapshot": "probe.cli.imports.folder.flow.background_job",
    "_background_payload": "probe.cli.imports.folder.flow.background_job",
    "_background_client": "probe.cli.imports.folder.flow.background_job",
    "run_background_job": "probe.cli.imports.folder.flow.background_job",
    "_completed_paths": "probe.cli.imports.folder.flow.background_job",
    "_phase": "probe.cli.imports.folder.flow.deliver",
    "_TransientFlush": "probe.cli.imports.folder.upload.flush",
    "FLUSH_ATTEMPTS": "probe.cli.imports.folder.upload.flush",
    "FLUSH_ATTEMPTS_ENV": "probe.cli.imports.folder.upload.flush",
    "flush_attempts": "probe.cli.imports.folder.upload.flush",
    "_flush_uploads": "probe.cli.imports.folder.upload.flush",
    "_run_units": "probe.cli.imports.folder.flow.deliver",
    "execute": "probe.cli.imports.folder.flow.scoped",
    "_choose_source": "probe.cli.imports.folder.flow.scoped",
    "_review": "probe.cli.imports.folder.flow.review",
    "_finish_approved_request": "probe.cli.imports.folder.flow.review",
    "_source_choice": "probe.cli.imports.folder.flow.review",
    "_save_reviewed_sources": "probe.cli.imports.folder.flow.review",
    "_skip_counts": "probe.cli.imports.folder.flow.flow",
    "_census_progress": "probe.cli.imports.folder.flow.flow",
    "_run": "probe.cli.imports.folder.flow.flow",
    "_reconcile_dead_units": "probe.cli.imports.folder.flow.flow",
    "_deliver_approved": "probe.cli.imports.folder.flow.deliver",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
