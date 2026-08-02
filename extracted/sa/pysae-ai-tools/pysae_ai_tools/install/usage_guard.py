"""Bootstrap entry for the Claude usage status-line feed.

Wraps the existing ``pysae-ai-tools usage setup`` command as a ``Category.EMBEDDED`` tool, so it
can be opted into from ``pysae-ai-tools tools install``. Off by default. The usage hooks
themselves (``PreToolUse`` + ``UserPromptSubmit``) now ship with the plugin; what remains here is
the ``statusLine`` feed those hooks read (the plugin does not manage status lines) and the
migration that strips any legacy usage hook still sitting in ``settings.json``.

Layering forbids ``install → usage``: the tool drives everything through the
``pysae-ai-tools usage setup …`` CLI (single source of truth), reading its ``status --json`` for
state rather than duplicating the settings.json probing here.
"""

import json
import shutil
import subprocess

import typer

from .common.base import BaseTool, InstallReport, ToolState


def _pysae_bin() -> str:
    return shutil.which("pysae-ai-tools") or "pysae-ai-tools"


def _setup(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_pysae_bin(), "usage", "setup", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


class UsageGuardTool(BaseTool):
    """Synthetic tool wrapping the usage notification + blocking hooks (no binary)."""

    @property
    def name(self) -> str:
        return "usage-guard"

    def get_state(self) -> ToolState:
        result = _setup("status", "--json")
        configured = False
        legacy = False
        try:
            data = json.loads(result.stdout or "{}")
            if isinstance(data, dict):
                configured = bool(data.get("configured"))
                hooks = data.get("hooks")
                legacy = isinstance(hooks, dict) and any(hooks.values())
        except (json.JSONDecodeError, ValueError):
            pass
        # ``configured`` tracks the status-line feed; a residual legacy hook flags a reconfigure so
        # ``usage setup install`` runs once more to strip it.
        return ToolState(
            needs_install=not configured,
            needs_reconfigure=configured and legacy,
            extra={"configured": configured, "legacy_hooks": legacy},
        )

    def do_install(self) -> InstallReport:
        # No binary — the status line lives in settings.json, written by do_configure.
        return InstallReport(action="install", method="nothing to install")

    def do_configure(self) -> InstallReport:
        result = _setup("install")
        if result.returncode != 0:
            return InstallReport(error=(result.stderr or result.stdout or "usage setup install a échoué").strip()[:300])
        return InstallReport(action="configure", method=(result.stdout or "").strip() or "statusline configurée")

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        if dry_run:
            present = bool(self.get_state().extra.get("configured"))
            return InstallReport(
                action="uninstall",
                method="hooks présents" if present else "hooks absents",
                extra={"removed": present},
            )
        result = _setup("uninstall")
        if result.returncode != 0:
            return InstallReport(error=(result.stderr or result.stdout or "").strip()[:300])
        return InstallReport(
            action="uninstall",
            method=(result.stdout or "").strip() or "statusline retirée",
            extra={"removed": "REMOVED" in (result.stdout or "")},
        )

    def format_check(self, state: ToolState) -> None:
        configured = bool(state.to_dict().get("configured"))
        typer.echo(f"{self.name}: {'statusline feed actif' if configured else 'NOT configured'}")


tool = UsageGuardTool()
