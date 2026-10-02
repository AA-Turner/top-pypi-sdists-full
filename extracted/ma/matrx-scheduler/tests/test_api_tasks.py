"""
Task CRUD route tests.

Verify the wire shapes, owner-scoping behavior, and error mapping for
``POST/GET/PATCH/DELETE /scheduler/tasks/...``. Uses the in-memory
FakeSupabase from conftest.
"""

from __future__ import annotations

import pytest


pytestmark = pytest.mark.asyncio


# ── Create ──────────────────────────────────────────────────────────────


async def test_create_task_minimal(client, fake_supabase, authed_user_id):
    """A bare-minimum 'agent' task with prompt creates parent + child rows."""
    payload = {
        "kind": "agent",
        "title": "Test task",
        "agent_task": {
            "agent_id": "agent-1",
            "prompt": "Do the thing",
        },
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)

    assert res.status_code == 201, res.text
    body = res.json()
    assert body["task"]["title"] == "Test task"
    assert body["task"]["user_id"] == authed_user_id
    assert body["task"]["kind"] == "agent"
    assert body["agent_task"]["prompt"] == "Do the thing"
    assert body["agent_task"]["max_runtime_seconds"] == 600  # default
    assert body["triggers"] == []
    # Sanity: row landed in the fake DB
    assert len(fake_supabase.rows["sch_task"]) == 1
    assert len(fake_supabase.rows["sch_agent_task"]) == 1


async def test_agent_task_row_carries_its_task_organization(client, fake_supabase):
    """sch_agent_task.organization_id is NOT NULL with no default and no trigger:
    the writer must copy the parent task's own organization into the child row."""
    payload = {
        "kind": "agent",
        "title": "Org carried to the child",
        "agent_task": {"agent_id": "agent-1", "prompt": "Do the thing"},
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)

    assert res.status_code == 201, res.text
    task = fake_supabase.rows["sch_task"][0]
    agent_task = fake_supabase.rows["sch_agent_task"][0]
    assert task["organization_id"]
    assert agent_task["organization_id"] == task["organization_id"]


async def test_tool_task_requires_feature_registry_identity(client, fake_supabase):
    payload = {
        "kind": "tool",
        "title": "Unclassified system job",
        "agent_task": {"variables": {"tool_name": "system.example"}},
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)

    assert res.status_code == 422, res.text
    assert "taxonomy_node_id" in res.json()["detail"]
    assert fake_supabase.rows["sch_task"] == []


async def test_tool_task_persists_feature_registry_identity(client, fake_supabase):
    taxonomy_node_id = "11111111-1111-4111-8111-111111111111"
    payload = {
        "kind": "tool",
        "title": "Classified system job",
        "taxonomy_node_id": taxonomy_node_id,
        "agent_task": {"variables": {"tool_name": "system.example"}},
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)

    assert res.status_code == 201, res.text
    assert res.json()["task"]["taxonomy_node_id"] == taxonomy_node_id
    assert fake_supabase.rows["sch_task"][0]["taxonomy_node_id"] == taxonomy_node_id


async def test_double_submit_returns_the_existing_schedule(client, fake_supabase):
    """THE SCHEDULER DUPLICATE GUARD, end to end.

    This is the incident: the SAME create arriving twice (a double-click, or an
    MCP retry whose first attempt actually succeeded) produced two complete
    always-on schedules that both fired hourly for five days. The second create
    must now return the FIRST schedule, not make another one.
    """
    payload = {
        "kind": "agent",
        "title": "Human Baseline Schedule",
        "agent_task": {"agent_id": "agent-1", "prompt": "Summarize the week."},
        "trigger": {"type": "cron", "config": {"expression": "0 * * * *"}, "enabled": True},
    }
    async with client:
        first = await client.post("/scheduler/tasks", json=payload)
        second = await client.post("/scheduler/tasks", json=payload)

    assert first.status_code == 201, first.text
    # A success, not an error — the caller asked for a schedule and has one.
    assert second.status_code == 200, second.text
    assert second.json()["deduplicated"] is True
    assert first.json()["deduplicated"] is False
    assert second.json()["task"]["id"] == first.json()["task"]["id"]
    # The whole point: ONE schedule exists, so it bills once.
    assert len(fake_supabase.rows["sch_task"]) == 1
    assert len(fake_supabase.rows["sch_trigger"]) == 1


async def test_a_renamed_duplicate_is_still_a_duplicate(client, fake_supabase):
    """Identity is what a schedule DOES, not what it is called — two schedules
    running one agent on one cron cost the same whether or not they share a name."""
    payload = {
        "kind": "agent",
        "title": "Morning Brief",
        "agent_task": {"agent_id": "agent-1", "prompt": "Summarize the week."},
        "trigger": {"type": "cron", "config": {"expression": "0 * * * *"}, "enabled": True},
    }
    async with client:
        first = await client.post("/scheduler/tasks", json=payload)
        second = await client.post("/scheduler/tasks", json={**payload, "title": "Daily Summary"})

    assert second.status_code == 200, second.text
    assert second.json()["task"]["id"] == first.json()["task"]["id"]
    assert len(fake_supabase.rows["sch_task"]) == 1


async def test_force_creates_the_second_schedule_anyway(client, fake_supabase):
    """A user who genuinely wants two similar schedules is never blocked."""
    payload = {
        "kind": "agent",
        "title": "Human Baseline Schedule",
        "agent_task": {"agent_id": "agent-1", "prompt": "Summarize the week."},
        "trigger": {"type": "cron", "config": {"expression": "0 * * * *"}, "enabled": True},
    }
    async with client:
        first = await client.post("/scheduler/tasks", json=payload)
        second = await client.post("/scheduler/tasks", json={**payload, "force": True})

    assert second.status_code == 201, second.text
    assert second.json()["deduplicated"] is False
    assert second.json()["task"]["id"] != first.json()["task"]["id"]
    assert len(fake_supabase.rows["sch_task"]) == 2


async def test_a_genuinely_different_schedule_is_never_blocked(client, fake_supabase):
    """The expensive failure mode for a guard like this is the FALSE positive."""
    base = {
        "kind": "agent",
        "title": "Weekly Marketing Recap",
        "agent_task": {"agent_id": "agent-1", "prompt": "Summarize the week."},
        "trigger": {"type": "cron", "config": {"expression": "0 * * * *"}, "enabled": True},
    }
    other = {
        **base,
        "agent_task": {"agent_id": "agent-1", "prompt": "Recap the marketing numbers."},
    }
    async with client:
        await client.post("/scheduler/tasks", json=base)
        res = await client.post("/scheduler/tasks", json=other)

    assert res.status_code == 201, res.text
    assert len(fake_supabase.rows["sch_task"]) == 2


async def test_duplicates_endpoint_reports_a_forced_pair(client):
    """The surface that shows the user what already duplicates what."""
    payload = {
        "kind": "agent",
        "title": "Human Baseline Schedule",
        "agent_task": {"agent_id": "agent-1", "prompt": "Summarize the week."},
        "trigger": {"type": "cron", "config": {"expression": "0 * * * *"}, "enabled": True},
    }
    async with client:
        await client.post("/scheduler/tasks", json=payload)
        await client.post("/scheduler/tasks", json={**payload, "force": True})
        res = await client.get("/scheduler/tasks/duplicates")

    assert res.status_code == 200, res.text
    groups = res.json()["groups"]
    assert len(groups) == 1
    assert groups[0]["redundant_count"] == 1
    assert groups[0]["enabled_count"] == 2
    members = groups[0]["members"]
    assert [m["is_original"] for m in members] == [True, False]


async def test_duplicates_endpoint_retries_a_timed_out_rls_read_once(client, fake_supabase, monkeypatch):
    """A transient command timeout poisons an RLS transaction, so retry its whole read."""
    from matrx_orm import QueryTimeoutError
    from matrx_scheduler.api import user_queries

    real_task_model = fake_supabase.db_models()["SchTask"]
    attempts = 0

    class _FlakyTaskQuery:
        def __init__(self, query):
            self._query = query

        async def values(self, *fields):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise QueryTimeoutError(operation="duplicate check", query="SELECT")
            return await self._query.values(*fields)

    class _FlakyTaskModel:
        @classmethod
        def filter(cls, **filters):
            return _FlakyTaskQuery(real_task_model.filter(**filters))

    real_get_model = user_queries.get_db_model
    monkeypatch.setattr(
        user_queries,
        "get_db_model",
        lambda name: _FlakyTaskModel if name == "SchTask" else real_get_model(name),
    )

    async with client:
        response = await client.get("/scheduler/tasks/duplicates")

    assert response.status_code == 200, response.text
    assert attempts == 2


async def test_create_task_with_cron_trigger(client, fake_supabase):
    """A task created with a cron trigger has next_due_at populated."""
    payload = {
        "kind": "agent",
        "title": "Weekly digest",
        "agent_task": {"agent_id": "agent-1", "prompt": "Generate weekly digest"},
        "trigger": {
            "type": "cron",
            "config": {"expression": "0 9 * * 1", "tz": "UTC"},
            "enabled": True,
        },
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)

    assert res.status_code == 201, res.text
    body = res.json()
    assert len(body["triggers"]) == 1
    trigger = body["triggers"][0]
    assert trigger["type"] == "cron"
    assert trigger["config"]["expression"] == "0 9 * * 1"
    # next_due_at should be set for cron triggers
    assert trigger["next_due_at"] is not None


async def test_create_task_one_shot_trigger(client):
    payload = {
        "kind": "ping",
        "title": "Health check",
        "trigger": {
            "type": "one-shot",
            "config": {"at": "2030-01-01T12:00:00Z"},
            "enabled": True,
        },
    }
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["task"]["kind"] == "ping"
    assert len(body["triggers"]) == 1
    assert body["triggers"][0]["next_due_at"] is not None


async def test_create_task_rejects_invalid_kind(client):
    payload = {"kind": "bogus", "title": "x"}
    async with client:
        res = await client.post("/scheduler/tasks", json=payload)
    assert res.status_code == 400
    assert "invalid kind" in res.json()["detail"]


async def test_create_task_requires_auth(anon_client):
    payload = {"kind": "ping", "title": "x"}
    async with anon_client:
        res = await anon_client.post("/scheduler/tasks", json=payload)
    assert res.status_code == 401


async def test_create_task_validates_title_length(client):
    async with client:
        res = await client.post("/scheduler/tasks", json={"kind": "ping", "title": ""})
    # Pydantic returns 422 for body validation errors
    assert res.status_code == 422


@pytest.mark.parametrize(
    "agent_task",
    [None, {"prompt": "Do the thing"}, {"agent_id": "", "prompt": "Do the thing"}],
)
async def test_create_agent_task_requires_explicit_agent(client, fake_supabase, agent_task):
    payload = {"kind": "agent", "title": "Impossible schedule"}
    if agent_task is not None:
        payload["agent_task"] = agent_task

    async with client:
        res = await client.post("/scheduler/tasks", json=payload)

    assert res.status_code == 422
    assert "agent" in res.json()["detail"].lower()
    assert fake_supabase.rows["sch_task"] == []


# ── List ────────────────────────────────────────────────────────────────


async def test_list_tasks_empty(client):
    async with client:
        res = await client.get("/scheduler/tasks")
    assert res.status_code == 200
    body = res.json()
    assert body["tasks"] == []
    assert body["total"] == 0


async def test_list_tasks_after_create(client):
    async with client:
        await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "first"},
        )
        await client.post(
            "/scheduler/tasks",
            json={
                "kind": "agent",
                "title": "second",
                "agent_task": {"agent_id": "agent-1", "prompt": "x"},
            },
        )
        res = await client.get("/scheduler/tasks")
    assert res.status_code == 200
    body = res.json()
    assert len(body["tasks"]) == 2
    assert body["total"] == 2


async def test_list_tasks_filter_by_kind(client):
    async with client:
        await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "p1"},
        )
        await client.post(
            "/scheduler/tasks",
            json={
                "kind": "agent",
                "title": "a1",
                "agent_task": {"agent_id": "agent-1", "prompt": "x"},
            },
        )
        res = await client.get("/scheduler/tasks?kind=ping")
    assert res.status_code == 200
    body = res.json()
    assert len(body["tasks"]) == 1
    assert body["tasks"][0]["kind"] == "ping"


async def test_list_tasks_filter_by_enabled(client):
    async with client:
        await client.post("/scheduler/tasks", json={"kind": "ping", "title": "on"})
        await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "off", "enabled": False},
        )
        on_res = await client.get("/scheduler/tasks?enabled=true")
        off_res = await client.get("/scheduler/tasks?enabled=false")
    assert len(on_res.json()["tasks"]) == 1
    assert on_res.json()["tasks"][0]["title"] == "on"
    assert len(off_res.json()["tasks"]) == 1
    assert off_res.json()["tasks"][0]["title"] == "off"


# ── Get one ─────────────────────────────────────────────────────────────


async def test_get_task_404(client):
    async with client:
        res = await client.get("/scheduler/tasks/does-not-exist")
    assert res.status_code == 404


async def test_get_task_with_hydration(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={
                "kind": "agent",
                "title": "T",
                "agent_task": {"agent_id": "agent-1", "prompt": "P"},
                "trigger": {
                    "type": "interval",
                    "config": {"every_seconds": 300},
                },
            },
        )
        task_id = created.json()["task"]["id"]
        res = await client.get(f"/scheduler/tasks/{task_id}")

    assert res.status_code == 200
    body = res.json()
    assert body["task"]["id"] == task_id
    assert body["agent_task"]["prompt"] == "P"
    assert len(body["triggers"]) == 1
    assert body["triggers"][0]["type"] == "interval"
    assert body["recent_runs"] == []


# ── Patch ───────────────────────────────────────────────────────────────


async def test_patch_task_partial(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "original"},
        )
        task_id = created.json()["task"]["id"]
        res = await client.patch(
            f"/scheduler/tasks/{task_id}",
            json={"title": "new title", "enabled": False},
        )

    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "new title"
    assert body["enabled"] is False


async def test_patch_task_can_clear_nullable_fields(client):
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={
                "kind": "ping",
                "title": "nullable fields",
                "description": "temporary",
                "expires_at": "2030-01-01T00:00:00Z",
            },
        )
        task_id = created.json()["task"]["id"]
        res = await client.patch(
            f"/scheduler/tasks/{task_id}",
            json={"description": None, "expires_at": None},
        )

    assert res.status_code == 200
    body = res.json()
    assert body["description"] is None
    assert body["expires_at"] is None


async def test_patch_task_404(client):
    async with client:
        res = await client.patch("/scheduler/tasks/does-not-exist", json={"title": "x"})
    assert res.status_code == 404


async def test_invalid_legacy_agent_task_cannot_be_reenabled_or_run(
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
        enabled = await client.patch(f"/scheduler/tasks/{task_id}", json={"enabled": True})
        run = await client.post(f"/scheduler/tasks/{task_id}/run-now")

    assert enabled.status_code == 422
    assert run.status_code == 422
    assert "choose an agent" in enabled.json()["detail"].lower()
    assert "choose an agent" in run.json()["detail"].lower()
    assert fake_supabase.rows["sch_task"][0]["enabled"] is False
    assert fake_supabase.rows["sch_run"] == []


# ── Delete ──────────────────────────────────────────────────────────────


async def test_delete_task_soft(client, fake_supabase):
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "to-delete"})
        task_id = created.json()["task"]["id"]
        res = await client.delete(f"/scheduler/tasks/{task_id}")
        # After soft-delete, GET 404s (the row is invisible to the user-
        # facing surface). PATCH on it also 404s. List excludes it.
        check = await client.get(f"/scheduler/tasks/{task_id}")
        patch_after = await client.patch(f"/scheduler/tasks/{task_id}", json={"title": "revive?"})
        listed = await client.get("/scheduler/tasks")

    assert res.status_code == 200
    body = res.json()
    assert body["deleted"] is True
    assert body["soft"] is True
    assert check.status_code == 404
    assert patch_after.status_code == 404
    assert task_id not in {t["id"] for t in listed.json()["tasks"]}

    # The underlying row is still in the table -- run history references
    # task_id, so we never hard-delete. Confirm deleted_at + enabled=false.
    row = next(r for r in fake_supabase.rows["sch_task"] if r["id"] == task_id)
    assert row["deleted_at"] is not None
    assert row["enabled"] is False


async def test_delete_task_404(client):
    async with client:
        res = await client.delete("/scheduler/tasks/does-not-exist")
    assert res.status_code == 404


# ── Run-now ─────────────────────────────────────────────────────────────


async def test_run_now_creates_run(client, fake_supabase):
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "fire-me"})
        task_id = created.json()["task"]["id"]
        res = await client.post(f"/scheduler/tasks/{task_id}/run-now")

    assert res.status_code == 200
    body = res.json()
    assert "run_id" in body
    # Fake RPC recorded
    assert any(
        call == ("sch_enqueue_manual_run", {"p_task_id": task_id})
        for call in fake_supabase.rpc_calls
    )
    # A queued sch_run row exists
    runs = fake_supabase.rows["sch_run"]
    assert len(runs) == 1
    assert runs[0]["task_id"] == task_id
    assert runs[0]["status"] == "queued"


async def test_run_now_404(client):
    async with client:
        res = await client.post("/scheduler/tasks/does-not-exist/run-now")
    assert res.status_code == 404


async def test_run_now_owner_mismatch_is_warning_not_error(client, fake_supabase, caplog):
    """Expected cross-owner refusal must not create an ERROR log family."""
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "owned"})
        task_id = created.json()["task"]["id"]
        fake_supabase.rows["sch_task"][0]["user_id"] = "00000000-0000-4000-8000-0000000fffe1"
        with caplog.at_level("WARNING", logger="matrx_scheduler.api.router_scheduler"):
            res = await client.post(f"/scheduler/tasks/{task_id}/run-now")

    assert res.status_code == 403
    records = [r for r in caplog.records if "owner mismatch" in r.getMessage()]
    assert records and all(r.levelname == "WARNING" for r in records)


async def test_run_now_requires_auth(anon_client):
    async with anon_client:
        res = await anon_client.post("/scheduler/tasks/x/run-now")
    assert res.status_code == 401
