"""``dataset:update_row`` accepts the row the model actually sends.

Live defect (2026-10-01 17:49–17:50Z, org Compass, agent Compass Dispatch Assistant): the
provider schema declared ``data`` as an ARRAY of objects (the create shape), so for
``update_row`` the model could only send the row object as a JSON STRING. The wire model
decoded that string, but the dispatcher then read the RAW ``args`` and handed the string to
``usertable_update_row``, which answered "data must be a dict of field values." five times
and the run ended without an answer. The arguments below are copied from ``chat.tool_call``
rows cb819f35…, 3499029b… and a2c3c906… exactly.

Each shape is proven against the record-store arm, the one home every table has.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.tools.implementations import datasets_tools
from matrx_ai.tools.models import ToolContext

_TABLE_ID = "522c3ff1-7229-439c-be00-5b20492cc328"
_ROW_ID = "4347f5b9-f339-459e-b49f-f849cee89874"
_USER_ID = "33333333-3333-4333-8333-333333333333"

_FULL_ROW = {
    "move": "4466",
    "carrier": "Golden State Movers",
    "linehaul": "$3,210",
    "booking_status": "Under way",
    "shipper_reference": "CRA-22871",
}

# chat.tool_call cb819f35-c9d0-448f-a896-8df362f00567 — verbatim.
_LEDGER_STRING_ROW = {
    "data": '{"move": "4466", "carrier": "Golden State Movers", "linehaul": "$3,210", '
    '"booking_status": "Under way", "shipper_reference": "CRA-22871"}',
    "action": "update_row",
    "row_id": _ROW_ID,
    "dataset_id": _TABLE_ID,
}


class _Ctx(ToolContext):
    @property
    def user_id(self) -> str:
        return _USER_ID


def _ctx() -> _Ctx:
    return _Ctx(call_id="call-1", tool_name="dataset")


class _Arm:
    def __init__(self) -> None:
        self.writes: list[tuple[str, str, Any]] = []

    async def read_row(self, table_id: str, row_id: str) -> dict[str, Any]:
        return dict(_FULL_ROW, booking_status="Booked")

    async def update_row(self, table_id: str, row_id: str, data: Any) -> dict[str, Any]:
        self.writes.append((table_id, row_id, data))
        return {"updated_row_id": row_id}


@pytest.fixture
def home(monkeypatch):
    """The record-store arm. Returns a reader of what reached the store."""
    arm = _Arm()
    monkeypatch.setattr(datasets_tools, "_store_arm", lambda: arm)
    return lambda: [data for _t, _r, data in arm.writes]


@pytest.mark.asyncio
async def test_ledger_json_string_row_is_written(home):
    result = await datasets_tools.dataset(dict(_LEDGER_STRING_ROW), _ctx())

    assert result.success, result.error
    assert home() == [_FULL_ROW]


@pytest.mark.asyncio
async def test_real_object_row_is_written(home):
    args = dict(_LEDGER_STRING_ROW, data=dict(_FULL_ROW))
    result = await datasets_tools.dataset(args, _ctx())

    assert result.success, result.error
    assert home() == [_FULL_ROW]


@pytest.mark.asyncio
async def test_field_value_pairs_are_the_same_row(home):
    pairs = [{"field": k, "value": v} for k, v in _FULL_ROW.items()]
    result = await datasets_tools.dataset(dict(_LEDGER_STRING_ROW, data=pairs), _ctx())

    assert result.success, result.error
    assert home() == [_FULL_ROW]


@pytest.mark.asyncio
async def test_missing_data_names_the_shape_with_an_example(home):
    # chat.tool_call a2c3c906-5229-4f8c-82c7-561471b473fc — no `data` at all.
    args = {"action": "update_row", "row_id": _ROW_ID, "dataset_id": _TABLE_ID}
    result = await datasets_tools.dataset(args, _ctx())

    assert not result.success
    message = result.error.message
    assert "data" in message and "{" in message, message
    assert "whole row" in message or "every field" in message, message
    assert home() == []


@pytest.mark.asyncio
async def test_a_bare_string_is_refused_with_the_shape(home):
    result = await datasets_tools.dataset(
        dict(_LEDGER_STRING_ROW, data="booking_status = Under way"), _ctx()
    )

    assert not result.success
    assert '"booking_status"' in result.error.message or "{" in result.error.message
    assert home() == []


# ── the class: a dispatcher reads its wire model's COERCED values, never the raw args ──


@pytest.mark.asyncio
async def test_picklist_create_reads_the_decoded_items_not_the_string(monkeypatch):
    from matrx_ai.tools.implementations import picklists_tools

    seen: list[Any] = []

    async def create_simple(args: dict[str, Any], _ctx: Any):
        seen.append(args["labels"])
        return picklists_tools.ToolResult(success=True, output={"ok": True})

    monkeypatch.setattr(picklists_tools, "userlist_create_simple", create_simple)
    result = await picklists_tools.picklist(
        {
            "action": "create",
            "picklist_name": "Carrier booking status",
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
            "dataset_name": {"type": "string", "required": True, "description": "Name."},
        },
        "add_rows": {
            "rows": {"type": "array", "items": {"type": "object"}, "required": True,
                     "description": "Row objects to append."},
            "dataset_id": {"type": "string", "required": True, "description": "Dataset."},
        },
        "update_row": {
            "data": {"description": "Full replacement row data."},
            "row_id": {"type": "string", "required": True, "description": "Row."},
            "dataset_id": {"type": "string", "required": True, "description": "Dataset."},
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
