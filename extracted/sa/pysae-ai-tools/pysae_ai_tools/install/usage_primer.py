"""Bootstrap entry for the 5H-window primer cron.

Wraps the ``pysae-ai-tools usage prime`` command in a ``*/5`` crontab entry so it shows up in
``pysae-ai-tools tools install`` alongside the other ``Category.EMBEDDED`` entries. Configure
prompts the working hours interactively (delegating to ``usage work-hours``), turns priming on
and installs the cron line; uninstall removes it.

The tool never imports the ``usage`` group (layering forbids ``install → usage``): it drives
everything through the ``pysae-ai-tools usage …`` CLI. Supported on Linux and macOS (crontab);
on Windows ``get_state`` reports nothing to do so the bootstrap quietly skips it.
"""

import platform
import shutil
import subprocess
import sys
from pathlib import Path

import typer

from .common.base import BaseTool, InstallReport, ToolState

SUPPORTED_PLATFORMS = ("Linux", "Darwin")
CRON_MARKER = "# pysae-ai-tools:usage-primer"
CRON_SCHEDULE = "*/5 * * * *"


def _pysae_bin() -> str:
    return shutil.which("pysae-ai-tools") or "pysae-ai-tools"


def _supported() -> bool:
    return platform.system() in SUPPORTED_PLATFORMS and shutil.which("crontab") is not None


def _crontab_read() -> str | None:
    """Current crontab text (``""`` when the user has none), or None if crontab is unusable."""
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
        )
    except (FileNotFoundError, OSError):
        return None
    # A non-zero exit is "no crontab for user" (empty), not a failure.
    return result.stdout if result.returncode == 0 else ""


def _crontab_write(text: str) -> bool:
    try:
        result = subprocess.run(
            ["crontab", "-"],
            input=text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except (FileNotFoundError, OSError):
        return False
    return result.returncode == 0


def _crontab_remove() -> bool:
    """Drop the user's crontab entirely (``crontab -r``), so removing our only line restores
    the true baseline (no crontab) rather than leaving an empty one behind."""
    try:
        result = subprocess.run(
            ["crontab", "-r"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
        )
    except (FileNotFoundError, OSError):
        return False
    return result.returncode == 0


def _cron_line() -> str:
    """The crontab line, with an explicit PATH so cron's minimal env finds both
    ``pysae-ai-tools`` and the ``claude`` binary it shells out to."""
    dirs = [str(Path(p).parent) for b in ("pysae-ai-tools", "claude") if (p := shutil.which(b))]
    path = ":".join(dict.fromkeys([*dirs, "/usr/local/bin", "/usr/bin", "/bin"]))
    return f'{CRON_SCHEDULE} PATH="{path}" {_pysae_bin()} usage prime >/dev/null 2>&1 {CRON_MARKER}'


def _set_cron(present: bool) -> str:
    """Add or remove the primer cron line, preserving every other line.

    Returns ``installed``/``updated`` (present=True), ``removed``/``absent`` (present=False),
    or ``error`` when the crontab could not be read/written."""
    current = _crontab_read()
    if current is None:
        return "error"
    existing = current.splitlines()
    kept = [line for line in existing if CRON_MARKER not in line]
    had = len(kept) != len(existing)
    if present:
        kept.append(_cron_line())
    if not kept:
        # Removed our only line → drop the crontab entirely rather than leave an empty one.
        if had and not _crontab_remove():
            return "error"
        return "removed" if had else "absent"
    body = "\n".join(kept) + "\n"
    if not _crontab_write(body):
        return "error"
    if present:
        return "updated" if had else "installed"
    return "removed" if had else "absent"


def _set_enabled(value: bool) -> None:
    """Flip ``usage.prime.enabled`` via the CLI (no ``usage`` import — layering)."""
    try:
        subprocess.run(
            [_pysae_bin(), "usage", "config", "set", "prime.enabled", "true" if value else "false"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except (FileNotFoundError, OSError):
        pass


class UsagePrimerTool(BaseTool):
    """Synthetic tool wrapping the 5H-window primer cron (no binary)."""

    @property
    def name(self) -> str:
        return "usage-primer"

    def get_state(self) -> ToolState:
        if not _supported():
            return ToolState(
                needs_install=False,
                extra={
                    "configured": True,
                    "note": f"non supporté ici ({platform.system()} / crontab absent) — ignoré.",
                },
            )
        current = _crontab_read()
        present = current is not None and CRON_MARKER in current
        return ToolState(needs_install=not present, extra={"configured": present, "schedule": CRON_SCHEDULE})

    def do_install(self) -> InstallReport:
        # No binary — the cron entry is pure configuration, written by do_configure.
        return InstallReport(action="install", method="nothing to install")

    def do_configure(self) -> InstallReport:
        if not _supported():
            return InstallReport(action="noop", method=f"non supporté ({platform.system()} / crontab absent)")
        # Prompt the working hours only with a real terminal — a non-interactive/CI run keeps
        # whatever is already configured and just enables + schedules.
        if sys.stdin.isatty():
            try:
                subprocess.run([_pysae_bin(), "usage", "work-hours"], check=False)
            except (FileNotFoundError, OSError):
                pass
        _set_enabled(True)
        status = _set_cron(True)
        if status == "error":
            return InstallReport(error="échec de l'écriture de la crontab")
        return InstallReport(
            action="configure", method=f"cron {status} ({CRON_SCHEDULE})", extra={"schedule": CRON_SCHEDULE}
        )

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        if not _supported():
            return InstallReport(action="uninstall", method="non supporté", extra={"removed": False})
        if dry_run:
            current = _crontab_read()
            present = current is not None and CRON_MARKER in current
            return InstallReport(
                action="uninstall",
                method="cron présent" if present else "cron absent",
                extra={"removed": present},
            )
        status = _set_cron(False)
        _set_enabled(False)
        if status == "error":
            return InstallReport(error="échec de la mise à jour de la crontab")
        return InstallReport(action="uninstall", method=f"cron {status}", extra={"removed": status == "removed"})

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        if d.get("configured") and "schedule" in d:
            typer.echo(f"{self.name}: cron actif ({d['schedule']})")
        elif "note" in d:
            typer.echo(f"{self.name}: {d['note']}")
        else:
            typer.echo(f"{self.name}: NOT configured")


tool = UsagePrimerTool()
