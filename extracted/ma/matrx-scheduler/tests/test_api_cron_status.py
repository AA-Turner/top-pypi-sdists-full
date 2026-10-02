"""
Cron / next-due / scanner-status route tests.

These routes are mostly pure compute (cron validation, next-due preview)
or read scanner state — no DB writes. Verify they correctly call into
the underlying helpers and gate admin-only routes properly.
"""

from __future__ import annotations

import pytest


pytestmark = pytest.mark.asyncio


# ── Cron validation ─────────────────────────────────────────────────────


async def test_validate_cron_ok(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/validate",
            json={"expression": "0 9 * * 1-5", "tz": "UTC", "next_n": 3},
        )
    assert res.status_code == 200
    body = res.json()
    assert body["valid"] is True
    assert body["error"] is None
    assert len(body["next_fires_utc"]) == 3


async def test_validate_cron_bad_expression(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/validate",
            json={"expression": "not a cron", "tz": "UTC", "next_n": 5},
        )
    assert res.status_code == 200
    body = res.json()
    assert body["valid"] is False
    assert body["error"] is not None
    assert body["next_fires_utc"] == []


async def test_validate_cron_bad_tz(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/validate",
            json={"expression": "0 9 * * *", "tz": "Not/A/Zone", "next_n": 5},
        )
    assert res.status_code == 200
    assert res.json()["valid"] is False


async def test_validate_cron_requires_auth(anon_client):
    async with anon_client:
        res = await anon_client.post(
            "/scheduler/cron/validate",
            json={"expression": "0 9 * * *", "tz": "UTC", "next_n": 5},
        )
    assert res.status_code == 401


# ── Preview fires ──────────────────────────────────────────────────────


async def test_preview_fires_cron(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/preview-fires",
            json={
                "trigger_type": "cron",
                "config": {"expression": "0 0 * * *", "tz": "UTC"},
                "n": 3,
            },
        )
    assert res.status_code == 200
    body = res.json()
    assert len(body["next_fires_utc"]) == 3
    assert body["event_driven"] is False


async def test_preview_fires_interval(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/preview-fires",
            json={
                "trigger_type": "interval",
                "config": {"every_seconds": 300},
                "n": 4,
            },
        )
    assert res.status_code == 200
    body = res.json()
    assert len(body["next_fires_utc"]) == 4


async def test_preview_fires_one_shot(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/preview-fires",
            json={
                "trigger_type": "one-shot",
                "config": {"at": "2030-01-01T12:00:00Z"},
                "n": 5,
            },
        )
    assert res.status_code == 200
    body = res.json()
    assert len(body["next_fires_utc"]) == 1


async def test_preview_fires_event_driven_empty(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/preview-fires",
            json={"trigger_type": "manual", "config": {}, "n": 5},
        )
    assert res.status_code == 200
    body = res.json()
    assert body["next_fires_utc"] == []
    assert body["event_driven"] is True


async def test_preview_fires_cron_bad_expression_returns_empty(client):
    async with client:
        res = await client.post(
            "/scheduler/cron/preview-fires",
            json={
                "trigger_type": "cron",
                "config": {"expression": "garbage"},
                "n": 5,
            },
        )
    assert res.status_code == 200
    assert res.json()["next_fires_utc"] == []


# ── Compute next-due-at ────────────────────────────────────────────────


async def test_compute_next_due_at_interval(client):
    async with client:
        res = await client.post(
            "/scheduler/compute-next-due-at",
            json={"trigger_type": "interval", "config": {"every_seconds": 60}},
        )
    assert res.status_code == 200
    body = res.json()
    assert body["next_due_at"] is not None
    assert body["event_driven"] is False


async def test_compute_next_due_at_event_driven(client):
    async with client:
        res = await client.post(
            "/scheduler/compute-next-due-at",
            json={"trigger_type": "event", "config": {}},
        )
    assert res.status_code == 200
    body = res.json()
    assert body["next_due_at"] is None
    assert body["event_driven"] is True


# ── Scanner status ─────────────────────────────────────────────────────


async def test_status_admin_only(client):
    """Non-admins get 403."""
    async with client:
        res = await client.get("/scheduler/status")
    assert res.status_code == 403


async def test_status_admin_ok(admin_client):
    async with admin_client:
        res = await admin_client.get("/scheduler/status")
    assert res.status_code == 200
    body = res.json()
    # Scanner hasn't started in tests; should be a clean snapshot
    assert body["running"] is False
    assert body["total_runs_dispatched"] == 0
    assert body["consecutive_errors"] == 0


async def test_status_requires_auth(anon_client):
    async with anon_client:
        res = await anon_client.get("/scheduler/status")
    assert res.status_code == 401
