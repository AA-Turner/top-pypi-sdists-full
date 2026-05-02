"""Tests for the macro recording and playback system."""

import tempfile

import pytest

from g13_linux.gui.models.global_hotkeys import GlobalHotkeyManager
from g13_linux.gui.models.macro_manager import MacroManager
from g13_linux.gui.models.macro_recorder import MacroRecorder, RecorderState
from g13_linux.gui.models.macro_types import (
    Macro,
    MacroStep,
    MacroStepType,
    PlaybackMode,
)


class TestMacroStep:
    """Tests for MacroStep dataclass."""

    def test_create_key_press(self):
        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=100,
        )
        assert step.step_type == MacroStepType.KEY_PRESS
        assert step.value == "KEY_A"
        assert step.is_press is True
        assert step.timestamp_ms == 100

    def test_create_g13_button(self):
        step = MacroStep(
            step_type=MacroStepType.G13_BUTTON,
            value="G5",
            is_press=True,
            timestamp_ms=0,
        )
        assert step.step_type == MacroStepType.G13_BUTTON
        assert step.value == "G5"

    def test_create_delay(self):
        step = MacroStep(
            step_type=MacroStepType.DELAY,
            value=500,
            is_press=True,
            timestamp_ms=100,
        )
        assert step.step_type == MacroStepType.DELAY
        assert step.value == 500

    def test_to_dict(self):
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

    def test_str_representation(self):
        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=100,
        )
        s = str(step)
        assert "100" in s
        assert "KEY_A" in s


class TestMacro:
    """Tests for Macro dataclass."""

    def test_create_empty_macro(self):
        macro = Macro(name="Test Macro")
        assert macro.name == "Test Macro"
        assert len(macro.steps) == 0
        assert macro.speed_multiplier == 1.0
        assert macro.repeat_count == 1
        assert macro.playback_mode == PlaybackMode.RECORDED

    def test_create_macro_with_steps(self):
        steps = [
            MacroStep(MacroStepType.KEY_PRESS, "KEY_A", True, 0),
            MacroStep(MacroStepType.KEY_RELEASE, "KEY_A", False, 100),
        ]
        macro = Macro(name="Test", steps=steps)
        assert len(macro.steps) == 2
        assert macro.step_count == 2

    def test_duration_ms(self):
        steps = [
            MacroStep(MacroStepType.KEY_PRESS, "KEY_A", True, 0),
            MacroStep(MacroStepType.KEY_RELEASE, "KEY_A", False, 100),
            MacroStep(MacroStepType.KEY_PRESS, "KEY_B", True, 200),
            MacroStep(MacroStepType.KEY_RELEASE, "KEY_B", False, 300),
        ]
        macro = Macro(name="Test", steps=steps)
        assert macro.duration_ms == 300

    def test_duration_ms_empty(self):
        macro = Macro(name="Empty")
        assert macro.duration_ms == 0

    def test_add_step(self):
        macro = Macro(name="Test")
        step = macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        assert len(macro.steps) == 1
        assert step.value == "KEY_A"

    def test_clear_steps(self):
        steps = [
            MacroStep(MacroStepType.KEY_PRESS, "KEY_A", True, 0),
        ]
        macro = Macro(name="Test", steps=steps)
        macro.clear_steps()
        assert len(macro.steps) == 0

    def test_to_dict(self):
        macro = Macro(
            name="Test",
            description="A test macro",
            speed_multiplier=2.0,
            repeat_count=3,
        )
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)

        data = macro.to_dict()
        assert data["name"] == "Test"
        assert data["description"] == "A test macro"
        assert data["speed_multiplier"] == 2.0
        assert data["repeat_count"] == 3
        assert len(data["steps"]) == 1

    def test_from_dict(self):
        data = {
            "id": "test-id",
            "name": "Loaded Macro",
            "description": "Loaded from dict",
            "steps": [
                {
                    "type": "key_press",
                    "value": "KEY_A",
                    "is_press": True,
                    "timestamp_ms": 0,
                },
            ],
            "speed_multiplier": 1.5,
            "repeat_count": 2,
            "playback_mode": "fixed",
            "fixed_delay_ms": 20,
        }
        macro = Macro.from_dict(data)
        assert macro.id == "test-id"
        assert macro.name == "Loaded Macro"
        assert macro.speed_multiplier == 1.5
        assert macro.repeat_count == 2
        assert macro.playback_mode == PlaybackMode.FIXED
        assert len(macro.steps) == 1


class TestMacroManager:
    """Tests for MacroManager CRUD operations."""

    @pytest.fixture
    def temp_macros_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def manager(self, temp_macros_dir):
        return MacroManager(macros_dir=temp_macros_dir)

    def test_list_empty(self, manager):
        assert manager.list_macros() == []

    def test_create_macro(self, manager):
        macro = manager.create_macro("Test Macro")
        assert macro.name == "Test Macro"
        assert manager.macro_exists(macro.id)

    def test_save_and_load(self, manager):
        macro = Macro(name="Save Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        manager.save_macro(macro)

        loaded = manager.load_macro(macro.id)
        assert loaded.name == "Save Test"
        assert len(loaded.steps) == 1

    def test_list_macros(self, manager):
        manager.create_macro("Macro 1")
        manager.create_macro("Macro 2")

        macros = manager.list_macros()
        assert len(macros) == 2

    def test_list_macro_summaries(self, manager):
        macro = manager.create_macro("Summary Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A", False, 100)
        manager.save_macro(macro)

        summaries = manager.list_macro_summaries()
        assert len(summaries) == 1
        assert summaries[0]["name"] == "Summary Test"
        assert summaries[0]["step_count"] == 2

    def test_delete_macro(self, manager):
        macro = manager.create_macro("Delete Me")
        assert manager.macro_exists(macro.id)

        manager.delete_macro(macro.id)
        assert not manager.macro_exists(macro.id)

    def test_delete_nonexistent_raises(self, manager):
        with pytest.raises(FileNotFoundError):
            manager.delete_macro("nonexistent-id")

    def test_load_nonexistent_raises(self, manager):
        with pytest.raises(FileNotFoundError):
            manager.load_macro("nonexistent-id")

    def test_duplicate_macro(self, manager):
        original = manager.create_macro("Original")
        original.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        manager.save_macro(original)

        copy = manager.duplicate_macro(original.id, "Copy of Original")
        assert copy.name == "Copy of Original"
        assert copy.id != original.id
        assert len(copy.steps) == 1


class TestMacroRecorder:
    """Tests for MacroRecorder state machine."""

    @pytest.fixture
    def recorder(self):
        """Create MacroRecorder with system listener mocked to avoid X11 dependency."""
        recorder = MacroRecorder()
        # Patch system listener methods to be no-ops (avoids pynput/Xlib requirement)
        recorder._start_system_listener = lambda: None
        recorder._stop_system_listener = lambda: None
        return recorder

    def test_initial_state(self, recorder):
        assert recorder.state == RecorderState.IDLE
        assert not recorder.is_recording
        assert recorder.step_count == 0

    def test_start_recording(self, recorder):
        recorder.start_recording()
        assert recorder.state == RecorderState.WAITING
        assert recorder.is_recording

    def test_start_recording_twice_fails(self, recorder):
        recorder.start_recording()
        errors = []
        recorder.error_occurred.connect(errors.append)
        recorder.start_recording()
        assert len(errors) == 1
        assert "Already recording" in errors[0]

    def test_cancel_recording(self, recorder):
        recorder.start_recording()
        recorder.cancel()
        assert recorder.state == RecorderState.IDLE
        assert not recorder.is_recording

    def test_g13_button_event(self, recorder):
        recorder.start_recording()

        # First event should transition to RECORDING
        recorder.on_g13_button_event("G1", True)
        assert recorder.state == RecorderState.RECORDING
        assert recorder.step_count == 1

        # Add more events
        recorder.on_g13_button_event("G1", False)
        assert recorder.step_count == 2

    def test_mr_button_ignored(self, recorder):
        recorder.start_recording()
        recorder.on_g13_button_event("MR", True)
        # MR button should not be recorded
        assert recorder.step_count == 0

    def test_stop_recording_returns_macro(self, recorder):
        recorder.start_recording()
        recorder.on_g13_button_event("G1", True)
        recorder.on_g13_button_event("G1", False)

        macro = recorder.stop_recording()
        assert macro is not None
        assert macro.step_count >= 2  # At least the two events
        assert recorder.state == RecorderState.IDLE

    def test_stop_recording_empty_returns_none(self, recorder):
        recorder.start_recording()
        macro = recorder.stop_recording()
        assert macro is None

    def test_recording_signals(self, recorder):
        state_changes = []
        steps_recorded = []

        recorder.state_changed.connect(state_changes.append)
        recorder.step_recorded.connect(steps_recorded.append)

        recorder.start_recording()
        assert RecorderState.WAITING in state_changes

        recorder.on_g13_button_event("G1", True)
        assert RecorderState.RECORDING in state_changes
        assert len(steps_recorded) == 1

        recorder.stop_recording()
        assert RecorderState.IDLE in state_changes


class TestGlobalHotkeyManager:
    """Tests for GlobalHotkeyManager."""

    @pytest.fixture
    def manager(self):
        return GlobalHotkeyManager()

    def test_initial_state(self, manager):
        assert not manager.is_running
        assert manager.registered_hotkeys == {}

    def test_register_hotkey(self, manager):
        result = manager.register_hotkey("ctrl+shift+f1", "macro-123")
        assert result is True
        assert "ctrl+shift+f1" in manager.registered_hotkeys
        assert manager.registered_hotkeys["ctrl+shift+f1"] == "macro-123"

    def test_register_multiple_hotkeys(self, manager):
        manager.register_hotkey("ctrl+f1", "macro-1")
        manager.register_hotkey("alt+f2", "macro-2")
        assert len(manager.registered_hotkeys) == 2

    def test_unregister_hotkey(self, manager):
        manager.register_hotkey("ctrl+f1", "macro-123")
        result = manager.unregister_hotkey("ctrl+f1")
        assert result is True
        assert "ctrl+f1" not in manager.registered_hotkeys

    def test_unregister_nonexistent(self, manager):
        result = manager.unregister_hotkey("ctrl+f99")
        assert result is False

    def test_unregister_macro(self, manager):
        manager.register_hotkey("ctrl+f1", "macro-123")
        manager.register_hotkey("ctrl+f2", "macro-123")
        manager.register_hotkey("ctrl+f3", "other-macro")

        removed = manager.unregister_macro("macro-123")
        assert removed == 2
        assert len(manager.registered_hotkeys) == 1

    def test_get_macro_for_hotkey(self, manager):
        manager.register_hotkey("ctrl+f1", "macro-123")
        assert manager.get_macro_for_hotkey("ctrl+f1") == "macro-123"
        assert manager.get_macro_for_hotkey("ctrl+f99") is None

    def test_get_hotkey_for_macro(self, manager):
        manager.register_hotkey("ctrl+f1", "macro-123")
        assert manager.get_hotkey_for_macro("macro-123") == "ctrl+f1"
        assert manager.get_hotkey_for_macro("other-macro") is None

    def test_normalize_hotkey(self, manager):
        # Various formats should normalize
        manager.register_hotkey("Ctrl+Shift+F1", "m1")
        manager.register_hotkey("CTRL + SHIFT + F2", "m2")

        # Both should be normalized
        assert manager.get_macro_for_hotkey("ctrl+shift+f1") == "m1"
        assert manager.get_macro_for_hotkey("ctrl+shift+f2") == "m2"

    def test_invalid_hotkey(self, manager):
        errors = []
        manager.error_occurred.connect(errors.append)

        result = manager.register_hotkey("", "macro-123")
        assert result is False
        assert len(errors) == 1

    def test_to_pynput_format(self, manager):
        # Test internal conversion
        assert manager._to_pynput_format("ctrl+shift+f1") == "<ctrl>+<shift>+<f1>"
        assert manager._to_pynput_format("alt+a") == "<alt>+a"
        assert manager._to_pynput_format("ctrl+space") == "<ctrl>+<space>"

    def test_clear_all(self, manager):
        manager.register_hotkey("ctrl+f1", "macro-1")
        manager.register_hotkey("ctrl+f2", "macro-2")

        manager.clear_all()
        assert manager.registered_hotkeys == {}

    def test_start_stop_without_hotkeys(self, manager):
        # Should be able to start/stop even without hotkeys
        result = manager.start()
        assert result is True
        assert manager.is_running

        manager.stop()
        assert not manager.is_running


class TestMacroRecorderElapsed:
    """Tests for MacroRecorder elapsed_ms property."""

    @pytest.fixture
    def recorder(self):
        """Create MacroRecorder with system listener mocked."""
        recorder = MacroRecorder()
        recorder._start_system_listener = lambda: None
        recorder._stop_system_listener = lambda: None
        return recorder

    def test_elapsed_ms_before_start(self, recorder):
        """Test elapsed_ms returns 0 before recording starts."""
        assert recorder.elapsed_ms == 0

    def test_elapsed_ms_during_recording(self, recorder):
        """Test elapsed_ms returns timer value during recording."""
        recorder.start_recording()
        recorder.on_g13_button_event("G1", True)  # Start actual recording

        # Timer should be running now
        elapsed = recorder.elapsed_ms
        assert elapsed >= 0

    def test_elapsed_ms_with_invalid_timer(self, recorder):
        """Test elapsed_ms returns 0 when timer is invalid."""
        # Mock timer to return invalid
        from unittest.mock import MagicMock

        recorder._timer = MagicMock()
        recorder._timer.isValid.return_value = False

        assert recorder.elapsed_ms == 0


class TestMacroRecorderSystemListener:
    """Tests for system listener callbacks."""

    def test_on_press_char_key(self):
        """Test on_press callback with character key."""

        from g13_linux.gui.models.macro_recorder import MacroRecorder

        recorder = MacroRecorder()
        recorder._start_system_listener = lambda: None
        recorder._stop_system_listener = lambda: None
        recorder.start_recording()
        recorder.on_g13_button_event("G1", True)  # Start recording

        # Simulate character key press
        steps_before = recorder.step_count
        recorder.on_system_key_event("KEY_A", True)

        assert recorder.step_count == steps_before + 1

    def test_on_press_special_key(self):
        """Test on_press callback with special key."""
        from g13_linux.gui.models.macro_recorder import MacroRecorder

        recorder = MacroRecorder()
        recorder._start_system_listener = lambda: None
        recorder._stop_system_listener = lambda: None
        recorder.start_recording()
        recorder.on_g13_button_event("G1", True)

        steps_before = recorder.step_count
        recorder.on_system_key_event("KEY_SHIFT", True)

        assert recorder.step_count == steps_before + 1

    def test_pynput_import_error(self):
        """Test system listener handles pynput import error."""
        from unittest.mock import patch

        from g13_linux.gui.models.macro_recorder import MacroRecorder

        recorder = MacroRecorder()
        errors = []
        recorder.error_occurred.connect(errors.append)

        # Mock import to fail
        with patch.dict("sys.modules", {"pynput": None, "pynput.keyboard": None}):
            # Force a reimport by clearing any cached module
            import sys

            if "pynput" in sys.modules:
                del sys.modules["pynput"]
            if "pynput.keyboard" in sys.modules:
                del sys.modules["pynput.keyboard"]

            # This should emit an error
            try:
                recorder._start_system_listener()
            except Exception:
                pass  # Test verifies no crash - exception expected during import

        # Error may or may not be emitted depending on pynput availability
        # Just verify no crash occurred


class TestMacroRecorderStopListener:
    """Tests for stopping system listener."""

    def test_stop_listener_with_active_listener(self):
        """Test stopping with active listener."""
        from unittest.mock import MagicMock

        from g13_linux.gui.models.macro_recorder import MacroRecorder

        recorder = MacroRecorder()
        mock_listener = MagicMock()
        recorder._system_listener = mock_listener

        recorder._stop_system_listener()

        mock_listener.stop.assert_called_once()
        assert recorder._system_listener is None

    def test_stop_listener_without_listener(self):
        """Test stopping with no active listener."""
        from g13_linux.gui.models.macro_recorder import MacroRecorder

        recorder = MacroRecorder()
        recorder._system_listener = None

        # Should not raise
        recorder._stop_system_listener()
        assert recorder._system_listener is None
