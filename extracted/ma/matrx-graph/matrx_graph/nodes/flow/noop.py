"""``flow.noop`` — a pass-through junction / annotation point.

Authors use these constantly for wiring clarity: fan several edges into one
junction and out again, park a note on a spot in the graph, or reserve a hook
where a real step will land later. It does nothing on purpose, and the payload
flows through byte-identical — so it declares no kinds and lets runtime
``__kind`` propagation carry the payload's identity.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success


class NoopInput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "pass-through junction; the payload flows unchanged"
        },
    )


class NoopOutput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "pass-through junction; the payload flows unchanged"
        },
    )


class NoopConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note: str = Field(
        default="",
        description=(
            "Optional annotation shown on the canvas. Purely for the humans "
            "reading the workflow — it never touches the data."
        ),
    )


class NoopExecutor:
    """Return the input payload untouched."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="flow.noop",
        category=NodeCategory.CONTROL,
        display_name="Pass Through",
        description=(
            "Does nothing — data flows straight through. Useful as a junction "
            "for tidy wiring, or as a place to leave a note."
        ),
        input_schema=NoopInput,
        output_schema=NoopOutput,
        config_schema=NoopConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        # PASS-THROUGH BY DESIGN — the payload flows out byte-identical, so
        # this node's real output shape is whatever reached it. Declared
        # dynamic (GAP 2, KINDS_EVERYWHERE_PLAN §10g) so the coverage board
        # and the boundary lint read the same posture the burndown ledger
        # already recorded; runtime __kind propagation carries identity.
        dynamic_output=True,
        determinism=ActionTier.PURE,
        icon="circle-dot",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: NoopInput,
        config: NoopConfig,
    ) -> NodeResult[NoopOutput]:
        _ = ctx, config
        return success(NoopOutput(**inputs.model_dump(mode="json")))
