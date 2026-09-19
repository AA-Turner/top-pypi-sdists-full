"""Bounded Docker CLI invocation and inventory discovery."""

from __future__ import annotations

import os
import platform
import signal
import shutil
import subprocess
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import IO, Callable, Generic, Literal, Protocol, TypedDict, TypeVar

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
from runlayer_cli.scan.containers.collector import FileCopyResult
from runlayer_cli.scan.container_limits import (
    SCAN_BASE_TIME_BUDGET_S,
    SCAN_MAX_TIME_BUDGET_S,
    SCAN_PER_CONTAINER_TIME_BUDGET_S,
)
from runlayer_cli.scan.file_collector import MAX_SINGLE_FILE_BYTES
from runlayer_cli.safe_parse import parse_json

SUBPROCESS_TIMEOUT_S = 10
MAX_INSPECT_BYTES = 5 * 1024 * 1024
MAX_PS_BYTES = 256 * 1024
MAX_IMAGE_LIST_BYTES = 1024 * 1024
MAX_IMAGE_INSPECT_BATCH = 64
MAX_DOCKER_CP_ARCHIVE_BYTES = MAX_SINGLE_FILE_BYTES + 64 * 1024
_READ_CHUNK_BYTES = 64 * 1024
_MAX_DOCKER_COPY_STDERR_BYTES = 8 * 1024

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


@dataclass(frozen=True)
class _RunWithSinkResult(Generic[_OUTPUT]):
    output: _OUTPUT | None = None
    returncode: int | None = None
    stderr: bytes = b""
    failure: Literal["spawn", "timeout", "wait", "drain"] | None = None


def _read_available(stream: IO[bytes], max_bytes: int) -> bytes:
    read1 = getattr(stream, "read1", None)
    if callable(read1):
        return read1(max_bytes)
    return stream.read(max_bytes)


class _BoundedBytesSink:
    def __init__(self, max_output: int) -> None:
        self.max_output = max_output
        self.output = bytearray()
        self.failed = False
        self.limit_exceeded = False

    def fail(self) -> None:
        self.failed = True

    def consume(self, stdout: IO[bytes], terminate: Callable[[], None]) -> None:
        while True:
            try:
                chunk = _read_available(stdout, _READ_CHUNK_BYTES)
            except (OSError, ValueError):
                self.failed = True
                return
            if not chunk:
                return
            if len(self.output) + len(chunk) > self.max_output:
                self.failed = True
                self.limit_exceeded = True
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
                chunk = _read_available(stdout, read_size)
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
    max_stderr: int | None = None,
) -> _RunWithSinkResult[_OUTPUT]:
    """Run one bounded subprocess lifecycle and delegate stdout consumption."""
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if max_stderr is not None else subprocess.DEVNULL,
            start_new_session=os.name != "nt",
        )
    except OSError:
        return _RunWithSinkResult(failure="spawn")

    def _terminate_producer() -> None:
        _kill_process(process)

    def _consume_stdout() -> None:
        stdout = process.stdout
        if stdout is None:
            sink.fail()
            return
        sink.consume(stdout, _terminate_producer)

    stderr_output = bytearray()

    def _consume_stderr() -> None:
        stderr = process.stderr
        if stderr is None or max_stderr is None:
            return
        while True:
            try:
                chunk = _read_available(stderr, _READ_CHUNK_BYTES)
            except (OSError, ValueError):
                return
            if not chunk:
                return
            remaining = max_stderr - len(stderr_output)
            if remaining > 0:
                stderr_output.extend(chunk[:remaining])

    reader = threading.Thread(target=_consume_stdout, daemon=True)
    reader.start()
    stderr_reader = (
        threading.Thread(target=_consume_stderr, daemon=True)
        if max_stderr is not None
        else None
    )
    if stderr_reader is not None:
        stderr_reader.start()
    failure: Literal["timeout", "wait", "drain"] | None = None
    returncode: int | None = None
    try:
        try:
            returncode = process.wait(timeout=max(timeout, 0.05))
        except subprocess.TimeoutExpired:
            failure = "timeout"
            _kill_and_reap(process)
        except OSError:
            failure = "wait"
            _kill_and_reap(process)

        streams_and_readers = [(process.stdout, reader)]
        if stderr_reader is not None:
            streams_and_readers.append((process.stderr, stderr_reader))
        for stream, stream_reader in streams_and_readers:
            stream_reader.join(timeout=1)
            if stream_reader.is_alive() and stream is not None:
                try:
                    stream.close()
                except (OSError, ValueError):
                    pass
                stream_reader.join(timeout=1)

        if failure is None and any(
            stream_reader.is_alive() for _, stream_reader in streams_and_readers
        ):
            failure = "drain"
        output = None if failure is not None else sink.finish(returncode)
        return _RunWithSinkResult(
            output=output,
            returncode=returncode,
            stderr=bytes(stderr_output),
            failure=failure,
        )
    finally:
        poll = getattr(process, "poll", None)
        if (poll() if poll is not None else process.returncode) is None:
            _kill_and_reap(process)
        # Close PIPE read-ends deterministically on every path — including the
        # happy path — instead of leaking fds until the Popen is GC'd.
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                try:
                    stream.close()
                except (OSError, ValueError):
                    pass


def _run_bytes(
    cmd: list[str],
    *,
    timeout: float,
    max_output: int,
) -> bytes | None:
    """Run a command with hard time/output caps, returning stdout on success."""
    result = _run_with_sink(
        cmd,
        timeout=timeout,
        sink=_BoundedBytesSink(max_output),
    )
    return result.output


def _run_file_copy(
    cmd: list[str],
    *,
    timeout: float,
    max_output: int,
) -> FileCopyResult:
    """Run ``docker cp`` with bounded output and classify definite absence."""
    sink = _BoundedBytesSink(max_output)
    result = _run_with_sink(
        cmd,
        timeout=timeout,
        sink=sink,
        max_stderr=_MAX_DOCKER_COPY_STDERR_BYTES,
    )
    if result.failure == "spawn":
        return FileCopyResult(
            status="failed",
            failure_reason="container_artifact_copy_spawn_failed",
        )
    if result.failure == "timeout":
        return FileCopyResult(
            status="failed",
            failure_reason="container_artifact_copy_timed_out",
        )
    if sink.limit_exceeded:
        return FileCopyResult(
            status="failed",
            failure_reason="container_artifact_copy_limit_exceeded",
        )
    if result.failure is not None or result.returncode is None:
        return FileCopyResult(
            status="failed",
            failure_reason="container_artifact_copy_wait_failed",
        )
    if result.returncode == 0 and result.output is not None:
        return FileCopyResult(status="success", archive=result.output)
    if result.returncode == 0:
        return FileCopyResult(
            status="failed",
            failure_reason="container_artifact_copy_wait_failed",
        )

    absent = _docker_copy_path_absent(result.stderr)
    return FileCopyResult(
        status="absent" if absent else "failed",
        failure_reason=(None if absent else "container_artifact_copy_nonzero"),
    )


def _docker_copy_path_absent(stderr: bytes) -> bool:
    message = stderr.decode("utf-8", errors="replace").casefold()
    return any(
        not any(
            marker in line
            for marker in ("dial unix ", "dial tcp ", "connect:", "connection refused")
        )
        and (
            "could not find the file" in line
            or (
                any(marker in line for marker in ("lstat ", "stat ", "failed to copy "))
                and any(
                    phrase in line
                    for phrase in ("no such file or directory", "does not exist")
                )
            )
        )
        for line in message.splitlines()
    )


def _run_bounded_utf8_lines(
    cmd: list[str],
    *,
    timeout: float,
    max_output: int,
    max_lines: int,
) -> _BoundedLineOutput | None:
    """Return complete UTF-8 lines, terminating the producer at either cap."""
    result = _run_with_sink(
        cmd,
        timeout=timeout,
        sink=_BoundedUtf8LineSink(
            max_output=max_output,
            max_lines=max_lines,
        ),
    )
    return result.output


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
        killed_group = False
        if os.name != "nt":
            try:
                os.killpg(process.pid, signal.SIGKILL)
                killed_group = True
            except (AttributeError, OSError):
                pass
        if not killed_group:
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


# ``ps --filter status=`` vocabularies differ per runtime, and podman/nerdctl
# reject values they do not know (the whole ``ps`` exits nonzero, so discovery
# for that runtime silently returns nothing). Each runtime gets only the
# statuses it documents; Docker's is the default for unknown runtimes since
# every other supported CLI advertises Docker compatibility.
_RUNNING_STATUS_FILTERS: dict[str, tuple[str, ...]] = {
    "docker": ("running", "paused", "restarting"),
    "podman": ("running", "paused"),
    "nerdctl": ("running", "paused", "pausing"),
}
_STOPPED_STATUS_FILTERS: dict[str, tuple[str, ...]] = {
    "docker": ("created", "exited", "dead", "removing"),
    "podman": ("created", "exited", "stopped"),
    "nerdctl": ("created", "stopped"),
}


def _status_filter_args(statuses: tuple[str, ...]) -> list[str]:
    args: list[str] = []
    for status in statuses:
        args.extend(("--filter", f"status={status}"))
    return args


def _discover_container_ids(
    *,
    docker: str,
    deadline: float,
    subprocess_timeout: float,
    runtime: str = "docker",
) -> DockerPSInventory | None:
    """List running container IDs and inventory quality metadata."""
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    statuses = _RUNNING_STATUS_FILTERS.get(runtime, _RUNNING_STATUS_FILTERS["docker"])
    output = _run_text(
        [
            docker,
            "ps",
            "--last",
            str(MAX_CONTAINERS + 1),
            "--no-trunc",
            *_status_filter_args(statuses),
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
    runtime: str = "docker",
) -> DockerPSInventory | None:
    """List bounded non-running container IDs."""
    timeout = _remaining_timeout(deadline, subprocess_timeout)
    if timeout is None:
        return None
    statuses = _STOPPED_STATUS_FILTERS.get(runtime, _STOPPED_STATUS_FILTERS["docker"])
    command = [
        docker,
        "ps",
        "-a",
        "--last",
        str(MAX_CONTAINERS + 1),
        "--no-trunc",
        *_status_filter_args(statuses),
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
    """Inspect a discovered container inventory.

    One batched ``inspect`` first. It exits nonzero when any ID vanished
    between ``ps`` and ``inspect`` (and the fail-closed parse rejects a batch
    where one container changed state), which used to discard every surviving
    container's artifacts. On batch failure fall back to one ``inspect`` per
    ID so survivors are still collected; the caller compares the returned set
    against the discovered IDs and withholds inventory authority when short.
    """
    containers = _inspect_batch(
        docker=docker,
        container_ids=container_ids,
        deadline=deadline,
        subprocess_timeout=subprocess_timeout,
        host_home=host_home,
        running=running,
    )
    if containers is None and len(container_ids) > 1:
        logger.warning(
            "Batched container inspect failed; inspecting per container",
            container_count=len(container_ids),
        )
        containers = _inspect_each(
            docker=docker,
            container_ids=container_ids,
            deadline=deadline,
            subprocess_timeout=subprocess_timeout,
            host_home=host_home,
            running=running,
        )
    return containers


def _inspect_batch(
    *,
    docker: str,
    container_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
    running: bool,
) -> list[DiscoveredContainer] | None:
    """Inspect ``container_ids`` in one call; None unless every ID parsed."""
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

    outcome = parse_json(output)
    if outcome["error"] is not None:
        return None
    rows = outcome["value"]
    if not isinstance(rows, list) or not rows:
        return None

    return parse_complete_inspect_inventory(
        rows,
        container_ids=container_ids,
        host_home=host_home,
        running=running,
    )


def _inspect_each(
    *,
    docker: str,
    container_ids: list[str],
    deadline: float,
    subprocess_timeout: float,
    host_home: Path,
    running: bool,
) -> list[DiscoveredContainer] | None:
    """Inspect each ID on its own, keeping the ones that still resolve.

    Returns None only when nothing resolved, so a fully vanished inventory
    reads the same as a failed inspect to the caller.
    """
    containers: list[DiscoveredContainer] = []
    for container_id in container_ids:
        if _remaining_timeout(deadline, subprocess_timeout) is None:
            break
        parsed = _inspect_batch(
            docker=docker,
            container_ids=[container_id],
            deadline=deadline,
            subprocess_timeout=subprocess_timeout,
            host_home=host_home,
            running=running,
        )
        if parsed is not None:
            containers.extend(parsed)
    return containers or None


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
