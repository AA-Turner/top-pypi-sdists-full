from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, EdgeKind, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


class BranchInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: JsonValue = Field(
        default=None,
        description="The incoming payload the predicate is evaluated against "
        "(available to the expression as `inputs`).",
    )


class BranchOutput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "input payload passthrough alongside the routing direction"
        },
    )

    direction: str = Field(description="Which handle the run took — 'true' or 'false'.")
    value: JsonValue = Field(
        default=None,
        description="The input value, passed through so downstream steps still receive it.",
    )


class BranchConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predicate: str = Field(
        min_length=1,
        description=(
            "Python expression evaluated against a dict of `inputs`. Result is "
            "coerced to bool; True routes to the 'true' handle, False to 'false'. "
            "Sandbox forbids function calls and attribute access."
        ),
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="inputs['value'] > 0",
            help="Safe Python subset. `inputs` is the incoming payload.",
        ),
    )


class BranchExecutor:
    """Route flow to 'true' or 'false' based on a sandboxed predicate.

    The node emits on the 'true' or 'false' output handle. Edges attached to
    the non-taken handle do not fire. Determinism is PURE — the decision is
    a function of inputs alone.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.branch",
        category=NodeCategory.CONTROL,
        display_name="Branch",
        description="Choose one of two paths based on a condition.",
        input_schema=BranchInput,
        output_schema=BranchOutput,
        config_schema=BranchConfig,
        output_kind="branch_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(
                id="true",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL, EdgeKind.DATA),
                required=False,
            ),
            HandleSpec(
                id="false",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.CONDITIONAL, EdgeKind.DATA),
                required=False,
            ),
        ),
        determinism=ActionTier.PURE,
        icon="git-branch",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: BranchInput,
        config: BranchConfig,
    ) -> NodeResult[BranchOutput]:
        # The predicate reads every declared field (an unset ``value`` reads as None), but what
        # travels on is exactly what arrived: the branch never adds its own ``value`` default to
        # the payload. A strict downstream state (extra=forbid) refused that stray key — live
        # 2026-10-22, agent_build "Tell the door" crashed on ``value: None``.
        received = inputs.model_dump(mode="json", exclude_unset=True)
        went_true = bool(safe_eval(config.predicate, inputs.model_dump(mode="json")))
        direction = "true" if went_true else "false"
        ctx.emit(direction, received)

        # The emitted payload is the unchanged upstream value. The returned node result is a
        # separate branch_result, with its own marker and authoritative routing direction.
        result_payload = {**received, "direction": direction, "__kind": "branch_result"}
        return success(BranchOutput.model_validate(result_payload))
