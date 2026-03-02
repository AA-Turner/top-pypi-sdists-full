"""Data models for the automation subsystem (cron jobs, heartbeat, webhooks)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ScheduleType(str, Enum):
    AT = "at"        # One-shot at a specific ISO datetime
    EVERY = "every"  # Recurring interval ("30m", "2h", "1d", "1w")
    CRON = "cron"    # Cron expression ("0 9 * * 1-5")


class ExecutionMode(str, Enum):
    MAIN_SESSION = "main_session"  # Injected into the active conversation
    ISOLATED = "isolated"          # Separate agent run


@dataclass
class AutomationJob:
    id: str                       # hex[:12]
    name: str
    schedule_type: str            # at / every / cron
    schedule_value: str           # ISO datetime / "30m" / "0 9 * * 1-5"
    payload: str                  # message sent to agent
    mode: str                     # main_session / isolated
    enabled: bool = True
    one_shot: bool = False
    created_at: str = ""
    last_run_at: str | None = None
    next_run_at: str | None = None
    run_count: int = 0
    consecutive_errors: int = 0
    last_status: str = ""       # "ok" | "error"
    last_error: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "schedule_type": self.schedule_type,
            "schedule_value": self.schedule_value,
            "payload": self.payload,
            "mode": self.mode,
            "enabled": self.enabled,
            "one_shot": self.one_shot,
            "created_at": self.created_at,
            "last_run_at": self.last_run_at,
            "next_run_at": self.next_run_at,
            "run_count": self.run_count,
            "consecutive_errors": self.consecutive_errors,
            "last_status": self.last_status,
            "last_error": self.last_error,
        }

    @classmethod
    def from_dict(cls, d: dict) -> AutomationJob:
        return cls(
            id=d["id"],
            name=d["name"],
            schedule_type=d["schedule_type"],
            schedule_value=d["schedule_value"],
            payload=d["payload"],
            mode=d.get("mode", "main_session"),
            enabled=d.get("enabled", True),
            one_shot=d.get("one_shot", False),
            created_at=d.get("created_at", ""),
            last_run_at=d.get("last_run_at"),
            next_run_at=d.get("next_run_at"),
            run_count=d.get("run_count", 0),
            consecutive_errors=d.get("consecutive_errors", 0),
            last_status=d.get("last_status", ""),
            last_error=d.get("last_error"),
        )


@dataclass
class HeartbeatConfig:
    enabled: bool = False
    interval_minutes: int = 30
    active_hours: tuple[int, int] = (8, 22)
    payload: str = "Heartbeat: check pending tasks, notifications, and scheduled reviews."

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "interval_minutes": self.interval_minutes,
            "active_hours": list(self.active_hours),
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, d: dict) -> HeartbeatConfig:
        ah = d.get("active_hours", [8, 22])
        return cls(
            enabled=d.get("enabled", False),
            interval_minutes=d.get("interval_minutes", 30),
            active_hours=(ah[0], ah[1]) if isinstance(ah, (list, tuple)) and len(ah) >= 2 else (8, 22),
            payload=d.get("payload", cls.payload),
        )


@dataclass
class WebhookConfig:
    enabled: bool = False
    token: str = ""
    custom_hooks: dict[str, str] = field(default_factory=dict)  # name -> payload template

    def to_dict(self) -> dict:
        return {
            "enabled": self.enabled,
            "token": self.token,
            "custom_hooks": dict(self.custom_hooks),
        }

    @classmethod
    def from_dict(cls, d: dict) -> WebhookConfig:
        return cls(
            enabled=d.get("enabled", False),
            token=d.get("token", ""),
            custom_hooks=d.get("custom_hooks", {}),
        )


@dataclass
class AutomationConfig:
    cron_enabled: bool = False
    heartbeat: HeartbeatConfig = field(default_factory=HeartbeatConfig)
    webhooks: WebhookConfig = field(default_factory=WebhookConfig)
    max_concurrent_runs: int = 2

    def to_dict(self) -> dict:
        return {
            "cron_enabled": self.cron_enabled,
            "heartbeat": self.heartbeat.to_dict(),
            "webhooks": self.webhooks.to_dict(),
            "max_concurrent_runs": self.max_concurrent_runs,
        }

    @classmethod
    def from_dict(cls, d: dict) -> AutomationConfig:
        return cls(
            cron_enabled=d.get("cron_enabled", False),
            heartbeat=HeartbeatConfig.from_dict(d.get("heartbeat", {})),
            webhooks=WebhookConfig.from_dict(d.get("webhooks", {})),
            max_concurrent_runs=d.get("max_concurrent_runs", 2),
        )
