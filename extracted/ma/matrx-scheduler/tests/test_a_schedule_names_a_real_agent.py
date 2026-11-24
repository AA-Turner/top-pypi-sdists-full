"""A schedule's ``agent_id`` must name an agent the caller can use (CGU-10, 2026-11-09).

The Android app stored ``sch_agent_task.agent_id`` = a random UUID through ``POST
/scheduler/tasks``; the schedule could only ever fail. Every door that stores or ARMS a direct
agent now asks the host's ``agent_access_check`` and answers 422 naming the id; the database
also refuses an id that names no agent (FK ``sch_agent_task_agent_id_fkey`` to
``agent.definition``). A Mandate selection is unaffected.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio

_MINE = "0d1a7e5c-1111-4a11-8a11-000000000001"
_RANDOM = "9b2f6c1e-7d3a-4e55-9a0c-5f1e2d3c4b5a"


def _agent_schedule(agent_id: str, **extra) -> dict:
    return {"kind": "agent", "title": "Weekly digest", "agent_task": {"agent_id": agent_id, "prompt": "Summarize."}, **extra}


async def test_a_random_agent_id_is_refused_and_nothing_is_written(client, fake_supabase) -> None:
    fake_supabase.usable_agents = {_MINE}
    async with client:
        res = await client.post("/scheduler/tasks", json=_agent_schedule(_RANDOM))
    assert res.status_code == 422, res.text
    assert _RANDOM in res.json()["detail"]
    assert fake_supabase.rows.get("sch_task", []) == []
    assert fake_supabase.rows.get("sch_agent_task", []) == []


async def test_a_non_uuid_agent_id_is_refused(client, fake_supabase) -> None:
    async with client:
        res = await client.post("/scheduler/tasks", json=_agent_schedule("not-an-agent"))
    assert res.status_code == 422, res.text
    assert fake_supabase.rows.get("sch_task", []) == []


async def test_an_agent_you_can_use_is_accepted(client, fake_supabase) -> None:
    fake_supabase.usable_agents = {_MINE}
    async with client:
        res = await client.post("/scheduler/tasks", json=_agent_schedule(_MINE))
    assert res.status_code == 201, res.text


async def test_a_mandate_schedule_never_asks(client, fake_supabase) -> None:
    fake_supabase.usable_agents = set()
    async with client:
        res = await client.post(
            "/scheduler/tasks",
            json={"kind": "agent", "title": "m", "agent_task": {"mandate_key": "weekly.digest", "prompt": "p"}},
        )
    assert res.status_code == 201, res.text


async def test_arming_a_schedule_whose_agent_is_gone_is_refused(client, fake_supabase) -> None:
    fake_supabase.usable_agents = {_MINE}
    async with client:
        created = await client.post("/scheduler/tasks", json=_agent_schedule(_MINE, enabled=False))
        assert created.status_code == 201, created.text
        task_id = created.json()["task"]["id"]
        fake_supabase.usable_agents = set()  # the agent was deleted, or access was withdrawn
        enable = await client.patch(f"/scheduler/tasks/{task_id}", json={"enabled": True})
        trigger = await client.post(
            "/scheduler/triggers",
            json={"task_id": task_id, "type": "interval", "config": {"every_seconds": 60}, "enabled": True},
        )
    assert enable.status_code == 422, enable.text
    assert trigger.status_code == 422, trigger.text
    assert fake_supabase.rows["sch_trigger"] == []


async def test_without_a_host_check_a_direct_agent_is_never_trusted(client, fake_supabase) -> None:
    from matrx_scheduler import _ext

    saved = _ext._registry.get("agent_access_check")
    _ext._registry["agent_access_check"] = None
    try:
        async with client:
            res = await client.post("/scheduler/tasks", json=_agent_schedule(_MINE))
    finally:
        _ext._registry["agent_access_check"] = saved
    assert res.status_code == 503, res.text
    assert fake_supabase.rows.get("sch_task", []) == []
