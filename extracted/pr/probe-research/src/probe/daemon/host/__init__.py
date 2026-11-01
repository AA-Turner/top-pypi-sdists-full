"""Hosting every session's worker in one process: host, in-process reads, proxy, write lease, per-run state.
LAZY door for the old `probe.daemon.host` (the service runs `from probe.daemon.host import main` for good)."""

from __future__ import annotations

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.daemon.host.host",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.daemon.host.host
    "ARGV_MARK": "probe.daemon.host.host",
    "BEAT_S": "probe.daemon.host.host",
    "Conn": "probe.daemon.host.host",
    "ENTRY": "probe.daemon.host.host",
    "HANDOVER_AHEAD_S": "probe.daemon.host.host",
    "Host": "probe.daemon.host.host",
    "HostRun": "probe.daemon.host.host",
    "IDLE_EXIT_S": "probe.daemon.host.host",
    "LOG_FORMAT": "probe.daemon.host.host",
    "LOG_HANDLERS_SLOT": "probe.daemon.host.host",
    "MAX_LINE": "probe.daemon.host.host",
    "ORPHAN_MARGIN_S": "probe.daemon.host.host",
    "PROTOCOL": "probe.daemon.host.host",
    "Path": "probe.daemon.host.host",
    "RunLogRouter": "probe.daemon.host.host",
    "SEND_TIMEOUT_S": "probe.daemon.host.host",
    "WATCH_REFRESH_PASSES": "probe.daemon.host.host",
    "WATCH_S": "probe.daemon.host.host",
    "_abs": "probe.daemon.host.host",
    "_close_run_client": "probe.daemon.host.host",
    "_date_handover": "probe.daemon.host.host",
    "_finishing": "probe.daemon.host.host",
    "_one": "probe.daemon.host.host",
    "_raise_open_files": "probe.daemon.host.host",
    "_stat_key": "probe.daemon.host.host",
    "_valid_sid": "probe.daemon.host.host",
    "annotations": "probe.daemon.host.host",
    "argparse": "probe.daemon.host.host",
    "asyncio": "probe.daemon.host.host",
    "contextlib": "probe.daemon.host.host",
    "dataclass": "probe.daemon.host.host",
    "faulthandler": "probe.daemon.host.host",
    "field": "probe.daemon.host.host",
    "json": "probe.daemon.host.host",
    "log": "probe.daemon.host.host",
    "logging": "probe.daemon.host.host",
    "main": "probe.daemon.host.host",
    "os": "probe.daemon.host.host",
    "parse_start": "probe.daemon.host.host",
    "run_handlers": "probe.daemon.host.host",
    "run_hosted": "probe.daemon.host.host",
    "run_loop": "probe.daemon.host.host",
    "selectors": "probe.daemon.host.host",
    "signal": "probe.daemon.host.host",
    "socket": "probe.daemon.host.host",
    "sys": "probe.daemon.host.host",
    "threading": "probe.daemon.host.host",
    "time": "probe.daemon.host.host",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES, is_lazy=True)
