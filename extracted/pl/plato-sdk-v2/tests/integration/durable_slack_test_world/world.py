"""Test world that runs a durable stage with Slack notifications enabled via config."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, Field

from plato.worlds import BaseWorld, Observation, RunConfig, StepResult, register_world
from plato.worlds.durable import DurableOutputs, FromArg, durable

logger = logging.getLogger(__name__)


class ComputeResult(BaseModel):
    answer: int


class StageOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    result: ComputeResult = Field(json_schema_extra={"json": "result.json"})


@durable(d=FromArg("d"))
async def compute_stage(d: Path) -> StageOutputs:
    """A simple durable stage that computes a value."""
    logger.info("Running compute_stage")
    return StageOutputs(result=ComputeResult(answer=42))


@register_world("plato-world-durable-slack-test")
class DurableSlackTestWorld(BaseWorld[RunConfig]):
    """Runs a single durable stage with Slack notifications to verify the integration."""

    name: ClassVar[str] = "durable-slack-test"
    description: ClassVar[str] = "Durable stage Slack notification test"

    async def reset(self) -> Observation:
        logger.info("DurableSlackTestWorld reset")

        # Run the durable stage — slack notification is auto-enabled by BaseWorld
        # when config.slack_notifications_enabled is True
        stage_dir = Path("/tmp/durable-slack-test-stage")
        stage_dir.mkdir(parents=True, exist_ok=True)
        result = await compute_stage(d=stage_dir)
        logger.info("Stage completed with answer=%d", result.result.answer)

        return Observation(data={"stage_answer": result.result.answer, "status": "ready"})

    async def step(self) -> StepResult:
        return StepResult(
            observation=Observation(data={"status": "passed"}),
            done=True,
        )
