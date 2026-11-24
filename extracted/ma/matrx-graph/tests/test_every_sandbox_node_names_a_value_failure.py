"""A zero divisor or mixed-kind operands in ANY sandbox node is a named Failure, never a raw run error.

math.evaluate and data.transform were fixed first (division_by_zero, operand_type_mismatch); the
conversion now lives in ``safe_eval`` (ExpressionFailure), so branch, assert, filter and rules —
which call the same sandbox — answer the same named codes instead of a run-level engine_error.
"""

from __future__ import annotations

import pytest

from matrx_graph.nodes.control.branch import BranchConfig, BranchExecutor, BranchInput
from matrx_graph.nodes.data.assert_ import AssertConfig, AssertExecutor, AssertInput
from matrx_graph.nodes.data.filter import FilterConfig, FilterExecutor, FilterInput
from matrx_graph.nodes.data.rules import RulesConfig, RulesExecutor, RulesInput
from matrx_graph.types.result import Failure

ZERO = "inputs['a'] / inputs['b'] > 1"
MIXED = "inputs['a'] + inputs['b'] > 1"


class _Ctx:
    def emit(self, *a: object, **k: object) -> None: ...


def _mixed_cases() -> list[tuple[str, str]]:
    return [("division_by_zero", ZERO), ("operand_type_mismatch", MIXED)]


def _values(code: str) -> dict[str, object]:
    return {"a": 6, "b": 0} if code == "division_by_zero" else {"a": 1, "b": {"value": 2}}


@pytest.mark.parametrize(("code", "expr"), _mixed_cases())
async def test_branch(code: str, expr: str) -> None:
    result = await BranchExecutor().execute(
        _Ctx(), BranchInput.model_validate(_values(code)), BranchConfig(predicate=expr)  # type: ignore[arg-type]
    )
    assert isinstance(result, Failure)
    assert result.error.code == code


@pytest.mark.parametrize(("code", "expr"), _mixed_cases())
async def test_assert(code: str, expr: str) -> None:
    result = await AssertExecutor().execute(
        None, AssertInput.model_validate(_values(code)), AssertConfig(predicate=expr, message="x")  # type: ignore[arg-type]
    )
    assert isinstance(result, Failure)
    assert result.error.code == code


@pytest.mark.parametrize(("code", "expr"), _mixed_cases())
async def test_filter(code: str, expr: str) -> None:
    item = _values(code)
    result = await FilterExecutor().execute(
        _Ctx(), FilterInput(items=[item]), FilterConfig(predicate=expr)  # type: ignore[arg-type]
    )
    assert isinstance(result, Failure)
    assert result.error.code == code


@pytest.mark.parametrize(("code", "expr"), _mixed_cases())
async def test_rules(code: str, expr: str) -> None:
    result = await RulesExecutor().execute(
        _Ctx(),  # type: ignore[arg-type]
        RulesInput.model_validate(_values(code)),
        RulesConfig.model_validate({"rules": [{"when": expr, "then": {"label": "x"}}]}),
    )
    assert isinstance(result, Failure)
    assert result.error.code == code
