"""
Main Menu Screen

Top-level menu providing access to all settings.
"""

from ...lcd.icons import ICON_INFO, ICON_LED, ICON_MACRO, ICON_PROFILE, ICON_SETTINGS
from ..items import MenuItem
from .base_menu import MenuScreen


class MainMenuScreen(MenuScreen):
    """
    Main menu with access to profiles, macros, LED, settings, and info.
    """

    def __init__(self, manager):
        """
        Initialize main menu.

        Args:
            manager: ScreenManager instance
        """
        items = [
            MenuItem(
                id="profiles",
                label="Profiles",
                icon=ICON_PROFILE,
                submenu=lambda: self._create_profiles_screen(),
            ),
            MenuItem(
                id="macros",
                label="Macros",
                icon=ICON_MACRO,
                submenu=lambda: self._create_macros_screen(),
            ),
            MenuItem(
                id="led",
                label="LED Settings",
                icon=ICON_LED,
                submenu=lambda: self._create_led_screen(),
            ),
            MenuItem(
                id="settings",
                label="Settings",
                icon=ICON_SETTINGS,
                submenu=lambda: self._create_settings_screen(),
            ),
            MenuItem(
                id="info",
                label="System Info",
                icon=ICON_INFO,
                submenu=lambda: self._create_info_screen(),
            ),
        ]
        super().__init__(manager, "MENU", items)

    def _create_profiles_screen(self):
        """Create profiles submenu."""
        from .profiles import ProfilesScreen

        return ProfilesScreen(self.manager)

    def _create_macros_screen(self):
        """Create macros submenu."""
        from .macros import MacrosScreen

        return MacrosScreen(self.manager)

    def _create_led_screen(self):
        """Create LED settings submenu."""
        from .led_settings import LEDSettingsScreen

        return LEDSettingsScreen(self.manager)

    def _create_settings_screen(self):
        """Create general settings submenu."""
        from .settings import SettingsScreen

        return SettingsScreen(self.manager)

    def _create_info_screen(self):
        """Create system info screen."""
        from .info import InfoScreen

        return InfoScreen(self.manager)
