"""Detect OpenClaw artifacts at rest and describe its runtime signatures.

Based on https://github.com/sun-security/openclaw-detector
Checks for CLI binary, state directory, config, and app bundle.

OpenClaw is an AI agent with no first-party manifest/source signatures to score,
so its at-rest installation is emitted as a
:class:`~runlayer_cli.scan.agents.detect.DiscoveredAgent` (``detection_method``
== ``install``), while service/port/container liveness is handled by the shared
process channel.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path

import structlog

from runlayer_cli.scan.agents.detect import (
    DiscoveredAgent,
    Evidence,
    build_install_agent,
    compute_fingerprint,
)
from runlayer_cli.scan.cli_binaries import get_cli_version, locate_cli_binary

logger = structlog.get_logger(__name__)

DEFAULT_GATEWAY_PORT = 18789

OPENCLAW_FRAMEWORK_ID = "openclaw"
OPENCLAW_DISPLAY_NAME = "OpenClaw"
OPENCLAW_FINGERPRINT_MARKERS = (OPENCLAW_FRAMEWORK_ID,)


@dataclass
class OpenClawDetection:
    """Result of scanning for OpenClaw artifacts at rest."""

    detected: bool = False
    summary: str = "not-installed"
    cli_path: str | None = None
    cli_version: str | None = None
    state_dir: str | None = None
    config_path: str | None = None
    app_bundle: str | None = None


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
    path = locate_cli_binary(
        "openclaw",
        home=_get_home(),
        system=platform.system(),
    )
    return str(path) if path is not None else None


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


def openclaw_launchd_labels() -> tuple[str, ...]:
    """Launchd labels identifying a running OpenClaw gateway."""
    profile = os.environ.get("OPENCLAW_PROFILE", "")
    label = f"bot.molt.gateway.{profile}" if profile else "bot.molt.gateway"
    return (label,)


def openclaw_systemd_units() -> tuple[str, ...]:
    """Systemd user units identifying a running OpenClaw gateway."""
    profile = os.environ.get("OPENCLAW_PROFILE", "")
    unit = (
        f"openclaw-gateway-{profile}.service" if profile else "openclaw-gateway.service"
    )
    return (unit,)


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


def openclaw_gateway_ports() -> tuple[int, ...]:
    """Configured OpenClaw gateway port, falling back to the default."""
    config_path = _get_state_path(_get_home()) / "openclaw.json"
    custom_port = _extract_port_from_config(config_path)
    return (custom_port or DEFAULT_GATEWAY_PORT,)


def openclaw_agent_fingerprint() -> str:
    """Stable identity shared by at-rest and runtime-only OpenClaw sightings."""
    return compute_fingerprint(
        OPENCLAW_FRAMEWORK_ID,
        None,
        OPENCLAW_FINGERPRINT_MARKERS,
    )


def openclaw_installation_path() -> str:
    """Opaque logical root shared across channels without exposing profile names."""
    profile = os.environ.get("OPENCLAW_PROFILE", "")
    if not profile:
        return "runtime:openclaw"
    profile_hash = hashlib.sha256(profile.encode("utf-8")).hexdigest()[:16]
    return f"runtime:openclaw:profile:{profile_hash}"


def detect_openclaw() -> OpenClawDetection:
    """Scan OpenClaw artifacts at rest and return the result."""
    result = OpenClawDetection()
    home = _get_home()

    # CLI binary
    result.cli_path = _locate_cli()
    if result.cli_path:
        result.cli_version = get_cli_version(result.cli_path)

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

    if not (result.cli_path or result.app_bundle or result.state_dir):
        result.summary = "not-installed"
        result.detected = False
    else:
        result.summary = "installed"
        result.detected = True

    return result


def build_openclaw_agent(detection: OpenClawDetection) -> DiscoveredAgent | None:
    """Convert detection results into an install-channel :class:`DiscoveredAgent`.

    Returns ``None`` if OpenClaw was not detected. The fingerprint is computed
    over the set of artifact *kinds* present (not absolute paths) so it stays
    stable across machines for per-org catalog dedupe.
    """
    if not detection.detected:
        return None

    evidence: list[Evidence] = []
    location = openclaw_installation_path()
    if detection.cli_path:
        evidence.append(Evidence("install_artifact", detection.cli_path, "cli"))
    if detection.app_bundle:
        evidence.append(Evidence("install_artifact", detection.app_bundle, "app"))
    if detection.state_dir:
        evidence.append(Evidence("install_artifact", location, "state"))
    if detection.config_path:
        evidence.append(
            Evidence("install_artifact", f"{location}/openclaw.json", "config")
        )

    return build_install_agent(
        framework_id=OPENCLAW_FRAMEWORK_ID,
        display_name=OPENCLAW_DISPLAY_NAME,
        location=location,
        evidence=evidence,
        markers=OPENCLAW_FINGERPRINT_MARKERS,
    )
