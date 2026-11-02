"""``math.evaluate`` — safe arithmetic over the node's inputs.

The evaluator is the ONE existing sandbox (``matrx_graph.nodes._sandbox
.safe_eval``) — the same restricted-AST subset ``data.transform`` /
``control.branch`` / ``data.filter`` already speak, with its regression guard.
Never ``eval``. The sandbox deliberately excludes ``**`` (``ast.Pow`` — a tiny
expression can allocate gigabytes) and attribute access; ``+ - * / % //``,
comparisons, conditionals, and the numeric helpers (``abs``, ``min``, ``max``,
``sum``, ``round``, ``int``, ``float``, ``len``) are all available.

The result must be a NUMBER — a non-numeric result is a node Failure, because
"Calculate" returning a list is an authoring mistake the author should hear
about, not data downstream should choke on. Output is the canonical ``Value``
archetype (kind ``value``), same as ``data.parse_json``.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.types.canonical_payloads import Value
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class MathEvaluateInput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": (
                "the expression references whatever numeric fields arrive; "
                "the contract is the config expression, not a fixed field set"
            )
        },
    )


class MathEvaluateConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expression: str = Field(
        min_length=1,
        description=(
            "Arithmetic expression over this node's inputs, e.g. "
            "``inputs['subtotal'] * (1 + inputs['tax_rate'])`` or "
            "``round(inputs['score'] / inputs['total'] * 100, 1)``. "
            "The result must be a number."
        ),
    )


class MathEvaluateExecutor:
    """Sandbox-evaluate an arithmetic expression; the result must be numeric."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="math.evaluate",
        category=NodeCategory.DATA,
        display_name="Calculate",
        description="Do arithmetic on incoming numbers and pass the result on.",
        input_schema=MathEvaluateInput,
        output_schema=Value[JsonValue],
        output_kind="value",
        config_schema=MathEvaluateConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="calculator",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: MathEvaluateInput,
        config: MathEvaluateConfig,
    ) -> NodeResult[Value[JsonValue]]:
        _ = ctx
        payload = inputs.model_dump(mode="json")
        try:
            result = safe_eval(config.expression, payload)
        except ExecutionError as e:
            return failure("expression_invalid", str(e))
        except Exception as e:  # noqa: BLE001 — user expression over user data
            return failure("evaluation_failed", f"{type(e).__name__}: {e}")
        if isinstance(result, bool) or not isinstance(result, int | float):
            return failure(
                "non_numeric_result",
                f"expression produced {type(result).__name__!s}, not a number "
                "— Calculate is for arithmetic; use Transform for reshaping.",
            )
        return success(Value[JsonValue](value=result))
