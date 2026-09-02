"""Agent install probes and shared runtime signatures.

The static channel is data-driven (``signatures.json`` + a registry); this gives
agent detection the same shape. Each registration owns an at-rest
``detect -> build_agent`` pair plus declarative runtime signatures consumed by
the shared process channel. The orchestrators never special-case a framework.

Add an install-detected agent by appending a probe here and shipping its
detect/build functions -- exactly like adding a static framework signature.

Standard-library only; safe for the frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from runlayer_cli.scan.agents.detect import DiscoveredAgent
from runlayer_cli.scan.agents.openclaw_detector import (
    build_openclaw_agent,
    detect_openclaw,
    openclaw_agent_fingerprint,
    openclaw_gateway_ports,
    openclaw_installation_path,
    openclaw_launchd_labels,
    openclaw_systemd_units,
)


class InstallDetection(Protocol):
    """Minimal shape the orchestrator reads from any probe's detection result."""

    detected: bool
    summary: str


def _no_runtime_identity() -> str | None:
    return None


@dataclass(frozen=True)
class AgentRuntimeSignature:
    """Signals that identify one framework in the shared process channel."""

    framework_id: str
    argv_markers: tuple[str, ...]
    gateway_ports: Callable[[], tuple[int, ...]]
    launchd_labels: Callable[[], tuple[str, ...]]
    systemd_units: Callable[[], tuple[str, ...]]
    docker_markers: tuple[str, ...]
    agent_fingerprint: Callable[[], str | None] = _no_runtime_identity
    installation_path: Callable[[], str | None] = _no_runtime_identity


@dataclass(frozen=True)
class InstallProbe:
    """One agent registration: at-rest detector, builder, and runtime signals.

    ``build_agent`` params are ``Any`` on purpose: each builder knows its own
    concrete detection type, while the orchestrator only relies on the
    :class:`InstallDetection` shape.
    """

    name: str
    detect: Callable[[], InstallDetection]
    build_agent: Callable[[Any], DiscoveredAgent | None]
    runtime: AgentRuntimeSignature


# The install-probe registry. Append to extend the install channel.
INSTALL_PROBES: tuple[InstallProbe, ...] = (
    InstallProbe(
        name="openclaw",
        detect=detect_openclaw,
        build_agent=build_openclaw_agent,
        runtime=AgentRuntimeSignature(
            framework_id="openclaw",
            argv_markers=("openclaw", "molt.gateway", "bot.molt"),
            gateway_ports=openclaw_gateway_ports,
            launchd_labels=openclaw_launchd_labels,
            systemd_units=openclaw_systemd_units,
            docker_markers=("openclaw",),
            agent_fingerprint=openclaw_agent_fingerprint,
            installation_path=openclaw_installation_path,
        ),
    ),
)


def runtime_signatures() -> tuple[AgentRuntimeSignature, ...]:
    """Runtime signatures registered for the shared process channel."""
    return tuple(probe.runtime for probe in INSTALL_PROBES)
