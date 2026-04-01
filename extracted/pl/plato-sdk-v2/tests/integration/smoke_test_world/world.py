"""Minimal integration test world — just reset+step, no agents."""

from __future__ import annotations

import logging
from typing import ClassVar

from plato.worlds import BaseWorld, Observation, RunConfig, StepResult, register_world

logger = logging.getLogger(__name__)


@register_world("plato-world-minimal-test")
class MinimalTestWorld(BaseWorld[RunConfig]):
    """Immediately completes after reset. For testing the runner exit path."""

    name: ClassVar[str] = "minimal-test"
    description: ClassVar[str] = "Minimal test world"

    async def reset(self) -> Observation:
        logger.info("MinimalTestWorld reset")
        return Observation(data={"status": "ready"})

    async def step(self) -> StepResult:
        logger.info("MinimalTestWorld step — returning done=True")
        return StepResult(
            observation=Observation(data={"status": "passed"}),
            done=True,
        )
