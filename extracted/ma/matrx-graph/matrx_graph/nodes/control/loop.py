"""control.loop — re-invoke the target until an exit condition holds.

Works via ``ctx.send`` — each iteration dispatches a fresh invocation of
the target node with the current accumulator. The target routes its output
back to the loop over a plain DATA edge (the return edge).

Loop state is ENGINE-carried (ENGINE_SPEC §9): the body Send pushes a
``LoopFrame`` onto the child's ``loop_stack``; when the body chain's
delivery returns to this node, the engine pops the frame and INJECTS
``iteration`` into the delivered payload (wrapping the body output as
``{"accumulator": ...}`` when the return edge has no mappings). The body
NEVER needs to echo ``iteration`` — ``inputs.iteration`` here is engine
truth, so ``exit_expression``/``max_iterations`` always terminate a
well-formed loop (never the old ``max_steps`` FAILED death, audit E7).
The spec declares ``default_join_policy='any'`` so the return edge
re-fires the loop per delivery instead of deadlocking the §3 join.

Exits on one of:
- ``iterations >= max_iterations``  (hard safety bound)
- ``exit_expression`` evaluates true over ``inputs`` (sandbox as branch)
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, EdgeKind, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class LoopInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    iteration: int = Field(
        default=0, description="The current loop iteration counter (starts at 0)."
    )
    accumulator: JsonValue = Field(
        default=None,
        description="The value carried across iterations (what the loop body returned last).",
    )


class LoopOutput(KindModel, kind="loop_iteration_result"):
    iteration: int = Field(description="The iteration number after this pass.")
    done: bool = Field(
        description="True when the exit condition or max_iterations was met — the loop stops."
    )
    accumulator: JsonValue = Field(
        default=None,
        description="The value carried to the next iteration, or the final result when done.",
    )


class LoopConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_node_id: str = Field(
        min_length=1,
        description="Node id to invoke each iteration.",
        json_schema_extra=field_extras(widget="text"),
    )
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Hard cap — prevents runaway loops.",
        json_schema_extra=field_extras(widget="number"),
    )
    exit_expression: str = Field(
        default="inputs['iteration'] >= 1",
        description="Sandboxed Python expression. Loop exits when this is truthy.",
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="inputs['accumulator']['total'] > 100",
        ),
    )


class LoopExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.loop",
        category=NodeCategory.CONTROL,
        display_name="Loop",
        description="Repeat a step until a condition is met.",
        input_schema=LoopInput,
        output_schema=LoopOutput,
        config_schema=LoopConfig,
        output_kind="loop_iteration_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(
                id="done",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL, EdgeKind.DATA),
                required=False,
            ),
            HandleSpec(
                id="iterate",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL, EdgeKind.DATA),
                required=False,
            ),
        ),
        determinism=ActionTier.PURE,
        icon="repeat",
        # §9: the return edge delivers once per iteration — the loop must
        # re-fire per delivery ('all' would deadlock the first firing, which
        # can never have a return delivery yet).
        default_join_policy="any",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: LoopInput,
        config: LoopConfig,
    ) -> NodeResult[LoopOutput]:
        payload = inputs.model_dump(mode="json")
        hit_cap = inputs.iteration >= config.max_iterations
        exit_ok = bool(safe_eval(config.exit_expression, payload))
        done = hit_cap or exit_ok

        if done:
            ctx.emit("done", {"accumulator": inputs.accumulator, "iteration": inputs.iteration})
        else:
            ctx.send(
                config.target_node_id,
                {
                    "iteration": inputs.iteration + 1,
                    "accumulator": inputs.accumulator,
                },
            )
            ctx.emit("iterate", {"iteration": inputs.iteration + 1})

        return success(
            LoopOutput(
                iteration=inputs.iteration,
                done=done,
                accumulator=inputs.accumulator,
            )
        )
