"""Periodic abstra-version check for the running editor.

Detection is otherwise boot-only, so a pod that stays up across a release would
never surface the update until it restarts. This re-checks PyPI on an interval
while the editor is actively open (an editor-status websocket is connected),
broadcasting when the availability changes — and stays quiet (no PyPI polling)
when no one is connected.

Mirrors WebEditorHeartbeat's start/stop lifecycle so editor() shuts it down
alongside the other watchers (via shutdown_editor_components).
"""

import threading
from datetime import timedelta
from typing import Optional

from abstra_internals.controllers.editor_status_events import (
    EditorStatusEventController,
)
from abstra_internals.logger import AbstraLogger

# Aligned with the PyPI version cache TTL.
VERSION_CHECK_INTERVAL_SECONDS = 15 * 60


class PeriodicVersionChecker:
    def __init__(self, *, interval: Optional[timedelta] = None):
        self._interval = interval or timedelta(seconds=VERSION_CHECK_INTERVAL_SECONDS)
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _check_once(self) -> None:
        # Only while the editor is active — an idle pod must not poll PyPI.
        if EditorStatusEventController.has_listeners():
            EditorStatusEventController.refresh_and_broadcast()

    def _run(self) -> None:
        # Wait-first: boot's _initial_lint already ran the initial check, so the
        # first periodic check is one interval in. Event.wait returns True as
        # soon as stop() is called, so shutdown is near-instant.
        while not self._stop_event.wait(self._interval.total_seconds()):
            try:
                self._check_once()
            except Exception as e:
                AbstraLogger.error(f"[VersionCheck] Periodic version check failed: {e}")

    def start(self) -> None:
        if self._thread is not None:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="PeriodicVersionCheck",
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        self._stop_event.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=timeout)
            self._thread = None
