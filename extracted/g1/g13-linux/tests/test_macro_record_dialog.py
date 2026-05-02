"""Tests for MacroRecordDialog."""

from unittest.mock import MagicMock, patch

import pytest


class TestMacroRecordDialogInit:
    """Tests for dialog initialization."""

    @pytest.fixture
    def mock_recorder(self):
        """Create a mock recorder."""
        recorder = MagicMock()
        recorder.is_recording = False
        recorder.state_changed = MagicMock()
        recorder.step_recorded = MagicMock()
        recorder.recording_complete = MagicMock()
        recorder.error_occurred = MagicMock()
        return recorder

    def test_init_with_recorder(self, qtbot, mock_recorder):
        """Test init with provided recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        dialog = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(dialog)

        assert dialog.recorder is mock_recorder

    def test_init_without_recorder(self, qtbot):
        """Test init creates default recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        with patch("g13_linux.gui.widgets.macro_record_dialog.MacroRecorder") as mock_cls:
            mock_instance = MagicMock()
            mock_instance.state_changed = MagicMock()
            mock_instance.step_recorded = MagicMock()
            mock_instance.recording_complete = MagicMock()
            mock_instance.error_occurred = MagicMock()
            mock_cls.return_value = mock_instance

            dialog = MacroRecordDialog()
            qtbot.addWidget(dialog)

            mock_cls.assert_called_once()
            assert dialog.recorder is mock_instance

    def test_init_recorded_macro_none(self, qtbot, mock_recorder):
        """Test _recorded_macro starts as None."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        dialog = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(dialog)

        assert dialog._recorded_macro is None


class TestMacroRecordDialogUI:
    """Tests for UI initialization."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_window_title(self, dialog):
        """Test dialog title is set."""
        assert dialog.windowTitle() == "Record Macro"

    def test_is_modal(self, dialog):
        """Test dialog is modal."""
        assert dialog.isModal() is True

    def test_has_status_indicator(self, dialog):
        """Test dialog has status indicator."""
        assert dialog.status_indicator is not None
        assert dialog.status_indicator.text() == "IDLE"

    def test_has_checkboxes(self, dialog):
        """Test dialog has input source checkboxes."""
        assert dialog.g13_checkbox is not None
        assert dialog.keyboard_checkbox is not None
        assert dialog.g13_checkbox.isChecked() is True
        assert dialog.keyboard_checkbox.isChecked() is True

    def test_has_steps_list(self, dialog):
        """Test dialog has steps list."""
        assert dialog.steps_list is not None
        assert dialog.steps_list.count() == 0

    def test_has_buttons(self, dialog):
        """Test dialog has control buttons."""
        assert dialog.record_btn is not None
        assert dialog.cancel_btn is not None
        assert dialog.save_btn is not None

    def test_save_btn_disabled_initially(self, dialog):
        """Test save button is disabled initially."""
        assert dialog.save_btn.isEnabled() is False

    def test_has_stats_labels(self, dialog):
        """Test dialog has stats labels."""
        assert dialog.step_count_label is not None
        assert dialog.duration_label is not None
        assert "0" in dialog.step_count_label.text()


class TestMacroRecordDialogInputSource:
    """Tests for input source determination."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_input_source_both(self, dialog):
        """Test both sources selected."""
        from g13_linux.gui.models.macro_types import InputSource

        dialog.g13_checkbox.setChecked(True)
        dialog.keyboard_checkbox.setChecked(True)

        assert dialog._get_input_source() == InputSource.BOTH

    def test_input_source_g13_only(self, dialog):
        """Test G13 only selected."""
        from g13_linux.gui.models.macro_types import InputSource

        dialog.g13_checkbox.setChecked(True)
        dialog.keyboard_checkbox.setChecked(False)

        assert dialog._get_input_source() == InputSource.G13_ONLY

    def test_input_source_system_only(self, dialog):
        """Test system keyboard only selected."""
        from g13_linux.gui.models.macro_types import InputSource

        dialog.g13_checkbox.setChecked(False)
        dialog.keyboard_checkbox.setChecked(True)

        assert dialog._get_input_source() == InputSource.SYSTEM_ONLY

    def test_input_source_none_defaults_g13(self, dialog):
        """Test no sources defaults to G13."""
        from g13_linux.gui.models.macro_types import InputSource

        dialog.g13_checkbox.setChecked(False)
        dialog.keyboard_checkbox.setChecked(False)

        assert dialog._get_input_source() == InputSource.G13_ONLY


class TestMacroRecordDialogRecording:
    """Tests for recording functionality."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_toggle_recording_start(self, dialog):
        """Test toggle starts recording when idle."""
        dialog.recorder.is_recording = False

        dialog._toggle_recording()

        dialog.recorder.start_recording.assert_called_once()

    def test_toggle_recording_stop(self, dialog):
        """Test toggle stops recording when active."""
        dialog.recorder.is_recording = True

        dialog._toggle_recording()

        dialog.recorder.stop_recording.assert_called_once()

    def test_toggle_recording_clears_list(self, dialog):
        """Test starting clears steps list."""
        dialog.steps_list.addItem("test step")
        dialog.recorder.is_recording = False

        dialog._toggle_recording()

        assert dialog.steps_list.count() == 0

    def test_toggle_recording_disables_save(self, dialog):
        """Test starting disables save button."""
        dialog.save_btn.setEnabled(True)
        dialog.recorder.is_recording = False

        dialog._toggle_recording()

        assert dialog.save_btn.isEnabled() is False


class TestMacroRecordDialogStateChanged:
    """Tests for state change handling."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_state_idle(self, dialog):
        """Test IDLE state updates UI."""
        from g13_linux.gui.models.macro_recorder import RecorderState

        dialog._on_state_changed(RecorderState.IDLE)

        assert dialog.status_indicator.text() == "IDLE"
        assert dialog.record_btn.text() == "Start Recording"
        assert dialog.g13_checkbox.isEnabled() is True

    def test_state_waiting(self, dialog):
        """Test WAITING state updates UI."""
        from g13_linux.gui.models.macro_recorder import RecorderState

        dialog._on_state_changed(RecorderState.WAITING)

        assert "ARMED" in dialog.status_indicator.text()
        assert dialog.record_btn.text() == "Stop Recording"
        assert dialog.g13_checkbox.isEnabled() is False

    def test_state_recording(self, dialog):
        """Test RECORDING state updates UI."""
        from g13_linux.gui.models.macro_recorder import RecorderState

        dialog._on_state_changed(RecorderState.RECORDING)

        assert dialog.status_indicator.text() == "RECORDING"
        assert dialog.record_btn.text() == "Stop Recording"

    def test_state_saving(self, dialog):
        """Test SAVING state updates UI."""
        from g13_linux.gui.models.macro_recorder import RecorderState

        dialog._on_state_changed(RecorderState.SAVING)

        assert "SAVING" in dialog.status_indicator.text()


class TestMacroRecordDialogStepRecorded:
    """Tests for step recording."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_step_added_to_list(self, dialog):
        """Test step is added to list."""
        from g13_linux.gui.models.macro_types import MacroStep, MacroStepType

        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=100,
        )

        dialog._on_step_recorded(step)

        assert dialog.steps_list.count() == 1
        assert "KEY_A" in dialog.steps_list.item(0).text()
        assert "100" in dialog.steps_list.item(0).text()

    def test_step_press_indicator(self, dialog):
        """Test press step shows + indicator."""
        from g13_linux.gui.models.macro_types import MacroStep, MacroStepType

        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_B",
            is_press=True,
            timestamp_ms=50,
        )

        dialog._on_step_recorded(step)

        assert "+" in dialog.steps_list.item(0).text()

    def test_step_release_indicator(self, dialog):
        """Test release step shows - indicator."""
        from g13_linux.gui.models.macro_types import MacroStep, MacroStepType

        step = MacroStep(
            step_type=MacroStepType.KEY_RELEASE,
            value="KEY_C",
            is_press=False,
            timestamp_ms=150,
        )

        dialog._on_step_recorded(step)

        assert "-" in dialog.steps_list.item(0).text()

    def test_step_updates_count(self, dialog):
        """Test step updates count label."""
        from g13_linux.gui.models.macro_types import MacroStep, MacroStepType

        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=100,
        )

        dialog._on_step_recorded(step)

        assert "1" in dialog.step_count_label.text()

    def test_step_updates_duration(self, dialog):
        """Test step updates duration label."""
        from g13_linux.gui.models.macro_types import MacroStep, MacroStepType

        step = MacroStep(
            step_type=MacroStepType.KEY_PRESS,
            value="KEY_A",
            is_press=True,
            timestamp_ms=250,
        )

        dialog._on_step_recorded(step)

        assert "250" in dialog.duration_label.text()


class TestMacroRecordDialogComplete:
    """Tests for recording completion."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_recording_complete_stores_macro(self, dialog):
        """Test recording complete stores macro."""
        from g13_linux.gui.models.macro_types import Macro

        macro = Macro(name="Test")

        dialog._on_recording_complete(macro)

        assert dialog._recorded_macro is macro

    def test_recording_complete_enables_save(self, dialog):
        """Test recording complete enables save button."""
        from g13_linux.gui.models.macro_types import Macro

        macro = Macro(name="Test")

        dialog._on_recording_complete(macro)

        assert dialog.save_btn.isEnabled() is True

    def test_recording_complete_updates_stats(self, dialog):
        """Test recording complete updates stats."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType

        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A", False, 100)

        dialog._on_recording_complete(macro)

        assert "2" in dialog.step_count_label.text()
        assert "100" in dialog.duration_label.text()


class TestMacroRecordDialogError:
    """Tests for error handling."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_error_shows_message_box(self, dialog):
        """Test error shows QMessageBox."""
        with patch("PyQt6.QtWidgets.QMessageBox") as mock_box:
            dialog._on_error("Test error message")

            mock_box.warning.assert_called_once()
            args = mock_box.warning.call_args[0]
            assert args[1] == "Recording Error"
            assert args[2] == "Test error message"


class TestMacroRecordDialogSave:
    """Tests for save functionality."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_save_emits_signal(self, dialog, qtbot):
        """Test save emits macro_recorded signal."""
        from g13_linux.gui.models.macro_types import Macro

        macro = Macro(name="Test")
        dialog._recorded_macro = macro

        with qtbot.waitSignal(dialog.macro_recorded, timeout=1000) as blocker:
            dialog._save_macro()

        assert blocker.args[0] is macro

    def test_save_without_macro_does_nothing(self, dialog, qtbot):
        """Test save without macro does nothing."""
        dialog._recorded_macro = None

        received = []
        dialog.macro_recorded.connect(received.append)

        dialog._save_macro()

        assert len(received) == 0


class TestMacroRecordDialogCancel:
    """Tests for cancel functionality."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_cancel_stops_recording(self, dialog):
        """Test cancel stops recording if active."""
        dialog.recorder.is_recording = True

        dialog._on_cancel()

        dialog.recorder.cancel.assert_called_once()

    def test_cancel_when_not_recording(self, dialog):
        """Test cancel without recording doesn't call cancel."""
        dialog.recorder.is_recording = False

        dialog._on_cancel()

        dialog.recorder.cancel.assert_not_called()


class TestMacroRecordDialogClose:
    """Tests for close event handling."""

    @pytest.fixture
    def dialog(self, qtbot):
        """Create dialog with mock recorder."""
        from g13_linux.gui.widgets.macro_record_dialog import MacroRecordDialog

        mock_recorder = MagicMock()
        mock_recorder.is_recording = False
        mock_recorder.state_changed = MagicMock()
        mock_recorder.step_recorded = MagicMock()
        mock_recorder.recording_complete = MagicMock()
        mock_recorder.error_occurred = MagicMock()

        d = MacroRecordDialog(recorder=mock_recorder)
        qtbot.addWidget(d)
        return d

    def test_close_cancels_recording(self, dialog):
        """Test close cancels recording if active."""
        from PyQt6.QtGui import QCloseEvent

        dialog.recorder.is_recording = True

        event = QCloseEvent()
        dialog.closeEvent(event)

        dialog.recorder.cancel.assert_called_once()

    def test_close_when_not_recording(self, dialog):
        """Test close without recording doesn't cancel."""
        from PyQt6.QtGui import QCloseEvent

        dialog.recorder.is_recording = False

        event = QCloseEvent()
        dialog.closeEvent(event)

        dialog.recorder.cancel.assert_not_called()
