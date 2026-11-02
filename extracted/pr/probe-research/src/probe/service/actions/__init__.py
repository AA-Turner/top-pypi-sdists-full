"""Actions over the service socket: runs, recovers and cancels, and the children they start.
Front door for the old `probe.service.actions`: names read live, a patch reaches every piece binding the name."""

from __future__ import annotations

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in load order: a write through the door reaches these only.
_PIECES = (
    "probe.service.actions.actions",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.service.actions.actions
    "ACTIONS": "probe.service.actions.actions",
    "ACTION_STOP_GRACE_ENV": "probe.service.actions.actions",
    "ACTION_STOP_GRACE_S": "probe.service.actions.actions",
    "ACTION_TIMEOUT_ENV": "probe.service.actions.actions",
    "ACTION_TIMEOUT_S": "probe.service.actions.actions",
    "Action": "probe.service.actions.actions",
    "ActionManager": "probe.service.actions.actions",
    "ActionState": "probe.service.actions.actions",
    "BusyHolder": "probe.service.actions.actions",
    "Callable": "probe.service.actions.actions",
    "DEDUPE_S": "probe.service.actions.actions",
    "DESKTOP_HUMAN_ENV": "probe.service.actions.actions",
    "EVENT_DEVICE_PROMPT": "probe.service.actions.actions",
    "EVENT_DONE": "probe.service.actions.actions",
    "EVENT_ERROR": "probe.service.actions.actions",
    "ErrorCode": "probe.service.actions.actions",
    "INTERRUPTED_EXIT": "probe.service.actions.actions",
    "JOURNAL_VERSION": "probe.service.actions.actions",
    "KEEP_S": "probe.service.actions.actions",
    "MAX_JOURNALS": "probe.service.actions.actions",
    "MAX_QUEUED_ACTIONS": "probe.service.actions.actions",
    "ORIGIN_DESKTOP": "probe.service.actions.actions",
    "Path": "probe.service.actions.actions",
    "REPORT_TRIGGERS": "probe.service.actions.actions",
    "Record": "probe.service.actions.actions",
    "RefusedReason": "probe.service.actions.actions",
    "ReportTrigger": "probe.service.actions.actions",
    "RpcError": "probe.service.actions.actions",
    "SERVICE_STOPPED": "probe.service.actions.actions",
    "TRIGGER_ENV": "probe.service.actions.actions",
    "_ACTION_ID": "probe.service.actions.actions",
    "_env_seconds": "probe.service.actions.actions",
    "_is_update": "probe.service.actions.actions",
    "_now": "probe.service.actions.actions",
    "_span": "probe.service.actions.actions",
    "asyncio": "probe.service.actions.actions",
    "contextlib": "probe.service.actions.actions",
    "dataclass": "probe.service.actions.actions",
    "done_event": "probe.service.actions.actions",
    "error_event": "probe.service.actions.actions",
    "field": "probe.service.actions.actions",
    "invalid_params": "probe.service.actions.actions",
    "json": "probe.service.actions.actions",
    "os": "probe.service.actions.actions",
    "paths": "probe.service.actions.actions",
    "procid": "probe.service.actions.actions",
    "re": "probe.service.actions.actions",
    "secrets": "probe.service.actions.actions",
    "shell_status": "probe.service.actions.actions",
    "signal": "probe.service.actions.actions",
    "time": "probe.service.actions.actions",
    "update_step": "probe.service.actions.actions",
}

from . import children, loginenv  # noqa: F401 -- the old module's own names for them

# Lazy: this package also holds light modules imported alone; a read loads its piece.
serve_pieces(__name__, _HOMES, pieces=_PIECES, is_lazy=True)
