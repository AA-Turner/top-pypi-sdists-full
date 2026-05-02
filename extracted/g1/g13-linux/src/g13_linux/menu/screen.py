"""
Screen Base Class

Abstract base class for LCD screens.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..lcd.canvas import Canvas
    from .manager import ScreenManager


class InputEvent(Enum):
    """Input events from G13 controls."""

    STICK_UP = "stick_up"
    STICK_DOWN = "stick_down"
    STICK_LEFT = "stick_left"
    STICK_RIGHT = "stick_right"
    STICK_PRESS = "stick_press"
    BUTTON_BD = "button_bd"  # Back/thumb button
    BUTTON_LEFT = "button_left"  # Left thumb button
    BUTTON_M1 = "button_m1"
    BUTTON_M2 = "button_m2"
    BUTTON_M3 = "button_m3"
    BUTTON_MR = "button_mr"


class Screen(ABC):
    """
    Abstract base class for LCD screens.

    All screens must implement on_input() and render() methods.
    """

    def __init__(self, manager: "ScreenManager"):
        """
        Initialize screen.

        Args:
            manager: ScreenManager instance for navigation
        """
        self.manager = manager
        self._dirty = True

    def mark_dirty(self):
        """Mark screen as needing re-render."""
        self._dirty = True

    @property
    def is_dirty(self) -> bool:
        """Check if screen needs re-render."""
        return self._dirty

    def on_enter(self):
        """
        Called when screen becomes active.

        Override to initialize screen state.
        """
        pass

    def on_exit(self):
        """
        Called when screen is deactivated.

        Override to clean up screen state.
        """
        pass

    @abstractmethod
    def on_input(self, event: InputEvent) -> bool:
        """
        Handle input event.

        Args:
            event: Input event to handle

        Returns:
            True if event was handled, False otherwise
        """
        pass

    @abstractmethod
    def render(self, canvas: "Canvas"):
        """
        Render screen contents to canvas.

        Args:
            canvas: Canvas to draw on
        """
        pass

    def update(self, dt: float):
        """
        Update screen state (called periodically).

        Args:
            dt: Time delta since last update in seconds

        Override for time-based updates (animations, clock, etc.)
        """
        pass
