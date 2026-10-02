"""
Trigger CRUD + run history route tests.
"""

from __future__ import annotations

import pytest


pytestmark = pytest.mark.asyncio


# ── Triggers ────────────────────────────────────────────────────────────


async def test_list_triggers_for_task(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={
                "kind": "ping",
                "title": "with-trigger",
                "trigger": {
                    "type": "interval",
                    "config": {"every_seconds": 60},
                },
            },
        )
        task_id = created.json()["task"]["id"]
        res = await client.get(f"/scheduler/triggers?task_id={task_id}")
    assert res.status_code == 200
    body = res.json()
    assert len(body["triggers"]) == 1
    assert body["triggers"][0]["task_id"] == task_id
    assert body["triggers"][0]["type"] == "interval"


async def test_create_trigger_on_existing_task(client):
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "p"})
        task_id = created.json()["task"]["id"]
        res = await client.post(
            "/scheduler/triggers",
            json={
                "task_id": task_id,
                "type": "cron",
                "config": {"expression": "*/5 * * * *", "tz": "UTC"},
            },
        )
    assert res.status_code == 201
    body = res.json()
    assert body["task_id"] == task_id
    assert body["type"] == "cron"
    assert body["next_due_at"] is not None  # cron triggers get a computed next


async def test_enabled_trigger_rejects_invalid_legacy_agent_task(
    client,
    fake_supabase,
    authed_user_id,
):
    task_id = "legacy-agent-task"
    fake_supabase.rows["sch_task"].append(
        {
            "id": task_id,
            "user_id": authed_user_id,
            "kind": "agent",
            "title": "Legacy invalid schedule",
            "queue": "default",
            "surfaces": ["any"],
            "enabled": False,
            "tags": [],
            "deleted_at": None,
        }
    )
    fake_supabase.rows["sch_agent_task"].append(
        {
            "id": task_id,
            "agent_id": None,
            "prompt": "Summarize the week.",
            "variables": {},
            "auth_mode": "ask",
            "max_runtime_seconds": 600,
            "max_concurrent": 1,
        }
    )

    async with client:
        res = await client.post(
            "/scheduler/triggers",
            json={
                "task_id": task_id,
                "type": "interval",
                "config": {"every_seconds": 60},
                "enabled": True,
            },
        )

    assert res.status_code == 422
    assert "choose an agent" in res.json()["detail"].lower()
    assert fake_supabase.rows["sch_trigger"] == []


async def test_patch_trigger_config_recomputes_next(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={
                "kind": "ping",
                "title": "p",
                "trigger": {
                    "type": "interval",
                    "config": {"every_seconds": 60},
                },
            },
        )
        trigger_id = created.json()["triggers"][0]["id"]
        first_next = created.json()["triggers"][0]["next_due_at"]
        res = await client.patch(
            f"/scheduler/triggers/{trigger_id}",
            json={"config": {"every_seconds": 3600}},
        )
    assert res.status_code == 200
    body = res.json()
    assert body["config"]["every_seconds"] == 3600
    # next_due_at recomputed (will differ because interval changed)
    assert body["next_due_at"] is not None
    assert body["next_due_at"] != first_next


async def test_patch_trigger_enabled_only(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={
                "kind": "ping",
                "title": "p",
                "trigger": {
                    "type": "interval",
                    "config": {"every_seconds": 60},
                },
            },
        )
        trigger_id = created.json()["triggers"][0]["id"]
        res = await client.patch(f"/scheduler/triggers/{trigger_id}", json={"enabled": False})
    assert res.status_code == 200
    body = res.json()
    assert body["enabled"] is False


async def test_delete_trigger(client, fake_supabase):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={
                "kind": "ping",
                "title": "p",
                "trigger": {
                    "type": "interval",
                    "config": {"every_seconds": 60},
                },
            },
        )
        trigger_id = created.json()["triggers"][0]["id"]
        res = await client.delete(f"/scheduler/triggers/{trigger_id}")
    assert res.status_code == 200
    assert res.json()["deleted"] is True
    # Soft delete (owner ruling 2026-09-20): the row stays, marked deleted and
    # disabled in the same write, so the clock can be explained or restored.
    assert res.json()["soft"] is True
    (row,) = [t for t in fake_supabase.rows["sch_trigger"] if t["id"] == trigger_id]
    assert row["deleted_at"] is not None
    assert row["enabled"] is False


async def test_delete_trigger_404(client):
    async with client:
        res = await client.delete("/scheduler/triggers/does-not-exist")
    assert res.status_code == 404


# ── Run history (read-only) ─────────────────────────────────────────────


async def test_list_runs_empty(client):
    async with client:
        res = await client.get("/scheduler/runs")
    assert res.status_code == 200
    assert res.json()["runs"] == []


async def test_list_runs_after_run_now(client):
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "p"})
        task_id = created.json()["task"]["id"]
        await client.post(f"/scheduler/tasks/{task_id}/run-now")
        res = await client.get(f"/scheduler/runs?task_id={task_id}")
    assert res.status_code == 200
    runs = res.json()["runs"]
    assert len(runs) == 1
    assert runs[0]["task_id"] == task_id
    assert runs[0]["status"] == "queued"


async def test_get_run_by_id(client):
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "p"})
        task_id = created.json()["task"]["id"]
        run_id = (await client.post(f"/scheduler/tasks/{task_id}/run-now")).json()["run_id"]
        res = await client.get(f"/scheduler/runs/{run_id}")
    assert res.status_code == 200
    assert res.json()["id"] == run_id


async def test_get_run_404(client):
    async with client:
        res = await client.get("/scheduler/runs/does-not-exist")
    assert res.status_code == 404
