"""Shared agent runtime probes layered onto process enumeration.

Process-table/listener enumeration remains the primary runtime source. Some
agent gateways also expose service-manager or container signals, so this module
runs those checks once for all registered agent signatures and annotates the
same :class:`ProcessCandidate` stream consumed by the classifier.

Standard-library only for the frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from collections.abc import Sequence

import structlog

from runlayer_cli import regex_safe
from runlayer_cli.scan.agents.install import AgentRuntimeSignature
from runlayer_cli.scan.processes.models import ProcessCandidate

logger = structlog.get_logger(__name__)

_LAUNCHCTL_PID_RE = regex_safe.compile(r"^\s*pid\s*=\s*(\d+)\s*$", regex_safe.MULTILINE)
_LAUNCHCTL_RUNNING_RE = regex_safe.compile(
    r"^\s*state\s*=\s*running\s*$",
    regex_safe.MULTILINE,
)


def _run_success(command: list[str], *, timeout: int) -> str | None:
    """Return stdout for a successful bounded subprocess."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout if result.returncode == 0 else None


def parse_launchctl_pid(output: str) -> int | None:
    """Extract a positive pid from ``launchctl print`` output."""
    match = _LAUNCHCTL_PID_RE.search(output)
    if match is None:
        return None
    pid = int(match.group(1))
    return pid if pid > 0 else None


def parse_systemd_main_pid(output: str) -> int | None:
    """Extract a positive MainPID from ``systemctl show --value`` output."""
    value = output.strip()
    if not value.isdigit():
        return None
    pid = int(value)
    return pid if pid > 0 else None


def _service_sightings(
    signatures: Sequence[AgentRuntimeSignature],
    *,
    timeout: int,
) -> list[tuple[str, str, int | None]]:
    """Return ``(framework_id, signal, pid)`` for active registered services."""
    system = platform.system()
    sightings: list[tuple[str, str, int | None]] = []

    if system == "Darwin":
        uid = os.getuid()
        for signature in signatures:
            for label in signature.launchd_labels():
                target = f"gui/{uid}/{label}"
                output = _run_success(
                    ["launchctl", "print", target],
                    timeout=timeout,
                )
                if output is not None and _LAUNCHCTL_RUNNING_RE.search(output):
                    sightings.append(
                        (
                            signature.framework_id,
                            "service:launchd",
                            parse_launchctl_pid(output),
                        )
                    )
    elif system == "Linux":
        for signature in signatures:
            for unit in signature.systemd_units():
                active = _run_success(
                    ["systemctl", "--user", "is-active", unit],
                    timeout=timeout,
                )
                if active is None or active.strip() != "active":
                    continue
                main_pid = _run_success(
                    [
                        "systemctl",
                        "--user",
                        "show",
                        unit,
                        "--property",
                        "MainPID",
                        "--value",
                    ],
                    timeout=timeout,
                )
                sightings.append(
                    (
                        signature.framework_id,
                        "service:systemd",
                        parse_systemd_main_pid(main_pid or ""),
                    )
                )

    return sightings


def _docker_sightings(
    signatures: Sequence[AgentRuntimeSignature],
    *,
    timeout: int,
) -> list[tuple[str, str, int | None]]:
    """Run one ``docker ps`` pass and match every registered signature."""
    if not any(signature.docker_markers for signature in signatures):
        return []
    if shutil.which("docker") is None:
        return []

    output = _run_success(
        ["docker", "ps", "--format", "{{.ID}}\t{{.Names}}\t{{.Image}}"],
        timeout=timeout,
    )
    if output is None:
        return []

    matched_frameworks: set[str] = set()
    for line in output.splitlines():
        haystack = line.lower()
        for signature in signatures:
            if any(marker.lower() in haystack for marker in signature.docker_markers):
                matched_frameworks.add(signature.framework_id)
    return [
        (framework_id, "docker", None) for framework_id in sorted(matched_frameworks)
    ]


def _next_synthetic_pid(candidates: Sequence[ProcessCandidate]) -> int:
    used = {candidate.pid for candidate in candidates}
    pid = -1
    while pid in used:
        pid -= 1
    return pid


def _annotate_candidate(
    candidates: list[ProcessCandidate],
    *,
    framework_id: str,
    signal: str,
    pid: int | None,
) -> None:
    candidate = next(
        (item for item in candidates if pid is not None and item.pid == pid),
        None,
    )
    if candidate is None and pid is None:
        signal_family = signal.partition(":")[0]
        candidate = next(
            (
                item
                for item in candidates
                if any(
                    existing.partition(":")[0] == signal_family
                    for existing in item.agent_runtime_signals.get(framework_id, ())
                )
            ),
            None,
        )
    if candidate is None:
        candidate = ProcessCandidate(
            pid=pid if pid is not None else _next_synthetic_pid(candidates),
            discovery_source="runtime_probe",
        )
        candidates.append(candidate)

    signals = candidate.agent_runtime_signals.setdefault(framework_id, [])
    if signal not in signals:
        signals.append(signal)


def probe_agent_runtime(
    candidates: list[ProcessCandidate],
    signatures: Sequence[AgentRuntimeSignature],
    *,
    timeout: int,
) -> list[ProcessCandidate]:
    """Annotate the enumerated stream with service/container runtime signals."""
    enriched = list(candidates)
    try:
        sightings = _service_sightings(signatures, timeout=timeout)
    except Exception as exc:
        logger.debug("agent_service_probe_failed", error=str(exc))
        sightings = []
    try:
        sightings.extend(_docker_sightings(signatures, timeout=timeout))
    except Exception as exc:
        logger.debug("agent_docker_probe_failed", error=str(exc))

    for framework_id, signal, pid in sightings:
        _annotate_candidate(
            enriched,
            framework_id=framework_id,
            signal=signal,
            pid=pid,
        )
    return enriched
