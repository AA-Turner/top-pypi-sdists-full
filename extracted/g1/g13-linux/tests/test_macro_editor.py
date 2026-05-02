"""Tests for MacroEditorWidget."""

from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_dependencies():
    """Mock external dependencies for MacroEditorWidget."""
    with (
        patch("g13_linux.gui.views.macro_editor.MacroManager") as mock_mgr,
        patch("g13_linux.gui.views.macro_editor.MacroRecorder") as mock_rec,
        patch("g13_linux.gui.views.macro_editor.MacroPlayer") as mock_player,
    ):
        mock_mgr_instance = MagicMock()
        mock_mgr_instance.list_macros.return_value = []
        mock_mgr_instance.list_macro_summaries.return_value = []
        mock_mgr.return_value = mock_mgr_instance

        mock_rec_instance = MagicMock()
        mock_rec_instance.state_changed = MagicMock()
        mock_rec_instance.recording_complete = MagicMock()
        mock_rec.return_value = mock_rec_instance

        mock_player_instance = MagicMock()
        mock_player_instance.playback_started = MagicMock()
        mock_player_instance.playback_complete = MagicMock()
        mock_player_instance.playback_error = MagicMock()
        mock_player.return_value = mock_player_instance

        yield {
            "manager_cls": mock_mgr,
            "manager": mock_mgr_instance,
            "recorder_cls": mock_rec,
            "recorder": mock_rec_instance,
            "player_cls": mock_player,
            "player": mock_player_instance,
        }


class TestMacroListItem:
    """Tests for MacroListItem."""

    def test_create_item(self, qapp):
        """Test creating a MacroListItem."""
        from g13_linux.gui.views.macro_editor import MacroListItem

        item = MacroListItem("macro-123", "Test Macro", 5)

        assert item.macro_id == "macro-123"
        assert "Test Macro" in item.text()
        assert "5 steps" in item.text()


class TestMacroEditorWidget:
    """Tests for MacroEditorWidget."""

    def test_init(self, qapp, mock_dependencies):
        """Test MacroEditorWidget initialization."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.macro_manager is not None
        assert widget.macro_recorder is not None
        assert widget.macro_player is not None
        assert widget._current_macro is None

    def test_has_signals(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has required signals."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert hasattr(widget, "macro_assigned")
        assert hasattr(widget, "macro_saved")

    def test_has_ui_elements(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has UI elements."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.macro_list is not None
        assert widget.name_edit is not None
        assert widget.description_edit is not None
        assert widget.hotkey_edit is not None
        assert widget.steps_list is not None

    def test_has_buttons(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has buttons."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.new_btn is not None
        assert widget.record_btn is not None
        assert widget.delete_btn is not None

    def test_delete_btn_disabled_initially(self, qapp, mock_dependencies):
        """Test delete button is disabled when no macro selected."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert widget.delete_btn.isEnabled() is False

    def test_refresh_macro_list(self, qapp, mock_dependencies):
        """Test refresh_macro_list updates list."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        # Set up mock to return summaries before widget creation
        mock_dependencies["manager"].list_macro_summaries.return_value = [
            {"id": "macro-1", "name": "Test", "step_count": 3}
        ]

        widget = MacroEditorWidget()

        assert widget.macro_list.count() == 1

    def test_create_new_macro(self, qapp, mock_dependencies):
        """Test creating a new macro."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        # Set up mock to return a new macro
        new_macro = MagicMock(spec=Macro)
        new_macro.id = "new-macro"
        new_macro.name = "New Macro"
        mock_dependencies["manager"].create_macro.return_value = new_macro
        mock_dependencies["manager"].list_macro_summaries.return_value = []

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("New Macro", True)
            widget._create_new_macro()

        # Macro should be created
        mock_dependencies["manager"].create_macro.assert_called_once_with("New Macro")

    def test_create_new_macro_cancelled(self, qapp, mock_dependencies):
        """Test cancelling new macro creation."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("", False)
            widget._create_new_macro()

        # Macro should not be saved
        mock_dependencies["manager"].save_macro.assert_not_called()

    def test_delete_macro_no_selection(self, qapp, mock_dependencies):
        """Test delete macro with no selection."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        # Should not raise
        widget._delete_macro()

        mock_dependencies["manager"].delete_macro.assert_not_called()

    def test_on_macro_selected_none(self, qapp, mock_dependencies):
        """Test selecting no macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        widget._on_macro_selected(None, None)

        assert widget._current_macro is None
        assert widget.delete_btn.isEnabled() is False

    def test_on_property_changed_no_macro(self, qapp, mock_dependencies):
        """Test property change with no current macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._on_property_changed()


class TestMacroEditorPlayback:
    """Tests for playback controls."""

    def test_has_playback_controls(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has playback controls."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert hasattr(widget, "play_btn")
        assert hasattr(widget, "stop_btn")

    def test_has_playback_settings(self, qapp, mock_dependencies):
        """Test MacroEditorWidget has playback settings."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        assert hasattr(widget, "speed_spin")
        assert hasattr(widget, "repeat_spin")
        assert hasattr(widget, "playback_mode_combo")


class TestMacroEditorSteps:
    """Tests for step management."""

    def test_insert_delay_no_macro(self, qapp, mock_dependencies):
        """Test insert delay with no current macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._insert_delay()

    def test_delete_step_no_selection(self, qapp, mock_dependencies):
        """Test delete step with no selection."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        # Should not raise
        widget._delete_step()


class TestMacroEditorRecordDialog:
    """Tests for record dialog integration."""

    def test_open_record_dialog(self, qapp, mock_dependencies):
        """Test opening record dialog."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.MacroRecordDialog") as mock_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = False
            mock_dialog.return_value = mock_dialog_instance

            widget._open_record_dialog()

            mock_dialog.assert_called_once()


class TestMacroEditorMacroSelection:
    """Tests for macro selection handling."""

    def test_on_macro_selected_loads_macro(self, qapp, mock_dependencies):
        """Test selecting macro loads it into editor."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget, MacroListItem

        mock_macro = MagicMock(spec=Macro)
        mock_macro.name = "Test Macro"
        mock_macro.description = "Desc"
        mock_macro.global_hotkey = ""
        mock_macro.speed_multiplier = 1.0
        mock_macro.repeat_count = 1
        mock_macro.repeat_delay_ms = 0
        mock_macro.fixed_delay_ms = 10
        mock_macro.playback_mode = MagicMock()
        mock_macro.steps = []

        mock_dependencies["manager"].load_macro.return_value = mock_macro

        widget = MacroEditorWidget()
        item = MacroListItem("test-id", "Test", 0)

        widget._on_macro_selected(item, None)

        assert widget._current_macro is mock_macro
        assert widget.delete_btn.isEnabled() is True

    def test_on_macro_selected_none_clears(self, qapp, mock_dependencies):
        """Test selecting None clears editor."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = MagicMock()

        widget._on_macro_selected(None, None)

        assert widget._current_macro is None
        assert widget.delete_btn.isEnabled() is False


class TestMacroEditorRefresh:
    """Tests for refresh functionality."""

    def test_refresh_steps_list(self, qapp, mock_dependencies):
        """Test refreshing steps list."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        mock_macro = Macro(name="Test")
        mock_macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        mock_macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A", False, 100)
        widget._current_macro = mock_macro

        widget._refresh_steps_list()

        assert widget.steps_list.count() == 2

    def test_refresh_steps_list_no_macro(self, qapp, mock_dependencies):
        """Test refreshing steps list with no macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None
        widget.steps_list.addItem("old item")

        widget._refresh_steps_list()

        assert widget.steps_list.count() == 0

    def test_refresh_macro_list_public(self, qapp, mock_dependencies):
        """Test public refresh_macro_list method."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        mock_dependencies["manager"].list_macro_summaries.return_value = [
            {"id": "m1", "name": "Macro1", "step_count": 5}
        ]

        widget = MacroEditorWidget()
        widget.refresh_macro_list()

        assert widget.macro_list.count() == 1


class TestMacroEditorSetEnabled:
    """Tests for editor enable/disable."""

    def test_set_editor_enabled_true(self, qapp, mock_dependencies):
        """Test enabling editor controls."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Test")
        widget._current_macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)

        widget._set_editor_enabled(True)

        assert widget.name_edit.isEnabled() is True
        assert widget.description_edit.isEnabled() is True
        assert widget.speed_spin.isEnabled() is True

    def test_set_editor_enabled_false(self, qapp, mock_dependencies):
        """Test disabling editor controls."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        widget._set_editor_enabled(False)

        assert widget.name_edit.isEnabled() is False
        assert widget.play_btn.isEnabled() is False


class TestMacroEditorApplyChanges:
    """Tests for applying changes."""

    def test_apply_changes_updates_macro(self, qapp, mock_dependencies):
        """Test apply changes updates macro properties."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Original")

        widget.name_edit.setText("Updated Name")
        widget.description_edit.setText("New desc")
        widget.speed_spin.setValue(2.5)
        widget.repeat_spin.setValue(3)

        widget._apply_changes()

        assert widget._current_macro.name == "Updated Name"
        assert widget._current_macro.description == "New desc"
        assert widget._current_macro.speed_multiplier == 2.5
        assert widget._current_macro.repeat_count == 3

    def test_apply_changes_no_macro(self, qapp, mock_dependencies):
        """Test apply changes with no macro does nothing."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._apply_changes()


class TestMacroEditorDeleteMacro:
    """Tests for delete macro."""

    def test_delete_macro_no_current(self, qapp, mock_dependencies):
        """Test delete with no current macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._delete_macro()

        mock_dependencies["manager"].delete_macro.assert_not_called()


class TestMacroEditorInsertDelay:
    """Tests for insert delay."""

    def test_insert_delay_no_macro(self, qapp, mock_dependencies):
        """Test insert delay with no macro."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._insert_delay()


class TestMacroEditorDeleteStep:
    """Tests for delete step."""

    def test_delete_step_removes_step(self, qapp, mock_dependencies):
        """Test delete step removes from list."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Test")
        widget._current_macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        widget._current_macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A", False, 100)
        widget._refresh_steps_list()
        widget.steps_list.setCurrentRow(0)

        widget._delete_step()

        assert widget._current_macro.step_count == 1

    def test_delete_step_no_selection(self, qapp, mock_dependencies):
        """Test delete step with no selection."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Test")
        widget._current_macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)

        # No selection
        widget.steps_list.setCurrentRow(-1)

        widget._delete_step()

        # Should not delete
        assert widget._current_macro.step_count == 1


class TestMacroEditorPlaybackActions:
    """Tests for playback control actions."""

    def test_play_macro(self, qapp, mock_dependencies):
        """Test play macro calls player."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Test")

        widget._play_macro()

        mock_dependencies["player"].play.assert_called_once()

    def test_play_macro_no_current(self, qapp, mock_dependencies):
        """Test play with no macro does nothing."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        widget._play_macro()

        mock_dependencies["player"].play.assert_not_called()

    def test_stop_macro(self, qapp, mock_dependencies):
        """Test stop macro calls player."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        widget._stop_macro()

        mock_dependencies["player"].stop.assert_called_once()


class TestMacroEditorSaveMacro:
    """Tests for save macro."""

    def test_save_macro(self, qapp, mock_dependencies):
        """Test save macro calls manager."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Test")

        widget._save_macro()

        mock_dependencies["manager"].save_macro.assert_called()

    def test_save_macro_emits_signal(self, qapp, mock_dependencies, qtbot):
        """Test save macro emits signal."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = Macro(name="Test")

        with qtbot.waitSignal(widget.macro_saved, timeout=1000):
            widget._save_macro()

    def test_save_macro_no_current(self, qapp, mock_dependencies):
        """Test save with no macro does nothing."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        widget._save_macro()

        mock_dependencies["manager"].save_macro.assert_not_called()


class TestMacroEditorPlaybackState:
    """Tests for playback state changes."""

    def test_on_playback_state_playing(self, qapp, mock_dependencies):
        """Test UI updates for PLAYING state."""
        from g13_linux.gui.models.macro_player import PlaybackState
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        widget._on_playback_state_changed(PlaybackState.PLAYING)

        assert widget.stop_btn.isEnabled() is True
        assert "Pause" in widget.play_btn.text()

    def test_on_playback_state_idle(self, qapp, mock_dependencies):
        """Test UI updates for IDLE state."""
        from g13_linux.gui.models.macro_player import PlaybackState
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        widget._on_playback_state_changed(PlaybackState.IDLE)

        assert widget.stop_btn.isEnabled() is False
        assert "Play" in widget.play_btn.text()

    def test_on_playback_complete(self, qapp, mock_dependencies):
        """Test playback complete resets UI."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget.stop_btn.setEnabled(True)

        widget._on_playback_complete()

        assert widget.stop_btn.isEnabled() is False
        assert widget.play_btn.text() == "Play"


class TestMacroEditorError:
    """Tests for error handling."""

    def test_on_error_shows_messagebox(self, qapp, mock_dependencies):
        """Test error shows message box."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.QMessageBox") as mock_box:
            widget._on_error("Test error")

            mock_box.warning.assert_called_once()


class TestMacroEditorLoadToEditor:
    """Tests for loading macro to editor."""

    def test_load_macro_to_editor(self, qapp, mock_dependencies):
        """Test loading macro populates fields."""
        from g13_linux.gui.models.macro_types import Macro, PlaybackMode
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(
            name="Test",
            description="Test desc",
            speed_multiplier=1.5,
            repeat_count=2,
            playback_mode=PlaybackMode.FIXED,
        )
        widget._current_macro = macro

        widget._load_macro_to_editor()

        assert widget.name_edit.text() == "Test"
        assert widget.description_edit.text() == "Test desc"
        assert widget.speed_spin.value() == 1.5
        assert widget.repeat_spin.value() == 2

    def test_load_macro_to_editor_no_macro(self, qapp, mock_dependencies):
        """Test loading with no macro does nothing."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        widget._current_macro = None

        # Should not raise
        widget._load_macro_to_editor()


class TestMacroEditorOnMacroRecorded:
    """Tests for macro recorded callback."""

    def test_on_macro_recorded_saves(self, qapp, mock_dependencies):
        """Test recorded macro is saved."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="Recorded")

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("New Name", True)

            widget._on_macro_recorded(macro)

            mock_dependencies["manager"].save_macro.assert_called_once()
            assert macro.name == "New Name"

    def test_on_macro_recorded_cancelled(self, qapp, mock_dependencies):
        """Test cancelled recording doesn't save."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="Recorded")

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("", False)

            widget._on_macro_recorded(macro)

            mock_dependencies["manager"].save_macro.assert_not_called()


class TestMacroEditorMacroNotFound:
    """Tests for macro not found error handling."""

    def test_on_macro_selected_file_not_found(self, qapp, mock_dependencies):
        """Test macro selection handles FileNotFoundError."""
        from g13_linux.gui.views.macro_editor import MacroEditorWidget, MacroListItem

        mock_dependencies["manager"].load_macro.side_effect = FileNotFoundError()

        widget = MacroEditorWidget()
        item = MacroListItem("test-id", "Test Macro", 5)
        widget.macro_list.addItem(item)

        with patch("g13_linux.gui.views.macro_editor.QMessageBox") as mock_box:
            widget._on_macro_selected(item, None)

            mock_box.warning.assert_called_once()
            assert "not found" in mock_box.warning.call_args[0][2].lower()


class TestMacroEditorCreateNewMacroSelection:
    """Tests for new macro creation and selection."""

    def test_create_new_macro_selects_new_item(self, qapp, mock_dependencies):
        """Test creating macro selects it in list."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget, MacroListItem

        new_macro = Macro(name="New Test")
        mock_dependencies["manager"].create_macro.return_value = new_macro
        mock_dependencies["manager"].load_macro.return_value = new_macro
        # list_macro_summaries returns list of dicts with id, name, step_count
        mock_dependencies["manager"].list_macro_summaries.return_value = [
            {"id": "other-id", "name": "Other", "step_count": 3},
            {"id": new_macro.id, "name": "New Test", "step_count": 0},
        ]

        widget = MacroEditorWidget()

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getText.return_value = ("New Test", True)

            widget._create_new_macro()

            # Check the new macro is selected
            current = widget.macro_list.currentItem()
            assert current is not None
            assert isinstance(current, MacroListItem)
            assert current.macro_id == new_macro.id


class TestMacroEditorDeleteMacroWithConfirmation:
    """Tests for delete macro with confirmation dialog."""

    def test_delete_macro_confirmed(self, qapp, mock_dependencies):
        """Test delete macro when user confirms."""
        from PyQt6.QtWidgets import QMessageBox

        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="ToDelete")
        widget._current_macro = macro
        widget._set_editor_enabled(True)

        with patch("g13_linux.gui.views.macro_editor.QMessageBox") as mock_box:
            mock_box.StandardButton = QMessageBox.StandardButton
            mock_box.question.return_value = QMessageBox.StandardButton.Yes

            widget._delete_macro()

            mock_dependencies["manager"].delete_macro.assert_called_once_with(macro.id)
            assert widget._current_macro is None

    def test_delete_macro_declined(self, qapp, mock_dependencies):
        """Test delete macro when user declines."""
        from PyQt6.QtWidgets import QMessageBox

        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="ToKeep")
        widget._current_macro = macro

        with patch("g13_linux.gui.views.macro_editor.QMessageBox") as mock_box:
            mock_box.StandardButton = QMessageBox.StandardButton
            mock_box.question.return_value = QMessageBox.StandardButton.No

            widget._delete_macro()

            mock_dependencies["manager"].delete_macro.assert_not_called()
            assert widget._current_macro is macro

    def test_delete_macro_handles_file_not_found(self, qapp, mock_dependencies):
        """Test delete macro handles FileNotFoundError silently."""
        from PyQt6.QtWidgets import QMessageBox

        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        mock_dependencies["manager"].delete_macro.side_effect = FileNotFoundError()

        widget = MacroEditorWidget()
        macro = Macro(name="Missing")
        widget._current_macro = macro

        with patch("g13_linux.gui.views.macro_editor.QMessageBox") as mock_box:
            mock_box.StandardButton = QMessageBox.StandardButton
            mock_box.question.return_value = QMessageBox.StandardButton.Yes

            # Should not raise
            widget._delete_macro()


class TestMacroEditorInsertDelayWithValue:
    """Tests for insert delay with actual value."""

    def test_insert_delay_adds_step(self, qapp, mock_dependencies):
        """Test insert delay adds step to macro."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        widget._current_macro = macro
        widget._refresh_steps_list()

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getInt.return_value = (500, True)  # 500ms delay

            widget._insert_delay()

            assert macro.step_count == 2
            # Delay inserted at end since no selection
            assert macro.steps[-1].step_type == MacroStepType.DELAY
            assert macro.steps[-1].value == 500

    def test_insert_delay_at_selection(self, qapp, mock_dependencies):
        """Test insert delay inserts at selected position."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        macro.add_step(MacroStepType.KEY_RELEASE, "KEY_A", False, 100)
        widget._current_macro = macro
        widget._refresh_steps_list()
        widget.steps_list.setCurrentRow(1)  # Select second item

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getInt.return_value = (200, True)

            widget._insert_delay()

            assert macro.step_count == 3
            # Delay inserted at index 1
            assert macro.steps[1].step_type == MacroStepType.DELAY
            assert macro.steps[1].value == 200

    def test_insert_delay_cancelled(self, qapp, mock_dependencies):
        """Test insert delay cancelled doesn't add step."""
        from g13_linux.gui.models.macro_types import Macro, MacroStepType
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="Test")
        macro.add_step(MacroStepType.KEY_PRESS, "KEY_A", True, 0)
        widget._current_macro = macro

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getInt.return_value = (0, False)  # Cancelled

            widget._insert_delay()

            assert macro.step_count == 1  # No change

    def test_insert_delay_enables_save(self, qapp, mock_dependencies):
        """Test insert delay enables save button."""
        from g13_linux.gui.models.macro_types import Macro
        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()
        macro = Macro(name="Test")
        widget._current_macro = macro
        widget.save_btn.setEnabled(False)

        with patch("g13_linux.gui.views.macro_editor.QInputDialog") as mock_dialog:
            mock_dialog.getInt.return_value = (100, True)

            widget._insert_delay()

            assert widget.save_btn.isEnabled() is True


class TestMacroEditorMissingCoverage:
    """Tests for edge cases to achieve 100% coverage."""

    def test_on_macro_selected_non_macro_list_item(self, qapp, mock_dependencies):
        """Test _on_macro_selected with non-MacroListItem (line 259->exit).

        When current is a QListWidgetItem but not a MacroListItem,
        the isinstance check fails and the branch is skipped.
        """
        from PyQt6.QtWidgets import QListWidgetItem

        from g13_linux.gui.views.macro_editor import MacroEditorWidget

        widget = MacroEditorWidget()

        # Create a plain QListWidgetItem (not MacroListItem)
        plain_item = QListWidgetItem("Not a macro")

        # Call with non-MacroListItem - should not raise, just skip
        widget._on_macro_selected(plain_item, None)

        # Editor should not be enabled (no macro loaded)
        assert widget._current_macro is None
