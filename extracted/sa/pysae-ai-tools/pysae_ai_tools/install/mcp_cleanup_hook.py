"""Bootstrap entry that migrates the MCP-cleanup ``SessionEnd`` hook out of settings.json.

Wraps :mod:`pysae_ai_tools.install.mcp_cleanup` so it shows up in
``pysae-ai-tools tools install`` alongside other ``Category.EMBEDDED`` entries
(``slack-env``, ``pysae-env-shell``). The hook itself now ships with the Pysae plugin
(``hooks/hooks.json``); this tool only strips a legacy entry a prior version wrote directly into
``~/.claude/settings.json`` so it does not fire twice. Cleanup is platform-agnostic — there is
nothing to install, only a stale entry to remove wherever one exists.
"""

from .common.base import BaseTool, InstallReport, ToolState
from .mcp_cleanup import (
    SETTINGS_PATH,
    install_hook,
    is_hook_installed,
    uninstall_hook,
)


class McpCleanupHookTool(BaseTool):
    """Synthetic tool migrating the MCP-cleanup ``SessionEnd`` hook to the plugin (no binary)."""

    @property
    def name(self) -> str:
        return "mcp-cleanup-hook"

    def get_state(self) -> ToolState:
        # The plugin provides the hook — nothing to install. A residual legacy entry flags a
        # reconfigure so do_configure runs once more to strip it.
        legacy = is_hook_installed()
        return ToolState(
            needs_install=False,
            needs_update=False,
            needs_reconfigure=legacy,
            extra={"configured": True, "legacy_hook": legacy, "settings_path": str(SETTINGS_PATH)},
        )

    def do_install(self) -> InstallReport:
        return InstallReport(action="install", method="nothing to install")

    def do_configure(self) -> InstallReport:
        if install_hook() == "already-migrated":
            return InstallReport(action="noop", path=str(SETTINGS_PATH), method="no legacy hook to migrate")
        return InstallReport(action="configure", path=str(SETTINGS_PATH), method="legacy SessionEnd hook migrated")

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        if dry_run:
            present = is_hook_installed()
            return InstallReport(
                action="uninstall",
                path=str(SETTINGS_PATH),
                method="SessionEnd hook present" if present else "hook not configured",
                extra={"removed": present},
            )
        removed = uninstall_hook() == "removed"
        return InstallReport(
            action="uninstall",
            path=str(SETTINGS_PATH),
            method="SessionEnd hook removed" if removed else "hook not configured",
            extra={"removed": removed},
        )


tool = McpCleanupHookTool()
