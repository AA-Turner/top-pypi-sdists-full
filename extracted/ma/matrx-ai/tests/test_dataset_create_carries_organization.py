"""`dataset:create` (and its sibling `picklist:create`) carry the organization — or hold.

A dataset is born in the record store, in the organization the conversation carries
(the store arm makes it under the ambient person and organization).

With no organization on the run, nothing is picked on the person's behalf: the
tool answers with the platform's one ``organization_required`` hold.

Realistic case: a dental clinic's front desk turns its insurance call sheet into
a dataset, and a list of the carriers it verifies.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai._ext import configure_ext
from matrx_ai.tools.models import ToolContext

ORG = "5b0e4a51-8d2f-4c52-9d0a-2f3c1e7a9b10"
PERSON = "0f6c2a3e-1b4d-4e5f-8a9b-7c6d5e4f3a21"
CALL_SHEET = [
    {"Patient": "Maria Lopez", "Carrier": "Blue Shield PPO", "Verified": "no"},
    {"Patient": "Dev Patel", "Carrier": "Delta Dental", "Verified": "yes"},
]


class FakeStoreArm:
    """The record-store arm's ``create``, recording what the tool asked it to make."""

    made: list[dict[str, Any]] = []

    async def create(self, *, name: str, description: str, data: list) -> dict[str, Any]:
        FakeStoreArm.made.append({"name": name, "rows": len(data)})
        return {"table_id": "c0ffee00-0000-4000-8000-000000000001", "table_name": name,
                "description": description, "row_count": len(data), "field_count": 3,
                "already_existed": False}


def _ctx(monkeypatch: pytest.MonkeyPatch, org: str | None) -> ToolContext:
    monkeypatch.setattr(ToolContext, "user_id", property(lambda self: PERSON))
    monkeypatch.setattr(ToolContext, "organization_id", property(lambda self: org))
    FakeStoreArm.made = []
    configure_ext(dataset_store_arm=FakeStoreArm())
    return ToolContext(call_id="call-front-desk")


@pytest.mark.asyncio
async def test_dataset_create_with_an_organization_is_made_in_the_store(monkeypatch):
    from matrx_ai.tools.implementations.datasets_tools import dataset

    ctx = _ctx(monkeypatch, ORG)
    result = await dataset(
        {"action": "create", "dataset_name": "Insurance verification — week of Sep 28",
         "data": CALL_SHEET},
        ctx,
    )
    assert result.success, result.error
    assert FakeStoreArm.made == [{"name": "Insurance verification — week of Sep 28", "rows": 2}]


@pytest.mark.asyncio
async def test_dataset_create_without_an_organization_is_held(monkeypatch):
    from matrx_connect.org_hold import assert_no_default_org_wording

    from matrx_ai.tools.implementations.datasets_tools import dataset

    ctx = _ctx(monkeypatch, None)
    result = await dataset(
        {"action": "create", "dataset_name": "Insurance verification", "data": CALL_SHEET}, ctx
    )
    assert not result.success
    assert result.error.error_type == "organization_required"
    assert result.output["hold"]["details"]["hold"] == "organization_required"
    assert FakeStoreArm.made == []
    assert_no_default_org_wording(result.error.message + (result.error.suggested_action or ""))


@pytest.mark.asyncio
async def test_picklist_create_without_an_organization_is_the_same_hold(monkeypatch):
    from matrx_ai.tools.implementations.picklists_tools import picklist

    ctx = _ctx(monkeypatch, None)
    result = await picklist(
        {"action": "create", "picklist_name": "Carriers we verify",
         "items": ["Blue Shield PPO", "Delta Dental", "Aetna DMO"]},
        ctx,
    )
    assert not result.success
    assert result.error.error_type == "organization_required"
