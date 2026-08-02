"""Install or update the glab CLI (GitLab CLI)."""

import re
import subprocess
from typing import Any

import typer

from .common import binary, gitlab, platform
from .common.base import ArchiveBinaryTool


class GlabTool(ArchiveBinaryTool):
    name = "glab"
    binary_name = "glab"
    cli_help = "Install/update the glab CLI and authenticate to gitlab.com"
    # winget's GitLab.cli package is unreliable (silent failures with empty
    # output, see ai-tools issue logs). Stick to the GitLab releases ZIP on
    # Windows — same binary, predictable behavior.
    brew_package = "glab"

    def fetch_latest_version(self) -> str:
        return gitlab.latest_release("gitlab-org/cli")

    def archive_info(self, version: str, plat: platform.Platform) -> tuple[str, str | None]:
        ver = version.lstrip("v")
        arch = "amd64" if plat.arch.value == "x86_64" else plat.arch.value
        base = f"https://gitlab.com/gitlab-org/cli/-/releases/v{ver}/downloads/glab_{ver}"
        if plat.is_windows:
            return f"{base}_{plat.os.value}_{arch}.zip", "bin/glab.exe"
        return f"{base}_{plat.os.value}_{arch}.tar.gz", "bin/glab"

    def check_auth(self) -> dict[str, Any] | None:
        if not binary.which(self.binary_name):
            return {"auth_ok": False, "auth_message": "glab not installed"}
        try:
            result = subprocess.run(
                [self.binary_name, "auth", "status"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"auth_ok": False, "auth_message": f"glab auth status failed: {exc}"}
        output = (result.stdout + result.stderr).strip()
        return {"auth_ok": result.returncode == 0, "auth_message": output}

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        msg = str(state.get("auth_message", ""))
        m = re.search(r"Logged in to .+ as (\S+)", msg)
        if m:
            return [(f"@{m.group(1)}", typer.colors.BRIGHT_BLACK)]
        return []


tool = GlabTool()
