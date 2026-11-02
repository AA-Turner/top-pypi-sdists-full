"""Front door: every name the module had before it was split into this folder."""

from __future__ import annotations

import importlib

from probe.foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.cli.install.updater.cli_installs.ephemeral",
    "probe.cli.install.upgrade.components",
    "probe.cli.install.upgrade.finish",
    "probe.cli.install.upgrade.package_step",
    "probe.cli.install.upgrade.plugin_pass",
    "probe.cli.install.upgrade.prelude",
    "probe.cli.install.upgrade.turn",
    "probe.shared.harness.harnesses.pi.package_upgrade",
    "probe.cli.install.upgrade.upgrade",
)

# Every piece loads here, as the old module ran whole on import.
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    "dataclasses": "probe.cli.install.upgrade.plugin_pass",
    "contextlib": "probe.cli.install.upgrade.components",
    "contextvars": "probe.cli.install.upgrade.components",
    "os": "probe.cli.install.upgrade.components",
    "signal": "probe.cli.install.upgrade.components",
    "threading": "probe.cli.install.upgrade.components",
    "time": "probe.cli.install.upgrade.components",
    "Sequence": "probe.cli.install.upgrade.upgrade",
    "Callable": "probe.cli.install.upgrade.components",
    "Future": "probe.cli.install.upgrade.components",
    "FuturesTimeout": "probe.cli.install.upgrade.components",
    "contextmanager": "probe.cli.install.upgrade.components",
    "ExitStack": "probe.cli.install.upgrade.turn",
    "field": "probe.cli.install.upgrade.plugin_pass",
    "dataclass": "probe.cli.install.upgrade.components",
    "StrEnum": "probe.cli.install.upgrade.upgrade",
    "wizard_lock": "probe.cli.install.upgrade.turn",
    "updater": "probe.cli.install.updater.cli_installs.ephemeral",
    "root_skills": "probe.cli.install.upgrade.plugin_pass",
    "autoupdate": "probe.cli.install.upgrade.finish",
    "claude_cli": "probe.cli.install.upgrade.components",
    "plugin_cli": "probe.cli.install.upgrade.plugin_pass",
    "versions": "probe.cli.install.updater.cli_installs.ephemeral",
    "update_report": "probe.cli.install.upgrade.finish",
    "agent_source": "probe.cli.install.upgrade.upgrade",
    "update_step": "probe.cli.install.upgrade.turn",
    "get_registry": "probe.cli.install.upgrade.finish",
    "json_events": "probe.cli.install.upgrade.finish",
    "UpdatePart": "probe.cli.install.upgrade.upgrade",
    "_progress": "probe.cli.install.upgrade.upgrade",
    "reporting_progress": "probe.cli.install.upgrade.upgrade",
    "_finished": "probe.cli.install.upgrade.upgrade",
    "UpdateOutcome": "probe.cli.install.upgrade.upgrade",
    "PICKED_UP": "probe.cli.install.upgrade.upgrade",
    "after_update_line": "probe.cli.install.upgrade.upgrade",
    "reloads_plugins": "probe.cli.install.upgrade.upgrade",
    "SKIP_CLI_ENV": "probe.cli.install.upgrade.turn",
    "FORCED_ENV": "probe.cli.install.upgrade.turn",
    "forced_past": "probe.cli.install.upgrade.turn",
    "menu_holds_update_off": "probe.cli.install.upgrade.turn",
    "cli_left_alone": "probe.cli.install.upgrade.prelude",
    "_service_stopped_on_windows": "probe.cli.install.upgrade.turn",
    "_update_turn": "probe.cli.install.upgrade.turn",
    "perform_update": "probe.cli.install.upgrade.upgrade",
    "COMPONENT_DEADLINE_S": "probe.cli.install.upgrade.components",
    "COMPONENT_DEADLINE_ENV": "probe.cli.install.upgrade.components",
    "component_deadline": "probe.cli.install.upgrade.components",
    "ComponentOverdue": "probe.cli.install.upgrade.components",
    "_deadline_words": "probe.cli.install.upgrade.components",
    "_Component": "probe.cli.install.upgrade.components",
    "_start": "probe.cli.install.upgrade.components",
    "_outcome_by": "probe.cli.install.upgrade.components",
    "_ENDING_SIGNALS": "probe.cli.install.upgrade.components",
    "_exit_on_signal": "probe.cli.install.upgrade.components",
    "_stopped_with_the_update": "probe.cli.install.upgrade.components",
    "_stopped_detail": "probe.cli.install.upgrade.components",
    "perform_updates": "probe.cli.install.upgrade.upgrade",
    "_plugin_passes": "probe.cli.install.upgrade.plugin_pass",
    "_plugins_of": "probe.cli.install.upgrade.plugin_pass",
    "_crashed_pass": "probe.cli.install.upgrade.finish",
    "_cli_from": "probe.cli.install.upgrade.finish",
    "_cli_line": "probe.cli.install.upgrade.finish",
    "_perform_update": "probe.cli.install.upgrade.upgrade",
    "_refresh_lifeboat": "probe.cli.install.upgrade.prelude",
    "_Prelude": "probe.cli.install.upgrade.prelude",
    "_AgentPass": "probe.cli.install.upgrade.plugin_pass",
    "_update_prelude": "probe.cli.install.upgrade.prelude",
    "_plugin_pass": "probe.cli.install.upgrade.plugin_pass",
    "_reports_failure": "probe.cli.install.upgrade.plugin_pass",
    "_versions_summary": "probe.cli.install.upgrade.plugin_pass",
    "_finish_pass": "probe.cli.install.upgrade.finish",
    "_record_crash": "probe.cli.install.upgrade.finish",
    "_agent_label": "probe.cli.install.upgrade.finish",
    "_report_attempt": "probe.cli.install.upgrade.finish",
    "_PiUpdate": "probe.shared.harness.harnesses.pi.package_upgrade",
    "package_harness": "probe.cli.install.upgrade.package_step",
    "_package_harness": "probe.cli.install.upgrade.package_step",
    "_pi_update_lock": "probe.shared.harness.harnesses.pi.package_upgrade",
    "_update_pi_package": "probe.shared.harness.harnesses.pi.package_upgrade",
    "_bounded_pi_update": "probe.cli.install.upgrade.package_step",
    "update_owed_pi_package": "probe.cli.install.upgrade.package_step",
    "_update_persistent_copy": "probe.cli.install.updater.cli_installs.ephemeral",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
