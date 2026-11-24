"""A dispatcher reads its wire model's decoded values, and a provider schema never narrows a per-action field.

Live defect (2026-10-01 17:49–17:50Z, org Compass, agent Compass Dispatch Assistant): the
provider schema declared ``data`` as an ARRAY of objects (the create shape), so for
``update_row`` the model could only send the row object as a JSON STRING, and the dispatcher
read the RAW ``args``. The ``table`` tool that defect hit was retired (custom-data PLAN C.12
step 9); the class it exposed is still guarded here for every dispatcher and every provider.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext

_USER_ID = "33333333-3333-4333-8333-333333333333"


class _Ctx(ToolContext):
    @property
    def user_id(self) -> str:
        return _USER_ID


def _ctx() -> _Ctx:
    return _Ctx(call_id="call-1", tool_name="pick_list")


# ── the class: a dispatcher reads its wire model's COERCED values, never the raw args ──


@pytest.mark.asyncio
async def test_picklist_create_reads_the_decoded_items_not_the_string(monkeypatch):
    from matrx_ai.tools.implementations import pick_list_tools

    seen: list[Any] = []

    async def create_simple(args: dict[str, Any], _ctx: Any):
        seen.append(args["labels"])
        return pick_list_tools.ToolResult(success=True, output={"ok": True})

    monkeypatch.setattr(pick_list_tools, "pick_list_create_simple", create_simple)
    result = await pick_list_tools.pick_list(
        {
            "action": "create",
            "pick_list_name": "Carrier booking status",
            "items": '["Booked", "Under way"]',
        },
        _ctx(),
    )

    assert result.success, result.error
    assert seen == [["Booked", "Under way"]]


# ── the declaration: the model is never told `data` is an array for update_row ──

#: ``tool.definition`` row ``dataset`` (57953f50…), read live 2026-10-01: the ROOT ``data``
#: says ``array`` of objects while both actions that carry it leave it untyped (``Any``).
_LIVE_DATASET_PARAMETERS: dict[str, Any] = {
    "action": {
        "enum": ["create", "add_rows", "update_row"],
        "type": "string",
        "required": True,
        "description": "The operation to perform.",
    },
    "data": {
        "type": "array",
        "items": {"type": "object"},
        "description": "Row objects. For action=create this seeds the dataset and defines "
        "columns from the first row. For action=update_row this is the full replacement "
        "row data.",
    },
    "rows": {"type": "array", "items": {"type": "object"}, "description": "Rows."},
    "$variants": {
        "create": {
            "data": {"description": "Seed row objects; first row defines columns."},
            "table_name": {"type": "string", "required": True, "description": "Name."},
        },
        "add_rows": {
            "rows": {"type": "array", "items": {"type": "object"}, "required": True,
                     "description": "Row objects to append."},
            "table_id": {"type": "string", "required": True, "description": "Dataset."},
        },
        "update_row": {
            "data": {"description": "Full replacement row data."},
            "row_id": {"type": "string", "required": True, "description": "Row."},
            "table_id": {"type": "string", "required": True, "description": "Dataset."},
        },
    },
}


@pytest.mark.parametrize("provider", ["anthropic", "openai", "google"])
def test_provider_schema_never_narrows_data_to_an_array(provider):
    from matrx_ai.tools.models import ToolDefinition

    tool = ToolDefinition(
        name="dataset", description="Datasets.", parameters=_LIVE_DATASET_PARAMETERS
    )
    schema = json.dumps(tool.get_provider_format(provider))
    fmt = tool.get_provider_format(provider)
    props = (
        fmt.get("input_schema")
        or fmt.get("parameters")
        or fmt.get("function", {}).get("parameters")
        or {}
    ).get("properties", {})
    assert "data" in props, schema
    data = props["data"]
    assert str(data.get("type", "")).lower() != "array", data
    # a field whose type is the same on every action keeps it
    assert str(props["rows"].get("type", "")).lower() == "array", props["rows"]
