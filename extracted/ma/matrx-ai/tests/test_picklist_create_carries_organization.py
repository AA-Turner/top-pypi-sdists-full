"""`picklist:create` carries the organization — or holds.

With no organization on the run, nothing is picked on the person's behalf: the
tool answers with the platform's one ``organization_required`` hold. (Its sibling
`table:create` was retired with the `table` tool, custom-data PLAN C.12 step 9.)

Realistic case: a dental clinic's front desk keeps a list of the carriers it verifies.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.models import ToolContext

PERSON = "0f6c2a3e-1b4d-4e5f-8a9b-7c6d5e4f3a21"


def _ctx(monkeypatch: pytest.MonkeyPatch, org: str | None) -> ToolContext:
    monkeypatch.setattr(ToolContext, "user_id", property(lambda self: PERSON))
    monkeypatch.setattr(ToolContext, "organization_id", property(lambda self: org))
    return ToolContext(call_id="call-front-desk")


@pytest.mark.asyncio
async def test_picklist_create_without_an_organization_is_the_same_hold(monkeypatch):
    from matrx_ai.tools.implementations.pick_list_tools import pick_list

    ctx = _ctx(monkeypatch, None)
    result = await pick_list(
        {"action": "create", "pick_list_name": "Carriers we verify",
         "items": ["Blue Shield PPO", "Delta Dental", "Aetna DMO"]},
        ctx,
    )
    assert not result.success
    assert result.error.error_type == "organization_required"
