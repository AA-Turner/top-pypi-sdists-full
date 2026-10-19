"""A task the host exempts is NEVER switched off — and is never silent either.

2026-10-17 20:05Z: three failed passes in a row suspended aidream's
``cloud_browser_lease_maintenance``; nothing renewed any browser lease after
that, and every Cloud Computer ended itself through its lease watchdog 150 s
later. A host names such infrastructure through ext ``suspension_exempt``.
Every ceiling below still reaches the escalation sink; none disables the task.
"""

from __future__ import annotations

import pytest

from matrx_scheduler import repeat_guard
from matrx_scheduler.repeat_guard import MAX_CONSECUTIVE_FAILURES

DB_BLIP = (
    "ConnectionDoesNotExistError: connection was closed in the middle of operation "
    "(pool 3 of 20, 2026-10-17T20:04:22Z)"
)
EXEMPT_ID = "renewer"
REASON = "renews every Cloud Computer's lease; a pause ends every machine"


class _Query:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def order_by(self, *_a: str) -> _Query:
        return self

    def limit(self, *_a: int) -> _Query:
        return self

    async def values(self, *_f: str) -> list[dict]:
        return self._rows


class _Updated:
    def __init__(self, n: int) -> None:
        self.updated_rows = [{}] * n


class _Table:
    rows: list[dict] = []

    @classmethod
    def filter(cls, **kw: object) -> _Query:
        wanted = kw.pop("status__in", None)
        rows = [r for r in cls.rows if all(r.get(k) == v for k, v in kw.items())]
        if wanted is not None:
            allowed = {str(s).lower() for s in wanted}  # type: ignore[union-attr]
            rows = [r for r in rows if str(r.get("status") or "").lower() in allowed]
        return _Query(rows)

    @classmethod
    async def update_where(cls, filters: dict, **updates: object) -> _Updated:
        hit = [r for r in cls.rows if all(r.get(k) == v for k, v in filters.items())]
        for row in hit:
            row.update(updates)
        return _Updated(len(hit))


class _Runs(_Table):
    rows: list[dict] = []


class _Tasks(_Table):
    rows: list[dict] = []


class _Triggers(_Table):
    rows: list[dict] = []


@pytest.fixture
def world(monkeypatch):
    alarms: list = []
    exts: dict = {}

    async def sink(alarm) -> None:
        alarms.append(alarm)

    async def exempt(task_id: str) -> str | None:
        return REASON if task_id == EXEMPT_ID else None

    exts["escalation_sink"] = sink
    exts["suspension_exempt"] = exempt

    def install(task_id: str, runs: list[dict]) -> None:
        _Runs.rows = [{**r, "task_id": task_id, "id": f"r{i}"} for i, r in enumerate(runs)]
        _Tasks.rows = [{"id": task_id, "enabled": True, "metadata": {}}]
        _Triggers.rows = [{"id": "t", "task_id": task_id, "enabled": True, "metadata": {}}]

    monkeypatch.setattr(
        repeat_guard,
        "get_db_model",
        lambda name: {"SchRun": _Runs, "SchTask": _Tasks, "SchTrigger": _Triggers}[name],
    )
    monkeypatch.setattr(repeat_guard, "get_optional_ext", lambda name: exts.get(name))
    return install, alarms, exts


def _failed(n: int) -> list[dict]:
    # A success further back: the renewer HAS worked, as it had on 10-17.
    return [{"status": "failed", "error_message": DB_BLIP}] * n + [{"status": "success"}]


@pytest.mark.asyncio
async def test_three_failed_passes_never_suspend_an_exempt_task(world) -> None:
    install, alarms, _ = world
    install(EXEMPT_ID, _failed(MAX_CONSECUTIVE_FAILURES))

    await repeat_guard.note_failed_run("r0", task_id=EXEMPT_ID)

    assert _Tasks.rows[0]["enabled"] is True
    assert _Triggers.rows[0]["enabled"] is True
    assert "auto_suspended" not in _Tasks.rows[0]["metadata"]
    # Never silent: the person still hears it, told it is still running.
    assert len(alarms) == 1
    assert alarms[0].escalate is True
    assert alarms[0].suspended is False
    assert alarms[0].exempt_reason == REASON


@pytest.mark.asyncio
async def test_twenty_failed_passes_still_never_suspend(world) -> None:
    install, alarms, _ = world
    install(EXEMPT_ID, _failed(20))
    for _ in range(20):
        await repeat_guard.note_failed_run("r0", task_id=EXEMPT_ID)
    assert _Tasks.rows[0]["enabled"] is True
    assert all(a.exempt_reason == REASON for a in alarms)


@pytest.mark.asyncio
async def test_every_other_task_is_still_suspended(world) -> None:
    install, alarms, _ = world
    install("ordinary", _failed(MAX_CONSECUTIVE_FAILURES))
    await repeat_guard.note_failed_run("r0", task_id="ordinary")
    assert _Tasks.rows[0]["enabled"] is False
    assert alarms[0].suspended is True
    assert alarms[0].exempt_reason is None


@pytest.mark.asyncio
async def test_the_failure_rate_ceiling_never_suspends_an_exempt_task(world) -> None:
    install, alarms, exts = world
    # Interleaved: no streak, but 50% of the window failed.
    install(EXEMPT_ID, [{"status": "failed", "error_message": DB_BLIP}, {"status": "success"}] * 5)

    async def limits(_task_id: str) -> dict:
        return {"max_failure_pct": 40, "failure_window_runs": 10, "failure_min_runs": 6}

    async def breach(*_a) -> None:
        return None

    exts["failure_rate_limits"] = limits
    exts["guardrail_breach"] = breach
    await repeat_guard.note_failed_run("r0", task_id=EXEMPT_ID)
    assert _Tasks.rows[0]["enabled"] is True
    assert alarms and alarms[0].exempt_reason == REASON


@pytest.mark.asyncio
async def test_suspend_now_never_suspends_an_exempt_task(world) -> None:
    install, alarms, _ = world
    install(EXEMPT_ID, [])
    await repeat_guard.suspend_schedule_now(
        EXEMPT_ID, "r0", error_message="unrunnable", reason="cannot run"
    )
    assert _Tasks.rows[0]["enabled"] is True
    assert alarms[0].exempt_reason == REASON


@pytest.mark.asyncio
async def test_an_unreadable_exemption_keeps_the_task_running(world) -> None:
    install, alarms, exts = world

    async def broken(_task_id: str) -> str | None:
        raise RuntimeError("registry unreadable")

    exts["suspension_exempt"] = broken
    install(EXEMPT_ID, _failed(MAX_CONSECUTIVE_FAILURES))
    await repeat_guard.note_failed_run("r0", task_id=EXEMPT_ID)
    assert _Tasks.rows[0]["enabled"] is True
    assert alarms[0].exempt_reason
