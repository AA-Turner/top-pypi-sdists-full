"""A step handed empty or wrong input fails as a typed NodeInputValidationError naming the field, not a raw pydantic dump
(live 2026-11-15: workflow_run_failed on CreateTaskItem / AddressesEnsureInput)."""

from pydantic import BaseModel, ConfigDict

from matrx_graph.errors import NodeInputValidationError
from matrx_graph.executor.scheduler import _parse_step_inputs, _typed_input_error


class CreateTaskItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    organization_id: str


def test_empty_input_names_the_missing_fields_in_plain_words():
    _, err, _ = _parse_step_inputs(CreateTaskItem, {"foo": "x"}, "t")
    assert err is not None and "validation error" in str(err)  # the raw form this replaces
    typed = _typed_input_error("make_task", err)
    assert isinstance(typed, NodeInputValidationError)
    text = str(typed)
    assert "make_task" in text and "title: is required" in text and "organization_id: is required" in text
    assert "foo: is not an input this step accepts" in text
    assert "pydantic" not in text and "validation error" not in text


def test_a_non_validation_error_passes_through():
    boom = RuntimeError("x")
    assert _typed_input_error("n", boom) is boom
