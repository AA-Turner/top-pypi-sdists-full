"""A schedule names the Cloud Computer it runs on (machines plan phase 3, "Runs on").

Red when: a create's ``machine_id`` does not land in ``sch_task.metadata.machine_id`` beside
``created_via``; a patch cannot set, change or clear it; or a patch that does not name it touches
the task's other metadata. The host's runner reads the key (aidream
``scheduling/agent_runner_adapter``); none = today's behavior (no machine)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


async def test_create_carries_the_machine(client, fake_supabase):
    async with client:
        res = await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "On my machine", "machine_id": "m-build"},
        )
    assert res.status_code == 201, res.text
    meta = res.json()["task"]["metadata"]
    assert meta["machine_id"] == "m-build"
    assert "created_via" in meta


async def test_create_without_a_machine_names_none(client):
    async with client:
        res = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "Cloud"})
    assert "machine_id" not in res.json()["task"]["metadata"]


async def test_patch_sets_changes_and_clears_the_machine(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks", json={"kind": "ping", "title": "t", "machine_id": "m-1"}
        )
        task_id = created.json()["task"]["id"]
        untouched = await client.patch(f"/scheduler/tasks/{task_id}", json={"title": "t2"})
        assert untouched.json()["metadata"]["machine_id"] == "m-1"
        changed = await client.patch(f"/scheduler/tasks/{task_id}", json={"machine_id": "m-2"})
        assert changed.status_code == 200, changed.text
        assert changed.json()["metadata"]["machine_id"] == "m-2"
        assert "created_via" in changed.json()["metadata"]
        cleared = await client.patch(f"/scheduler/tasks/{task_id}", json={"machine_id": None})
    assert "machine_id" not in cleared.json()["metadata"]
    assert "created_via" in cleared.json()["metadata"]
