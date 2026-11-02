"""Durable local jobs for already-approved imports.

Workers detach from the terminal and reuse the import lanes' existing journals.
No credentials are saved here. Each lane must verify the approved destination
against its runtime credentials and replay only the approved files/sessions.
A folder-scoped automatic approval may prepare its plan in the worker; that
lane persists the exact resulting delivery snapshot before sending any files.
A machine restart stops workers; opening job status can recover their journals.
There is no boot service. Connection failures wait and retry; other failed jobs
need an explicit resume after their cause has been addressed.
"""

# Front door: every name the old cli/import_jobs.py had; its docstring above is the worker's --help.

from __future__ import annotations

import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.imports.jobs.errors",
    "probe.cli.imports.jobs.failure_report",
    "probe.cli.imports.jobs.kind",
    "probe.cli.imports.jobs.kinds.transcripts",
    "probe.cli.imports.jobs.runner",
    "probe.cli.imports.jobs.store",
    "probe.cli.imports.jobs.telemetry",
    "probe.cli.imports.jobs.workers",
    "probe.cli.imports.jobs.jobs",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "argparse": "probe.cli.imports.jobs.runner",
    "errno": "probe.cli.imports.jobs.errors",
    "fcntl": "probe.cli.imports.jobs.kinds.transcripts",
    "hashlib": "probe.cli.imports.jobs.failure_report",
    "json": "probe.cli.imports.jobs.failure_report",
    "math": "probe.cli.imports.jobs.runner",
    "os": "probe.cli.imports.jobs.kinds.transcripts",
    "re": "probe.cli.imports.jobs.store",
    "signal": "probe.cli.imports.jobs.runner",
    "shutil": "probe.cli.imports.jobs.jobs",
    "socket": "probe.cli.imports.jobs.errors",
    "subprocess": "probe.cli.imports.jobs.workers",
    "sys": "probe.cli.imports.jobs.runner",
    "threading": "probe.cli.imports.jobs.runner",
    "time": "probe.cli.imports.jobs.runner",
    "redirect_stdout": "probe.cli.imports.jobs.runner",
    "redirect_stderr": "probe.cli.imports.jobs.runner",
    "contextmanager": "probe.cli.imports.jobs.kinds.transcripts",
    "ExitStack": "probe.cli.imports.jobs.runner",
    "timezone": "probe.cli.imports.jobs.telemetry",
    "datetime": "probe.cli.imports.jobs.telemetry",
    "StrEnum": "probe.cli.imports.jobs.kind",
    "Path": "probe.cli.imports.jobs.failure_report",
    "URLError": "probe.cli.imports.jobs.errors",
    "HTTPError": "probe.cli.imports.jobs.errors",
    "write_text_atomic": "probe.cli.imports.jobs.store",
    "now_iso": "probe.cli.imports.jobs.kinds.transcripts",
    "file_lock": "probe.cli.imports.jobs.jobs",
    "STALL_REPORT_INTERVAL_S": "probe.cli.imports.jobs.runner",
    "STALL_GRACE_S": "probe.cli.imports.jobs.runner",
    "ACTIVITY_LINES": "probe.cli.imports.jobs.store",
    "ACTIVITY_LINE_CHARS": "probe.cli.imports.jobs.store",
    "Kind": "probe.cli.imports.jobs.kind",
    "State": "probe.cli.imports.jobs.store",
    "JobError": "probe.cli.imports.jobs.errors",
    "RetryableJobError": "probe.cli.imports.jobs.errors",
    "UnitRetryJobError": "probe.cli.imports.jobs.errors",
    "is_retryable_error": "probe.cli.imports.jobs.errors",
    "_Interrupted": "probe.cli.imports.jobs.errors",
    "_ID": "probe.cli.imports.jobs.store",
    "_SECRET_KEYS": "probe.cli.imports.jobs.store",
    "_active_job": "probe.cli.imports.jobs.runner",
    "_attempt_meter": "probe.cli.imports.jobs.runner",
    "prepared_approval_digest": "probe.cli.imports.jobs.runner",
    "remember_prepared_approval": "probe.cli.imports.jobs.runner",
    "remember_skipped": "probe.cli.imports.jobs.runner",
    "default_dir": "probe.cli.imports.jobs.store",
    "_root": "probe.cli.imports.jobs.store",
    "_directory": "probe.cli.imports.jobs.store",
    "_check_payload": "probe.cli.imports.jobs.store",
    "_clean": "probe.cli.imports.jobs.store",
    "_identity": "probe.cli.imports.jobs.store",
    "_telemetry": "probe.cli.imports.jobs.telemetry",
    "_context": "probe.cli.imports.jobs.telemetry",
    "_origin_stamp": "probe.cli.imports.jobs.telemetry",
    "_job_props": "probe.cli.imports.jobs.telemetry",
    "_elapsed_seconds": "probe.cli.imports.jobs.telemetry",
    "_emit_finished": "probe.cli.imports.jobs.telemetry",
    "_REPORT_TIMEOUT_S": "probe.cli.imports.jobs.failure_report",
    "_job_context_name": "probe.cli.imports.jobs.failure_report",
    "_report_digest": "probe.cli.imports.jobs.failure_report",
    "_post_failure_report": "probe.cli.imports.jobs.failure_report",
    "_report_failure": "probe.cli.imports.jobs.failure_report",
    "_machine_label": "probe.cli.imports.jobs.failure_report",
    "_emit_enqueued": "probe.cli.imports.jobs.telemetry",
    "_emit_stalled": "probe.cli.imports.jobs.telemetry",
    "_read": "probe.cli.imports.jobs.store",
    "_save": "probe.cli.imports.jobs.store",
    "_update": "probe.cli.imports.jobs.store",
    "_progress_message": "probe.cli.imports.jobs.store",
    "_ProgressEstimate": "probe.cli.imports.jobs.runner",
    "_try_lock": "probe.cli.imports.jobs.store",
    "_job_lock": "probe.cli.imports.jobs.store",
    "_lifecycle": "probe.cli.imports.jobs.jobs",
    "_process_identity": "probe.cli.imports.jobs.workers",
    "_alive": "probe.cli.imports.jobs.workers",
    "register_child": "probe.cli.imports.jobs.workers",
    "unregister_child": "probe.cli.imports.jobs.workers",
    "spawn_child": "probe.cli.imports.jobs.workers",
    "_reclaim_children": "probe.cli.imports.jobs.workers",
    "get_job": "probe.cli.imports.jobs.jobs",
    "_source_root": "probe.cli.imports.jobs.workers",
    "_launch": "probe.cli.imports.jobs.workers",
    "_record_launch": "probe.cli.imports.jobs.workers",
    "_launch_failed": "probe.cli.imports.jobs.workers",
    "enqueue": "probe.cli.imports.jobs.jobs",
    "_enqueue": "probe.cli.imports.jobs.jobs",
    "resume": "probe.cli.imports.jobs.jobs",
    "_resume": "probe.cli.imports.jobs.jobs",
    "_signal_worker": "probe.cli.imports.jobs.workers",
    "_stopped_worker": "probe.cli.imports.jobs.workers",
    "cancel": "probe.cli.imports.jobs.jobs",
    "_cancel_locked": "probe.cli.imports.jobs.jobs",
    "clear_all": "probe.cli.imports.jobs.jobs",
    "list_jobs": "probe.cli.imports.jobs.jobs",
    "recover_jobs": "probe.cli.imports.jobs.jobs",
    "_dispatch": "probe.cli.imports.jobs.kind",
    "_agent_meter": "probe.cli.imports.jobs.runner",
    "_agent_props": "probe.cli.imports.jobs.runner",
    "_serial_lane": "probe.cli.imports.jobs.kinds.transcripts",
    "run_worker": "probe.cli.imports.jobs.runner",
    "main": "probe.cli.imports.jobs.runner",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
