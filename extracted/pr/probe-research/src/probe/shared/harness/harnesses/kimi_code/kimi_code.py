"""Kimi Code's integration (HarnessIntegration): no plugin command, so Probe edits its plugin list; its session log."""

from __future__ import annotations

from types import ModuleType

from ...harness import PluginCli

HARNESS_ID = "kimi_code"


def _get_plugin_list() -> ModuleType:
    from . import config

    return config


class KimiCodeIntegration:
    harness_id = HARNESS_ID
    extra_names = ()
    plugin_cli = PluginCli(
        binary="kimi",
        plugin_list=_get_plugin_list,
        no_command="Kimi Code has no plugin command; kimi_config edits its plugin list",
    )
    should_audit_inline = False
    has_plugin_ledger = False

    @property
    def session_log(self):
        from .session_log import KimiCode

        return KimiCode


INTEGRATION = KimiCodeIntegration()
