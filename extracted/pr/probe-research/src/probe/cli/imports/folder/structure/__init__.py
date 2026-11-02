"""Front door: every name the module had before it was split into this folder."""

from __future__ import annotations

import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.imports.folder.structure.resolution",
    "probe.cli.imports.folder.structure.run_records",
    "probe.cli.imports.folder.structure.moved_files",
    "probe.cli.imports.folder.structure.structure",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "hashlib": "probe.cli.imports.folder.structure.run_records",
    "json": "probe.cli.imports.folder.structure.run_records",
    "math": "probe.cli.imports.folder.structure.run_records",
    "re": "probe.cli.imports.folder.structure.run_records",
    "ThreadPoolExecutor": "probe.cli.imports.folder.structure.moved_files",
    "field": "probe.cli.imports.folder.structure.resolution",
    "dataclass": "probe.cli.imports.folder.structure.resolution",
    "timezone": "probe.cli.imports.folder.structure.run_records",
    "datetime": "probe.cli.imports.folder.structure.run_records",
    "Path": "probe.cli.imports.folder.structure.run_records",
    "tomllib": "probe.cli.imports.folder.structure.run_records",
    "StrEnum": "probe.cli.imports.folder.structure.resolution",
    "RUN_SOURCE": "probe.cli.imports.folder.structure.structure",
    "RUN_SCHEMA": "probe.cli.imports.folder.structure.run_records",
    "META_KEY": "probe.cli.imports.folder.structure.resolution",
    "REVIEWED_KEY": "probe.cli.imports.folder.structure.resolution",
    "STRUCTURE_VERSION": "probe.cli.imports.folder.structure.resolution",
    "MAX_METRICS": "probe.cli.imports.folder.structure.run_records",
    "MAX_CONFIG": "probe.cli.imports.folder.structure.run_records",
    "MAX_PARSE_BYTES": "probe.cli.imports.folder.structure.run_records",
    "MAX_CONFIG_TEXT": "probe.cli.imports.folder.structure.run_records",
    "MAX_SOURCES": "probe.cli.imports.folder.structure.run_records",
    "SHOWN": "probe.cli.imports.folder.structure.resolution",
    "FILE_WORKERS": "probe.cli.imports.folder.structure.moved_files",
    "REPLAY_HEADER": "probe.cli.imports.folder.structure.structure",
    "Level": "probe.cli.imports.folder.structure.resolution",
    "Ended": "probe.cli.imports.folder.structure.run_records",
    "_RESULT_JSON": "probe.cli.imports.folder.structure.run_records",
    "_LONE_NUMBER": "probe.cli.imports.folder.structure.run_records",
    "_CONFIG": "probe.cli.imports.folder.structure.run_records",
    "STATUS_FIELDS": "probe.cli.imports.folder.structure.run_records",
    "_DONE": "probe.cli.imports.folder.structure.run_records",
    "_FAILED": "probe.cli.imports.folder.structure.run_records",
    "_CANCELED": "probe.cli.imports.folder.structure.run_records",
    "is_result_file": "probe.cli.imports.folder.structure.run_records",
    "is_config_file": "probe.cli.imports.folder.structure.run_records",
    "_MANIFEST": "probe.cli.imports.folder.structure.run_records",
    "_LOG": "probe.cli.imports.folder.structure.run_records",
    "run_candidates": "probe.cli.imports.folder.structure.run_records",
    "RunRecord": "probe.cli.imports.folder.structure.run_records",
    "_iso": "probe.cli.imports.folder.structure.run_records",
    "_number": "probe.cli.imports.folder.structure.run_records",
    "_scalar": "probe.cli.imports.folder.structure.run_records",
    "_SKIP": "probe.cli.imports.folder.structure.run_records",
    "_read_text": "probe.cli.imports.folder.structure.run_records",
    "_json_object": "probe.cli.imports.folder.structure.run_records",
    "_lone_number": "probe.cli.imports.folder.structure.run_records",
    "_YAML_KEY": "probe.cli.imports.folder.structure.run_records",
    "_yaml_top": "probe.cli.imports.folder.structure.run_records",
    "_config_values": "probe.cli.imports.folder.structure.run_records",
    "_status_of": "probe.cli.imports.folder.structure.run_records",
    "_keyed": "probe.cli.imports.folder.structure.run_records",
    "read_run": "probe.cli.imports.folder.structure.run_records",
    "_ancestors": "probe.cli.imports.folder.structure.resolution",
    "Resolved": "probe.cli.imports.folder.structure.resolution",
    "resolve": "probe.cli.imports.folder.structure.resolution",
    "counts_line": "probe.cli.imports.folder.structure.resolution",
    "describe": "probe.cli.imports.folder.structure.resolution",
    "plan_json": "probe.cli.imports.folder.structure.resolution",
    "remember": "probe.cli.imports.folder.structure.resolution",
    "merge_planned": "probe.cli.imports.folder.structure.resolution",
    "reviewed_version": "probe.cli.imports.folder.structure.resolution",
    "decline": "probe.cli.imports.folder.structure.resolution",
    "external_id": "probe.cli.imports.folder.structure.structure",
    "_creation_key": "probe.cli.imports.folder.structure.structure",
    "Built": "probe.cli.imports.folder.structure.structure",
    "_create_experiment": "probe.cli.imports.folder.structure.structure",
    "_converge": "probe.cli.imports.folder.structure.structure",
    "_same_time": "probe.cli.imports.folder.structure.structure",
    "_create_run": "probe.cli.imports.folder.structure.structure",
    "metric_points": "probe.cli.imports.folder.structure.structure",
    "_chart": "probe.cli.imports.folder.structure.structure",
    "SAVE_EVERY": "probe.cli.imports.folder.structure.structure",
    "build": "probe.cli.imports.folder.structure.structure",
    "build_plan": "probe.cli.imports.folder.structure.structure",
    "FINAL_MOVE_STATUSES": "probe.cli.imports.folder.structure.moved_files",
    "file_delivered": "probe.cli.imports.folder.structure.moved_files",
    "_landed": "probe.cli.imports.folder.structure.moved_files",
    "file_moves": "probe.cli.imports.folder.structure.moved_files",
    "restructure_candidates": "probe.cli.imports.folder.structure.moved_files",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
