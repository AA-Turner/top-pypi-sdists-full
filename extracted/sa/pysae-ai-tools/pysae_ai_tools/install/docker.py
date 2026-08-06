"""Install or update Docker Engine.

- Linux: official `get.docker.com` convenience script.
- macOS / Windows: report manual install (Docker Desktop is the only supported path
  and ships with its own installer/updater that we don't try to automate).

Configuration posts the GitLab container-registry login, so a ``docker pull``
from the private registry needs nothing further.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import httpx
import typer

from ..common.docker import daemon_running, registry_logins
from . import registry_credential
from .common import binary, platform
from .common.base import BaseTool, InstallReport, ToolState
from .common.privileged import run_privileged


def compose_available() -> bool:
    if not binary.which("docker"):
        return False
    r = subprocess.run(
        ["docker", "compose", "version"], capture_output=True, text=True, encoding="utf-8", check=False, timeout=5
    )
    return r.returncode == 0


def _install_linux() -> InstallReport:
    with tempfile.TemporaryDirectory(prefix="pysae-docker-") as tmp_dir:
        script = Path(tmp_dir) / "get-docker.sh"
        try:
            r = httpx.get("https://get.docker.com", timeout=30, follow_redirects=True)
            r.raise_for_status()
            script.write_text(r.text, encoding="utf-8")
            script.chmod(0o755)
        except Exception as exc:  # noqa: BLE001
            return InstallReport(error=f"could not fetch get.docker.com: {exc}")
        result = run_privileged(["sh", str(script)], what="Installing Docker Engine")
        if not result.ok:
            return InstallReport(error=result.error or "get.docker.com script failed")

    # Add user to docker group (best-effort)
    user = os.environ.get("USER") or os.environ.get("USERNAME") or ""
    if user:
        run_privileged(["usermod", "-aG", "docker", user], what="Adding you to the docker group", timeout=60)

    return InstallReport(
        method="get.docker.com",
        extra={
            "manual": "Log out and back in (or run `newgrp docker`) so the docker group takes effect.",
        },
    )


def _install_macos() -> InstallReport:
    from .common import brew

    r = brew.install("docker", cask=True)
    if r is not None:
        if r.error:
            return r
        r.extra["manual"] = "Start Docker Desktop from /Applications to launch the engine."
        return r
    return InstallReport(
        extra={
            "manual": (
                "Install Docker Desktop for macOS from https://www.docker.com/products/docker-desktop/ "
                "or run `brew install --cask docker`. Then start Docker Desktop from /Applications."
            ),
        },
    )


def _install_windows() -> InstallReport:
    from .common import winget

    r = winget.install("Docker.DockerDesktop", binary_name="docker")
    if r is not None:
        if r.error:
            return r
        r.extra["manual"] = "WSL2 backend is required. Start Docker Desktop after install."
        return r
    return InstallReport(
        extra={
            "manual": (
                "Install Docker Desktop for Windows from https://www.docker.com/products/docker-desktop/ "
                "or run `winget install Docker.DockerDesktop`. WSL2 backend is required."
            ),
        },
    )


class DockerTool(BaseTool):
    name = "docker"
    cli_help = "Install/update Docker Engine/Desktop and configure registries"
    env_optional = (registry_credential.TOKEN_VAR,)

    def get_state(self) -> ToolState:
        bin_status = binary.status("docker", version_arg="--version")
        daemon = daemon_running()
        compose = compose_available()
        ecr_helper = bool(shutil.which("docker-credential-ecr-login"))
        registries = registry_logins()

        state = ToolState(
            needs_install=not bin_status.installed,
            extra={
                "binary": bin_status.to_dict(),
                "daemon_running": daemon,
                "compose_available": compose,
                "ecr_helper_installed": ecr_helper,
                "registries": registries,
            },
        )
        return registry_credential.augment_state(self.name, state)

    def do_configure(self) -> InstallReport:
        return registry_credential.configure_report(self.name)

    def do_uninstall(self, *, dry_run: bool = False) -> InstallReport:
        return registry_credential.uninstall_report(self.name, dry_run=dry_run)

    def do_install(self) -> InstallReport:
        try:
            plat = platform.detect()
        except ValueError as exc:
            return InstallReport(error=str(exc))
        if plat.is_linux:
            return _install_linux()
        if plat.is_macos:
            return _install_macos()
        if plat.is_windows:
            return _install_windows()
        return InstallReport(error=f"unsupported OS: {plat.os}")

    def format_check(self, state: ToolState) -> None:
        d = state.to_dict()
        bin_info = d.get("binary", {})
        version = bin_info.get("version", "n/a") if isinstance(bin_info, dict) else "n/a"
        daemon = d.get("daemon_running", False)
        compose = d.get("compose_available", False)
        ecr = d.get("ecr_helper_installed", False)
        registries = d.get("registries", {})
        installed = isinstance(bin_info, dict) and bin_info.get("installed", False)

        if installed:
            typer.echo(f"docker: {version} (daemon {'OK' if daemon else 'NOT running'})")
            typer.echo(f"  compose: {'OK' if compose else 'NOT installed'}")
            typer.echo(f"  ECR helper: {'OK' if ecr else 'NOT installed'}")
            typer.echo(f"  registries: {', '.join(registries) or 'none'}")
        else:
            typer.echo("docker: NOT installed")

    def format_install(self, report: InstallReport) -> None:
        if report.error:
            typer.echo(f"FAILED: {report.error}", err=True)
        elif report.method:
            typer.echo(f"installed docker via {report.method}")
            manual = report.extra.get("manual", "")
            if manual:
                typer.echo(str(manual))
        else:
            manual = report.extra.get("manual", "")
            if manual:
                typer.echo(str(manual))

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        if state.get("daemon_running"):
            lines.append(("daemon: running", None))
        registries = state.get("registries", {})
        if registries:
            lines.append((f"registries: {', '.join(registries)}", None))
        lines.extend(registry_credential.identity_lines(state))
        return lines


tool = DockerTool()
