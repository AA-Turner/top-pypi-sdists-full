"""Native window setup shared by local and hosted simulation."""

from __future__ import annotations

import sys
from contextlib import suppress
from typing import Any


def open_window(cv2: Any, title: str) -> None:
    with suppress(Exception):
        cv2.startWindowThread()
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    with suppress(Exception):
        cv2.setWindowProperty(title, cv2.WND_PROP_TOPMOST, 1)
    if sys.platform == "darwin":
        with suppress(Exception):
            import AppKit

            app = AppKit.NSRunningApplication.currentApplication()
            app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
