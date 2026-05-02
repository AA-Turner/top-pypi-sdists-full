"""
Settings Screen

General settings configuration with persistence.
"""

from ..items import MenuItem
from .base_menu import MenuScreen
from .toast import ToastScreen


class SettingsScreen(MenuScreen):
    """
    General settings menu.

    Provides access to device and application settings.
    Settings are persisted via SettingsManager.
    """

    def __init__(self, manager):
        """
        Initialize settings screen.

        Args:
            manager: ScreenManager instance
        """
        self.settings_mgr = getattr(manager, "settings_manager", None)

        items = [
            MenuItem(
                id="clock",
                label="Clock Display",
                submenu=lambda: ClockSettingsScreen(manager),
            ),
            MenuItem(
                id="idle_timeout",
                label="Idle Timeout",
                value_getter=self._get_timeout_value,
                submenu=lambda: TimeoutSettingsScreen(manager),
            ),
            MenuItem(
                id="stick_sensitivity",
                label="Stick Sensitivity",
                value_getter=self._get_sensitivity_value,
                action=self._cycle_sensitivity,
            ),
            MenuItem(
                id="reset",
                label="Reset to Defaults",
                action=self._reset_defaults,
            ),
        ]
        super().__init__(manager, "SETTINGS", items)

    def _get_timeout_value(self) -> str:
        """Get current timeout as display string."""
        if not self.settings_mgr:
            return "30s"
        timeout = self.settings_mgr.idle_timeout
        if timeout == 0:
            return "Never"
        elif timeout < 60:
            return f"{timeout}s"
        else:
            return f"{timeout // 60}m"

    def _get_sensitivity_value(self) -> str:
        """Get current sensitivity as display string."""
        if not self.settings_mgr:
            return "Normal"
        return self.settings_mgr.stick_sensitivity.capitalize()

    def _cycle_sensitivity(self):
        """Cycle through sensitivity options."""
        options = ["low", "normal", "high"]
        if self.settings_mgr:
            current = self.settings_mgr.stick_sensitivity
            try:
                idx = options.index(current)
                new_value = options[(idx + 1) % len(options)]
            except ValueError:
                new_value = "normal"
            self.settings_mgr.stick_sensitivity = new_value
            display = new_value.capitalize()
        else:
            display = "Normal"

        toast = ToastScreen(self.manager, f"Sensitivity: {display}")
        self.manager.show_overlay(toast, duration=1.5)
        self.mark_dirty()

    def _reset_defaults(self):
        """Reset all settings to defaults."""
        if self.settings_mgr:
            self.settings_mgr.reset_to_defaults()
        toast = ToastScreen(self.manager, "Settings reset")
        self.manager.show_overlay(toast, duration=2.0)
        self.mark_dirty()


class ClockSettingsScreen(MenuScreen):
    """Clock display settings."""

    def __init__(self, manager):
        self.settings_mgr = getattr(manager, "settings_manager", None)

        items = [
            MenuItem(
                id="format_24",
                label="24-hour",
                value_getter=lambda: self._check_mark("24h"),
                action=lambda: self._set_format("24h"),
            ),
            MenuItem(
                id="format_12",
                label="12-hour",
                value_getter=lambda: self._check_mark("12h"),
                action=lambda: self._set_format("12h"),
            ),
            MenuItem(
                id="show_seconds",
                label="Show Seconds",
                value_getter=self._get_seconds_value,
                action=self._toggle_seconds,
            ),
            MenuItem(
                id="show_date",
                label="Show Date",
                value_getter=self._get_date_value,
                action=self._toggle_date,
            ),
        ]
        super().__init__(manager, "CLOCK", items)

    def _check_mark(self, fmt: str) -> str:
        """Return checkmark if this format is selected."""
        if self.settings_mgr and self.settings_mgr.clock_format == fmt:
            return "*"
        return ""

    def _get_seconds_value(self) -> str:
        """Get show seconds setting."""
        if self.settings_mgr:
            return "On" if self.settings_mgr.clock_show_seconds else "Off"
        return "On"

    def _get_date_value(self) -> str:
        """Get show date setting."""
        if self.settings_mgr:
            return "On" if self.settings_mgr.clock_show_date else "Off"
        return "On"

    def _set_format(self, fmt: str):
        """Set clock format."""
        if self.settings_mgr:
            self.settings_mgr.clock_format = fmt
        toast = ToastScreen(self.manager, f"Format: {fmt}")
        self.manager.show_overlay(toast, duration=1.5)
        self.mark_dirty()

    def _toggle_seconds(self):
        """Toggle show seconds."""
        if self.settings_mgr:
            new_value = not self.settings_mgr.clock_show_seconds
            self.settings_mgr.clock_show_seconds = new_value
            display = "On" if new_value else "Off"
        else:
            display = "On"
        toast = ToastScreen(self.manager, f"Seconds: {display}")
        self.manager.show_overlay(toast, duration=1.5)
        self.mark_dirty()

    def _toggle_date(self):
        """Toggle show date."""
        if self.settings_mgr:
            new_value = not self.settings_mgr.clock_show_date
            self.settings_mgr.clock_show_date = new_value
            display = "On" if new_value else "Off"
        else:
            display = "On"
        toast = ToastScreen(self.manager, f"Date: {display}")
        self.manager.show_overlay(toast, duration=1.5)
        self.mark_dirty()


class TimeoutSettingsScreen(MenuScreen):
    """Idle timeout settings."""

    TIMEOUT_OPTIONS = [
        (0, "Never"),
        (15, "15 seconds"),
        (30, "30 seconds"),
        (60, "1 minute"),
        (300, "5 minutes"),
    ]

    def __init__(self, manager):
        self.settings_mgr = getattr(manager, "settings_manager", None)

        items = []
        for seconds, label in self.TIMEOUT_OPTIONS:
            items.append(
                MenuItem(
                    id=f"t_{seconds}",
                    label=label,
                    value_getter=lambda s=seconds: self._check_mark(s),
                    action=lambda s=seconds: self._set_timeout(s),
                )
            )

        super().__init__(manager, "TIMEOUT", items)

    def _check_mark(self, seconds: int) -> str:
        """Return checkmark if this timeout is selected."""
        if self.settings_mgr and self.settings_mgr.idle_timeout == seconds:
            return "*"
        return ""

    def _set_timeout(self, seconds: int):
        """Set idle timeout."""
        if self.settings_mgr:
            self.settings_mgr.idle_timeout = seconds

        if seconds == 0:
            msg = "Timeout: Never"
        elif seconds < 60:
            msg = f"Timeout: {seconds}s"
        else:
            msg = f"Timeout: {seconds // 60}m"

        toast = ToastScreen(self.manager, msg)
        self.manager.show_overlay(toast, duration=1.5)
        self.manager.pop()
