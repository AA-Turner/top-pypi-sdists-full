"""Regression coverage for typed tool lifecycle payloads."""

from __future__ import annotations

import pytest

from matrx_connect.context.tool_event_data import ToolCompletedData


@pytest.mark.parametrize(
    "result",
    [
        None,
        "done",
        42,
        3.5,
        True,
        [1, "two", False],
        {"answer": 42, "items": [1, 2]},
    ],
)
def test_tool_completed_accepts_every_json_result_shape(result) -> None:
    assert ToolCompletedData(result=result).model_dump()["result"] == result
