"""Integration test world for file-pattern checkpoint triggers.

Tests that file changes on the agent VM trigger checkpoints on the world VM
with span context propagated via the CheckpointTriggerServer.

The agent is instructed to write a progress.json file. The world configures
a file trigger for ``**/progress.json`` and verifies that:
1. A checkpoint is triggered when progress.json is written
2. The workspace ref has a trigger_span_id
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Annotated, ClassVar

from plato.worlds import (
    Agent,
    AgentConfig,
    BaseWorld,
    Observation,
    RunConfig,
    StepResult,
    Workspace,
    register_world,
)
from plato.worlds.checkpoint import FileCheckpointTrigger, checkpoint

logger = logging.getLogger(__name__)

INSTRUCTION = """\
Complete these steps in order:

1. Write /workspace/progress.json with this exact content:
   {"stage": "started", "progress": 0}

2. Wait 3 seconds (use sleep or equivalent).

3. Update /workspace/progress.json to:
   {"stage": "working", "progress": 50}

4. Wait 3 seconds.

5. Update /workspace/progress.json to:
   {"stage": "done", "progress": 100}

6. Write /workspace/result.json with:
   {"status": "ok"}
"""


class CheckpointTriggerTestConfig(RunConfig):
    """Config for checkpoint trigger test world."""

    agent: Annotated[AgentConfig, Agent(description="Agent that writes progress files")]
    code: Annotated[
        Path,
        Workspace(
            description="Tracked workspace for checkpoint trigger testing",
            tracked=True,
            mount_path="/workspace",
        ),
    ] = Path("/workspace")


@register_world("plato-world-checkpoint-trigger-test")
class CheckpointTriggerTestWorld(BaseWorld[CheckpointTriggerTestConfig]):
    """Test world: agent writes progress.json, world triggers checkpoints on file changes."""

    name: ClassVar[str] = "checkpoint-trigger-test"
    description: ClassVar[str] = "Integration test for file-pattern checkpoint triggers"

    async def reset(self) -> Observation:
        return Observation(data={"status": "ready"})

    async def step(self) -> StepResult:
        code_ws = self.workspace("code")
        workspace_path = Path(code_ws.path)
        workspace_path.mkdir(parents=True, exist_ok=True)

        file_triggers = [FileCheckpointTrigger(pattern="**/progress.json", debounce_s=1.0)]

        async with checkpoint(
            self.checkpoint,
            "agent-run",
            step=1,
            interval_s=300,
            file_triggers=file_triggers,
        ) as ctx:
            agent_runner = self.agent(self.config.agent, workspaces=[code_ws]).with_file_triggers_from(ctx)
            await agent_runner.run(INSTRUCTION)

        # Verify agent output
        result_path = workspace_path / "result.json"
        if not result_path.exists():
            raise RuntimeError("Agent did not create /workspace/result.json")
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if result.get("status") != "ok":
            raise RuntimeError(f"Unexpected result.json: {result!r}")

        progress_path = workspace_path / "progress.json"
        if not progress_path.exists():
            raise RuntimeError("Agent did not create /workspace/progress.json")
        progress = json.loads(progress_path.read_text(encoding="utf-8"))

        # Validate checkpoints via Chronos API
        session_id = self._session_id or "unknown"
        chronos_url = self._get_chronos_base_url()
        api_key = os.environ.get("PLATO_API_KEY", "")

        validation = {"progress_final": progress, "session_id": session_id}

        if chronos_url and session_id != "unknown" and api_key:
            from plato.chronos.sdk import AsyncChronos

            async with AsyncChronos(base_url=chronos_url, api_key=api_key) as client:
                refs = await client.get_workspace_refs(session_id, repo_name=f"{self.name}/code")
                file_triggered_refs = [r for r in refs if ".file." in r.get("step_name", "")]
                validation["total_refs"] = len(refs)
                validation["file_triggered_refs"] = len(file_triggered_refs)
                validation["ref_steps"] = [r.get("step_name") for r in refs]

                # Check if any refs have trigger_span_id
                triggered_with_span = [r for r in file_triggered_refs if r.get("trigger_span_id")]
                validation["refs_with_trigger_span"] = len(triggered_with_span)

                logger.info(
                    "Checkpoint validation: %d total refs, %d file-triggered, %d with span",
                    len(refs),
                    len(file_triggered_refs),
                    len(triggered_with_span),
                )

        return StepResult(
            observation=Observation(data=validation),
            done=True,
        )
