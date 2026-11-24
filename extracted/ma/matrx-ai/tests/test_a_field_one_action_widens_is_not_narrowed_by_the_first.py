"""records record_delete takes ``record_id`` as one id OR a list; record_read takes one id.

Live 2026-11-14 19:45Z (conversation 5ae00046…): the model sent ``record_delete`` with a list,
the tool ran it, and the flattened Content IR input contract (first action's ``string``)
refused it — ToolInputContractDrift. The contract must accept the widest action's shape.
"""

from __future__ import annotations

from matrx_ai.tools.models import ToolDefinition

_IDS = ["1f9def6b-80ef-4b26-b416-dd7ee188a587", "21a0440b-5141-4c31-a131-7a678d500c3b"]


def _tool() -> ToolDefinition:
    return ToolDefinition(
        name="records",
        tool_id="30cf4ddd-d9e6-4f43-af3a-595f467bd661",
        parameters={
            "action": {"enum": ["record_read", "record_delete"], "type": "string", "required": True},
            "$variants": {
                "record_read": {
                    "action": {"type": "string", "enum": ["record_read"]},
                    "record_id": {"type": "string", "default": None, "description": "One record."},
                },
                "record_delete": {
                    "action": {"type": "string", "enum": ["record_delete"]},
                    "record_id": {
                        "anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}],
                        "required": True,
                        "description": "A record or a list of records.",
                    },
                },
            },
        },
    )


def test_the_contract_accepts_a_list_for_the_action_that_takes_one() -> None:
    from matrx_graph.contract_kinds import check_schema

    schema = _tool()._build_json_schema(contract=True)
    for value in ("one-id", _IDS):
        verdict = check_schema({"action": "record_delete", "record_id": value}, schema)
        assert verdict.errors == [], verdict.errors
