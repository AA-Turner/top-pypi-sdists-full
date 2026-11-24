"""A tool declared to return a KindModel is measured against THAT model, never a stale stored copy.

Live 2026-11-01 09:04-09:09 UTC (feedback 84721e9b): every successful kind_create and kind_get filed
``tool_output_contract_drift`` - "Additional properties are not allowed ('dry_run', 'names',
'requested_kind', 'status' were unexpected)" / "('found' was unexpected)". The tools returned exactly
their declared KindModels; the stored ``tool.definition.output_schema`` predated those fields.
"""

from __future__ import annotations

from matrx_ai.tools.kinds import result_kind_model
from matrx_ai.tools.models import ToolDefinition


def _stale(name: str) -> dict:
    schema = result_kind_model(name).model_json_schema()
    schema["properties"] = {k: v for k, v in schema["properties"].items() if k in ("kind", "message")}
    return schema


def test_a_stale_stored_schema_never_judges_a_declared_tool() -> None:
    for name, field in (("kind_create", "dry_run"), ("kind_get", "found")):
        tool = ToolDefinition(name=name, parameters={}, output_schema=_stale(name))
        _, output = tool.content_ir_contracts()
        assert output is not None
        assert field in output.json_schema["properties"], name


def test_an_undeclared_tool_keeps_its_stored_schema() -> None:
    stored = {"type": "object", "properties": {"x": {"type": "string"}}, "additionalProperties": False}
    tool = ToolDefinition(name="some_undeclared_tool_xyz", parameters={}, output_schema=stored)
    _, output = tool.content_ir_contracts()
    assert output is not None and output.json_schema["properties"] == stored["properties"]
