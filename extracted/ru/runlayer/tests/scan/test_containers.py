"""Tests for Mode B running-container MCP config discovery."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import pytest
import structlog

from runlayer_cli.scan.agent_definition_scanner import DiscoveredAgentDefinition
from runlayer_cli.scan.clients import (
    ConfigPath,
    InstallProbe,
    MCPClientDefinition,
    NpmPackage,
    ProjectConfigPattern,
)
from runlayer_cli.scan.containers import (
    MAX_SINGLE_FILE_BYTES,
    ContainerMount,
    ContainerScanResult,
    DiscoveredContainer,
    parse_container_inspect,
    path_is_shared_with_host_home,
    scan_running_containers,
)
from runlayer_cli.scan.containers import collect as containers_module
from runlayer_cli.scan.containers import docker_cli as docker_cli_module
from runlayer_cli.scan.containers import docker_socket as docker_socket_module
from runlayer_cli.scan.containers import inspect_parse as inspect_parse_module
from runlayer_cli.scan.containers import tar_walk as tar_walk_module
from runlayer_cli.scan.containers.docker_cli import _find_docker_cli
from runlayer_cli.scan.containers.inspect_parse import _parse_docker_ps_inventory
from runlayer_cli.scan.containers.tar_walk import _extract_copied_file
from runlayer_cli.scan.config_parser import MCPClientConfig, parse_config_content
from runlayer_cli.scan.skill_scanner import DiscoveredSkillArtifact


def _tar_file(content: bytes, name: str = "mcp.json") -> bytes:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as copied:
        info = tarfile.TarInfo(name=name)
        info.size = len(content)
        copied.addfile(info, io.BytesIO(content))
    return archive.getvalue()


def _tar_files(files: dict[str, bytes]) -> bytes:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as copied:
        for name, content in files.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            copied.addfile(info, io.BytesIO(content))
    return archive.getvalue()


class _FakeDockerCopyProcess:
    def __init__(self, archive: bytes, *, running: bool = False) -> None:
        self.stdout = io.BytesIO(archive)
        self.returncode = None if running else 0
        self.killed = False
        self.waited = False

    def poll(self):
        return self.returncode

    def kill(self):
        self.killed = True
        self.returncode = -9

    def wait(self, timeout=None):
        del timeout
        self.waited = True
        if self.returncode is None:
            self.returncode = 0
        return self.returncode


def _inspect_row(
    *,
    mounts: list[dict[str, str]] | None = None,
    working_dir: str = "/workspace",
) -> dict:
    return {
        "Id": "container-1",
        "Name": "/devbox",
        "Image": "sha256:image-id",
        "Config": {
            "Image": "ghcr.io/acme/devbox:latest",
            "User": "vscode",
            "Env": ["HOME=/home/vscode", "TOKEN=secret"],
            "WorkingDir": working_dir,
            "Labels": {
                "devcontainer.local_folder": "/Users/alex/project",
                "safe": "value",
            },
        },
        "State": {"Running": True},
        "Mounts": mounts or [],
    }


def test_parse_docker_ps_ignores_malformed_rows():
    output = "\n".join(
        [
            json.dumps({"ID": "abc"}),
            "not-json",
            json.dumps({"ID": "abc"}),
            json.dumps({"Id": "def"}),
        ]
    )

    assert _parse_docker_ps_inventory(output)["container_ids"] == ["abc", "def"]


def test_docker_ps_reports_inventory_truncation():
    output = "\n".join(json.dumps({"ID": f"container-{index}"}) for index in range(65))

    parsed = _parse_docker_ps_inventory(output)

    assert len(parsed["container_ids"]) == inspect_parse_module.MAX_CONTAINERS
    assert parsed["truncated"] is True


def test_find_docker_cli_checks_launchd_fallbacks(monkeypatch):
    monkeypatch.setattr(docker_cli_module.shutil, "which", lambda _: None)
    monkeypatch.setattr(docker_cli_module.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        docker_cli_module.Path,
        "is_file",
        lambda path: str(path) == "/usr/local/bin/docker",
    )
    monkeypatch.setattr(
        docker_cli_module.os,
        "access",
        lambda path, mode: str(path) == "/usr/local/bin/docker",
    )

    assert _find_docker_cli() == "/usr/local/bin/docker"


def test_find_docker_cli_checks_windows_fallbacks(monkeypatch):
    expected = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
    monkeypatch.setattr(docker_cli_module.shutil, "which", lambda _: None)
    monkeypatch.setattr(docker_cli_module.platform, "system", lambda: "Windows")
    monkeypatch.setenv("ProgramFiles", r"C:\Program Files")
    monkeypatch.delenv("ProgramW6432", raising=False)
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    monkeypatch.setattr(
        docker_cli_module.Path,
        "is_file",
        lambda path: str(path) == expected,
    )
    monkeypatch.setattr(
        docker_cli_module.os,
        "access",
        lambda path, mode: str(path) == expected,
    )

    assert _find_docker_cli() == expected


def test_default_container_scan_budget_scales_and_caps():
    assert docker_cli_module._scaled_scan_time_budget(0) == 30
    assert docker_cli_module._scaled_scan_time_budget(1) == 40
    assert docker_cli_module._scaled_scan_time_budget(7) == 100
    assert docker_cli_module._scaled_scan_time_budget(64) == 300


def test_parse_container_inspect_extracts_context():
    containers = parse_container_inspect(
        [_inspect_row()],
        host_home=Path("/Users/alex"),
    )

    assert len(containers) == 1
    container = containers[0]
    assert container.container_id == "container-1"
    assert container.name == "devbox"
    assert container.image_ref == "ghcr.io/acme/devbox:latest"
    # Content-addressed image id doubles as the digest until
    # _collect_image_digests enriches with the repository digest.
    assert container.image_digest == "sha256:image-id"
    assert container.home == "/home/vscode"
    assert container.working_dir == "/workspace"
    assert container.is_devcontainer is True
    assert container.labels["safe"] == "value"


@pytest.mark.parametrize(
    ("config_format", "servers_key", "content"),
    [
        (
            "json",
            "mcpServers",
            b'{"mcpServers":{"github":{"command":"npx"}}}',
        ),
        (
            "yaml",
            "mcpServers",
            b"mcpServers:\n  github:\n    command: npx\n",
        ),
        (
            "toml",
            "mcp_servers",
            b'[mcp_servers.github]\ncommand = "npx"\n',
        ),
    ],
)
def test_in_memory_parser_supports_registered_config_formats(
    config_format, servers_key, content
):
    client = MCPClientDefinition(
        name="format-test",
        display_name="Format Test",
        paths=[],
        servers_key=servers_key,
        config_format=config_format,
    )

    assert [server.name for server in parse_config_content(client, content)] == [
        "github"
    ]


def test_shared_bind_mount_maps_container_path_to_host_home():
    mounts = [
        ContainerMount(
            mount_type="bind",
            source="/Users/alex/project",
            destination="/workspace",
        )
    ]

    assert path_is_shared_with_host_home(
        "/workspace/.cursor/mcp.json",
        mounts,
        Path("/Users/alex"),
    )
    assert not path_is_shared_with_host_home(
        "/opt/app/.cursor/mcp.json",
        mounts,
        Path("/Users/alex"),
    )


def test_streaming_tar_walker_finds_nested_project_config():
    archive = _tar_files(
        {
            "workspace/orders-api/.cursor/mcp.json": (
                b'{"mcpServers":{"github":{"command":"npx"}}}'
            ),
        }
    )

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda path: path.endswith("/.cursor/mcp.json"),
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=10,
    )

    assert result.files == {
        "/workspace/orders-api/.cursor/mcp.json": (
            b'{"mcpServers":{"github":{"command":"npx"}}}'
        )
    }
    assert result.truncated is False


def test_project_skill_root_is_exact_and_limited_to_four_levels():
    at_workdir = containers_module._project_skill_file_match(
        "/workspace/skills/deploy/SKILL.md",
        root_path="/workspace",
    )
    within = containers_module._project_skill_file_match(
        "/workspace/a/b/c/d/.agents/skills/deploy/SKILL.md",
        root_path="/workspace",
    )
    beyond = containers_module._project_skill_file_match(
        "/workspace/a/b/c/d/e/.agents/skills/deploy/SKILL.md",
        root_path="/workspace",
    )

    assert at_workdir is not None
    assert at_workdir.project_path == "/workspace"
    assert at_workdir.skill_path == "/workspace/skills/deploy"
    assert within is not None
    assert within.project_path == "/workspace/a/b/c/d"
    assert within.skill_path == "/workspace/a/b/c/d/.agents/skills/deploy"
    assert beyond is None


def test_streaming_tar_walker_skips_dependency_directories():
    skipped_dirs = ("node_modules", ".venv", "venv", "vendor", "dist", ".tox", ".git")
    archive = _tar_files(
        {
            **{
                f"workspace/{directory}/pkg/.cursor/mcp.json": b"ignored"
                for directory in skipped_dirs
            },
            "workspace/orders-api/.cursor/mcp.json": b"wanted",
        }
    )

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda path: path.endswith("/.cursor/mcp.json"),
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=10,
    )

    assert result.files == {"/workspace/orders-api/.cursor/mcp.json": b"wanted"}
    assert result.truncated is False


def test_streaming_tar_walker_skips_oversized_matched_file():
    archive = _tar_files(
        {"workspace/orders-api/.cursor/mcp.json": (b"x" * (MAX_SINGLE_FILE_BYTES + 1))}
    )

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda path: path.endswith("/.cursor/mcp.json"),
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=10,
    )

    assert result.files == {}
    assert result.truncated is False


def test_streaming_tar_walker_stops_at_stream_byte_budget():
    archive = _tar_files({"workspace/orders-api/.cursor/mcp.json": b"wanted"})

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda path: True,
        deadline=time.monotonic() + 1,
        max_stream_bytes=511,
        max_matched_files=10,
    )

    assert result.files == {}
    assert result.truncated is True


def test_streaming_tar_walker_stops_at_match_budget():
    archive = _tar_files(
        {
            "workspace/first/.cursor/mcp.json": b"first",
            "workspace/second/.cursor/mcp.json": b"second",
        }
    )

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda path: path.endswith("/.cursor/mcp.json"),
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=1,
    )

    assert result.files == {"/workspace/first/.cursor/mcp.json": b"first"}
    assert result.truncated is True


def test_streaming_tar_walker_reserves_priority_matches_after_regular_cap():
    package_path = "/workspace/node_modules/@anthropic-ai/claude-code/package.json"
    archive = _tar_files(
        {
            "workspace/first.dat": b"first",
            "workspace/second.dat": b"second",
            package_path.removeprefix("/"): b'{"name":"@anthropic-ai/claude-code"}',
        }
    )

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda _path: True,
        allow_file_in_skipped_directory=lambda path: path == package_path,
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=1,
    )

    assert result.files == {
        "/workspace/first.dat": b"first",
        package_path: b'{"name":"@anthropic-ai/claude-code"}',
    }
    assert result.truncated is True


def test_streaming_tar_walker_evicts_regular_match_for_priority_bytes(monkeypatch):
    package_path = "/workspace/node_modules/agent/package.json"
    archive = _tar_files(
        {
            "workspace/noise.dat": b"noise",
            package_path.removeprefix("/"): b"agent",
        }
    )
    monkeypatch.setattr(tar_walk_module, "MAX_TOTAL_BYTES", 5)

    result = tar_walk_module._walk_tar_stream(
        io.BytesIO(archive),
        root_path="/workspace",
        wanted_file=lambda _path: True,
        allow_file_in_skipped_directory=lambda path: path == package_path,
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=10,
    )

    assert result.files == {package_path: b"agent"}
    assert result.truncated is True


def test_streaming_tar_walker_stops_at_deadline(monkeypatch):
    clock = [0.0]

    class AdvancingStream(io.BytesIO):
        def read(self, size=-1):
            content = super().read(size)
            clock[0] = 1.0
            return content

    archive = _tar_files({"workspace/orders-api/.cursor/mcp.json": b"wanted"})
    monkeypatch.setattr(tar_walk_module.time, "monotonic", lambda: clock[0])

    result = tar_walk_module._walk_tar_stream(
        AdvancingStream(archive),
        root_path="/workspace",
        wanted_file=lambda path: True,
        deadline=0.5,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=10,
    )

    assert result.files == {}
    assert result.truncated is True


def test_streaming_tar_walker_treats_tar_error_as_truncated_without_logging():
    with structlog.testing.capture_logs() as logs:
        result = tar_walk_module._walk_tar_stream(
            io.BytesIO(b"not a tar archive"),
            root_path="/workspace",
            wanted_file=lambda path: True,
            deadline=time.monotonic() + 1,
            max_stream_bytes=64,
            max_matched_files=10,
        )

    assert result.files == {}
    assert result.truncated is True
    assert logs == []


def test_streaming_tar_walker_logs_unexpected_error_type():
    archive = _tar_files({"workspace/orders-api/.cursor/mcp.json": b"wanted"})

    def raising_wanted_file(_path: str) -> bool:
        raise KeyError("boom")

    with structlog.testing.capture_logs() as logs:
        result = tar_walk_module._walk_tar_stream(
            io.BytesIO(archive),
            root_path="/workspace",
            wanted_file=raising_wanted_file,
            deadline=time.monotonic() + 1,
            max_stream_bytes=len(archive) + 1,
            max_matched_files=10,
        )

    assert result.files == {}
    assert result.truncated is True
    unexpected = [
        entry
        for entry in logs
        if entry["event"] == "Unexpected error walking container tar stream"
    ]
    assert unexpected == [
        {
            "event": "Unexpected error walking container tar stream",
            "log_level": "warning",
            "error_type": "KeyError",
        }
    ]


def test_streaming_tree_copy_kills_and_reaps_on_budget_exhaustion(monkeypatch):
    archive = _tar_files(
        {
            "workspace/first/.cursor/mcp.json": b"first",
            "workspace/second/.cursor/mcp.json": b"second",
        }
    )
    process = _FakeDockerCopyProcess(archive, running=True)
    commands = []

    def fake_popen(cmd, *, stdout, stderr):
        assert stdout is tar_walk_module.subprocess.PIPE
        assert stderr is tar_walk_module.subprocess.DEVNULL
        commands.append(cmd)
        return process

    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = tar_walk_module._copy_container_tree(
        docker="/docker",
        container_id="container-1",
        root_path="/workspace",
        wanted_file=lambda path: path.endswith("/.cursor/mcp.json"),
        deadline=time.monotonic() + 1,
        max_stream_bytes=len(archive) + 1,
        max_matched_files=1,
    )

    assert commands == [["/docker", "cp", "container-1:/workspace", "-"]]
    assert result.truncated is True
    assert process.killed is True
    assert process.waited is True


def test_scan_reads_known_config_from_docker_cp(monkeypatch):
    client = MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[ConfigPath("~/.cursor/mcp.json", platform="linux")],
        servers_key="mcpServers",
    )
    inspect_output = json.dumps([_inspect_row(working_dir="")])

    monkeypatch.setattr(docker_cli_module.shutil, "which", lambda _: "/usr/bin/docker")

    def fake_run_text(cmd, *, timeout, max_output):
        del timeout, max_output
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return json.dumps(
                [
                    {
                        "Id": "sha256:image-id",
                        "RepoDigests": ["ghcr.io/acme/devbox@sha256:" + "b" * 64],
                    }
                ]
            )
        return inspect_output

    config = {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
            }
        }
    }

    def fake_run_bytes(cmd, *, timeout, max_output):
        del timeout, max_output
        assert cmd[-2:] == ["container-1:/home/vscode/.cursor/mcp.json", "-"]
        return _tar_file(json.dumps(config).encode())

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(containers_module, "_run_bytes", fake_run_bytes)

    result = scan_running_containers(
        clients=[client],
        host_home=Path("/Users/alex"),
    )

    assert len(result.containers) == 1
    assert len(result.configurations) == 1
    found = result.configurations[0]
    assert found.client == "cursor"
    assert found.config_scope == "container"
    assert found.config_path == "/home/vscode/.cursor/mcp.json"
    assert found.container_id == "container-1"
    assert found.container_name == "devbox"
    assert found.container_image_digest == "sha256:" + "b" * 64
    assert [server.name for server in found.servers] == ["github"]
    assert found.servers[0].runtime == "container"
    assert result.containers[0].has_mcp_configs is True
    assert result.containers[0].to_api_payload()["has_mcp_configs"] is True


def test_scan_collects_stopped_containers_and_local_images(monkeypatch):
    stopped_row = _inspect_row()
    stopped_row["Id"] = "stopped-1"
    stopped_row["Name"] = "/stopped-devbox"
    stopped_row["State"] = {"Running": False}

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            if "-a" in cmd:
                return json.dumps({"ID": "stopped-1"})
            return ""
        if cmd[1] == "inspect":
            return json.dumps([stopped_row])
        if cmd[1:3] == ["image", "inspect"]:
            image_id = cmd[3]
            return json.dumps(
                [
                    {
                        "Id": image_id,
                        "RepoDigests": (
                            ["ghcr.io/acme/devbox@" + "sha256:" + "c" * 64]
                            if image_id == "sha256:image-id"
                            else []
                        ),
                        "Config": {
                            "Labels": {
                                "org.opencontainers.image.source": (
                                    "https://github.com/modelcontextprotocol/servers"
                                )
                            },
                            "Entrypoint": ["node", "dist/index.js"],
                        },
                    }
                ]
            )
        raise AssertionError(cmd)

    def fake_run_bounded_lines(cmd, **kwargs):
        del kwargs
        assert cmd[1:3] == ["image", "ls"]
        return {
            "text": json.dumps(
                {
                    "Repository": "ghcr.io/example/mcp",
                    "Tag": "latest",
                    "Digest": "sha256:" + "a" * 64,
                    "ID": "sha256:" + "b" * 64,
                }
            ),
            "truncation_reason": None,
        }

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(
        docker_cli_module, "_run_bounded_utf8_lines", fake_run_bounded_lines
    )

    result = scan_running_containers(clients=[])

    assert result.scan_succeeded is True
    assert result.stopped_containers_succeeded is True
    assert [container.container_id for container in result.stopped_containers] == [
        "stopped-1"
    ]
    assert result.stopped_containers[0].is_running is False
    assert result.stopped_containers[0].image_digest == "sha256:" + "c" * 64
    assert result.container_images_succeeded is True
    assert result.container_images_truncated is False
    assert [image.to_api_payload() for image in result.container_images] == [
        {
            "repository": "ghcr.io/example/mcp",
            "tag": "latest",
            "digest": "sha256:" + "a" * 64,
            "labels": {
                "org.opencontainers.image.source": (
                    "https://github.com/modelcontextprotocol/servers"
                )
            },
            "entrypoint": ["node", "dist/index.js"],
        }
    ]


def test_container_image_inventory_is_capped():
    output = "\n".join(
        json.dumps(
            {
                "Repository": f"ghcr.io/example/mcp-{index}",
                "Tag": "latest",
                "Digest": "sha256:" + f"{index:064x}",
            }
        )
        for index in range(inspect_parse_module.MAX_CONTAINER_IMAGES + 5)
    )

    inventory = inspect_parse_module.parse_docker_image_ls(output)

    assert inventory is not None
    assert len(inventory["images"]) == inspect_parse_module.MAX_CONTAINER_IMAGES
    assert inventory["truncated"] is True


def test_image_inspect_batches_continue_after_failed_batch(monkeypatch):
    commands: list[list[str]] = []

    def fake_run_text(cmd, **_kwargs):
        commands.append(cmd)
        return None if "image-1" in cmd else "[]"

    monkeypatch.setattr(docker_cli_module, "MAX_IMAGE_INSPECT_BATCH", 2)
    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    outputs = list(
        docker_cli_module._inspect_image_batches(  # noqa: SLF001
            docker="/docker",
            image_ids=["image-1", "image-2", "image-3"],
            deadline=time.monotonic() + 10,
            subprocess_timeout=1,
        )
    )

    assert commands == [
        ["/docker", "image", "inspect", "image-1", "image-2"],
        ["/docker", "image", "inspect", "image-3"],
    ]
    assert outputs == ["[]"]


def test_cli_image_inventory_preserves_metadata_after_failed_batch(monkeypatch):
    rows = [
        {
            "Repository": f"local/image-{index}",
            "Tag": "latest",
            "Digest": "<none>",
            "ID": f"sha256:image-{index}",
        }
        for index in range(2)
    ]

    monkeypatch.setattr(docker_cli_module, "MAX_IMAGE_INSPECT_BATCH", 1)
    monkeypatch.setattr(
        docker_cli_module,
        "_run_bounded_utf8_lines",
        lambda *_args, **_kwargs: {
            "text": "\n".join(json.dumps(row) for row in rows),
            "truncation_reason": None,
        },
    )

    def fake_run_text(cmd, **_kwargs):
        image_id = cmd[3]
        if image_id == "sha256:image-0":
            return None
        return json.dumps(
            [
                {
                    "Id": image_id,
                    "Config": {
                        "Labels": {"safe": "value"},
                        "Entrypoint": ["node", "index.js"],
                    },
                }
            ]
        )

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    inventory = docker_cli_module._list_container_images(
        docker="/docker",
        deadline=time.monotonic() + 1,
        subprocess_timeout=1,
    )

    assert inventory is not None
    first, second = [image.to_api_payload() for image in inventory["images"]]
    assert "labels" not in first
    assert "entrypoint" not in first
    assert second["labels"] == {"safe": "value"}
    assert second["entrypoint"] == ["node", "index.js"]


@pytest.mark.parametrize(
    ("config", "uncollected_field"),
    [
        (
            {"Labels": ["not", "a", "mapping"], "Entrypoint": ["node"]},
            "labels",
        ),
        (
            {"Labels": {"safe": "value"}, "Entrypoint": {"not": "a list"}},
            "entrypoint",
        ),
    ],
    ids=["malformed-labels", "malformed-entrypoint"],
)
def test_cli_image_inventory_does_not_collect_malformed_config_as_empty(
    monkeypatch,
    config,
    uncollected_field,
):
    image_id = "sha256:image"
    monkeypatch.setattr(
        docker_cli_module,
        "_run_bounded_utf8_lines",
        lambda *_args, **_kwargs: {
            "text": json.dumps(
                {
                    "Repository": "local/image",
                    "Tag": "latest",
                    "Digest": "<none>",
                    "ID": image_id,
                }
            ),
            "truncation_reason": None,
        },
    )
    monkeypatch.setattr(
        docker_cli_module,
        "_run_text",
        lambda *_args, **_kwargs: json.dumps([{"Id": image_id, "Config": config}]),
    )

    inventory = docker_cli_module._list_container_images(
        docker="/docker",
        deadline=time.monotonic() + 1,
        subprocess_timeout=1,
    )

    assert inventory is not None
    payload = inventory["images"][0].to_api_payload()
    assert uncollected_field not in payload
    if uncollected_field == "labels":
        assert payload["entrypoint"] == ["node"]
    else:
        assert payload["labels"] == {"safe": "value"}


@pytest.mark.parametrize(
    "config",
    [
        {"Labels": None, "Entrypoint": None},
        {"Labels": {}, "Entrypoint": []},
    ],
    ids=["null", "empty"],
)
def test_cli_image_inventory_collects_explicit_empty_config(monkeypatch, config):
    image_id = "sha256:image"
    monkeypatch.setattr(
        docker_cli_module,
        "_run_bounded_utf8_lines",
        lambda *_args, **_kwargs: {
            "text": json.dumps(
                {
                    "Repository": "local/image",
                    "Tag": "latest",
                    "Digest": "<none>",
                    "ID": image_id,
                }
            ),
            "truncation_reason": None,
        },
    )
    monkeypatch.setattr(
        docker_cli_module,
        "_run_text",
        lambda *_args, **_kwargs: json.dumps([{"Id": image_id, "Config": config}]),
    )

    inventory = docker_cli_module._list_container_images(
        docker="/docker",
        deadline=time.monotonic() + 1,
        subprocess_timeout=1,
    )

    assert inventory is not None
    payload = inventory["images"][0].to_api_payload()
    assert payload["labels"] == {}
    assert payload["entrypoint"] == []


def test_socket_image_inventory_fetches_config_metadata_with_aggregate_bound(
    monkeypatch,
):
    image_ids = ["sha256:image-1", "sha256:image-2"]
    summary = json.dumps(
        [
            {
                "Id": image_id,
                "RepoTags": (
                    ["local/image-1:latest", "local/image-1:stable"]
                    if index == 1
                    else [f"local/image-{index}:latest"]
                ),
                "RepoDigests": [],
            }
            for index, image_id in enumerate(image_ids, start=1)
        ]
    ).encode()
    details = {
        image_id: json.dumps(
            {
                "Id": image_id,
                "Config": {
                    "Labels": {"image": str(index)},
                    "Entrypoint": ["node", f"server-{index}.js"],
                },
            }
        ).encode()
        for index, image_id in enumerate(image_ids, start=1)
    }
    client = docker_socket_module.DockerSocketClient(
        "/var/run/docker.sock",
        request_timeout=1,
    )
    requests: list[tuple[str, int]] = []

    def fake_get(path, *, deadline, max_bytes):
        del deadline
        requests.append((path, max_bytes))
        if path == "/images/json?all=false&digests=true":
            return summary
        for image_id, detail in details.items():
            if path == client._resource_path("images", image_id):
                return detail
        raise AssertionError(path)

    monkeypatch.setattr(client, "_get", fake_get)

    inventory = client.list_container_images(deadline=time.monotonic() + 1)

    assert inventory is not None
    assert [image.to_api_payload() for image in inventory["images"]] == [
        {
            "repository": "local/image-1",
            "tag": "latest",
            "digest": "sha256:image-1",
            "labels": {"image": "1"},
            "entrypoint": ["node", "server-1.js"],
        },
        {
            "repository": "local/image-1",
            "tag": "stable",
            "digest": "sha256:image-1",
            "labels": {"image": "1"},
            "entrypoint": ["node", "server-1.js"],
        },
        {
            "repository": "local/image-2",
            "tag": "latest",
            "digest": "sha256:image-2",
            "labels": {"image": "2"},
            "entrypoint": ["node", "server-2.js"],
        },
    ]
    assert requests[1:] == [
        (
            client._resource_path("images", image_ids[0]),
            docker_socket_module.MAX_INSPECT_BYTES,
        ),
        (
            client._resource_path("images", image_ids[1]),
            docker_socket_module.MAX_INSPECT_BYTES - len(details[image_ids[0]]),
        ),
    ]


def test_socket_image_inventory_skips_failed_config_inspects(monkeypatch):
    image_ids = ["sha256:image-1", "sha256:image-2"]
    summary = json.dumps(
        [
            {
                "Id": image_id,
                "RepoTags": [f"local/image-{index}:latest"],
                "RepoDigests": [],
            }
            for index, image_id in enumerate(image_ids, start=1)
        ]
    ).encode()
    detail = json.dumps(
        {
            "Id": image_ids[1],
            "Config": {
                "Labels": {"image": "2"},
                "Entrypoint": ["node", "server-2.js"],
            },
        }
    ).encode()
    client = docker_socket_module.DockerSocketClient(
        "/var/run/docker.sock",
        request_timeout=1,
    )

    def fake_get(path, *, deadline, max_bytes):
        del deadline, max_bytes
        if path == "/images/json?all=false&digests=true":
            return summary
        if path == client._resource_path("images", image_ids[0]):
            return None
        if path == client._resource_path("images", image_ids[1]):
            return detail
        raise AssertionError(path)

    monkeypatch.setattr(client, "_get", fake_get)

    inventory = client.list_container_images(deadline=time.monotonic() + 1)

    assert inventory is not None
    assert [image.to_api_payload() for image in inventory["images"]] == [
        {
            "repository": "local/image-1",
            "tag": "latest",
            "digest": "sha256:image-1",
        },
        {
            "repository": "local/image-2",
            "tag": "latest",
            "digest": "sha256:image-2",
            "labels": {"image": "2"},
            "entrypoint": ["node", "server-2.js"],
        },
    ]


def test_image_config_metadata_is_sanitized_and_bounded():
    labels = {
        f"label-{index}": "x" * (inspect_parse_module.MAX_LABEL_VALUE_CHARS + 10)
        for index in range(inspect_parse_module.MAX_LABELS + 5)
    }
    labels["ORG.OPENCONTAINERS.IMAGE.SOURCE"] = "x" * (
        inspect_parse_module.MAX_LABEL_VALUE_CHARS + 10
    )
    entrypoint = [
        "y" * (inspect_parse_module.MAX_ENTRYPOINT_ITEM_CHARS + 10)
        for _ in range(inspect_parse_module.MAX_ENTRYPOINT_ITEMS + 5)
    ]

    metadata = inspect_parse_module.parse_image_config_metadata(
        json.dumps(
            [
                {
                    "Id": "sha256:image",
                    "Config": {"Labels": labels, "Entrypoint": entrypoint},
                }
            ]
        )
    )["sha256:image"]

    assert len(metadata["labels"]) == inspect_parse_module.MAX_LABELS
    assert "org.opencontainers.image.source" in metadata["labels"]
    assert all(
        len(value) == inspect_parse_module.MAX_LABEL_VALUE_CHARS
        for value in metadata["labels"].values()
    )
    assert len(metadata["entrypoint"]) == inspect_parse_module.MAX_ENTRYPOINT_ITEMS
    assert all(
        len(value) == inspect_parse_module.MAX_ENTRYPOINT_ITEM_CHARS
        for value in metadata["entrypoint"]
    )


def test_image_payload_distinguishes_failed_and_empty_metadata_collection():
    failed = inspect_parse_module.DiscoveredContainerImage(
        repository="local/image",
        tag="latest",
        digest=None,
    )
    collected_empty = inspect_parse_module.DiscoveredContainerImage(
        repository="local/image",
        tag="latest",
        digest=None,
        labels_collected=True,
        entrypoint_collected=True,
    )

    assert "labels" not in failed.to_api_payload()
    assert "entrypoint" not in failed.to_api_payload()
    assert collected_empty.to_api_payload()["labels"] == {}
    assert collected_empty.to_api_payload()["entrypoint"] == []


def test_image_config_metadata_has_scan_wide_cap(monkeypatch):
    monkeypatch.setattr(
        inspect_parse_module,
        "MAX_IMAGE_CONFIG_METADATA_CHARS",
        10,
    )

    metadata = inspect_parse_module.parse_image_config_metadata(
        json.dumps(
            [
                {"Id": "one", "Config": {"Labels": {"k": "123456"}}},
                {"Id": "two", "Config": {"Labels": {"k": "123456"}}},
            ]
        )
    )

    assert set(metadata) == {"one"}


def test_repeated_image_alias_metadata_stays_inside_wire_cap(monkeypatch):
    monkeypatch.setattr(
        inspect_parse_module,
        "MAX_IMAGE_CONFIG_METADATA_CHARS",
        10,
    )
    images = [
        inspect_parse_module.DiscoveredContainerImage(
            repository=f"local/image-{index}",
            tag="latest",
            digest="sha256:same",
            labels={"k": "123456"},
            labels_collected=True,
        )
        for index in range(2)
    ]

    inspect_parse_module.bound_image_inventory_metadata(images)

    assert images[0].to_api_payload()["labels"] == {"k": "123456"}
    assert "labels" not in images[1].to_api_payload()


def test_cli_image_inventory_keeps_parseable_prefix_when_output_exceeds_byte_cap(
    monkeypatch,
):
    first_row = json.dumps(
        {
            "Repository": "ghcr.io/example/first",
            "Tag": "latest",
            "Digest": "sha256:" + "1" * 64,
        }
    )
    second_row = json.dumps(
        {
            "Repository": "ghcr.io/example/second",
            "Tag": "latest",
            "Digest": "sha256:" + "2" * 64,
        }
    )
    process = _FakeDockerCopyProcess(f"{first_row}\n{second_row}\n".encode())
    monkeypatch.setattr(
        docker_cli_module.subprocess,
        "Popen",
        lambda *args, **kwargs: process,
    )
    monkeypatch.setattr(
        docker_cli_module,
        "MAX_IMAGE_LIST_BYTES",
        len(first_row.encode()) + 1,
    )

    with structlog.testing.capture_logs() as logs:
        inventory = docker_cli_module._list_container_images(
            docker="/docker",
            deadline=time.monotonic() + 1,
            subprocess_timeout=1,
        )

    assert inventory is not None
    assert [image.repository for image in inventory["images"]] == [
        "ghcr.io/example/first"
    ]
    assert inventory["truncated"] is True
    assert process.killed is True
    assert process.waited is True
    assert logs == [
        {
            "event": "Container image inventory truncated",
            "log_level": "warning",
            "max_bytes": len(first_row.encode()) + 1,
            "max_images": inspect_parse_module.MAX_CONTAINER_IMAGES,
            "reason": "max_bytes",
        }
    ]


def test_cli_image_inventory_never_accepts_incomplete_json_line(monkeypatch):
    first_row = json.dumps(
        {
            "Repository": "ghcr.io/example/first",
            "Tag": "latest",
            "Digest": "sha256:" + "1" * 64,
        }
    )
    incomplete_row = '{"Repository":"ghcr.io/example/incomplete"'
    process = _FakeDockerCopyProcess(f"{first_row}\n{incomplete_row}".encode())
    monkeypatch.setattr(
        docker_cli_module.subprocess,
        "Popen",
        lambda *args, **kwargs: process,
    )

    with structlog.testing.capture_logs() as logs:
        inventory = docker_cli_module._list_container_images(
            docker="/docker",
            deadline=time.monotonic() + 1,
            subprocess_timeout=1,
        )

    assert inventory is not None
    assert [image.repository for image in inventory["images"]] == [
        "ghcr.io/example/first"
    ]
    assert inventory["truncated"] is True
    assert process.waited is True
    assert logs[0]["reason"] == "incomplete_line"


def test_cli_image_inventory_terminates_at_image_cap(monkeypatch):
    output = "".join(
        json.dumps(
            {
                "Repository": f"ghcr.io/example/mcp-{index}",
                "Tag": "latest",
                "Digest": "sha256:" + f"{index:064x}",
            }
        )
        + "\n"
        for index in range(inspect_parse_module.MAX_CONTAINER_IMAGES + 1)
    )
    process = _FakeDockerCopyProcess(output.encode())
    monkeypatch.setattr(
        docker_cli_module.subprocess,
        "Popen",
        lambda *args, **kwargs: process,
    )

    inventory = docker_cli_module._list_container_images(
        docker="/docker",
        deadline=time.monotonic() + 1,
        subprocess_timeout=1,
    )

    assert inventory is not None
    assert len(inventory["images"]) == inspect_parse_module.MAX_CONTAINER_IMAGES
    assert inventory["truncated"] is True
    assert process.killed is True
    assert process.waited is True


def test_cli_image_inventory_uses_image_id_when_repo_digest_is_absent():
    image_id = "sha256:" + "a" * 64
    output = json.dumps(
        {
            "Repository": "local/mcp",
            "Tag": "latest",
            "Digest": "<none>",
            "ID": image_id,
        }
    )

    inventory = inspect_parse_module.parse_docker_image_ls(output)

    assert inventory is not None
    assert inventory["truncated"] is False
    assert [image.to_api_payload() for image in inventory["images"]] == [
        {
            "repository": "local/mcp",
            "tag": "latest",
            "digest": image_id,
        }
    ]


def test_engine_image_inventory_shares_image_id_across_local_tags():
    image_id = "sha256:" + "b" * 64
    output = json.dumps(
        [
            {
                "Id": image_id,
                "RepoTags": ["local/mcp:latest", "local/mcp:stable"],
                "RepoDigests": None,
            }
        ]
    )

    inventory = inspect_parse_module.parse_docker_engine_images(output)

    assert inventory is not None
    assert inventory["truncated"] is False
    assert [(image.tag, image.digest) for image in inventory["images"]] == [
        ("latest", image_id),
        ("stable", image_id),
    ]


def test_malformed_image_inventory_is_not_reported_successful(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return ""
        raise AssertionError(cmd)

    def fake_run_bounded_lines(cmd, **kwargs):
        del kwargs
        assert cmd[1:3] == ["image", "ls"]
        return {"text": "not-json", "truncation_reason": None}

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(
        docker_cli_module, "_run_bounded_utf8_lines", fake_run_bounded_lines
    )

    result = scan_running_containers(clients=[])

    assert result.scan_succeeded is True
    assert result.stopped_containers_succeeded is True
    assert result.container_images_succeeded is False


def test_engine_image_inventory_rejects_partial_malformed_response():
    output = json.dumps(
        [
            {
                "RepoTags": ["ghcr.io/example/mcp:latest"],
                "RepoDigests": ["ghcr.io/example/mcp@sha256:" + "a" * 64],
            },
            "not-an-image-row",
        ]
    )

    assert inspect_parse_module.parse_docker_engine_images(output) is None


def test_socket_stopped_inspect_enforces_aggregate_response_cap(monkeypatch):
    rows: dict[str, bytes] = {}
    for container_id in ("stopped-1", "stopped-2"):
        row = _inspect_row()
        row["Id"] = container_id
        row["State"] = {"Running": False}
        rows[f"/containers/{container_id}/json"] = json.dumps(row).encode()

    aggregate_cap = sum(len(output) for output in rows.values()) - 1
    monkeypatch.setattr(docker_socket_module, "MAX_INSPECT_BYTES", aggregate_cap)
    client = docker_socket_module.DockerSocketClient(
        "/var/run/docker.sock",
        request_timeout=1,
    )
    requested_caps: list[int] = []

    def fake_get(path: str, *, deadline: float, max_bytes: int) -> bytes:
        assert deadline > 0
        requested_caps.append(max_bytes)
        return rows[path]

    monkeypatch.setattr(client, "_get", fake_get)

    assert (
        client.inspect_stopped_containers(
            container_ids=["stopped-1", "stopped-2"],
            deadline=time.monotonic() + 1,
            host_home=Path("/Users/alex"),
        )
        is None
    )
    assert requested_caps[0] == aggregate_cap


def test_scan_streams_nested_project_config_and_skill_once(monkeypatch):
    client = MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[],
        project_config=ProjectConfigPattern(".cursor/mcp.json"),
    )
    inspect_output = json.dumps([_inspect_row()])
    archive = _tar_files(
        {
            "workspace/orders-api/.cursor/mcp.json": (
                b'{"mcpServers":{"github":{"command":"npx"}}}'
            ),
            "workspace/orders-api/.agents/skills/deploy/SKILL.md": (
                b"---\nname: deploy\ndescription: Deploy safely\n---\n# Deploy"
            ),
            "workspace/orders-api/.agents/skills/deploy/LICENSE.txt": b"license",
            "workspace/orders-api/.agents/skills/deploy/scripts/deploy.py": (
                b"print('deploy')"
            ),
            "workspace/orders-api/.agents/skills/deploy/vendor/template.md": (
                b"# Template"
            ),
        }
    )
    empty_archive = _tar_files({})
    project_processes = []
    copy_commands = []

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            if "-a" in cmd:
                return ""
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        if cmd[1:3] == ["image", "ls"]:
            return ""
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        assert stdout is tar_walk_module.subprocess.PIPE
        assert stderr is tar_walk_module.subprocess.DEVNULL
        copy_commands.append(cmd)
        if cmd[2] == "container-1:/workspace":
            process = _FakeDockerCopyProcess(archive)
            project_processes.append(process)
            return process
        return _FakeDockerCopyProcess(empty_archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[client],
        host_home=Path("/Users/alex"),
    )

    assert copy_commands.count(["/docker", "cp", "container-1:/workspace", "-"]) == 1
    assert len(project_processes) == 1
    assert project_processes[0].waited is True
    assert len(result.configurations) == 1
    found = result.configurations[0]
    assert found.client == "cursor"
    assert found.config_scope == "container"
    assert found.config_path == "/workspace/orders-api/.cursor/mcp.json"
    assert found.project_path == "/workspace/orders-api"
    assert found.container_id == "container-1"
    assert [server.name for server in found.servers] == ["github"]
    assert found.servers[0].runtime == "container"
    assert found.servers[0].project_name == "/workspace/orders-api"
    assert len(result.skills) == 1
    skill = result.skills[0]
    assert skill.name == "deploy"
    assert skill.path == "/workspace/orders-api/.agents/skills/deploy"
    assert skill.project_path == "/workspace/orders-api"
    assert skill.scope == "project"
    assert skill.tool == "multi"
    assert skill.source_type == "user"
    assert skill.git_remote_url is None
    assert skill.symlinks_found == []
    assert skill.has_scripts is True
    assert {file.title for file in skill.files} == {
        "SKILL.md",
        "LICENSE.txt",
        "scripts/deploy.py",
    }
    assert skill.identifier is not None
    assert skill.container_id == "container-1"
    monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/workspace")
    skill_payload = skill.to_api_payload()
    assert skill_payload["path"] == "/workspace/orders-api/.agents/skills/deploy"
    assert skill_payload["project_path"] == "/workspace/orders-api"
    assert skill_payload["container"] == {
        "container_id": "container-1",
        "name": "devbox",
        "image_ref": "ghcr.io/acme/devbox:latest",
        "image_digest": "sha256:image-id",
        "runtime": "docker",
        "is_devcontainer": True,
        "is_running": True,
        "labels": {
            "devcontainer.local_folder": "/Users/alex/project",
            "safe": "value",
        },
        "mounts_host_home": False,
    }


def test_scan_discovers_project_and_user_agent_definitions_in_existing_tar_pass(
    monkeypatch,
):
    inspect_output = json.dumps([_inspect_row()])
    project_content = b"---\nname: reviewer\ndescription: Reviews code\n---\n# Review\n"
    user_content = b"---\nname: fixer\ndescription: Fixes code\n---\n# Fix\n"
    workdir_archive = _tar_files(
        {
            "workspace/.goose/recipes/root.yaml": b"title: root\n",
            "workspace/a/b/c/d/.gemini/agents/depth-four.md": b"# Depth four\n",
            "workspace/orders/.claude/agents/review.md": project_content,
            "workspace/payments/.claude/agents/review.md": project_content,
            "workspace/a/b/c/d/e/.cursor/agents/too-deep.md": b"# Too deep\n",
        }
    )
    user_archive = _tar_files(
        {
            "agents/fix.md": user_content,
            "agents/node_modules/noise.md": b"# Dependency noise\n",
        }
    )
    empty_archive = _tar_files({})
    copy_commands = []

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        assert stdout is tar_walk_module.subprocess.PIPE
        assert stderr is tar_walk_module.subprocess.DEVNULL
        copy_commands.append(cmd)
        if cmd[2] == "container-1:/workspace":
            archive = workdir_archive
        elif cmd[2] == "container-1:/home/vscode/.cursor/agents":
            archive = user_archive
        else:
            archive = empty_archive
        return _FakeDockerCopyProcess(archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[],
        host_home=Path("/Users/alex"),
    )

    assert copy_commands.count(["/docker", "cp", "container-1:/workspace", "-"]) == 1
    assert [
        (item.client, item.name, item.scope, item.path, item.project_path)
        for item in result.agent_definitions
    ] == [
        (
            "goose",
            "root",
            "project",
            "/workspace/.goose/recipes/root.yaml",
            "/workspace",
        ),
        (
            "gemini_cli",
            "depth-four",
            "project",
            "/workspace/a/b/c/d/.gemini/agents/depth-four.md",
            "/workspace/a/b/c/d",
        ),
        (
            "claude_code",
            "reviewer",
            "project",
            "/workspace/orders/.claude/agents/review.md",
            "/workspace/orders",
        ),
        (
            "claude_code",
            "reviewer",
            "project",
            "/workspace/payments/.claude/agents/review.md",
            "/workspace/payments",
        ),
        (
            "cursor",
            "fixer",
            "user",
            "/home/vscode/.cursor/agents/fix.md",
            None,
        ),
    ]
    assert (
        result.agent_definitions[2].content_hash
        == result.agent_definitions[3].content_hash
    )
    payload = result.agent_definitions[0].to_api_payload()
    assert payload["container"] == {
        "container_id": "container-1",
        "name": "devbox",
        "image_ref": "ghcr.io/acme/devbox:latest",
        "image_digest": "sha256:image-id",
        "runtime": "docker",
        "is_devcontainer": True,
        "is_running": True,
        "labels": {
            "devcontainer.local_folder": "/Users/alex/project",
            "safe": "value",
        },
        "mounts_host_home": False,
    }


def test_scan_skips_container_user_definitions_mounted_from_host_home(monkeypatch):
    inspect_output = json.dumps(
        [
            _inspect_row(
                working_dir="",
                mounts=[
                    {
                        "Type": "bind",
                        "Source": "/Users/alex/.cursor/agents",
                        "Destination": "/home/vscode/.cursor/agents",
                    }
                ],
            )
        ]
    )
    empty_archive = _tar_files({})
    copy_commands = []
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        del stdout, stderr
        copy_commands.append(cmd)
        return _FakeDockerCopyProcess(empty_archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[],
        host_home=Path("/Users/alex"),
    )

    assert result.agent_definitions == []
    assert [
        "/docker",
        "cp",
        "container-1:/home/vscode/.cursor/agents",
        "-",
    ] not in copy_commands
    assert result.containers[0].mounts_host_home is True


def test_scan_discovers_global_container_skill_and_skips_host_home_mount(monkeypatch):
    inspect_output = json.dumps(
        [
            _inspect_row(
                working_dir="/home/vscode",
                mounts=[
                    {
                        "Type": "bind",
                        "Source": "/Users/alex/.agents/skills",
                        "Destination": "/home/vscode/.agents/skills",
                    }
                ],
            )
        ]
    )
    claude_archive = _tar_files(
        {
            "skills/review/SKILL.md": (
                b"---\nname: review\ndescription: Review code\n---\n# Review"
            ),
            "skills/review/references/checklist.md": b"# Checklist",
            "skills/review/node_modules/pkg/noise.md": b"# Dependency noise",
        }
    )
    home_archive = _tar_files(
        {
            "vscode/.claude/skills/review/SKILL.md": (
                b"---\nname: review\ndescription: Review code\n---\n# Review"
            ),
            "vscode/.claude/skills/review/references/checklist.md": b"# Checklist",
        }
    )
    empty_archive = _tar_files({})
    copy_commands = []

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        assert stdout is tar_walk_module.subprocess.PIPE
        assert stderr is tar_walk_module.subprocess.DEVNULL
        copy_commands.append(cmd)
        archive = (
            claude_archive
            if cmd[2] == "container-1:/home/vscode/.claude/skills"
            else (
                home_archive if cmd[2] == "container-1:/home/vscode" else empty_archive
            )
        )
        return _FakeDockerCopyProcess(archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[],
        host_home=Path("/Users/alex"),
    )

    assert len(result.skills) == 1
    skill = result.skills[0]
    assert skill.name == "review"
    assert skill.path == "/home/vscode/.claude/skills/review"
    assert skill.project_path is None
    assert skill.scope == "global"
    assert skill.tool == "claude_code"
    assert skill.source_type == "installed"
    assert {file.title for file in skill.files} == {
        "SKILL.md",
        "references/checklist.md",
    }
    assert all(
        cmd[2] != "container-1:/home/vscode/.agents/skills" for cmd in copy_commands
    )


def test_scan_discovers_disguised_skills_in_generically_hidden_container_paths(
    monkeypatch,
):
    inspect_output = json.dumps([_inspect_row(working_dir="/workspace")])
    hidden_archive = _tar_files(
        {
            "tmp/.mozilla-profile-bak/.state/profile.dat": (
                b"---\nname: review\ndescription: Review code\n---\n# Review"
            ),
            "tmp/.gtk-icon-cache-bak/state/blob.bin": (
                b"---\nname: deploy\ndescription: Deploy safely\n---\n# Deploy"
            ),
            "tmp/ordinary-prefix/state.dat": (
                b"---\nname: observe\ndescription: Observe safely\n---\n# Observe"
            ),
        }
    )
    working_dir_archive = _tar_files(
        {
            "workspace/.editor-state/cache.dat": (
                b"---\nname: triage\ndescription: Triage incidents\n---\n# Triage"
            )
        }
    )
    empty_archive = _tar_files({})

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        assert stdout is tar_walk_module.subprocess.PIPE
        assert stderr is tar_walk_module.subprocess.DEVNULL
        if cmd[2] == "container-1:/var/tmp":
            archive = hidden_archive
        elif cmd[2] == "container-1:/workspace":
            archive = working_dir_archive
        else:
            archive = empty_archive
        return _FakeDockerCopyProcess(archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[],
        detect_disguised_skills=True,
        host_home=Path("/Users/alex"),
    )

    assert {skill.name for skill in result.skills} == {
        "deploy",
        "observe",
        "review",
        "triage",
    }
    assert {skill.path for skill in result.skills} == {
        "/var/tmp/.gtk-icon-cache-bak/state/blob.bin",
        "/var/tmp/.mozilla-profile-bak/.state/profile.dat",
        "/var/tmp/ordinary-prefix/state.dat",
        "/workspace/.editor-state/cache.dat",
    }
    assert all(skill.container_id == "container-1" for skill in result.skills)


@pytest.mark.parametrize(
    ("hidden_prefix", "manifest_name", "target_present", "expected_detection"),
    [
        (".fontconfig-cache", "@anthropic-ai/claude-code", True, True),
        (".gtk-icon-cache-bak", "@anthropic-ai/claude-code", True, True),
        (".npm", "@anthropic-ai/claude-code", True, True),
        ("ordinary-prefix", "@anthropic-ai/claude-code", True, True),
        (".forged", "@anthropic-ai/claude-code", False, False),
        (".updater-tmp", "@example/innocent-tool", True, False),
    ],
)
def test_scan_detects_npm_agent_identity_in_container_prefix(
    monkeypatch,
    hidden_prefix,
    manifest_name,
    target_present,
    expected_detection,
):
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    client = MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[],
        install_probe=InstallProbe(npm_packages=[package]),
    )
    inspect_output = json.dumps([_inspect_row(working_dir="")])
    manifest_path = (
        f"/var/tmp/{hidden_prefix}/lib/node_modules/"
        "@anthropic-ai/claude-code/package.json"
    )
    hidden_archive = _tar_files(
        {
            (
                f"tmp/{hidden_prefix}/lib/node_modules/"
                "@anthropic-ai/claude-code/package.json"
            ): (
                json.dumps(
                    {
                        "name": manifest_name,
                        "version": "4.5.6",
                        "bin": {"claude": "bin/claude.js"},
                    }
                ).encode()
            ),
        }
    )
    target_archive = _tar_files({"claude.js": b"#!/usr/bin/env node\n"})
    empty_archive = _tar_files({})

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        assert stdout is tar_walk_module.subprocess.PIPE
        assert stderr is tar_walk_module.subprocess.DEVNULL
        if cmd[2] == "container-1:/var/tmp":
            archive = hidden_archive
        elif cmd[2].endswith("/bin/claude.js") and target_present:
            archive = target_archive
        else:
            archive = empty_archive
        return _FakeDockerCopyProcess(archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[client],
        host_home=Path("/Users/alex"),
    )

    assert result.containers[0].has_ai_agents is expected_detection
    assert result.containers[0].to_api_payload()["has_ai_agents"] is expected_detection
    if expected_detection:
        assert result.detected_clients[0].client == "claude_code"
        assert result.detected_clients[0].client_version == "4.5.6"
        assert result.detected_clients[0].detected_via == ["container"]
        assert result.detected_clients[0].config_paths == [
            f"container:devbox:{manifest_path}"
        ]
    else:
        assert result.detected_clients == []


def test_standard_container_npm_agent_requires_manifest_and_bin_target():
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    client = MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[],
        install_probe=InstallProbe(npm_packages=[package]),
    )
    manifest = json.dumps(
        {
            "name": package.name,
            "version": "4.5.6",
            "bin": {"claude": "bin/claude.js"},
        }
    ).encode()
    archives = {
        "/usr/local/lib/node_modules/@anthropic-ai/claude-code/package.json": (
            _tar_files({"package.json": manifest})
        ),
        "/usr/local/lib/node_modules/@anthropic-ai/claude-code/bin/claude.js": (
            _tar_files({"claude.js": b"#!/usr/bin/env node\n"})
        ),
    }

    class _Collector:
        def copy_file_archive(self, *, container, path, deadline):
            del container, deadline
            return archives.get(path)

    artifacts = containers_module._CollectedContainerArtifacts()
    ctx = containers_module._PhaseContext(
        collector=_Collector(),
        artifacts=artifacts,
        budget=containers_module._ArtifactByteBudget(),
        deadline=time.monotonic() + 10,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )
    container = DiscoveredContainer(
        container_id="container-1",
        name="devbox",
        image_ref=None,
        image_digest=None,
    )

    containers_module._collect_standard_container_npm_agents(
        ctx,
        container,
        (containers_module._ContainerNpmSpec(client=client, package=package),),
    )

    assert container.has_ai_agents is True
    assert artifacts.detected_clients[0].config_paths == [
        "container:devbox:/usr/local/lib/node_modules/"
        "@anthropic-ai/claude-code/package.json"
    ]


def test_container_npm_manifest_with_nul_bin_target_does_not_abort_collection():
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    client = MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[],
        install_probe=InstallProbe(npm_packages=[package]),
    )
    manifest = json.dumps(
        {
            "name": package.name,
            "version": "4.5.6",
            "bin": {"claude": "bin/clau\x00de.js"},
        }
    ).encode()
    manifest_path = "/usr/local/lib/node_modules/@anthropic-ai/claude-code/package.json"

    class _Collector:
        def copy_file_archive(self, *, container, path, deadline):
            del container, deadline
            if path == manifest_path:
                return _tar_files({"package.json": manifest})
            if "\x00" in path:
                raise ValueError("embedded null byte")
            return None

    artifacts = containers_module._CollectedContainerArtifacts()
    ctx = containers_module._PhaseContext(
        collector=_Collector(),
        artifacts=artifacts,
        budget=containers_module._ArtifactByteBudget(),
        deadline=time.monotonic() + 10,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )
    container = DiscoveredContainer(
        container_id="container-1",
        name="devbox",
        image_ref=None,
        image_digest=None,
    )

    containers_module._collect_standard_container_npm_agents(
        ctx,
        container,
        (containers_module._ContainerNpmSpec(client=client, package=package),),
    )

    assert artifacts.detected_clients == []
    assert container.has_ai_agents is False


def test_nested_host_home_bind_is_not_collected_as_container_npm():
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    client = MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[],
        install_probe=InstallProbe(npm_packages=[package]),
    )
    mounted_destination = "/usr/local/lib/node_modules/@anthropic-ai/claude-code"
    manifest_path = f"{mounted_destination}/package.json"
    target_path = f"{mounted_destination}/bin/claude.js"
    archives = {
        manifest_path: _tar_files(
            {
                "package.json": json.dumps(
                    {
                        "name": package.name,
                        "version": "4.5.6",
                        "bin": {"claude": "bin/claude.js"},
                    }
                ).encode()
            }
        ),
        target_path: _tar_files({"claude.js": b"#!/usr/bin/env node\n"}),
    }
    requested_paths: list[str] = []

    class _Collector:
        def copy_file_archive(self, *, container, path, deadline):
            del container, deadline
            requested_paths.append(path)
            return archives.get(path)

    artifacts = containers_module._CollectedContainerArtifacts()
    ctx = containers_module._PhaseContext(
        collector=_Collector(),
        artifacts=artifacts,
        budget=containers_module._ArtifactByteBudget(),
        deadline=time.monotonic() + 10,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )
    container = DiscoveredContainer(
        container_id="container-1",
        name="devbox",
        image_ref=None,
        image_digest=None,
        mounts=[
            ContainerMount(
                mount_type="bind",
                source="/Users/alex/.npm/lib/node_modules/@anthropic-ai/claude-code",
                destination=mounted_destination,
            )
        ],
    )

    containers_module._collect_standard_container_npm_agents(
        ctx,
        container,
        (containers_module._ContainerNpmSpec(client=client, package=package),),
    )

    assert not [
        path
        for path in requested_paths
        if path == mounted_destination or path.startswith(f"{mounted_destination}/")
    ]
    assert artifacts.detected_clients == []
    assert container.has_ai_agents is False


def test_broad_container_tree_skips_nested_host_home_files_only():
    streamed_roots: list[str] = []
    wanted_paths: dict[str, bool] = {}

    class _Collector:
        def copy_tree(self, *, root_path, wanted_file, **_kwargs):
            streamed_roots.append(root_path)
            wanted_paths["container-local"] = wanted_file(
                "/var/tmp/.fontconfig-cache/profile.dat"
            )
            wanted_paths["host-mounted"] = wanted_file("/var/tmp/.cache/profile.dat")
            return tar_walk_module._TarWalkResult()

    ctx = containers_module._PhaseContext(
        collector=_Collector(),
        artifacts=containers_module._CollectedContainerArtifacts(),
        budget=containers_module._ArtifactByteBudget(),
        deadline=time.monotonic() + 10,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )
    container = DiscoveredContainer(
        container_id="container-1",
        name="devbox",
        image_ref=None,
        image_digest=None,
        home="/root",
        mounts=[
            ContainerMount(
                mount_type="bind",
                source="/Users/alex/.cache",
                destination="/var/tmp/.cache",
            )
        ],
    )

    containers_module._collect_container_hidden_artifacts(
        ctx,
        container,
        npm_specs=(),
        detect_disguised_skills=True,
    )

    assert "/var/tmp" in streamed_roots
    assert wanted_paths == {
        "container-local": True,
        "host-mounted": False,
    }


def test_artifact_byte_budget_charges_walked_files_in_aggregate(monkeypatch):
    monkeypatch.setattr(containers_module, "MAX_TOTAL_BYTES", 10)
    budget = containers_module._ArtifactByteBudget()
    budget.charge_files({"/a": b"1234", "/b": b"12345"})
    assert budget.total_bytes == 9
    with pytest.raises(containers_module._CollectionBudgetExhausted):
        budget.charge_files({"/c": b"12"})


def test_scan_wide_stream_budget_stops_noise_without_starving_later_npm(
    monkeypatch,
):
    package = NpmPackage("@anthropic-ai/claude-code", "claude")
    client = MCPClientDefinition(
        name="claude_code",
        display_name="Claude Code",
        paths=[],
        install_probe=InstallProbe(npm_packages=[package]),
    )
    containers = [
        DiscoveredContainer(
            container_id="container-1",
            name="first",
            image_ref=None,
            image_digest=None,
            home="/home/first",
        ),
        DiscoveredContainer(
            container_id="container-2",
            name="second",
            image_ref=None,
            image_digest=None,
            home="/home/second",
        ),
    ]
    priority_npm_containers: list[str] = []
    broad_tree_requests: list[tuple[str, str]] = []
    stream_cap = getattr(
        containers_module,
        "MAX_DOCKER_SCAN_STREAM_BYTES",
        getattr(
            tar_walk_module,
            "MAX_DOCKER_SCAN_STREAM_BYTES",
            tar_walk_module.MAX_DOCKER_TREE_STREAM_BYTES,
        ),
    )

    class _Collector:
        def copy_tree(self, *, container, root_path, **_kwargs):
            broad_tree_requests.append((container.container_id, root_path))
            result = tar_walk_module._TarWalkResult(truncated=True)
            setattr(
                result,
                "stream_bytes",
                stream_cap if len(broad_tree_requests) == 1 else 0,
            )
            return result

    for phase in (
        "_collect_container_configs",
        "_collect_container_project_tree",
        "_collect_container_global_skills",
        "_collect_container_user_definitions",
    ):
        monkeypatch.setattr(
            containers_module,
            phase,
            lambda *_args, **_kwargs: None,
        )

    def record_priority_npm(_ctx, container, _specs):
        priority_npm_containers.append(container.container_id)

    monkeypatch.setattr(
        containers_module,
        "_collect_standard_container_npm_agents",
        record_priority_npm,
    )

    containers_module._collect_container_artifacts(
        collector=_Collector(),
        containers=containers,
        clients=[client],
        deadline=time.monotonic() + 10,
        subprocess_timeout=1,
        host_home=Path("/Users/alex"),
    )

    assert priority_npm_containers == ["container-1", "container-2"]
    assert len(broad_tree_requests) == 1


def test_scan_collected_skill_bytes_exhaust_shared_byte_budget(monkeypatch):
    """Skill/agent-def bytes count against the same budget as config bytes."""
    inspect_output = json.dumps([_inspect_row(working_dir="")])
    claude_archive = _tar_files(
        {
            "skills/review/SKILL.md": (
                b"---\nname: review\ndescription: Review code\n---\n# Review"
            ),
        }
    )
    empty_archive = _tar_files({})
    copy_commands = []

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(containers_module, "MAX_TOTAL_BYTES", 16)

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def fake_popen(cmd, *, stdout, stderr):
        del stdout, stderr
        copy_commands.append(cmd)
        archive = (
            claude_archive
            if cmd[2] == "container-1:/home/vscode/.claude/skills"
            else empty_archive
        )
        return _FakeDockerCopyProcess(archive)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(
        docker_cli_module,
        "_run_bounded_utf8_lines",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(tar_walk_module.subprocess, "Popen", fake_popen)

    result = scan_running_containers(
        clients=[],
        host_home=Path("/Users/alex"),
    )

    # The over-budget skill walk aborts collection: its artifact is dropped and
    # no further trees (remaining global roots, agent user roots) are copied.
    assert result.skills == []
    assert result.agent_definitions == []
    assert copy_commands == [
        ["/docker", "cp", "container-1:/home/vscode/.claude/skills", "-"]
    ]


def test_scan_parses_container_inspect_output_once(monkeypatch):
    inspect_output = json.dumps([_inspect_row(working_dir="")])
    real_json_loads = json.loads
    inspect_parse_count = 0

    def counting_json_loads(value, *args, **kwargs):
        nonlocal inspect_parse_count
        if value == inspect_output:
            inspect_parse_count += 1
        return real_json_loads(value, *args, **kwargs)

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            if "-a" in cmd:
                return ""
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        if cmd[1:3] == ["image", "ls"]:
            return ""
        return inspect_output

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(docker_cli_module.json, "loads", counting_json_loads)

    result = scan_running_containers(clients=[])

    assert result.containers
    assert inspect_parse_count == 1


def test_scan_skips_project_config_shared_with_host_home(monkeypatch):
    client = MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[],
        project_config=ProjectConfigPattern(".cursor/mcp.json"),
    )
    inspect_output = json.dumps(
        [
            _inspect_row(
                mounts=[
                    {
                        "Type": "bind",
                        "Source": "/Users/alex/project",
                        "Destination": "/workspace",
                    }
                ]
            )
        ]
    )
    monkeypatch.setattr(docker_cli_module.shutil, "which", lambda _: "/usr/bin/docker")

    def fake_run_text(cmd, *, timeout, max_output):
        del timeout, max_output
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return inspect_output

    def unexpected_copy(*args, **kwargs):
        raise AssertionError("shared config must not be copied")

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(containers_module, "_run_bytes", unexpected_copy)

    result = scan_running_containers(
        clients=[client],
        host_home=Path("/Users/alex"),
    )

    assert result.configurations == []
    assert result.containers[0].mounts_host_home is True
    assert result.containers[0].has_mcp_configs is False


def test_oversized_copied_file_is_rejected():
    archive = _tar_file(b"x" * (MAX_SINGLE_FILE_BYTES + 1))

    assert _extract_copied_file(archive) is None


def test_malformed_nonempty_docker_ps_is_not_a_successful_empty_scan(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(
        docker_cli_module,
        "_run_text",
        lambda *args, **kwargs: "not-json",
    )

    result = scan_running_containers(clients=[])

    assert result.scan_succeeded is False


def test_partially_malformed_docker_ps_is_not_authoritative(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    ps_output = "\n".join([json.dumps({"ID": "container-1"}), "not-json"])

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return ps_output
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return json.dumps([_inspect_row(working_dir="")])

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    result = scan_running_containers(clients=[])

    assert result.containers
    assert result.scan_succeeded is False


def test_malformed_docker_inspect_is_not_a_successful_empty_scan(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        return "{}"

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    result = scan_running_containers(clients=[])

    assert result.scan_succeeded is False


def test_mismatched_docker_inspect_ids_are_not_authoritative(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    mismatched_row = _inspect_row(working_dir="")
    mismatched_row["Id"] = "different-container"

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return json.dumps({"ID": "container-1"})
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return json.dumps([mismatched_row])

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    result = scan_running_containers(clients=[])

    assert result.scan_succeeded is False


def test_truncated_inventory_is_not_authoritative(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    ps_output = "\n".join(
        json.dumps({"ID": f"container-{index}"}) for index in range(65)
    )
    inspect_rows = []
    for index in range(inspect_parse_module.MAX_CONTAINERS):
        row = _inspect_row(working_dir="")
        row["Id"] = f"container-{index}"
        inspect_rows.append(row)

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[1] == "ps":
            return ps_output
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return json.dumps(inspect_rows)

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    result = scan_running_containers(clients=[])

    assert len(result.containers) == inspect_parse_module.MAX_CONTAINERS
    assert result.scan_succeeded is False


def test_missing_docker_transport_is_a_noop(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: None)
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)

    assert scan_running_containers().containers == []


def test_docker_cli_takes_precedence_over_socket(monkeypatch):
    docker_lookups = 0
    socket_checked = False

    def find_docker_cli():
        nonlocal docker_lookups
        docker_lookups += 1
        return "/docker"

    def unexpected_socket_lookup():
        nonlocal socket_checked
        socket_checked = True
        return "/var/run/docker.sock"

    monkeypatch.setattr(containers_module, "_find_docker_cli", find_docker_cli)
    monkeypatch.setattr(
        containers_module,
        "find_docker_socket",
        unexpected_socket_lookup,
    )
    monkeypatch.setattr(docker_cli_module, "_run_text", lambda *args, **kwargs: "")
    monkeypatch.setattr(
        docker_cli_module,
        "_run_bounded_utf8_lines",
        lambda *args, **kwargs: {"text": "", "truncation_reason": None},
    )

    result = scan_running_containers(clients=[])

    assert result.scan_succeeded is True
    assert docker_lookups == 1
    assert socket_checked is False


def test_docker_scan_shares_scaled_budget_with_supplemental_inventory(monkeypatch):
    deadlines: list[tuple[str, float]] = []
    running_container = DiscoveredContainer(
        container_id="running-1",
        name="running",
        image_ref=None,
        image_digest=None,
    )

    class Collector:
        def discover_stopped_container_ids(self, *, deadline):
            deadlines.append(("stopped-discovery", deadline))
            return {
                "container_ids": ["stopped-1", "stopped-2"],
                "truncated": False,
                "malformed": False,
                "output_empty": False,
            }

        def inspect_stopped_containers(self, *, container_ids, deadline, host_home):
            del container_ids, host_home
            deadlines.append(("stopped-inspect", deadline))
            return []

        def collect_image_digests(self, *, containers, deadline):
            del deadline
            return containers

        def list_container_images(self, *, deadline):
            deadlines.append(("images", deadline))
            return {"images": [], "truncated": False}

    collector = Collector()
    started_at = 100.0

    def fake_scan_with_collector(*, started_at, **_kwargs):
        deadlines.append(("running", started_at))
        return ContainerScanResult(
            containers=[running_container],
            scan_succeeded=True,
        )

    monkeypatch.setattr(containers_module.time, "monotonic", lambda: started_at)
    monkeypatch.setattr(
        containers_module,
        "_iter_available_docker_collectors",
        lambda **_kwargs: iter([collector]),
    )
    monkeypatch.setattr(
        containers_module,
        "_iter_available_k3s_collectors",
        lambda **_kwargs: iter(()),
    )
    monkeypatch.setattr(
        containers_module,
        "_scan_with_collector",
        fake_scan_with_collector,
    )

    result = scan_running_containers(clients=[])

    running_deadline = started_at + docker_cli_module._scaled_scan_time_budget(1)
    combined_deadline = started_at + docker_cli_module._scaled_scan_time_budget(3)
    assert deadlines == [
        ("running", started_at),
        ("stopped-discovery", running_deadline),
        ("stopped-inspect", combined_deadline),
        ("images", combined_deadline),
    ]
    assert result.containers == [running_container]
    assert result.stopped_containers_succeeded is True
    assert result.container_images_succeeded is True


def test_docker_supplemental_inventory_is_not_starved_by_k3s(monkeypatch):
    clock = [100.0]
    phases: list[str] = []
    running_container = DiscoveredContainer(
        container_id="running-1",
        name="running",
        image_ref=None,
        image_digest=None,
    )

    class DockerCollector:
        def discover_stopped_container_ids(self, *, deadline):
            phases.append("docker-supplemental")
            if deadline <= clock[0]:
                return None
            return {
                "container_ids": [],
                "truncated": False,
                "malformed": False,
                "output_empty": True,
            }

        def list_container_images(self, *, deadline):
            if deadline <= clock[0]:
                return None
            return {"images": [], "truncated": False}

    docker_collector = DockerCollector()

    def fake_scan_runtime(
        collectors,
        *,
        discovered_collectors=None,
        started_at=None,
        **_kwargs,
    ):
        collector = next(iter(collectors), None)
        if collector is None:
            return None  # absent runtime (podman/nerdctl not installed)
        if discovered_collectors is not None:
            phases.append("docker-running")
            discovered_collectors.append(collector)
            assert started_at == 100.0
            return ContainerScanResult(
                containers=[running_container],
                scan_succeeded=True,
            )

        phases.append("k3s")
        clock[0] += 50.0
        return ContainerScanResult(scan_succeeded=True)

    monkeypatch.setattr(containers_module.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(
        containers_module,
        "_iter_available_docker_collectors",
        lambda **_kwargs: iter([docker_collector]),
    )
    monkeypatch.setattr(
        containers_module,
        "_iter_available_k3s_collectors",
        lambda **_kwargs: iter([object()]),
    )
    monkeypatch.setattr(containers_module, "_scan_runtime", fake_scan_runtime)

    result = scan_running_containers(clients=[], time_budget=40.0)

    assert phases == ["docker-running", "docker-supplemental", "k3s"]
    assert result.stopped_containers_succeeded is True
    assert result.container_images_succeeded is True


def test_scan_falls_back_to_engine_api_socket(monkeypatch):
    client = MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[ConfigPath("~/.cursor/mcp.json", platform="linux")],
        servers_key="mcpServers",
    )
    config_archive = _tar_file(
        b'{"mcpServers":{"github":{"command":"npx","args":["-y","github"]}}}'
    )
    digest = "sha256:" + "b" * 64
    stopped_row = _inspect_row(working_dir="")
    stopped_row["Id"] = "stopped-1"
    stopped_row["State"] = {"Running": False}
    routes = {
        docker_socket_module.DockerSocketClient._inventory_path(): (
            200,
            json.dumps([{"Id": "container-1"}]).encode(),
        ),
        docker_socket_module.DockerSocketClient._stopped_inventory_path(): (
            200,
            json.dumps([{"Id": "stopped-1"}]).encode(),
        ),
        "/containers/container-1/json": (
            200,
            json.dumps(_inspect_row(working_dir="")).encode(),
        ),
        "/containers/stopped-1/json": (
            200,
            json.dumps(stopped_row).encode(),
        ),
        "/images/sha256%3Aimage-id/json": (
            200,
            json.dumps(
                {
                    "Id": "sha256:image-id",
                    "RepoDigests": [f"ghcr.io/acme/devbox@{digest}"],
                }
            ).encode(),
        ),
        "/images/json?all=false&digests=true": (
            200,
            json.dumps(
                [
                    {
                        "Id": "sha256:image-id",
                        "RepoTags": ["ghcr.io/acme/devbox:latest"],
                        "RepoDigests": [f"ghcr.io/acme/devbox@{digest}"],
                    }
                ]
            ).encode(),
        ),
        "/containers/container-1/archive?path=%2Fhome%2Fvscode%2F.cursor%2Fmcp.json": (
            200,
            config_archive,
        ),
    }
    requested_paths: list[str] = []

    class FakeResponse(io.BytesIO):
        def __init__(self, status: int, body: bytes) -> None:
            super().__init__(body)
            self.status = status

    class FakeConnection:
        def __init__(self, socket_path: str, *, timeout: float) -> None:
            assert socket_path == "/var/run/docker.sock"
            assert timeout > 0
            self.sock = None
            self.path = ""

        def request(self, method: str, path: str) -> None:
            assert method == "GET"
            self.path = path
            requested_paths.append(path)

        def getresponse(self) -> FakeResponse:
            status, body = routes.get(self.path, (404, b""))
            return FakeResponse(status, body)

        def close(self) -> None:
            pass

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: None)
    monkeypatch.setattr(
        containers_module,
        "find_docker_socket",
        lambda: "/var/run/docker.sock",
    )
    monkeypatch.setattr(
        docker_socket_module,
        "_UnixHTTPConnection",
        FakeConnection,
    )

    result = scan_running_containers(
        clients=[client],
        host_home=Path("/Users/alex"),
    )

    assert result.scan_succeeded is True
    assert len(result.containers) == 1
    assert result.containers[0].runtime == "docker"
    assert result.containers[0].image_digest == digest
    assert len(result.configurations) == 1
    assert result.configurations[0].config_path == "/home/vscode/.cursor/mcp.json"
    assert [container.container_id for container in result.stopped_containers] == [
        "stopped-1"
    ]
    assert result.stopped_containers_succeeded is True
    assert [image.to_api_payload() for image in result.container_images] == [
        {
            "repository": "ghcr.io/acme/devbox",
            "tag": "latest",
            "digest": digest,
        }
    ]
    assert result.container_images_succeeded is True
    assert [server.name for server in result.configurations[0].servers] == ["github"]
    assert requested_paths[:4] == [
        docker_socket_module.DockerSocketClient._inventory_path(),
        "/containers/container-1/json",
        "/images/sha256%3Aimage-id/json",
        "/containers/container-1/archive?path=%2Fhome%2Fvscode%2F.cursor%2Fmcp.json",
    ]
    assert requested_paths[-5:] == [
        docker_socket_module.DockerSocketClient._stopped_inventory_path(),
        "/containers/stopped-1/json",
        "/images/sha256%3Aimage-id/json",
        "/images/json?all=false&digests=true",
        "/images/sha256%3Aimage-id/json",
    ]


def test_windows_scans_when_docker_is_available(monkeypatch):
    docker_looked_up = False

    def fake_find_docker_cli():
        nonlocal docker_looked_up
        docker_looked_up = True
        return r"C:\Program Files\Docker\docker.exe"

    monkeypatch.setattr(docker_cli_module.platform, "system", lambda: "Windows")
    monkeypatch.setattr(containers_module, "_find_docker_cli", fake_find_docker_cli)
    monkeypatch.setattr(
        docker_cli_module,
        "_run_text",
        lambda *args, **kwargs: "",
    )

    result = scan_running_containers(clients=[])

    assert docker_looked_up is True
    assert result.scan_succeeded is True


def test_docker_cli_running_inventory_is_producer_bounded(monkeypatch):
    captured: list[str] = []

    def fake_run_text(command, **_kwargs):
        captured.extend(command)
        return ""

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    inventory = docker_cli_module._discover_container_ids(
        docker="/usr/bin/docker",
        deadline=time.monotonic() + 5,
        subprocess_timeout=1,
    )

    assert inventory is not None
    assert captured == [
        "/usr/bin/docker",
        "ps",
        "--last",
        str(inspect_parse_module.MAX_CONTAINERS + 1),
        "--no-trunc",
        "--filter",
        "status=running",
        "--filter",
        "status=paused",
        "--filter",
        "status=restarting",
        "--format",
        "{{json .}}",
    ]


def test_docker_cli_stopped_inventory_excludes_restarting(monkeypatch):
    captured: list[str] = []

    def fake_run_text(command, **_kwargs):
        captured.extend(command)
        return ""

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)

    inventory = docker_cli_module._discover_stopped_container_ids(
        docker="/usr/bin/docker",
        deadline=time.monotonic() + 5,
        subprocess_timeout=1,
    )

    assert inventory is not None
    assert captured == [
        "/usr/bin/docker",
        "ps",
        "-a",
        "--last",
        str(inspect_parse_module.MAX_CONTAINERS + 1),
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


def test_scan_falls_back_to_socket_when_cli_discovery_fails(monkeypatch):
    calls: list[str] = []

    class UnavailableCollector:
        def discover_container_ids(self, *, deadline):
            assert deadline > 0
            calls.append("cli")
            return None

    class EmptyInventoryCollector:
        def discover_container_ids(self, *, deadline):
            assert deadline > 0
            calls.append("socket")
            return {
                "container_ids": [],
                "truncated": False,
                "malformed": False,
                "output_empty": True,
            }

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(
        containers_module,
        "find_docker_socket",
        lambda: "/var/run/docker.sock",
    )
    monkeypatch.setattr(
        containers_module,
        "DockerCliCollector",
        lambda *args, **kwargs: UnavailableCollector(),
    )
    monkeypatch.setattr(
        containers_module,
        "DockerSocketCollector",
        lambda *args, **kwargs: EmptyInventoryCollector(),
    )

    result = scan_running_containers(clients=[])

    assert calls == ["cli", "socket"]
    assert result.scan_succeeded is True


def test_scan_returns_empty_when_cli_discovery_fails_without_socket(monkeypatch):
    class UnavailableCollector:
        def discover_container_ids(self, *, deadline):
            assert deadline > 0
            return None

    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)
    monkeypatch.setattr(
        containers_module,
        "DockerCliCollector",
        lambda *args, **kwargs: UnavailableCollector(),
    )

    result = scan_running_containers(clients=[])

    assert result == ContainerScanResult()


def test_merge_scan_results_prefers_first_container_and_its_artifacts():
    preferred = DiscoveredContainer(
        container_id="shared",
        name="cli",
        image_ref=None,
        image_digest=None,
    )
    duplicate = DiscoveredContainer(
        container_id="shared",
        name="socket",
        image_ref=None,
        image_digest=None,
    )
    unique = DiscoveredContainer(
        container_id="unique",
        name="k3s",
        image_ref=None,
        image_digest=None,
    )
    preferred_config = MCPClientConfig(client="cli", container_id="shared")
    duplicate_config = MCPClientConfig(client="socket", container_id="shared")
    unique_config = MCPClientConfig(client="k3s", container_id="unique")
    preferred_skill = DiscoveredSkillArtifact(
        name="cli-skill",
        path="/cli-skill",
        artifact_type="skill",
        scope="global",
        tool="cursor",
        container_id="shared",
    )
    duplicate_skill = DiscoveredSkillArtifact(
        name="socket-skill",
        path="/socket-skill",
        artifact_type="skill",
        scope="global",
        tool="cursor",
        container_id="shared",
    )
    unique_skill = DiscoveredSkillArtifact(
        name="k3s-skill",
        path="/k3s-skill",
        artifact_type="skill",
        scope="global",
        tool="cursor",
        container_id="unique",
    )
    preferred_definition = DiscoveredAgentDefinition(
        client="cli",
        name="cli-agent",
        description=None,
        scope="user",
        path="/cli-agent.md",
        project_path=None,
        content_hash="cli",
        container_id="shared",
    )
    duplicate_definition = DiscoveredAgentDefinition(
        client="socket",
        name="socket-agent",
        description=None,
        scope="user",
        path="/socket-agent.md",
        project_path=None,
        content_hash="socket",
        container_id="shared",
    )
    unique_definition = DiscoveredAgentDefinition(
        client="k3s",
        name="k3s-agent",
        description=None,
        scope="user",
        path="/k3s-agent.md",
        project_path=None,
        content_hash="k3s",
        container_id="unique",
    )

    merged = containers_module._merge_scan_results(
        [
            ContainerScanResult(
                containers=[preferred],
                configurations=[preferred_config],
                skills=[preferred_skill],
                agent_definitions=[preferred_definition],
                scan_succeeded=True,
            ),
            ContainerScanResult(
                containers=[duplicate, unique],
                configurations=[duplicate_config, unique_config],
                skills=[duplicate_skill, unique_skill],
                agent_definitions=[duplicate_definition, unique_definition],
                scan_succeeded=False,
            ),
        ]
    )

    assert merged.containers == [preferred, unique]
    assert merged.configurations == [preferred_config, unique_config]
    assert merged.skills == [preferred_skill, unique_skill]
    assert merged.agent_definitions == [preferred_definition, unique_definition]
    assert merged.scan_succeeded is False


def test_merge_scan_results_caps_containers_and_artifacts():
    container_count = inspect_parse_module.MAX_CONTAINERS + 1
    containers = [
        DiscoveredContainer(
            container_id=f"container-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
        )
        for index in range(container_count)
    ]
    configurations = [
        MCPClientConfig(client=str(index), container_id=container.container_id)
        for index, container in enumerate(containers)
    ]

    merged = containers_module._merge_scan_results(
        [
            ContainerScanResult(
                containers=containers,
                configurations=configurations,
                scan_succeeded=True,
            )
        ]
    )

    assert len(merged.containers) == inspect_parse_module.MAX_CONTAINERS
    assert len(merged.configurations) == inspect_parse_module.MAX_CONTAINERS
    assert merged.containers[-1].container_id == "container-63"
    # Truncating to fit the cap dropped a running container, so the merged
    # inventory is not authoritative regardless of the input's success flag.
    # (In production a single runtime over the cap is flagged truncated at
    # discovery, so this exact input never reaches the merge; the merge stays
    # cap-safe on its own regardless.)
    assert merged.scan_succeeded is False


def test_merge_scan_results_shares_budget_across_runtimes():
    """A runtime that fills MAX_CONTAINERS must not starve a later runtime.

    Docker is merged before k3s. When Docker discovery alone reaches the shared
    MAX_CONTAINERS cap, the k3s collector's containers (and their artifacts) must
    still appear in the merged result. The backend rejects any scan whose
    container list exceeds MAX_CONTAINERS, so the total stays capped while each
    runtime keeps a fair share of the budget.
    """
    k3s_count = 5
    docker_containers = [
        DiscoveredContainer(
            container_id=f"docker-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
            runtime="docker",
        )
        for index in range(inspect_parse_module.MAX_CONTAINERS)
    ]
    k3s_containers = [
        DiscoveredContainer(
            container_id=f"k3s-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
            runtime="k3s",
        )
        for index in range(k3s_count)
    ]
    k3s_configs = [
        MCPClientConfig(client="k3s", container_id=container.container_id)
        for container in k3s_containers
    ]

    merged = containers_module._merge_scan_results(
        [
            ContainerScanResult(
                containers=docker_containers,
                scan_succeeded=True,
            ),
            ContainerScanResult(
                containers=k3s_containers,
                configurations=k3s_configs,
                scan_succeeded=True,
            ),
        ]
    )

    merged_ids = {container.container_id for container in merged.containers}
    # Total stays within the backend-enforced cap...
    assert len(merged.containers) == inspect_parse_module.MAX_CONTAINERS
    # ...yet every k3s container survives even though Docker alone filled it...
    assert all(container.container_id in merged_ids for container in k3s_containers)
    # ...and k3s artifacts ride along with their accepted containers.
    assert merged.configurations == k3s_configs
    # Docker yields exactly enough slots for k3s to fit inside the shared budget.
    docker_kept = sum(1 for c in merged.containers if c.runtime == "docker")
    assert docker_kept == inspect_parse_module.MAX_CONTAINERS - k3s_count
    # Cap-truncation dropped running containers, so the merged inventory is not
    # authoritative even though both runtimes were individually complete.
    assert merged.scan_succeeded is False


def test_merge_scan_results_cap_truncation_across_runtimes_is_not_authoritative():
    """Cross-runtime cap-truncation must not report scan_succeeded=True.

    Each runtime is individually complete (scan_succeeded=True) and within the
    cap, but their combined distinct count exceeds MAX_CONTAINERS. The merge
    drops the overflow to fit the cap; reporting success would let the backend
    reap those still-running containers as stopped. Contrast a cross-runtime
    duplicate container_id, which dedupes harmlessly and stays authoritative.
    """
    docker_count = 60
    k3s_count = 10
    assert docker_count + k3s_count > inspect_parse_module.MAX_CONTAINERS
    docker_containers = [
        DiscoveredContainer(
            container_id=f"docker-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
            runtime="docker",
        )
        for index in range(docker_count)
    ]
    k3s_containers = [
        DiscoveredContainer(
            container_id=f"k3s-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
            runtime="k3s",
        )
        for index in range(k3s_count)
    ]

    merged = containers_module._merge_scan_results(
        [
            ContainerScanResult(
                containers=docker_containers,
                scan_succeeded=True,
            ),
            ContainerScanResult(
                containers=k3s_containers,
                scan_succeeded=True,
            ),
        ]
    )

    assert len(merged.containers) == inspect_parse_module.MAX_CONTAINERS
    assert merged.scan_succeeded is False


def test_merge_scan_results_dedup_only_drop_stays_authoritative():
    """Dropping cross-runtime duplicates (not cap overflow) keeps success.

    The distinct container count fits within MAX_CONTAINERS, so no running
    container is lost — only redundant copies of already-kept ids are dropped.
    A merge that only deduped must remain authoritative.
    """
    shared = [
        DiscoveredContainer(
            container_id=f"shared-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
            runtime="docker",
        )
        for index in range(inspect_parse_module.MAX_CONTAINERS)
    ]
    duplicates = [
        DiscoveredContainer(
            container_id=container.container_id,
            name=None,
            image_ref=None,
            image_digest=None,
            runtime="k3s",
        )
        for container in shared
    ]

    merged = containers_module._merge_scan_results(
        [
            ContainerScanResult(containers=shared, scan_succeeded=True),
            ContainerScanResult(containers=duplicates, scan_succeeded=True),
        ]
    )

    assert len(merged.containers) == inspect_parse_module.MAX_CONTAINERS
    assert merged.scan_succeeded is True


# ---------------------------------------------------------------------------
# Podman / nerdctl distinct-runtime discovery
# ---------------------------------------------------------------------------


def test_find_container_cli_prefers_path(monkeypatch):
    monkeypatch.setattr(
        docker_cli_module.shutil, "which", lambda binary: f"/usr/bin/{binary}"
    )

    assert docker_cli_module._find_container_cli("podman") == "/usr/bin/podman"


def test_find_container_cli_checks_darwin_homebrew_fallbacks(monkeypatch):
    monkeypatch.setattr(docker_cli_module.shutil, "which", lambda _: None)
    monkeypatch.setattr(docker_cli_module.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        docker_cli_module.Path,
        "is_file",
        lambda path: str(path) == "/opt/homebrew/bin/nerdctl",
    )
    monkeypatch.setattr(
        docker_cli_module.os,
        "access",
        lambda path, mode: str(path) == "/opt/homebrew/bin/nerdctl",
    )

    assert docker_cli_module._find_container_cli("nerdctl") == (
        "/opt/homebrew/bin/nerdctl"
    )


def test_find_container_cli_absent(monkeypatch):
    monkeypatch.setattr(docker_cli_module.shutil, "which", lambda _: None)
    monkeypatch.setattr(docker_cli_module.platform, "system", lambda: "Linux")

    assert docker_cli_module._find_container_cli("podman") is None


def _runtime_ps_row(container_id: str) -> str:
    return json.dumps({"ID": container_id})


def _runtime_inspect_output(container_id: str) -> str:
    row = _inspect_row(working_dir="")
    row["Id"] = container_id
    return json.dumps([row])


def test_scan_discovers_podman_containers_with_runtime_label(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: None)
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)
    monkeypatch.setattr(
        containers_module,
        "_find_container_cli",
        lambda binary: "/usr/bin/podman" if binary == "podman" else None,
    )

    def fake_run_text(cmd, **kwargs):
        del kwargs
        assert cmd[0] == "/usr/bin/podman"
        if cmd[1] == "ps":
            if "-a" in cmd:
                return ""
            return _runtime_ps_row("podman-1")
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return _runtime_inspect_output("podman-1")

    def fake_run_bounded_lines(cmd, **kwargs):
        del kwargs
        assert cmd[0] == "/usr/bin/podman"
        assert cmd[1:3] == ["image", "ls"]
        return {"text": "", "truncation_reason": None}

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(
        docker_cli_module, "_run_bounded_utf8_lines", fake_run_bounded_lines
    )

    result = scan_running_containers(clients=[])

    assert [container.container_id for container in result.containers] == ["podman-1"]
    assert result.containers[0].runtime == "podman"
    assert result.containers[0].to_api_payload()["runtime"] == "podman"
    assert result.scan_succeeded is True
    assert result.stopped_containers_succeeded is True
    assert result.container_images_succeeded is True


def test_scan_merges_coexisting_docker_and_podman(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)
    monkeypatch.setattr(
        containers_module,
        "_find_container_cli",
        lambda binary: "/usr/bin/podman" if binary == "podman" else None,
    )
    ids_by_binary = {"/docker": "docker-1", "/usr/bin/podman": "podman-1"}
    images_by_binary = {
        "/docker": "ghcr.io/example/docker-image",
        "/usr/bin/podman": "ghcr.io/example/podman-image",
    }

    def fake_run_text(cmd, **kwargs):
        del kwargs
        container_id = ids_by_binary[cmd[0]]
        if cmd[1] == "ps":
            if "-a" in cmd:
                return ""
            return _runtime_ps_row(container_id)
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return _runtime_inspect_output(container_id)

    def fake_run_bounded_lines(cmd, **kwargs):
        del kwargs
        assert cmd[1:3] == ["image", "ls"]
        return {
            "text": json.dumps(
                {
                    "Repository": images_by_binary[cmd[0]],
                    "Tag": "latest",
                    "Digest": "sha256:" + "a" * 64,
                    "ID": "sha256:" + "b" * 64,
                }
            ),
            "truncation_reason": None,
        }

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(
        docker_cli_module, "_run_bounded_utf8_lines", fake_run_bounded_lines
    )

    result = scan_running_containers(clients=[])

    assert {
        (container.container_id, container.runtime) for container in result.containers
    } == {("docker-1", "docker"), ("podman-1", "podman")}
    assert result.scan_succeeded is True
    assert {image.repository for image in result.container_images} == {
        "ghcr.io/example/docker-image",
        "ghcr.io/example/podman-image",
    }
    assert result.container_images_succeeded is True
    assert result.stopped_containers_succeeded is True


def test_scan_freezes_reaping_when_podman_present_but_discovery_fails(monkeypatch):
    monkeypatch.setattr(containers_module, "_find_docker_cli", lambda: "/docker")
    monkeypatch.setattr(containers_module, "find_docker_socket", lambda: None)
    monkeypatch.setattr(
        containers_module,
        "_find_container_cli",
        lambda binary: "/usr/bin/podman" if binary == "podman" else None,
    )

    def fake_run_text(cmd, **kwargs):
        del kwargs
        if cmd[0] == "/usr/bin/podman":
            return None  # podman present but every invocation fails
        if cmd[1] == "ps":
            if "-a" in cmd:
                return ""
            return _runtime_ps_row("docker-1")
        if cmd[1:3] == ["image", "inspect"]:
            return "[]"
        return _runtime_inspect_output("docker-1")

    def fake_run_bounded_lines(cmd, **kwargs):
        del kwargs
        if cmd[0] == "/usr/bin/podman":
            return None
        return {"text": "", "truncation_reason": None}

    monkeypatch.setattr(docker_cli_module, "_run_text", fake_run_text)
    monkeypatch.setattr(
        docker_cli_module, "_run_bounded_utf8_lines", fake_run_bounded_lines
    )

    result = scan_running_containers(clients=[])

    assert [container.container_id for container in result.containers] == ["docker-1"]
    assert result.scan_succeeded is False
    assert result.stopped_containers_succeeded is False
    assert result.container_images_succeeded is False


def test_merge_inventory_results_combines_and_caps():
    docker_inventory = containers_module.DockerInventoryResult(
        container_images=[
            inspect_parse_module.DiscoveredContainerImage(
                repository=f"docker/image-{index}", tag="latest", digest=None
            )
            for index in range(inspect_parse_module.MAX_CONTAINER_IMAGES)
        ],
        stopped_containers_succeeded=True,
        container_images_succeeded=True,
    )
    podman_inventory = containers_module.DockerInventoryResult(
        container_images=[
            inspect_parse_module.DiscoveredContainerImage(
                repository="podman/image", tag="latest", digest=None
            )
        ],
        stopped_containers_succeeded=True,
        container_images_succeeded=True,
    )

    merged = containers_module._merge_inventory_results(
        [docker_inventory, podman_inventory]
    )

    assert len(merged.container_images) == inspect_parse_module.MAX_CONTAINER_IMAGES
    assert merged.container_images_truncated is True
    assert merged.container_images_succeeded is True
    assert merged.stopped_containers_succeeded is True


def test_merge_inventory_results_stopped_overflow_still_submits_capped_list():
    """Cross-runtime stopped-container overflow keeps success (capped list ships).

    Stopped inventory has no reap-on-absence on the backend, so a capped list
    is strictly better than none. Demoting stopped_containers_succeeded would
    make service.py omit stopped_containers from the wire payload entirely —
    losing all detections instead of just the overflow. This mirrors the
    single-runtime path, which submits a truncated stopped discovery as
    succeeded with only a warning.
    """

    def stopped_container(runtime: str, index: int) -> DiscoveredContainer:
        return DiscoveredContainer(
            container_id=f"{runtime}-stopped-{index}",
            name=None,
            image_ref=None,
            image_digest=None,
            runtime=runtime,
            is_running=False,
        )

    docker_inventory = containers_module.DockerInventoryResult(
        stopped_containers=[
            stopped_container("docker", index)
            for index in range(inspect_parse_module.MAX_CONTAINERS)
        ],
        stopped_containers_succeeded=True,
        container_images_succeeded=True,
    )
    podman_inventory = containers_module.DockerInventoryResult(
        stopped_containers=[stopped_container("podman", 0)],
        stopped_containers_succeeded=True,
        container_images_succeeded=True,
    )

    merged = containers_module._merge_inventory_results(
        [docker_inventory, podman_inventory]
    )

    assert len(merged.stopped_containers) == inspect_parse_module.MAX_CONTAINERS
    assert merged.stopped_containers_succeeded is True


def test_merge_inventory_results_failure_is_not_masked():
    succeeded = containers_module.DockerInventoryResult(
        stopped_containers_succeeded=True,
        container_images_succeeded=True,
    )
    failed = containers_module.DockerInventoryResult()

    merged = containers_module._merge_inventory_results([succeeded, failed])

    assert merged.stopped_containers_succeeded is False
    assert merged.container_images_succeeded is False


def test_merge_inventory_results_empty_matches_absent_runtimes():
    merged = containers_module._merge_inventory_results([])

    assert merged.stopped_containers == []
    assert merged.container_images == []
    assert merged.stopped_containers_succeeded is False
    assert merged.container_images_succeeded is False


def test_run_with_sink_closes_stdout_on_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The PIPE read-end is closed deterministically on the happy path — not
    left to Popen GC, which leaks one fd per subprocess for the scan's life."""
    spawned: list[subprocess.Popen[bytes]] = []
    real_popen = subprocess.Popen

    def recording_popen(*args: object, **kwargs: object) -> subprocess.Popen[bytes]:
        process = real_popen(*args, **kwargs)  # type: ignore[arg-type,call-overload]
        spawned.append(process)
        return process

    monkeypatch.setattr(docker_cli_module.subprocess, "Popen", recording_popen)

    output = docker_cli_module._run_bytes(
        [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'ok')"],
        timeout=30,
        max_output=1024,
    )

    assert output == b"ok"
    (process,) = spawned
    assert process.stdout is not None
    assert process.stdout.closed
