"""Front door: every name the module had before it was split into this folder."""

from __future__ import annotations

import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.wizard.doctor.daemon_rows",
    "probe.cli.wizard.doctor.local_rows",
    "probe.cli.wizard.doctor.repairs",
    "probe.cli.wizard.doctor.report",
    "probe.cli.wizard.doctor.server_state",
    "probe.cli.wizard.doctor.service_status",
    "probe.cli.wizard.doctor.version_rows",
    "probe.shared.harness.diagnosis",
    "probe.shared.harness.harnesses.codex.doctor",
    "probe.shared.harness.harnesses.kimi_code.doctor",
    "probe.shared.harness.harnesses.pi.doctor",
    "probe.cli.wizard.doctor.doctor",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "dataclasses": "probe.cli.wizard.doctor.server_state",
    "json": "probe.cli.wizard.doctor.local_rows",
    "os": "probe.cli.wizard.doctor.local_rows",
    "shutil": "probe.cli.wizard.doctor.doctor",
    "sys": "probe.cli.wizard.doctor.repairs",
    "time": "probe.cli.wizard.doctor.doctor",
    "Iterator": "probe.cli.wizard.doctor.server_state",
    "Callable": "probe.cli.wizard.doctor.server_state",
    "contextmanager": "probe.cli.wizard.doctor.server_state",
    "ContextVar": "probe.cli.wizard.doctor.server_state",
    "dataclass": "probe.cli.wizard.doctor.server_state",
    "autoupdate": "probe.cli.wizard.doctor.doctor",
    "agent_rules": "probe.cli.wizard.doctor.report",
    "codex_config": "probe.shared.harness.harnesses.codex.doctor",
    "plugin_cli": "probe.cli.wizard.doctor.report",
    "tracking_plugin_name": "probe.cli.wizard.doctor.report",
    "tap_token_env": "probe.cli.wizard.doctor.report",
    "TokenSource": "probe.cli.wizard.doctor.report",
    "PluginState": "probe.cli.wizard.doctor.doctor",
    "McpCredential": "probe.cli.wizard.doctor.doctor",
    "DeviceStateOutcome": "probe.cli.wizard.doctor.doctor",
    "DeviceState": "probe.cli.wizard.doctor.server_state",
    "Capabilities": "probe.cli.wizard.doctor.daemon_rows",
    "TAP_PLUGIN_NAME": "probe.cli.wizard.doctor.report",
    "CODEX_MCP_NOT_CHECKED": "probe.cli.wizard.doctor.doctor",
    "_OK": "probe.shared.harness.diagnosis",
    "_OFF": "probe.shared.harness.diagnosis",
    "_MISSING": "probe.shared.harness.diagnosis",
    "_SOURCE_LABEL": "probe.cli.wizard.doctor.report",
    "_team_note_rows": "probe.cli.wizard.doctor.local_rows",
    "_snapshot_ref_rows": "probe.cli.wizard.doctor.local_rows",
    "_parked_rows": "probe.cli.wizard.doctor.local_rows",
    "_interrupted_import_rows": "probe.cli.wizard.doctor.local_rows",
    "_pi_capture_rows": "probe.shared.harness.harnesses.pi.doctor",
    "_row": "probe.shared.harness.diagnosis",
    "_dropped_with_rows": "probe.cli.wizard.doctor.local_rows",
    "DAEMON_ERROR_LINES": "probe.cli.wizard.doctor.daemon_rows",
    "name_account": "probe.cli.wizard.doctor.server_state",
    "daemon_error_lines": "probe.cli.wizard.doctor.daemon_rows",
    "_daemon_rows": "probe.cli.wizard.doctor.daemon_rows",
    "_diagnostic_reports": "probe.cli.wizard.doctor.daemon_rows",
    "_who_records_rows": "probe.cli.wizard.doctor.daemon_rows",
    "_reader_tokens_today": "probe.cli.wizard.doctor.daemon_rows",
    "_reader_rows": "probe.cli.wizard.doctor.daemon_rows",
    "_version_comparison": "probe.cli.wizard.doctor.doctor",
    "tap_behind_warning": "probe.cli.wizard.doctor.version_rows",
    "_sessions_follow": "probe.cli.wizard.doctor.version_rows",
    "_format_age": "probe.cli.wizard.doctor.daemon_rows",
    "_version_rows": "probe.cli.wizard.doctor.version_rows",
    "codex_hook_rows": "probe.shared.harness.harnesses.codex.doctor",
    "SERVICE_ROWS_SHOWN": "probe.cli.wizard.doctor.service_status",
    "_short": "probe.cli.wizard.doctor.service_status",
    "_session_state": "probe.cli.wizard.doctor.service_status",
    "_recorder_state": "probe.cli.wizard.doctor.service_status",
    "service_rows": "probe.cli.wizard.doctor.service_status",
    "render": "probe.cli.wizard.doctor.report",
    "_device_problems": "probe.cli.wizard.doctor.report",
    "summary": "probe.cli.wizard.doctor.report",
    "stale_codex_token_warning": "probe.shared.harness.harnesses.codex.doctor",
    "_LoginCheck": "probe.cli.wizard.doctor.server_state",
    "_check_login": "probe.cli.wizard.doctor.server_state",
    "_login_from_state": "probe.cli.wizard.doctor.server_state",
    "with_server_state": "probe.cli.wizard.doctor.server_state",
    "_remote_state": "probe.cli.wizard.doctor.server_state",
    "device_state_scope": "probe.cli.wizard.doctor.server_state",
    "collect": "probe.cli.wizard.doctor.doctor",
    "_probe_plugin_of": "probe.cli.wizard.doctor.doctor",
    "_attempt_as_it_stands": "probe.cli.wizard.doctor.doctor",
    "_mcp_token_held": "probe.cli.wizard.doctor.doctor",
    "_daemon_ai_libraries": "probe.cli.wizard.doctor.doctor",
    "_capture_awaiting_confirmation": "probe.cli.wizard.doctor.doctor",
    "_capture_last_stop": "probe.cli.wizard.doctor.doctor",
    "TAP_PYTHON_MISSING": "probe.cli.wizard.doctor.doctor",
    "capture_python_missing": "probe.cli.wizard.doctor.doctor",
    "_agent_version": "probe.cli.wizard.doctor.doctor",
    "_kimi_rows": "probe.shared.harness.harnesses.kimi_code.doctor",
    "_live_runs": "probe.cli.wizard.doctor.doctor",
    "_outbox_status": "probe.cli.wizard.doctor.doctor",
    "drop_unrecoverable_dead_letters": "probe.cli.wizard.doctor.repairs",
    "rescue_outbox": "probe.cli.wizard.doctor.repairs",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
