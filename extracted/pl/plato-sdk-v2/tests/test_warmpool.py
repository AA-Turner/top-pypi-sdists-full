"""Unit tests for the warm VM pool and agent reset commands."""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import shlex
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from plato.agents.base import BaseAgent
from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import VMConfig
from plato.agents.runtime.warmpool import PooledVM, WarmPool


class _FakeClock:
    """Auto-advance the event loop clock so asyncio.sleep returns instantly."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self._real_time = loop.time
        self._offset = 0.0
        loop.time = self.time  # type: ignore[assignment]

    def time(self) -> float:
        return self._real_time() + self._offset

    def advance(self, seconds: float) -> None:
        self._offset += seconds


@pytest.fixture()
def event_loop():
    """Provide the event_loop fixture for fake_clock."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def fake_clock(event_loop: asyncio.AbstractEventLoop, monkeypatch: pytest.MonkeyPatch) -> _FakeClock:
    """Patch the event loop clock so tenacity retry sleeps resolve instantly."""
    clock = _FakeClock(event_loop)

    _original_sleep = asyncio.sleep

    async def _instant_sleep(delay: float, *args, **kwargs):
        clock.advance(delay)
        await _original_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", _instant_sleep)
    return clock


def _make_ctx() -> AgentContext:
    return AgentContext(
        image="test-agent:latest",
        config={"mode": "sleep"},
        instruction="",
        display_name="warm-test",
        agent_code_path=Path("/agents/test-agent"),
    )


def _make_vm(alias: str, mesh_ip: str = "10.0.0.2") -> PooledVM:
    env = MagicMock()
    env.alias = alias
    env.job_id = f"job-{alias}"
    return PooledVM(
        agent_env=env,
        mesh_ip=mesh_ip,
        alias=alias,
        image="test-agent:latest",
        runner_path="/usr/local/bin/plato-agent-runner",
        created_at=1.0,
        last_used_at=1.0,
        use_count=0,
    )


@pytest.mark.asyncio
async def test_prewarm_release_and_reacquire(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MagicMock()
    session.remove_env = AsyncMock()
    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
        max_size=2,
        pre_warm=1,
    )
    pooled_vm = _make_vm("agent-a")

    monkeypatch.setattr(pool, "_provision_vm", AsyncMock(return_value=pooled_vm))
    monkeypatch.setattr(pool, "_reset_vm", AsyncMock(return_value=True))
    monkeypatch.setattr(pool, "_health_check", AsyncMock(return_value=True))

    await pool.pre_warm()
    acquired = await pool.acquire()
    assert acquired.alias == "agent-a"
    assert acquired.use_count == 1

    await pool.release(acquired, workspace_paths=["/workspace"])

    reacquired = await pool.acquire()
    assert reacquired.alias == "agent-a"
    assert reacquired.use_count == 2
    await pool.shutdown()


@pytest.mark.asyncio
async def test_release_destroys_vm_when_reset_command_discovery_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MagicMock()
    session.remove_env = AsyncMock()
    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )
    pooled_vm = _make_vm("agent-b")
    pool._all_vms[pooled_vm.alias] = pooled_vm
    pool._in_use[pooled_vm.alias] = pooled_vm

    monkeypatch.setattr(
        pool,
        "_get_reset_commands",
        AsyncMock(side_effect=RuntimeError("reset-commands subcommand missing")),
    )

    await pool.release(pooled_vm, workspace_paths=["/workspace"])

    session.remove_env.assert_awaited_once_with(pooled_vm.agent_env)
    assert pooled_vm.alias not in pool._all_vms


@pytest.mark.asyncio
async def test_acquire_replaces_unhealthy_available_vm(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MagicMock()
    session.remove_env = AsyncMock()
    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
        max_size=1,
    )
    unhealthy_vm = _make_vm("agent-old")
    unhealthy_vm.use_count = 1
    replacement_vm = _make_vm("agent-new")
    pool._all_vms[unhealthy_vm.alias] = unhealthy_vm
    pool._available.append(unhealthy_vm)

    monkeypatch.setattr(pool, "_health_check", AsyncMock(side_effect=[False]))
    monkeypatch.setattr(pool, "_provision_vm", AsyncMock(return_value=replacement_vm))

    acquired = await pool.acquire()

    assert acquired.alias == "agent-new"
    session.remove_env.assert_awaited_once_with(unhealthy_vm.agent_env)
    assert replacement_vm.alias in pool._all_vms


@pytest.mark.asyncio
async def test_get_reset_commands_requires_valid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MagicMock()
    session.remove_env = AsyncMock()
    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )
    pooled_vm = _make_vm("agent-json")

    monkeypatch.setattr(pool, "_run_ssh", AsyncMock(return_value=(0, "not-json", "")))

    with pytest.raises(RuntimeError, match="invalid reset command JSON"):
        await pool._get_reset_commands(pooled_vm, ["/workspace"])


@pytest.mark.asyncio
async def test_get_reset_commands_uses_resolved_runner_path(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MagicMock()
    session.remove_env = AsyncMock()
    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )
    pooled_vm = _make_vm("agent-reset")
    run_ssh = AsyncMock(return_value=(0, '["echo reset"]', ""))
    monkeypatch.setattr(pool, "_run_ssh", run_ssh)

    commands = await pool._get_reset_commands(pooled_vm, ["/workspace", "/workspace/code"])

    assert commands == ["echo reset"]
    assert run_ssh.await_args.args[0] == "10.0.0.2"
    assert run_ssh.await_args.args[1].startswith("/usr/local/bin/plato-agent-runner reset-commands")


# --------------------------------------------------------------------------- #
# Reset command tests
# --------------------------------------------------------------------------- #


class TestBaseResetCommands:
    def test_returns_core_cleanup_commands(self) -> None:
        commands = BaseAgent.reset_commands([])
        assert any("pkill" in cmd for cmd in commands)
        assert any("/etc/environment" in cmd for cmd in commands)
        assert any("/tmp/plato-" in cmd for cmd in commands)

    def test_workspace_paths_are_shell_quoted(self) -> None:
        commands = BaseAgent.reset_commands(["/workspace", "/data/my workspace"])
        ws_cmds = [c for c in commands if "umount" in c]
        assert len(ws_cmds) == 2
        assert shlex.quote("/data/my workspace") in ws_cmds[1]

    def test_no_workspace_paths_skips_mount_cleanup(self) -> None:
        commands = BaseAgent.reset_commands([])
        assert not any("umount" in cmd for cmd in commands)

    def test_cleans_etc_hosts_runtime_entries(self) -> None:
        commands = BaseAgent.reset_commands([])
        hosts_cmds = [c for c in commands if "sed" in c and "/etc/hosts" in c]
        assert hosts_cmds, "reset_commands must clean stale /etc/hosts entries via sed"
        # Must target runtime.plato.internal specifically
        assert any("runtime" in c and "internal" in c for c in hosts_cmds)

    def test_pkill_uses_exact_name_match(self) -> None:
        commands = BaseAgent.reset_commands([])
        pkill_cmds = [c for c in commands if "pkill" in c]
        for cmd in pkill_cmds:
            # -x matches exact process name, not full cmdline, preventing self-kill
            assert "pkill -x" in cmd


_claude_code_available = importlib.util.find_spec("claude_code") is not None
_codex_available = importlib.util.find_spec("codex_agent") is not None


@pytest.mark.skipif(not _claude_code_available, reason="claude_code package not installed")
class TestClaudeCodeResetCommands:
    def test_inherits_base_and_adds_claude_cleanup(self) -> None:
        from claude_code import ClaudeCodeAgent

        commands = ClaudeCodeAgent.reset_commands(["/workspace"])
        assert any("pkill -x plato-agent-runner" in cmd for cmd in commands)
        assert any("umount" in cmd for cmd in commands)
        assert any(".claude" in cmd for cmd in commands)
        claude_pkill = [c for c in commands if "pkill -x claude" in c]
        assert claude_pkill


@pytest.mark.skipif(not _codex_available, reason="codex_agent package not installed")
class TestCodexResetCommands:
    def test_inherits_base_and_adds_codex_cleanup(self) -> None:
        from codex_agent import CodexAgent

        commands = CodexAgent.reset_commands(["/workspace"])
        assert any("pkill -x plato-agent-runner" in cmd for cmd in commands)
        assert any(".codex" in cmd for cmd in commands)
        codex_pkill = [c for c in commands if "pkill -x codex" in c]
        assert codex_pkill


@pytest.mark.parametrize(
    "agent_cls_path",
    [
        pytest.param("plato.agents.base:BaseAgent", id="base"),
        pytest.param(
            "claude_code:ClaudeCodeAgent",
            id="claude-code",
            marks=pytest.mark.skipif(not _claude_code_available, reason="claude_code not installed"),
        ),
        pytest.param(
            "codex_agent:CodexAgent",
            id="codex",
            marks=pytest.mark.skipif(not _codex_available, reason="codex_agent not installed"),
        ),
    ],
)
def test_pkill_commands_use_exact_name_match(agent_cls_path: str) -> None:
    """Every pkill in reset commands must use -x (exact name match) not -f
    (full cmdline match) to avoid killing the bash shell running the reset."""
    module_path, cls_name = agent_cls_path.split(":")
    module = importlib.import_module(module_path)
    agent_cls = getattr(module, cls_name)

    commands = agent_cls.reset_commands(["/workspace"])
    for cmd in commands:
        if "pkill" not in cmd:
            continue
        # Must use -x, never -f
        assert "pkill -x" in cmd, f"pkill command must use -x (exact name), got: {cmd}"
        assert "pkill -f" not in cmd, f"pkill -f is unsafe for reset commands: {cmd}"


@pytest.mark.asyncio
async def test_provision_vm_requires_ssh_key_path_early(fake_clock: _FakeClock) -> None:
    """ssh_key_path must be validated before any VM operations (single early guard)."""
    session = MagicMock()
    session.add_env = AsyncMock()
    pool = WarmPool(
        session=session,
        ssh_key_path=None,
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )
    with pytest.raises(RuntimeError, match="ssh_key_path required"):
        await pool._provision_vm(_make_ctx())
    # Crucially, no VM should have been created
    session.add_env.assert_not_awaited()


@pytest.mark.asyncio
async def test_provision_vm_retries_on_transient_failure(
    monkeypatch: pytest.MonkeyPatch, fake_clock: _FakeClock
) -> None:
    """_provision_vm retries with exponential backoff like the cold path's _create_vm."""
    agent_env = MagicMock()
    agent_env.mesh_ip = "10.0.0.1"
    agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")
    agent_env.add_ssh_key = AsyncMock()

    session = MagicMock()
    session.add_env = AsyncMock(side_effect=[RuntimeError("transient"), agent_env])

    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )

    monkeypatch.setattr("plato.agents.runtime.warmpool.install_agent_code_on_vm", AsyncMock())
    monkeypatch.setattr(
        "plato.agents.runtime.warmpool.resolve_runner_path", AsyncMock(return_value="/usr/local/bin/plato-agent-runner")
    )
    monkeypatch.setattr("pathlib.Path.read_text", lambda self: "ssh-ed25519 AAAATEST")

    vm = await pool._provision_vm(_make_ctx())
    assert vm.mesh_ip == "10.0.0.1"
    assert session.add_env.await_count == 2


@pytest.mark.asyncio
async def test_provision_vm_cleans_up_on_post_creation_failure(
    monkeypatch: pytest.MonkeyPatch, fake_clock: _FakeClock
) -> None:
    """If add_ssh_key/install/resolve fails after VM creation, the VM must be destroyed."""
    agent_env = MagicMock()
    agent_env.mesh_ip = "10.0.0.1"
    agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")
    agent_env.add_ssh_key = AsyncMock(side_effect=RuntimeError("SSH key upload failed"))

    session = MagicMock()
    session.add_env = AsyncMock(return_value=agent_env)
    session.remove_env = AsyncMock()

    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )

    monkeypatch.setattr("pathlib.Path.read_text", lambda self: "ssh-ed25519 AAAATEST")

    with pytest.raises(RuntimeError, match="SSH key upload failed"):
        await pool._provision_vm(_make_ctx())

    # Every retry must clean up its VM — 3 attempts = 3 remove_env calls
    assert session.remove_env.await_count == 3
    for call in session.remove_env.await_args_list:
        assert call.args == (agent_env,)


@pytest.mark.asyncio
async def test_shutdown_awaits_replenish_task_and_cleans_up(monkeypatch: pytest.MonkeyPatch) -> None:
    """shutdown() must await the replenish task so in-flight provisioning
    can clean up, preventing VM leaks from CancelledError."""
    agent_env = MagicMock()
    agent_env.mesh_ip = "10.0.0.1"
    agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")
    agent_env.add_ssh_key = AsyncMock()

    session = MagicMock()
    session.add_env = AsyncMock(return_value=agent_env)
    session.remove_env = AsyncMock()

    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
        max_size=2,
        pre_warm=1,
    )

    # Make _provision_vm slow so we can cancel it mid-flight
    async def slow_provision(ctx):
        # Simulate add_env succeeding, then a slow post-creation step
        env = await session.add_env(MagicMock())
        pool._untracked_envs.add(env)
        await asyncio.sleep(10)  # Will be cancelled here
        return _make_vm("agent-slow")

    monkeypatch.setattr(pool, "_provision_vm", slow_provision)

    # Start replenishing (will block on slow_provision)
    pool._pre_warm_target = 1
    pool._replenish_task = asyncio.create_task(pool._replenish_to_target())

    # Give the task time to start provisioning
    await asyncio.sleep(0.05)

    # Shutdown should cancel and await the replenish task, then clean up
    await pool.shutdown()

    # The env added to _untracked_envs should be cleaned up by shutdown
    assert len(pool._untracked_envs) == 0
    session.remove_env.assert_awaited()


@pytest.mark.asyncio
async def test_provision_vm_cleans_up_on_cancellation(monkeypatch: pytest.MonkeyPatch) -> None:
    """CancelledError during post-creation steps must still destroy the VM."""
    agent_env = MagicMock()
    agent_env.mesh_ip = "10.0.0.1"
    agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")
    agent_env.add_ssh_key = AsyncMock()

    session = MagicMock()
    session.add_env = AsyncMock(return_value=agent_env)
    session.remove_env = AsyncMock()

    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )

    monkeypatch.setattr("pathlib.Path.read_text", lambda self: "ssh-ed25519 AAAATEST")

    # install_agent_code_on_vm raises CancelledError (simulating task cancellation)
    async def cancel_during_install(*args, **kwargs):
        raise asyncio.CancelledError()

    monkeypatch.setattr("plato.agents.runtime.warmpool.install_agent_code_on_vm", cancel_during_install)

    with pytest.raises(asyncio.CancelledError):
        await pool._provision_vm(_make_ctx())

    # VM must be cleaned up despite CancelledError being a BaseException
    session.remove_env.assert_awaited_once_with(agent_env)
    # Must not remain in _untracked_envs
    assert agent_env not in pool._untracked_envs


@pytest.mark.asyncio
async def test_shutdown_destroys_untracked_envs(monkeypatch: pytest.MonkeyPatch) -> None:
    """VMs provisioned but never registered in _all_vms (e.g. gather
    cancellation discarding completed results) must be destroyed by shutdown."""
    session = MagicMock()
    session.remove_env = AsyncMock()

    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )

    # Simulate an env that was created but never tracked in _all_vms
    leaked_env = MagicMock()
    pool._untracked_envs.add(leaked_env)

    await pool.shutdown()

    session.remove_env.assert_awaited_once_with(leaked_env)
    assert len(pool._untracked_envs) == 0


@pytest.mark.asyncio
async def test_provision_vm_keeps_env_tracked_when_cleanup_fails(
    monkeypatch: pytest.MonkeyPatch, fake_clock: _FakeClock
) -> None:
    """If remove_env fails during post-creation cleanup, the env must remain
    in _untracked_envs so shutdown() can retry destroying it."""
    agent_env = MagicMock()
    agent_env.mesh_ip = "10.0.0.1"
    agent_env.get_mesh_ip = AsyncMock(return_value="10.0.0.1")
    agent_env.add_ssh_key = AsyncMock(side_effect=RuntimeError("SSH key upload failed"))

    session = MagicMock()
    session.add_env = AsyncMock(return_value=agent_env)
    session.remove_env = AsyncMock(side_effect=RuntimeError("API timeout"))

    pool = WarmPool(
        session=session,
        ssh_key_path=Path("/tmp/test-key"),
        vm_config=VMConfig(),
        prototype_ctx=_make_ctx(),
    )

    monkeypatch.setattr("pathlib.Path.read_text", lambda self: "ssh-ed25519 AAAATEST")

    with pytest.raises(RuntimeError, match="SSH key upload failed"):
        await pool._provision_vm(_make_ctx())

    # remove_env was attempted but failed — env must still be in _untracked_envs
    assert agent_env in pool._untracked_envs

    # shutdown() should attempt to clean it up
    session.remove_env.side_effect = None  # reset so shutdown succeeds
    await pool.shutdown()
    assert agent_env not in pool._untracked_envs
