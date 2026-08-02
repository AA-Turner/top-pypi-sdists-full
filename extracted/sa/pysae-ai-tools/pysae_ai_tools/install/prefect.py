"""Install or update the Prefect CLI via uv tool."""

import subprocess
from typing import Any

import httpx
import typer

from .common import binary
from .common.base import UvTool


class PrefectTool(UvTool):
    name = "prefect"
    binary_name = "prefect"
    version_arg = "--version"  # fast, local-only (vs "version" which connects to cloud)
    pip_package = "prefect"
    cli_help = "Install/update the Prefect CLI and configure server connection"

    def fetch_latest_version(self) -> str:
        r = httpx.get("https://pypi.org/pypi/prefect/json", timeout=5.0, follow_redirects=True)
        r.raise_for_status()
        v = r.json().get("info", {}).get("version", "")
        return str(v) if v else ""

    def check_auth(self) -> dict[str, Any] | None:
        if not binary.which(self.binary_name):
            return None
        profile = ""
        try:
            r = subprocess.run(
                [self.binary_name, "profile", "ls"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            r = None
        if r is not None:
            for line in r.stdout.splitlines():
                if line.strip().startswith("*"):
                    profile = line.replace("*", "").strip()
                    break

        api_url = ""
        try:
            r = subprocess.run(
                [self.binary_name, "config", "view"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            r = None
        if r is not None:
            for line in r.stdout.splitlines():
                if "PREFECT_API_URL" in line:
                    api_url = line.split("=", 1)[-1].strip().strip("'\"")
                    break

        return {"profile": profile, "api_url": api_url}

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        url = str(state.get("api_url", ""))
        if url:
            label = "Prefect Cloud" if "prefect.cloud" in url else url
            return [(label, typer.colors.BRIGHT_BLACK)]
        return []


tool = PrefectTool()
