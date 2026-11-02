"""Claude Code's integration (HarnessIntegration): its plugin command line, session log and plugin ledger."""

from __future__ import annotations

from pathlib import Path

from ...harness import PluginCli
from . import binary

HARNESS_ID = "claude_code"


def _run_plugin_command(args: list[str], timeout: float) -> binary.Result:
    """Through `binary.run`, which finds the claude executable the way the rest of Probe does."""
    return binary.run(args, timeout=timeout)


def _get_marketplace_checkout(name: str) -> Path:
    """Its plugins folder (`capabilities.claude_plugin_ledger`), `marketplaces/<name>`."""
    from probe.shared.harness.harnesses.claude_code.plugin_ledger import claude_plugin_ledger  # noqa: PLC0415 - it imports the plugin commands

    return claude_plugin_ledger().parent / "marketplaces" / name


class ClaudeCodeIntegration:
    harness_id = HARNESS_ID
    #: `cc`: the capture side's short name for it.
    extra_names = ("cc",)
    plugin_cli = PluginCli(
        binary="claude",
        verbs={"refresh": "update", "install": "install", "uninstall": "uninstall", "list": ("plugin", "list")},
        run=_run_plugin_command,
        checkout=_get_marketplace_checkout,
    )
    should_audit_inline = False
    #: `installed_plugins.json` names the tap's installed version.
    has_plugin_ledger = True

    @property
    def session_log(self):
        from .session_log import ClaudeCode

        return ClaudeCode


INTEGRATION = ClaudeCodeIntegration()
