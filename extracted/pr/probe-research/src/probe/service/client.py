"""The service client (`python -m probe.service.client ...`, run by every release's hooks and hand-offs).
Front door for the old `probe.service.client`: names read live, a patch reaches every piece binding the name."""

from __future__ import annotations

import sys

if __name__ == "__main__":  # A1, kept for good: the cli piece has no main block
    from probe.foundation.service_api.cli import main

    sys.exit(main())

from probe.foundation.front_door.front_door import serve_pieces

# Every piece loads here, in load order, as the old module ran whole on import (static, so the
# test gate's import graph sees this door use them).
import probe.foundation.service_api.service_api as _piece_service_api  # noqa: F401
import probe.foundation.service_api.start as _piece_start  # noqa: F401
import probe.foundation.service_api.calls as _piece_calls  # noqa: F401
import probe.foundation.service_api.cli as _piece_cli  # noqa: F401

#: The old module's pieces, in load order: a write through the door reaches these only.
_PIECES = (
    "probe.foundation.service_api.service_api",
    "probe.foundation.service_api.start",
    "probe.foundation.service_api.calls",
    "probe.foundation.service_api.cli",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.foundation.service_api.service_api
    "API_VERSION": "probe.foundation.service_api.service_api",
    "AnswerTimeout": "probe.foundation.service_api.service_api",
    "Callable": "probe.foundation.service_api.service_api",
    "Client": "probe.foundation.service_api.service_api",
    "Connection": "probe.foundation.service_api.service_api",
    "DESKTOP_TIMEOUT_S": "probe.foundation.service_api.service_api",
    "HANDOFF_BUDGET_S": "probe.foundation.service_api.service_api",
    "JSONRPC": "probe.foundation.service_api.service_api",
    "MAX_LINE_BYTES": "probe.foundation.service_api.service_api",
    "Method": "probe.foundation.service_api.service_api",
    "ServiceError": "probe.foundation.service_api.service_api",
    "TIMEOUT_S": "probe.foundation.service_api.service_api",
    "Unanswered": "probe.foundation.service_api.service_api",
    "call": "probe.foundation.service_api.service_api",
    "call_within": "probe.foundation.service_api.service_api",
    "connect": "probe.foundation.service_api.service_api",
    "contextlib": "probe.foundation.service_api.service_api",
    "encode": "probe.foundation.service_api.service_api",
    "json": "probe.foundation.service_api.service_api",
    "paths": "probe.foundation.service_api.service_api",
    "request": "probe.foundation.service_api.service_api",
    "socket": "probe.foundation.service_api.service_api",
    "time": "probe.foundation.service_api.service_api",
    # probe.foundation.service_api.start
    "ENV_ALLOWLIST": "probe.foundation.service_api.start",
    "Ensured": "probe.foundation.service_api.start",
    "MAX_STARTS": "probe.foundation.service_api.start",
    "SPAWN_SETTLE_S": "probe.foundation.service_api.start",
    "START_LOCK_WAIT_S": "probe.foundation.service_api.start",
    "START_WINDOW_S": "probe.foundation.service_api.start",
    "UNINSTALLING_MESSAGE": "probe.foundation.service_api.start",
    "_BREAKAWAY": "probe.foundation.service_api.start",
    "_DETACHED": "probe.foundation.service_api.start",
    "_children": "probe.foundation.service_api.start",
    "_clean_env": "probe.foundation.service_api.start",
    "_lock": "probe.foundation.service_api.start",
    "_pid_runs": "probe.foundation.service_api.start",
    "_read_starts": "probe.foundation.service_api.start",
    "_reap": "probe.foundation.service_api.start",
    "_spawn": "probe.foundation.service_api.start",
    "_venv_base": "probe.foundation.service_api.start",
    "_without_venv_launcher": "probe.foundation.service_api.start",
    "_write_starts": "probe.foundation.service_api.start",
    "ensure": "probe.foundation.service_api.start",
    "forget_start": "probe.foundation.service_api.start",
    "importlib": "probe.foundation.service_api.start",
    "no_new_privs": "probe.foundation.service_api.start",
    "os": "probe.foundation.service_api.start",
    "procid": "probe.foundation.service_api.start",
    "runtime_python": "probe.foundation.service_api.start",
    "subprocess": "probe.foundation.service_api.start",
    "sys": "probe.foundation.service_api.start",
    "uninstall_barrier": "probe.foundation.service_api.start",
    "write_runtime": "probe.foundation.service_api.start",
    # probe.foundation.service_api.calls
    "CHECK_NOW_WAIT_S": "probe.foundation.service_api.calls",
    "REPORT_ENV": "probe.foundation.service_api.calls",
    "WAIT_FOR_PID_S": "probe.foundation.service_api.calls",
    "_dict": "probe.foundation.service_api.calls",
    "check_now": "probe.foundation.service_api.calls",
    "desktop_request": "probe.foundation.service_api.calls",
    "drain_outbox": "probe.foundation.service_api.calls",
    "end": "probe.foundation.service_api.calls",
    "finish_recorders": "probe.foundation.service_api.calls",
    "hold_run": "probe.foundation.service_api.calls",
    "locations": "probe.foundation.service_api.calls",
    "owner_of": "probe.foundation.service_api.calls",
    "queue_hook": "probe.foundation.service_api.calls",
    "refresh_manifest": "probe.foundation.service_api.calls",
    "refresh_statusline": "probe.foundation.service_api.calls",
    "register": "probe.foundation.service_api.calls",
    "release_run": "probe.foundation.service_api.calls",
    "send_telemetry": "probe.foundation.service_api.calls",
    "start_import": "probe.foundation.service_api.calls",
    "sync_notes": "probe.foundation.service_api.calls",
    "wait_for_exit": "probe.foundation.service_api.calls",
    "watch_box": "probe.foundation.service_api.calls",
    # probe.foundation.service_api.cli
    "CHECK_TRIGGERS": "probe.foundation.service_api.cli",
    "Mode": "probe.foundation.service_api.cli",
    "argparse": "probe.foundation.service_api.cli",
    "main": "probe.foundation.service_api.cli",
    "report_consent": "probe.foundation.service_api.cli",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
