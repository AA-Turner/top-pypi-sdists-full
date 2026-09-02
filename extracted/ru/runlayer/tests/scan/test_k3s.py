"""Tests for k3s CRI discovery and procfs artifact reads."""

from __future__ import annotations

import json
import time
from pathlib import Path

import structlog

from runlayer_cli.scan.containers import collect as containers_module
from runlayer_cli.scan.containers import k3s_cli as k3s_module
from runlayer_cli.scan.containers import proc_walk as proc_walk_module
from runlayer_cli.scan.containers.inspect_parse import (
    MAX_CONTAINERS,
    ContainerScanResult,
    DiscoveredContainer,
)
from runlayer_cli.scan.containers.tar_walk import _extract_copied_file


def _ps_row(
    container_id: str,
    *,
    namespace: str = "default",
    name: str | None = "app",
    state: object = "CONTAINER_RUNNING",
) -> dict[str, object]:
    labels = {
        "io.kubernetes.pod.name": "app-pod",
        "io.kubernetes.pod.namespace": namespace,
    }
    if name is not None:
        labels["io.kubernetes.container.name"] = name
    return {
        "id": container_id,
        "state": state,
        "labels": labels,
    }


def _inspect_payload(
    container_id: str,
    *,
    pid: object = 4242,
    state: object = "CONTAINER_RUNNING",
) -> dict[str, object]:
    return {
        "status": {
            "id": container_id,
            "metadata": {"name": "api"},
            "state": state,
            "image": {"image": "ghcr.io/acme/api:latest"},
            "imageRef": f"ghcr.io/acme/api@sha256:{'a' * 64}",
            "labels": {
                "io.kubernetes.container.name": "api",
                "io.kubernetes.pod.namespace": "engineering",
                "safe": "value",
            },
            "annotations": {"io.kubernetes.pod.name": "api-7f9"},
            "mounts": [
                {
                    "hostPath": "/home/alex/project",
                    "containerPath": "/workspace",
                }
            ],
        },
        "info": {
            "pid": pid,
            "config": {
                "envs": [
                    {"key": "HOME", "value": "/home/app"},
                    {"key": "TOKEN", "value": "secret"},
                ],
                "working_dir": "/workspace",
            },
            "runtimeSpec": {
                "process": {
                    "cwd": "/runtime-fallback",
                    "env": ["HOME=/runtime-home"],
                }
            },
        },
    }


def _container(
    container_id: str,
    *,
    runtime: str = "k3s",
    image_id: str | None = None,
    pid: int | None = None,
) -> DiscoveredContainer:
    return DiscoveredContainer(
        container_id=container_id,
        name="app",
        image_ref="ghcr.io/acme/app:latest",
        image_digest=None,
        runtime=runtime,
        image_id=image_id,
        pid=pid,
    )


def _fake_proc_root(
    tmp_path: Path,
    pid: int = 4242,
    *,
    container_id: str | None = None,
) -> tuple[Path, Path]:
    proc_root = tmp_path / "proc"
    container_root = proc_root / str(pid) / "root"
    container_root.mkdir(parents=True)
    if container_id is not None:
        _write_proc_cgroup(proc_root, pid, container_id)
    return proc_root, container_root


def _write_proc_cgroup(proc_root: Path, pid: int, container_id: str) -> None:
    (proc_root / str(pid) / "cgroup").write_text(
        f"0::/kubepods/besteffort/pod123/cri-containerd-{container_id}.scope\n"
    )


def test_k3s_discovery_is_linux_root_only(monkeypatch):
    monkeypatch.setattr(k3s_module.platform, "system", lambda: "Darwin")

    assert k3s_module._find_k3s_crictl() is None

    monkeypatch.setattr(k3s_module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(k3s_module.os, "geteuid", lambda: 1000)

    assert k3s_module._find_k3s_crictl() is None


def test_k3s_discovery_prefers_k3s_binary(monkeypatch):
    monkeypatch.setattr(k3s_module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(k3s_module.os, "geteuid", lambda: 0)
    monkeypatch.setattr(
        k3s_module.shutil,
        "which",
        lambda binary: "/opt/k3s" if binary == "k3s" else "/opt/crictl",
    )

    assert k3s_module._find_k3s_crictl() == ("/opt/k3s", "crictl")


def test_k3s_discovery_supports_standalone_crictl(monkeypatch, tmp_path):
    monkeypatch.setattr(k3s_module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(k3s_module.os, "geteuid", lambda: 0)
    monkeypatch.setattr(
        k3s_module.shutil,
        "which",
        lambda binary: "/opt/crictl" if binary == "crictl" else None,
    )
    monkeypatch.setattr(k3s_module, "K3S_CONFIG_DIR", tmp_path)
    monkeypatch.setattr(
        k3s_module,
        "K3S_FALLBACK_BINARY",
        tmp_path / "missing-k3s",
    )

    assert k3s_module._find_k3s_crictl() == (
        "/opt/crictl",
        "--runtime-endpoint",
        k3s_module.K3S_CONTAINERD_ENDPOINT,
    )


def test_parse_crictl_inventory_filters_system_and_sandbox_containers():
    payload = {
        "containers": [
            _ps_row("app"),
            _ps_row("system", namespace="kube-system"),
            _ps_row("sandbox", name=None),
            _ps_row("stopped", state="CONTAINER_EXITED"),
        ]
    }

    parsed = k3s_module._parse_crictl_ps_inventory(
        json.dumps(payload),
        include_kube_system=False,
    )

    assert parsed == {
        "container_ids": ["app"],
        "truncated": False,
        "malformed": False,
        "output_empty": False,
    }


def test_parse_crictl_inventory_env_can_include_system_namespaces(
    monkeypatch,
):
    monkeypatch.setenv(k3s_module.INCLUDE_KUBE_SYSTEM_ENV, "true")
    payload = {"containers": [_ps_row("system", namespace="kube-system")]}

    parsed = k3s_module._parse_crictl_ps_inventory(json.dumps(payload))

    assert parsed["container_ids"] == ["system"]


def test_parse_crictl_inventory_tracks_malformed_and_truncated_rows():
    rows = [_ps_row(f"container-{index}") for index in range(MAX_CONTAINERS + 1)]
    rows.insert(0, _ps_row(""))
    payload = {"containers": rows}

    parsed = k3s_module._parse_crictl_ps_inventory(
        json.dumps(payload),
        include_kube_system=False,
    )

    assert len(parsed["container_ids"]) == MAX_CONTAINERS
    assert parsed["malformed"] is True
    assert parsed["truncated"] is True


def test_crictl_discovery_uses_bounded_json_command(monkeypatch):
    calls: list[tuple[list[str], float, int]] = []

    def _run_text(cmd, *, timeout, max_output):
        calls.append((cmd, timeout, max_output))
        return json.dumps({"containers": [_ps_row("app")]})

    monkeypatch.setattr(k3s_module, "_run_text", _run_text)

    result = k3s_module._discover_container_ids(
        crictl=("/opt/k3s", "crictl"),
        deadline=time.monotonic() + 10,
        subprocess_timeout=2,
    )

    assert result is not None
    assert result["container_ids"] == ["app"]
    assert calls[0][0] == ["/opt/k3s", "crictl", "ps", "-o", "json"]
    assert 0 < calls[0][1] <= 2
    assert calls[0][2] == k3s_module.MAX_PS_BYTES


def test_parse_crictl_inspect_normalizes_container_context():
    container = k3s_module._parse_crictl_inspect(
        json.dumps(_inspect_payload("container-1")),
        host_home=Path("/home/alex"),
    )

    assert container is not None
    assert container.container_id == "container-1"
    assert container.name == "api"
    assert container.runtime == "k3s"
    assert container.pid == 4242
    assert container.image_ref == "ghcr.io/acme/api:latest"
    assert container.image_digest == f"sha256:{'a' * 64}"
    assert container.home == "/home/app"
    assert container.working_dir == "/workspace"
    assert container.environment["TOKEN"] == "secret"
    assert container.labels == {
        "io.kubernetes.pod.name": "api-7f9",
        "io.kubernetes.pod.namespace": "engineering",
        "io.kubernetes.container.name": "api",
        "safe": "value",
    }
    assert container.mounts_host_home is True
    assert container.to_api_payload()["runtime"] == "k3s"
    assert "pid" not in container.to_api_payload()


def test_parse_crictl_inspect_skips_missing_pid_and_stopped_container():
    assert (
        k3s_module._parse_crictl_inspect(
            json.dumps(_inspect_payload("missing", pid=None)),
            host_home=Path("/home/alex"),
        )
        is None
    )
    assert (
        k3s_module._parse_crictl_inspect(
            json.dumps(_inspect_payload("stopped", state="CONTAINER_EXITED")),
            host_home=Path("/home/alex"),
        )
        is None
    )


def test_crictl_inspects_each_container_individually(monkeypatch):
    commands: list[list[str]] = []

    def _run_text(cmd, *, timeout, max_output):
        del timeout, max_output
        commands.append(cmd)
        return json.dumps(_inspect_payload(cmd[-1]))

    monkeypatch.setattr(k3s_module, "_run_text", _run_text)

    containers = k3s_module._inspect_containers(
        crictl=("/opt/k3s", "crictl"),
        container_ids=["one", "two"],
        deadline=time.monotonic() + 10,
        subprocess_timeout=2,
        host_home=Path("/home/alex"),
    )

    assert containers is not None
    assert [container.container_id for container in containers] == ["one", "two"]
    assert commands == [
        ["/opt/k3s", "crictl", "inspect", "-o", "json", "one"],
        ["/opt/k3s", "crictl", "inspect", "-o", "json", "two"],
    ]


def test_crictl_inspect_drops_id_mismatch_row_without_discarding_others(monkeypatch):
    """A CRI id mismatch drops only that row, mirroring a failed parse.

    crictl inspect can echo a different container's status.id (prefix reuse, a
    race, or a crictl bug). That single anomalous row must be dropped like a
    parse failure rather than returning None for the whole runtime, which would
    discard every already-inspected container and collapse the k3s scan to empty.
    """

    def _run_text(cmd, *, timeout, max_output):
        del timeout, max_output
        requested = cmd[-1]
        # Inspecting "two" comes back describing an unrelated container id.
        returned = "other" if requested == "two" else requested
        return json.dumps(_inspect_payload(returned))

    monkeypatch.setattr(k3s_module, "_run_text", _run_text)

    containers = k3s_module._inspect_containers(
        crictl=("/opt/k3s", "crictl"),
        container_ids=["one", "two"],
        deadline=time.monotonic() + 10,
        subprocess_timeout=2,
        host_home=Path("/home/alex"),
    )

    assert containers is not None
    assert [container.container_id for container in containers] == ["one"]


def test_crictl_image_digest_enrichment_is_cached(monkeypatch):
    calls: list[list[str]] = []
    digest = f"sha256:{'b' * 64}"

    def _run_text(cmd, *, timeout, max_output):
        del timeout, max_output
        calls.append(cmd)
        return json.dumps({"status": {"repoDigests": [f"ghcr.io/acme/app@{digest}"]}})

    monkeypatch.setattr(k3s_module, "_run_text", _run_text)
    containers = [
        _container("one", image_id="sha256:image"),
        _container("two", image_id="sha256:image"),
    ]

    enriched = k3s_module._collect_image_digests(
        crictl=("/opt/k3s", "crictl"),
        containers=containers,
        deadline=time.monotonic() + 10,
        subprocess_timeout=2,
    )

    assert [container.image_digest for container in enriched] == [digest, digest]
    assert calls == [
        [
            "/opt/k3s",
            "crictl",
            "inspecti",
            "-o",
            "json",
            "sha256:image",
        ]
    ]


def test_proc_file_read_is_tar_compatible(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    config = container_root / "home/app/.cursor/mcp.json"
    config.parent.mkdir(parents=True)
    config.write_bytes(b'{"mcpServers": {}}')

    archive = proc_walk_module._copy_proc_file_archive(
        proc_root=proc_root,
        pid=4242,
        path="/home/app/.cursor/mcp.json",
        deadline=time.monotonic() + 10,
    )

    assert archive is not None
    assert _extract_copied_file(archive) == b'{"mcpServers": {}}'


def test_proc_file_read_rejects_traversal_and_final_symlink(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside"
    outside.write_text("secret")
    (workspace / "link").symlink_to(outside)

    assert (
        proc_walk_module._read_proc_file(
            proc_root=proc_root,
            pid=4242,
            path="/workspace/../outside",
            deadline=time.monotonic() + 10,
        )
        is None
    )
    assert (
        proc_walk_module._read_proc_file(
            proc_root=proc_root,
            pid=4242,
            path="/workspace/link",
            deadline=time.monotonic() + 10,
        )
        is None
    )


def test_proc_tree_walk_filters_skipped_directories_with_allow_override(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    files = {
        "workspace/good/mcp.json": b"good",
        "workspace/node_modules/blocked/mcp.json": b"blocked",
        "workspace/node_modules/allowed/mcp.json": b"allowed",
    }
    for relative, content in files.items():
        path = container_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    walked = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda path: path.endswith(".json"),
        deadline=time.monotonic() + 10,
    )
    allowed = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda path: path.endswith(".json"),
        allow_file_in_skipped_directory=lambda path: "/allowed/" in path,
        deadline=time.monotonic() + 10,
    )

    assert walked.files == {"/workspace/good/mcp.json": b"good"}
    assert allowed.files == {
        "/workspace/good/mcp.json": b"good",
        "/workspace/node_modules/allowed/mcp.json": b"allowed",
    }


def test_proc_tree_walk_reserves_allowed_match_after_regular_cap(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "noise.dat").write_bytes(b"noise")
    package = workspace / "node_modules" / "agent" / "package.json"
    package.parent.mkdir(parents=True)
    package.write_bytes(b'{"name":"agent"}')
    package_path = "/workspace/node_modules/agent/package.json"

    walked = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        allow_file_in_skipped_directory=lambda path: path == package_path,
        deadline=time.monotonic() + 10,
        max_matched_files=1,
    )

    assert walked.files == {
        "/workspace/noise.dat": b"noise",
        package_path: b'{"name":"agent"}',
    }
    assert walked.truncated is False


def test_proc_tree_walk_evicts_regular_match_for_allowed_bytes(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "noise.dat").write_bytes(b"noise")
    package = workspace / "node_modules" / "agent" / "package.json"
    package.parent.mkdir(parents=True)
    package.write_bytes(b"agent")
    package_path = "/workspace/node_modules/agent/package.json"

    walked = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        allow_file_in_skipped_directory=lambda path: path == package_path,
        deadline=time.monotonic() + 10,
        max_total_bytes=5,
    )

    assert walked.files == {package_path: b"agent"}
    assert walked.truncated is True


def test_proc_tree_walk_enforces_file_byte_and_deadline_caps(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "a.json").write_bytes(b"aa")
    (workspace / "b.json").write_bytes(b"bb")

    file_capped = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
        max_matched_files=1,
    )
    byte_capped = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
        max_total_bytes=2,
    )
    deadline_capped = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() - 1,
    )

    assert file_capped.files == {"/workspace/a.json": b"aa"}
    assert file_capped.truncated is True
    assert byte_capped.files == {"/workspace/a.json": b"aa"}
    assert byte_capped.truncated is True
    assert deadline_capped.files == {}
    assert deadline_capped.truncated is True


def test_proc_tree_walk_caps_directory_entry_fanout(monkeypatch, tmp_path):
    # A single directory on a live (possibly adversarial) container rootfs can
    # list an unbounded number of entries. The per-directory work below the
    # top-of-loop deadline check — directory_names.sort() + a per-subdir
    # is_symlink() lstat + sorted(file_names) — runs with no interleaved
    # deadline check, so a pathological fanout could burn the whole wall-clock
    # budget inside one os.walk step (tar_walk has no analogue: its byte cap
    # already bounds total work). The breadth cap must be enforced *before* that
    # work, so an over-cap directory is neither lstat-stormed nor scanned; it is
    # marked truncated instead.
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    for index in range(200):
        (workspace / f"dir-{index:03d}").mkdir()
    (workspace / "mcp.json").write_bytes(b"{}")

    lstat_calls = 0
    original_lstat = proc_walk_module.os.lstat

    def _counting_lstat(path):
        nonlocal lstat_calls
        lstat_calls += 1
        return original_lstat(path)

    monkeypatch.setattr(proc_walk_module.os, "lstat", _counting_lstat)

    over_cap = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
        max_dir_entries=3,
    )

    assert over_cap.truncated is True
    assert over_cap.files == {}
    # Short-circuited before the per-subdir lstat storm and the file scan.
    assert lstat_calls == 0

    under_cap = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda path: path.endswith(".json"),
        deadline=time.monotonic() + 10,
        max_dir_entries=1000,
    )

    assert under_cap.files == {"/workspace/mcp.json": b"{}"}
    assert under_cap.truncated is False


def test_proc_tree_walk_handles_missing_pid_and_exit_race(
    monkeypatch,
    tmp_path,
):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    raced_file = workspace / "mcp.json"
    raced_file.write_bytes(b"{}")

    missing = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=9999,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
    )
    original_lstat = proc_walk_module.os.lstat

    def _racing_lstat(path):
        if Path(path) == raced_file:
            raise FileNotFoundError
        return original_lstat(path)

    monkeypatch.setattr(proc_walk_module.os, "lstat", _racing_lstat)
    raced = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
    )

    assert missing == proc_walk_module._TarWalkResult()
    assert raced.files == {}
    assert raced.truncated is True


def test_proc_tree_walk_does_not_follow_directory_symlinks(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.json").write_bytes(b"secret")
    (workspace / "linked").symlink_to(outside, target_is_directory=True)

    walked = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
    )

    assert walked.files == {}


def test_proc_tree_walk_does_not_count_symlinks_against_matched_cap(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    # File symlinks matching wanted_file must not consume the matched-file cap;
    # only the regular file should, mirroring tar_walk._walk_tar_stream.
    (workspace / "aaa.json").symlink_to("/nonexistent-a")
    (workspace / "bbb.json").symlink_to("/nonexistent-b")
    (workspace / "zzz-real.json").write_bytes(b"real")

    walked = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda path: path.endswith(".json"),
        deadline=time.monotonic() + 10,
        max_matched_files=1,
    )

    assert walked.files == {"/workspace/zzz-real.json": b"real"}
    assert walked.truncated is False


def test_proc_tree_walk_logs_unexpected_error_type(tmp_path):
    # An unexpected bug must surface as a warning, not be silently swallowed as
    # "truncated" — parity with tar_walk._walk_tar_stream.
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "mcp.json").write_bytes(b"{}")

    def raising_wanted_file(_path: str) -> bool:
        raise KeyError("boom")

    with structlog.testing.capture_logs() as logs:
        walked = proc_walk_module._walk_proc_tree(
            proc_root=proc_root,
            pid=4242,
            root_path="/workspace",
            wanted_file=raising_wanted_file,
            deadline=time.monotonic() + 10,
        )

    assert walked.files == {}
    assert walked.truncated is True
    unexpected = [
        entry
        for entry in logs
        if entry["event"] == "Unexpected error walking container proc tree"
    ]
    assert unexpected == [
        {
            "event": "Unexpected error walking container proc tree",
            "log_level": "warning",
            "error_type": "KeyError",
        }
    ]


def test_proc_tree_walk_treats_expected_error_as_truncated_without_logging(tmp_path):
    # Expected filesystem/path errors (here ValueError) stay silent so live
    # container churn does not spam warnings — again mirroring tar_walk.
    proc_root, container_root = _fake_proc_root(tmp_path)
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "mcp.json").write_bytes(b"{}")

    def raising_wanted_file(_path: str) -> bool:
        raise ValueError("expected")

    with structlog.testing.capture_logs() as logs:
        walked = proc_walk_module._walk_proc_tree(
            proc_root=proc_root,
            pid=4242,
            root_path="/workspace",
            wanted_file=raising_wanted_file,
            deadline=time.monotonic() + 10,
        )

    assert walked.files == {}
    assert walked.truncated is True
    assert logs == []


def test_k3s_collector_uses_inspected_pid_for_proc_reads(
    monkeypatch,
    tmp_path,
):
    proc_root, container_root = _fake_proc_root(tmp_path, container_id="container-1")
    config = container_root / "root/.cursor/mcp.json"
    config.parent.mkdir(parents=True)
    config.write_bytes(b"{}")
    discovered = _container("container-1", pid=4242)
    monkeypatch.setattr(
        containers_module,
        "_inspect_k3s_containers",
        lambda **_kwargs: [discovered],
    )
    collector = containers_module.K3sCrictlCollector(
        ("/opt/k3s", "crictl"),
        operation_timeout=2,
        proc_root=proc_root,
    )

    assert collector.inspect_containers(
        container_ids=["container-1"],
        deadline=time.monotonic() + 10,
        host_home=Path("/home/alex"),
    ) == [discovered]
    archive = collector.copy_file_archive(
        container=discovered,
        path="/root/.cursor/mcp.json",
        deadline=time.monotonic() + 10,
    )

    assert archive is not None
    assert _extract_copied_file(archive) == b"{}"


def test_pid_matches_container_guards_recycled_and_exited_pids(tmp_path):
    proc_root = tmp_path / "proc"
    (proc_root / "4242").mkdir(parents=True)
    _write_proc_cgroup(proc_root, 4242, "longcontainerid99")
    matches = proc_walk_module._pid_matches_container

    assert matches(proc_root=proc_root, pid=4242, container_id="longcontainerid99")
    # Recycled pid: a different (host) process's cgroup lacks the container id.
    assert not matches(proc_root=proc_root, pid=4242, container_id="othercontainer42")
    # Exited container: no cgroup file -> fail-closed.
    assert not matches(proc_root=proc_root, pid=1, container_id="longcontainerid99")
    # Too-short id -> substring match is not trustworthy -> fail-closed.
    assert not matches(proc_root=proc_root, pid=4242, container_id="abc")


def test_proc_read_refuses_when_cgroup_identity_mismatches(tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path, container_id="containerabc12")
    config = container_root / "root/.cursor/mcp.json"
    config.parent.mkdir(parents=True)
    config.write_bytes(b"{}")

    assert (
        proc_walk_module._read_proc_file(
            proc_root=proc_root,
            pid=4242,
            path="/root/.cursor/mcp.json",
            deadline=time.monotonic() + 10,
            container_id="containerabc12",
        )
        == b"{}"
    )
    assert (
        proc_walk_module._read_proc_file(
            proc_root=proc_root,
            pid=4242,
            path="/root/.cursor/mcp.json",
            deadline=time.monotonic() + 10,
            container_id="recycledhostxyz",
        )
        is None
    )


def test_proc_tree_walk_revalidates_identity_per_matched_file(monkeypatch, tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path, container_id="containerabc12")
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "mcp.json").write_bytes(b"{}")

    calls = {"count": 0}

    def _pid_matches_once(**_kwargs):
        calls["count"] += 1
        # Pre-traversal check passes; the per-matched-file read sees a recycle.
        return calls["count"] == 1

    monkeypatch.setattr(
        proc_walk_module,
        "_pid_matches_container",
        _pid_matches_once,
    )
    walked = proc_walk_module._walk_proc_tree(
        proc_root=proc_root,
        pid=4242,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
        container_id="containerabc12",
    )

    assert walked.files == {}
    assert walked.truncated is True
    assert calls["count"] >= 2


def test_k3s_collector_skips_reads_when_pid_recycled(monkeypatch, tmp_path):
    proc_root, container_root = _fake_proc_root(tmp_path)
    (proc_root / "4242" / "cgroup").write_text("0::/system.slice/sshd.service\n")
    config = container_root / "root/.cursor/mcp.json"
    config.parent.mkdir(parents=True)
    config.write_bytes(b"{}")
    workspace = container_root / "workspace"
    workspace.mkdir()
    (workspace / "mcp.json").write_bytes(b"{}")
    discovered = _container("container-1", pid=4242)
    monkeypatch.setattr(
        containers_module,
        "_inspect_k3s_containers",
        lambda **_kwargs: [discovered],
    )
    collector = containers_module.K3sCrictlCollector(
        ("/opt/k3s", "crictl"),
        operation_timeout=2,
        proc_root=proc_root,
    )
    collector.inspect_containers(
        container_ids=["container-1"],
        deadline=time.monotonic() + 10,
        host_home=Path("/home/alex"),
    )

    archive = collector.copy_file_archive(
        container=discovered,
        path="/root/.cursor/mcp.json",
        deadline=time.monotonic() + 10,
    )
    walked = collector.copy_tree(
        container=discovered,
        root_path="/workspace",
        wanted_file=lambda _path: True,
        deadline=time.monotonic() + 10,
    )

    assert archive is None
    assert walked.files == {}


def test_scan_runs_k3s_alongside_first_working_docker_transport(monkeypatch):
    docker_collector = object()
    k3s_collector = object()
    calls: list[object] = []
    monkeypatch.setattr(
        containers_module,
        "_iter_available_docker_collectors",
        lambda **_kwargs: iter([docker_collector]),
    )
    monkeypatch.setattr(
        containers_module,
        "_iter_available_k3s_collectors",
        lambda **_kwargs: iter([k3s_collector]),
    )

    def _scan_with_collector(*, collector, **_kwargs):
        calls.append(collector)
        runtime = "docker" if collector is docker_collector else "k3s"
        return ContainerScanResult(
            containers=[_container(runtime, runtime=runtime)],
            scan_succeeded=True,
        )

    monkeypatch.setattr(
        containers_module,
        "_scan_with_collector",
        _scan_with_collector,
    )

    result = containers_module._scan_running_containers(
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    assert calls == [docker_collector, k3s_collector]
    assert [container.runtime for container in result.containers] == [
        "docker",
        "k3s",
    ]
    assert result.scan_succeeded is True


def test_scan_freezes_reaping_when_k3s_present_but_discovery_fails(monkeypatch):
    """A present-but-unscannable k3s runtime must not leave scan_succeeded True.

    k3s discovery returning None (transient crictl timeout / subprocess error /
    deadline) makes ``_scan_with_collector`` return None. Dropping that runtime
    from the merge would report the Docker-only inventory as authoritative, and
    the backend reaps any previously-seen k3s container absent from a successful
    scan. Docker artifacts are still collected, but the merge must freeze reaping
    (scan_succeeded=False) rather than reap the still-running k3s containers.
    """
    docker_collector = object()
    k3s_collector = object()
    monkeypatch.setattr(
        containers_module,
        "_iter_available_docker_collectors",
        lambda **_kwargs: iter([docker_collector]),
    )
    monkeypatch.setattr(
        containers_module,
        "_iter_available_k3s_collectors",
        lambda **_kwargs: iter([k3s_collector]),
    )

    def _scan_with_collector(*, collector, **_kwargs):
        if collector is docker_collector:
            return ContainerScanResult(
                containers=[_container("docker-1", runtime="docker")],
                scan_succeeded=True,
            )
        return None  # k3s present but discovery failed

    monkeypatch.setattr(
        containers_module,
        "_scan_with_collector",
        _scan_with_collector,
    )

    result = containers_module._scan_running_containers(
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    assert [container.container_id for container in result.containers] == ["docker-1"]
    assert result.scan_succeeded is False


def test_scan_freezes_reaping_when_docker_present_but_all_transports_fail(monkeypatch):
    """Every Docker transport failing must not let a k3s-only scan reap Docker.

    Both Docker transports (CLI then socket) returning None means Docker is
    present but unscannable — symmetric to the k3s discovery-failure case. A
    k3s-only inventory reported scan_succeeded=True would let the backend reap
    previously-seen Docker containers, so the merge must freeze reaping.
    """
    docker_cli = object()
    docker_socket = object()
    k3s_collector = object()
    seen: list[object] = []
    monkeypatch.setattr(
        containers_module,
        "_iter_available_docker_collectors",
        lambda **_kwargs: iter([docker_cli, docker_socket]),
    )
    monkeypatch.setattr(
        containers_module,
        "_iter_available_k3s_collectors",
        lambda **_kwargs: iter([k3s_collector]),
    )

    def _scan_with_collector(*, collector, **_kwargs):
        seen.append(collector)
        if collector is k3s_collector:
            return ContainerScanResult(
                containers=[_container("k3s-1", runtime="k3s")],
                scan_succeeded=True,
            )
        return None  # both Docker transports fail discovery

    monkeypatch.setattr(
        containers_module,
        "_scan_with_collector",
        _scan_with_collector,
    )

    result = containers_module._scan_running_containers(
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    # The socket transport is still tried after the CLI fails before Docker is
    # marked present-but-unscannable.
    assert seen == [docker_cli, docker_socket, k3s_collector]
    assert [container.container_id for container in result.containers] == ["k3s-1"]
    assert result.scan_succeeded is False


def test_scan_stays_authoritative_when_a_runtime_is_absent(monkeypatch):
    """An absent runtime (no collector available) must not freeze reaping.

    Present-but-unscannable and absent are different: only the former freezes
    reaping. With no k3s collector yielded, a successful Docker scan stays
    authoritative so the backend can still reap genuinely stopped containers.
    """
    docker_collector = object()
    monkeypatch.setattr(
        containers_module,
        "_iter_available_docker_collectors",
        lambda **_kwargs: iter([docker_collector]),
    )
    monkeypatch.setattr(
        containers_module,
        "_iter_available_k3s_collectors",
        lambda **_kwargs: iter([]),
    )

    def _scan_with_collector(*, collector, **_kwargs):
        assert collector is docker_collector
        return ContainerScanResult(
            containers=[_container("docker-1", runtime="docker")],
            scan_succeeded=True,
        )

    monkeypatch.setattr(
        containers_module,
        "_scan_with_collector",
        _scan_with_collector,
    )

    result = containers_module._scan_running_containers(
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    assert [container.container_id for container in result.containers] == ["docker-1"]
    assert result.scan_succeeded is True


def _crictl_scan_run_text(*, running_ids, exited_ids, mismatch_ids=()):
    """Serve a bounded crictl ps + per-container inspect fake for one scan."""

    def _run_text(cmd, *, timeout, max_output):
        del timeout, max_output
        if "ps" in cmd:
            rows = [_ps_row(cid) for cid in (*running_ids, *exited_ids, *mismatch_ids)]
            return json.dumps({"containers": rows})
        if "inspecti" in cmd:
            return None  # image-digest enrichment is best-effort
        if "inspect" in cmd:
            container_id = cmd[-1]
            if container_id in exited_ids:
                # Raced to stopped between ps and inspect: _parse_crictl_inspect
                # returns None for a non-running container.
                return json.dumps(
                    _inspect_payload(container_id, state="CONTAINER_EXITED")
                )
            if container_id in mismatch_ids:
                # crictl echoes a different container's status.id: the row must
                # be dropped like a failed parse, not abandon the whole runtime.
                return json.dumps(_inspect_payload(f"{container_id}-mismatch"))
            return json.dumps(_inspect_payload(container_id))
        return None

    return _run_text


def test_scan_marks_partial_k3s_inventory_unsuccessful(monkeypatch, tmp_path):
    """A dropped CRI row must not leave scan_succeeded True.

    crictl ps reports two running containers; one races to stopped and fails
    to parse, so it is dropped from the inspected set. Reporting the short
    inventory as authoritative would let the backend mark the still-running
    container stopped, so scan_succeeded must be False.
    """
    monkeypatch.setattr(
        k3s_module,
        "_run_text",
        _crictl_scan_run_text(running_ids=("one",), exited_ids=("two",)),
    )
    collector = containers_module.K3sCrictlCollector(
        ("/opt/k3s", "crictl"),
        operation_timeout=2,
        proc_root=tmp_path / "proc",
    )

    result = containers_module._scan_with_collector(
        collector=collector,
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    assert result is not None
    assert [container.container_id for container in result.containers] == ["one"]
    assert result.scan_succeeded is False


def test_scan_marks_complete_k3s_inventory_successful(monkeypatch, tmp_path):
    """The full discovered set inspecting cleanly still reports success."""
    monkeypatch.setattr(
        k3s_module,
        "_run_text",
        _crictl_scan_run_text(running_ids=("one", "two"), exited_ids=()),
    )
    collector = containers_module.K3sCrictlCollector(
        ("/opt/k3s", "crictl"),
        operation_timeout=2,
        proc_root=tmp_path / "proc",
    )

    result = containers_module._scan_with_collector(
        collector=collector,
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    assert result is not None
    assert [container.container_id for container in result.containers] == ["one", "two"]
    assert result.scan_succeeded is True


def test_scan_keeps_containers_when_one_crictl_row_id_mismatches(monkeypatch, tmp_path):
    """A crictl id mismatch drops that row but preserves the rest of the scan.

    Inspecting "two" echoes a different container's status.id. That row is
    dropped like a failed parse: the earlier "one" survives and scan_succeeded
    reports False, rather than the whole k3s scan collapsing to an empty
    inventory that would let the backend reap the still-running "one".
    """
    monkeypatch.setattr(
        k3s_module,
        "_run_text",
        _crictl_scan_run_text(
            running_ids=("one",),
            exited_ids=(),
            mismatch_ids=("two",),
        ),
    )
    collector = containers_module.K3sCrictlCollector(
        ("/opt/k3s", "crictl"),
        operation_timeout=2,
        proc_root=tmp_path / "proc",
    )

    result = containers_module._scan_with_collector(
        collector=collector,
        clients=[],
        subprocess_timeout=2,
        time_budget=10,
        host_home=Path("/home/alex"),
    )

    assert result is not None
    assert [container.container_id for container in result.containers] == ["one"]
    assert result.scan_succeeded is False
