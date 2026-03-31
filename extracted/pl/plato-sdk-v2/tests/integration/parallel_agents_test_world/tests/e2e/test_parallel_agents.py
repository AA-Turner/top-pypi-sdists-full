"""E2E tests for ParallelAgentOrchestrator on a real Chronos VM."""

from __future__ import annotations

import shutil
from pathlib import Path

from plato.agents import ParallelAgentOrchestrator
from plato.agents.runtime.transport import GitTransport
from plato.utils.subprocess import run_local
from plato.worlds import AgentConfig


def _task_agent_config(world, *, shared_mode: str) -> AgentConfig:
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
