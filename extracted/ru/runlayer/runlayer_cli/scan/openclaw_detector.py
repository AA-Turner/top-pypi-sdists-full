"""Detect locally installed OpenClaw on the device.

Based on https://github.com/sun-security/openclaw-detector
Checks for CLI binary, state directory, config, app bundle, gateway service,
gateway port, and Docker artifacts.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import structlog

from runlayer_cli.scan.config_parser import (
    MCPClientConfig,
    MCPServerConfig,
    compute_config_hash,
)

logger = structlog.get_logger(__name__)

DEFAULT_GATEWAY_PORT = 18789


@dataclass
class OpenClawDetection:
    """Result of scanning for OpenClaw presence."""

    detected: bool = False
    summary: str = "not-installed"
    cli_path: str | None = None
    cli_version: str | None = None
    state_dir: str | None = None
    config_path: str | None = None
    app_bundle: str | None = None
    gateway_service: str | None = None
    gateway_port: int | None = None
    gateway_listening: bool = False
    docker_images: list[str] = field(default_factory=list)
    docker_containers: list[str] = field(default_factory=list)


def _get_home() -> Path:
    return Path.home()


def _get_state_path(home: Path) -> Path:
    """Build state directory path, respecting OPENCLAW_PROFILE."""
    profile = os.environ.get("OPENCLAW_PROFILE", "")
    if profile:
        return home / f".openclaw-{profile}"
    return home / ".openclaw"


def _locate_cli() -> str | None:
    """Find the openclaw CLI binary."""
    # Check PATH first
    path = shutil.which("openclaw")
    if path:
        return path

    home = _get_home()
    system = platform.system()

    user_paths = [
        home / ".volta" / "bin" / "openclaw",
        home / ".local" / "bin" / "openclaw",
        home / ".nvm" / "current" / "bin" / "openclaw",
        home / "bin" / "openclaw",
        home / ".cargo" / "bin" / "openclaw",
        home / ".asdf" / "shims" / "openclaw",
        home / ".mise" / "shims" / "openclaw",
        home / ".nix-profile" / "bin" / "openclaw",
    ]
    for candidate in user_paths:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)

    system_paths = [
        Path("/usr/local/bin/openclaw"),
        Path("/usr/bin/openclaw"),
        Path("/opt/openclaw/bin/openclaw"),
    ]
    if system == "Darwin":
        system_paths.append(Path("/opt/homebrew/bin/openclaw"))
    elif system == "Linux":
        system_paths.extend(
            [
                Path("/snap/bin/openclaw"),
                Path("/nix/var/nix/profiles/default/bin/openclaw"),
            ]
        )

    for candidate in system_paths:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)

    return None


def _get_cli_version(cli_path: str) -> str | None:
    """Get version string from the openclaw binary."""
    try:
        result = subprocess.run(
            [cli_path, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split("\n")[0]
    except Exception:
        pass
    return None


def _find_macos_app_bundle() -> str | None:
    """Check for OpenClaw.app on macOS."""
    if platform.system() != "Darwin":
        return None
    for bundle in [
        Path("/Applications/OpenClaw.app"),
        _get_home() / "Applications" / "OpenClaw.app",
    ]:
        if bundle.is_dir():
            return str(bundle)
    return None


def _check_gateway_service() -> str | None:
    """Check for running OpenClaw gateway service."""
    system = platform.system()
    profile = os.environ.get("OPENCLAW_PROFILE", "")

    if system == "Darwin":
        label = f"bot.molt.gateway.{profile}" if profile else "bot.molt.gateway"
        try:
            uid = os.getuid()
            result = subprocess.run(
                ["launchctl", "print", f"gui/{uid}/{label}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return f"gui/{uid}/{label}"
        except Exception:
            pass

    elif system == "Linux":
        unit = (
            f"openclaw-gateway-{profile}.service"
            if profile
            else "openclaw-gateway.service"
        )
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", unit],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return unit
        except Exception:
            pass

    return None


def _probe_port(port: int) -> bool:
    """Check if a TCP port is listening on localhost."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2):
            return True
    except (OSError, TimeoutError):
        return False


def _extract_port_from_config(config_path: Path) -> int | None:
    """Read custom gateway port from openclaw.json."""
    try:
        data = json.loads(config_path.read_text())
        port = data.get("port")
        if isinstance(port, int):
            return port
    except Exception:
        pass
    return None


def _scan_docker() -> tuple[list[str], list[str]]:
    """Scan for OpenClaw Docker images and running containers."""
    images: list[str] = []
    containers: list[str] = []

    if not shutil.which("docker"):
        return images, containers

    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            images = [
                line
                for line in result.stdout.strip().splitlines()
                if "openclaw" in line.lower()
            ]
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}} ({{.Image}})"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            containers = [
                line
                for line in result.stdout.strip().splitlines()
                if "openclaw" in line.lower()
            ]
    except Exception:
        pass

    return images, containers


def detect_openclaw() -> OpenClawDetection:
    """Run all OpenClaw detection checks and return results."""
    result = OpenClawDetection()
    home = _get_home()

    # CLI binary
    result.cli_path = _locate_cli()
    if result.cli_path:
        result.cli_version = _get_cli_version(result.cli_path)

    # State directory
    state_path = _get_state_path(home)
    if state_path.is_dir():
        result.state_dir = str(state_path)

    # Config file
    config_file = state_path / "openclaw.json"
    if config_file.is_file():
        result.config_path = str(config_file)

    # macOS app bundle
    result.app_bundle = _find_macos_app_bundle()

    # Gateway service
    result.gateway_service = _check_gateway_service()

    # Gateway port
    port = DEFAULT_GATEWAY_PORT
    if result.config_path:
        custom_port = _extract_port_from_config(Path(result.config_path))
        if custom_port:
            port = custom_port
    if _probe_port(port):
        result.gateway_listening = True
        result.gateway_port = port

    # Docker
    result.docker_images, result.docker_containers = _scan_docker()

    # Determine summary
    is_installed = bool(
        result.cli_path
        or result.app_bundle
        or result.state_dir
        or result.gateway_service
        or result.gateway_listening
        or result.docker_images
        or result.docker_containers
    )
    is_running = bool(
        result.gateway_service or result.gateway_listening or result.docker_containers
    )

    if not is_installed:
        result.summary = "not-installed"
        result.detected = False
    elif is_running:
        result.summary = "installed-and-running"
        result.detected = True
    else:
        result.summary = "installed-not-running"
        result.detected = True

    return result


def build_openclaw_config(detection: OpenClawDetection) -> MCPClientConfig | None:
    """Convert detection results into a synthetic MCPClientConfig.

    Returns None if OpenClaw was not detected.
    """
    if not detection.detected:
        return None

    servers: list[MCPServerConfig] = []

    # Gateway server entry
    if detection.gateway_listening and detection.gateway_port:
        gw = MCPServerConfig(
            name="openclaw-gateway",
            type="http",
            url=f"http://localhost:{detection.gateway_port}",
        )
        gw.config_hash = compute_config_hash(gw)
        servers.append(gw)

    # CLI entry
    if detection.cli_path:
        cli = MCPServerConfig(
            name="openclaw-cli",
            type="stdio",
            command=detection.cli_path,
        )
        cli.config_hash = compute_config_hash(cli)
        servers.append(cli)

    # App bundle (macOS)
    if detection.app_bundle:
        app = MCPServerConfig(
            name="openclaw-app",
            type="stdio",
            command=detection.app_bundle,
        )
        app.config_hash = compute_config_hash(app)
        servers.append(app)

    # Docker containers
    for container in detection.docker_containers:
        dc = MCPServerConfig(
            name=f"openclaw-docker-{container.split()[0]}",
            type="stdio",
            command="docker",
            args=["exec", container.split()[0], "openclaw"],
        )
        dc.config_hash = compute_config_hash(dc)
        servers.append(dc)

    if not servers:
        # Detected but no specific server artifacts — create a placeholder
        placeholder = MCPServerConfig(
            name="openclaw",
            type="stdio",
            command="openclaw",
        )
        placeholder.config_hash = compute_config_hash(placeholder)
        servers.append(placeholder)

    return MCPClientConfig(
        client="openclaw",
        client_version=detection.cli_version,
        config_path=detection.config_path or detection.state_dir,
        servers=servers,
        config_scope="global",
    )
