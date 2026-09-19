"""Bounded, allowlisted execution inside running WSL distributions."""

from __future__ import annotations

import math
import os
import subprocess
import threading
import time
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from itertools import islice

from runlayer_cli.scan.containers.inspect_parse import (
    MAX_CONTAINERS,
    DiscoveredContainer,
)
from runlayer_cli.scan.completeness import CompletionStatusResult, ScanCompletionStatus
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.safe_parse import parse_json
from runlayer_cli.scan.wsl_limits import (
    MAX_WSL_DISTROS,
    WSL_CONTAINER_SCAN_TIME_BUDGET_S,
)

WSL_EXEC_TIMEOUT_S = 10.0
MAX_WSL_EXEC_OUTPUT_BYTES = 512 * 1024
_READ_CHUNK_BYTES = 64 * 1024
_MIN_WSL_EXEC_TIMEOUT_MS = 50
_MAX_WSL_EXEC_TIMEOUT_MS = 300_000
_WSL_TIMEOUT_HEADROOM_MS = 1_000
_RUNLAYER_CREDENTIAL_ENV_NAMES = frozenset(
    name.casefold()
    for name in (
        "RUNLAYER_API_KEY",
        "RUNLAYER_ORG_API_KEY",
        "RUNLAYER_ENROLLMENT_API_KEY",
        "RUNLAYER_SKILL_SYNC_API_KEY",
        "RUNLAYER_SELF_UPDATE_ORG_KEY",
    )
)
_DOCKER_PS_ARGS = (
    "ps",
    "--last",
    str(MAX_CONTAINERS + 1),
    "--no-trunc",
    "--filter",
    "status=running",
    "--filter",
    "status=paused",
    "--filter",
    "status=restarting",
    "--format",
    "{{json .}}",
)
_PODMAN_PS_ARGS = (
    "ps",
    "--last",
    str(MAX_CONTAINERS + 1),
    "--no-trunc",
    "--filter",
    "status=running",
    "--filter",
    "status=paused",
    "--format",
    "{{json .}}",
)
_CONTAINER_PS_ARGS_BY_RUNTIME = {
    "docker": _DOCKER_PS_ARGS,
    "podman": _PODMAN_PS_ARGS,
}
WSL_PS_ARGS = ("-axww", "-o", "pid=,ppid=,user:32=,lstart=,args=")


@dataclass(frozen=True)
class WSLCommandResult:
    stdout: str


@dataclass
class WSLContainerScanResult(CompletionStatusResult):
    containers: list[DiscoveredContainer] = field(default_factory=list)
    scanned_distros: list[str] = field(default_factory=list)
    completion: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)


@dataclass
class _ContainerAccumulator:
    limit: int
    containers: list[DiscoveredContainer]
    seen: set[tuple[str, str]] = field(default_factory=set)

    @property
    def full(self) -> bool:
        return len(self.containers) >= self.limit

    def add(self, container: DiscoveredContainer) -> bool:
        """Retain a novel container and report true aggregate overflow."""
        key = ((container.wsl_distro or "").casefold(), container.container_id)
        if key in self.seen:
            return False
        self.seen.add(key)
        if self.full:
            return True
        self.containers.append(container)
        return False


@dataclass
class _WSLDistroScanOutcome(CompletionStatusResult):
    scanned: bool = False
    stop: bool = False
    completion: ScanCompletionStatus = field(default_factory=ScanCompletionStatus)


def _command_is_allowed(command: Sequence[str]) -> bool:
    if not command:
        return False
    container_args = _CONTAINER_PS_ARGS_BY_RUNTIME.get(command[0])
    if container_args is not None:
        return tuple(command[1:]) == container_args
    return command[0] == "ps" and tuple(command[1:]) == WSL_PS_ARGS


def _wsl_environment() -> dict[str, str]:
    environment = dict(os.environ)
    for name in tuple(environment):
        casefolded_name = name.casefold()
        if casefolded_name in _RUNLAYER_CREDENTIAL_ENV_NAMES:
            del environment[name]
        elif casefolded_name == "wslenv":
            environment[name] = ":".join(
                entry
                for entry in environment[name].split(":")
                if entry.partition("/")[0].casefold()
                not in _RUNLAYER_CREDENTIAL_ENV_NAMES
            )
        elif casefolded_name == "wsl_utf8":
            del environment[name]
    environment["WSL_UTF8"] = "1"
    return environment


def _bounded_timeout_ms(timeout: float) -> int | None:
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        return None
    try:
        timeout_seconds = float(timeout)
    except OverflowError:
        return None
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        return None
    bounded_timeout_seconds = min(
        max(timeout_seconds, _MIN_WSL_EXEC_TIMEOUT_MS / 1_000),
        _MAX_WSL_EXEC_TIMEOUT_MS / 1_000,
    )
    return int(bounded_timeout_seconds * 1_000)


def _in_vm_timeout_arg(timeout_ms: int) -> str:
    headroom_ms = min(_WSL_TIMEOUT_HEADROOM_MS, max(1, timeout_ms // 2))
    deadline_ms = timeout_ms - headroom_ms
    return str(max(1, (deadline_ms + 999) // 1_000))


def run_wsl_command(
    distro: str,
    command: Sequence[str],
    *,
    timeout: float = WSL_EXEC_TIMEOUT_S,
    max_output_bytes: int = MAX_WSL_EXEC_OUTPUT_BYTES,
) -> WSLCommandResult | None:
    """Run one fixed read-only command with hard time and stdout caps."""
    if not distro or not _command_is_allowed(command):
        raise ValueError("unsupported WSL command")

    timeout_ms = _bounded_timeout_ms(timeout)
    if timeout_ms is None:
        return None
    environment = _wsl_environment()
    try:
        process = subprocess.Popen(
            [
                "wsl.exe",
                "--distribution",
                distro,
                "--exec",
                "timeout",
                "-s",
                "KILL",
                _in_vm_timeout_arg(timeout_ms),
                *command,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=environment,
        )
    except OSError:
        return None

    output = bytearray()
    read_failed = False
    truncated = False

    def terminate() -> None:
        try:
            process.kill()
        except OSError:
            pass

    def read_stdout() -> None:
        nonlocal read_failed, truncated
        stdout = process.stdout
        if stdout is None:
            read_failed = True
            return
        while True:
            try:
                chunk = stdout.read(_READ_CHUNK_BYTES)
            except (OSError, ValueError):
                read_failed = True
                return
            if not chunk:
                return
            if len(output) + len(chunk) > max_output_bytes:
                truncated = True
                terminate()
                return
            output.extend(chunk)

    reader = threading.Thread(target=read_stdout, daemon=True)
    reader.start()
    wait_failed = False
    try:
        try:
            process.wait(timeout=timeout_ms / 1_000)
        except (OSError, subprocess.TimeoutExpired):
            wait_failed = True
            terminate()
            try:
                process.wait(timeout=1)
            except (OSError, subprocess.TimeoutExpired):
                pass
        reader.join(timeout=1)
        if reader.is_alive() and process.stdout is not None:
            try:
                process.stdout.close()
            except (OSError, ValueError):
                pass
            reader.join(timeout=1)
        if (
            wait_failed
            or reader.is_alive()
            or read_failed
            or truncated
            or process.returncode != 0
        ):
            return None
        try:
            return WSLCommandResult(stdout=bytes(output).decode("utf-8"))
        except UnicodeDecodeError:
            return None
    finally:
        if process.stdout is not None:
            try:
                process.stdout.close()
            except (OSError, ValueError):
                pass


def _parse_container_rows(
    text: str,
    *,
    runtime: str,
    distro: str,
) -> tuple[list[DiscoveredContainer], bool]:
    containers: list[DiscoveredContainer] = []
    seen: set[str] = set()
    malformed = False
    truncated = False
    for line in text.splitlines():
        if not line.strip():
            malformed = True
            continue
        outcome = parse_json(line)
        if outcome["error"] is not None:
            malformed = True
            continue
        row = outcome["value"]
        if not isinstance(row, dict):
            malformed = True
            continue
        container_id = row.get("ID") or row.get("Id")
        if not isinstance(container_id, str) or not container_id:
            malformed = True
            continue
        if container_id in seen:
            malformed = True
            continue
        if len(containers) >= MAX_CONTAINERS:
            truncated = True
            break
        seen.add(container_id)
        name = row.get("Names")
        if isinstance(name, list):
            name = next(
                (
                    candidate
                    for candidate in name
                    if isinstance(candidate, str) and candidate
                ),
                None,
            )
        image_ref = row.get("Image")
        containers.append(
            DiscoveredContainer(
                container_id=container_id,
                name=name if isinstance(name, str) and name else None,
                image_ref=(
                    image_ref if isinstance(image_ref, str) and image_ref else None
                ),
                image_digest=None,
                runtime=runtime,
                wsl_distro=distro,
            )
        )
    return containers, not malformed and not truncated


def _scan_wsl_container_distro(
    distro: DiscoveredWSLDistro,
    *,
    deadline: float,
    timeout: float,
    accumulator: _ContainerAccumulator,
    has_remaining_distros: bool,
    checkpoint: Callable[[], None] | None,
) -> _WSLDistroScanOutcome:
    """Scan one distro and decide its authority, reason, and stop state."""
    outcome = _WSLDistroScanOutcome()
    if time.monotonic() >= deadline:
        outcome.mark_incomplete("wsl_container_scan_timed_out")
        outcome.stop = True
        return outcome

    runtime_succeeded = False
    inventory_complete = True
    parsed_inventory_incomplete = False
    over_capacity = False
    expected_runtimes = set(distro.container_runtimes)
    for runtime in ("docker", "podman"):
        if checkpoint is not None:
            checkpoint()
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            runtime_expected_or_unknown = (
                runtime in expected_runtimes or not expected_runtimes
            )
            if runtime_expected_or_unknown:
                inventory_complete = False
            if runtime_expected_or_unknown or has_remaining_distros:
                outcome.mark_incomplete("wsl_container_scan_timed_out")
            outcome.stop = True
            break
        command_result = run_wsl_command(
            distro.name,
            (runtime, *_CONTAINER_PS_ARGS_BY_RUNTIME[runtime]),
            timeout=min(timeout, remaining),
        )
        if command_result is None:
            if runtime in expected_runtimes:
                inventory_complete = False
            continue
        containers, complete = _parse_container_rows(
            command_result.stdout,
            runtime=runtime,
            distro=distro.name,
        )
        parsed_inventory_incomplete |= not complete
        runtime_succeeded |= complete
        inventory_complete &= complete
        for container in containers:
            over_capacity |= accumulator.add(container)

    outcome.scanned = runtime_succeeded and inventory_complete and not over_capacity
    if (
        not outcome.scanned
        and not over_capacity
        and (expected_runtimes or parsed_inventory_incomplete)
    ):
        outcome.mark_incomplete("wsl_container_inventory_incomplete")
    if over_capacity or (accumulator.full and has_remaining_distros):
        outcome.mark_incomplete("wsl_container_scan_capped")
    outcome.stop |= over_capacity or accumulator.full
    return outcome


def scan_wsl_containers(
    distros: Iterable[DiscoveredWSLDistro],
    *,
    timeout: float = WSL_EXEC_TIMEOUT_S,
    max_containers: int = MAX_CONTAINERS,
    checkpoint: Callable[[], None] | None = None,
) -> WSLContainerScanResult:
    """List running Docker/Podman containers in each reachable running distro."""
    result = WSLContainerScanResult()
    max_containers = max(0, min(max_containers, MAX_CONTAINERS))
    if max_containers == 0:
        result.mark_incomplete("wsl_container_scan_capacity_exhausted")
        return result

    deadline = time.monotonic() + WSL_CONTAINER_SCAN_TIME_BUDGET_S
    runnable_distros = (
        distro
        for distro in distros
        if distro.is_running and distro.name.casefold() != "docker-desktop"
    )
    distro_list = tuple(islice(runnable_distros, MAX_WSL_DISTROS + 1))
    if len(distro_list) > MAX_WSL_DISTROS:
        result.mark_incomplete("wsl_container_distro_scan_capped")
    scanned_distro_candidates = distro_list[:MAX_WSL_DISTROS]
    accumulator = _ContainerAccumulator(
        limit=max_containers,
        containers=result.containers,
    )
    for distro_index, distro in enumerate(scanned_distro_candidates):
        outcome = _scan_wsl_container_distro(
            distro,
            deadline=deadline,
            timeout=timeout,
            accumulator=accumulator,
            has_remaining_distros=(distro_index + 1 < len(scanned_distro_candidates)),
            checkpoint=checkpoint,
        )
        result.completion.merge(outcome.completion)
        if outcome.scanned:
            result.scanned_distros.append(distro.name)
        if outcome.stop:
            break
    return result
