"""Notification engine — orchestrates system monitors, file watchers, and reminders.

Runs as a background subsystem within the orchestrator. Rate-limits all outgoing
notifications to prevent spam.

Dependencies (optional): apscheduler, watchdog, psutil (already core).
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)

# Rate limiting
MAX_NOTIFICATIONS_PER_MINUTE = 1
MAX_NOTIFICATIONS_PER_DAY = 20


class NotificationEngine:
    """Manages all proactive notification sources.

    Sources:
      - SystemMonitor: battery, CPU, RAM, disk
      - FileWatcher: new files in Downloads
      - Scheduler: user-set reminders (via set_reminder tool)
    """

    def __init__(
        self,
        send_fn: Callable[[str, str], Awaitable[None]],
        user_id: str,
        watch_dirs: list[str] | None = None,
        daily_limit: int = MAX_NOTIFICATIONS_PER_DAY,
    ) -> None:
        """Initialize the notification engine.

        Args:
            send_fn: Async callable (to, text) to send a message.
            user_id: The primary user to notify (WhatsApp number).
            watch_dirs: Directories to watch for new files.
            daily_limit: Maximum notifications per day.
        """
        self._send_fn = send_fn
        self._user_id = user_id
        self._watch_dirs = watch_dirs or ["~/Downloads"]
        self._daily_limit = daily_limit
        self._tasks: list[asyncio.Task[None]] = []
        self._scheduler: object | None = None

        # Rate limiting state
        self._last_notification_time = 0.0
        self._daily_count = 0
        self._daily_reset_time = time.monotonic()

    async def _rate_limited_notify(self, text: str) -> None:
        """Send a notification if rate limits allow."""
        now = time.monotonic()

        # Reset daily counter every 24 hours
        if now - self._daily_reset_time > 86400:
            self._daily_count = 0
            self._daily_reset_time = now

        # Check daily limit
        if self._daily_count >= self._daily_limit:
            logger.debug("Daily notification limit reached, skipping")
            return

        # Check per-minute limit
        if now - self._last_notification_time < 60 / MAX_NOTIFICATIONS_PER_MINUTE:
            logger.debug("Rate limit: too soon since last notification, skipping")
            return

        self._last_notification_time = now
        self._daily_count += 1

        try:
            await self._send_fn(self._user_id, text)
        except Exception as e:
            logger.error("Failed to send notification: %s", e)

    async def start(self) -> None:
        """Start all notification sources."""
        logger.info("NotificationEngine starting for user %s", self._user_id)

        # System monitor (psutil — always available)
        from ghost_pc.notifications.monitors import SystemMonitor

        monitor = SystemMonitor(
            notify_fn=self._rate_limited_notify,
            interval=60.0,
        )
        self._tasks.append(asyncio.create_task(monitor.run()))

        # File watcher (polling-based, no extra deps)
        from ghost_pc.notifications.monitors import FileWatchHandler

        watcher = FileWatchHandler(
            notify_fn=self._rate_limited_notify,
            watch_dirs=self._watch_dirs,
            interval=10.0,
        )
        self._tasks.append(asyncio.create_task(watcher.run()))

        # Scheduler for reminders (requires apscheduler, optional)
        try:
            from apscheduler.schedulers.asyncio import AsyncIOScheduler

            self._scheduler = AsyncIOScheduler()
            self._scheduler.start()  # type: ignore[union-attr]
            logger.info("APScheduler started for reminders")
        except ImportError:
            logger.debug("apscheduler not installed — reminders unavailable")

        logger.info("NotificationEngine started (%d sources)", len(self._tasks))

    async def stop(self) -> None:
        """Stop all notification sources."""
        if self._scheduler is not None:
            try:
                self._scheduler.shutdown(wait=False)  # type: ignore[union-attr]
            except Exception:
                pass

        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        logger.info("NotificationEngine stopped")

    def add_reminder(self, description: str, delay_minutes: int) -> bool:
        """Schedule a reminder notification.

        Args:
            description: What to remind the user about.
            delay_minutes: Minutes from now to send the reminder.

        Returns:
            True if scheduled, False if scheduler unavailable.
        """
        if self._scheduler is None:
            return False

        import datetime

        run_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=delay_minutes)

        async def _fire_reminder() -> None:
            await self._rate_limited_notify(f"*Reminder:* {description}")

        try:
            self._scheduler.add_job(  # type: ignore[union-attr]
                _fire_reminder,
                trigger="date",
                run_date=run_time,
                id=f"reminder_{int(time.monotonic())}",
            )
            return True
        except Exception as e:
            logger.error("Failed to schedule reminder: %s", e)
            return False
