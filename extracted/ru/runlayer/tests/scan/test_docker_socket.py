"""Tests for bounded Docker Engine API access over a Unix socket."""

from __future__ import annotations

import io
import json
import stat
import tarfile
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from runlayer_cli.scan.containers import docker_socket as docker_socket_module
from runlayer_cli.scan.containers import inspect_parse as inspect_parse_module
from runlayer_cli.scan.containers.docker_socket import (
    DockerSocketClient,
    _UnixHTTPConnection,
    find_docker_socket,
)

_ResponseSpec = tuple[int, bytes] | OSError

# The bounded inventory request the client issues (``limit`` + running filter).
_INVENTORY_PATH = DockerSocketClient._inventory_path()


class _FakeSocket:
    def __init__(self) -> None:
        self.timeouts: list[float | object] = []
        self.connected_to: str | None = None
        self.closed = False

    def settimeout(self, timeout: float | object) -> None:
        self.timeouts.append(timeout)

    def connect(self, path: str) -> None:
        self.connected_to = path

    def close(self) -> None:
        self.closed = True


class _FakeResponse:
    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self._body = io.BytesIO(body)
        self.closed = False

    def read(self, size: int = -1) -> bytes:
        return self._body.read(size)

    def close(self) -> None:
        self.closed = True


class _FakeConnection:
    def __init__(
        self,
        factory: _ConnectionFactory,
        socket_path: str,
        *,
        timeout: float,
    ) -> None:
        self._factory = factory
        self.socket_path = socket_path
        self.timeout = timeout
        self.sock = _FakeSocket()
        self.path: str | None = None
        self.closed = False

    def request(self, method: str, path: str) -> None:
        assert method == "GET"
        self.path = path
        self._factory.paths.append(path)
        spec = self._factory.routes[path]
        if isinstance(spec, OSError):
            raise spec

    def getresponse(self) -> _FakeResponse:
        assert self.path is not None
        spec = self._factory.routes[self.path]
        assert not isinstance(spec, OSError)
        response = _FakeResponse(*spec)
        self._factory.responses.append(response)
        return response

    def close(self) -> None:
        self.closed = True


class _ConnectionFactory:
    def __init__(self, routes: dict[str, _ResponseSpec]) -> None:
        self.routes = routes
        self.paths: list[str] = []
        self.connections: list[_FakeConnection] = []
        self.responses: list[_FakeResponse] = []

    def __call__(self, socket_path: str, *, timeout: float) -> _FakeConnection:
        connection = _FakeConnection(
            self,
            socket_path,
            timeout=timeout,
        )
        self.connections.append(connection)
        return connection


def _client(
    monkeypatch: pytest.MonkeyPatch,
    routes: dict[str, _ResponseSpec],
) -> tuple[DockerSocketClient, _ConnectionFactory]:
    factory = _ConnectionFactory(routes)
    monkeypatch.setattr(docker_socket_module, "_UnixHTTPConnection", factory)
    return (
        DockerSocketClient("/var/run/docker.sock", request_timeout=1),
        factory,
    )


def _inspect_row() -> dict[str, object]:
    return {
        "Id": "container-1",
        "Name": "/devbox",
        "Image": "sha256:image-id",
        "Config": {
            "Image": "ghcr.io/acme/devbox:latest",
            "User": "vscode",
            "Env": ["HOME=/home/vscode"],
            "WorkingDir": "/workspace",
            "Labels": {},
        },
        "State": {"Running": True},
        "Mounts": [],
    }


def _tar_files(files: dict[str, bytes]) -> bytes:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as copied:
        for name, content in files.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            copied.addfile(info, io.BytesIO(content))
    return archive.getvalue()


def test_unix_http_connection_uses_socket_path(monkeypatch):
    created: list[tuple[int, int]] = []
    fake_socket = _FakeSocket()

    def fake_create_socket(family: int, kind: int) -> _FakeSocket:
        created.append((family, kind))
        return fake_socket

    monkeypatch.setattr(docker_socket_module.socket, "socket", fake_create_socket)

    connection = _UnixHTTPConnection("/var/run/docker.sock", timeout=1.5)
    connection.connect()

    assert created == [
        (docker_socket_module.socket.AF_UNIX, docker_socket_module.socket.SOCK_STREAM)
    ]
    assert fake_socket.timeouts == [1.5]
    assert fake_socket.connected_to == "/var/run/docker.sock"
    assert connection.sock is fake_socket


def test_find_docker_socket_requires_linux_socket_and_access(monkeypatch):
    socket_mode = stat.S_IFSOCK | 0o660
    monkeypatch.setattr(docker_socket_module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        docker_socket_module.os,
        "stat",
        lambda _: type("_Stat", (), {"st_mode": socket_mode})(),
    )
    monkeypatch.setattr(docker_socket_module.os, "access", lambda *_: True)

    assert find_docker_socket() == "/var/run/docker.sock"

    monkeypatch.setattr(docker_socket_module.platform, "system", lambda: "Darwin")
    assert find_docker_socket() is None

    monkeypatch.setattr(docker_socket_module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        docker_socket_module.os,
        "stat",
        lambda _: type("_Stat", (), {"st_mode": stat.S_IFREG | 0o660})(),
    )
    assert find_docker_socket() is None

    monkeypatch.setattr(
        docker_socket_module.os,
        "stat",
        lambda _: type("_Stat", (), {"st_mode": socket_mode})(),
    )
    monkeypatch.setattr(docker_socket_module.os, "access", lambda *_: False)
    assert find_docker_socket() is None


def test_find_docker_socket_handles_missing_path(monkeypatch):
    monkeypatch.setattr(docker_socket_module.platform, "system", lambda: "Linux")

    def missing_stat(_: str) -> object:
        raise FileNotFoundError

    monkeypatch.setattr(docker_socket_module.os, "stat", missing_stat)

    assert find_docker_socket() is None


def test_engine_api_inventory_inspect_and_image_digest(monkeypatch):
    digest = "sha256:" + "b" * 64
    routes: dict[str, _ResponseSpec] = {
        _INVENTORY_PATH: (200, json.dumps([{"Id": "container-1"}]).encode()),
        "/containers/container-1/json": (200, json.dumps(_inspect_row()).encode()),
        "/images/sha256%3Aimage-id/json": (
            200,
            json.dumps(
                {
                    "Id": "sha256:image-id",
                    "RepoDigests": [f"ghcr.io/acme/devbox@{digest}"],
                }
            ).encode(),
        ),
    }
    client, factory = _client(monkeypatch, routes)
    deadline = time.monotonic() + 5

    inventory = client.discover_container_ids(deadline=deadline)
    assert inventory == {
        "container_ids": ["container-1"],
        "truncated": False,
        "malformed": False,
        "output_empty": False,
    }

    containers = client.inspect_containers(
        container_ids=inventory["container_ids"],
        deadline=deadline,
        host_home=Path("/Users/alex"),
    )
    assert containers is not None
    assert containers[0].runtime == "docker"
    assert containers[0].working_dir == "/workspace"

    enriched = client.collect_image_digests(
        containers=containers,
        deadline=deadline,
    )
    assert enriched[0].image_digest == digest
    assert factory.paths == list(routes)
    assert all(response.closed for response in factory.responses)


def test_engine_inventory_marks_malformed_and_truncated(monkeypatch):
    rows: list[object] = [
        {"Id": "container-0"},
        {"Id": "container-0"},
        "bad",
        *[
            {"Id": f"container-{index}"}
            for index in range(1, inspect_parse_module.MAX_CONTAINERS + 1)
        ],
    ]
    client, _ = _client(
        monkeypatch,
        {_INVENTORY_PATH: (200, json.dumps(rows).encode())},
    )

    inventory = client.discover_container_ids(deadline=time.monotonic() + 5)

    assert inventory is not None
    assert len(inventory["container_ids"]) == inspect_parse_module.MAX_CONTAINERS
    assert inventory["malformed"] is True
    assert inventory["truncated"] is True


def test_discover_container_ids_bounds_busy_host_payload(monkeypatch):
    """Busy hosts must cap the inventory request instead of streaming it whole.

    Regression: the unbounded ``/containers/json`` request pulled the full
    running inventory before the parser truncated it, so a busy Portainer
    host's fatter Engine API payload blew past the byte cap, ``_get`` returned
    ``None``, and the whole container scan silently no-oped. The request now
    caps rows with ``limit`` (+1 so truncation past ``MAX_CONTAINERS`` is still
    detected) and a running ``status`` filter.
    """
    bounded = json.dumps(
        [
            {"Id": f"container-{index}"}
            for index in range(inspect_parse_module.MAX_CONTAINERS + 1)
        ]
    ).encode()
    oversized = b"x" * (2 * 1024 * 1024)
    requested_paths: list[str] = []

    class _BusyHostConnection:
        def __init__(self, socket_path: str, *, timeout: float) -> None:
            self.sock = _FakeSocket()
            self._path = ""

        def request(self, method: str, path: str) -> None:
            self._path = path
            requested_paths.append(path)

        def getresponse(self) -> _FakeResponse:
            # No ``limit`` ⇒ the pre-fix full-inventory payload overruns the cap.
            body = bounded if "limit=" in self._path else oversized
            return _FakeResponse(200, body)

        def close(self) -> None:
            pass

    monkeypatch.setattr(
        docker_socket_module, "_UnixHTTPConnection", _BusyHostConnection
    )
    client = DockerSocketClient("/var/run/docker.sock", request_timeout=1)

    inventory = client.discover_container_ids(deadline=time.monotonic() + 5)

    assert inventory is not None
    assert len(inventory["container_ids"]) == inspect_parse_module.MAX_CONTAINERS
    assert inventory["truncated"] is True

    assert len(requested_paths) == 1
    query = parse_qs(urlparse(requested_paths[0]).query)
    assert query["limit"] == [str(inspect_parse_module.MAX_CONTAINERS + 1)]
    assert query["filters"] == ['{"status":["running","paused","restarting"]}']
    stopped_query = parse_qs(
        urlparse(DockerSocketClient._stopped_inventory_path()).query
    )
    assert stopped_query["filters"] == [
        '{"status":["created","removing","exited","dead"]}'
    ]


def test_engine_api_archive_file_and_tree(monkeypatch):
    file_archive = _tar_files({"mcp.json": b"{}"})
    tree_archive = _tar_files({"workspace/project/.cursor/mcp.json": b'{"ok":true}'})
    routes: dict[str, _ResponseSpec] = {
        "/containers/container%2F1/archive?path=%2Fhome%2Fvscode%2Fmcp.json": (
            200,
            file_archive,
        ),
        "/containers/container%2F1/archive?path=%2Fworkspace": (200, tree_archive),
    }
    client, factory = _client(monkeypatch, routes)
    deadline = time.monotonic() + 5

    copied = client.copy_file_archive(
        container_id="container/1",
        path="/home/vscode/mcp.json",
        deadline=deadline,
    )
    walked = client.copy_tree(
        container_id="container/1",
        root_path="/workspace",
        wanted_file=lambda path: path.endswith("mcp.json"),
        deadline=deadline,
    )

    assert copied == file_archive
    assert walked.truncated is False
    assert walked.files == {"/workspace/project/.cursor/mcp.json": b'{"ok":true}'}
    assert factory.paths == list(routes)


def test_engine_api_responses_are_size_bounded(monkeypatch):
    routes: dict[str, _ResponseSpec] = {
        _INVENTORY_PATH: (200, b'[{"Id":"container-1"}]'),
        "/containers/container-1/json": (200, json.dumps(_inspect_row()).encode()),
        "/containers/container-1/archive?path=%2Fconfig": (200, b"12345"),
        "/containers/container-1/archive?path=%2Fworkspace": (
            200,
            _tar_files({"workspace/file": b"content"}),
        ),
    }
    client, _ = _client(monkeypatch, routes)
    monkeypatch.setattr(docker_socket_module, "MAX_ENGINE_INVENTORY_BYTES", 4)
    monkeypatch.setattr(docker_socket_module, "MAX_INSPECT_BYTES", 4)
    deadline = time.monotonic() + 5

    assert client.discover_container_ids(deadline=deadline) is None
    assert (
        client.inspect_containers(
            container_ids=["container-1"],
            deadline=deadline,
            host_home=Path("/"),
        )
        is None
    )
    assert (
        client.copy_file_archive(
            container_id="container-1",
            path="/config",
            deadline=deadline,
            max_bytes=4,
        )
        is None
    )
    walked = client.copy_tree(
        container_id="container-1",
        root_path="/workspace",
        wanted_file=lambda _: True,
        deadline=deadline,
        max_stream_bytes=4,
    )
    assert walked.truncated is True
    assert walked.files == {}


@pytest.mark.parametrize(
    "response",
    [
        (500, b"daemon error"),
        OSError("connect failed"),
    ],
)
def test_engine_api_failures_are_nonfatal(monkeypatch, response: _ResponseSpec):
    client, factory = _client(
        monkeypatch,
        {_INVENTORY_PATH: response},
    )

    assert client.discover_container_ids(deadline=time.monotonic() + 5) is None
    assert all(connection.closed for connection in factory.connections)


def test_engine_api_read_stops_at_deadline(monkeypatch):
    client, factory = _client(
        monkeypatch,
        {_INVENTORY_PATH: (200, b"[]")},
    )
    # request_deadline, open, then a refresh past the deadline aborts the read.
    readings = iter([0.0, 0.0, 2.0])
    monkeypatch.setattr(
        docker_socket_module.time,
        "monotonic",
        lambda: next(readings),
    )

    assert client.discover_container_ids(deadline=1.0) is None
    assert factory.responses[0].closed is True


def test_engine_api_open_stops_when_request_timeout_already_elapsed(monkeypatch):
    client, factory = _client(
        monkeypatch,
        {_INVENTORY_PATH: (200, b"[]")},
    )
    readings = iter([0.0, 2.0])
    monkeypatch.setattr(
        docker_socket_module.time,
        "monotonic",
        lambda: next(readings),
    )

    assert client.discover_container_ids(deadline=100.0) is None
    assert factory.responses == []


def test_slow_drip_request_bounded_by_request_timeout(monkeypatch):
    """A slow-drip response must abort after ``request_timeout`` wall-clock, not
    ride the whole scan deadline by refreshing the per-read socket timeout."""
    clock = {"now": 0.0}
    monkeypatch.setattr(
        docker_socket_module.time,
        "monotonic",
        lambda: clock["now"],
    )

    class _DripResponse:
        def __init__(self) -> None:
            self.status = 200
            self.closed = False
            self.reads = 0

        def read(self, size: int = -1) -> bytes:
            # Each read "blocks" just under the request timeout then dribbles a
            # byte, never reaching EOF — the pathological Engine API drip.
            self.reads += 1
            clock["now"] += 0.5
            return b" "

        def close(self) -> None:
            self.closed = True

    drip = _DripResponse()

    class _DripConnection:
        def __init__(self, socket_path: str, *, timeout: float) -> None:
            self.sock = _FakeSocket()
            self.path: str | None = None
            self.closed = False

        def request(self, method: str, path: str) -> None:
            self.path = path

        def getresponse(self) -> _DripResponse:
            return drip

        def close(self) -> None:
            self.closed = True

    monkeypatch.setattr(docker_socket_module, "_UnixHTTPConnection", _DripConnection)

    client = DockerSocketClient("/var/run/docker.sock", request_timeout=1)

    assert client.discover_container_ids(deadline=100.0) is None
    # Bounded by request_timeout (~1s), not the 100s scan deadline.
    assert clock["now"] <= 5.0
    assert drip.reads <= 5
    assert drip.closed is True
