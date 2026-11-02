"""``flow.throttle`` — pace fan-out items through a rate-limited section.

Place it between a dispatcher (``control.map``, a kind-filtered ``each`` edge,
``control.work_queue``) and a rate-limited step: every fanned item passes
through, spaced ``interval_seconds`` apart. The spacing is deterministic —
item *i* of a dispatch waits ``i × interval`` from the moment its super-step
starts — so 20 items with a 3-second interval leave this node over one minute
instead of as one burst.

Durability posture: the wait is inline (all items of a dispatch execute in ONE
super-step, so the step simply takes as long as the pacing demands). A worker
that dies mid-step re-runs the step from the last checkpoint — items that
already completed replay from their recorded outcomes instantly; unfinished
items re-wait their own slot. Nothing is lost or doubled; the worst case is
re-waiting. Long delays are ``flow.sleep``'s job — the schema caps the total
window a throttle may spread items across.

Pass-through: the payload flows unchanged; no kinds declared (runtime
``__kind`` propagation carries identity).
"""

from __future__ import annotations

import asyncio
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

#: Ceiling on ONE item's computed delay (index × interval): one hour. Keeps a
#: fat fan-out with a generous interval from pinning a worker slot for a day —
#: that shape wants batching (data.batch) or flow.sleep, and the failure says so.
MAX_ITEM_DELAY_SECONDS = 3600.0


class ThrottleInput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "pass-through pacing node; the payload flows unchanged"
        },
    )


class ThrottleOutput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "pass-through pacing node; the payload flows unchanged"
        },
    )


class ThrottleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    interval_seconds: float = Field(
        gt=0,
        le=300,
        description=(
            "Minimum spacing between items. Item N of a fan-out waits "
            "N × interval before continuing, so items leave this step at a "
            "steady rate instead of all at once."
        ),
    )


class ThrottleExecutor:
    """Deterministic per-item spacing: delay = item_index × interval."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="flow.throttle",
        category=NodeCategory.CONTROL,
        display_name="Slow Down",
        description=(
            "Space out items so the next step isn't hit all at once — useful "
            "in front of rate-limited services."
        ),
        input_schema=ThrottleInput,
        output_schema=ThrottleOutput,
        config_schema=ThrottleConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        # PASS-THROUGH BY DESIGN — the payload flows through unchanged (see
        # module docstring). Declared dynamic (GAP 2, KINDS_EVERYWHERE_PLAN
        # §10g) so runtime __kind propagation is the recorded posture rather
        # than an undeclared NULL.
        dynamic_output=True,
        determinism=ActionTier.NON_DETERMINISTIC,
        icon="gauge",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ThrottleInput,
        config: ThrottleConfig,
    ) -> NodeResult[ThrottleOutput]:
        delay = ctx.item_index * float(config.interval_seconds)
        if delay > MAX_ITEM_DELAY_SECONDS:
            return failure(
                "throttle_window_exceeded",
                f"item {ctx.item_index} would wait {delay:.0f}s (> "
                f"{MAX_ITEM_DELAY_SECONDS:.0f}s). Split the list with "
                "data.batch or lower the interval — a wait this long belongs "
                "to flow.sleep.",
            )
        if delay > 0:
            await asyncio.sleep(delay)
        return success(ThrottleOutput(**inputs.model_dump(mode="json")))
