"""Macro editor widget with list, editor, and playback controls."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..models.macro_manager import MacroManager
from ..models.macro_player import MacroPlayer, PlaybackState
from ..models.macro_recorder import MacroRecorder
from ..models.macro_types import Macro, MacroStep, PlaybackMode
from ..widgets.macro_record_dialog import MacroRecordDialog


class MacroListItem(QListWidgetItem):
    """List item representing a macro."""

    def __init__(self, macro_id: str, name: str, step_count: int):
        super().__init__()
        self.macro_id = macro_id
        self.setText(f"{name} ({step_count} steps)")


class MacroEditorWidget(QWidget):
    """
    Full-featured macro editor with library, editor panel, and playback.

    Layout:
    - Left: Macro library list with New/Delete buttons
    - Right: Editor panel with properties, step list, and playback settings
    """

    macro_assigned = pyqtSignal(str, str)  # (button_id, macro_id)
    macro_saved = pyqtSignal(object)  # Emits Macro when saved

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.macro_manager = MacroManager()
        self.macro_recorder = MacroRecorder()
        self.macro_player = MacroPlayer()
        self._current_macro: Macro | None = None
        self._init_ui()
        self._connect_signals()
        self._refresh_macro_list()

    def _init_ui(self) -> None:
        layout = QHBoxLayout()

        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Macro library
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        library_label = QLabel("Macro Library")
        library_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        left_layout.addWidget(library_label)

        self.macro_list = QListWidget()
        self.macro_list.currentItemChanged.connect(self._on_macro_selected)
        left_layout.addWidget(self.macro_list)

        # Library buttons
        lib_buttons = QHBoxLayout()
        self.new_btn = QPushButton("New")
        self.new_btn.clicked.connect(self._create_new_macro)
        self.record_btn = QPushButton("Record")
        self.record_btn.clicked.connect(self._open_record_dialog)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self._delete_macro)
        self.delete_btn.setEnabled(False)
        lib_buttons.addWidget(self.new_btn)
        lib_buttons.addWidget(self.record_btn)
        lib_buttons.addWidget(self.delete_btn)
        left_layout.addLayout(lib_buttons)

        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        # Right panel: Editor
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Properties group
        props_group = QGroupBox("Macro Properties")
        props_layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Macro name...")
        self.name_edit.textChanged.connect(self._on_property_changed)
        props_layout.addRow("Name:", self.name_edit)

        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Description (optional)")
        self.description_edit.textChanged.connect(self._on_property_changed)
        props_layout.addRow("Description:", self.description_edit)

        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setPlaceholderText("e.g., Ctrl+Shift+F1")
        self.hotkey_edit.setToolTip(
            "Global hotkey to trigger this macro.\n"
            "Format: Ctrl+Shift+F1, Alt+F12, etc.\n"
            "Leave empty for no hotkey."
        )
        self.hotkey_edit.textChanged.connect(self._on_property_changed)
        props_layout.addRow("Global Hotkey:", self.hotkey_edit)

        props_group.setLayout(props_layout)
        right_layout.addWidget(props_group)

        # Steps group
        steps_group = QGroupBox("Macro Steps")
        steps_layout = QVBoxLayout()

        self.steps_list = QListWidget()
        self.steps_list.setStyleSheet(
            """
            QListWidget {
                font-family: monospace;
                font-size: 10px;
            }
        """
        )
        steps_layout.addWidget(self.steps_list)

        # Step buttons
        step_buttons = QHBoxLayout()
        self.insert_delay_btn = QPushButton("Insert Delay")
        self.insert_delay_btn.clicked.connect(self._insert_delay)
        self.delete_step_btn = QPushButton("Delete Step")
        self.delete_step_btn.clicked.connect(self._delete_step)
        step_buttons.addWidget(self.insert_delay_btn)
        step_buttons.addWidget(self.delete_step_btn)
        step_buttons.addStretch()
        steps_layout.addLayout(step_buttons)

        steps_group.setLayout(steps_layout)
        right_layout.addWidget(steps_group)

        # Playback settings group
        playback_group = QGroupBox("Playback Settings")
        playback_layout = QFormLayout()

        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(0.1, 10.0)
        self.speed_spin.setValue(1.0)
        self.speed_spin.setSingleStep(0.1)
        self.speed_spin.setSuffix("x")
        self.speed_spin.valueChanged.connect(self._on_property_changed)
        playback_layout.addRow("Speed:", self.speed_spin)

        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(0, 1000)
        self.repeat_spin.setValue(1)
        self.repeat_spin.setSpecialValueText("Infinite")
        self.repeat_spin.valueChanged.connect(self._on_property_changed)
        playback_layout.addRow("Repeat:", self.repeat_spin)

        self.repeat_delay_spin = QSpinBox()
        self.repeat_delay_spin.setRange(0, 60000)
        self.repeat_delay_spin.setValue(0)
        self.repeat_delay_spin.setSuffix(" ms")
        self.repeat_delay_spin.valueChanged.connect(self._on_property_changed)
        playback_layout.addRow("Repeat Delay:", self.repeat_delay_spin)

        self.playback_mode_combo = QComboBox()
        self.playback_mode_combo.addItems(["Recorded Timing", "Fixed Delay", "As Fast As Possible"])
        self.playback_mode_combo.currentIndexChanged.connect(self._on_property_changed)
        playback_layout.addRow("Timing Mode:", self.playback_mode_combo)

        self.fixed_delay_spin = QSpinBox()
        self.fixed_delay_spin.setRange(1, 1000)
        self.fixed_delay_spin.setValue(10)
        self.fixed_delay_spin.setSuffix(" ms")
        self.fixed_delay_spin.valueChanged.connect(self._on_property_changed)
        playback_layout.addRow("Fixed Delay:", self.fixed_delay_spin)

        playback_group.setLayout(playback_layout)
        right_layout.addWidget(playback_group)

        # Action buttons
        action_layout = QHBoxLayout()

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self._play_macro)
        self.play_btn.setEnabled(False)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self._stop_macro)
        self.stop_btn.setEnabled(False)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self._save_macro)
        self.save_btn.setEnabled(False)

        action_layout.addWidget(self.play_btn)
        action_layout.addWidget(self.stop_btn)
        action_layout.addStretch()
        action_layout.addWidget(self.save_btn)

        right_layout.addLayout(action_layout)

        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setSizes([200, 400])

        layout.addWidget(splitter)
        self.setLayout(layout)

        # Disable editor initially
        self._set_editor_enabled(False)

    def _connect_signals(self) -> None:
        self.macro_player.state_changed.connect(self._on_playback_state_changed)
        self.macro_player.playback_complete.connect(self._on_playback_complete)
        self.macro_player.error_occurred.connect(self._on_error)

    def _refresh_macro_list(self) -> None:
        """Refresh the macro library list."""
        self.macro_list.clear()
        for summary in self.macro_manager.list_macro_summaries():
            item = MacroListItem(summary["id"], summary["name"], summary["step_count"])
            self.macro_list.addItem(item)

    def _on_macro_selected(
        self, current: QListWidgetItem | None, previous: QListWidgetItem | None
    ) -> None:
        """Handle macro selection from list."""
        if current is None:
            self._current_macro = None
            self._set_editor_enabled(False)
            self.delete_btn.setEnabled(False)
            return

        if isinstance(current, MacroListItem):
            try:
                self._current_macro = self.macro_manager.load_macro(current.macro_id)
                self._load_macro_to_editor()
                self._set_editor_enabled(True)
                self.delete_btn.setEnabled(True)
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "Macro not found")

    def _load_macro_to_editor(self) -> None:
        """Load current macro into editor fields."""
        if not self._current_macro:
            return

        # Block signals to prevent triggering save
        self.name_edit.blockSignals(True)
        self.description_edit.blockSignals(True)
        self.hotkey_edit.blockSignals(True)
        self.speed_spin.blockSignals(True)
        self.repeat_spin.blockSignals(True)
        self.repeat_delay_spin.blockSignals(True)
        self.playback_mode_combo.blockSignals(True)
        self.fixed_delay_spin.blockSignals(True)

        self.name_edit.setText(self._current_macro.name)
        self.description_edit.setText(self._current_macro.description)
        self.hotkey_edit.setText(self._current_macro.global_hotkey or "")
        self.speed_spin.setValue(self._current_macro.speed_multiplier)
        self.repeat_spin.setValue(self._current_macro.repeat_count)
        self.repeat_delay_spin.setValue(self._current_macro.repeat_delay_ms)
        self.fixed_delay_spin.setValue(self._current_macro.fixed_delay_ms)

        mode_index = {
            PlaybackMode.RECORDED: 0,
            PlaybackMode.FIXED: 1,
            PlaybackMode.AS_FAST: 2,
        }.get(self._current_macro.playback_mode, 0)
        self.playback_mode_combo.setCurrentIndex(mode_index)

        # Unblock signals
        self.name_edit.blockSignals(False)
        self.description_edit.blockSignals(False)
        self.hotkey_edit.blockSignals(False)
        self.speed_spin.blockSignals(False)
        self.repeat_spin.blockSignals(False)
        self.repeat_delay_spin.blockSignals(False)
        self.playback_mode_combo.blockSignals(False)
        self.fixed_delay_spin.blockSignals(False)

        self._refresh_steps_list()

    def _refresh_steps_list(self) -> None:
        """Refresh the steps list from current macro."""
        self.steps_list.clear()
        if self._current_macro:
            for idx, step in enumerate(self._current_macro.steps):
                action = "+" if step.is_press else "-"
                text = f"{idx:03d} | {step.timestamp_ms:6d}ms | {action} {step.value}"
                self.steps_list.addItem(text)

    def _set_editor_enabled(self, enabled: bool) -> None:
        """Enable/disable editor controls."""
        self.name_edit.setEnabled(enabled)
        self.description_edit.setEnabled(enabled)
        self.hotkey_edit.setEnabled(enabled)
        self.speed_spin.setEnabled(enabled)
        self.repeat_spin.setEnabled(enabled)
        self.repeat_delay_spin.setEnabled(enabled)
        self.playback_mode_combo.setEnabled(enabled)
        self.fixed_delay_spin.setEnabled(enabled)
        self.insert_delay_btn.setEnabled(enabled)
        self.delete_step_btn.setEnabled(enabled)
        self.play_btn.setEnabled(
            enabled and bool(self._current_macro and self._current_macro.steps)
        )
        self.save_btn.setEnabled(enabled)

    def _on_property_changed(self) -> None:
        """Mark macro as modified when property changes."""
        self.save_btn.setEnabled(True)

    def _apply_changes(self) -> None:
        """Apply UI changes to current macro."""
        if not self._current_macro:
            return

        self._current_macro.name = self.name_edit.text()
        self._current_macro.description = self.description_edit.text()
        hotkey = self.hotkey_edit.text().strip()
        self._current_macro.global_hotkey = hotkey if hotkey else None
        self._current_macro.speed_multiplier = self.speed_spin.value()
        self._current_macro.repeat_count = self.repeat_spin.value()
        self._current_macro.repeat_delay_ms = self.repeat_delay_spin.value()
        self._current_macro.fixed_delay_ms = self.fixed_delay_spin.value()

        mode_map = {
            0: PlaybackMode.RECORDED,
            1: PlaybackMode.FIXED,
            2: PlaybackMode.AS_FAST,
        }
        self._current_macro.playback_mode = mode_map.get(
            self.playback_mode_combo.currentIndex(), PlaybackMode.RECORDED
        )

    def _create_new_macro(self) -> None:
        """Create a new empty macro."""
        name, ok = QInputDialog.getText(self, "New Macro", "Macro name:")
        if ok and name:
            macro = self.macro_manager.create_macro(name)
            self._refresh_macro_list()
            # Select the new macro
            for i in range(self.macro_list.count()):
                item = self.macro_list.item(i)
                if isinstance(item, MacroListItem) and item.macro_id == macro.id:
                    self.macro_list.setCurrentItem(item)
                    break

    def _open_record_dialog(self) -> None:
        """Open the macro recording dialog."""
        dialog = MacroRecordDialog(self.macro_recorder, self)
        dialog.macro_recorded.connect(self._on_macro_recorded)
        dialog.exec()

    def _on_macro_recorded(self, macro: Macro) -> None:
        """Handle newly recorded macro."""
        # Prompt for name
        name, ok = QInputDialog.getText(self, "Save Macro", "Macro name:", text=macro.name)
        if ok and name:
            macro.name = name
            self.macro_manager.save_macro(macro)
            self._refresh_macro_list()

    def _delete_macro(self) -> None:
        """Delete the selected macro."""
        if not self._current_macro:
            return

        reply = QMessageBox.question(
            self,
            "Delete Macro",
            f"Delete macro '{self._current_macro.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.macro_manager.delete_macro(self._current_macro.id)
                self._current_macro = None
                self._refresh_macro_list()
                self._set_editor_enabled(False)
            except FileNotFoundError:
                pass  # Macro file already deleted, update UI anyway

    def _insert_delay(self) -> None:
        """Insert a delay step at current position."""
        if not self._current_macro:
            return

        delay_ms, ok = QInputDialog.getInt(self, "Insert Delay", "Delay (ms):", 100, 1, 60000)
        if ok:
            from ..models.macro_types import MacroStepType

            # Insert at current selection or end
            idx = self.steps_list.currentRow()
            if idx < 0:
                idx = len(self._current_macro.steps)

            step = MacroStep(
                step_type=MacroStepType.DELAY,
                value=delay_ms,
                is_press=True,
                timestamp_ms=0,
            )
            self._current_macro.steps.insert(idx, step)
            self._refresh_steps_list()
            self.save_btn.setEnabled(True)

    def _delete_step(self) -> None:
        """Delete the selected step."""
        if not self._current_macro:
            return

        idx = self.steps_list.currentRow()
        if idx >= 0 and idx < len(self._current_macro.steps):
            del self._current_macro.steps[idx]
            self._refresh_steps_list()
            self.save_btn.setEnabled(True)

    def _play_macro(self) -> None:
        """Play the current macro."""
        if self._current_macro:
            self._apply_changes()
            self.macro_player.play(self._current_macro)

    def _stop_macro(self) -> None:
        """Stop macro playback."""
        self.macro_player.stop()

    def _save_macro(self) -> None:
        """Save the current macro."""
        if self._current_macro:
            self._apply_changes()
            self.macro_manager.save_macro(self._current_macro)
            self._refresh_macro_list()
            self.save_btn.setEnabled(False)
            self.macro_saved.emit(self._current_macro)

    def _on_playback_state_changed(self, state: PlaybackState) -> None:
        """Update UI based on playback state."""
        is_playing = state in (PlaybackState.PLAYING, PlaybackState.PAUSED)
        self.play_btn.setEnabled(not is_playing and self._current_macro is not None)
        self.stop_btn.setEnabled(is_playing)
        self.play_btn.setText("Pause" if state == PlaybackState.PLAYING else "Play")

    def _on_playback_complete(self) -> None:
        """Handle playback completion."""
        self.play_btn.setEnabled(self._current_macro is not None)
        self.stop_btn.setEnabled(False)
        self.play_btn.setText("Play")

    def _on_error(self, message: str) -> None:
        """Handle error."""
        QMessageBox.warning(self, "Macro Error", message)

    def refresh_macro_list(self) -> None:
        """Public method to refresh macro list."""
        self._refresh_macro_list()
