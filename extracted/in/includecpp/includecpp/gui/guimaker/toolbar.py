"""
CSSL GUI Builder - Main toolbar with file, edit, and view actions.
"""

from PyQt6.QtWidgets import QToolBar, QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

from .commands import CommandHistory
from . import theme


class MainToolbar(QToolBar):
    """Application toolbar with New/Open/Save/Undo/Redo/Grid/Snap/Zoom."""

    # File signals
    new_project = pyqtSignal()
    open_file = pyqtSignal()
    save_file = pyqtSignal()
    save_file_as = pyqtSignal()
    preview_code = pyqtSignal()

    # View signals
    zoom_in = pyqtSignal()
    zoom_out = pyqtSignal()
    zoom_reset = pyqtSignal()
    toggle_grid = pyqtSignal()
    toggle_snap = pyqtSignal()

    def __init__(self, command_history: CommandHistory, parent: QWidget = None):
        super().__init__("Main Toolbar", parent)
        self._command_history = command_history
        self._undo_action: QAction | None = None
        self._redo_action: QAction | None = None

        self.setMovable(False)
        self._build_actions()
        self._command_history.add_listener(self._on_history_change)

    def _build_actions(self) -> None:
        # --- File ---
        act_new = QAction("New", self)
        act_new.setShortcut(QKeySequence.StandardKey.New)
        act_new.setToolTip("New Project (Ctrl+N)")
        act_new.triggered.connect(self.new_project.emit)
        self.addAction(act_new)

        act_open = QAction("Open", self)
        act_open.setShortcut(QKeySequence.StandardKey.Open)
        act_open.setToolTip("Open .cssl File (Ctrl+O)")
        act_open.triggered.connect(self.open_file.emit)
        self.addAction(act_open)

        act_save = QAction("Save", self)
        act_save.setShortcut(QKeySequence.StandardKey.Save)
        act_save.setToolTip("Save (Ctrl+S)")
        act_save.triggered.connect(self.save_file.emit)
        self.addAction(act_save)

        act_save_as = QAction("Save As", self)
        act_save_as.setShortcut(QKeySequence("Ctrl+Shift+S"))
        act_save_as.setToolTip("Save As (Ctrl+Shift+S)")
        act_save_as.triggered.connect(self.save_file_as.emit)
        self.addAction(act_save_as)

        self.addSeparator()

        # --- Edit ---
        self._undo_action = QAction("Undo", self)
        self._undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self._undo_action.setToolTip("Undo (Ctrl+Z)")
        self._undo_action.setEnabled(False)
        self._undo_action.triggered.connect(self._do_undo)
        self.addAction(self._undo_action)

        self._redo_action = QAction("Redo", self)
        self._redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self._redo_action.setToolTip("Redo (Ctrl+Y)")
        self._redo_action.setEnabled(False)
        self._redo_action.triggered.connect(self._do_redo)
        self.addAction(self._redo_action)

        self.addSeparator()

        # --- View ---
        act_code = QAction("Code", self)
        act_code.setShortcut(QKeySequence("Ctrl+P"))
        act_code.setToolTip("Preview Generated Code (Ctrl+P)")
        act_code.triggered.connect(self.preview_code.emit)
        self.addAction(act_code)

        self.addSeparator()

        act_zin = QAction("Zoom +", self)
        act_zin.setShortcut(QKeySequence("Ctrl+="))
        act_zin.triggered.connect(self.zoom_in.emit)
        self.addAction(act_zin)

        act_zout = QAction("Zoom \u2212", self)
        act_zout.setShortcut(QKeySequence("Ctrl+-"))
        act_zout.triggered.connect(self.zoom_out.emit)
        self.addAction(act_zout)

        act_zreset = QAction("1:1", self)
        act_zreset.setShortcut(QKeySequence("Ctrl+0"))
        act_zreset.setToolTip("Reset Zoom")
        act_zreset.triggered.connect(self.zoom_reset.emit)
        self.addAction(act_zreset)

        self.addSeparator()

        act_grid = QAction("Grid", self)
        act_grid.setCheckable(True)
        act_grid.setChecked(True)
        act_grid.setToolTip("Toggle Grid (G)")
        act_grid.setShortcut(QKeySequence("G"))
        act_grid.triggered.connect(self.toggle_grid.emit)
        self.addAction(act_grid)

        act_snap = QAction("Snap", self)
        act_snap.setCheckable(True)
        act_snap.setChecked(True)
        act_snap.setToolTip("Toggle Snap to Grid (S)")
        act_snap.setShortcut(QKeySequence("S"))
        act_snap.triggered.connect(self.toggle_snap.emit)
        self.addAction(act_snap)

    def _do_undo(self) -> None:
        self._command_history.undo()

    def _do_redo(self) -> None:
        self._command_history.redo()

    def _on_history_change(self, can_undo: bool, can_redo: bool) -> None:
        if self._undo_action:
            self._undo_action.setEnabled(can_undo)
        if self._redo_action:
            self._redo_action.setEnabled(can_redo)
