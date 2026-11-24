"""An operand-type mismatch in Calculate / Transform is a named, plain-language Failure.

Live 2026-11-13 22:28Z: a Transform ``{'v': sum(inputs['values'])}`` over a For-each gather
(each value is a wrapped ``{"value": n}`` object) died as a run-level engine_error
``TypeError: unsupported operand type(s) for +: 'int' and 'dict'``.
"""

from __future__ import annotations

import pytest

from matrx_graph.nodes.data.transform import TransformConfig, TransformExecutor, TransformInput
from matrx_graph.nodes.math_.evaluate import MathEvaluateConfig, MathEvaluateExecutor, MathEvaluateInput
from matrx_graph.types.result import Failure


async def test_transform_sum_over_wrapped_values_is_named() -> None:
    result = await TransformExecutor().execute(
        None,  # type: ignore[arg-type]
        TransformInput(values=[{"value": 1}, {"value": 2}]),
        TransformConfig(expression="{'v': sum(inputs['values'])}"),
    )
    assert isinstance(result, Failure)
    assert result.error.code == "operand_type_mismatch"
    assert "'values'" in result.error.message and "object" in result.error.message
    assert "TypeError" not in result.error.message
    assert result.error.technical and "TypeError" in result.error.technical


@pytest.mark.parametrize("op", ["+", "-", "/", "<"])
async def test_calculate_number_with_text_is_named(op: str) -> None:
    result = await MathEvaluateExecutor().execute(
        None,  # type: ignore[arg-type]
        MathEvaluateInput(a=1, b="x"),
        MathEvaluateConfig(expression=f"inputs['a'] {op} inputs['b']"),
    )
    assert isinstance(result, Failure)
    assert result.error.code == "operand_type_mismatch"
    assert "'a' is number" in result.error.message and "'b' is text" in result.error.message
