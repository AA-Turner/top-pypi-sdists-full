"""Run, split by job (metrics/, files/, closing/, launch/ ...). LAZY front door for the old `probe.sdk.run`:
light leaves live under it and must not load Run; a patch lands on every piece binding the name."""

from __future__ import annotations

from ...foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.sdk.run.closing.close",
    "probe.sdk.run.closing.closing",
    "probe.sdk.run.handle",
    "probe.sdk.run.closing.drain",
    "probe.sdk.run.closing.heartbeat",
    "probe.sdk.run.closing.lease",
    "probe.sdk.run.closing.outage",
    "probe.sdk.run.closing.status",
    "probe.sdk.run.closing.terminal",
    "probe.sdk.run.config",
    "probe.sdk.run.files.capture",
    "probe.sdk.run.files.code_files",
    "probe.sdk.run.files.code_upload",
    "probe.sdk.run.files.files",
    "probe.sdk.run.files.registry",
    "probe.sdk.run.files.snapshot",
    "probe.sdk.run.files.uploads",
    "probe.sdk.run.launch.execute",
    "probe.sdk.run.launch.host_claims",
    "probe.sdk.run.metadata",
    "probe.sdk.run.metrics.derived",
    "probe.sdk.run.metrics.values",
    "probe.sdk.run.metrics.metrics",
    "probe.sdk.run.metrics.pending",
    "probe.sdk.run.metrics.resume",
    "probe.sdk.run.metrics.spans",
    "probe.sdk.run.summary",
    "probe.sdk.run.run",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.sdk.run.files.code_upload
    "contextvars": "probe.sdk.run.files.code_upload",
    "re": "probe.sdk.run.files.code_upload",
    "tempfile": "probe.sdk.run.files.code_upload",
    "CODE_STORAGE_ENV": "probe.sdk.run.files.code_upload",
    "CODE_STORAGE_ARCHIVE": "probe.sdk.run.files.code_upload",
    "CODE_STORAGE_ARTIFACTS": "probe.sdk.run.files.code_upload",
    "DEFAULT_CODE_STORAGE": "probe.sdk.run.files.code_upload",
    "CAPTURE_DEADLINE_SECONDS": "probe.sdk.run.files.code_upload",
    "_SIGNED_QUERY": "probe.sdk.run.files.code_upload",
    "_code_storage": "probe.sdk.run.files.code_upload",
    "_capture_deadline": "probe.sdk.run.files.code_upload",
    "_redact_signed": "probe.sdk.run.files.code_upload",
    "_warn_credential_skips": "probe.sdk.run.files.code_upload",
    "_OWN_UPLOAD_WARNING": "probe.sdk.run.files.code_upload",
    # probe.sdk.run.files.files
    "errno": "probe.sdk.run.files.files",
    "nullcontext": "probe.sdk.run.files.files",
    "stat": "probe.sdk.run.files.files",
    "CredentialInPath": "probe.sdk.run.files.files",
    "InspectionResult": "probe.sdk.run.files.files",
    "PreparedUpload": "probe.sdk.run.files.files",
    "unit_context": "probe.sdk.run.files.files",
    "artifact_kind_for": "probe.sdk.run.files.files",
    "name_with_extension": "probe.sdk.run.files.files",
    "reference_fields": "probe.sdk.run.files.files",
    "ArtifactCreate": "probe.sdk.run.files.files",
    "_gate_reason": "probe.sdk.run.files.files",
    "_require_upload_source": "probe.sdk.run.files.files",
    # probe.sdk.run.metrics.values
    "functools": "probe.sdk.run.metrics.values",
    "timedelta": "probe.sdk.run.metrics.values",
    "is_sensitive_key": "probe.sdk.run.metrics.values",
    "_now": "probe.sdk.run.metrics.values",
    "_last_log_stamp": "probe.sdk.run.metrics.values",
    "_log_stamp_lock": "probe.sdk.run.metrics.values",
    "_log_stamp": "probe.sdk.run.metrics.values",
    "_as_metric_value": "probe.sdk.run.metrics.values",
    "_json_safe": "probe.sdk.run.metrics.values",
    "_FLATTEN_MAX_DEPTH": "probe.sdk.run.metrics.values",
    "_NESTED_KEY_BUDGET": "probe.sdk.run.metrics.values",
    "_NESTED_KEY_MAX_CHARS": "probe.sdk.run.metrics.values",
    "_sensitive_key_name": "probe.sdk.run.metrics.values",
    "_is_omegaconf": "probe.sdk.run.metrics.values",
    "_BudgetSpent": "probe.sdk.run.metrics.values",
    "_key_name": "probe.sdk.run.metrics.values",
    "_flatten": "probe.sdk.run.metrics.values",
    # probe.sdk.run.metrics.pending
    "json": "probe.sdk.run.metrics.pending",
    "_CLOSE_LOCK_WAIT_SECONDS": "probe.sdk.run.metrics.pending",
    "_PendingRow": "probe.sdk.run.metrics.pending",
    # probe.sdk.run.files.registry
    "Iterable": "probe.sdk.run.files.registry",
    "Mapping": "probe.sdk.run.files.registry",
    "file_extension": "probe.sdk.run.files.registry",
    # probe.sdk.run.files.code_files
    "ThreadPoolExecutor": "probe.sdk.run.files.code_files",
    "as_completed": "probe.sdk.run.files.code_files",
    "datetime": "probe.sdk.run.files.code_files",
    "timezone": "probe.sdk.run.files.code_files",
    "CredentialBlocked": "probe.sdk.run.files.code_files",
    "check_upload": "probe.sdk.run.files.code_files",
    "_snapshot": "probe.sdk.run.files.code_files",
    "OUTAGE_MIN_WINDOW": "probe.sdk.run.files.code_files",
    "CAPTURE_WINDOW": "probe.sdk.run.files.code_files",
    "CAPTURE_PUT_WORKERS": "probe.sdk.run.files.code_files",
    # probe.sdk.run.closing.heartbeat
    "math": "probe.sdk.run.closing.heartbeat",
    "random": "probe.sdk.run.closing.heartbeat",
    "weakref": "probe.sdk.run.closing.heartbeat",
    "_HEARTBEAT_INTERVAL_SECONDS": "probe.sdk.run.closing.heartbeat",
    "_heartbeat_interval": "probe.sdk.run.closing.heartbeat",
    "_beat_forever": "probe.sdk.run.closing.heartbeat",
    "_Progress": "probe.sdk.run.closing.heartbeat",
    "_RECOVERY_RETRY": "probe.sdk.run.closing.heartbeat",
    "_MAX_RECOVERY_TRIES": "probe.sdk.run.closing.heartbeat",
    "_lease_beat": "probe.sdk.run.closing.heartbeat",
    "_beat_once": "probe.sdk.run.closing.heartbeat",
    # probe.sdk.run.closing.close
    "os": "probe.sdk.run.closing.close",
    "time": "probe.sdk.run.closing.close",
    "Any": "probe.sdk.run.closing.close",
    "_diagnostics": "probe.sdk.run.closing.close",
    "errors": "probe.sdk.run.closing.close",
    "SIGN_IN_HINT": "probe.sdk.run.closing.close",
    "_multipart": "probe.sdk.run.closing.close",
    "_outputs": "probe.sdk.run.closing.close",
    "_preempt": "probe.sdk.run.closing.close",
    # probe.sdk.run.files.uploads
    "socket": "probe.sdk.run.files.uploads",
    "freeze_upload": "probe.sdk.run.files.uploads",
    "original_upload_path": "probe.sdk.run.files.uploads",
    "kind_to_send": "probe.sdk.run.files.uploads",
    "fingerprint": "probe.sdk.run.files.uploads",
    "local_file_uri": "probe.sdk.run.files.uploads",
    "UploadRequest": "probe.sdk.run.files.uploads",
    "_env_async_uploads": "probe.sdk.run.files.uploads",
    "_NOT_QUEUED": "probe.sdk.run.files.uploads",
    "_fingerprint": "probe.sdk.run.files.uploads",
    # probe.sdk.run.launch.execute
    "subprocess": "probe.sdk.run.launch.execute",
    "EXEC_FINALIZES_ENV": "probe.sdk.run.launch.execute",
    # probe.sdk.run.closing.closing
    "threading": "probe.sdk.run.closing.closing",
    "TYPE_CHECKING": "probe.sdk.run.closing.closing",
    "_FINISHING": "probe.sdk.run.closing.closing",
    # probe.sdk.run.files.capture
    "warnings": "probe.sdk.run.files.capture",
    "_ignore": "probe.sdk.run.files.capture",
    "_logstream": "probe.sdk.run.files.capture",
    # probe.sdk.run.metrics.spans
    "NAMESPACE_URL": "probe.sdk.run.metrics.spans",
    "UUID": "probe.sdk.run.metrics.spans",
    "uuid5": "probe.sdk.run.metrics.spans",
    "SpanBatch": "probe.sdk.run.metrics.spans",
    "SpanCreate": "probe.sdk.run.metrics.spans",
    "_current_span": "probe.sdk.run.metrics.spans",
    "_SPAN_NS": "probe.sdk.run.metrics.spans",
    "_span_id_for": "probe.sdk.run.metrics.spans",
    "SpanHandle": "probe.sdk.run.metrics.spans",
    # probe.sdk.run.closing.outage
    "uuid4": "probe.sdk.run.closing.outage",
    "_recover_after_outage": "probe.sdk.run.closing.outage",
    "_SYSTEM_CRASH_REASONS": "probe.sdk.run.closing.outage",
    "_crashed_by_the_system": "probe.sdk.run.closing.outage",
    # probe.sdk.run.config
    "_coerce": "probe.sdk.run.config",
    "RunConfig": "probe.sdk.run.config",
    # probe.sdk.run.files.snapshot
    "_launch": "probe.sdk.run.files.snapshot",
    "ExecutionRecordCreate": "probe.sdk.run.files.snapshot",
    "PATHS_TEXT_MAX_BYTES": "probe.sdk.run.files.snapshot",
    # probe.sdk.run.metadata
    "FailureContext": "probe.sdk.run.metadata",
    "UnitContext": "probe.sdk.run.metadata",
    # probe.sdk.run.metrics.metrics
    "MAX_METRIC_KEY_BYTES": "probe.sdk.run.metrics.metrics",
    "_STEP_MAX": "probe.sdk.run.metrics.metrics",
    "_STEP_MIN": "probe.sdk.run.metrics.metrics",
    "_key_too_long": "probe.sdk.run.metrics.metrics",
    "_FLATTEN_WARNINGS_REMEMBERED": "probe.sdk.run.metrics.metrics",
    "_KEPT_WHOLE_REASONS": "probe.sdk.run.metrics.metrics",
    "_STEP_ATTRIBUTES_REMEMBERED": "probe.sdk.run.metrics.metrics",
    # probe.sdk.run.metrics.derived
    "DerivedProvenance": "probe.sdk.run.metrics.derived",
    "MetricBatch": "probe.sdk.run.metrics.derived",
    "MetricPointIn": "probe.sdk.run.metrics.derived",
    "_metric_batch_body": "probe.sdk.run.metrics.derived",
    "_derived_provenance": "probe.sdk.run.metrics.derived",
    # probe.sdk.run.handle
    "_UNSET": "probe.sdk.run.handle",
    # probe.sdk.run.closing.drain
    "WAITING_PROMOTE_TIMEOUT": "probe.sdk.run.closing.drain",
    "FINISH_TIMEOUT_DEFAULT_SECONDS": "probe.sdk.run.closing.drain",
    "_FINISH_BACKOFF": "probe.sdk.run.closing.drain",
    "_CLOSE_RESERVE_SECONDS": "probe.sdk.run.closing.drain",
    "_close_reserve": "probe.sdk.run.closing.drain",
    "_FINISH_LOCK_POLL_SECONDS": "probe.sdk.run.closing.drain",
    # probe.sdk.run.closing.status
    "_TERMINAL_STATUSES": "probe.sdk.run.closing.status",
    "_status_for_system_exit": "probe.sdk.run.closing.status",
    "_status_for_exit": "probe.sdk.run.closing.status",
    # probe.sdk.run.launch.host_claims
    "_global_rank": "probe.sdk.run.launch.host_claims",
    # probe.sdk.run.closing.lease
    "_LEASE_DRAIN_SECONDS": "probe.sdk.run.closing.lease",
    "_CLOSE_BEAT_SECONDS": "probe.sdk.run.closing.lease",
    "_DRAINING_BEAT_MIN_SECONDS": "probe.sdk.run.closing.lease",
    # probe.sdk.run.summary
    "_summary_wire": "probe.sdk.run.summary",
    "_one_summary": "probe.sdk.run.summary",
    "_with_finish_accounting": "probe.sdk.run.summary",
    # probe.sdk.run.run
    "Run": "probe.sdk.run.run",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES, is_lazy=True)
