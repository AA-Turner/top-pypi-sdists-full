"""Dialog for recording new macros."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
)

from ..models.macro_recorder import MacroRecorder, RecorderState
from ..models.macro_types import InputSource, Macro, MacroStep


class MacroRecordDialog(QDialog):
    """
    Dialog for recording new macros.

    Shows recording status, captured steps, and provides start/stop controls.
    """

    macro_recorded = pyqtSignal(object)  # Macro

    def __init__(self, recorder: MacroRecorder | None = None, parent: object | None = None):
        super().__init__(parent)
        self.recorder = recorder or MacroRecorder()
        self._recorded_macro: Macro | None = None
        self._init_ui()
        self._connect_signals()

    def _init_ui(self) -> None:
        self.setWindowTitle("Record Macro")
        self.setMinimumSize(500, 450)
        self.setModal(True)

        layout = QVBoxLayout()

        # Status indicator
        status_layout = QHBoxLayout()
        self.status_indicator = QLabel("IDLE")
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_indicator.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                background-color: #555555;
                color: white;
            }
        """
        )
        status_layout.addWidget(self.status_indicator)
        layout.addLayout(status_layout)

        # Input source options
        source_group = QGroupBox("Capture Sources")
        source_layout = QHBoxLayout()
        self.g13_checkbox = QCheckBox("G13 Buttons")
        self.g13_checkbox.setChecked(True)
        self.keyboard_checkbox = QCheckBox("System Keyboard")
        self.keyboard_checkbox.setChecked(True)
        source_layout.addWidget(self.g13_checkbox)
        source_layout.addWidget(self.keyboard_checkbox)
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Instructions
        instructions = QLabel(
            "Click 'Start Recording' or press MR button on G13.\n"
            "Recording begins when you press any key.\n"
            "Press 'Stop Recording' or MR button again to finish."
        )
        instructions.setStyleSheet("color: #888888; font-style: italic;")
        layout.addWidget(instructions)

        # Live step view
        steps_group = QGroupBox("Recorded Steps")
        steps_layout = QVBoxLayout()

        self.steps_list = QListWidget()
        self.steps_list.setStyleSheet(
            """
            QListWidget {
                font-family: monospace;
                font-size: 11px;
                background-color: #1E1E1E;
                color: #00FF00;
            }
            QListWidget::item {
                padding: 2px;
            }
        """
        )
        steps_layout.addWidget(self.steps_list)

        # Stats row
        stats_layout = QHBoxLayout()
        self.step_count_label = QLabel("Steps: 0")
        self.duration_label = QLabel("Duration: 0ms")
        stats_layout.addWidget(self.step_count_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.duration_label)
        steps_layout.addLayout(stats_layout)

        steps_group.setLayout(steps_layout)
        layout.addWidget(steps_group)

        # Controls
        control_layout = QHBoxLayout()

        self.record_btn = QPushButton("Start Recording")
        self.record_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #D32F2F;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
        """
        )
        self.record_btn.clicked.connect(self._toggle_recording)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel)

        self.save_btn = QPushButton("Save Macro")
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #388E3C;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2E7D32;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """
        )
        self.save_btn.clicked.connect(self._save_macro)

        control_layout.addWidget(self.record_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.cancel_btn)
        control_layout.addWidget(self.save_btn)

        layout.addLayout(control_layout)

        self.setLayout(layout)

    def _connect_signals(self) -> None:
        self.recorder.state_changed.connect(self._on_state_changed)
        self.recorder.step_recorded.connect(self._on_step_recorded)
        self.recorder.recording_complete.connect(self._on_recording_complete)
        self.recorder.error_occurred.connect(self._on_error)

    def _get_input_source(self) -> InputSource:
        g13 = self.g13_checkbox.isChecked()
        keyboard = self.keyboard_checkbox.isChecked()

        if g13 and keyboard:
            return InputSource.BOTH
        elif g13:
            return InputSource.G13_ONLY
        elif keyboard:
            return InputSource.SYSTEM_ONLY
        else:
            return InputSource.G13_ONLY  # Default

    def _toggle_recording(self) -> None:
        if self.recorder.is_recording:
            self.recorder.stop_recording()
        else:
            self.steps_list.clear()
            self._recorded_macro = None
            self.save_btn.setEnabled(False)
            self.recorder.start_recording(self._get_input_source())

    def _on_state_changed(self, state: RecorderState) -> None:
        states = {
            RecorderState.IDLE: ("IDLE", "#555555", "Start Recording"),
            RecorderState.WAITING: (
                "ARMED - Press any key",
                "#FFA000",
                "Stop Recording",
            ),
            RecorderState.RECORDING: ("RECORDING", "#D32F2F", "Stop Recording"),
            RecorderState.SAVING: ("SAVING...", "#388E3C", "Please wait..."),
        }

        text, color, btn_text = states.get(state, ("Unknown", "#555555", "..."))
        self.status_indicator.setText(text)
        self.status_indicator.setStyleSheet(
            f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                background-color: {color};
                color: white;
            }}
        """
        )
        self.record_btn.setText(btn_text)

        # Disable source checkboxes while recording
        is_idle = state == RecorderState.IDLE
        self.g13_checkbox.setEnabled(is_idle)
        self.keyboard_checkbox.setEnabled(is_idle)

    def _on_step_recorded(self, step: MacroStep) -> None:
        action = "+" if step.is_press else "-"
        text = f"{step.timestamp_ms:6d}ms | {action} {step.value}"
        self.steps_list.addItem(text)
        self.steps_list.scrollToBottom()

        count = self.steps_list.count()
        self.step_count_label.setText(f"Steps: {count}")
        self.duration_label.setText(f"Duration: {step.timestamp_ms}ms")

    def _on_recording_complete(self, macro: Macro) -> None:
        self._recorded_macro = macro
        self.save_btn.setEnabled(True)
        self.step_count_label.setText(f"Steps: {macro.step_count}")
        self.duration_label.setText(f"Duration: {macro.duration_ms}ms")

    def _on_error(self, message: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.warning(self, "Recording Error", message)

    def _save_macro(self) -> None:
        if self._recorded_macro:
            self.macro_recorded.emit(self._recorded_macro)
            self.accept()

    def _on_cancel(self) -> None:
        if self.recorder.is_recording:
            self.recorder.cancel()
        self.reject()

    def closeEvent(self, event) -> None:
        if self.recorder.is_recording:
            self.recorder.cancel()
        super().closeEvent(event)
