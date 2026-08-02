"""Bootstrap entry for the activity-tracker hooks (PostToolUse + Stop activity logging).

Wraps ``pysae-ai-tools tracker setup`` as a ``Category.EMBEDDED`` tool so it can be opted into from
``pysae-ai-tools tools install``. Off by default. The hooks themselves ship with the Pysae plugin
(``hooks/hooks.json``, gated on this tool's selection); ``tracker setup`` only migrates a legacy
``~/.claude/settings.json`` entry a prior version wrote and keeps the log directory.

Layering forbids ``install → tracker``: the tool drives everything through the
``pysae-ai-tools tracker setup …`` CLI, reading its status output for state.
"""

import shutil
import subprocess

import typer

from .common.base import BaseTool, InstallReport, ToolState


def _pysae_bin() -> str:
    return shutil.which("pysae-ai-tools") or "pysae-ai-tools"


def _setup(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_pysae_bin(), "tracker", "setup", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


class ActivityTrackerTool(BaseTool):
    """Synthetic tool wrapping the activity-tracker hooks (no binary)."""

    @property
    def name(self) -> str:
        return "activity-tracker"

    def get_state(self) -> ToolState:
        # The plugin provides the hooks — nothing to install. A residual legacy entry in
        # settings.json flags a reconfigure so do_configure runs once more to strip it.
        legacy = "LEGACY" in (_setup("status").stdout or "")
        return ToolState(
            needs_install=False,
            needs_update=False,
            needs_reconfigure=legacy,
            extra={"configured": True, "legacy_hook": legacy},
        )

    def do_install(self) -> InstallReport:
        return InstallReport(action="install", method="nothing to install")

    def do_configure(self) -> InstallReport:
        result = _setup("install")
        if result.returncode != 0:
            return InstallReport(
                error=(result.stderr or result.stdout or "tracker setup install a échoué").strip()[:300]
            )
        return InstallReport(action="configure", method=(result.stdout or "").strip() or "tracker prêt")

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        if dry_run:
            present = bool(self.get_state().extra.get("legacy_hook"))
            return InstallReport(
                action="uninstall",
                method="hook legacy présent" if present else "hook absent",
                extra={"removed": present},
            )
        result = _setup("uninstall")
        if result.returncode != 0:
            return InstallReport(error=(result.stderr or result.stdout or "").strip()[:300])
        return InstallReport(
            action="uninstall",
            method=(result.stdout or "").strip() or "hook retiré",
            extra={"removed": "REMOVED" in (result.stdout or "")},
        )

    def format_check(self, state: ToolState) -> None:
        legacy = bool(state.to_dict().get("legacy_hook"))
        typer.echo(f"{self.name}: {'hook legacy à migrer' if legacy else 'suivi d’activité (hooks tracker)'}")


tool = ActivityTrackerTool()
