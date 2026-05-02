"""
Settings Manager

Manages persistent user settings for the G13 daemon.
"""

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


@dataclass
class Settings:
    """
    User settings data structure.

    All settings with their default values.
    """

    # Clock display settings
    clock_format: Literal["12h", "24h"] = "24h"
    clock_show_seconds: bool = True
    clock_show_date: bool = True

    # Idle/screensaver settings
    idle_timeout: int = 30  # seconds, 0 = never

    # Input settings
    stick_sensitivity: Literal["low", "normal", "high"] = "normal"
    stick_deadzone: int = 20  # 0-50

    # Display settings
    lcd_brightness: int = 100  # 0-100 (if supported)
    led_brightness: int = 100  # 0-100

    # Last loaded profile
    last_profile: str = ""


class SettingsManager:
    """
    Manages loading and saving user settings.

    Settings are stored as JSON in the user's config directory.
    """

    DEFAULT_FILENAME = "settings.json"

    def __init__(self, config_dir: str | Path | None = None):
        """
        Initialize settings manager.

        Args:
            config_dir: Directory for config files (default: ~/.config/g13-linux)
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "g13-linux"

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings_path = self.config_dir / self.DEFAULT_FILENAME

        # Current settings (loaded or default)
        self.settings = Settings()

        # Load existing settings if available
        self.load()

    def load(self) -> Settings:
        """
        Load settings from file.

        Returns:
            Loaded settings (or defaults if file doesn't exist)
        """
        if not self.settings_path.exists():
            logger.info("No settings file found, using defaults")
            return self.settings

        try:
            with open(self.settings_path) as f:
                data = json.load(f)

            # Update settings with loaded values (preserving defaults for missing keys)
            for key, value in data.items():
                if hasattr(self.settings, key):
                    setattr(self.settings, key, value)

            logger.info(f"Loaded settings from {self.settings_path}")

        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Could not load settings: {e}")

        return self.settings

    def save(self):
        """Save current settings to file."""
        try:
            with open(self.settings_path, "w") as f:
                json.dump(asdict(self.settings), f, indent=2)
            logger.debug(f"Saved settings to {self.settings_path}")
        except OSError as e:
            logger.error(f"Could not save settings: {e}")

    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.settings = Settings()
        self.save()
        logger.info("Settings reset to defaults")

    # Convenience getters/setters

    def get(self, key: str, default=None):
        """Get a setting value."""
        return getattr(self.settings, key, default)

    def set(self, key: str, value, save: bool = True):
        """
        Set a setting value.

        Args:
            key: Setting name
            value: New value
            save: Whether to save immediately (default True)
        """
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            if save:
                self.save()
        else:
            logger.warning(f"Unknown setting: {key}")

    # Clock settings

    @property
    def clock_format(self) -> str:
        return self.settings.clock_format

    @clock_format.setter
    def clock_format(self, value: str):
        self.settings.clock_format = value
        self.save()

    @property
    def clock_show_seconds(self) -> bool:
        return self.settings.clock_show_seconds

    @clock_show_seconds.setter
    def clock_show_seconds(self, value: bool):
        self.settings.clock_show_seconds = value
        self.save()

    @property
    def clock_show_date(self) -> bool:
        return self.settings.clock_show_date

    @clock_show_date.setter
    def clock_show_date(self, value: bool):
        self.settings.clock_show_date = value
        self.save()

    # Idle settings

    @property
    def idle_timeout(self) -> int:
        return self.settings.idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, value: int):
        self.settings.idle_timeout = value
        self.save()

    # Input settings

    @property
    def stick_sensitivity(self) -> str:
        return self.settings.stick_sensitivity

    @stick_sensitivity.setter
    def stick_sensitivity(self, value: str):
        self.settings.stick_sensitivity = value
        self.save()

    # Brightness settings

    @property
    def led_brightness(self) -> int:
        return self.settings.led_brightness

    @led_brightness.setter
    def led_brightness(self, value: int):
        self.settings.led_brightness = value
        self.save()
