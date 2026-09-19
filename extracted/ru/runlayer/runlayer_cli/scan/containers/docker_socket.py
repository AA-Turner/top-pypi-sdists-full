"""Bounded Docker Engine API access over local Unix and Windows transports."""

from __future__ import annotations

import http.client
import io
import json
import os
import platform
import socket
import stat
import time
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Callable, cast
from urllib.parse import quote, urlencode

from runlayer_cli.scan.containers.docker_cli import (
    MAX_DOCKER_CP_ARCHIVE_BYTES,
    MAX_IMAGE_LIST_BYTES,
    MAX_INSPECT_BYTES,
    _docker_copy_path_absent,
)
from runlayer_cli.scan.containers.inspect_parse import (
    MAX_CONTAINERS,
    MAX_IMAGE_CONFIG_METADATA_CHARS,
    ContainerImageInventory,
    DiscoveredContainer,
    DockerPSInventory,
    _parse_docker_engine_inventory,
    bound_image_inventory_metadata,
    parse_complete_inspect_inventory,
    parse_docker_engine_images,
    parse_image_config_metadata,
    parse_image_digests,
)
from runlayer_cli.scan.containers.tar_walk import (
    MAX_DOCKER_TREE_MATCHED_FILES,
    MAX_DOCKER_TREE_STREAM_BYTES,
    _TarWalkResult,
    _walk_tar_stream,
)
from runlayer_cli.scan.containers.windows_named_pipe import (
    _WindowsNamedPipeHTTPConnection,
    _windows_named_pipe_available,
)
from runlayer_cli.scan.containers.collector import FileCopyResult
from runlayer_cli.safe_parse import parse_json

DOCKER_SOCKET_PATH = "/var/run/docker.sock"
WINDOWS_DOCKER_PIPE = r"\\.\pipe\docker_engine"
_READ_CHUNK_BYTES = 64 * 1024
_MAX_ENGINE_ERROR_BYTES = 8 * 1024

# Engine API ``/containers/json`` summaries are far fatter than
# ``docker ps --format`` lines (they embed Mounts, NetworkSettings, and Ports),
# so the running-inventory read gets its own ceiling rather than the CLI's
# ``MAX_PS_BYTES``. Paired with the ``limit`` query param below, the payload
# stays bounded to a small multiple of ``MAX_CONTAINERS`` fat rows even on busy
# Portainer hosts.
MAX_ENGINE_INVENTORY_BYTES = 1024 * 1024

# ``limit`` on its own returns the newest containers *including non-running*
# ones, so the state filter mirrors ``docker ps``. Restarting containers remain
# part of the authoritative running inventory even though Engine inspect reports
# ``State.Running=false`` while it is between restart attempts.
_RUNNING_INVENTORY_STATUSES = ("running", "paused", "restarting")
_STOPPED_INVENTORY_STATUSES = (
    "created",
    "removing",
    "exited",
    "dead",
)


class _UnixHTTPConnection(http.client.HTTPConnection):
    """HTTP connection whose transport is an ``AF_UNIX`` socket."""

    def __init__(self, socket_path: str, *, timeout: float) -> None:
        super().__init__("localhost", timeout=timeout)
        self._socket_path = socket_path

    def connect(self) -> None:
        unix_family = getattr(socket, "AF_UNIX", None)
        if unix_family is None:
            raise OSError("Unix sockets are unavailable")

        sock = socket.socket(unix_family, socket.SOCK_STREAM)
        try:
            sock.settimeout(self.timeout)
            sock.connect(self._socket_path)
        except BaseException:
            sock.close()
            raise
        self.sock = sock


def _http_connection_for_endpoint(
    endpoint: str,
    *,
    timeout: float,
    deadline: float,
) -> http.client.HTTPConnection:
    if endpoint.casefold().startswith("\\\\.\\pipe\\"):
        return _WindowsNamedPipeHTTPConnection(
            endpoint,
            timeout=timeout,
            deadline=deadline,
        )
    return _UnixHTTPConnection(endpoint, timeout=timeout)


@dataclass
class _OpenResponse:
    connection: http.client.HTTPConnection
    response: http.client.HTTPResponse

    def close(self) -> None:
        try:
            self.response.close()
        finally:
            self.connection.close()


@dataclass
class _OpenGetResult:
    opened: _OpenResponse | None
    status: int | None
    error_body: bytes | None = None


class _DeadlineResponseStream(io.RawIOBase):
    """Refresh the socket timeout before each streaming response read."""

    def __init__(
        self,
        client: DockerSocketClient,
        opened: _OpenResponse,
        *,
        deadline: float,
    ) -> None:
        self._client = client
        self._opened = opened
        self._deadline = deadline

    def readable(self) -> bool:
        return True

    def read(self, size: int = -1) -> bytes:
        self._client._refresh_timeout(self._opened, deadline=self._deadline)
        chunk = self._opened.response.read(size)
        if not isinstance(chunk, bytes):
            raise OSError
        return chunk


def find_docker_socket() -> str | None:
    """Return a reachable local Docker Engine endpoint."""
    system = platform.system()
    if system == "Windows":
        if _windows_named_pipe_available(WINDOWS_DOCKER_PIPE):
            return WINDOWS_DOCKER_PIPE
        return None
    if system != "Linux" or not hasattr(socket, "AF_UNIX"):
        return None
    try:
        socket_stat = os.stat(DOCKER_SOCKET_PATH)
    except OSError:
        return None
    required_access = os.R_OK | os.W_OK
    if not stat.S_ISSOCK(socket_stat.st_mode) or not os.access(
        DOCKER_SOCKET_PATH, required_access
    ):
        return None
    return DOCKER_SOCKET_PATH


class DockerSocketClient:
    """Minimal Engine API client sharing the CLI collector's safety bounds."""

    def __init__(self, socket_path: str, *, request_timeout: float) -> None:
        self._socket_path = socket_path
        self._request_timeout = request_timeout

    def _next_timeout(self, deadline: float) -> float | None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None
        return max(min(self._request_timeout, remaining), 0.05)

    def _request_deadline(self, deadline: float) -> float:
        """Cap one request to ``request_timeout`` total wall-clock.

        Mirrors the CLI transport, where ``subprocess_timeout`` bounds an entire
        ``docker`` invocation. Refreshing the per-read socket timeout alone lets a
        slow-drip Engine API response ride the whole scan deadline, so the request
        deadline is the earlier of the scan deadline and now + ``request_timeout``.
        """
        return min(deadline, time.monotonic() + self._request_timeout)

    def _open_get(self, path: str, *, deadline: float) -> _OpenResponse | None:
        return self._open_get_with_status(path, deadline=deadline).opened

    def _open_get_with_status(
        self,
        path: str,
        *,
        deadline: float,
    ) -> _OpenGetResult:
        timeout = self._next_timeout(deadline)
        if timeout is None:
            return _OpenGetResult(opened=None, status=None)
        connection = _http_connection_for_endpoint(
            self._socket_path,
            timeout=timeout,
            deadline=deadline,
        )
        try:
            connection.request("GET", path)
            response = connection.getresponse()
        except (OSError, ValueError, http.client.HTTPException):
            connection.close()
            return _OpenGetResult(opened=None, status=None)
        opened = _OpenResponse(connection=connection, response=response)
        if response.status == http.client.OK:
            return _OpenGetResult(opened=opened, status=response.status)

        error_body = None
        try:
            if response.status == http.client.NOT_FOUND:
                error_body = self._read_error_body(opened, deadline=deadline)
        finally:
            opened.close()
        return _OpenGetResult(
            opened=None,
            status=response.status,
            error_body=error_body,
        )

    def _refresh_timeout(self, opened: _OpenResponse, *, deadline: float) -> None:
        timeout = self._next_timeout(deadline)
        if timeout is None:
            raise TimeoutError
        if opened.connection.sock is not None:
            set_deadline = getattr(opened.connection.sock, "set_deadline", None)
            if callable(set_deadline):
                set_deadline(deadline)
            opened.connection.sock.settimeout(timeout)

    def _read_error_body(
        self,
        opened: _OpenResponse,
        *,
        deadline: float,
    ) -> bytes | None:
        output = bytearray()
        try:
            while True:
                self._refresh_timeout(opened, deadline=deadline)
                read_size = min(
                    _READ_CHUNK_BYTES,
                    _MAX_ENGINE_ERROR_BYTES - len(output) + 1,
                )
                chunk = opened.response.read(read_size)
                if not isinstance(chunk, bytes):
                    return None
                if not chunk:
                    return bytes(output)
                output.extend(chunk)
                if len(output) > _MAX_ENGINE_ERROR_BYTES:
                    return None
        except (OSError, ValueError, http.client.HTTPException):
            return None

    def _get(self, path: str, *, deadline: float, max_bytes: int) -> bytes | None:
        request_deadline = self._request_deadline(deadline)
        opened = self._open_get(path, deadline=request_deadline)
        if opened is None:
            return None

        output = bytearray()
        try:
            while True:
                self._refresh_timeout(opened, deadline=request_deadline)
                read_size = min(_READ_CHUNK_BYTES, max_bytes - len(output) + 1)
                chunk = opened.response.read(read_size)
                if not isinstance(chunk, bytes):
                    return None
                if not chunk:
                    return bytes(output)
                output.extend(chunk)
                if len(output) > max_bytes:
                    return None
        except (OSError, http.client.HTTPException):
            return None
        finally:
            opened.close()

    @staticmethod
    def _decode(output: bytes) -> str | None:
        try:
            return output.decode("utf-8")
        except UnicodeDecodeError:
            return None

    @staticmethod
    def _resource_path(resource: str, identifier: str) -> str:
        return f"/{resource}/{quote(identifier, safe='')}/json"

    @staticmethod
    def _archive_path(container_id: str, path: str) -> str:
        query = urlencode({"path": path})
        return f"/containers/{quote(container_id, safe='')}/archive?{query}"

    @staticmethod
    def _archive_path_absent(error_body: bytes | None) -> bool:
        if error_body is None:
            return False
        text = DockerSocketClient._decode(error_body)
        if text is None:
            return False
        outcome = parse_json(text)
        if outcome["error"] is not None:
            return False
        error = outcome["value"]
        if not isinstance(error, dict):
            return False
        message = error.get("message")
        if not isinstance(message, str):
            return False
        return _docker_copy_path_absent(message.encode())

    @staticmethod
    def _inventory_path() -> str:
        # ``limit`` bounds the rows the daemon serializes so a busy host's full
        # inventory never has to be downloaded (and busted against the cap)
        # before the parser truncates it. ``+1`` lets the parser still flag a
        # truncated inventory when more than ``MAX_CONTAINERS`` are running.
        query = urlencode(
            {
                "limit": MAX_CONTAINERS + 1,
                "filters": json.dumps(
                    {"status": list(_RUNNING_INVENTORY_STATUSES)},
                    separators=(",", ":"),
                ),
            }
        )
        return f"/containers/json?{query}"

    @staticmethod
    def _stopped_inventory_path() -> str:
        query = urlencode(
            {
                "all": "true",
                "limit": MAX_CONTAINERS + 1,
                "filters": json.dumps(
                    {"status": list(_STOPPED_INVENTORY_STATUSES)},
                    separators=(",", ":"),
                ),
            }
        )
        return f"/containers/json?{query}"

    def discover_container_ids(self, *, deadline: float) -> DockerPSInventory | None:
        output = self._get(
            self._inventory_path(),
            deadline=deadline,
            max_bytes=MAX_ENGINE_INVENTORY_BYTES,
        )
        if output is None:
            return None
        text = self._decode(output)
        if text is None:
            return None
        return _parse_docker_engine_inventory(text)

    def _fetch_inspect_rows(
        self,
        *,
        container_ids: list[str],
        deadline: float,
    ) -> list[object] | None:
        """Fetch one inspect row per container within an aggregate byte cap."""
        rows: list[object] = []
        remaining_bytes = MAX_INSPECT_BYTES
        for container_id in container_ids:
            if remaining_bytes <= 0:
                return None
            output = self._get(
                self._resource_path("containers", container_id),
                deadline=deadline,
                max_bytes=remaining_bytes,
            )
            if output is None or len(output) > remaining_bytes:
                return None
            remaining_bytes -= len(output)
            text = self._decode(output)
            if text is None:
                return None
            outcome = parse_json(text)
            if outcome["error"] is not None:
                return None
            row = outcome["value"]
            if not isinstance(row, dict):
                return None
            rows.append(row)
        return rows

    def inspect_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        rows = self._fetch_inspect_rows(
            container_ids=container_ids,
            deadline=deadline,
        )
        if rows is None:
            return None
        return parse_complete_inspect_inventory(
            rows,
            container_ids=container_ids,
            host_home=host_home,
            running=True,
        )

    def discover_stopped_container_ids(
        self, *, deadline: float
    ) -> DockerPSInventory | None:
        output = self._get(
            self._stopped_inventory_path(),
            deadline=deadline,
            max_bytes=MAX_ENGINE_INVENTORY_BYTES,
        )
        if output is None:
            return None
        text = self._decode(output)
        if text is None:
            return None
        return _parse_docker_engine_inventory(text)

    def inspect_stopped_containers(
        self,
        *,
        container_ids: list[str],
        deadline: float,
        host_home: Path,
    ) -> list[DiscoveredContainer] | None:
        rows = self._fetch_inspect_rows(
            container_ids=container_ids,
            deadline=deadline,
        )
        if rows is None:
            return None
        return parse_complete_inspect_inventory(
            rows,
            container_ids=container_ids,
            host_home=host_home,
            running=False,
        )

    def list_container_images(
        self, *, deadline: float
    ) -> ContainerImageInventory | None:
        query = urlencode({"all": "false", "digests": "true"})
        output = self._get(
            f"/images/json?{query}",
            deadline=deadline,
            max_bytes=MAX_IMAGE_LIST_BYTES,
        )
        if output is None:
            return None
        text = self._decode(output)
        if text is None:
            return None
        inventory = parse_docker_engine_images(text)
        if inventory is None:
            return None

        remaining_raw_bytes = MAX_INSPECT_BYTES
        remaining_metadata_chars = MAX_IMAGE_CONFIG_METADATA_CHARS
        metadata = {}
        image_ids = tuple(
            dict.fromkeys(
                image.image_id
                for image in inventory["images"]
                if image.image_id is not None
            )
        )
        for image_id in image_ids:
            if remaining_raw_bytes <= 0 or time.monotonic() >= deadline:
                break
            config_output = self._get(
                self._resource_path("images", image_id),
                deadline=deadline,
                max_bytes=remaining_raw_bytes,
            )
            # One failed/oversized inspect must not suppress the remaining
            # images' enrichment (mirrors the CLI's per-batch skip).
            if config_output is None or len(config_output) > remaining_raw_bytes:
                continue
            remaining_raw_bytes -= len(config_output)
            config_text = self._decode(config_output)
            if config_text is None:
                continue
            parsed = parse_image_config_metadata(
                config_text,
                max_metadata_chars=remaining_metadata_chars,
            )
            metadata.update(parsed)
            remaining_metadata_chars -= sum(
                sum(
                    len(key) + len(value)
                    for key, value in item.get("labels", {}).items()
                )
                + sum(len(value) for value in item.get("entrypoint", ()))
                for item in parsed.values()
            )

        for image in inventory["images"]:
            image_metadata = metadata.get(image.image_id or "")
            if image_metadata is None:
                continue
            if "labels" in image_metadata:
                image.labels = image_metadata["labels"]
                image.labels_collected = True
            if "entrypoint" in image_metadata:
                image.entrypoint = image_metadata["entrypoint"]
                image.entrypoint_collected = True
        bound_image_inventory_metadata(inventory["images"])
        return inventory

    def collect_image_digests(
        self,
        *,
        containers: list[DiscoveredContainer],
        deadline: float,
    ) -> list[DiscoveredContainer]:
        image_ids = sorted(
            {
                container.image_id
                for container in containers
                if isinstance(container.image_id, str) and container.image_id
            }
        )
        image_digests: dict[str, str] = {}
        for image_id in image_ids:
            output = self._get(
                self._resource_path("images", image_id),
                deadline=deadline,
                max_bytes=MAX_INSPECT_BYTES,
            )
            if output is None:
                continue
            text = self._decode(output)
            if text is not None:
                image_digests.update(parse_image_digests(text))

        for container in containers:
            digest = image_digests.get(container.image_id or "")
            if digest is not None:
                container.image_digest = digest[:140]
        return containers

    def copy_file_archive(
        self,
        *,
        container_id: str,
        path: str,
        deadline: float,
        max_bytes: int = MAX_DOCKER_CP_ARCHIVE_BYTES,
    ) -> FileCopyResult:
        request_deadline = self._request_deadline(deadline)
        open_result = self._open_get_with_status(
            self._archive_path(container_id, path),
            deadline=request_deadline,
        )
        opened = open_result.opened
        if opened is None:
            if (
                open_result.status == http.client.NOT_FOUND
                and self._archive_path_absent(open_result.error_body)
            ):
                return FileCopyResult(status="absent")
            return FileCopyResult(
                status="failed",
                failure_reason=(
                    "container_artifact_socket_transport_failed"
                    if open_result.status is None
                    else f"container_artifact_socket_http_{open_result.status}"
                ),
            )
        output = bytearray()
        try:
            while True:
                self._refresh_timeout(opened, deadline=request_deadline)
                read_size = min(_READ_CHUNK_BYTES, max_bytes - len(output) + 1)
                chunk = opened.response.read(read_size)
                if not isinstance(chunk, bytes):
                    return FileCopyResult(
                        status="failed",
                        failure_reason="container_artifact_socket_read_failed",
                    )
                if not chunk:
                    return FileCopyResult(status="success", archive=bytes(output))
                output.extend(chunk)
                if len(output) > max_bytes:
                    return FileCopyResult(
                        status="failed",
                        failure_reason="container_artifact_copy_limit_exceeded",
                    )
        except (OSError, http.client.HTTPException, TimeoutError):
            return FileCopyResult(
                status="failed",
                failure_reason="container_artifact_socket_read_failed",
            )
        finally:
            opened.close()

    def copy_tree(
        self,
        *,
        container_id: str,
        root_path: str,
        wanted_file: Callable[[str], bool],
        allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
        deadline: float,
        max_stream_bytes: int = MAX_DOCKER_TREE_STREAM_BYTES,
        max_matched_files: int = MAX_DOCKER_TREE_MATCHED_FILES,
    ) -> _TarWalkResult:
        if time.monotonic() >= deadline:
            return _TarWalkResult(truncated=True)
        request_deadline = self._request_deadline(deadline)
        open_result = self._open_get_with_status(
            self._archive_path(container_id, root_path),
            deadline=request_deadline,
        )
        opened = open_result.opened
        if opened is None:
            if (
                open_result.status == http.client.NOT_FOUND
                and self._archive_path_absent(open_result.error_body)
            ):
                return _TarWalkResult()
            return _TarWalkResult(
                failure_reason=(
                    "container_artifact_socket_transport_failed"
                    if open_result.status is None
                    else f"container_artifact_socket_http_{open_result.status}"
                )
            )

        stream = _DeadlineResponseStream(self, opened, deadline=deadline)
        try:
            return _walk_tar_stream(
                cast(IO[bytes], stream),
                root_path=root_path,
                wanted_file=wanted_file,
                allow_file_in_skipped_directory=allow_file_in_skipped_directory,
                deadline=deadline,
                max_stream_bytes=max_stream_bytes,
                max_matched_files=max_matched_files,
            )
        finally:
            opened.close()
