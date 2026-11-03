"""HTTP to the Probe server, as one front door over its pieces.
Names are served live, so a patch on the defining piece reaches callers here; code imports pieces."""

from __future__ import annotations

import importlib

# Every piece loads here, as `probe.sdk.transport` loaded whole: a piece first imported at interpreter
# exit would exec there (CPython 3.12 then loses an uncaught Ctrl-C's exit code).
for _piece in (
    "probe.sdk.delivery.transport.blobs",
    "probe.sdk.delivery.transport.deadlines",
    "probe.sdk.delivery.transport.failures",
    "probe.sdk.delivery.transport.headers",
    "probe.sdk.delivery.transport.notices",
    "probe.sdk.delivery.transport.tracking",
    "probe.sdk.delivery.transport.transport",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    # probe.sdk.delivery.transport.blobs
    "_warn_upload_inspection": "probe.sdk.delivery.transport.blobs",
    "_iter_file": "probe.sdk.delivery.transport.blobs",
    "_blob_label": "probe.sdk.delivery.transport.blobs",
    "_instrumented": "probe.sdk.delivery.transport.blobs",
    # probe.sdk.delivery.transport.deadlines
    "_TRANSPORT_BACKOFF": "probe.sdk.delivery.transport.deadlines",
    "_INLINE_RETRY_AFTER_MAX": "probe.sdk.delivery.transport.deadlines",
    "_request_deadline": "probe.sdk.delivery.transport.deadlines",
    "deadline_scope": "probe.sdk.delivery.transport.deadlines",
    "fresh_deadline_scope": "probe.sdk.delivery.transport.deadlines",
    "_NOT_PATIENT": "probe.sdk.delivery.transport.deadlines",
    "_patience_outer": "probe.sdk.delivery.transport.deadlines",
    "_patience_state": "probe.sdk.delivery.transport.deadlines",
    "_PATIENCE_BACKOFF": "probe.sdk.delivery.transport.deadlines",
    "_PATIENCE_LAST_ATTEMPT": "probe.sdk.delivery.transport.deadlines",
    "_JITTER": "probe.sdk.delivery.transport.deadlines",
    "_patient": "probe.sdk.delivery.transport.deadlines",
    "patience": "probe.sdk.delivery.transport.deadlines",
    "without_patience": "probe.sdk.delivery.transport.deadlines",
    "pause_patience": "probe.sdk.delivery.transport.deadlines",
    "deadline_remaining": "probe.sdk.delivery.transport.deadlines",
    "_retry_after_seconds": "probe.sdk.delivery.transport.deadlines",
    "_announce_patience": "probe.sdk.delivery.transport.deadlines",
    "wait_out_retry_after": "probe.sdk.delivery.transport.deadlines",
    "_with_retry_after": "probe.sdk.delivery.transport.deadlines",
    # probe.sdk.delivery.transport.failures
    "_AMBIGUOUS_STATUSES": "probe.sdk.delivery.transport.failures",
    "outcome_unknown": "probe.sdk.delivery.transport.failures",
    "_presigned_put_error": "probe.sdk.delivery.transport.failures",
    "_is_trash_notice": "probe.sdk.delivery.transport.failures",
    # probe.sdk.delivery.transport.headers
    "Attribution": "probe.sdk.delivery.transport.headers",
    "_attribution_override": "probe.sdk.delivery.transport.headers",
    "resolve_attribution": "probe.sdk.delivery.transport.headers",
    "attribution_scope": "probe.sdk.delivery.transport.headers",
    "_event_at": "probe.sdk.delivery.transport.headers",
    "event_at_scope": "probe.sdk.delivery.transport.headers",
    "_OWN_SESSION": "probe.sdk.delivery.transport.headers",
    "_queued_session": "probe.sdk.delivery.transport.headers",
    "queued_session_scope": "probe.sdk.delivery.transport.headers",
    "_session_headers": "probe.sdk.delivery.transport.headers",
    "_event_at_header": "probe.sdk.delivery.transport.headers",
    "_OWN_ORIGIN": "probe.sdk.delivery.transport.headers",
    "_queued_origin": "probe.sdk.delivery.transport.headers",
    "queued_origin_scope": "probe.sdk.delivery.transport.headers",
    "_write_origin_header": "probe.sdk.delivery.transport.headers",
    "_DEVICE_REPORTING_SURFACES": "probe.sdk.delivery.transport.headers",
    "_device_headers_for": "probe.sdk.delivery.transport.headers",
    # probe.sdk.delivery.transport.notices
    "NOTICE_WATCHER": "probe.sdk.delivery.transport.notices",
    "NoticeWatcher": "probe.sdk.delivery.transport.notices",
    "AgentPoster": "probe.sdk.delivery.transport.notices",
    # probe.sdk.delivery.transport.tracking
    "_RESEARCH_PATH_PREFIXES": "probe.sdk.delivery.transport.tracking",
    "_READ_METHODS": "probe.sdk.delivery.transport.tracking",
    "_TRACKING_MEMO_CAP": "probe.sdk.delivery.transport.tracking",
    "_is_research_path": "probe.sdk.delivery.transport.tracking",
    # probe.sdk.delivery.transport.transport
    "LEASES_HEADER": "probe.sdk.delivery.transport.transport",
    "_RETRYABLE": "probe.sdk.delivery.transport.transport",
    "CLOCK_SKEW_WARN_SECONDS": "probe.sdk.delivery.transport.transport",
    "_clock_checked": "probe.sdk.delivery.transport.transport",
    "_check_clock_skew": "probe.sdk.delivery.transport.transport",
    "_DEFAULT_TIMEOUT": "probe.sdk.delivery.transport.transport",
    "_MAX_RETRIES": "probe.sdk.delivery.transport.transport",
    "_DEFAULT_CONNECT_TIMEOUT": "probe.sdk.delivery.transport.transport",
    "_CONNECT_ERRORS": "probe.sdk.delivery.transport.transport",
    "Page": "probe.sdk.delivery.transport.transport",
    "Transport": "probe.sdk.delivery.transport.transport",
    "_IDEMPOTENCY_ENV": "probe.sdk.delivery.transport.transport",
    "_idempotency_count": "probe.sdk.delivery.transport.transport",
    "_idempotency_key": "probe.sdk.delivery.transport.transport",
    # imported by the old module: the same objects, read through a piece that imports them
    "InspectionResult": "probe.sdk.delivery.transport.blobs",
    "freeze_stream": "probe.sdk.delivery.transport.blobs",
    "freeze_upload": "probe.sdk.delivery.transport.blobs",
    "warn_if_incomplete": "probe.sdk.delivery.transport.blobs",
    "hashlib": "probe.sdk.delivery.transport.headers",
    "hmac": "probe.sdk.delivery.transport.headers",
    "json": "probe.sdk.delivery.transport.failures",
    "os": "probe.sdk.delivery.transport.deadlines",
    "random": "probe.sdk.delivery.transport.deadlines",
    "re": "probe.sdk.delivery.transport.transport",
    "sys": "probe.sdk.delivery.transport.deadlines",
    "time": "probe.sdk.delivery.transport.blobs",
    "contextmanager": "probe.sdk.delivery.transport.deadlines",
    "ContextVar": "probe.sdk.delivery.transport.deadlines",
    "StrEnum": "probe.sdk.delivery.transport.headers",
    "dataclass": "probe.sdk.delivery.transport.transport",
    "Mapping": "probe.sdk.delivery.transport.headers",
    "Any": "probe.sdk.delivery.transport.deadlines",
    "httpx": "probe.sdk.delivery.transport.blobs",
    "CLIENT_KIND_HEADER": "probe.sdk.delivery.transport.transport",
    "device_headers": "probe.sdk.delivery.transport.headers",
    "CLIENT_VERSION_HEADER": "probe.sdk.delivery.transport.transport",
    "client_version_headers": "probe.sdk.delivery.transport.transport",
    "current_client_headers": "probe.sdk.delivery.transport.transport",
    "functools": "probe.sdk.delivery.transport.blobs",
    "urlsplit": "probe.sdk.delivery.transport.blobs",
    "device_mark": "probe.sdk.delivery.transport.transport",
    "client_status": "probe.sdk.delivery.transport.transport",
    "durable": "probe.sdk.delivery.transport.deadlines",
    "errors": "probe.sdk.delivery.transport.transport",
    "safe_warn": "probe.sdk.delivery.transport.transport",
    "session_marker": "probe.sdk.delivery.transport.headers",
    "unstorable": "probe.sdk.delivery.transport.transport",
    "_workspace_limit": "probe.sdk.delivery.transport.headers",
    "DAEMON_SHELL_CONFIG": "probe.sdk.delivery.transport.headers",
    "Settings": "probe.sdk.delivery.transport.transport",
    "AGENT_HEADER": "probe.sdk.delivery.transport.headers",
    "AGENT_SESSION_HEADER": "probe.sdk.delivery.transport.headers",
    "EVENT_AT_ENV": "probe.sdk.delivery.transport.headers",
    "EVENT_AT_HEADER": "probe.sdk.delivery.transport.headers",
    "RUN_WRITE_ORIGIN": "probe.sdk.delivery.transport.headers",
    "WRITE_ORIGIN_HEADER": "probe.sdk.delivery.transport.headers",
    "agent_session_headers": "probe.sdk.delivery.transport.headers",
    "recorded_session_headers": "probe.sdk.delivery.transport.headers",
    "run_write_origin": "probe.sdk.delivery.transport.headers",
    "ATTRIBUTION_HEADER": "probe.sdk.delivery.transport.transport",
    "SURFACE_HEADER": "probe.sdk.delivery.transport.transport",
    "TOOL_HEADER": "probe.sdk.delivery.transport.transport",
    "Surface": "probe.sdk.delivery.transport.headers",
    "current_tool": "probe.sdk.delivery.transport.transport",
    "ssl_context": "probe.sdk.delivery.transport.transport",
}
#: `from <door> import *` takes what the old module's did: every public name.
__all__ = [name for name in _HOMES if not name.startswith("_")]


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
