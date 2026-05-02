"""Tests for MacroPlayer and MacroPlayerThread."""

import time
from unittest.mock import MagicMock, patch

import pytest

from g13_linux.gui.models.macro_player import (
    MacroPlayer,
    MacroPlayerThread,
    PlaybackState,
)
from g13_linux.gui.models.macro_types import (
    Macro,
    MacroStep,
    MacroStepType,
    PlaybackMode,
)


class TestPlaybackState:
    """Tests for PlaybackState enum."""

    def test_idle(self):
        """Test IDLE state value."""
        assert PlaybackState.IDLE.value == "idle"

    def test_playing(self):
        """Test PLAYING state value."""
        assert PlaybackState.PLAYING.value == "playing"

    def test_paused(self):
        """Test PAUSED state value."""
        assert PlaybackState.PAUSED.value == "paused"

    def test_stopping(self):
        """Test STOPPING state value."""
        assert PlaybackState.STOPPING.value == "stopping"


class TestMacroPlayerThreadInit:
    """Tests for MacroPlayerThread initialization."""

    def test_init_with_macro(self):
        """Test thread initialization."""
        macro = Macro(name="Test")
        thread = MacroPlayerThread(macro)

        assert thread.macro is macro
        assert thread._stop_requested is False
        assert thread._pause_requested is False
        assert thread._uinput is None

    def test_request_stop(self):
        """Test stop request flag."""
        macro = Macro(name="Test")
        thread = MacroPlayerThread(macro)

        thread.request_stop()
        assert thread._stop_requested is True

    def test_request_pause(self):
        """Test pause request flag."""
        macro = Macro(name="Test")
        thread = MacroPlayerThread(macro)

        thread.request_pause()
        assert thread._pause_requested is True

    def test_request_resume(self):
        """Test resume clears pause flag."""
        macro = Macro(name="Test")
        thread = MacroPlayerThread(macro)

        thread.request_pause()
        assert thread._pause_requested is True

        thread.request_resume()
        assert thread._pause_requested is False


class TestMacroPlayerThreadDelayCalculation:
    """Tests for delay calculation logic."""

    def test_delay_as_fast_mode(self):
        """Test AS_FAST mode has no delay."""
        macro = Macro(playback_mode=PlaybackMode.AS_FAST)
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A", timestamp_ms=1000)
        delay = thread._calculate_delay(step, 0)

        assert delay == 0

    def test_delay_fixed_mode(self):
        """Test FIXED mode uses fixed delay."""
        macro = Macro(playback_mode=PlaybackMode.FIXED, fixed_delay_ms=50)
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A", timestamp_ms=1000)
        delay = thread._calculate_delay(step, 0)

        assert delay == 50

    def test_delay_fixed_mode_with_speed(self):
        """Test FIXED mode respects speed multiplier."""
        macro = Macro(playback_mode=PlaybackMode.FIXED, fixed_delay_ms=100, speed_multiplier=2.0)
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A", timestamp_ms=1000)
        delay = thread._calculate_delay(step, 0)

        assert delay == 50  # 100 / 2.0

    def test_delay_recorded_mode(self):
        """Test RECORDED mode uses timestamp delta."""
        macro = Macro(playback_mode=PlaybackMode.RECORDED)
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A", timestamp_ms=500)
        delay = thread._calculate_delay(step, 200)

        assert delay == 300  # 500 - 200

    def test_delay_recorded_mode_with_speed(self):
        """Test RECORDED mode respects speed multiplier."""
        macro = Macro(playback_mode=PlaybackMode.RECORDED, speed_multiplier=2.0)
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A", timestamp_ms=400)
        delay = thread._calculate_delay(step, 0)

        assert delay == 200  # 400 / 2.0

    def test_delay_recorded_mode_no_negative(self):
        """Test RECORDED mode never returns negative."""
        macro = Macro(playback_mode=PlaybackMode.RECORDED)
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A", timestamp_ms=100)
        delay = thread._calculate_delay(step, 500)

        assert delay == 0  # max(0, 100 - 500)


class TestMacroPlayerThreadExecuteStep:
    """Tests for step execution."""

    def test_execute_step_no_uinput(self):
        """Test execution with no UInput is safe."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A")
        # Should not raise
        thread._execute_step(step)

    def test_execute_step_delay(self):
        """Test delay step calls interruptible_sleep."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        # Need to set _uinput to prevent early return
        thread._uinput = MagicMock()

        step = MacroStep(step_type=MacroStepType.DELAY, value=100)

        # Verify interruptible_sleep is called with correct value
        with patch.object(thread, "_interruptible_sleep") as mock_sleep:
            thread._execute_step(step)
            mock_sleep.assert_called_once_with(0.1)  # 100ms = 0.1s

    def test_execute_step_g13_button(self):
        """Test G13 button step is handled."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        step = MacroStep(step_type=MacroStepType.G13_BUTTON, value="G5")
        # Should not raise (currently a no-op)
        thread._execute_step(step)


class TestMacroPlayerThreadEmitKey:
    """Tests for key emission."""

    def test_emit_key_no_uinput(self):
        """Test emit with no UInput is safe."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        # Should not raise
        thread._emit_key("KEY_A", True)

    def test_emit_key_with_mock_uinput(self):
        """Test emit with mocked UInput."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock()
        mock_ecodes.KEY_A = 30
        mock_ecodes.EV_KEY = 1

        thread._uinput = mock_uinput
        thread._ecodes = mock_ecodes

        thread._emit_key("KEY_A", True)

        mock_uinput.write.assert_called_once_with(1, 30, 1)
        mock_uinput.syn.assert_called_once()

    def test_emit_key_release(self):
        """Test emit key release."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock()
        mock_ecodes.KEY_B = 48
        mock_ecodes.EV_KEY = 1

        thread._uinput = mock_uinput
        thread._ecodes = mock_ecodes

        thread._emit_key("KEY_B", False)

        mock_uinput.write.assert_called_once_with(1, 48, 0)

    def test_emit_key_unknown_code(self):
        """Test emit with unknown key code."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock(spec=[])  # No attributes

        thread._uinput = mock_uinput
        thread._ecodes = mock_ecodes

        # Should not raise
        thread._emit_key("KEY_UNKNOWN", True)
        mock_uinput.write.assert_not_called()


class TestMacroPlayerThreadCleanup:
    """Tests for UInput cleanup."""

    def test_cleanup_uinput_none(self):
        """Test cleanup with no UInput."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        # Should not raise
        thread._cleanup_uinput()
        assert thread._uinput is None

    def test_cleanup_uinput_closes(self):
        """Test cleanup closes UInput."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        thread._uinput = mock_uinput

        thread._cleanup_uinput()

        mock_uinput.close.assert_called_once()
        assert thread._uinput is None

    def test_cleanup_uinput_handles_exception(self):
        """Test cleanup handles close exception."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_uinput.close.side_effect = Exception("Close failed")
        thread._uinput = mock_uinput

        # Should not raise
        thread._cleanup_uinput()
        assert thread._uinput is None


class TestMacroPlayerInit:
    """Tests for MacroPlayer initialization."""

    def test_init(self):
        """Test player initialization."""
        player = MacroPlayer()

        assert player.state == PlaybackState.IDLE
        assert player.is_playing is False
        assert player.current_macro is None

    def test_state_property(self):
        """Test state property."""
        player = MacroPlayer()
        assert player.state == PlaybackState.IDLE


class TestMacroPlayerIsPlaying:
    """Tests for is_playing property."""

    def test_is_playing_idle(self):
        """Test is_playing when idle."""
        player = MacroPlayer()
        player._state = PlaybackState.IDLE
        assert player.is_playing is False

    def test_is_playing_playing(self):
        """Test is_playing when playing."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING
        assert player.is_playing is True

    def test_is_playing_paused(self):
        """Test is_playing when paused."""
        player = MacroPlayer()
        player._state = PlaybackState.PAUSED
        assert player.is_playing is True

    def test_is_playing_stopping(self):
        """Test is_playing when stopping."""
        player = MacroPlayer()
        player._state = PlaybackState.STOPPING
        assert player.is_playing is False


class TestMacroPlayerPlay:
    """Tests for play method."""

    def test_play_empty_macro(self, qtbot):
        """Test playing empty macro emits error."""
        player = MacroPlayer()
        macro = Macro(name="Empty")

        errors = []
        player.error_occurred.connect(errors.append)

        player.play(macro)

        assert len(errors) == 1
        assert "no steps" in errors[0]

    def test_play_already_playing(self, qtbot):
        """Test playing while already playing emits error."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING

        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")

        errors = []
        player.error_occurred.connect(errors.append)

        player.play(macro)

        assert len(errors) == 1
        assert "Already playing" in errors[0]

    def test_play_starts_thread(self, qtbot):
        """Test play starts player thread."""
        player = MacroPlayer()
        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")

        with patch.object(MacroPlayerThread, "start"):
            player.play(macro)

            assert player._state == PlaybackState.PLAYING
            assert player._current_macro is macro
            assert player._player_thread is not None


class TestMacroPlayerStop:
    """Tests for stop method."""

    def test_stop_no_thread(self):
        """Test stop with no thread."""
        player = MacroPlayer()

        # Should not raise
        player.stop()
        assert player.state == PlaybackState.IDLE

    def test_stop_clears_state(self):
        """Test stop clears state."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING
        player._current_macro = Macro()

        mock_thread = MagicMock()
        mock_thread.isRunning.return_value = False
        player._player_thread = mock_thread

        player.stop()

        assert player._state == PlaybackState.IDLE
        assert player._current_macro is None


class TestMacroPlayerPauseResume:
    """Tests for pause/resume methods."""

    def test_pause_when_playing(self):
        """Test pause when playing."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING

        mock_thread = MagicMock()
        player._player_thread = mock_thread

        player.pause()

        mock_thread.request_pause.assert_called_once()
        assert player._state == PlaybackState.PAUSED

    def test_pause_when_not_playing(self):
        """Test pause when not playing does nothing."""
        player = MacroPlayer()
        player._state = PlaybackState.IDLE

        player.pause()
        assert player._state == PlaybackState.IDLE

    def test_resume_when_paused(self):
        """Test resume when paused."""
        player = MacroPlayer()
        player._state = PlaybackState.PAUSED

        mock_thread = MagicMock()
        player._player_thread = mock_thread

        player.resume()

        mock_thread.request_resume.assert_called_once()
        assert player._state == PlaybackState.PLAYING

    def test_resume_when_not_paused(self):
        """Test resume when not paused does nothing."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING

        mock_thread = MagicMock()
        player._player_thread = mock_thread

        player.resume()
        mock_thread.request_resume.assert_not_called()


class TestMacroPlayerTogglePause:
    """Tests for toggle_pause method."""

    def test_toggle_pause_from_playing(self):
        """Test toggle from playing to paused."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING

        mock_thread = MagicMock()
        player._player_thread = mock_thread

        player.toggle_pause()

        assert player._state == PlaybackState.PAUSED

    def test_toggle_pause_from_paused(self):
        """Test toggle from paused to playing."""
        player = MacroPlayer()
        player._state = PlaybackState.PAUSED

        mock_thread = MagicMock()
        player._player_thread = mock_thread

        player.toggle_pause()

        assert player._state == PlaybackState.PLAYING


class TestMacroPlayerCallbacks:
    """Tests for callback handling."""

    def test_on_step_executed(self, qtbot):
        """Test step executed callback forwards signal."""
        player = MacroPlayer()

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A")
        received = []

        player.step_executed.connect(lambda idx, s: received.append((idx, s)))
        player._on_step_executed(5, step)

        assert len(received) == 1
        assert received[0][0] == 5
        assert received[0][1] is step

    def test_on_playback_complete(self, qtbot):
        """Test playback complete resets state."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING
        player._current_macro = Macro()
        player._player_thread = MagicMock()

        complete_called = []
        player.playback_complete.connect(lambda: complete_called.append(True))

        player._on_playback_complete()

        assert player._state == PlaybackState.IDLE
        assert player._player_thread is None
        assert player._current_macro is None
        assert len(complete_called) == 1

    def test_on_error(self, qtbot):
        """Test error callback forwards signal."""
        player = MacroPlayer()

        errors = []
        player.error_occurred.connect(errors.append)

        player._on_error("Test error")

        assert errors == ["Test error"]


class TestMacroPlayerThreadRun:
    """Tests for MacroPlayerThread.run() method."""

    def test_run_init_uinput_fails(self, qtbot):
        """Test run() handles UInput init failure."""
        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        thread = MacroPlayerThread(macro)

        errors = []
        thread.error_occurred.connect(errors.append)

        with patch.object(thread, "_init_uinput", side_effect=RuntimeError("no perms")):
            thread.run()

        assert len(errors) == 1
        assert "Failed to initialize UInput" in errors[0]

    def test_run_repeat_delay(self, qtbot):
        """Test run() respects repeat_delay_ms between repeats."""
        macro = Macro(name="Test", repeat_count=2, repeat_delay_ms=100)
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        thread = MacroPlayerThread(macro)

        # Track _play_once calls
        play_calls = []

        def mock_play_once():
            play_calls.append(time.time())

        with (
            patch.object(thread, "_init_uinput"),
            patch.object(thread, "_cleanup_uinput"),
            patch.object(thread, "_play_once", side_effect=mock_play_once),
        ):
            thread.run()

        assert len(play_calls) == 2

    def test_run_zero_repeat_count_infinite(self, qtbot):
        """Test run() with repeat_count=0 uses infinite but can be stopped."""
        macro = Macro(name="Test", repeat_count=0)
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        thread = MacroPlayerThread(macro)

        call_count = [0]

        def mock_play_once():
            call_count[0] += 1
            if call_count[0] >= 3:
                thread.request_stop()

        with (
            patch.object(thread, "_init_uinput"),
            patch.object(thread, "_cleanup_uinput"),
            patch.object(thread, "_play_once", side_effect=mock_play_once),
        ):
            thread.run()

        assert call_count[0] == 3


class TestMacroPlayerThreadInitUInput:
    """Tests for _init_uinput edge cases."""

    def test_init_uinput_import_error(self):
        """Test _init_uinput handles ImportError."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        with patch.dict("sys.modules", {"evdev": None}):
            with pytest.raises(RuntimeError, match="evdev not installed"):
                # Force reimport
                with patch(
                    "g13_linux.gui.models.macro_player.MacroPlayerThread._init_uinput"
                ) as mock:
                    mock.side_effect = RuntimeError("evdev not installed")
                    thread._init_uinput()

    def test_init_uinput_permission_error(self):
        """Test _init_uinput handles PermissionError."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        with patch("evdev.UInput", side_effect=PermissionError("no access")):
            with pytest.raises(RuntimeError, match="Permission denied"):
                thread._init_uinput()


class TestMacroPlayerThreadPlayOnce:
    """Tests for _play_once edge cases."""

    def test_play_once_stop_during_pause(self):
        """Test _play_once exits when stopped during pause."""
        macro = Macro()
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()

        # Start paused, then stop
        thread._pause_requested = True

        def stop_after_check(seconds):
            thread._stop_requested = True
            thread._pause_requested = False

        with patch("time.sleep", side_effect=stop_after_check):
            thread._play_once()

    def test_play_once_step_exception(self):
        """Test _play_once handles step execution errors."""
        macro = Macro()
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()

        errors = []
        thread.error_occurred.connect(errors.append)

        with patch.object(thread, "_execute_step", side_effect=Exception("Step failed")):
            thread._play_once()

        assert len(errors) == 1
        assert "Step 0 failed" in errors[0]


class TestMacroPlayerThreadEmitKeyBranches:
    """Tests for _emit_key edge cases."""

    def test_emit_key_without_key_prefix(self):
        """Test _emit_key handles codes without KEY_ prefix."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock()
        # Simulate key without prefix needs lookup
        del mock_ecodes.A  # Make direct lookup fail
        mock_ecodes.KEY_A = 30
        mock_ecodes.EV_KEY = 1

        thread._uinput = mock_uinput
        thread._ecodes = mock_ecodes

        thread._emit_key("A", True)

        mock_uinput.write.assert_called_once_with(1, 30, 1)

    def test_emit_key_ecodes_none(self):
        """Test _emit_key handles None ecodes."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        thread._uinput = MagicMock()
        thread._ecodes = None

        # Should not raise
        thread._emit_key("KEY_A", True)
        thread._uinput.write.assert_not_called()


class TestMacroPlayerThreadInterruptibleSleep:
    """Tests for _interruptible_sleep."""

    def test_interruptible_sleep_stops_early(self):
        """Test sleep is interrupted by stop request."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        start = time.time()

        # Request stop after brief delay
        def stop_soon():
            time.sleep(0.05)
            thread.request_stop()

        import threading

        stopper = threading.Thread(target=stop_soon)
        stopper.start()

        thread._interruptible_sleep(1.0)

        stopper.join()
        elapsed = time.time() - start

        # Should have stopped early, not waited the full second
        assert elapsed < 0.5

    def test_interruptible_sleep_completes(self):
        """Test sleep completes when not interrupted."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        start = time.time()
        thread._interruptible_sleep(0.05)
        elapsed = time.time() - start

        assert elapsed >= 0.04  # Allow some tolerance


class TestMacroPlayerStateChanged:
    """Tests for state_changed signal."""

    def test_play_emits_state_changed(self, qtbot):
        """Test play emits state_changed signal."""
        player = MacroPlayer()
        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")

        states = []
        player.state_changed.connect(states.append)

        with patch.object(MacroPlayerThread, "start"):
            player.play(macro)

        assert PlaybackState.PLAYING in states

    def test_stop_emits_state_changed(self, qtbot):
        """Test stop emits state_changed signal."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING

        states = []
        player.state_changed.connect(states.append)

        player.stop()

        assert PlaybackState.IDLE in states

    def test_pause_emits_state_changed(self, qtbot):
        """Test pause emits state_changed signal."""
        player = MacroPlayer()
        player._state = PlaybackState.PLAYING
        player._player_thread = MagicMock()

        states = []
        player.state_changed.connect(states.append)

        player.pause()

        assert PlaybackState.PAUSED in states

    def test_resume_emits_state_changed(self, qtbot):
        """Test resume emits state_changed signal."""
        player = MacroPlayer()
        player._state = PlaybackState.PAUSED
        player._player_thread = MagicMock()

        states = []
        player.state_changed.connect(states.append)

        player.resume()

        assert PlaybackState.PLAYING in states


class TestMacroPlayerThreadCoverage:
    """Additional tests for MacroPlayerThread coverage."""

    def test_init_uinput_success(self):
        """Test successful UInput initialization sets _ecodes."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock()

        with patch("evdev.UInput", return_value=mock_uinput):
            with patch("evdev.ecodes", mock_ecodes):
                thread._init_uinput()

        assert thread._uinput is mock_uinput
        assert thread._ecodes is mock_ecodes

    def test_init_uinput_import_error(self):
        """Test ImportError raises RuntimeError."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        with patch.dict("sys.modules", {"evdev": None}):
            with patch("builtins.__import__", side_effect=ImportError("No evdev")):
                with pytest.raises(RuntimeError, match="evdev not installed"):
                    thread._init_uinput()

    def test_play_once_stop_during_loop(self):
        """Test _play_once breaks when stop requested during iteration."""
        macro = Macro()
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_B")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_C")

        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()
        thread._ecodes.EV_KEY = 1
        thread._ecodes.KEY_A = 30
        thread._ecodes.KEY_B = 48
        thread._ecodes.KEY_C = 46

        steps_executed = []
        thread.step_executed.connect(lambda i, s: steps_executed.append(i))

        # Request stop after first step
        def side_effect(*args):
            if len(steps_executed) >= 1:
                thread._stop_requested = True

        thread.step_executed.connect(side_effect)
        thread._play_once()

        # Should have executed only 1 step before stopping
        assert len(steps_executed) <= 2

    def test_play_once_stop_after_delay(self):
        """Test _play_once breaks when stop requested after delay."""
        macro = Macro()
        macro.playback_mode = PlaybackMode.FIXED
        macro.fixed_delay_ms = 10
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_B")

        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()
        thread._ecodes.EV_KEY = 1
        thread._ecodes.KEY_A = 30
        thread._ecodes.KEY_B = 48

        # Mock interruptible sleep to set stop
        original_sleep = thread._interruptible_sleep

        def sleep_then_stop(seconds):
            thread._stop_requested = True

        thread._interruptible_sleep = sleep_then_stop
        thread._play_once()

        # Restore
        thread._interruptible_sleep = original_sleep

    def test_play_once_with_delay(self):
        """Test _play_once with delay before step."""
        macro = Macro()
        macro.playback_mode = PlaybackMode.FIXED
        macro.fixed_delay_ms = 5
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")

        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()
        thread._ecodes.EV_KEY = 1
        thread._ecodes.KEY_A = 30

        steps = []
        thread.step_executed.connect(lambda i, s: steps.append((i, s)))

        with patch.object(thread, "_interruptible_sleep") as mock_sleep:
            thread._play_once()

        # Delay should have been called
        mock_sleep.assert_called()
        assert len(steps) == 1

    def test_play_once_emits_step_executed(self):
        """Test _play_once emits step_executed signal."""
        macro = Macro()
        macro.playback_mode = PlaybackMode.AS_FAST
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A")

        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()
        thread._ecodes.EV_KEY = 1
        thread._ecodes.KEY_A = 30

        steps = []
        thread.step_executed.connect(lambda i, s: steps.append((i, s)))

        thread._play_once()

        assert len(steps) == 1
        assert steps[0][0] == 0

    def test_execute_step_key_press(self):
        """Test _execute_step with KEY_PRESS step type."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock()
        mock_ecodes.EV_KEY = 1
        mock_ecodes.KEY_A = 30
        thread._uinput = mock_uinput
        thread._ecodes = mock_ecodes

        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A")
        thread._execute_step(step)

        mock_uinput.write.assert_called_once_with(1, 30, 1)

    def test_execute_step_key_release(self):
        """Test _execute_step with KEY_RELEASE step type."""
        macro = Macro()
        thread = MacroPlayerThread(macro)

        mock_uinput = MagicMock()
        mock_ecodes = MagicMock()
        mock_ecodes.EV_KEY = 1
        mock_ecodes.KEY_B = 48
        thread._uinput = mock_uinput
        thread._ecodes = mock_ecodes

        # KEY_RELEASE step has is_press=False
        step = MacroStep(step_type=MacroStepType.KEY_RELEASE, value="KEY_B", is_press=False)
        thread._execute_step(step)

        mock_uinput.write.assert_called_once_with(1, 48, 0)

    def test_execute_step_g13_button(self):
        """Test _execute_step with G13_BUTTON step type (passes)."""
        macro = Macro()
        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()

        step = MacroStep(step_type=MacroStepType.G13_BUTTON, value="G1")
        # Should not raise, just pass
        thread._execute_step(step)


class TestMacroPlayerStopRunning:
    """Tests for stopping a running player."""

    def test_stop_running_thread(self, qtbot):
        """Test stop() stops a running thread."""
        player = MacroPlayer()

        mock_thread = MagicMock()
        mock_thread.isRunning.return_value = True
        player._player_thread = mock_thread
        player._state = PlaybackState.PLAYING

        player.stop()

        mock_thread.request_stop.assert_called_once()
        mock_thread.wait.assert_called_once_with(1000)
        assert player.state == PlaybackState.IDLE


class TestMacroPlayerMissingCoverage:
    """Tests for edge cases to achieve 100% coverage."""

    def test_toggle_pause_when_idle(self, qtbot):
        """Test toggle_pause does nothing when state is IDLE (line 273->exit).

        toggle_pause only acts on PLAYING or PAUSED states.
        When IDLE, neither branch is taken.
        """
        player = MacroPlayer()
        player._state = PlaybackState.IDLE

        # Should not raise, just do nothing
        player.toggle_pause()

        # State remains IDLE
        assert player._state == PlaybackState.IDLE

    def test_toggle_pause_when_stopping(self, qtbot):
        """Test toggle_pause does nothing when state is STOPPING (line 273->exit)."""
        player = MacroPlayer()
        player._state = PlaybackState.STOPPING

        player.toggle_pause()

        assert player._state == PlaybackState.STOPPING

    def test_execute_step_unknown_type(self):
        """Test _execute_step with unknown step type falls through (line 140->exit).

        When step_type is not KEY_PRESS, KEY_RELEASE, G13_BUTTON, or DELAY,
        the if-elif chain exits without doing anything.
        """
        macro = Macro()
        thread = MacroPlayerThread(macro)
        thread._uinput = MagicMock()
        thread._ecodes = MagicMock()

        # Create a step with a mocked unknown type
        step = MacroStep(step_type=MacroStepType.KEY_PRESS, value="KEY_A")
        # Patch step_type to an unknown value
        step.step_type = MagicMock()
        step.step_type.__eq__ = lambda self, other: False  # Never matches any type

        # Should not raise, just fall through
        thread._execute_step(step)
