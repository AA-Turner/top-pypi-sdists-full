"""Unit tests for the parallel agent orchestrator."""

from __future__ import annotations

import asyncio
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import cast
from unittest.mock import AsyncMock

import pytest

from plato.agents.parallel import ParallelAgentOrchestrator, ParallelAgentResult
from plato.runtime import VMRuntimeConfig
from plato.transports import GitPublishedRef, GitTransport
from plato.worlds.base import BaseWorld
from plato.worlds.config import AgentConfig, GitTransportConfig
from plato.worlds.workspace import Workspace


class _FakeRunner:
    def __init__(
        self,
        run_fn: Callable[[str, str, list[Workspace] | None], asyncio.Future[str] | asyncio.Task[str] | object],
        display_name: str,
        workspaces: list[Workspace] | None,
    ) -> None:
        self._run_fn = run_fn
        self._display_name = display_name
        self._workspaces = workspaces

    async def run(self, instruction: str) -> str:
        result = self._run_fn(self._display_name, instruction, self._workspaces)
        if asyncio.isfuture(result) or asyncio.iscoroutine(result):
            return await result
        return str(result)


class _FakeWorld:
    def __init__(
        self,
        run_fn: Callable[[str, str, list[Workspace] | None], asyncio.Future[str] | asyncio.Task[str] | object],
    ) -> None:
        self._run_fn = run_fn
        self.agent_calls: list[tuple[str | None, list[Workspace] | None]] = []
        self.checkpoint_calls: list[str] = []

    def agent(
        self,
        config: AgentConfig,
        display_name: str | None = None,
        workspaces: list[Workspace] | None = None,
        warm_pool=None,
        agent_code_path=None,
    ) -> _FakeRunner:
        del config
        del warm_pool
        del agent_code_path
        self.agent_calls.append((display_name, workspaces))
        return _FakeRunner(self._run_fn, display_name or "", workspaces)

    async def checkpoint(self, label: str, *, trigger_span_id: str = "") -> None:
        del trigger_span_id
        self.checkpoint_calls.append(label)


def _make_workspace(tmp_path: Path, *, tracked: bool = False) -> Workspace:
    root = tmp_path / "code"
    root.mkdir()
    if tracked:
        (root / "data").mkdir()
    (root / "seed.txt").write_text("seed\n")
    bare_repo = root / ".git-bare"
    _git(["init", "-b", "main"], cwd=root)
    _git(["config", "user.email", "plato@plato.dev"], cwd=root)
    _git(["config", "user.name", "Plato"], cwd=root)
    _git(["add", "-A"], cwd=root)
    _git(["commit", "-m", "Seed workspace", "--allow-empty"], cwd=root)
    _git(["init", "--bare", "-b", "main", str(bare_repo)], cwd=tmp_path)
    _git(["remote", "add", "origin", str(bare_repo)], cwd=root)
    _git(["push", "origin", "main"], cwd=root)
    shutil.rmtree(root / ".git")
    workspace = Workspace("code", root, tracked=tracked, mount_path="/workspace", backup=tracked)
    transport = GitTransport(
        str(workspace.path),
        "127.0.0.1",
        Path("/tmp/parallel-test-key"),
        git_config=GitTransportConfig(),
    )
    workspace.transport = transport
    return workspace


def _make_agent_config() -> AgentConfig:
    return AgentConfig(
        image="test-agent:latest",
        runtime=VMRuntimeConfig(),
        config={"mode": "git_io"},
    )


def _set_published_ref(workspaces: list[Workspace] | None, *, name: str) -> None:
    assert workspaces is not None
    transport = workspaces[0].transport
    assert isinstance(transport, GitTransport)
    transport._published_ref = GitPublishedRef(  # pyright: ignore[reportPrivateUsage]
        commit_sha=f"sha-{name}",
        ref=f"refs/plato/tasks/{name}/sha-{name}",
    )


class TestParallelAgentOrchestrator:
    @pytest.mark.asyncio
    async def test_submit_skip_and_success(self, tmp_path: Path) -> None:
        calls: list[str] = []

        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del workspaces
            calls.append(f"{display_name}:{instruction}")
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(
            cast(BaseWorld, world), workspace, _make_agent_config(), max_parallel=2
        )

        await orchestrator.submit("skip-me", "ignored", skip_if=lambda: True)
        await orchestrator.submit("run-me", "do work")

        results = await orchestrator.run_all()

        assert [result.status for result in results] == ["skipped", "success"]
        assert results[1].agent_id == "agent-run-me"
        assert results[1].merged is True
        assert calls == ["run-me:do work"]
        assert workspace.transport is not None
        assert isinstance(workspace.transport, GitTransport)
        assert workspace.transport.publish_ref_prefix is None

    @pytest.mark.asyncio
    async def test_collects_mixed_success_failure_skip_and_published_integrations(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del instruction
            if display_name == "queued":
                _set_published_ref(workspaces, name=display_name)
            if display_name == "failure":
                raise RuntimeError("boom")
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())

        merge_calls: list[str] = []

        async def fake_integrate(task, published_ref, max_retries):  # type: ignore[no-untyped-def]
            merge_calls.append(f"{task.name}:{published_ref.commit_sha}:{max_retries}")
            return True

        monkeypatch.setattr(orchestrator, "_integrate_published_ref", fake_integrate)

        await orchestrator.submit("skip", "ignored", skip_if=lambda: True)
        await orchestrator.submit("success", "ok")
        await orchestrator.submit("queued", "merge me")
        await orchestrator.submit("failure", "nope")

        results = await orchestrator.run_all()

        assert [(result.name, result.status) for result in results] == [
            ("skip", "skipped"),
            ("success", "success"),
            ("queued", "success"),
            ("failure", "failed"),
        ]
        assert merge_calls == ["queued:sha-queued:3"]
        assert results[2].merged is True
        assert results[2].agent_id == "agent-queued"
        assert results[3].error == "boom"

    @pytest.mark.asyncio
    async def test_run_all_resolves_base_ref_once_and_pins_task_transports(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        seen_base_refs: list[str | None] = []

        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del display_name, instruction
            assert workspaces is not None
            transport = workspaces[0].transport
            assert isinstance(transport, GitTransport)
            seen_base_refs.append(transport.checkout_base_ref)
            return "agent"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())
        resolve_mock = AsyncMock(return_value="base-sha")
        monkeypatch.setattr(orchestrator, "_resolve_base_ref", resolve_mock)

        await orchestrator.submit("task-a", "work-a")
        await orchestrator.submit("task-b", "work-b")

        results = await orchestrator.run_all()

        assert [result.status for result in results] == ["success", "success"]
        assert seen_base_refs == ["base-sha", "base-sha"]
        assert orchestrator.resolved_base_ref == "base-sha"
        resolve_mock.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_later_task_workspace_keeps_original_pinned_base_after_main_advances(self, tmp_path: Path) -> None:
        world = _FakeWorld(lambda display_name, instruction, workspaces: f"agent-{display_name}")
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())
        initial_main = _git(["--git-dir", str(Path(workspace.path) / ".git-bare"), "rev-parse", "main"], cwd=tmp_path)
        orchestrator._resolved_base_ref = initial_main.stdout.strip()  # pyright: ignore[reportPrivateUsage]

        await orchestrator.submit("task-a", "work-a")
        await orchestrator.submit("task-b", "work-b")

        advance_clone = tmp_path / "advance-clone"
        _git(["clone", str(Path(workspace.path) / ".git-bare"), str(advance_clone)], cwd=tmp_path)
        _git(["config", "user.email", "plato@plato.dev"], cwd=advance_clone)
        _git(["config", "user.name", "Plato"], cwd=advance_clone)
        (advance_clone / "advanced.txt").write_text("new main state\n")
        _git(["add", "advanced.txt"], cwd=advance_clone)
        _git(["commit", "-m", "Advance main"], cwd=advance_clone)
        _git(["push", "origin", "main"], cwd=advance_clone)
        advanced_main = _git(["--git-dir", str(Path(workspace.path) / ".git-bare"), "rev-parse", "main"], cwd=tmp_path)

        assert advanced_main.stdout.strip() != orchestrator.resolved_base_ref

        _, task_transport = orchestrator._make_task_workspace(orchestrator._tasks[1])

        assert task_transport.checkout_base_ref == orchestrator.resolved_base_ref

    @pytest.mark.asyncio
    async def test_agent_slots_release_before_integration_finishes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        started_runs: list[str] = []
        integration_started = asyncio.Event()
        allow_integration = asyncio.Event()

        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del instruction
            started_runs.append(display_name)
            _set_published_ref(workspaces, name=display_name)
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(
            cast(BaseWorld, world), workspace, _make_agent_config(), max_parallel=1
        )

        async def fake_integrate(task, published_ref, max_retries):  # type: ignore[no-untyped-def]
            del task, published_ref, max_retries
            integration_started.set()
            await allow_integration.wait()
            return True

        monkeypatch.setattr(orchestrator, "_integrate_published_ref", fake_integrate)

        await orchestrator.submit("task-1", "work-1")
        await orchestrator.submit("task-2", "work-2")

        results_task = asyncio.create_task(orchestrator.run_all())
        await integration_started.wait()
        await asyncio.sleep(0)

        assert started_runs == ["task-1", "task-2"]

        allow_integration.set()
        results = await results_task

        assert all(result.status == "success" for result in results)

    @pytest.mark.asyncio
    async def test_tracked_workspace_checkpointed_after_successful_integration(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        world = _FakeWorld(lambda display_name, instruction, workspaces: f"agent-{display_name}")
        workspace = _make_workspace(tmp_path, tracked=True)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())

        await orchestrator.submit("tracked-task", "work")
        queued_task = orchestrator._tasks[0]
        published_ref = GitPublishedRef(
            commit_sha="abc123def4567890",
            ref="refs/plato/tasks/tracked/abc123def4567890",
        )

        async def noop(*args, **kwargs):  # type: ignore[no-untyped-def]
            del args, kwargs
            return None

        async def merge_clean(*args, **kwargs):  # type: ignore[no-untyped-def]
            del args, kwargs
            return False

        monkeypatch.setattr(orchestrator, "_clone_repo", noop)
        monkeypatch.setattr(orchestrator, "_fetch_ref", noop)
        monkeypatch.setattr(orchestrator, "_merge_fetched_commit", merge_clean)
        monkeypatch.setattr(orchestrator, "_push_resolved_main", noop)
        monkeypatch.setattr(orchestrator, "_delete_ref", noop)
        monkeypatch.setattr(workspace, "ensure_fuse_mount", noop)
        monkeypatch.setattr(workspace, "materialize_current_tree_into_overlay", noop)

        merged = await orchestrator._integrate_published_ref(queued_task, published_ref, max_retries=1)

        assert merged is True
        assert world.checkpoint_calls == ["parallel_agents.tracked-task.abc123def456"]

    @pytest.mark.asyncio
    async def test_clone_and_fetch_hidden_task_ref_from_local_bare_repo(self, tmp_path: Path) -> None:
        workspace = _make_workspace(tmp_path)
        transport = workspace.transport
        assert isinstance(transport, GitTransport)
        await transport.initialize()

        seed_clone = tmp_path / "seed-clone"
        _git(["clone", transport.bare_repo_path, str(seed_clone)], cwd=tmp_path)
        _git(["config", "user.email", "plato@plato.dev"], cwd=seed_clone)
        _git(["config", "user.name", "Plato"], cwd=seed_clone)

        hidden_ref = "refs/plato/tasks/group-a/abc123"
        (seed_clone / "local.txt").write_text("hello\n")
        _git(["add", "local.txt"], cwd=seed_clone)
        _git(["commit", "-m", "Add hidden ref content"], cwd=seed_clone)
        expected_sha = _git(["rev-parse", "HEAD"], cwd=seed_clone).stdout.strip()
        _git(["push", "origin", f"HEAD:{hidden_ref}"], cwd=seed_clone)

        world = _FakeWorld(lambda display_name, instruction, workspaces: f"agent-{display_name}")
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())

        integration_clone = tmp_path / "integration-clone"
        await orchestrator._clone_repo(integration_clone)
        await orchestrator._fetch_ref(integration_clone, hidden_ref)

        fetched_sha = _git(["rev-parse", "FETCH_HEAD"], cwd=integration_clone).stdout.strip()
        assert fetched_sha == expected_sha

    @pytest.mark.asyncio
    async def test_on_completed_fires_before_run_all_returns(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """on_completed must fire during run_all (after integration),
        not after run_all returns — so durable cache is written before
        the next DVC checkpoint."""
        callback_order: list[str] = []

        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del instruction
            if display_name == "with-ref":
                _set_published_ref(workspaces, name="with-ref")
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())

        async def fake_integrate(task, published_ref, max_retries):  # type: ignore[no-untyped-def]
            del published_ref, max_retries
            callback_order.append(f"integrate:{task.name}")
            return True

        monkeypatch.setattr(orchestrator, "_integrate_published_ref", fake_integrate)

        def on_completed_a(result: ParallelAgentResult) -> None:
            callback_order.append(f"on_completed:{result.name}:{result.status}")

        def on_completed_b(result: ParallelAgentResult) -> None:
            callback_order.append(f"on_completed:{result.name}:{result.status}")

        def on_completed_c(result: ParallelAgentResult) -> None:
            callback_order.append(f"on_completed:{result.name}:{result.status}")

        await orchestrator.submit("skipped", "ignored", skip_if=lambda: True, on_completed=on_completed_a)
        await orchestrator.submit("no-ref", "work", on_completed=on_completed_b)
        await orchestrator.submit("with-ref", "work", on_completed=on_completed_c)

        results = await orchestrator.run_all()
        callback_order.append("run_all_returned")

        # All on_completed callbacks fire BEFORE run_all returns
        assert callback_order.index("on_completed:skipped:skipped") < callback_order.index("run_all_returned")
        assert callback_order.index("on_completed:no-ref:success") < callback_order.index("run_all_returned")
        assert callback_order.index("on_completed:with-ref:success") < callback_order.index("run_all_returned")

        # For the integrated task, on_completed fires AFTER integration
        assert callback_order.index("integrate:with-ref") < callback_order.index("on_completed:with-ref:success")

        assert [r.status for r in results] == ["skipped", "success", "success"]

    @pytest.mark.asyncio
    async def test_on_completed_not_called_on_failure(self, tmp_path: Path) -> None:
        """on_completed should NOT fire for failed tasks."""
        callback_calls: list[str] = []

        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del instruction, workspaces
            if display_name == "fail":
                raise RuntimeError("boom")
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())

        def on_completed(result: ParallelAgentResult) -> None:
            callback_calls.append(result.name)

        await orchestrator.submit("fail", "work", on_completed=on_completed)
        results = await orchestrator.run_all()

        assert results[0].status == "failed"
        assert callback_calls == []

    @pytest.mark.asyncio
    async def test_on_completed_exception_does_not_break_orchestrator(self, tmp_path: Path) -> None:
        """A failing on_completed callback must not crash run_all."""

        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del instruction, workspaces
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())

        def bad_callback(result: ParallelAgentResult) -> None:
            raise ValueError("callback exploded")

        await orchestrator.submit("task-a", "work", on_completed=bad_callback)
        await orchestrator.submit("task-b", "work")

        results = await orchestrator.run_all()

        # Both tasks succeed despite the broken callback
        assert [r.status for r in results] == ["success", "success"]

    @pytest.mark.asyncio
    async def test_task_workspace_preserves_agent_mount_path(self, tmp_path: Path) -> None:
        world = _FakeWorld(lambda display_name, instruction, workspaces: f"agent-{display_name}")
        workspace = _make_workspace(tmp_path, tracked=True)
        orchestrator = ParallelAgentOrchestrator(cast(BaseWorld, world), workspace, _make_agent_config())
        await orchestrator.submit("demo", "work")

        task_workspace, task_transport = orchestrator._make_task_workspace(orchestrator._tasks[0])

        assert task_workspace.mount_path == "/workspace"
        assert task_transport.mount_path == "/workspace"
        assert task_transport.path == str(workspace.path)
        assert task_transport.checkout_base_ref is None

    @pytest.mark.asyncio
    async def test_warm_pool_disables_semaphore(self, tmp_path: Path) -> None:
        """When warm pool is enabled, semaphore is None (pool provides backpressure)."""
        workspace = _make_workspace(tmp_path)

        orchestrator = ParallelAgentOrchestrator(
            _FakeWorld(lambda d, i, w: "ok"),
            workspace,
            _make_agent_config(),
            max_parallel=2,
            warm_pool=True,
        )

        assert orchestrator._semaphore is None

    @pytest.mark.asyncio
    async def test_no_warm_pool_creates_semaphore(self, tmp_path: Path) -> None:
        """Without warm pool, a semaphore is created for concurrency control."""
        workspace = _make_workspace(tmp_path)

        orchestrator = ParallelAgentOrchestrator(
            _FakeWorld(lambda d, i, w: "ok"),
            workspace,
            _make_agent_config(),
            max_parallel=3,
        )

        assert orchestrator._semaphore is not None

    @pytest.mark.asyncio
    async def test_warm_pool_prewarms_and_shuts_down(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        async def run_fn(display_name: str, instruction: str, workspaces: list[Workspace] | None) -> str:
            del instruction, workspaces
            return f"agent-{display_name}"

        world = _FakeWorld(run_fn)
        workspace = _make_workspace(tmp_path)
        warm_pool_stub = type(
            "_WarmPoolStub",
            (),
            {
                "pre_warm": AsyncMock(),
                "shutdown": AsyncMock(),
                "max_size": 1,
            },
        )()

        orchestrator = ParallelAgentOrchestrator(
            world,
            workspace,
            _make_agent_config(),
            max_parallel=1,
            warm_pool=True,
        )

        # Inject stub pool so we don't need a real Plato session
        monkeypatch.setattr(orchestrator, "_create_warm_pool", lambda num_tasks: warm_pool_stub)

        await orchestrator.submit("task-1", "work-1")
        await orchestrator.submit("task-2", "work-2")

        results = await orchestrator.run_all()

        assert [result.status for result in results] == ["success", "success"]
        warm_pool_stub.pre_warm.assert_awaited_once()
        warm_pool_stub.shutdown.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_warm_pool_max_size_set_to_max_parallel(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """_create_warm_pool sets max_size to max_parallel."""
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(
            _FakeWorld(lambda d, i, w: "ok"),
            workspace,
            _make_agent_config(),
            max_parallel=3,
            warm_pool=True,
        )

        # Provide a fake world with session/ssh_key
        orchestrator._world.plato_session = type("_Sess", (), {})()  # type: ignore[union-attr]
        orchestrator._world._ssh_key_path = Path("/tmp/fake-key")  # type: ignore[union-attr]

        pool = orchestrator._create_warm_pool(num_tasks=6)
        assert pool.max_size == 3

    @pytest.mark.asyncio
    async def test_warm_pool_timeout_scales_with_task_count(
        self,
        tmp_path: Path,
    ) -> None:
        """Pool VM timeout should scale based on number of task waves."""
        workspace = _make_workspace(tmp_path)
        orchestrator = ParallelAgentOrchestrator(
            _FakeWorld(lambda d, i, w: "ok"),
            workspace,
            _make_agent_config(),
            max_parallel=2,
            warm_pool=True,
        )

        orchestrator._world.plato_session = type("_Sess", (), {})()  # type: ignore[union-attr]
        orchestrator._world._ssh_key_path = Path("/tmp/fake-key")  # type: ignore[union-attr]

        # 5 tasks with max_parallel=2 → 3 waves → timeout = 7200 * 3
        pool = orchestrator._create_warm_pool(num_tasks=5)
        assert pool.vm_config.timeout == 7200 * 3


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
