from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest

from plato.agents.runtime.transport import GitTransport, NFSTransport, RsyncTransport
from plato.v2.async_.environment import Environment
from plato.worlds.base import BaseWorld
from plato.worlds.config import GitTransportConfig, MergeAgentConfig, RunConfig, SessionConfig
from plato.worlds.models import Observation, StepResult


class _TestWorld(BaseWorld[RunConfig]):
    name = "transport-mode-test"

    async def reset(self) -> Observation:
        return Observation()

    async def step(self) -> StepResult:
        return StepResult(observation=Observation(), done=True)


class _RuntimeEnv:
    alias = "runtime"

    async def get_mesh_ip(self) -> str:
        return "10.100.0.9"


# ---------------------------------------------------------------------------
# BaseWorld integration tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_transport_stores_mesh_ip(monkeypatch):
    """_create_transport should store mesh IP without creating transport yet."""
    world = _TestWorld()
    world.config = RunConfig()
    world.session = SessionConfig(session_id="s1")
    world._ssh_key_path = Path("/tmp/test-key")
    world.plato_session = SimpleNamespace(envs=[_RuntimeEnv()])

    await world._create_transport()

    assert world._mesh_ip == "10.100.0.9"
    assert world._transport is None


@pytest.mark.asyncio
async def test_start_transport_creates_and_initializes(monkeypatch, tmp_path):
    """_start_transport should create NFSTransport from workspace paths and initialize."""
    world = _TestWorld()
    world.config = RunConfig()
    world._mesh_ip = "10.100.0.9"
    world._transport_mode = "nfs_kernel"
    world._ssh_key_path = Path("/tmp/test-key")

    # Simulate a workspace
    from plato.worlds.workspace import Workspace

    ws = Workspace(name="data", path=tmp_path / "recordings", tracked=False)
    world._workspaces = {"data": ws}

    calls: list[str] = []

    class FakeNFS(NFSTransport):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)

        async def initialize(self):
            calls.append("initialize")

        async def refresh_exports(self):
            calls.append("refresh_exports")

    monkeypatch.setattr("plato.worlds.base.NFSTransport", FakeNFS)

    async def fake_ensure_fuse_mount():
        return None

    monkeypatch.setattr(ws, "ensure_fuse_mount", fake_ensure_fuse_mount)

    await world._start_transport()

    assert world._transport is not None
    assert world._transport.path == str(tmp_path / "recordings")
    assert calls == ["initialize", "refresh_exports"]


@pytest.mark.asyncio
async def test_start_transport_noop_when_no_mesh_ip():
    """_start_transport should be a no-op when no mesh IP is set."""
    world = _TestWorld()
    await world._start_transport()


@pytest.mark.asyncio
async def test_untracked_workspace_uses_empty_manifest_fuse_mount(monkeypatch, tmp_path):
    from plato.worlds.dvc_models import DVCManifest, LazyDVCMount
    from plato.worlds.workspace import Workspace

    ws = Workspace(name="data", path=tmp_path / "recordings", tracked=False)
    ws.path.mkdir(parents=True)
    (ws.path / "file.txt").write_text("hello")

    calls = {}

    async def fake_mount_lazy(mountpoint, manifest, s3_config, cache_dir):
        calls["mountpoint"] = mountpoint
        calls["manifest"] = manifest
        calls["s3_config"] = s3_config
        calls["cache_dir"] = cache_dir
        return LazyDVCMount(mountpoint=mountpoint, cache_dir=cache_dir, manifest=manifest)

    monkeypatch.setattr("plato.worlds.lazy_dvc.mount_lazy", fake_mount_lazy)

    await ws.ensure_fuse_mount()

    assert calls["mountpoint"] == ws.path
    assert isinstance(calls["manifest"], DVCManifest)
    assert calls["manifest"].entries_list == []
    assert calls["s3_config"].bucket == ""
    assert calls["s3_config"].credentials == {}
    assert ws._lazy_mounts[ws.path.name].mountpoint == ws.path


def test_run_config_transport_mode_defaults_to_nfs_kernel():
    cfg = RunConfig()
    assert cfg.transport_mode == "nfs_kernel"


# ---------------------------------------------------------------------------
# NFSTransport.initialize tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_nfs_transport_initialize_exports_with_crossmnt(monkeypatch):
    """NFSTransport.initialize should export with crossmnt for FUSE traversal."""
    commands: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        commands.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    await t.initialize()

    # Should export /workspace independently (no crossmnt, no /srv/nfs)
    export_cmds = [c for c in commands if "/etc/exports" in c]
    assert len(export_cmds) == 1
    export_cmd = export_cmds[0]
    assert "/workspace" in export_cmd
    assert "crossmnt" not in export_cmd
    assert "fsid=0" in export_cmd
    assert "/srv/nfs" not in export_cmd

    # Should start nfs-kernel-server
    assert any("nfs-kernel-server" in cmd for cmd in commands)


@pytest.mark.asyncio
async def test_nfs_transport_initialize_raises_on_export_failure(monkeypatch):
    """initialize should raise when /etc/exports write fails."""
    call_count = 0

    async def fake_run_local(command: str, timeout: int = 60):
        nonlocal call_count
        call_count += 1
        # First call: which exportfs (success)
        # Second call: mkdir -p (success)
        # Third call: chown/chmod (success)
        # Fourth call: /etc/exports write (fail)
        if "/etc/exports" in command:
            return 1, "", "permission denied"
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    with pytest.raises(RuntimeError, match="Failed to configure NFS exports"):
        await t.initialize()


@pytest.mark.asyncio
async def test_nfs_transport_initialize_raises_on_nfsd_mount_failure(monkeypatch):
    """initialize should raise when mounting nfsd filesystem fails."""

    async def fake_run_local(command: str, timeout: int = 60):
        if "modprobe nfsd" in command:
            return 1, "", "modprobe failed"
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    with pytest.raises(RuntimeError, match="Failed to mount nfsd filesystem"):
        await t.initialize()


@pytest.mark.asyncio
async def test_nfs_transport_initialize_raises_on_server_start_failure(monkeypatch):
    """initialize should raise when nfs-kernel-server fails to start."""

    async def fake_run_local(command: str, timeout: int = 60):
        if "nfs-kernel-server" in command:
            return 1, "", "systemctl start failed"
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    with pytest.raises(RuntimeError, match="Failed to start NFS server"):
        await t.initialize()


@pytest.mark.asyncio
async def test_nfs_transport_initialize_installs_nfs_server_if_missing(monkeypatch):
    """initialize should install nfs-kernel-server if exportfs is not found."""
    commands: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        commands.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    await t.initialize()

    install_cmd = commands[0]
    assert "which exportfs" in install_cmd
    assert "nfs-kernel-server" in install_cmd


# ---------------------------------------------------------------------------
# NFSTransport.refresh_exports tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_nfs_transport_refresh_exports(monkeypatch):
    commands: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        commands.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    await t.refresh_exports()

    assert any("exportfs -ra" in cmd for cmd in commands)


@pytest.mark.asyncio
async def test_nfs_transport_refresh_exports_warns_on_failure(monkeypatch, caplog):
    """refresh_exports should warn (not raise) on failure."""

    async def fake_run_local(command: str, timeout: int = 60):
        return 1, "", "exportfs failed"

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/test-key"))
    # Should not raise
    await t.refresh_exports()


# ---------------------------------------------------------------------------
# NFSTransport.with_path tests
# ---------------------------------------------------------------------------


def test_with_path_computes_sub_mount_path():
    """with_path should derive sub mount_path when original has mount_path."""
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"), mount_path="/mnt/ws")
    sub = t.with_path("/workspace/code")
    assert sub.mount_path == "/mnt/ws/code"


def test_with_path_no_sub_mount_when_path_doesnt_start_with_parent():
    """with_path should not set sub mount when new path is unrelated."""
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"), mount_path="/mnt/ws")
    sub = t.with_path("/other/path")
    assert sub.mount_path is None


def test_with_path_preserves_world_vm_ip_and_ssh_key():
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"))
    sub = t.with_path("/workspace/sub")
    assert sub.world_vm_ip == "10.100.0.9"
    assert sub.ssh_key_path == Path("/tmp/key")


# ---------------------------------------------------------------------------
# NFSTransport.setup_agent tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_setup_agent_mounts_correct_nfs_source(monkeypatch):
    """setup_agent should mount using the correct NFS client path."""
    local_cmds: list[str] = []
    ssh_cmds: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        local_cmds.append(command)
        return 0, "", ""

    async def fake_run_ssh(key_path, hostname, command, timeout=60):
        ssh_cmds.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)
    monkeypatch.setattr("plato.agents.runtime.transport.run_ssh", fake_run_ssh)

    t = NFSTransport(
        "/workspace/recordings",
        "10.100.0.9",
        Path("/tmp/key"),
        mount_path="/workspace/recordings",
    )
    await t.setup_agent(None, "10.100.1.5")

    # All commands are combined into a single SSH call
    assert len(ssh_cmds) == 1
    combined = ssh_cmds[0]
    assert "mount -t nfs" in combined
    assert "10.100.0.9:/workspace/recordings" in combined
    assert "/workspace/recordings" in combined


@pytest.mark.asyncio
async def test_setup_agent_mounts_full_path(monkeypatch):
    """setup_agent should mount using the full server path."""
    ssh_cmds: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        return 0, "", ""

    async def fake_run_ssh(key_path, hostname, command, timeout=60):
        ssh_cmds.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)
    monkeypatch.setattr("plato.agents.runtime.transport.run_ssh", fake_run_ssh)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"))
    await t.setup_agent(None, "10.100.1.5")

    assert len(ssh_cmds) == 1
    assert "mount -t nfs" in ssh_cmds[0]
    assert "10.100.0.9:/workspace" in ssh_cmds[0]


@pytest.mark.asyncio
async def test_setup_agent_enables_read_write_audit_for_tracked_workspaces(monkeypatch):
    """Tracked workspaces should audit reads as well as writes for tool attribution."""
    ssh_cmds: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        return 0, "", ""

    async def fake_run_ssh(key_path, hostname, command, timeout=60):
        ssh_cmds.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)
    monkeypatch.setattr("plato.agents.runtime.transport.run_ssh", fake_run_ssh)

    t = NFSTransport(
        "/workspace",
        "10.100.0.9",
        Path("/tmp/key"),
    )
    t.configure_workspace(name="code", repo_root=Path("/tmp/repo"), tracked=True)
    t.configure_audit_scope(audit_run_id="run-1", audit_key="plato_scope")
    await t.setup_agent(None, "10.100.1.5")

    # Mount + audit combined into single SSH call
    assert len(ssh_cmds) == 1
    combined = ssh_cmds[0]
    assert "auditctl -a always,exit" in combined
    assert "-F perm=rwa -k plato_scope" in combined


@pytest.mark.asyncio
async def test_setup_agent_raises_on_mount_failure(monkeypatch):
    """setup_agent should raise when NFS mount fails."""

    async def fake_run_local(command: str, timeout: int = 60):
        return 0, "", ""

    async def fake_run_ssh(key_path, hostname, command, timeout=60):
        if "mount -t nfs" in command:
            return 1, "", "mount.nfs: access denied"
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)
    monkeypatch.setattr("plato.agents.runtime.transport.run_ssh", fake_run_ssh)

    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"))
    with pytest.raises(RuntimeError, match="Failed to mount NFS on agent VM"):
        await t.setup_agent(None, "10.100.1.5")


# ---------------------------------------------------------------------------
# NFSTransport.sync_back and mount_at
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sync_back_is_noop():
    """NFS sync_back should be a no-op (writes are immediate)."""
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"))
    # Should not raise
    await t.sync_back(None, "10.100.1.5")


def test_agent_mount_path_returns_mount_path_when_set():
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"), mount_path="/mnt/data")
    assert t.agent_mount_path == "/mnt/data"


def test_agent_mount_path_falls_back_to_path():
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"))
    assert t.agent_mount_path == "/workspace"


def test_mount_at_returns_copy_with_custom_mount():
    t = NFSTransport("/workspace", "10.100.0.9", Path("/tmp/key"))
    t2 = t.mount_at("/custom/mount")
    assert t2.mount_path == "/custom/mount"
    assert t2.path == "/workspace"
    assert t2 is not t


# ---------------------------------------------------------------------------
# NFSTransport.prepare tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_prepare_creates_workspace_directory(monkeypatch):
    """prepare should create the workspace directory."""
    commands: list[str] = []

    async def fake_run_local(command: str, timeout: int = 60):
        commands.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_local", fake_run_local)

    t = NFSTransport("/workspace/data", "10.100.0.9", Path("/tmp/key"))
    await t.prepare()

    assert any("mkdir -p /workspace/data" in cmd for cmd in commands)


# ---------------------------------------------------------------------------
# RsyncTransport tests
# ---------------------------------------------------------------------------


def test_rsync_transport_with_path_computes_sub_mount():
    t = RsyncTransport("/workspace", Path("/tmp/key"), mount_path="/mnt/ws")
    sub = t.with_path("/workspace/code")
    assert sub.mount_path == "/mnt/ws/code"
    assert sub.path == "/workspace/code"


def test_rsync_transport_with_path_no_sub_mount_for_unrelated():
    t = RsyncTransport("/workspace", Path("/tmp/key"), mount_path="/mnt/ws")
    sub = t.with_path("/other")
    assert sub.mount_path is None


def test_rsync_transport_agent_mount_path():
    t = RsyncTransport("/workspace", Path("/tmp/key"))
    assert t.agent_mount_path == "/workspace"

    t2 = RsyncTransport("/workspace", Path("/tmp/key"), mount_path="/mnt/data")
    assert t2.agent_mount_path == "/mnt/data"


@pytest.mark.asyncio
async def test_git_transport_resolve_and_retry_ours_force_pushes_local_head(monkeypatch):
    commands: list[str] = []

    async def fake_run_ssh(key_path, hostname, command, timeout=60):
        del key_path, hostname, timeout
        commands.append(command)
        return 0, "", ""

    monkeypatch.setattr("plato.agents.runtime.transport.run_ssh", fake_run_ssh)

    transport = GitTransport(
        "/workspace/data",
        "10.100.0.9",
        Path("/tmp/key"),
        mount_path="/workspace",
        git_config=GitTransportConfig(),
    )

    resolved = await transport._resolve_and_retry(  # pyright: ignore[reportPrivateUsage]
        cast(Environment, object()),
        "10.100.1.5",
        "/workspace",
        MergeAgentConfig(strategy="ours"),
    )

    assert resolved is True
    assert commands == ["cd /workspace && git fetch origin && git push --force origin HEAD:main"]
