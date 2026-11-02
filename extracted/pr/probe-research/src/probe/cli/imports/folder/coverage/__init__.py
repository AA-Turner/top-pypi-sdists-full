"""Front door: every name the module had before it was split into this folder."""

from __future__ import annotations

import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.imports.folder.coverage.delivery",
    "probe.cli.imports.folder.coverage.observe",
    "probe.cli.imports.folder.coverage.report",
    "probe.cli.imports.folder.coverage.scope",
    "probe.cli.imports.folder.coverage.signatures",
    "probe.cli.imports.folder.coverage.coverage",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "Callable": "probe.cli.imports.folder.coverage.observe",
    "ThreadPoolExecutor": "probe.cli.imports.folder.coverage.coverage",
    "contextmanager": "probe.cli.imports.folder.coverage.coverage",
    "dataclass": "probe.cli.imports.folder.coverage.observe",
    "asdict": "probe.cli.imports.folder.coverage.scope",
    "fcntl": "probe.cli.imports.folder.coverage.coverage",
    "hashlib": "probe.cli.imports.folder.coverage.scope",
    "json": "probe.cli.imports.folder.coverage.scope",
    "os": "probe.cli.imports.folder.coverage.observe",
    "PurePath": "probe.cli.imports.folder.coverage.observe",
    "Path": "probe.cli.imports.folder.coverage.observe",
    "sqlite3": "probe.cli.imports.folder.coverage.coverage",
    "stat": "probe.cli.imports.folder.coverage.signatures",
    "time": "probe.cli.imports.folder.coverage.signatures",
    "unicodedata": "probe.cli.imports.folder.coverage.coverage",
    "urlunsplit": "probe.cli.imports.folder.coverage.scope",
    "urlsplit": "probe.cli.imports.folder.coverage.scope",
    "uuid": "probe.cli.imports.folder.coverage.coverage",
    "StrEnum": "probe.cli.imports.folder.coverage.observe",
    "write_text_atomic": "probe.cli.imports.folder.coverage.coverage",
    "read_json": "probe.cli.imports.folder.coverage.coverage",
    "now_iso": "probe.cli.imports.folder.coverage.coverage",
    "file_lock": "probe.cli.imports.folder.coverage.coverage",
    "fingerprint": "probe.cli.imports.folder.coverage.coverage",
    "default_dir": "probe.cli.imports.folder.coverage.coverage",
    "SCHEMA": "probe.cli.imports.folder.coverage.coverage",
    "MIGRATABLE_SCHEMAS": "probe.cli.imports.folder.coverage.coverage",
    "OBSERVE_BATCH_FILES": "probe.cli.imports.folder.coverage.observe",
    "OBSERVE_BATCH_SECONDS": "probe.cli.imports.folder.coverage.observe",
    "OBSERVE_HASH_WORKERS": "probe.cli.imports.folder.coverage.observe",
    "SIGNATURE_SETTLE_SECONDS": "probe.cli.imports.folder.coverage.signatures",
    "SkipRule": "probe.cli.imports.folder.coverage.observe",
    "WalkSkips": "probe.cli.imports.folder.coverage.observe",
    "own_names": "probe.cli.imports.folder.coverage.delivery",
    "delivers_approved_bytes": "probe.cli.imports.folder.coverage.delivery",
    "CoverageError": "probe.cli.imports.folder.coverage.coverage",
    "CoverageReport": "probe.cli.imports.folder.coverage.report",
    "Scope": "probe.cli.imports.folder.coverage.scope",
    "_default_workspace": "probe.cli.imports.folder.coverage.scope",
    "_signature_tuple": "probe.cli.imports.folder.coverage.signatures",
    "signature_of": "probe.cli.imports.folder.coverage.signatures",
    "hash_current": "probe.cli.imports.folder.coverage.signatures",
    "hash_current_signed": "probe.cli.imports.folder.coverage.signatures",
    "reusable_signature": "probe.cli.imports.folder.coverage.signatures",
    "Coverage": "probe.cli.imports.folder.coverage.coverage",
    "skipped_folders": "probe.cli.imports.folder.coverage.observe",
    "_skip_rules": "probe.cli.imports.folder.coverage.observe",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
