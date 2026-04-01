"""E2E tests for ParallelAgentOrchestrator on a real Chronos VM."""

from __future__ import annotations

import shutil
from pathlib import Path

from plato.agents import ParallelAgentOrchestrator
from plato.agents.runtime.transport import GitTransport
from plato.utils.subprocess import run_local
from plato.worlds import AgentConfig


def _task_agent_config(world, *, shared_mode: str) -> AgentConfig:
    return _task_agent_config_with_options(world, shared_mode=shared_mode)


def _task_agent_config_with_options(
    world,
    *,
    shared_mode: str,
    initial_snapshot_path: str = "",
) -> AgentConfig:
    base = world.config.agent
    return AgentConfig(
        package=base.package,
        image=base.image,
        runtime=base.runtime,
        config={
            **base.config,
            "mode": "git_io",
            "workspace_dir": world.workspace("code").mount_path,
            "duration_seconds": 1,
            "file_count": 1,
            "file_size_kb": 1,
            "git_shared_mode": shared_mode,
            "git_initial_snapshot_path": initial_snapshot_path,
        },
    )


def _merge_agent_config(world) -> AgentConfig:
    base = world.config.merge_agent
    return AgentConfig(
        package=base.package,
        image=base.image,
        runtime=base.runtime,
        config={
            **base.config,
            "mode": "git_merge_resolve",
            "workspace_dir": world.workspace("code").mount_path,
        },
    )


def _warm_pool_agent_config(world) -> AgentConfig:
    base = world.config.agent
    return AgentConfig(
        package=base.package,
        image=base.image,
        runtime=base.runtime,
        config={
            **base.config,
            "mode": "warm_pool_probe",
            "workspace_dir": world.workspace("code").mount_path,
        },
    )


async def setup_module(world) -> None:
    await _reset_workspace(world, shared_content="base\n")


async def test_parallel_non_conflicting_agents(world) -> None:
    await _reset_workspace(world, shared_content="base\n")
    code_ws = world.workspace("code")
    before_steps = set(await _auto_checkpoint_steps(code_ws))

    orchestrator = ParallelAgentOrchestrator(
        world,
        code_ws,
        _task_agent_config(world, shared_mode="ignore"),
        max_parallel=3,
        merge_agent_config=_merge_agent_config(world),
    )
    before = {path.name for path in Path(code_ws.path).glob("git-agent-*")}

    for idx in range(3):
        await orchestrator.submit(f"unique-{idx}", f"Write unique output {idx}")

    results = await orchestrator.run_all()

    assert all(result.status == "success" for result in results), results
    assert all(result.merged for result in results), results
    assert await _hidden_task_refs(world) == []
    after_steps = set(await _auto_checkpoint_steps(code_ws))
    assert len(after_steps - before_steps) >= 1

    after = {path.name for path in Path(code_ws.path).glob("git-agent-*")}
    assert len(after - before) == 3


async def test_parallel_conflict_resolution_agent(world) -> None:
    await _reset_workspace(world, shared_content="base\n")
    code_ws = world.workspace("code")
    before_steps = set(await _auto_checkpoint_steps(code_ws))

    orchestrator = ParallelAgentOrchestrator(
        world,
        code_ws,
        _task_agent_config(world, shared_mode="replace"),
        max_parallel=2,
        merge_agent_config=_merge_agent_config(world),
    )

    for idx in range(2):
        await orchestrator.submit(f"conflict-{idx}", f"Cause shared conflict {idx}")

    results = await orchestrator.run_all()

    assert all(result.status == "success" for result in results), results
    assert await _hidden_task_refs(world) == []
    after_steps = set(await _auto_checkpoint_steps(code_ws))
    assert len(after_steps - before_steps) >= 1
    shared_content = (Path(code_ws.path) / "shared.txt").read_text()
    assert shared_content.count("line from agent") >= 2


async def test_parallel_agents_with_warm_pool_reuse_vms(world) -> None:
    await _reset_workspace(world, shared_content="base\n")
    code_ws = world.workspace("code")
    agent_config = _warm_pool_agent_config(world)

    orchestrator = ParallelAgentOrchestrator(
        world,
        code_ws,
        agent_config,
        max_parallel=2,
        warm_pool=True,
    )

    for idx in range(6):
        await orchestrator.submit(f"pooled-{idx}", f"Warm pool probe {idx}")

    results = await orchestrator.run_all()

    failed = [r for r in results if r.status != "success"]
    assert not failed, f"Tasks failed: {failed}"
    unique_agents = {r.agent_id for r in results if r.agent_id}
    assert len(unique_agents) <= 2, f"Expected VM reuse but got {len(unique_agents)} unique agents: {unique_agents}"
    probe_files = list(Path(code_ws.path).glob("pool-probe-*.txt"))
    assert len(probe_files) == 6, f"Expected 6 probe files, got {len(probe_files)}"


async def test_pinned_base_checkout_ignores_integrated_main_advance(world) -> None:
    await _reset_workspace(world, shared_content="base\n")
    code_ws = world.workspace("code")

    orchestrator = ParallelAgentOrchestrator(
        world,
        code_ws,
        _task_agent_config(world, shared_mode="replace"),
        max_parallel=1,
        merge_agent_config=_merge_agent_config(world),
    )
    await orchestrator.submit("task-a", "Advance shared state from task A")
    await orchestrator.submit("task-b", "Snapshot initial shared state from task B")

    orchestrator._resolved_base_ref = await orchestrator._resolve_base_ref()  # pyright: ignore[reportPrivateUsage]
    original_base = orchestrator.resolved_base_ref
    assert original_base is not None

    task_a = orchestrator._tasks[0]  # pyright: ignore[reportPrivateUsage]
    task_a_ws, task_a_transport = orchestrator._make_task_workspace(task_a)  # pyright: ignore[reportPrivateUsage]
    await world.agent(
        _task_agent_config(world, shared_mode="replace"),
        display_name="task-a",
        workspaces=[task_a_ws],
    ).run(task_a.instruction)
    assert task_a_transport.published_ref is not None
    merged_a = await orchestrator._integrate_published_ref(  # pyright: ignore[reportPrivateUsage]
        task_a,
        task_a_transport.published_ref,
        max_retries=task_a_ws.transport.merge_config.merge_agent.max_retries,  # type: ignore[union-attr]
    )
    assert merged_a is True

    shared_path = Path(code_ws.path) / "shared.txt"
    assert shared_path.read_text() != "base\n"

    task_b = orchestrator._tasks[1]  # pyright: ignore[reportPrivateUsage]
    task_b_ws, task_b_transport = orchestrator._make_task_workspace(task_b)  # pyright: ignore[reportPrivateUsage]
    assert isinstance(task_b_transport, GitTransport)
    assert task_b_transport.checkout_base_ref == original_base

    snapshot_relpath = "initial-observation/task-b-shared.txt"
    await world.agent(
        _task_agent_config_with_options(
            world,
            shared_mode="ignore",
            initial_snapshot_path=snapshot_relpath,
        ),
        display_name="task-b",
        workspaces=[task_b_ws],
    ).run(task_b.instruction)
    assert task_b_transport.published_ref is not None
    merged_b = await orchestrator._integrate_published_ref(  # pyright: ignore[reportPrivateUsage]
        task_b,
        task_b_transport.published_ref,
        max_retries=task_b_ws.transport.merge_config.merge_agent.max_retries,  # type: ignore[union-attr]
    )
    assert merged_b is True

    snapshot_path = Path(code_ws.path) / snapshot_relpath
    assert snapshot_path.exists()
    assert snapshot_path.read_text() == "base\n"


async def _reset_workspace(world, *, shared_content: str) -> None:
    code_ws = world.workspace("code")
    code_path = Path(code_ws.path)

    for path in code_path.glob("git-agent-*"):
        if path.is_dir():
            shutil.rmtree(path)

    (code_path / "shared.txt").write_text(shared_content)
    transport = code_ws.transport
    assert isinstance(transport, GitTransport)
    await transport.update_bare_repo("Reset parallel agent e2e workspace")


async def _hidden_task_refs(world) -> list[str]:
    transport = world.workspace("code").transport
    assert isinstance(transport, GitTransport)
    exit_code, stdout, stderr = await run_local(
        f"git --git-dir {transport.bare_repo_path} for-each-ref --format='%(refname)' refs/plato/tasks",
        timeout=30,
    )
    assert exit_code == 0, stderr
    return [line for line in stdout.splitlines() if line]


async def _auto_checkpoint_steps(workspace) -> list[str]:
    return [step for step in await workspace.list_steps() if step.startswith("parallel_agents.")]
