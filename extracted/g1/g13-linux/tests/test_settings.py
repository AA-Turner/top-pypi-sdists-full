"""Tests for settings management."""

import json
import sys
from pathlib import Path

# Add src to path without importing through __init__.py
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from g13_linux.settings import Settings, SettingsManager


class TestSettingsDataclass:
    """Tests for Settings dataclass."""

    def test_default_values(self):
        """Settings has expected default values."""
        settings = Settings()
        assert settings.clock_format == "24h"
        assert settings.clock_show_seconds is True
        assert settings.clock_show_date is True
        assert settings.idle_timeout == 30
        assert settings.stick_sensitivity == "normal"
        assert settings.stick_deadzone == 20
        assert settings.lcd_brightness == 100
        assert settings.led_brightness == 100
        assert settings.last_profile == ""

    def test_custom_values(self):
        """Settings accepts custom values."""
        settings = Settings(
            clock_format="12h",
            clock_show_seconds=False,
            idle_timeout=60,
            led_brightness=50,
        )
        assert settings.clock_format == "12h"
        assert settings.clock_show_seconds is False
        assert settings.idle_timeout == 60
        assert settings.led_brightness == 50


class TestSettingsManagerInit:
    """Tests for SettingsManager initialization."""

    def test_creates_config_directory(self, tmp_path):
        """SettingsManager creates config directory if it doesn't exist."""
        config_dir = tmp_path / "new_config"
        assert not config_dir.exists()

        SettingsManager(config_dir)

        assert config_dir.exists()
        assert config_dir.is_dir()

    def test_uses_default_settings(self, tmp_path):
        """SettingsManager starts with default settings when no file exists."""
        manager = SettingsManager(tmp_path)

        assert manager.settings.clock_format == "24h"
        assert manager.settings.led_brightness == 100


class TestSettingsManagerLoadSave:
    """Tests for loading and saving settings."""

    def test_save_creates_file(self, tmp_path):
        """save() creates settings.json file."""
        manager = SettingsManager(tmp_path)
        manager.save()

        assert (tmp_path / "settings.json").exists()

    def test_save_writes_json(self, tmp_path):
        """save() writes valid JSON."""
        manager = SettingsManager(tmp_path)
        manager.settings.clock_format = "12h"
        manager.save()

        with open(tmp_path / "settings.json") as f:
            data = json.load(f)

        assert data["clock_format"] == "12h"

    def test_load_reads_file(self, tmp_path):
        """load() reads settings from file."""
        settings_data = {
            "clock_format": "12h",
            "idle_timeout": 60,
            "led_brightness": 75,
        }
        with open(tmp_path / "settings.json", "w") as f:
            json.dump(settings_data, f)

        manager = SettingsManager(tmp_path)

        assert manager.settings.clock_format == "12h"
        assert manager.settings.idle_timeout == 60
        assert manager.settings.led_brightness == 75

    def test_load_preserves_defaults_for_missing_keys(self, tmp_path):
        """load() preserves defaults for keys not in file."""
        settings_data = {"clock_format": "12h"}
        with open(tmp_path / "settings.json", "w") as f:
            json.dump(settings_data, f)

        manager = SettingsManager(tmp_path)

        assert manager.settings.clock_format == "12h"
        assert manager.settings.led_brightness == 100  # default preserved

    def test_load_handles_corrupt_json(self, tmp_path):
        """load() handles corrupt JSON gracefully."""
        with open(tmp_path / "settings.json", "w") as f:
            f.write("{ invalid json }")

        manager = SettingsManager(tmp_path)

        # Should use defaults
        assert manager.settings.clock_format == "24h"


class TestSettingsManagerResetToDefaults:
    """Tests for reset_to_defaults."""

    def test_reset_restores_defaults(self, tmp_path):
        """reset_to_defaults() restores all defaults."""
        manager = SettingsManager(tmp_path)
        manager.settings.clock_format = "12h"
        manager.settings.led_brightness = 50
        manager.save()

        manager.reset_to_defaults()

        assert manager.settings.clock_format == "24h"
        assert manager.settings.led_brightness == 100

    def test_reset_saves_to_file(self, tmp_path):
        """reset_to_defaults() saves the reset settings."""
        manager = SettingsManager(tmp_path)
        manager.settings.clock_format = "12h"
        manager.save()

        manager.reset_to_defaults()

        # Verify file contains defaults
        with open(tmp_path / "settings.json") as f:
            data = json.load(f)
        assert data["clock_format"] == "24h"


class TestSettingsManagerGetSet:
    """Tests for get() and set() methods."""

    def test_get_existing_key(self, tmp_path):
        """get() returns value for existing key."""
        manager = SettingsManager(tmp_path)
        manager.settings.clock_format = "12h"

        assert manager.get("clock_format") == "12h"

    def test_get_missing_key(self, tmp_path):
        """get() returns default for missing key."""
        manager = SettingsManager(tmp_path)

        assert manager.get("nonexistent", "default") == "default"

    def test_set_existing_key(self, tmp_path):
        """set() updates existing key."""
        manager = SettingsManager(tmp_path)
        manager.set("clock_format", "12h")

        assert manager.settings.clock_format == "12h"

    def test_set_auto_saves(self, tmp_path):
        """set() auto-saves by default."""
        manager = SettingsManager(tmp_path)
        manager.set("led_brightness", 50)

        # Reload and verify
        manager2 = SettingsManager(tmp_path)
        assert manager2.settings.led_brightness == 50

    def test_set_no_save(self, tmp_path):
        """set() with save=False doesn't save."""
        manager = SettingsManager(tmp_path)
        manager.set("led_brightness", 50, save=False)

        # Reload and verify old value
        manager2 = SettingsManager(tmp_path)
        assert manager2.settings.led_brightness == 100  # default


class TestSettingsManagerProperties:
    """Tests for property getters and setters."""

    def test_clock_format_property(self, tmp_path):
        """clock_format property gets and sets."""
        manager = SettingsManager(tmp_path)

        manager.clock_format = "12h"
        assert manager.clock_format == "12h"

    def test_led_brightness_property(self, tmp_path):
        """led_brightness property gets and sets."""
        manager = SettingsManager(tmp_path)

        manager.led_brightness = 75
        assert manager.led_brightness == 75

    def test_property_setters_auto_save(self, tmp_path):
        """Property setters auto-save."""
        manager = SettingsManager(tmp_path)
        manager.idle_timeout = 45

        # Reload and verify
        manager2 = SettingsManager(tmp_path)
        assert manager2.idle_timeout == 45
