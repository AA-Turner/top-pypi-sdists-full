"""The "Run an Action" step's `payload` holds the picked Action's own inputs, required ones included: the step form
must show it open (priority "primary"), never fold it under "More options - 1 more" (proof desk, 2026-11)."""

from __future__ import annotations

from matrx_graph.nodes.tool.call import ToolCallInput


def test_the_payload_is_a_primary_field() -> None:
    schema = ToolCallInput.model_json_schema()
    assert schema["properties"]["payload"]["ui:priority"] == "primary"
