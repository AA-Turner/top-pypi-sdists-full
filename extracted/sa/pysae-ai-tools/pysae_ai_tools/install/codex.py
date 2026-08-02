"""Install or update the Codex CLI via its official standalone installer.

Codex ships a native standalone build (the Rust binary under
``~/.codex/packages/standalone``) installed and upgraded by the official script
at ``chatgpt.com/codex/install.sh`` (``install.ps1`` on Windows) — the same
channel the built-in ``codex update`` subcommand drives. The script is
idempotent: it installs when absent and swaps the ``current`` release symlink
when a newer version exists, so we invoke it for both first install and upgrade.

The "needs update" signal comes from the latest GitHub release of
``openai/codex`` (the source of the standalone binaries); its tags carry a
``rust-v`` prefix, so we extract the semver from the tag name.
"""

import os
import subprocess

from .common import binary, github, platform
from .common.base import BinaryTool, InstallReport

_REPO = "openai/codex"
_INSTALL_SH_URL = "https://chatgpt.com/codex/install.sh"
_INSTALL_PS1_URL = "https://chatgpt.com/codex/install.ps1"


class CodexTool(BinaryTool):
    name = "codex"
    binary_name = "codex"
    cli_help = "Install/update the Codex CLI"

    def fetch_latest_version(self) -> str:
        try:
            return binary.extract_version(github.latest_release(_REPO))
        except Exception:  # noqa: BLE001
            return ""

    def install_linux(self, plat: platform.Platform) -> InstallReport:
        return self._official_install()

    def install_macos(self, plat: platform.Platform) -> InstallReport:
        return self._official_install()

    def install_windows(self, plat: platform.Platform) -> InstallReport:
        return self._official_install_windows()

    def _report_from_binary(self, method: str) -> InstallReport:
        return InstallReport(
            version=binary.get_version(self.binary_name, "--version"),
            path=binary.which(self.binary_name),
            method=method,
        )

    def _official_install(self) -> InstallReport:
        try:
            r = subprocess.run(
                ["sh", "-c", f"curl -fsSL {_INSTALL_SH_URL} | sh"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=300,
                env={**os.environ, "CODEX_NON_INTERACTIVE": "1"},
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return InstallReport(error=f"installer failed: {exc}")
        if r.returncode != 0:
            return InstallReport(error=(r.stderr or r.stdout).strip()[:500])
        return self._report_from_binary("standalone (install.sh)")

    def _official_install_windows(self) -> InstallReport:
        command = f"$env:CODEX_NON_INTERACTIVE='1'; irm {_INSTALL_PS1_URL} | iex"
        try:
            r = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
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
        return self._report_from_binary("standalone (install.ps1)")


tool = CodexTool()
