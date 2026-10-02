"""A schedule belongs to the organization of the request that created it.

``scheduler.sch_task`` and ``scheduler.sch_trigger`` carry ``organization_id``
NOT NULL with no default and no stamping trigger (Data Doctrine, 2026-09-19:
nothing may choose an organization for the caller). The create routes wrote
neither, so every schedule create died 23502 in production while the fake —
which accepted a missing organization — kept these routes green.
"""

from __future__ import annotations

import pytest

from .conftest import TEST_ORGANIZATION_ID

pytestmark = pytest.mark.asyncio

_CRON = {"type": "cron", "config": {"expression": "0 9 * * *", "timezone": "UTC"}}


async def test_task_and_trigger_carry_the_request_organization(client, fake_supabase):
    payload = {
        "kind": "agent",
        "title": "Morning digest",
        "agent_task": {"agent_id": "agent-1", "prompt": "Summarize"},
        "trigger": _CRON,
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)
    assert res.status_code == 201, res.text
    assert fake_supabase.rows["sch_task"][0]["organization_id"] == TEST_ORGANIZATION_ID
    assert fake_supabase.rows["sch_trigger"][0]["organization_id"] == TEST_ORGANIZATION_ID


async def test_a_trigger_added_later_inherits_its_task_organization(client, fake_supabase):
    async with client:
        res = await client.post(
            "/scheduler/tasks",
            json={"kind": "agent", "title": "t", "agent_task": {"agent_id": "a", "prompt": "p"}},
        )
        assert res.status_code == 201, res.text
        task_id = res.json()["task"]["id"]
        res = await client.post(
            "/scheduler/triggers", json={"task_id": task_id, **_CRON, "enabled": False}
        )
    assert res.status_code in (200, 201), res.text
    assert fake_supabase.rows["sch_trigger"][0]["organization_id"] == TEST_ORGANIZATION_ID


async def test_no_organization_is_held_at_the_one_door(no_org_client, fake_supabase):
    async with no_org_client:
        res = await no_org_client.post(
            "/scheduler/tasks",
            json={"kind": "agent", "title": "t", "agent_task": {"agent_id": "a", "prompt": "p"}},
        )
    assert res.status_code == 400, res.text
    assert "organization_required" in res.text
    assert fake_supabase.rows["sch_task"] == []
