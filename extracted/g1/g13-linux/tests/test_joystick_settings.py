"""Tests for JoystickSettingsWidget"""

import pytest

from g13_linux.gui.views.joystick_settings import JoystickSettingsWidget


@pytest.fixture
def widget(qtbot):
    """Create a JoystickSettingsWidget"""
    w = JoystickSettingsWidget()
    qtbot.addWidget(w)
    return w


class TestJoystickSettingsWidgetInit:
    """Tests for widget initialization"""

    def test_init(self, widget):
        assert widget.mode_combo is not None
        assert widget.deadzone_spin is not None
        assert widget.sensitivity_slider is not None

    def test_mode_combo_options(self, widget):
        assert widget.mode_combo.count() == 3
        assert widget.mode_combo.itemData(0) == "analog"
        assert widget.mode_combo.itemData(1) == "digital"
        assert widget.mode_combo.itemData(2) == "disabled"

    def test_default_values(self, widget):
        config = widget.get_config()
        assert config["mode"] == "analog"
        assert config["deadzone"] == 20
        assert config["sensitivity"] == 1.0
        assert config["key_up"] == "KEY_UP"

    def test_key_combos_populated(self, widget):
        assert widget.key_up_combo.count() > 0
        assert widget.key_down_combo.count() > 0
        assert widget.key_left_combo.count() > 0
        assert widget.key_right_combo.count() > 0


class TestJoystickSettingsWidgetModeChange:
    """Tests for mode selection changes"""

    def test_mode_change_emits_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.config_changed, timeout=1000):
            widget.mode_combo.setCurrentIndex(1)  # Digital

    def test_mode_change_updates_description(self, widget):
        widget.mode_combo.setCurrentIndex(1)  # Digital
        assert "keyboard" in widget.mode_desc.text().lower()

    def test_mode_change_shows_correct_groups(self, widget):
        # Note: isVisible() requires the widget to be shown.
        # We test isHidden() instead which works without showing.

        # Analog mode
        widget.mode_combo.setCurrentIndex(0)
        assert not widget.analog_group.isHidden()
        assert widget.digital_group.isHidden()

        # Digital mode
        widget.mode_combo.setCurrentIndex(1)
        assert widget.analog_group.isHidden()
        assert not widget.digital_group.isHidden()

        # Disabled mode
        widget.mode_combo.setCurrentIndex(2)
        assert widget.analog_group.isHidden()
        assert widget.digital_group.isHidden()


class TestJoystickSettingsWidgetConfig:
    """Tests for get_config and set_config"""

    def test_get_config(self, widget):
        config = widget.get_config()
        assert "mode" in config
        assert "deadzone" in config
        assert "sensitivity" in config
        assert "key_up" in config
        assert "key_down" in config
        assert "key_left" in config
        assert "key_right" in config
        assert "allow_diagonals" in config

    def test_set_config_mode(self, widget):
        widget.set_config({"mode": "digital"})
        assert widget.mode_combo.currentData() == "digital"

    def test_set_config_deadzone(self, widget):
        widget.set_config({"deadzone": 50})
        assert widget.deadzone_spin.value() == 50

    def test_set_config_sensitivity(self, widget):
        widget.set_config({"sensitivity": 1.5})
        assert widget.sensitivity_slider.value() == 150
        assert widget.sensitivity_label.text() == "150%"

    def test_set_config_keys(self, widget):
        widget.set_config(
            {
                "key_up": "KEY_W",
                "key_down": "KEY_S",
                "key_left": "KEY_A",
                "key_right": "KEY_D",
            }
        )
        assert widget.key_up_combo.currentData() == "KEY_W"
        assert widget.key_down_combo.currentData() == "KEY_S"
        assert widget.key_left_combo.currentData() == "KEY_A"
        assert widget.key_right_combo.currentData() == "KEY_D"

    def test_set_config_diagonals(self, widget):
        widget.set_config({"allow_diagonals": False})
        assert widget.diagonals_combo.currentData() is False

    def test_set_config_invalid_mode(self, widget):
        # Should not crash with invalid mode
        widget.set_config({"mode": "invalid_mode"})
        # Mode combo stays at current value

    def test_set_config_missing_keys(self, widget):
        # Should use defaults for missing keys
        widget.set_config({})
        config = widget.get_config()
        assert config["deadzone"] == 20  # Default


class TestJoystickSettingsWidgetSignals:
    """Tests for signal emission"""

    def test_deadzone_change_emits_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.config_changed, timeout=1000):
            widget.deadzone_spin.setValue(50)

    def test_sensitivity_change_emits_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.config_changed, timeout=1000):
            widget.sensitivity_slider.setValue(150)

    def test_key_combo_change_emits_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.config_changed, timeout=1000):
            widget.key_up_combo.setCurrentIndex(4)  # KEY_W

    def test_diagonals_change_emits_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.config_changed, timeout=1000):
            widget.diagonals_combo.setCurrentIndex(1)  # Cardinal Only


class TestJoystickSettingsWidgetDirection:
    """Tests for direction indicator"""

    def test_update_direction_center(self, widget):
        widget.update_direction("center")
        assert "center" in widget.direction_label.text()
        assert "#333" in widget.direction_label.styleSheet()

    def test_update_direction_active(self, widget):
        widget.update_direction("up")
        assert "up" in widget.direction_label.text()
        assert "#2a5" in widget.direction_label.styleSheet()

    def test_update_direction_diagonal(self, widget):
        widget.update_direction("up+right")
        assert "up+right" in widget.direction_label.text()


class TestJoystickSettingsWidgetRoundTrip:
    """Tests for config round-trip"""

    def test_config_round_trip(self, widget):
        original = {
            "mode": "digital",
            "deadzone": 35,
            "sensitivity": 1.25,
            "key_up": "KEY_W",
            "key_down": "KEY_S",
            "key_left": "KEY_A",
            "key_right": "KEY_D",
            "allow_diagonals": False,
        }
        widget.set_config(original)
        result = widget.get_config()

        assert result["mode"] == original["mode"]
        assert result["deadzone"] == original["deadzone"]
        assert result["sensitivity"] == original["sensitivity"]
        assert result["key_up"] == original["key_up"]
        assert result["key_down"] == original["key_down"]
        assert result["key_left"] == original["key_left"]
        assert result["key_right"] == original["key_right"]
        assert result["allow_diagonals"] == original["allow_diagonals"]
