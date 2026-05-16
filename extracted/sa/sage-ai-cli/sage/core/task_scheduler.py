"""Scheduled tasks — sage's answer to OpenClaw's autonomous cron-driven agent.

Lets users persist prompts that should run on a schedule:

    sage schedule add "check my email and summarize new ones" --every 1h
    sage schedule add "post Monday's product update" --cron "0 9 * * 1"
    sage schedule list
    sage schedule pause <id>
    sage schedule remove <id>

A separate runner — `sage schedule run-due` — executes any tasks whose
``next_run_at`` is in the past, updates their state, and persists. The
runner can be invoked manually, or scheduled via the user's OS cron /
launchd / systemd timer for full autonomy.

Storage: ``~/.sage/scheduled_tasks.json``. Plain JSON for portability —
no Redis or DB. Locking via atomic-replace on write.
"""

from __future__ import annotations

import json
import logging
import re
import secrets
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

logger = logging.getLogger("sage.task_scheduler")


# Default state path. Tests override via constructor arg.
_DEFAULT_STATE_PATH = Path.home() / ".sage" / "scheduled_tasks.json"


class InvalidScheduleError(ValueError):
    """Raised when a schedule string can't be parsed as either an
    interval ("5m", "1h", "1d") or a cron expression (5 fields)."""


# ── Schedule parsing ─────────────────────────────────────────────────────────


# Interval strings: <number><unit> where unit ∈ {s,m,h,d,w}
# (seconds disabled by default because <1m schedules are usually a mistake,
# but tests can opt in by passing through directly).
_INTERVAL_RE = re.compile(r"^\s*(\d+)\s*(m|h|d|w)\s*$", re.IGNORECASE)

# Cron: 5 fields (minute hour day-of-month month day-of-week). We don't
# support extended cron (@reboot, @yearly etc.) — keep parsing simple.
_CRON_RE = re.compile(r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$")


def _parse_schedule_to_next_run(schedule: str, base: datetime | None = None) -> datetime:
    """Given a schedule string, return the next datetime it should fire.

    Raises InvalidScheduleError on garbage input.
    """
    if base is None:
        base = datetime.now(timezone.utc)

    # Interval form first — much more common
    m = _INTERVAL_RE.match(schedule)
    if m:
        n, unit = int(m.group(1)), m.group(2).lower()
        delta = {
            "m": timedelta(minutes=n),
            "h": timedelta(hours=n),
            "d": timedelta(days=n),
            "w": timedelta(weeks=n),
        }[unit]
        return base + delta

    # Cron form — minimal support: literal numbers + "*" in each field
    if _CRON_RE.match(schedule):
        return _cron_next(schedule, base)

    raise InvalidScheduleError(
        f"Could not parse schedule {schedule!r}. "
        "Use an interval like '5m', '1h', '2d', '1w', or a 5-field cron "
        "expression like '0 9 * * 1' (Mondays at 9am)."
    )


def _cron_next(cron: str, base: datetime) -> datetime:
    """Compute the next fire time for a 5-field cron expression.

    Intentionally minimal: supports '*' wildcard and literal integers per
    field. No ranges, lists, or step values yet. Good enough for the
    common patterns ("every day at 9am", "every Monday at noon", etc.);
    we can layer croniter on top if users need fancier expressions.
    """
    minute_f, hour_f, dom_f, month_f, dow_f = cron.split()

    # Start checking from the next minute boundary so we don't fire
    # immediately on schedules that match "now exactly".
    candidate = base.replace(second=0, microsecond=0) + timedelta(minutes=1)

    # Search up to one year ahead. Most expressions match within a week.
    # If we don't find a match in 366 days, the cron is effectively a
    # never-fires schedule and we raise.
    for _ in range(366 * 24 * 60):
        if (
            _cron_field_matches(candidate.minute, minute_f)
            and _cron_field_matches(candidate.hour, hour_f)
            and _cron_field_matches(candidate.day, dom_f)
            and _cron_field_matches(candidate.month, month_f)
            and _cron_field_matches(_cron_dow(candidate), dow_f)
        ):
            return candidate
        candidate += timedelta(minutes=1)
    raise InvalidScheduleError(
        f"Cron expression {cron!r} does not match any time in the next year"
    )


def _cron_field_matches(value: int, field_expr: str) -> bool:
    """True if ``value`` matches ``field_expr``. Supports '*' and integers."""
    if field_expr == "*":
        return True
    try:
        return int(field_expr) == value
    except ValueError:
        # Future: support ranges (1-5), lists (1,2,3), steps (*/5)
        return False


def _cron_dow(dt: datetime) -> int:
    """Cron day-of-week: 0=Sunday..6=Saturday (matches POSIX cron)."""
    # Python's weekday(): Monday=0..Sunday=6
    return (dt.weekday() + 1) % 7


# ── Data type ────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ScheduledTask:
    id: str
    prompt: str
    schedule: str
    status: str  # "active" | "paused"
    last_run_at: datetime | None
    next_run_at: datetime | None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "schedule": self.schedule,
            "status": self.status,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "next_run_at": self.next_run_at.isoformat() if self.next_run_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduledTask":
        return cls(
            id=data["id"],
            prompt=data["prompt"],
            schedule=data["schedule"],
            status=data.get("status", "active"),
            last_run_at=_parse_iso(data.get("last_run_at")),
            next_run_at=_parse_iso(data.get("next_run_at")),
        )

    def with_next_run_at(self, when: datetime | None) -> "ScheduledTask":
        return replace(self, next_run_at=when)

    def with_status(self, status: str) -> "ScheduledTask":
        return replace(self, status=status)

    def with_last_run(self, when: datetime, next_when: datetime) -> "ScheduledTask":
        return replace(self, last_run_at=when, next_run_at=next_when)


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    dt = datetime.fromisoformat(s)
    # Ensure tzinfo is set — older JSON might be naive UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


# ── Main scheduler ───────────────────────────────────────────────────────────


class TaskScheduler:
    """Stores + manages scheduled sage tasks. JSON-backed; cheap operations
    do a full reload from disk so multiple sage processes can coordinate."""

    def __init__(self, state_path: Path | None = None):
        self._state_path = Path(state_path or _DEFAULT_STATE_PATH)
        self._tasks: dict[str, ScheduledTask] = {}
        self._load()

    # ── CRUD ──────────────────────────────────────────────────────────────

    def add(self, prompt: str, schedule: str) -> ScheduledTask:
        """Register a new scheduled task. Returns the persisted task."""
        if not prompt or not prompt.strip():
            raise ValueError("Cannot schedule an empty prompt.")
        next_run = _parse_schedule_to_next_run(schedule)  # validates schedule

        task = ScheduledTask(
            id=_new_id(),
            prompt=prompt.strip(),
            schedule=schedule,
            status="active",
            last_run_at=None,
            next_run_at=next_run,
        )
        self._tasks[task.id] = task
        self._save()
        return task

    def list(self) -> list[ScheduledTask]:
        return list(self._tasks.values())

    def get(self, task_id: str) -> ScheduledTask | None:
        return self._tasks.get(task_id)

    def remove(self, task_id: str) -> None:
        """Remove a task. Idempotent — no-op if ``task_id`` doesn't exist."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()

    def pause(self, task_id: str) -> None:
        task = self._tasks.get(task_id)
        if task is None:
            return
        self._tasks[task_id] = task.with_status("paused")
        self._save()

    def resume(self, task_id: str) -> None:
        task = self._tasks.get(task_id)
        if task is None:
            return
        self._tasks[task_id] = task.with_status("active")
        self._save()

    # ── Execution helpers ────────────────────────────────────────────────

    def due_now(self) -> list[ScheduledTask]:
        """Return tasks whose ``next_run_at`` is in the past AND whose
        status is 'active'. The runner calls this each tick."""
        now = datetime.now(timezone.utc)
        return [
            t for t in self._tasks.values()
            if t.status == "active"
            and t.next_run_at is not None
            and t.next_run_at <= now
        ]

    def mark_run(self, task_id: str) -> None:
        """Called by the runner after a task fires. Updates last_run_at +
        recomputes next_run_at based on the task's schedule."""
        task = self._tasks.get(task_id)
        if task is None:
            return
        now = datetime.now(timezone.utc)
        next_run = _parse_schedule_to_next_run(task.schedule, base=now)
        self._tasks[task_id] = task.with_last_run(now, next_run)
        self._save()

    # ── Persistence ──────────────────────────────────────────────────────

    def _load(self) -> None:
        if not self._state_path.exists():
            self._tasks = {}
            return
        try:
            raw = json.loads(self._state_path.read_text())
            self._tasks = {
                t["id"]: ScheduledTask.from_dict(t)
                for t in raw.get("tasks", [])
            }
        except Exception as exc:
            logger.warning("Could not load %s: %s", self._state_path, exc)
            self._tasks = {}

    def _save(self) -> None:
        """Atomic write — tmp file + rename — so concurrent reads never
        see a half-written file."""
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._state_path.with_suffix(self._state_path.suffix + ".tmp")
        payload = {"tasks": [t.to_dict() for t in self._tasks.values()]}
        tmp.write_text(json.dumps(payload, indent=2))
        tmp.replace(self._state_path)


def _new_id() -> str:
    """Short, unguessable, URL-safe ID. 8 bytes = 16 hex chars."""
    return secrets.token_hex(8)


__all__ = [
    "ScheduledTask",
    "TaskScheduler",
    "InvalidScheduleError",
]
