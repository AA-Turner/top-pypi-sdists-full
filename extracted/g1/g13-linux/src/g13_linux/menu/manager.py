"""
Screen Manager

Manages screen stack and rendering for G13 LCD menu system.
"""

import logging
import threading
from typing import TYPE_CHECKING

from ..lcd.canvas import Canvas
from .screen import InputEvent, Screen

if TYPE_CHECKING:
    from ..hardware.lcd import G13LCD

logger = logging.getLogger(__name__)


class ScreenManager:
    """
    Manages screen stack and coordinates rendering.

    Provides navigation between screens and overlay support for toasts.
    """

    def __init__(self, lcd: "G13LCD | None" = None):
        """
        Initialize screen manager.

        Args:
            lcd: G13LCD instance for display output
        """
        self.lcd = lcd
        self._canvas = Canvas()
        self._stack: list[Screen] = []
        self._overlay: Screen | None = None
        self._overlay_timer: threading.Timer | None = None
        self._lock = threading.Lock()

        # Injected dependencies (set by daemon)
        self.led_controller = None
        self.profile_manager = None
        self.daemon = None

    @property
    def current(self) -> Screen | None:
        """Get current (topmost) screen."""
        with self._lock:
            return self._stack[-1] if self._stack else None

    @property
    def stack_depth(self) -> int:
        """Get number of screens on stack."""
        return len(self._stack)

    def push(self, screen: Screen):
        """
        Push new screen onto stack.

        Args:
            screen: Screen to push
        """
        with self._lock:
            if self._stack:
                self._stack[-1].on_exit()
            self._stack.append(screen)
            screen.on_enter()
            screen.mark_dirty()
            logger.debug(f"Pushed screen: {screen.__class__.__name__}")

    def pop(self) -> Screen | None:
        """
        Pop current screen and return to previous.

        Returns:
            The popped screen, or None if stack was empty
        """
        with self._lock:
            if not self._stack:
                return None

            old = self._stack.pop()
            old.on_exit()
            logger.debug(f"Popped screen: {old.__class__.__name__}")

            if self._stack:
                self._stack[-1].on_enter()
                self._stack[-1].mark_dirty()

            return old

    def pop_to_root(self):
        """Pop all screens except the root (first) screen."""
        with self._lock:
            while len(self._stack) > 1:
                old = self._stack.pop()
                old.on_exit()

            if self._stack:
                self._stack[0].on_enter()
                self._stack[0].mark_dirty()

    def replace(self, screen: Screen):
        """
        Replace current screen with new one.

        Args:
            screen: Screen to show
        """
        with self._lock:
            if self._stack:
                self._stack.pop().on_exit()
            self._stack.append(screen)
            screen.on_enter()
            screen.mark_dirty()

    def show_overlay(self, screen: Screen, duration: float | None = None):
        """
        Show overlay screen (e.g., toast notification).

        Args:
            screen: Overlay screen to show
            duration: Auto-dismiss after seconds (None = manual dismiss)
        """
        self.dismiss_overlay()

        self._overlay = screen
        screen.on_enter()
        screen.mark_dirty()
        logger.debug(f"Showing overlay: {screen.__class__.__name__}")

        if duration is not None:
            self._overlay_timer = threading.Timer(duration, self.dismiss_overlay)
            self._overlay_timer.daemon = True
            self._overlay_timer.start()

    def dismiss_overlay(self):
        """Dismiss current overlay."""
        if self._overlay_timer:
            self._overlay_timer.cancel()
            self._overlay_timer = None

        if self._overlay:
            self._overlay.on_exit()
            self._overlay = None
            if self.current:
                self.current.mark_dirty()
            logger.debug("Overlay dismissed")

    def handle_input(self, event: InputEvent):
        """
        Route input to current screen or overlay.

        Args:
            event: Input event to handle
        """
        # Overlay gets first chance at input
        if self._overlay:
            if self._overlay.on_input(event):
                return

        # Then current screen
        if self.current:
            self.current.on_input(event)

    def update(self, dt: float):
        """
        Update all active screens.

        Args:
            dt: Time delta since last update
        """
        if self.current:
            self.current.update(dt)
        if self._overlay:
            self._overlay.update(dt)

    def render(self) -> bool:
        """
        Render current screen and overlay if dirty.

        Returns:
            True if rendering occurred
        """
        needs_render = False

        # Check if anything needs rendering
        if self.current and self.current.is_dirty:
            needs_render = True
        if self._overlay and self._overlay.is_dirty:
            needs_render = True

        if not needs_render:
            return False

        # Render current screen
        if self.current and self.current.is_dirty:
            self._canvas.clear()
            self.current.render(self._canvas)
            self.current._dirty = False

        # Render overlay on top
        if self._overlay and self._overlay.is_dirty:
            self._overlay.render(self._canvas)
            self._overlay._dirty = False

        # Send to LCD
        if self.lcd:
            self.lcd.write_bitmap(self._canvas.to_bytes())

        return True

    def force_render(self):
        """Force a full re-render."""
        if self.current:
            self.current.mark_dirty()
        if self._overlay:
            self._overlay.mark_dirty()
        self.render()
