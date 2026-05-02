"""Macro playback with threading and timing control."""

import time
from enum import Enum

from PyQt6.QtCore import QObject, QThread, pyqtSignal

from .macro_types import Macro, MacroStep, MacroStepType, PlaybackMode


class PlaybackState(Enum):
    """Playback state machine states."""

    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPING = "stopping"


class MacroPlayerThread(QThread):
    """Background thread for macro playback with timing."""

    step_executed = pyqtSignal(int, object)  # (step_index, MacroStep)
    playback_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, macro: Macro, parent: QObject | None = None):
        super().__init__(parent)
        self.macro = macro
        self._stop_requested = False
        self._pause_requested = False
        self._uinput = None

    def run(self) -> None:
        """Execute macro with timing."""
        try:
            self._init_uinput()
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize UInput: {e}")
            return

        repeat = 0
        max_repeats = self.macro.repeat_count if self.macro.repeat_count > 0 else float("inf")

        try:
            while repeat < max_repeats and not self._stop_requested:
                self._play_once()
                repeat += 1

                if repeat < max_repeats and self.macro.repeat_delay_ms > 0:
                    delay = self.macro.repeat_delay_ms / self.macro.speed_multiplier
                    self._interruptible_sleep(delay / 1000.0)
        finally:
            self._cleanup_uinput()

        self.playback_complete.emit()

    def _init_uinput(self) -> None:
        """Initialize UInput for key injection."""
        try:
            from evdev import UInput
            from evdev import ecodes as e

            # Create UInput with common keys
            self._uinput = UInput()
            self._ecodes = e
        except ImportError:
            raise RuntimeError("evdev not installed")
        except PermissionError:
            raise RuntimeError("Permission denied - need root or uinput access")

    def _cleanup_uinput(self) -> None:
        """Cleanup UInput."""
        if self._uinput:
            try:
                self._uinput.close()
            except Exception:
                pass  # Best-effort cleanup, device may already be closed
            self._uinput = None

    def _play_once(self) -> None:
        """Play macro steps once."""
        last_timestamp = 0

        for idx, step in enumerate(self.macro.steps):
            if self._stop_requested:
                break

            # Handle pause
            while self._pause_requested and not self._stop_requested:
                time.sleep(0.01)

            if self._stop_requested:
                break

            # Calculate delay based on playback mode
            delay_ms = self._calculate_delay(step, last_timestamp)
            if delay_ms > 0:
                self._interruptible_sleep(delay_ms / 1000.0)

            if self._stop_requested:
                break

            # Execute step
            try:
                self._execute_step(step)
                self.step_executed.emit(idx, step)
            except Exception as ex:
                self.error_occurred.emit(f"Step {idx} failed: {ex}")

            last_timestamp = step.timestamp_ms

    def _calculate_delay(self, step: MacroStep, last_timestamp: int) -> float:
        """Calculate delay before executing step."""
        if self.macro.playback_mode == PlaybackMode.AS_FAST:
            return 0
        elif self.macro.playback_mode == PlaybackMode.FIXED:
            return self.macro.fixed_delay_ms / self.macro.speed_multiplier
        else:  # RECORDED
            delay = step.timestamp_ms - last_timestamp
            return max(0, delay / self.macro.speed_multiplier)

    def _execute_step(self, step: MacroStep) -> None:
        """Execute a single macro step."""
        if self._uinput is None:
            return

        if step.step_type in (MacroStepType.KEY_PRESS, MacroStepType.KEY_RELEASE):
            self._emit_key(step.value, step.is_press)

        elif step.step_type == MacroStepType.G13_BUTTON:
            # G13 button events - these would need profile mapping
            # For now, we just emit a placeholder or skip
            # The ApplicationController should handle this by looking up
            # the button's mapped key in the current profile
            pass

        elif step.step_type == MacroStepType.DELAY:
            self._interruptible_sleep(step.value / 1000.0)

    def _emit_key(self, key_code: str, is_press: bool) -> None:
        """Emit a key press/release via UInput."""
        if self._uinput is None or self._ecodes is None:
            return

        # Convert key code string to evdev keycode
        evdev_code = getattr(self._ecodes, key_code, None)
        if evdev_code is None:
            # Try without KEY_ prefix
            if key_code.startswith("KEY_"):
                evdev_code = getattr(self._ecodes, key_code, None)
            else:
                evdev_code = getattr(self._ecodes, f"KEY_{key_code}", None)

        if evdev_code is not None:
            state = 1 if is_press else 0
            self._uinput.write(self._ecodes.EV_KEY, evdev_code, state)
            self._uinput.syn()

    def _interruptible_sleep(self, seconds: float) -> None:
        """Sleep that can be interrupted by stop request."""
        end_time = time.time() + seconds
        while time.time() < end_time and not self._stop_requested:
            time.sleep(min(0.01, end_time - time.time()))

    def request_stop(self) -> None:
        """Request playback stop."""
        self._stop_requested = True

    def request_pause(self) -> None:
        """Request playback pause."""
        self._pause_requested = True

    def request_resume(self) -> None:
        """Request playback resume."""
        self._pause_requested = False


class MacroPlayer(QObject):
    """
    Plays back recorded macros with configurable timing.

    Signals:
        state_changed(PlaybackState): Playback state changes
        step_executed(int, MacroStep): Step executed with index
        playback_complete(): Macro finished
        error_occurred(str): Error during playback
    """

    state_changed = pyqtSignal(object)  # PlaybackState
    step_executed = pyqtSignal(int, object)  # (index, MacroStep)
    playback_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._state = PlaybackState.IDLE
        self._player_thread: MacroPlayerThread | None = None
        self._current_macro: Macro | None = None

    @property
    def state(self) -> PlaybackState:
        """Current playback state."""
        return self._state

    @property
    def is_playing(self) -> bool:
        """True if playing or paused."""
        return self._state in (PlaybackState.PLAYING, PlaybackState.PAUSED)

    @property
    def current_macro(self) -> Macro | None:
        """Currently playing macro."""
        return self._current_macro

    def play(self, macro: Macro) -> None:
        """
        Start playing a macro.

        Args:
            macro: Macro to play
        """
        if self._state != PlaybackState.IDLE:
            self.error_occurred.emit("Already playing")
            return

        if not macro.steps:
            self.error_occurred.emit("Macro has no steps")
            return

        self._current_macro = macro

        # Create and start player thread
        self._player_thread = MacroPlayerThread(macro, self)
        self._player_thread.step_executed.connect(self._on_step_executed)
        self._player_thread.playback_complete.connect(self._on_playback_complete)
        self._player_thread.error_occurred.connect(self._on_error)

        self._state = PlaybackState.PLAYING
        self.state_changed.emit(self._state)
        self._player_thread.start()

    def stop(self) -> None:
        """Stop playback immediately."""
        if self._player_thread and self._player_thread.isRunning():
            self._player_thread.request_stop()
            self._player_thread.wait(1000)

        self._state = PlaybackState.IDLE
        self._current_macro = None
        self.state_changed.emit(self._state)

    def pause(self) -> None:
        """Pause playback."""
        if self._state == PlaybackState.PLAYING and self._player_thread:
            self._player_thread.request_pause()
            self._state = PlaybackState.PAUSED
            self.state_changed.emit(self._state)

    def resume(self) -> None:
        """Resume paused playback."""
        if self._state == PlaybackState.PAUSED and self._player_thread:
            self._player_thread.request_resume()
            self._state = PlaybackState.PLAYING
            self.state_changed.emit(self._state)

    def toggle_pause(self) -> None:
        """Toggle between playing and paused."""
        if self._state == PlaybackState.PLAYING:
            self.pause()
        elif self._state == PlaybackState.PAUSED:
            self.resume()

    def _on_step_executed(self, index: int, step: MacroStep) -> None:
        """Forward step executed signal."""
        self.step_executed.emit(index, step)

    def _on_playback_complete(self) -> None:
        """Handle playback completion."""
        self._state = PlaybackState.IDLE
        self._player_thread = None
        self._current_macro = None
        self.state_changed.emit(self._state)
        self.playback_complete.emit()

    def _on_error(self, message: str) -> None:
        """Handle error from player thread."""
        self.error_occurred.emit(message)
