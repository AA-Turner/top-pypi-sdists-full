"""Macro recording with state machine and multi-source capture."""

from enum import Enum

from PyQt6.QtCore import QElapsedTimer, QObject, pyqtSignal

from .macro_types import InputSource, Macro, MacroStep, MacroStepType


class RecorderState(Enum):
    """Recording state machine states."""

    IDLE = "idle"
    WAITING = "waiting"  # Armed, waiting for first event
    RECORDING = "recording"  # Actively recording
    SAVING = "saving"  # Finalizing macro


class MacroRecorder(QObject):
    """
    Records macro sequences from G13 buttons and/or system keyboard.

    State machine: IDLE -> WAITING -> RECORDING -> SAVING -> IDLE

    Signals:
        state_changed(RecorderState): Emitted when recorder state changes
        step_recorded(MacroStep): Emitted when a step is captured
        recording_complete(Macro): Emitted when recording is finalized
        error_occurred(str): Emitted on errors
    """

    state_changed = pyqtSignal(object)  # RecorderState
    step_recorded = pyqtSignal(object)  # MacroStep
    recording_complete = pyqtSignal(object)  # Macro
    error_occurred = pyqtSignal(str)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._state = RecorderState.IDLE
        self._timer = QElapsedTimer()
        self._steps: list[MacroStep] = []
        self._input_source = InputSource.BOTH
        self._system_listener = None
        self._pressed_keys: set[str] = set()  # Track held keys

    @property
    def state(self) -> RecorderState:
        """Current recorder state."""
        return self._state

    @property
    def is_recording(self) -> bool:
        """True if recording or waiting to record."""
        return self._state in (RecorderState.WAITING, RecorderState.RECORDING)

    @property
    def step_count(self) -> int:
        """Number of steps recorded so far."""
        return len(self._steps)

    @property
    def elapsed_ms(self) -> int:
        """Milliseconds since recording started."""
        if self._timer.isValid():
            return self._timer.elapsed()
        return 0

    def start_recording(self, input_source: InputSource = InputSource.BOTH) -> None:
        """
        Arm the recorder. Recording begins on first event.

        Args:
            input_source: What inputs to capture (G13, system keyboard, or both)
        """
        if self._state != RecorderState.IDLE:
            self.error_occurred.emit("Already recording")
            return

        self._steps = []
        self._pressed_keys = set()
        self._input_source = input_source
        self._state = RecorderState.WAITING

        # Start system keyboard listener if needed
        if input_source in (InputSource.SYSTEM_ONLY, InputSource.BOTH):
            self._start_system_listener()

        self.state_changed.emit(self._state)

    def stop_recording(self) -> Macro | None:
        """
        Stop recording and return the captured macro.

        Returns:
            Macro object with recorded steps, or None if no steps
        """
        if self._state == RecorderState.IDLE:
            return None

        self._stop_system_listener()
        self._state = RecorderState.SAVING
        self.state_changed.emit(self._state)

        # Generate release events for any held keys
        self._generate_release_events()

        if not self._steps:
            self._state = RecorderState.IDLE
            self.state_changed.emit(self._state)
            return None

        # Create macro from recorded steps
        macro = Macro(
            name=f"Recorded Macro ({len(self._steps)} steps)",
            steps=self._steps.copy(),
        )

        self._state = RecorderState.IDLE
        self.state_changed.emit(self._state)
        self.recording_complete.emit(macro)

        return macro

    def cancel(self) -> None:
        """Cancel recording without saving."""
        self._stop_system_listener()
        self._steps = []
        self._pressed_keys = set()
        self._state = RecorderState.IDLE
        self.state_changed.emit(self._state)

    def on_g13_button_event(self, button_id: str, is_pressed: bool) -> None:
        """
        Handle G13 button event during recording.

        Called by ApplicationController when G13 button changes.
        """
        if self._state == RecorderState.IDLE:
            return

        if self._input_source == InputSource.SYSTEM_ONLY:
            return

        # Ignore MR button (it's the record trigger)
        if button_id == "MR":
            return

        # Start timer on first event
        if self._state == RecorderState.WAITING:
            self._timer.start()
            self._state = RecorderState.RECORDING
            self.state_changed.emit(self._state)

        timestamp = self._timer.elapsed()

        step = MacroStep(
            step_type=MacroStepType.G13_BUTTON,
            value=button_id,
            is_press=is_pressed,
            timestamp_ms=timestamp,
        )

        self._steps.append(step)
        self.step_recorded.emit(step)

        # Track pressed buttons
        key_id = f"G13:{button_id}"
        if is_pressed:
            self._pressed_keys.add(key_id)
        else:
            self._pressed_keys.discard(key_id)

    def on_system_key_event(self, key_code: str, is_pressed: bool) -> None:
        """
        Handle system keyboard event during recording.

        Called by system keyboard listener.
        """
        if self._state == RecorderState.IDLE:
            return

        if self._input_source == InputSource.G13_ONLY:
            return

        # Start timer on first event
        if self._state == RecorderState.WAITING:
            self._timer.start()
            self._state = RecorderState.RECORDING
            self.state_changed.emit(self._state)

        timestamp = self._timer.elapsed()
        step_type = MacroStepType.KEY_PRESS if is_pressed else MacroStepType.KEY_RELEASE

        step = MacroStep(
            step_type=step_type,
            value=key_code,
            is_press=is_pressed,
            timestamp_ms=timestamp,
        )

        self._steps.append(step)
        self.step_recorded.emit(step)

        # Track pressed keys
        key_id = f"KEY:{key_code}"
        if is_pressed:
            self._pressed_keys.add(key_id)
        else:
            self._pressed_keys.discard(key_id)

    def add_delay(self, delay_ms: int) -> None:
        """
        Add an explicit delay step.

        Useful for manual macro editing.
        """
        if self._state != RecorderState.RECORDING:
            return

        timestamp = self._timer.elapsed() if self._timer.isValid() else 0

        step = MacroStep(
            step_type=MacroStepType.DELAY,
            value=delay_ms,
            is_press=True,
            timestamp_ms=timestamp,
        )

        self._steps.append(step)
        self.step_recorded.emit(step)

    def _generate_release_events(self) -> None:
        """Generate release events for any held keys at end of recording."""
        if not self._pressed_keys:
            return

        timestamp = self._timer.elapsed() if self._timer.isValid() else 0

        # Release in reverse order (LIFO)
        for key in sorted(self._pressed_keys, reverse=True):
            if key.startswith("G13:"):
                button_id = key[4:]
                step = MacroStep(
                    step_type=MacroStepType.G13_BUTTON,
                    value=button_id,
                    is_press=False,
                    timestamp_ms=timestamp,
                )
            else:
                key_code = key[4:]
                step = MacroStep(
                    step_type=MacroStepType.KEY_RELEASE,
                    value=key_code,
                    is_press=False,
                    timestamp_ms=timestamp,
                )
            self._steps.append(step)

        self._pressed_keys.clear()

    def _start_system_listener(self) -> None:
        """Start listening for system keyboard events."""
        try:
            from pynput import keyboard

            def on_press(key):
                try:
                    if hasattr(key, "char") and key.char:
                        key_code = f"KEY_{key.char.upper()}"
                    elif hasattr(key, "name"):
                        key_code = f"KEY_{key.name.upper()}"
                    else:
                        key_code = str(key)
                    self.on_system_key_event(key_code, True)
                except Exception:
                    pass  # Ignore unknown key types from pynput

            def on_release(key):
                try:
                    if hasattr(key, "char") and key.char:
                        key_code = f"KEY_{key.char.upper()}"
                    elif hasattr(key, "name"):
                        key_code = f"KEY_{key.name.upper()}"
                    else:
                        key_code = str(key)
                    self.on_system_key_event(key_code, False)
                except Exception:
                    pass  # Ignore unknown key types from pynput

            self._system_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            self._system_listener.start()

        except ImportError:
            self.error_occurred.emit("pynput not installed - system keyboard capture disabled")

    def _stop_system_listener(self) -> None:
        """Stop system keyboard listener."""
        if self._system_listener:
            self._system_listener.stop()
            self._system_listener = None
