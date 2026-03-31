"""Minimal world for ParallelAgentOrchestrator integration tests."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar

from plato.agents.runtime.transport import GitTransport
from plato.worlds import Agent, AgentConfig, BaseWorld, Observation, RunConfig, StepResult, Workspace, register_world


class ParallelAgentsTestWorldConfig(RunConfig):
    agent: Annotated[AgentConfig, Agent(description="Parallel task agent")]
    merge_agent: Annotated[AgentConfig, Agent(description="Merge conflict resolution agent")]
    code: Annotated[
        Path,
        Workspace(
            description="Git-backed workspace for parallel agent tests",
            tracked=True,
            mount_path="/workspace",
            transport="git",
        ),
    ] = Path("/workspace")


@register_world("plato-world-parallel-agents-test")
class ParallelAgentsTestWorld(BaseWorld[ParallelAgentsTestWorldConfig]):
    name: ClassVar[str] = "parallel-agents-test"
    description: ClassVar[str] = "Integration test world for parallel git agent orchestration"

    async def reset(self) -> Observation:
        code_ws = self.workspace("code")
        code_path = Path(code_ws.path)
        code_path.mkdir(parents=True, exist_ok=True)
        (code_path / "shared.txt").write_text("base\n")
        (code_path / "notes.txt").write_text("seed\n")

        transport = code_ws.transport
        if not isinstance(transport, GitTransport):
            raise RuntimeError("Expected git transport for 'code' workspace")
        await transport.update_bare_repo("Seed integration test workspace")

        return Observation(data={"status": "ready"})

    async def step(self) -> StepResult:
        return StepResult(
            observation=Observation(data={"status": "unused"}),
            done=True,
        )
