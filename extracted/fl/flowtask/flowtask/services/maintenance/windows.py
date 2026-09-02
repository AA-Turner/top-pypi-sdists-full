"""Maintenance window registration, listing and email notification.

A maintenance window is a day plus an hour range. Windows are persisted through
:class:`MaintenanceStore` and advertised on the status page. On server startup
the service emails the configured recipient a summary of the upcoming windows
using ``async-notify``'s Email provider.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from .models import MaintenanceWindow
from .store import MaintenanceStore

logger = logging.getLogger(__name__)


class MaintenanceWindowManager:
    """CRUD-ish coordinator for maintenance windows over a store.

    Args:
        store: The persistence backend.
    """

    def __init__(self, store: MaintenanceStore) -> None:
        self.store = store
        self.logger = logger

    async def register(self, window: MaintenanceWindow) -> MaintenanceWindow:
        """Persist a new maintenance window, assigning an id when missing."""
        if not window.identifier:
            window.identifier = uuid.uuid4().hex
        await self.store.save_window(window)
        self.logger.info(
            "Registered maintenance window %s (%s %s-%s)",
            window.identifier,
            window.day,
            window.start_time,
            window.end_time,
        )
        return window

    async def all_windows(self) -> list[MaintenanceWindow]:
        """Return every stored window sorted by start time."""
        return await self.store.list_windows()

    async def upcoming(
        self, now: Optional[datetime] = None
    ) -> list[MaintenanceWindow]:
        """Return windows that are active now or start in the future."""
        moment = now or datetime.now(timezone.utc)
        return [w for w in await self.store.list_windows() if w.is_upcoming(moment)]

    async def remove(self, identifier: str) -> bool:
        """Delete a window by id; ``True`` when one was removed."""
        return await self.store.remove_window(identifier)


class MaintenanceNotifier:
    """Send maintenance-window notifications by email via ``async-notify``.

    The notifier degrades gracefully: if ``async-notify`` or the SMTP settings
    are unavailable it logs and returns ``False`` instead of raising, so a
    misconfigured mailer never blocks startup.

    Args:
        recipient: Destination email address.
        account: SMTP account dict (``host``/``port``/``username``/``password``).
        sender_name: Display name for the recipient actor.
    """

    def __init__(
        self,
        *,
        recipient: Optional[str] = None,
        account: Optional[dict] = None,
        sender_name: str = "Flowtask Operations",
    ) -> None:
        self.recipient = recipient
        self.account = account or {}
        self.sender_name = sender_name
        self.logger = logger

    def _build_message(self, windows: list[MaintenanceWindow]) -> str:
        """Compose a plain-text body listing the upcoming windows."""
        lines = ["The following maintenance windows are scheduled:", ""]
        for w in windows:
            lines.append(f"• {w.title}")
            lines.append(
                f"  {w.day.isoformat()} "
                f"{w.start_time.strftime('%H:%M')}–{w.end_time.strftime('%H:%M')}"
            )
            if w.description:
                lines.append(f"  {w.description}")
            lines.append("")
        return "\n".join(lines)

    async def notify_upcoming(self, windows: list[MaintenanceWindow]) -> bool:
        """Email the recipient a summary of ``windows``.

        Returns:
            ``True`` when an email was dispatched, ``False`` otherwise.
        """
        if not windows:
            self.logger.info("No upcoming maintenance windows to notify.")
            return False
        if not self.recipient or not self.account.get("host"):
            self.logger.warning(
                "Maintenance email skipped: recipient or SMTP host not configured."
            )
            return False
        try:
            from notify.models import Actor
            from notify.providers.email import Email
        except ImportError as err:  # pragma: no cover - notify optional at test time
            self.logger.warning("async-notify unavailable; email skipped (%s).", err)
            return False

        account = dict(self.account)
        if "port" in account:
            try:
                account["port"] = int(account["port"])
            except (TypeError, ValueError):
                pass

        actor = Actor(
            name=self.sender_name, account={"address": self.recipient}
        )
        subject = f"[Flowtask] {len(windows)} upcoming maintenance window(s)"
        message = self._build_message(windows)
        try:
            mailer = Email(**account)
            async with mailer as mail:
                await mail.send(
                    recipient=actor, subject=subject, message=message
                )
            self.logger.info(
                "Maintenance notification sent to %s for %d window(s).",
                self.recipient,
                len(windows),
            )
            return True
        except Exception as err:  # network / SMTP best-effort
            self.logger.error("Failed to send maintenance email: %s", err)
            return False
