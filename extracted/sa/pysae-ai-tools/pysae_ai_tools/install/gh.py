"""Install or update the GitHub CLI (gh)."""

import os
import re
import subprocess
from typing import Any

import typer

from .common import binary, github, platform
from .common.base import ArchiveBinaryTool


class GhTool(ArchiveBinaryTool):
    name = "gh"
    binary_name = "gh"
    cli_help = "Install/update the GitHub CLI (gh) and authenticate"
    winget_package = "GitHub.cli"
    brew_package = "gh"

    def fetch_latest_version(self) -> str:
        return github.latest_release("cli/cli")

    def archive_info(self, version: str, plat: platform.Platform) -> tuple[str, str | None]:
        ver = version.lstrip("v")
        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        if plat.is_windows:
            return (
                f"https://github.com/cli/cli/releases/download/v{ver}/gh_{ver}_windows_{arch}.zip",
                "bin/gh.exe",
            )
        base = f"gh_{ver}_{plat.os.value}_{arch}"
        return f"https://github.com/cli/cli/releases/download/v{ver}/{base}.tar.gz", f"{base}/bin/gh"

    def check_auth(self) -> dict[str, Any] | None:
        if not binary.which(self.binary_name):
            return {"auth_ok": False, "auth_message": "gh not installed"}
        try:
            r = subprocess.run(
                [self.binary_name, "auth", "status"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10,
                env={**os.environ},
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {
                "auth_ok": False,
                "auth_message": f"gh auth status failed: {exc}",
                "has_gh_token_env": bool(os.environ.get("GH_TOKEN")),
            }
        return {
            "auth_ok": r.returncode == 0,
            "auth_message": (r.stdout + r.stderr).strip(),
            "has_gh_token_env": bool(os.environ.get("GH_TOKEN")),
        }

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        msg = str(state.get("auth_message", ""))
        m = re.search(r"Logged in to .+ account (\S+)", msg)
        if m:
            return [(f"@{m.group(1)}", typer.colors.BRIGHT_BLACK)]
        return []


tool = GhTool()
