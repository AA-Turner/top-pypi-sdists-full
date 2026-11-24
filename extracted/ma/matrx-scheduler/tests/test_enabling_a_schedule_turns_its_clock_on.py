"""Turning a schedule ON turns its clock on too (2026-11-17, "Daily Check emails").

The 2026-08-20 governance sweep paused every clock trigger (``sch_trigger.enabled=false`` +
``metadata.governance_suspended``). A person's own schedule then read ON for three months and never
fired: the owner PATCH ``enabled=true`` only touched ``sch_task``, so no control a person has could
put the clock back. Enabling now flips the task's triggers on with it (the admin door already pairs
them) and moves each suspension record into ``suspension_history`` so the row says it was restored.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio

_AGENT = "0d1a7e5c-1111-4a11-8a11-000000000001"


async def test_enable_turns_a_paused_trigger_back_on(client, fake_supabase) -> None:
    fake_supabase.usable_agents = {_AGENT}
    async with client:
        res = await client.post("/scheduler/tasks", json={
            "kind": "agent", "title": "Daily check",
            "agent_task": {"agent_id": _AGENT, "prompt": "Check."},
            "trigger": {"type": "interval", "config": {"every_seconds": 79200}, "enabled": True},
        })
        assert res.status_code == 201, res.text
        task_id = res.json()["task"]["id"]
        trigger = fake_supabase.rows["sch_trigger"][0]
        trigger["enabled"] = False
        trigger["metadata"] = {"governance_suspended": {"at": "2026-08-20T20:20:45+00:00", "reason": "Paused"}}

        res = await client.patch(f"/scheduler/tasks/{task_id}", json={"enabled": True})
        assert res.status_code == 200, res.text

    trigger = fake_supabase.rows["sch_trigger"][0]
    assert trigger["enabled"] is True
    assert "governance_suspended" not in (trigger.get("metadata") or {})
    history = (trigger.get("metadata") or {}).get("suspension_history") or []
    assert history and history[0]["key"] == "governance_suspended"


async def test_pausing_leaves_triggers_alone(client, fake_supabase) -> None:
    fake_supabase.usable_agents = {_AGENT}
    async with client:
        res = await client.post("/scheduler/tasks", json={
            "kind": "agent", "title": "Daily check",
            "agent_task": {"agent_id": _AGENT, "prompt": "Check."},
            "trigger": {"type": "interval", "config": {"every_seconds": 79200}, "enabled": True},
        })
        task_id = res.json()["task"]["id"]
        res = await client.patch(f"/scheduler/tasks/{task_id}", json={"enabled": False})
        assert res.status_code == 200, res.text
    assert fake_supabase.rows["sch_trigger"][0]["enabled"] is True
