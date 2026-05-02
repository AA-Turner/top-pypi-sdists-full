"""
Navigation Controller

State machine for menu navigation.
"""

import logging
from enum import Enum
from typing import TYPE_CHECKING

from ..menu.screen import InputEvent

if TYPE_CHECKING:
    from ..menu.manager import ScreenManager
    from ..menu.screen import Screen

logger = logging.getLogger(__name__)


class NavigationState(Enum):
    """Navigation state machine states."""

    IDLE = "idle"  # Showing idle/status screen
    MENU = "menu"  # In menu navigation
    EDITING = "editing"  # Editing a value


class NavigationController:
    """
    Controls navigation flow between screens.

    Handles transitions between idle, menu, and editing states.
    """

    def __init__(self, screen_manager: "ScreenManager", idle_screen: "Screen"):
        """
        Initialize navigation controller.

        Args:
            screen_manager: ScreenManager for screen transitions
            idle_screen: Default idle screen to show
        """
        self.screen_manager = screen_manager
        self.idle_screen = idle_screen
        self.state = NavigationState.IDLE

        # Profile quick-switch callbacks
        self._profile_callbacks: dict[InputEvent, callable] = {}

        # Initialize with idle screen
        screen_manager.push(idle_screen)
        logger.info("Navigation controller initialized")

    def on_input(self, event: InputEvent):
        """
        Handle input based on current state.

        Args:
            event: Input event to handle
        """
        logger.debug(f"Input: {event.value} (state: {self.state.value})")

        if self.state == NavigationState.IDLE:
            self._handle_idle_input(event)
        else:
            # Delegate to screen manager
            self.screen_manager.handle_input(event)
            self._update_state()

    def _handle_idle_input(self, event: InputEvent):
        """
        Handle input when in idle state.

        Args:
            event: Input event
        """
        if event == InputEvent.STICK_PRESS:
            # Open main menu
            self._open_main_menu()
            return

        # Quick profile switch with M-keys
        if event in (
            InputEvent.BUTTON_M1,
            InputEvent.BUTTON_M2,
            InputEvent.BUTTON_M3,
        ):
            callback = self._profile_callbacks.get(event)
            if callback:
                callback()
            return

        # Other events pass through to idle screen
        self.screen_manager.handle_input(event)

    def _open_main_menu(self):
        """Open the main menu."""
        from ..menu.screens.main_menu import MainMenuScreen

        menu = MainMenuScreen(self.screen_manager)
        self.screen_manager.push(menu)
        self.state = NavigationState.MENU
        logger.info("Opened main menu")

    def _update_state(self):
        """Update state based on screen stack depth."""
        depth = self.screen_manager.stack_depth

        if depth <= 1:
            self.state = NavigationState.IDLE
        else:
            self.state = NavigationState.MENU

    def go_home(self):
        """Return to idle screen."""
        self.screen_manager.pop_to_root()
        self.state = NavigationState.IDLE
        logger.info("Returned to home")

    def set_profile_callback(self, event: InputEvent, callback: callable):
        """
        Set callback for quick profile switch.

        Args:
            event: M-key event (M1, M2, M3)
            callback: Function to call
        """
        if event in (InputEvent.BUTTON_M1, InputEvent.BUTTON_M2, InputEvent.BUTTON_M3):
            self._profile_callbacks[event] = callback

    def show_toast(self, message: str, duration: float = 2.0):
        """
        Show a toast notification.

        Args:
            message: Message to display
            duration: Display duration in seconds
        """
        from ..menu.screens.toast import ToastScreen

        toast = ToastScreen(self.screen_manager, message)
        self.screen_manager.show_overlay(toast, duration)
