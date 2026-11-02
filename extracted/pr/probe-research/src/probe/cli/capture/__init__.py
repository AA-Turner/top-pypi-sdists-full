"""Capture: turning it off as a verified postcondition (`capture.py`), and whether it is on
(`state.py`). LAZY front door for the old `probe.cli.capture` module, whose import path this
folder took (agent:14): a read loads `capture.py`; `state.py` never pulls it in."""

from __future__ import annotations

from ...foundation.front_door.front_door import serve_pieces

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "AWAITING_CONFIRMATION": "probe.cli.capture.capture",
    "MARKETPLACE": "probe.cli.capture.capture",
    "OffMode": "probe.cli.capture.capture",
    "PID_DIR_ENV": "probe.cli.capture.capture",
    "Path": "probe.cli.capture.capture",
    "StrEnum": "probe.cli.capture.capture",
    "TokenSource": "probe.cli.capture.capture",
    "TurnOffResult": "probe.cli.capture.capture",
    "_SOURCE_LABELS": "probe.cli.capture.capture",
    "_STOP_LOG_KEEP_LINES": "probe.cli.capture.capture",
    "_STOP_LOG_MAX_BYTES": "probe.cli.capture.capture",
    "_append_stop_log": "probe.cli.capture.capture",
    "_clear_paired_token": "probe.cli.capture.capture",
    "_clear_probe_config_token": "probe.cli.capture.capture",
    "_finish_hosted_recorders": "probe.cli.capture.capture",
    "_looks_like_the_uploader": "probe.cli.capture.capture",
    "_other_sources_with_capture_installed": "probe.cli.capture.capture",
    "_pid_dir": "probe.cli.capture.capture",
    "_set_killswitch": "probe.cli.capture.capture",
    "_source_label": "probe.cli.capture.capture",
    "_source_labels": "probe.cli.capture.capture",
    "_stop_daemon": "probe.cli.capture.capture",
    "_uninstall_plugin": "probe.cli.capture.capture",
    "agent_source": "probe.cli.capture.capture",
    "annotations": "probe.cli.capture.capture",
    "awaiting_confirmation": "probe.cli.capture.capture",
    "capture_plugin_name": "probe.cli.capture.capture",
    "capture_token_sources": "probe.cli.capture.capture",
    "clear_killswitch": "probe.cli.capture.capture",
    "clear_stray_pi_killswitch": "probe.cli.capture.capture",
    "consumes_cli_capture_token": "probe.cli.capture.capture",
    "dataclass": "probe.cli.capture.capture",
    "describe_last_stop": "probe.cli.capture.capture",
    "field": "probe.cli.capture.capture",
    "installed_plugins": "probe.cli.capture.capture",
    "last_stop_event": "probe.cli.capture.capture",
    "os": "probe.cli.capture.capture",
    "pi_config": "probe.cli.capture.capture",
    "plugin_cli": "probe.cli.capture.capture",
    "probe_config_path": "probe.cli.capture.capture",
    "revoke_capture_device": "probe.cli.capture.capture",
    "stop_log_path": "probe.cli.capture.capture",
    "subprocess": "probe.cli.capture.capture",
    "tap_plugin_dir": "probe.cli.capture.capture",
    "tap_token_env": "probe.cli.capture.capture",
    "turn_off": "probe.cli.capture.capture",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=("probe.cli.capture.capture",), is_lazy=True)
