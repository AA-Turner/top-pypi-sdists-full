"""AutomationManager — singleton facade for the automation subsystem."""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Any

from .models import AutomationConfig, AutomationJob
from .scheduler import CronScheduler
from .storage import AutomationStorage

# Module-level singleton (same pattern as ChannelRouter)
_manager: AutomationManager | None = None


def get_automation_manager() -> AutomationManager | None:
    return _manager


def set_automation_manager(manager: AutomationManager) -> None:
    global _manager
    _manager = manager


class AutomationManager:
    """High-level facade that owns storage + scheduler."""

    def __init__(self, emdash_dir: Path) -> None:
        self._emdash_dir = emdash_dir
        self._storage = AutomationStorage(emdash_dir)
        self._scheduler = CronScheduler(self._storage, emdash_dir)

    # -- Lifecycle -----------------------------------------------------------

    async def start(self, server_url: str) -> None:
        await self._scheduler.start(server_url)

    async def stop(self) -> None:
        await self._scheduler.stop()

    # -- Job CRUD (delegated to scheduler) -----------------------------------

    def add_job(
        self,
        name: str,
        schedule_type: str,
        schedule_value: str,
        payload: str,
        mode: str = "main_session",
    ) -> AutomationJob:
        job_id = secrets.token_hex(6)
        job = AutomationJob(
            id=job_id,
            name=name,
            schedule_type=schedule_type,
            schedule_value=schedule_value,
            payload=payload,
            mode=mode,
        )
        return self._scheduler.add_job(job)

    def remove_job(self, job_id: str) -> bool:
        return self._scheduler.remove_job(job_id)

    def list_jobs(self) -> list[dict]:
        return [j.to_dict() for j in self._scheduler.list_jobs()]

    def update_job(self, job_id: str, **updates: Any) -> AutomationJob | None:
        return self._scheduler.update_job(job_id, **updates)

    # -- Config --------------------------------------------------------------

    def get_config(self) -> AutomationConfig:
        return self._storage.load_config()

    def update_config(self, **updates: Any) -> AutomationConfig:
        config = self._storage.load_config()

        for key, value in updates.items():
            if key == "cron_enabled":
                config.cron_enabled = bool(value)
            elif key == "max_concurrent_runs":
                config.max_concurrent_runs = int(value)
            elif key == "heartbeat_enabled":
                config.heartbeat.enabled = bool(value)
            elif key == "heartbeat_interval":
                config.heartbeat.interval_minutes = int(value)
            elif key == "heartbeat_active_hours":
                if isinstance(value, (list, tuple)) and len(value) >= 2:
                    config.heartbeat.active_hours = (int(value[0]), int(value[1]))
            elif key == "heartbeat_payload":
                config.heartbeat.payload = str(value)
            elif key == "webhooks_enabled":
                config.webhooks.enabled = bool(value)
                if config.webhooks.enabled and not config.webhooks.token:
                    config.webhooks.token = secrets.token_urlsafe(32)
            elif key == "webhooks_token":
                config.webhooks.token = str(value)
            elif key == "custom_hooks":
                if isinstance(value, dict):
                    config.webhooks.custom_hooks.update(value)

        self._storage.save_config(config)
        # Re-sync heartbeat job inside the scheduler
        self._scheduler._ensure_heartbeat()
        return config
