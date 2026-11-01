"""Codex's integration (HarnessIntegration): its plugin command line and session log; its sandbox reaps detached work."""

from __future__ import annotations

from pathlib import Path

from ...harness import PluginCli

HARNESS_ID = "codex"


def _get_marketplace_checkout(name: str) -> Path:
    """`$CODEX_HOME/.tmp/marketplaces/<name>`."""
    from .config import codex_home

    return codex_home() / ".tmp" / "marketplaces" / name


class CodexIntegration:
    harness_id = HARNESS_ID
    extra_names = ()
    plugin_cli = PluginCli(
        binary="codex",
        verbs={"refresh": "upgrade", "install": "add", "uninstall": "remove", "list": ("plugin", "list", "--json")},
        checkout=_get_marketplace_checkout,
    )
    #: Its sandbox reaps detached processes, so a background subagent would die with the turn.
    should_audit_inline = True
    has_plugin_ledger = False

    @property
    def session_log(self):
        from .session_log import Codex

        return Codex


INTEGRATION = CodexIntegration()
