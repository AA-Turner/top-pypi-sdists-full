"""The two-pass import: classify once, then upload in resumable units.

The shape exists to resolve a real conflict in the requirement. Files for one
line of work are scattered across directories, which wants ONE agent with the
whole folder in view. An import that runs for hours will be interrupted, which
wants MANY small agents you can resume. Those pull opposite ways, so the work is
split by what each half is good at:

    PASS A -- classify.  One agent, whole-folder view, uploads nothing. It sees
                         evidence (not a directory listing) and decides which
                         project each FILE belongs to. Completed local turns
                         can be reused when preparation is restarted.

    PASS B -- import.    One agent per unit, each told which project it is
                         filing into. Units are independent, so a crash costs
                         one unit rather than the run.

Between them sits a human, once, looking at the classification with the files
the agent was least sure about pulled to the top.

WHAT EACH HALF IS AUTHORITATIVE FOR, because getting this backwards is how a
backfill lies:

    the walk        how many files exist          (never the model)
    the agent       what they mean                (never the count)
    the ledger      which units are done          (never the agent's word)
    the outbox      what actually reached storage (never "the agent said so")

Agents do not upload. They write a manifest and one process enqueues it: a
process start plus a slug lookup per file is tens of CPU-hours before any bytes
move at the sizes this feature is for.
"""

from __future__ import annotations


# -- front door: every piece's names, served live ---------------------------------
import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.imports.folder.classify.chunked",
    "probe.cli.imports.folder.classify.classify",
    "probe.cli.imports.folder.classify.context",
    "probe.cli.imports.folder.classify.passes",
    "probe.cli.imports.folder.classify.plan_view",
    "probe.cli.imports.folder.flow.plan_run",
    "probe.cli.imports.folder.upload.units",
    "probe.cli.imports.folder.upload.upload",
    "probe.cli.imports.folder.walk.traversal",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "contextlib": "probe.cli.imports.folder.classify.passes",
    "hashlib": "probe.cli.imports.folder.classify.classify",
    "json": "probe.cli.imports.folder.classify.chunked",
    "os": "probe.cli.imports.folder.classify.context",
    "shutil": "probe.cli.imports.folder.classify.passes",
    "sys": "probe.cli.imports.folder.classify.context",
    "threading": "probe.cli.imports.folder.classify.context",
    "time": "probe.cli.imports.folder.flow.plan_run",
    "uuid": "probe.cli.imports.folder.classify.classify",
    "as_completed": "probe.cli.imports.folder.upload.units",
    "ThreadPoolExecutor": "probe.cli.imports.folder.classify.chunked",
    "contextmanager": "probe.cli.imports.folder.classify.context",
    "copy_context": "probe.cli.imports.folder.classify.chunked",
    "ContextVar": "probe.cli.imports.folder.classify.context",
    "field": "probe.cli.imports.folder.flow.plan_run",
    "dataclass": "probe.cli.imports.folder.classify.context",
    "functools": "probe.cli.imports.folder.classify.classify",
    "Path": "probe.cli.imports.folder.classify.chunked",
    "TYPE_CHECKING": "probe.cli.imports.folder.flow.plan_run",
    "bf": "probe.cli.imports.folder.classify.chunked",
    "evidence_mod": "probe.cli.imports.folder.classify.chunked",
    "index_mod": "probe.cli.imports.folder.walk.traversal",
    "ledger_mod": "probe.cli.imports.folder.upload.units",
    "validate_manifest": "probe.cli.imports.folder.upload.units",
    "plan_mod": "probe.cli.imports.folder.classify.chunked",
    "tool_mod": "probe.cli.imports.folder.classify.chunked",
    "projects_mod": "probe.cli.imports.folder.classify.chunked",
    "prompts": "probe.cli.imports.folder.classify.chunked",
    "launch_kwargs": "probe.cli.imports.folder.classify.passes",
    "cached": "probe.cli.imports.folder.classify.context",
    "Lane": "probe.cli.imports.folder.classify.passes",
    "AgentSettings": "probe.cli.imports.folder.classify.chunked",
    "StrEnum": "probe.cli.imports.folder.classify.passes",
    "_env_concurrency": "probe.cli.imports.folder.upload.units",
    "UNIT_CONCURRENCY_DEFAULT": "probe.cli.imports.folder.upload.units",
    "CLASSIFY_CONCURRENCY_DEFAULT": "probe.cli.imports.folder.classify.chunked",
    "unit_concurrency": "probe.cli.imports.folder.upload.units",
    "classify_concurrency": "probe.cli.imports.folder.classify.chunked",
    "DEFAULT_CONCURRENCY": "probe.cli.imports.folder.upload.units",
    "UNIT_TIMEOUT_S": "probe.cli.imports.folder.upload.units",
    "CLASSIFY_TIMEOUT_S": "probe.cli.imports.folder.classify.passes",
    "new_session_id": "probe.cli.imports.folder.classify.classify",
    "UnitOutcome": "probe.cli.imports.folder.upload.units",
    "Report": "probe.cli.imports.folder.flow.plan_run",
    "_ReadProgress": "probe.cli.imports.folder.classify.context",
    "_read_progress": "probe.cli.imports.folder.classify.context",
    "SURVEY_CONCURRENCY": "probe.cli.imports.folder.classify.chunked",
    "_classification_results": "probe.cli.imports.folder.classify.chunked",
    "_ClassificationProgress": "probe.cli.imports.folder.classify.context",
    "_ClassificationContext": "probe.cli.imports.folder.classify.context",
    "_classification_context": "probe.cli.imports.folder.classify.context",
    "_PREP_CACHE_VERSION": "probe.cli.imports.folder.classify.context",
    "_PREP_CACHE_ENTRY_BYTES": "probe.cli.imports.folder.classify.context",
    "_PREP_CACHE_BYTES": "probe.cli.imports.folder.classify.context",
    "_PREP_CACHE_ENTRIES": "probe.cli.imports.folder.classify.context",
    "classification_context": "probe.cli.imports.folder.classify.context",
    "_classification_progress": "probe.cli.imports.folder.classify.context",
    "_classification_cache_path": "probe.cli.imports.folder.classify.context",
    "_read_classification_cache": "probe.cli.imports.folder.classify.context",
    "_write_classification_cache": "probe.cli.imports.folder.classify.context",
    "_cached_plan": "probe.cli.imports.folder.classify.context",
    "_usable_pass": "probe.cli.imports.folder.classify.passes",
    "_git_note": "probe.cli.imports.folder.classify.classify",
    "classify": "probe.cli.imports.folder.classify.classify",
    "IMPORTED_WHY": "probe.cli.imports.folder.classify.classify",
    "_own_pairs": "probe.cli.imports.folder.classify.classify",
    "_fixed_seed": "probe.cli.imports.folder.classify.classify",
    "NAMING_TOKEN_BUDGET": "probe.cli.imports.folder.classify.chunked",
    "PASS_ATTEMPTS": "probe.cli.imports.folder.classify.passes",
    "_run_pass": "probe.cli.imports.folder.classify.passes",
    "_fit_findings": "probe.cli.imports.folder.classify.chunked",
    "INHERIT_FLOOR": "probe.cli.imports.folder.classify.passes",
    "SessionOutcome": "probe.cli.imports.folder.classify.passes",
    "ToolPass": "probe.cli.imports.folder.classify.passes",
    "CONTINUE_NOTE": "probe.cli.imports.folder.classify.passes",
    "_plan_state": "probe.cli.imports.folder.classify.passes",
    "_session_key": "probe.cli.imports.folder.classify.classify",
    "_outcome": "probe.cli.imports.folder.classify.passes",
    "_final_message": "probe.cli.imports.folder.classify.classify",
    "_run_tool_pass": "probe.cli.imports.folder.classify.passes",
    "_launch_tool_pass": "probe.cli.imports.folder.classify.passes",
    "_folder_project": "probe.cli.imports.folder.classify.chunked",
    "_row_files": "probe.cli.imports.folder.classify.chunked",
    "_plan_from_passes": "probe.cli.imports.folder.classify.passes",
    "classify_chunked": "probe.cli.imports.folder.classify.chunked",
    "revise": "probe.cli.imports.folder.classify.classify",
    "PLAN_VIEW_LINES": "probe.cli.imports.folder.classify.plan_view",
    "plan_view": "probe.cli.imports.folder.classify.plan_view",
    "_destination": "probe.cli.imports.folder.classify.plan_view",
    "describe_plan": "probe.cli.imports.folder.classify.plan_view",
    "run_unit": "probe.cli.imports.folder.upload.units",
    "write_unaccounted": "probe.cli.imports.folder.upload.units",
    "sizes_for_tails": "probe.cli.imports.folder.upload.units",
    "_manifest_notes": "probe.cli.imports.folder.upload.units",
    "_saved_notes": "probe.cli.imports.folder.upload.units",
    "_save_notes": "probe.cli.imports.folder.upload.units",
    "_finish_failed_unit": "probe.cli.imports.folder.upload.units",
    "_write_unit_manifest": "probe.cli.imports.folder.upload.units",
    "_fulfil_tail_unit": "probe.cli.imports.folder.upload.units",
    "_manifest_rows": "probe.cli.imports.folder.upload.units",
    "run_units": "probe.cli.imports.folder.upload.units",
    "_ingest_summary": "probe.cli.imports.folder.upload.upload",
    "enqueue_manifests": "probe.cli.imports.folder.upload.upload",
    "WATCH_POLL_S": "probe.cli.imports.folder.upload.upload",
    "watch_outbox": "probe.cli.imports.folder.upload.upload",
    "execute": "probe.cli.imports.folder.flow.plan_run",
    "PROGRESS_EVERY": "probe.cli.imports.folder.walk.traversal",
    "WARN_SHOWN": "probe.cli.imports.folder.walk.traversal",
    "_index": "probe.cli.imports.folder.walk.traversal",
    "incomplete_lines": "probe.cli.imports.folder.walk.traversal",
    "SKIPPED_SHOWN": "probe.cli.imports.folder.walk.traversal",
    "skipped_lines": "probe.cli.imports.folder.walk.traversal",
    "refused_includes": "probe.cli.imports.folder.walk.traversal",
    "_execute": "probe.cli.imports.folder.flow.plan_run",
    "_run_transcript_lane": "probe.cli.imports.folder.flow.plan_run",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
