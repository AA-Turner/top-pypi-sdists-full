"""Bootstrap entry for the ``pysae-env`` shell integration.

Adds the ``pysae-ai-tools env shell-init`` line to the startup file of **every
shell installed on the machine** (bash, zsh, fish, PowerShell) — the same
multi-shell approach as ``conda init``. For cmd.exe (which has no shell functions)
a ``pysae-env.bat`` shim is dropped next to the ``pysae-ai-tools`` executable on
PATH instead. Idempotent: a shell already carrying the line (or the shim) is left
untouched.
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ..env.shell_init import CMD_SHIM
from .common.base import BaseTool, InstallReport, ToolState

MARKER = "pysae-ai-tools env shell-init"
COMMENT = "# pysae-ai-tools shell integration (pysae-env)"
CMD_SHIM_NAME = "pysae-env.bat"

POSIX_LINE = f'{COMMENT}\neval "$(pysae-ai-tools env shell-init)"\n'
FISH_LINE = f"{COMMENT}\npysae-ai-tools env shell-init --shell fish | source\n"
POWERSHELL_LINE = f"{COMMENT}\npysae-ai-tools env shell-init --shell powershell | Out-String | Invoke-Expression\n"


@dataclass(frozen=True)
class _Target:
    shell: str
    rc: Path
    line: str


def _powershell_profile() -> Path | None:
    """Resolve the current-user PowerShell profile path via the pwsh/powershell binary."""
    exe = shutil.which("pwsh") or shutil.which("powershell")
    if not exe:
        return None
    try:
        result = subprocess.run(
            [exe, "-NoProfile", "-Command", "$PROFILE.CurrentUserCurrentHost"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    path = (result.stdout or "").strip()
    return Path(path) if path else None


def _targets() -> list[_Target]:
    """One entry per shell whose binary is on PATH (cmd.exe excluded)."""
    home = Path.home()
    targets: list[_Target] = []
    if shutil.which("bash"):
        targets.append(_Target("bash", home / ".bashrc", POSIX_LINE))
    if shutil.which("zsh"):
        targets.append(_Target("zsh", home / ".zshrc", POSIX_LINE))
    if shutil.which("fish"):
        targets.append(_Target("fish", home / ".config" / "fish" / "config.fish", FISH_LINE))
    profile = _powershell_profile()
    if profile is not None:
        targets.append(_Target("powershell", profile, POWERSHELL_LINE))
    return targets


def _candidate_rcs() -> list[Path]:
    """Every rc file we might have written to — for cleanup, regardless of which
    shell binaries are still on PATH (a shell may have been removed since)."""
    home = Path.home()
    candidates = [home / ".bashrc", home / ".zshrc", home / ".config" / "fish" / "config.fish"]
    profile = _powershell_profile()
    if profile is not None:
        candidates.append(profile)
    return candidates


def _cmd_shim_path() -> Path | None:
    """Where the ``pysae-env.bat`` cmd shim belongs — next to the ``pysae-ai-tools``
    executable (guaranteed on PATH). ``None`` off Windows or when that exe isn't found."""
    if sys.platform != "win32":
        return None
    exe = shutil.which("pysae-ai-tools")
    if not exe:
        return None
    return Path(exe).parent / CMD_SHIM_NAME


def _has_marker(rc: Path) -> bool:
    if not rc.exists():
        return False
    try:
        return MARKER in rc.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def _strip_block(rc: Path) -> None:
    """Remove the injected comment + init line from ``rc`` in place."""
    text = rc.read_text(encoding="utf-8", errors="replace")
    kept = [ln for ln in text.splitlines() if MARKER not in ln and ln.strip() != COMMENT]
    rc.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")


class ShellInitTool(BaseTool):
    """Synthetic tool wrapping the ``pysae-env`` shell integration (no binary)."""

    @property
    def name(self) -> str:
        return "pysae-env-shell"

    def get_state(self) -> ToolState:
        targets = _targets()
        shim = _cmd_shim_path()
        shells = [t.shell for t in targets]
        missing = [t.shell for t in targets if not _has_marker(t.rc)]
        if shim is not None:
            shells.append("cmd")
            if not _has_marker(shim):
                missing.append("cmd")
        if not shells:
            return ToolState(
                needs_install=False,
                needs_update=False,
                extra={"configured": True, "note": "no supported shell detected on PATH"},
            )
        return ToolState(
            needs_install=bool(missing),
            needs_update=False,
            extra={
                "configured": not missing,
                "shells": shells,
                "missing": missing,
            },
        )

    def do_install(self) -> InstallReport:
        # No binary — the shell integration is pure configuration, written by
        # do_configure.
        return InstallReport(action="install", method="nothing to install")

    def do_configure(self) -> InstallReport:
        targets = _targets()
        shim = _cmd_shim_path()
        if not targets and shim is None:
            return InstallReport(action="noop", method="no supported shell on PATH")

        added: list[str] = []
        for t in targets:
            if _has_marker(t.rc):
                continue
            t.rc.parent.mkdir(parents=True, exist_ok=True)
            with t.rc.open("a", encoding="utf-8") as f:
                f.write(("" if not t.rc.exists() else "\n") + t.line)
            added.append(t.shell)

        if shim is not None and not _has_marker(shim):
            shim.write_text(CMD_SHIM + "\n", encoding="utf-8")
            added.append("cmd")

        if not added:
            return InstallReport(action="noop", method="pysae-env already configured in every shell")
        return InstallReport(
            action="configure",
            method=f"pysae-env added to: {', '.join(added)}",
            extra={"shells": added},
        )

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        """Strip the ``pysae-env`` integration from every shell rc, and the cmd shim."""
        hit = [rc for rc in _candidate_rcs() if _has_marker(rc)]
        shim = _cmd_shim_path()
        shim_hit = shim is not None and _has_marker(shim)
        removed = [str(rc) for rc in hit] + ([str(shim)] if shim_hit else [])
        if dry_run:
            return InstallReport(action="uninstall", extra={"removed": removed})
        for rc in hit:
            _strip_block(rc)
        if shim_hit and shim is not None:
            try:
                shim.unlink()
            except OSError:
                pass
        return InstallReport(action="uninstall", extra={"removed": removed})


tool = ShellInitTool()
