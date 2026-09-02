from __future__ import annotations

import math
import time
from typing import Any

from matrx_ai.tools.arg_models.math_args import CalculateArgs
from matrx_ai.tools.kinds.execution import CalculationResult
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

SAFE_MATH_NAMES: dict[str, Any] = {
    k: getattr(math, k) for k in dir(math) if not k.startswith("_")
}
SAFE_MATH_NAMES.update(
    {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "int": int,
        "float": float,
    }
)


async def math_calculate(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    from matrx_ai.tools._generated_declarations import MathCalculateArgs
    MathCalculateArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    parsed = CalculateArgs(**args)

    try:
        result = eval(parsed.expression, {"__builtins__": {}}, SAFE_MATH_NAMES)
        return ToolResult(
            success=True,
            # KindModel result (KIND_TOOL_LEDGER): `__kind` rides the payload.
            output=CalculationResult(
                expression=parsed.expression,
                result=str(result),
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="calculate",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="evaluation",
                message=f"Failed to evaluate expression: {exc}",
                suggested_action="Check the expression syntax. Use standard math operations and functions.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="calculate",
            call_id=ctx.call_id,
        )
