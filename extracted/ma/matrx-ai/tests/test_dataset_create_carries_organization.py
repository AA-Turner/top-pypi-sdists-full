"""`dataset:create` (and its sibling `picklist:create`) carry the organization — or hold.

Verifier, 2026-09-26: ``dataset:create`` died on a null ``organization_id`` on
``workbench.udt_datasets``: the tool built its creator from the person alone, so
the insert never named the organization the conversation was working in. The
fake creator below has the host creator's real shape (``organization_id`` is
keyword-only and the insert refuses a missing one exactly as Postgres does).

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


class FakeDatasetCreator:
    """The host creator's shape (user_data/dataset_creator.py), with the DB's refusal."""

    made: list[dict[str, Any]] = []

    def __init__(self, user_id: str, *, organization_id: str | None = None) -> None:
        self.user_id = user_id
        self.organization_id = organization_id

    def create_table_from_data(self, data: list, table_name: str, description: str | None = None,
                               is_public: bool = False, batch_size: int = 50) -> dict[str, Any]:
        if not self.organization_id:
            raise RuntimeError(
                'null value in column "organization_id" of relation "udt_datasets" '
                "violates not-null constraint"
            )
        FakeDatasetCreator.made.append({"organization_id": self.organization_id, "name": table_name})
        return {"success": True, "table_id": "c0ffee00-0000-4000-8000-000000000001",
                "table_name": table_name, "row_count": len(data), "field_count": 3}


def _ctx(monkeypatch: pytest.MonkeyPatch, org: str | None) -> ToolContext:
    monkeypatch.setattr(ToolContext, "user_id", property(lambda self: PERSON))
    monkeypatch.setattr(ToolContext, "organization_id", property(lambda self: org))
    FakeDatasetCreator.made = []
    configure_ext(DatasetCreator=FakeDatasetCreator)
    return ToolContext(call_id="call-front-desk")


@pytest.mark.asyncio
@pytest.mark.parametrize("typed", [False, True])
async def test_dataset_create_writes_the_carried_organization(monkeypatch, typed):
    from matrx_ai.tools.implementations.datasets_tools import dataset

    ctx = _ctx(monkeypatch, ORG)
    result = await dataset(
        {"action": "create", "dataset_name": "Insurance verification — week of Sep 28",
         "data": CALL_SHEET, "typed": typed},
        ctx,
    )
    assert result.success, result.error
    assert FakeDatasetCreator.made == [
        {"organization_id": ORG, "name": "Insurance verification — week of Sep 28"}
    ]


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
    assert FakeDatasetCreator.made == []
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
