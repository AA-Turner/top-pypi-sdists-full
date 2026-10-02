"""THE DARK SCHEDULE — a task that reads enabled but can never fire.

Live on 2026-09-12, mid-restore, sch_task a7c1e2d3-…432 sat enabled with its
only trigger disabled: the console said "enabled" while the schedule fired
nothing. Both halves of the repeat guard's suspend/restore can leave that state
(the suspend disables the task first and then loops the triggers; a partial
re-enable flips the task and forgets the clock), and so can any direct row edit.

A task with NO triggers is dispatch-on-demand, not dark — the live
"HR Time & Attendance recompute (dispatch-on-demand)" task is exactly that and
must never be flagged.
"""

from __future__ import annotations

import pytest

from matrx_scheduler import queries, scanner


class _Q:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def limit(self, *_a: int) -> "_Q":
        return self

    async def values(self, *_f: str) -> list[dict]:
        return self._rows


class _Tasks:
    rows: list[dict] = []

    @classmethod
    def filter(cls, **kw: object) -> _Q:
        return _Q([r for r in cls.rows if all(r.get(k) == v for k, v in kw.items())])


class _Triggers:
    rows: list[dict] = []

    @classmethod
    def filter(cls, **kw: object) -> _Q:
        wanted = kw.get("task_id__in")
        if wanted is None:
            return _Q(cls.rows)
        return _Q([r for r in cls.rows if str(r.get("task_id")) in set(wanted)])  # type: ignore[arg-type]


@pytest.fixture
def ledger(monkeypatch):
    def _install(tasks: list[dict], triggers: list[dict]) -> None:
        _Tasks.rows = tasks
        _Triggers.rows = triggers
        monkeypatch.setattr(
            queries,
            "get_db_model",
            lambda name: {"SchTask": _Tasks, "SchTrigger": _Triggers}[name],
        )

    return _install


def _task(tid: str, title: str, enabled: bool = True) -> dict:
    return {"id": tid, "title": title, "enabled": enabled, "deleted_at": None}


@pytest.mark.asyncio
async def test_enabled_task_with_only_disabled_triggers_is_dark(ledger) -> None:
    ledger(
        [_task("432", "SEO — universal facet backfill")],
        [{"task_id": "432", "enabled": False}],
    )
    dark = await queries.find_dark_tasks()
    assert [d["id"] for d in dark] == ["432"]
    assert dark[0]["title"] == "SEO — universal facet backfill"


@pytest.mark.asyncio
async def test_a_task_with_no_triggers_is_dispatch_on_demand_not_dark(ledger) -> None:
    ledger([_task("f1", "HR Time & Attendance recompute (dispatch-on-demand)")], [])
    assert await queries.find_dark_tasks() == []


@pytest.mark.asyncio
async def test_one_live_trigger_is_enough(ledger) -> None:
    ledger(
        [_task("432", "ok")],
        [{"task_id": "432", "enabled": False}, {"task_id": "432", "enabled": True}],
    )
    assert await queries.find_dark_tasks() == []


@pytest.mark.asyncio
async def test_a_disabled_task_is_not_dark(ledger) -> None:
    ledger([_task("432", "off", enabled=False)], [{"task_id": "432", "enabled": False}])
    assert await queries.find_dark_tasks() == []


@pytest.mark.asyncio
async def test_the_sweep_screams_and_records_but_never_raises(ledger, monkeypatch, caplog) -> None:
    ledger([_task("432", "SEO — universal facet backfill")], [{"task_id": "432", "enabled": False}])
    scanner._status.dark_tasks_checked_at = None
    with caplog.at_level("ERROR"):
        await scanner._sweep_dark_tasks()
    assert [d["id"] for d in scanner._status.dark_tasks] == ["432"]
    assert scanner._status.dark_tasks_checked_at is not None
    assert "dark-schedule" in caplog.text and "fires NOTHING" in caplog.text

    # Throttled: a second call inside the window does not re-query.
    calls = {"n": 0}

    async def counting(*_a, **_k):
        calls["n"] += 1
        return []

    monkeypatch.setattr(queries, "find_dark_tasks", counting)
    await scanner._sweep_dark_tasks()
    assert calls["n"] == 0


@pytest.mark.asyncio
async def test_an_unreadable_ledger_never_breaks_the_scanner(monkeypatch) -> None:
    async def boom(*_a, **_k):
        raise RuntimeError("ledger down")

    monkeypatch.setattr(queries, "find_dark_tasks", boom)
    scanner._status.dark_tasks_checked_at = None
    await scanner._sweep_dark_tasks()  # must not raise
