"""System monitors for proactive notifications.

Polls system metrics via psutil and watches filesystem for new files.
All monitors are async-friendly and designed for long-running background use.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from collections.abc import Awaitable, Callable
from pathlib import Path

import psutil

logger = logging.getLogger(__name__)

# Cooldown between same-type alerts (seconds)
ALERT_COOLDOWN = 30 * 60  # 30 minutes


class SystemMonitor:
    """Polls system metrics and fires alerts for abnormal conditions.

    Checks: battery, CPU, RAM, disk space.
    Each check has an independent cooldown to prevent spam.
    """

    def __init__(
        self,
        notify_fn: Callable[[str], Awaitable[None]],
        interval: float = 60.0,
    ) -> None:
        self._notify = notify_fn
        self._interval = interval
        self._last_alert: dict[str, float] = {}  # alert_type → timestamp

    def _can_alert(self, alert_type: str) -> bool:
        last = self._last_alert.get(alert_type, 0.0)
        if time.monotonic() - last < ALERT_COOLDOWN:
            return False
        self._last_alert[alert_type] = time.monotonic()
        return True

    async def run(self) -> None:
        """Run the monitoring loop indefinitely."""
        logger.info("SystemMonitor started (interval=%ds)", self._interval)
        try:
            while True:
                await self._check_all()
                await asyncio.sleep(self._interval)
        except asyncio.CancelledError:
            pass

    async def _check_all(self) -> None:
        """Run all system checks."""
        await self._check_battery()
        await self._check_cpu()
        await self._check_ram()
        await self._check_disk()

    async def _check_battery(self) -> None:
        battery = psutil.sensors_battery()
        if battery is None:
            return
        if battery.percent < 20 and not battery.power_plugged:
            if self._can_alert("battery_low"):
                await self._notify(
                    f"*Low Battery:* {battery.percent}% remaining. Plug in your charger soon."
                )

    async def _check_cpu(self) -> None:
        # Use a 10-second window average to avoid transient spikes
        cpu = await asyncio.to_thread(psutil.cpu_percent, interval=5)
        if cpu > 90:
            if self._can_alert("cpu_high"):
                await self._notify(
                    f"*High CPU Usage:* {cpu:.0f}% — your computer may be slow. "
                    f"Check running processes."
                )

    async def _check_ram(self) -> None:
        mem = psutil.virtual_memory()
        if mem.percent > 90:
            if self._can_alert("ram_high"):
                used_gb = mem.used / (1024**3)
                total_gb = mem.total / (1024**3)
                await self._notify(
                    f"*High Memory Usage:* {mem.percent:.0f}% "
                    f"({used_gb:.1f}/{total_gb:.1f} GB). "
                    f"Close some applications to free memory."
                )

    async def _check_disk(self) -> None:
        try:
            usage = psutil.disk_usage("C:\\")
        except OSError:
            usage = psutil.disk_usage("/")
        free_gb = usage.free / (1024**3)
        if free_gb < 5:
            if self._can_alert("disk_low"):
                await self._notify(
                    f"*Low Disk Space:* {free_gb:.1f} GB free on system drive. "
                    f"Clean up files to avoid issues."
                )


class FileWatchHandler:
    """Watches directories for new files and notifies the user.

    Uses polling instead of OS-level watchers for maximum compatibility.
    Debounces by waiting 5s after detecting a new file (in case it's still
    being written/downloaded).
    """

    def __init__(
        self,
        notify_fn: Callable[[str], Awaitable[None]],
        watch_dirs: list[str],
        interval: float = 10.0,
    ) -> None:
        self._notify = notify_fn
        self._watch_dirs = [Path(os.path.expanduser(d)) for d in watch_dirs]
        self._interval = interval
        self._known_files: dict[str, set[str]] = {}

    async def run(self) -> None:
        """Run the file watching loop."""
        # Initialize known files
        for d in self._watch_dirs:
            if d.is_dir():
                self._known_files[str(d)] = {f.name for f in d.iterdir() if f.is_file()}

        logger.info(
            "FileWatcher started for: %s",
            [str(d) for d in self._watch_dirs],
        )

        try:
            while True:
                await asyncio.sleep(self._interval)
                await self._check_new_files()
        except asyncio.CancelledError:
            pass

    async def _check_new_files(self) -> None:
        """Check for new files in watched directories."""
        for d in self._watch_dirs:
            if not d.is_dir():
                continue

            dir_key = str(d)
            current_files = {f.name for f in d.iterdir() if f.is_file()}
            known = self._known_files.get(dir_key, set())
            new_files = current_files - known

            for fname in new_files:
                fpath = d / fname
                # Debounce: wait 5s to ensure file is fully written
                await asyncio.sleep(5)

                if not fpath.exists():
                    continue

                try:
                    size = fpath.stat().st_size
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size / 1024:.1f} KB"
                    else:
                        size_str = f"{size / (1024 * 1024):.1f} MB"

                    await self._notify(f"*New file in {d.name}:* {fname} ({size_str})")
                except OSError:
                    pass

            self._known_files[dir_key] = current_files
