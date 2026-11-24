"""A zero divisor in Calculate (``math.evaluate``) is a named, plain-language Failure.

Live 2026-11-13: workflow runs died with ``evaluation_failed: ZeroDivisionError:
division by zero`` — a raw Python exception name was the only thing the author read.
Every arithmetic operator that can divide (``/``, ``//``, ``%``) shares the one
sandbox, so one code covers the class; the raw text rides ``technical``.
"""

from __future__ import annotations

import pytest

from matrx_graph.nodes.math_.evaluate import (
    MathEvaluateConfig,
    MathEvaluateExecutor,
    MathEvaluateInput,
)
from matrx_graph.types.result import Failure, Success


@pytest.mark.parametrize("op", ["/", "//", "%"])
async def test_a_zero_divisor_fails_as_division_by_zero(op: str) -> None:
    result = await MathEvaluateExecutor().execute(
        None,  # type: ignore[arg-type]  # the executor never reads ctx
        MathEvaluateInput(a=6, b=0),
        MathEvaluateConfig(expression=f"inputs['a'] {op} inputs['b']"),
    )
    assert isinstance(result, Failure)
    assert result.error.code == "division_by_zero"
    assert "ZeroDivisionError" not in result.error.message
    assert "zero" in result.error.message
    assert result.error.technical and "ZeroDivisionError" in result.error.technical


async def test_a_nonzero_divisor_still_divides() -> None:
    result = await MathEvaluateExecutor().execute(
        None,  # type: ignore[arg-type]
        MathEvaluateInput(a=6, b=4),
        MathEvaluateConfig(expression="inputs['a'] / inputs['b']"),
    )
    assert isinstance(result, Success)
    assert result.result.value == 1.5
