"""An unreadable cron expression sent to a trigger door is a 422 naming it, never a 500.

2026-11-07 (system_error classes sec_6150ecf3 + sec_6383509c): ``PATCH /scheduler/triggers/{id}``
with ``{"expression": "61 25 * * *"}`` (and one with too few columns) crashed the request —
``compute_next_due_at`` let croniter's error escape the route, so the person got a 500 and the
platform filed a ``request_crash``. The expression is the caller's mistake: it is refused,
named, and nothing is written.
"""

from __future__ import annotations

import pytest

from matrx_scheduler.next_due import InvalidCronExpression, compute_next_due_at

pytestmark = pytest.mark.asyncio

_BAD = ["61 25 * * *", "* * *"]


@pytest.mark.parametrize("expression", _BAD)
async def test_next_due_names_the_bad_expression(expression: str) -> None:
    with pytest.raises(InvalidCronExpression) as caught:
        compute_next_due_at("cron", {"expression": expression, "tz": "UTC"})
    assert expression in str(caught.value)
    assert isinstance(caught.value, ValueError)  # every existing caller keeps its behavior


@pytest.mark.parametrize("expression", _BAD)
async def test_patch_trigger_with_a_bad_cron_is_422(client, fake_supabase, expression: str) -> None:
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "p", "trigger": {"type": "cron", "config": {"expression": "*/5 * * * *"}}},
        )
        trigger_id = created.json()["triggers"][0]["id"]
        res = await client.patch(
            f"/scheduler/triggers/{trigger_id}",
            json={"config": {"expression": expression, "tz": "UTC"}},
        )
    assert res.status_code == 422, res.text
    assert expression in res.json()["detail"]
    stored = next(r for r in fake_supabase.rows["sch_trigger"] if str(r["id"]) == trigger_id)
    assert stored["config"]["expression"] == "*/5 * * * *"


@pytest.mark.parametrize("expression", _BAD)
async def test_create_trigger_with_a_bad_cron_is_422(client, fake_supabase, expression: str) -> None:
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "p"})
        task_id = created.json()["task"]["id"]
        res = await client.post(
            "/scheduler/triggers",
            json={"task_id": task_id, "type": "cron", "config": {"expression": expression}},
        )
        preview = await client.post(
            "/scheduler/compute-next-due-at",
            json={"trigger_type": "cron", "config": {"expression": expression}},
        )
    assert res.status_code == 422, res.text
    assert preview.status_code == 422, preview.text
    assert fake_supabase.rows["sch_trigger"] == []


# 2026-11-07: an unknown ``tz`` used to be silently replaced with UTC, so a schedule written
# for 09:00 Los Angeles fired at 09:00 UTC with no word to anyone. The write doors now refuse it.


async def test_unknown_timezone_is_refused() -> None:
    from matrx_scheduler.next_due import InvalidCronTimezone, validate_trigger_timing

    with pytest.raises(InvalidCronTimezone) as caught:
        validate_trigger_timing("cron", {"expression": "0 9 * * *", "tz": "Pacific/Nowhere"})
    assert "Pacific/Nowhere" in str(caught.value)
    validate_trigger_timing("cron", {"expression": "0 9 * * *", "tz": "America/Los_Angeles"})


async def test_patch_trigger_with_unknown_timezone_is_422(client, fake_supabase) -> None:
    async with client:
        created = await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "p", "trigger": {"type": "cron", "config": {"expression": "*/5 * * * *"}}},
        )
        trigger_id = created.json()["triggers"][0]["id"]
        res = await client.patch(
            f"/scheduler/triggers/{trigger_id}",
            json={"config": {"expression": "0 9 * * *", "tz": "Pacific/Nowhere"}},
        )
    assert res.status_code == 422, res.text
    assert "Pacific/Nowhere" in res.json()["detail"]


# CGU-10 (2026-11-09, found by the Android app): the doors still crashed on expressions croniter
# PARSES but cannot step — a date that never comes — and on a non-string; and a cron trigger with
# no expression, an interval of 0 or a one-shot with no readable time was stored and never fired.
# One check (``require_valid_cron`` / ``validate_trigger_timing``) now backs every door AND
# ``POST /scheduler/cron/validate``, so "valid" there means a write door accepts it.

_NEVER_OR_NOT_TEXT = ["0 0 31 2 *", "not a cron", 5]


@pytest.mark.parametrize("expression", _NEVER_OR_NOT_TEXT)
async def test_create_task_with_unsteppable_cron_is_422(client, fake_supabase, expression) -> None:
    async with client:
        res = await client.post(
            "/scheduler/tasks",
            json={"kind": "ping", "title": "p", "trigger": {"type": "cron", "config": {"expression": expression}}},
        )
        preview = await client.post(
            "/scheduler/compute-next-due-at",
            json={"trigger_type": "cron", "config": {"expression": expression}},
        )
        verdict = await client.post("/scheduler/cron/validate", json={"expression": str(expression)})
    assert res.status_code == 422, res.text
    assert str(expression) in res.json()["detail"]
    assert preview.status_code == 422, preview.text
    assert verdict.json()["valid"] is False
    assert fake_supabase.rows.get("sch_task", []) == []


@pytest.mark.parametrize(
    ("trigger_type", "config"),
    [
        ("cron", {}),
        ("cron", {"expression": "   "}),
        ("interval", {"every_seconds": 0}),
        ("interval", {}),
        ("heartbeat", {"every_seconds": "soon"}),
        ("one-shot", {"at": "not a date"}),
        ("one-shot", {}),
    ],
)
async def test_a_trigger_that_could_never_fire_is_refused(client, fake_supabase, trigger_type, config) -> None:
    async with client:
        created = await client.post("/scheduler/tasks", json={"kind": "ping", "title": "p"})
        task_id = created.json()["task"]["id"]
        res = await client.post("/scheduler/triggers", json={"task_id": task_id, "type": trigger_type, "config": config})
    assert res.status_code == 422, res.text
    assert fake_supabase.rows["sch_trigger"] == []


async def test_validate_and_the_doors_agree() -> None:
    from matrx_scheduler.cron_helpers import validate_cron
    from matrx_scheduler.next_due import InvalidCronExpression, require_valid_cron

    for expression in ["0 0 31 2 *", "61 25 * * *", "not a cron"]:
        assert validate_cron(expression) is not None
        with pytest.raises(InvalidCronExpression):
            require_valid_cron(expression)
    assert validate_cron("0 9 * * 1-5", "America/Los_Angeles") is None
    require_valid_cron("0 9 * * 1-5", "America/Los_Angeles")
