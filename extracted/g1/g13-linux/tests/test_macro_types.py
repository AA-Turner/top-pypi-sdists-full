"""Tests for macro_types module."""

from g13_linux.gui.models.macro_types import (
    InputSource,
    Macro,
    MacroStep,
    MacroStepType,
    PlaybackMode,
)


class TestMacroStepType:
    """Tests for MacroStepType enum."""

    def test_values(self):
        """Test enum values."""
        assert MacroStepType.KEY_PRESS.value == "key_press"
        assert MacroStepType.KEY_RELEASE.value == "key_release"
        assert MacroStepType.G13_BUTTON.value == "g13_button"
        assert MacroStepType.DELAY.value == "delay"


class TestPlaybackMode:
    """Tests for PlaybackMode enum."""

    def test_values(self):
        """Test enum values."""
        assert PlaybackMode.RECORDED.value == "recorded"
        assert PlaybackMode.FIXED.value == "fixed"
        assert PlaybackMode.AS_FAST.value == "as_fast"


class TestInputSource:
    """Tests for InputSource enum."""

    def test_values(self):
        """Test enum values."""
        assert InputSource.G13_ONLY.value == "g13_only"
        assert InputSource.SYSTEM_ONLY.value == "system_only"
        assert InputSource.BOTH.value == "both"


class TestMacroStep:
    """Tests for MacroStep dataclass."""

    def test_creation_with_defaults(self):
        """Test creating step with defaults."""
        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A")
        assert step.step_type == MacroStepType.KEY_PRESS
        assert step.value == "KEY_A"
        assert step.is_press is True
        assert step.timestamp_ms == 0

    def test_creation_with_all_fields(self):
        """Test creating step with all fields."""
        step = MacroStep(
            step_type=MacroStepType.KEY_RELEASE,
            value="KEY_B",
            is_press=False,
            timestamp_ms=1500,
        )
        assert step.step_type == MacroStepType.KEY_RELEASE
        assert step.value == "KEY_B"
        assert step.is_press is False
        assert step.timestamp_ms == 1500

    def test_delay_step(self):
        """Test delay step with int value."""
        step = MacroStep(step_type=MacroStepType.DELAY, value=500)
        assert step.step_type == MacroStepType.DELAY
        assert step.value == 500

    def test_g13_button_step(self):
        """Test G13 button step."""
        step = MacroStep(step_type=MacroStepType.G13_BUTTON, value="G5")
        assert step.step_type == MacroStepType.G13_BUTTON
        assert step.value == "G5"

    def test_to_dict(self):
        """Test serialization to dict."""
        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=100,
        )
        data = step.to_dict()

        assert data["type"] == "key_press"
        assert data["value"] == "KEY_A"
        assert data["is_press"] is True
        assert data["timestamp_ms"] == 100

    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "type": "key_release",
            "value": "KEY_B",
            "is_press": False,
            "timestamp_ms": 200,
        }
        step = MacroStep.from_dict(data)

        assert step.step_type == MacroStepType.KEY_RELEASE
        assert step.value == "KEY_B"
        assert step.is_press is False
        assert step.timestamp_ms == 200

    def test_from_dict_defaults(self):
        """Test deserialization with missing optional fields."""
        data = {"type": "key_press", "value": "KEY_C"}
        step = MacroStep.from_dict(data)

        assert step.is_press is True
        assert step.timestamp_ms == 0

    def test_str_press(self):
        """Test string representation for press."""
        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=1000,
        )
        assert "+KEY_A" in str(step)
        assert "1000ms" in str(step)

    def test_str_release(self):
        """Test string representation for release."""
        step = MacroStep(
            step_type=MacroStepType.KEY_RELEASE,
            value="KEY_A",
            is_press=False,
            timestamp_ms=1100,
        )
        assert "-KEY_A" in str(step)


class TestMacro:
    """Tests for Macro dataclass."""

    def test_creation_with_defaults(self):
        """Test creating macro with defaults."""
        macro = Macro()

        assert macro.id is not None
        assert len(macro.id) > 0
        assert macro.name == "Untitled Macro"
        assert macro.description == ""
        assert macro.steps == []
        assert macro.speed_multiplier == 1.0
        assert macro.repeat_count == 1
        assert macro.repeat_delay_ms == 0
        assert macro.playback_mode == PlaybackMode.RECORDED
        assert macro.fixed_delay_ms == 10
        assert macro.assigned_button is None
        assert macro.global_hotkey is None
        assert macro.created_at != ""

    def test_creation_with_custom_values(self):
        """Test creating macro with custom values."""
        macro = Macro(
            name="Test Macro",
            description="A test",
            speed_multiplier=2.0,
            repeat_count=5,
            playback_mode=PlaybackMode.FIXED,
        )

        assert macro.name == "Test Macro"
        assert macro.description == "A test"
        assert macro.speed_multiplier == 2.0
        assert macro.repeat_count == 5
        assert macro.playback_mode == PlaybackMode.FIXED

    def test_playback_mode_string_conversion(self):
        """Test playback_mode conversion from string."""
        macro = Macro(playback_mode="fixed")
        assert macro.playback_mode == PlaybackMode.FIXED

    def test_add_step(self):
        """Test adding steps to macro."""
        macro = Macro()
        step = macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", timestamp_ms=100)

        assert len(macro.steps) == 1
        assert macro.steps[0] == step
        assert step.step_type == MacroStepType.KEY_PRESS
        assert step.value == "KEY_A"
        assert step.timestamp_ms == 100

    def test_clear_steps(self):
        """Test clearing all steps."""
        macro = Macro()
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A")

        assert len(macro.steps) == 2
        macro.clear_steps()
        assert len(macro.steps) == 0

    def test_duration_ms_empty(self):
        """Test duration with no steps."""
        macro = Macro()
        assert macro.duration_ms == 0

    def test_duration_ms_with_steps(self):
        """Test duration calculation from steps."""
        macro = Macro()
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", timestamp_ms=100)
        macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A", timestamp_ms=250)
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_B", timestamp_ms=500)

        assert macro.duration_ms == 500

    def test_step_count(self):
        """Test step count property."""
        macro = Macro()
        assert macro.step_count == 0

        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        assert macro.step_count == 1

        macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A")
        assert macro.step_count == 2

    def test_to_dict(self):
        """Test serialization to dict."""
        macro = Macro(
            id="test-id",
            name="Test Macro",
            description="Test description",
            speed_multiplier=1.5,
            repeat_count=3,
            playback_mode=PlaybackMode.FIXED,
            assigned_button="G5",
        )
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", timestamp_ms=0)

        data = macro.to_dict()

        assert data["id"] == "test-id"
        assert data["name"] == "Test Macro"
        assert data["description"] == "Test description"
        assert data["speed_multiplier"] == 1.5
        assert data["repeat_count"] == 3
        assert data["playback_mode"] == "fixed"
        assert data["assigned_button"] == "G5"
        assert len(data["steps"]) == 1

    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "id": "macro-123",
            "name": "Loaded Macro",
            "description": "From dict",
            "steps": [
                {"type": "key_press", "value": "KEY_X", "is_press": True, "timestamp_ms": 0},
                {"type": "key_release", "value": "KEY_X", "is_press": False, "timestamp_ms": 100},
            ],
            "speed_multiplier": 0.5,
            "repeat_count": 2,
            "playback_mode": "as_fast",
            "fixed_delay_ms": 20,
            "assigned_button": "G10",
            "global_hotkey": "Ctrl+F1",
        }
        macro = Macro.from_dict(data)

        assert macro.id == "macro-123"
        assert macro.name == "Loaded Macro"
        assert macro.description == "From dict"
        assert len(macro.steps) == 2
        assert macro.steps[0].value == "KEY_X"
        assert macro.speed_multiplier == 0.5
        assert macro.repeat_count == 2
        assert macro.playback_mode == PlaybackMode.AS_FAST
        assert macro.fixed_delay_ms == 20
        assert macro.assigned_button == "G10"
        assert macro.global_hotkey == "Ctrl+F1"

    def test_from_dict_defaults(self):
        """Test deserialization with minimal data."""
        data = {}
        macro = Macro.from_dict(data)

        assert macro.id is not None
        assert macro.name == "Untitled"
        assert macro.steps == []
        assert macro.speed_multiplier == 1.0
        assert macro.playback_mode == PlaybackMode.RECORDED

    def test_roundtrip_serialization(self):
        """Test that to_dict/from_dict roundtrip preserves data."""
        original = Macro(
            name="Roundtrip Test",
            description="Testing serialization",
            speed_multiplier=1.25,
            repeat_count=10,
            playback_mode=PlaybackMode.FIXED,
            fixed_delay_ms=50,
            assigned_button="G22",
        )
        original.add_step(MacroStepType.KEY_PRESS, "KEY_SPACE", timestamp_ms=0)
        original.add_step(MacroStepType.DELAY, 500, timestamp_ms=0)
        original.add_step(MacroStepType.KEY_RELEASE, "KEY_SPACE", timestamp_ms=500)

        data = original.to_dict()
        restored = Macro.from_dict(data)

        assert restored.name == original.name
        assert restored.description == original.description
        assert restored.speed_multiplier == original.speed_multiplier
        assert restored.repeat_count == original.repeat_count
        assert restored.playback_mode == original.playback_mode
        assert restored.fixed_delay_ms == original.fixed_delay_ms
        assert restored.assigned_button == original.assigned_button
        assert len(restored.steps) == len(original.steps)
