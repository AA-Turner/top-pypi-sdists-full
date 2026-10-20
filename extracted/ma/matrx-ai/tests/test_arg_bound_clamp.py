"""Out-of-range numbers are clamped, never refused; stripped bounds reach the model.

2026-10-09: the Applet builder called ``ask_person`` with ``timeout_seconds``
under the floor of 30. The OpenAI strict schema had dropped ``minimum`` without
a word, the executor refused the call, and the person saw "invalid arguments".
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, Field, ValidationError

from matrx_ai.tools._dispatch_util import clamp_out_of_range_numbers, constraint_sentence
from matrx_ai.tools.models import ToolDefinition


class _Args(BaseModel):
    message: str
    timeout_seconds: int | None = Field(default=None, ge=30, le=600)
    ratio: float = Field(default=0.5, gt=0, lt=1)
    count: int = Field(default=1, gt=0)


def _errors(args: dict) -> ValidationError:
    with pytest.raises(ValidationError) as info:
        _Args.model_validate(args)
    return info.value


def test_below_floor_clamps_to_floor() -> None:
    args = {"message": "hi", "timeout_seconds": 10}
    out = clamp_out_of_range_numbers(args, _errors(args))
    assert out is not None
    fixed, changes = out
    assert fixed["timeout_seconds"] == 30
    assert changes == [("timeout_seconds", 10, 30)]
    _Args.model_validate(fixed)


def test_above_ceiling_clamps_to_ceiling() -> None:
    args = {"message": "hi", "timeout_seconds": 99999}
    fixed, _ = clamp_out_of_range_numbers(args, _errors(args))  # type: ignore[misc]
    assert fixed["timeout_seconds"] == 600


def test_exclusive_integer_bound_moves_one_step_inside() -> None:
    args = {"message": "hi", "count": 0}
    fixed, _ = clamp_out_of_range_numbers(args, _errors(args))  # type: ignore[misc]
    assert fixed["count"] == 1
    _Args.model_validate(fixed)


def test_non_number_is_left_to_refuse() -> None:
    args = {"message": "hi", "timeout_seconds": "soon"}
    assert clamp_out_of_range_numbers(args, _errors(args)) is None


def test_strict_schema_carries_the_bound_in_the_description() -> None:
    tool = ToolDefinition(
        name="ask_person_like",
        description="d",
        parameters={
            "timeout_seconds": {
                "type": "integer",
                "minimum": 30,
                "maximum": 600,
                "description": "Stop waiting after this many seconds.",
            }
        },
    )
    strict = tool._build_json_schema(strip_openai_unsupported=True)
    prop = strict["properties"]["timeout_seconds"]
    assert "minimum" not in prop
    # The bound is dropped and recorded, NEVER appended to the description as prose.
    assert prop["description"] == "Stop waiting after this many seconds."
    loose = tool._build_json_schema()
    assert loose["properties"]["timeout_seconds"]["minimum"] == 30


def test_constraint_sentence_empty_without_bounds() -> None:
    assert constraint_sentence({"type": "string"}) == ""
