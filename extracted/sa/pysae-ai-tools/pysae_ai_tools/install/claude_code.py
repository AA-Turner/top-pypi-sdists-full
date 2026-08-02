"""Install or update the Claude Code CLI via the official Anthropic installer.

Delegates to ``https://claude.ai/install.sh`` (Linux/macOS) or
``https://claude.ai/install.ps1`` (Windows) — these are idempotent: running
them again upgrades to the latest version, so we don't try to derive a
"needs update" signal from a public manifest (Anthropic doesn't publish one).
"""

import shutil
import subprocess
from pathlib import Path

from .common import binary, platform
from .common.base import BinaryTool, InstallReport


class ClaudeCodeTool(BinaryTool):
    name = "claude-code"
    binary_name = "claude"
    cli_help = "Install/update the Claude Code CLI"

    def fetch_latest_version(self) -> str:
        # No public version manifest — let the installer be the source of truth.
        return ""

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._run_unix_installer()

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._run_unix_installer()

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        try:
            r = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    "irm https://claude.ai/install.ps1 | iex",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=300,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return InstallReport(error=f"installer failed: {exc}")
        if r.returncode != 0:
            return InstallReport(error=(r.stderr or r.stdout).strip()[:500])
        return InstallReport(
            version=binary.get_version(self.binary_name, "--version"),
            path=shutil.which(self.binary_name) or "",
        )

    def _run_unix_installer(self) -> InstallReport:
        try:
            r = subprocess.run(
                ["bash", "-c", "curl -fsSL https://claude.ai/install.sh | bash"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=300,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return InstallReport(error=f"installer failed: {exc}")
        if r.returncode != 0:
            return InstallReport(error=(r.stderr or r.stdout).strip()[:500])
        installed_path = shutil.which(self.binary_name) or str(Path.home() / ".local" / "bin" / self.binary_name)
        return InstallReport(
            version=binary.get_version(self.binary_name, "--version"),
            path=installed_path,
        )


tool = ClaudeCodeTool()
