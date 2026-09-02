"""Bounded Docker CLI invocation and inventory discovery."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import threading
import time
from collections.abc import Iterator
from pathlib import Path, PureWindowsPath
from typing import IO, Callable, Protocol, TypedDict, TypeVar

import structlog

from runlayer_cli.scan.containers.inspect_parse import (
    MAX_CONTAINER_IMAGES,
    MAX_CONTAINERS,
    MAX_IMAGE_CONFIG_METADATA_CHARS,
    ContainerImageInventory,
    DiscoveredContainer,
    DockerPSInventory,
    ImageConfigMetadata,
    _parse_docker_ps_inventory,
    bound_image_inventory_metadata,
    parse_complete_inspect_inventory,
    parse_docker_image_ls,
    parse_image_config_metadata,
    parse_image_digests,
)
from runlayer_cli.scan.file_collector import MAX_SINGLE_FILE_BYTES

SUBPROCESS_TIMEOUT_S = 10
SCAN_BASE_TIME_BUDGET_S = 30
SCAN_PER_CONTAINER_TIME_BUDGET_S = 10
SCAN_MAX_TIME_BUDGET_S = 300
MAX_INSPECT_BYTES = 5 * 1024 * 1024
MAX_PS_BYTES = 256 * 1024
MAX_IMAGE_LIST_BYTES = 1024 * 1024
MAX_IMAGE_INSPECT_BATCH = 64
MAX_DOCKER_CP_ARCHIVE_BYTES = MAX_SINGLE_FILE_BYTES + 64 * 1024
_READ_CHUNK_BYTES = 64 * 1024

logger = structlog.get_logger(__name__)

_OUTPUT = TypeVar("_OUTPUT", covariant=True)


class _BoundedLineOutput(TypedDict):
    text: str
    truncation_reason: str | None


class _OutputSink(Protocol[_OUTPUT]):
    def fail(self) -> None: ...

    def consume(
        self,
        stdout: IO[bytes],
        terminate: Callable[[], None],
    ) -> None: ...

    def finish(self, returncode: int | None) -> _OUTPUT | None: ...


class _BoundedBytesSink:
    def __init__(self, max_output: int) -> None:
        self.max_output = max_output
        self.output = bytearray()
        self.failed = False

    def fail(self) -> None:
        self.failed = True

    def consume(self, stdout: IO[bytes], terminate: Callable[[], None]) -> None:
        while True:
            try:
                chunk = stdout.read(_READ_CHUNK_BYTES)
            except (OSError, ValueError):
                self.failed = True
                return
            if not chunk:
                return
            if len(self.output) + len(chunk) > self.max_output:
                self.failed = True
                terminate()
                return
            self.output.extend(chunk)

    def finish(self, returncode: int | None) -> bytes | None:
        if self.failed or returncode != 0:
            return None
        return bytes(self.output)


class _BoundedUtf8LineSink:
    def __init__(self, *, max_output: int, max_lines: int) -> None:
        self.max_output = max_output
        self.max_lines = max_lines
        self.lines: list[str] = []
        self.pending = bytearray()
        self.bytes_read = 0
        self.truncation_reason: str | None = None
        self.failed = False

    def fail(self) -> None:
        self.failed = True

    def _truncate(self, reason: str, terminate: Callable[[], None]) -> None:
        if self.truncation_reason is None:
            self.truncation_reason = reason
        terminate()

    def consume(self, stdout: IO[bytes], terminate: Callable[[], None]) -> None:
        while True:
            if len(self.lines) >= self.max_lines:
                self._truncate("max_images", terminate)
                return
            if self.bytes_read >= self.max_output:
                self._truncate("max_bytes", terminate)
                return

            read_size = min(_READ_CHUNK_BYTES, self.max_output - self.bytes_read)
            try:
                chunk = stdout.read(read_size)
            except (OSError, ValueError):
                self.failed = True
                return
            if not chunk:
                if self.pending:
                    self.truncation_reason = "incomplete_line"
                return

            self.bytes_read += len(chunk)
            self.pending.extend(chunk)
            while True:
                newline_index = self.pending.find(b"\n")
                if newline_index < 0:
                    break
                raw_line = bytes(self.pending[: newline_index + 1])
                del self.pending[: newline_index + 1]
                try:
                    self.lines.append(raw_line.decode("utf-8"))
                except UnicodeDecodeError:
                    self.failed = True
                    terminate()
                    return
                if len(self.lines) >= self.max_lines:
                    self._truncate("max_images", terminate)
                    return

    def finish(self, returncode: int | None) -> _BoundedLineOutput | None:
        terminated_for_cap = self.truncation_reason in {"max_bytes", "max_images"}
        if self.failed or (returncode != 0 and not terminated_for_cap):
            return None
        return {
            "text": "".join(self.lines),
            "truncation_reason": self.truncation_reason,
        }


def _run_with_sink(
    cmd: list[str],
    *,
    timeout: float,
    sink: _OutputSink[_OUTPUT],
) -> _OUTPUT | None:
    """Run one bounded subprocess lifecycle and delegate stdout consumption."""
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None

    def _terminate_producer() -> None:
        try:
            process.kill()
        except OSError:
            pass

    def _consume_stdout() -> None:
        stdout = process.stdout
        if stdout is None:
            sink.fail()
            return
        sink.consume(stdout, _terminate_producer)

    reader = threading.Thread(target=_consume_stdout, daemon=True)
    reader.start()
    wait_failed = False
    try:
        try:
            process.wait(timeout=max(timeout, 0.05))
        except subprocess.TimeoutExpired:
            wait_failed = True
            _kill_and_reap(process)
        except OSError:
            wait_failed = True
            _kill_and_reap(process)

        reader.join(timeout=1)
        if reader.is_alive() and process.stdout is not None:
            try:
                process.stdout.close()
            except (OSError, ValueError):
                pass
            reader.join(timeout=1)

        if wait_failed or reader.is_alive():
            return None
        return sink.finish(process.returncode)
    finally:
        # Close the PIPE read-end deterministically on every path — including
        # the happy path — instead of leaking the fd until the Popen is GC'd.
        if process.stdout is not None:
            try:
                process.stdout.close()
            except (OSError, ValueError):
                pass


def _run_bytes(
    cmd: list[str],
    *,
    timeout: float,
    max_output: int,
) -> bytes | None:
    """Run a command with hard time/output caps, returning stdout on success."""
    return _run_with_sink(
        cmd,
        timeout=timeout,
        sink=_BoundedBytesSink(max_output),
    )


def _run_bounded_utf8_lines(
    cmd: list[str],
    *,
    timeout: float,
    max_output: int,
    max_lines: int,
) -> _BoundedLineOutput | None:
    """Return complete UTF-8 lines, terminating the producer at either cap."""
    return _run_with_sink(
        cmd,
        timeout=timeout,
        sink=_BoundedUtf8LineSink(
            max_output=max_output,
            max_lines=max_lines,
        ),
    )


def _run_text(
    cmd: list[str],
    *,
    timeout: float,
    max_output: int,
) -> str | None:
    output = _run_bytes(cmd, timeout=timeout, max_output=max_output)
    if output is None:
        return None
    try:
        return output.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _kill_process(process: subprocess.Popen[bytes]) -> None:
    try:
        if process.poll() is None:
            process.kill()
    except OSError:
        pass


def _kill_and_reap(process: subprocess.Popen[bytes]) -> None:
    _kill_process(process)
    try:
        process.wait()
    except OSError:
        pass


def _remaining_timeout(deadline: float, subprocess_timeout: float) -> float | None:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return None
    return min(subprocess_timeout, remaining)


def _inspect_image_batches(
    *,
    docker: str,
    image_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
) -> Iterator[str]:
    """Keep one oversized image set from suppressing every inspect result."""
    for offset in range(0, len(image_ids), MAX_IMAGE_INSPECT_BATCH):
        timeout = _remaining_timeout(deadline, subprocess_timeout)
        if timeout is None:
            break
        output = _run_text(
            [
                docker,
                "image",
                "inspect",
                *image_ids[offset : offset + MAX_IMAGE_INSPECT_BATCH],
            ],
            timeout=timeout,
            max_output=MAX_INSPECT_BYTES,
        )
        if output is not None:
            yield output


def _scaled_scan_time_budget(container_count: int) -> float:
    """Return the bounded default budget after inventory size is known."""
    return min(
        SCAN_MAX_TIME_BUDGET_S,
        SCAN_BASE_TIME_BUDGET_S
        + max(container_count, 0) * SCAN_PER_CONTAINER_TIME_BUDGET_S,
    )


def _find_container_cli(binary: str) -> str | None:
    """Resolve a docker-CLI-compatible binary (podman/nerdctl) from PATH.

    Falls back to the common Homebrew install prefixes on macOS, where
    launchd's minimal default PATH omits them.
    """
    resolved = shutil.which(binary)
    if resolved is not None:
        return resolved
    if platform.system() == "Darwin":
        for candidate in (
            Path("/usr/local/bin") / binary,
            Path("/opt/homebrew/bin") / binary,
        ):
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)
    return None


def _find_docker_cli() -> str | None:
    """Resolve Docker even under launchd's minimal default PATH."""
    docker = shutil.which("docker")
    system = platform.system()
    candidates: tuple[Path, ...] = ()
    if docker is None and system == "Darwin":
        candidates = (
            Path("/usr/local/bin/docker"),
            Path("/opt/homebrew/bin/docker"),
            Path.home() / ".docker/bin/docker",
            Path("/Applications/Docker.app/Contents/Resources/bin/docker"),
        )
    elif docker is None and system == "Windows":
        windows_paths: list[PureWindowsPath] = []
        for variable in ("ProgramFiles", "ProgramW6432"):
            root = os.environ.get(variable)
            if root:
                windows_paths.append(
                    PureWindowsPath(root)
                    / "Docker"
                    / "Docker"
                    / "resources"
                    / "bin"
                    / "docker.exe"
                )
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            windows_paths.append(
                PureWindowsPath(local_app_data)
                / "Docker"
                / "resources"
                / "bin"
                / "docker.exe"
            )
        candidates = tuple(Path(str(path)) for path in windows_paths)

    if docker is None:
        for candidate in candidates:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                docker = str(candidate)
                break
    return docker


def _discover_container_ids(
    *,
    docker: str,
    deadline: float,
    subprocess_timeout: float,
) -> DockerPSInventory | None:
    """List running container IDs and inventory quality metadata."""
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    output = _run_text(
        [
            docker,
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
        ],
        timeout=timeout,
        max_output=MAX_PS_BYTES,
    )
    if output is None:
        return None

    inventory = _parse_docker_ps_inventory(output)
    if inventory["truncated"]:
        logger.warning(
            "Container inventory truncated",
            max_containers=MAX_CONTAINERS,
        )
    return inventory


def _discover_stopped_container_ids(
    *,
    docker: str,
    deadline: float,
    subprocess_timeout: float,
) -> DockerPSInventory | None:
    """List bounded non-running container IDs."""
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    command = [
        docker,
        "ps",
        "-a",
        "--last",
        str(MAX_CONTAINERS + 1),
        "--no-trunc",
        "--filter",
        "status=created",
        "--filter",
        "status=exited",
        "--filter",
        "status=dead",
        "--filter",
        "status=removing",
        "--format",
        "{{json .}}",
    ]
    output = _run_text(command, timeout=timeout, max_output=MAX_PS_BYTES)
    if output is None:
        return None
    return _parse_docker_ps_inventory(output)


def _inspect_inventory(
    *,
    docker: str,
    container_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
    running: bool,
) -> list[DiscoveredContainer] | None:
    """Inspect and fail-closed validate a discovered container inventory."""
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    output = _run_text(
        [docker, "inspect", *container_ids],
        timeout=timeout,
        max_output=MAX_INSPECT_BYTES,
    )
    if output is None:
        return None

    try:
        rows = json.loads(output)
    except (TypeError, ValueError):
        return None
    if not isinstance(rows, list) or not rows:
        return None

    return parse_complete_inspect_inventory(
        rows,
        container_ids=container_ids,
        host_home=host_home,
        running=running,
    )


def _inspect_containers(
    *,
    docker: str,
    container_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
) -> list[DiscoveredContainer] | None:
    """Inspect and validate the discovered container inventory."""
    return _inspect_inventory(
        docker=docker,
        container_ids=container_ids,
        deadline=deadline,
        subprocess_timeout=subprocess_timeout,
        host_home=host_home,
        running=True,
    )


def _inspect_stopped_containers(
    *,
    docker: str,
    container_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
) -> list[DiscoveredContainer] | None:
    """Inspect a complete stopped-container inventory."""
    return _inspect_inventory(
        docker=docker,
        container_ids=container_ids,
        deadline=deadline,
        subprocess_timeout=subprocess_timeout,
        host_home=host_home,
        running=False,
    )


def _list_container_images(
    *,
    docker: str,
    deadline: float,
    subprocess_timeout: float,
) -> ContainerImageInventory | None:
    """List bounded tagged and digest-addressed local Docker images.

    Truncation (byte cap, line cap, or the parser's image cap) is reported to
    the caller so a partial list is never treated as an authoritative snapshot.
    """
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    result = _run_bounded_utf8_lines(
        [
            docker,
            "image",
            "ls",
            "--no-trunc",
            "--digests",
            "--format",
            "{{json .}}",
        ],
        timeout=timeout,
        max_output=MAX_IMAGE_LIST_BYTES,
        max_lines=MAX_CONTAINER_IMAGES,
    )
    if result is None:
        return None
    if result["truncation_reason"] is not None:
        logger.warning(
            "Container image inventory truncated",
            max_bytes=MAX_IMAGE_LIST_BYTES,
            max_images=MAX_CONTAINER_IMAGES,
            reason=result["truncation_reason"],
        )
    inventory = parse_docker_image_ls(result["text"])
    if inventory is None:
        return None
    if result["truncation_reason"] is not None:
        inventory["truncated"] = True
    image_ids = sorted(
        {image.image_id for image in inventory["images"] if image.image_id is not None}
    )
    if image_ids:
        metadata: dict[str, ImageConfigMetadata] = {}
        remaining_metadata_chars = MAX_IMAGE_CONFIG_METADATA_CHARS
        for output in _inspect_image_batches(
            docker=docker,
            image_ids=image_ids,
            deadline=deadline,
            subprocess_timeout=subprocess_timeout,
        ):
            batch_metadata = parse_image_config_metadata(
                output,
                max_metadata_chars=remaining_metadata_chars,
            )
            metadata.update(batch_metadata)
            remaining_metadata_chars -= sum(
                sum(
                    len(key) + len(value)
                    for key, value in item.get("labels", {}).items()
                )
                + sum(len(value) for value in item.get("entrypoint", ()))
                for item in batch_metadata.values()
            )
        for image in inventory["images"]:
            image_metadata = metadata.get(image.image_id or "")
            if image_metadata is not None:
                if "labels" in image_metadata:
                    image.labels = image_metadata["labels"]
                    image.labels_collected = True
                if "entrypoint" in image_metadata:
                    image.entrypoint = image_metadata["entrypoint"]
                    image.entrypoint_collected = True
        bound_image_inventory_metadata(inventory["images"])
    return inventory


def _collect_image_digests(
    *,
    docker: str,
    containers: list[DiscoveredContainer],
    deadline: float,
    subprocess_timeout: float,
) -> list[DiscoveredContainer]:
    """Best-effort enrich inspected containers with repository digests."""
    image_ids = sorted(
        {
            container.image_id
            for container in containers
            if isinstance(container.image_id, str) and container.image_id
        }
    )
    if not image_ids:
        return containers

    image_digests: dict[str, str] = {}
    for output in _inspect_image_batches(
        docker=docker,
        image_ids=image_ids,
        deadline=deadline,
        subprocess_timeout=subprocess_timeout,
    ):
        image_digests.update(parse_image_digests(output))
    for container in containers:
        digest = image_digests.get(container.image_id or "")
        if digest is not None:
            container.image_digest = digest[:140]
    return containers
