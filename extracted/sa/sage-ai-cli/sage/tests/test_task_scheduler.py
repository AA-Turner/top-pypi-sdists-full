"""Tests for TaskScheduler — sage's answer to OpenClaw's autonomous cron.

Persists scheduled tasks to ~/.sage/scheduled_tasks.json. Each task has:
  - a unique ID
  - a sage prompt to run
  - a schedule (cron expression or interval string)
  - last_run_at / next_run_at timestamps
  - a status (active / paused)

A separate runner (sage schedule run-due) executes tasks whose
next_run_at is in the past, updates their state, and persists.

TDD: tests describe the contract. The implementation uses simple cron
expressions ("0 9 * * 1" = Mondays at 9am) and interval strings ("5m",
"1h", "1d") for the most common scheduling needs.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from sage.core.task_scheduler import (
    ScheduledTask,
    TaskScheduler,
    InvalidScheduleError,
)


# ── Task data shape ──────────────────────────────────────────────────────────


class TestScheduledTask:
    def test_task_has_required_fields(self):
        task = ScheduledTask(
            id="abc",
            prompt="check my email",
            schedule="0 9 * * *",
            status="active",
            last_run_at=None,
            next_run_at=datetime(2026, 5, 16, 9, 0, tzinfo=timezone.utc),
        )
        assert task.id == "abc"
        assert task.status == "active"

    def test_task_round_trips_to_dict(self):
        next_run = datetime(2026, 5, 16, 9, 0, tzinfo=timezone.utc)
        task = ScheduledTask(
            id="abc", prompt="x", schedule="5m", status="active",
            last_run_at=None, next_run_at=next_run,
        )
        d = task.to_dict()
        round = ScheduledTask.from_dict(d)
        assert round.id == task.id
        assert round.prompt == task.prompt
        assert round.schedule == task.schedule
        assert round.next_run_at == task.next_run_at

    def test_paused_status_persists(self):
        t = ScheduledTask.from_dict({
            "id": "abc", "prompt": "x", "schedule": "1h",
            "status": "paused", "last_run_at": None, "next_run_at": None,
        })
        assert t.status == "paused"


# ── Scheduler.add() ──────────────────────────────────────────────────────────


class TestAdd:
    @pytest.fixture
    def scheduler(self, tmp_path):
        return TaskScheduler(state_path=tmp_path / "tasks.json")

    def test_add_creates_unique_id(self, scheduler):
        t1 = scheduler.add("check email", "1h")
        t2 = scheduler.add("post tweet", "1d")
        assert t1.id != t2.id

    def test_add_sets_status_active(self, scheduler):
        t = scheduler.add("x", "5m")
        assert t.status == "active"

    def test_add_persists_to_disk(self, scheduler, tmp_path):
        scheduler.add("x", "5m")
        assert (tmp_path / "tasks.json").exists()
        scheduler2 = TaskScheduler(state_path=tmp_path / "tasks.json")
        assert len(scheduler2.list()) == 1

    def test_add_computes_next_run_at(self, scheduler):
        before = _now()
        t = scheduler.add("x", "5m")
        # next_run_at should be approximately 5 minutes from now
        assert t.next_run_at is not None
        delta = (t.next_run_at - before).total_seconds()
        assert 290 < delta < 310  # 5 min ± 10s

    def test_add_supports_interval_strings(self, scheduler):
        scheduler.add("x", "1m")
        scheduler.add("x", "30m")
        scheduler.add("x", "1h")
        scheduler.add("x", "1d")
        assert len(scheduler.list()) == 4

    def test_add_supports_cron_expressions(self, scheduler):
        # Mondays at 9am — full 5-field cron
        t = scheduler.add("weekly check", "0 9 * * 1")
        assert t.schedule == "0 9 * * 1"
        assert t.next_run_at is not None

    def test_add_rejects_invalid_schedule(self, scheduler):
        with pytest.raises(InvalidScheduleError):
            scheduler.add("x", "not a schedule")

    def test_add_empty_prompt_raises(self, scheduler):
        with pytest.raises(ValueError, match="empty"):
            scheduler.add("", "5m")


# ── Scheduler.list() / get() ─────────────────────────────────────────────────


class TestListAndGet:
    @pytest.fixture
    def scheduler(self, tmp_path):
        s = TaskScheduler(state_path=tmp_path / "tasks.json")
        s.add("first", "5m")
        s.add("second", "1h")
        return s

    def test_list_returns_all_tasks(self, scheduler):
        assert len(scheduler.list()) == 2

    def test_get_returns_task_by_id(self, scheduler):
        first = scheduler.list()[0]
        fetched = scheduler.get(first.id)
        assert fetched.id == first.id

    def test_get_missing_returns_none(self, scheduler):
        assert scheduler.get("does-not-exist") is None


# ── Scheduler.remove() / pause() / resume() ──────────────────────────────────


class TestLifecycle:
    @pytest.fixture
    def scheduler(self, tmp_path):
        return TaskScheduler(state_path=tmp_path / "tasks.json")

    def test_remove_drops_task(self, scheduler):
        t = scheduler.add("x", "5m")
        scheduler.remove(t.id)
        assert scheduler.get(t.id) is None
        assert scheduler.list() == []

    def test_remove_unknown_id_is_noop(self, scheduler):
        # Should not raise — idempotent
        scheduler.remove("unknown")

    def test_pause_marks_status_paused(self, scheduler):
        t = scheduler.add("x", "5m")
        scheduler.pause(t.id)
        assert scheduler.get(t.id).status == "paused"

    def test_resume_marks_status_active(self, scheduler):
        t = scheduler.add("x", "5m")
        scheduler.pause(t.id)
        scheduler.resume(t.id)
        assert scheduler.get(t.id).status == "active"


# ── Due-task discovery ──────────────────────────────────────────────────────


class TestDueTasks:
    @pytest.fixture
    def scheduler(self, tmp_path):
        return TaskScheduler(state_path=tmp_path / "tasks.json")

    def test_due_returns_tasks_whose_next_run_passed(self, scheduler):
        # Manually set next_run_at to the past
        t = scheduler.add("x", "1h")
        # Backdate it to make it due
        scheduler._tasks[t.id] = scheduler._tasks[t.id].with_next_run_at(_now() - timedelta(minutes=1))
        scheduler._save()
        due = scheduler.due_now()
        assert len(due) == 1
        assert due[0].id == t.id

    def test_due_skips_future_tasks(self, scheduler):
        scheduler.add("x", "1h")  # next_run_at is 1h in the future
        assert scheduler.due_now() == []

    def test_due_skips_paused_tasks(self, scheduler):
        t = scheduler.add("x", "1h")
        scheduler._tasks[t.id] = scheduler._tasks[t.id].with_next_run_at(_now() - timedelta(minutes=1))
        scheduler.pause(t.id)
        assert scheduler.due_now() == []


# ── Mark run ─────────────────────────────────────────────────────────────────


class TestMarkRun:
    def test_mark_run_updates_last_and_next(self, tmp_path):
        scheduler = TaskScheduler(state_path=tmp_path / "tasks.json")
        t = scheduler.add("x", "5m")
        before_next = t.next_run_at
        scheduler.mark_run(t.id)
        after = scheduler.get(t.id)
        assert after.last_run_at is not None
        # Next run pushed forward by another interval
        assert after.next_run_at > before_next


# ── Helpers ──────────────────────────────────────────────────────────────────


def _now() -> datetime:
    return datetime.now(timezone.utc)
