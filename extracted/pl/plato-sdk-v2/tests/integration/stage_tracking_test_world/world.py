"""Test world that runs multiple durable stages to verify stage tracking.

When run with slack_notifications_enabled=True, each @durable stage will
report started/completed events to Chronos. After the session, check the
Pipeline tab in Chronos to verify stages appear with correct timing.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, Field

from plato.worlds import BaseWorld, Observation, RunConfig, StepResult, register_world
from plato.worlds.durable import DurableOutputs, FromArg, durable

logger = logging.getLogger(__name__)


class AnalysisResult(BaseModel):
    entities: int
    relationships: int


class AnalysisOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/analysis"
    result: AnalysisResult = Field(json_schema_extra={"json": "result.json"})


class SchemaResult(BaseModel):
    tables: int


class SchemaOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/schema"
    result: SchemaResult = Field(json_schema_extra={"json": "result.json"})


class BuildResult(BaseModel):
    routes: int


class BuildOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/build"
    result: BuildResult = Field(json_schema_extra={"json": "result.json"})


@durable(d=FromArg("d"))
async def analysis_stage(d: Path) -> AnalysisOutputs:
    """Simulates a graph analysis stage."""
    logger.info("Running analysis stage")
    await asyncio.sleep(2)
    return AnalysisOutputs(result=AnalysisResult(entities=5, relationships=3))


@durable(d=FromArg("d"))
async def schema_stage(d: Path) -> SchemaOutputs:
    """Simulates a DB schema stage."""
    logger.info("Running schema stage")
    await asyncio.sleep(1)
    return SchemaOutputs(result=SchemaResult(tables=5))


@durable(d=FromArg("d"))
async def build_stage(d: Path) -> BuildOutputs:
    """Simulates a build routes stage."""
    logger.info("Running build stage")
    await asyncio.sleep(3)
    return BuildOutputs(result=BuildResult(routes=12))


@register_world("plato-world-stage-tracking-test")
class StageTrackingTestWorld(BaseWorld[RunConfig]):
    """Runs multiple sequential durable stages to test stage tracking visibility."""

    name: ClassVar[str] = "stage-tracking-test"
    description: ClassVar[str] = "Stage tracking integration test"

    async def reset(self) -> Observation:
        logger.info("StageTrackingTestWorld reset")

        base_dir = Path("/tmp/stage-tracking-test")
        base_dir.mkdir(parents=True, exist_ok=True)

        # Run stages sequentially — each should appear in the Pipeline tab
        analysis = await analysis_stage(d=base_dir)
        logger.info("Analysis: %d entities, %d rels", analysis.result.entities, analysis.result.relationships)

        schema = await schema_stage(d=base_dir)
        logger.info("Schema: %d tables", schema.result.tables)

        build = await build_stage(d=base_dir)
        logger.info("Build: %d routes", build.result.routes)

        return Observation(
            data={
                "entities": analysis.result.entities,
                "tables": schema.result.tables,
                "routes": build.result.routes,
                "status": "ready",
            }
        )

    async def step(self) -> StepResult:
        return StepResult(
            observation=Observation(data={"status": "passed"}),
            done=True,
        )
