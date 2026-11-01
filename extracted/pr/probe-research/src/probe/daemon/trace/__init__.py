"""The daemon's own record of what its agents did: trace files and their shipper (twin: app/companion).
LAZY door for the old `probe.daemon.trace`."""

from __future__ import annotations

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.daemon.trace.trace",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.daemon.trace.trace
    "Any": "probe.daemon.trace.trace",
    "ENV_TRACE": "probe.daemon.trace.trace",
    "ENV_TRACE_MAX_MB": "probe.daemon.trace.trace",
    "KEEP_S": "probe.daemon.trace.trace",
    "MAX_TRACE_BYTES": "probe.daemon.trace.trace",
    "NOISY_LOGGERS": "probe.daemon.trace.trace",
    "Path": "probe.daemon.trace.trace",
    "Recording": "probe.daemon.trace.trace",
    "TaskTrace": "probe.daemon.trace.trace",
    "TraceFile": "probe.daemon.trace.trace",
    "WORKER_LOG": "probe.daemon.trace.trace",
    "_args": "probe.daemon.trace.trace",
    "_drop_none": "probe.daemon.trace.trace",
    "_dump": "probe.daemon.trace.trace",
    "_encode": "probe.daemon.trace.trace",
    "_max_bytes": "probe.daemon.trace.trace",
    "_ms": "probe.daemon.trace.trace",
    "_now": "probe.daemon.trace.trace",
    "_private_dir": "probe.daemon.trace.trace",
    "_sha": "probe.daemon.trace.trace",
    "_tool_defs": "probe.daemon.trace.trace",
    "annotations": "probe.daemon.trace.trace",
    "dataclass": "probe.daemon.trace.trace",
    "datetime": "probe.daemon.trace.trace",
    "enabled": "probe.daemon.trace.trace",
    "finite": "probe.daemon.trace.trace",
    "hashlib": "probe.daemon.trace.trace",
    "json": "probe.daemon.trace.trace",
    "log": "probe.daemon.trace.trace",
    "log_handlers": "probe.daemon.trace.trace",
    "logging": "probe.daemon.trace.trace",
    "math": "probe.daemon.trace.trace",
    "os": "probe.daemon.trace.trace",
    "quiet_noisy_loggers": "probe.daemon.trace.trace",
    "session_dir": "probe.daemon.trace.trace",
    "sessions_dir": "probe.daemon.trace.trace",
    "state_dir": "probe.daemon.trace.trace",
    "store_path": "probe.daemon.trace.trace",
    "time": "probe.daemon.trace.trace",
    "timezone": "probe.daemon.trace.trace",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES, is_lazy=True)
