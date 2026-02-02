"""
CSSL GUI Builder - Main application window.
Orchestrates all panels, canvas, toolbar, and file operations.
"""

import os

from PyQt6.QtWidgets import (QMainWindow, QDockWidget, QFileDialog,
                              QMessageBox, QStatusBar, QApplication,
                              QWidget)
from PyQt6.QtCore import Qt, QSize

from .models import SceneModel, WidgetModel
from .constants import CsslWidgetType, WIDGET_REGISTRY
from .commands import CommandHistory
from .canvas import DesignCanvas
from .widget_palette import WidgetPalette
from .property_editor import PropertyEditor
from .widget_tree import WidgetTreePanel
from .toolbar import MainToolbar
from .dialogs import NewProjectDialog, CodePreviewDialog
from . import theme


class GuiMakerApp(QMainWindow):
    """Main window for the CSSL GUI Builder application."""

    def __init__(self, initial_file: str = ""):
        super().__init__()
        self.setWindowTitle("CSSL GUI Builder")
        self.setMinimumSize(QSize(1100, 700))
        self.resize(1400, 850)

        # Core state
        self._scene_model = SceneModel()
        self._command_history = CommandHistory()
        self._current_file: str = ""
        self._dirty = False

        self._setup_ui()
        self._connect_signals()

        # Apply theme
        self.setStyleSheet(theme.STYLESHEET)

        # Load initial file or create new project
        if initial_file and os.path.isfile(initial_file):
            self._load_file(initial_file)
        else:
            self._new_project_auto()

    def _setup_ui(self) -> None:
        # --- Central widget: Canvas ---
        self._canvas = DesignCanvas(self._scene_model, self._command_history)
        self.setCentralWidget(self._canvas)

        # --- Toolbar ---
        self._toolbar = MainToolbar(self._command_history, self)
        self.addToolBar(self._toolbar)

        # --- Left dock: Widget Palette ---
        self._palette_dock = QDockWidget("Widgets", self)
        self._palette_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self._palette = WidgetPalette()
        self._palette_dock.setWidget(self._palette)
        self._palette_dock.setMinimumWidth(200)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._palette_dock)

        # --- Right dock: Property Editor ---
        self._props_dock = QDockWidget("Properties", self)
        self._props_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self._property_editor = PropertyEditor(self._scene_model, self._command_history)
        self._props_dock.setWidget(self._property_editor)
        self._props_dock.setMinimumWidth(260)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._props_dock)

        # --- Bottom dock: Widget Tree ---
        self._tree_dock = QDockWidget("Widget Tree", self)
        self._tree_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self._widget_tree = WidgetTreePanel(self._scene_model, self._command_history)
        self._tree_dock.setWidget(self._widget_tree)
        self._tree_dock.setMinimumHeight(120)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._tree_dock)

        # --- Status bar ---
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("Ready")

    def _connect_signals(self) -> None:
        # Toolbar -> app
        self._toolbar.new_project.connect(self._on_new_project)
        self._toolbar.open_file.connect(self._on_open_file)
        self._toolbar.save_file.connect(self._on_save_file)
        self._toolbar.save_file_as.connect(self._on_save_file_as)
        self._toolbar.preview_code.connect(self._on_preview_code)
        self._toolbar.zoom_in.connect(self._canvas.zoom_in)
        self._toolbar.zoom_out.connect(self._canvas.zoom_out)
        self._toolbar.zoom_reset.connect(self._canvas.zoom_reset)
        self._toolbar.toggle_grid.connect(self._on_toggle_grid)
        self._toolbar.toggle_snap.connect(self._on_toggle_snap)

        # Canvas -> app
        self._canvas.widget_selected.connect(self._on_canvas_widget_selected)
        self._canvas.widget_deselected.connect(self._on_canvas_widget_deselected)
        self._canvas.widget_added.connect(self._on_widget_added)

        # Tree -> app
        self._widget_tree.widget_selected.connect(self._on_tree_widget_selected)
        self._widget_tree.widget_deselected.connect(self._on_tree_widget_deselected)

        # Command history -> dirty flag
        self._command_history.add_listener(self._on_command_history_change)

    # --- Selection coordination ---

    def _on_canvas_widget_selected(self, widget_id: str) -> None:
        self._property_editor.set_widget(widget_id)
        self._widget_tree.select_widget(widget_id)

    def _on_canvas_widget_deselected(self) -> None:
        self._property_editor.clear_selection()
        self._widget_tree.deselect_all()

    def _on_tree_widget_selected(self, widget_id: str) -> None:
        self._canvas.select_widget(widget_id)
        self._property_editor.set_widget(widget_id)

    def _on_tree_widget_deselected(self) -> None:
        self._canvas.deselect_all()
        self._property_editor.clear_selection()

    def _on_widget_added(self, widget_id: str) -> None:
        self._widget_tree.rebuild()
        self._status.showMessage(f"Widget added: {widget_id}", 3000)

    # --- View toggles ---

    def _on_toggle_grid(self) -> None:
        self._canvas._grid_visible = not self._canvas._grid_visible
        self._canvas.scene().update()

    def _on_toggle_snap(self) -> None:
        self._canvas._snap_to_grid = not self._canvas._snap_to_grid
        snap_state = "ON" if self._canvas._snap_to_grid else "OFF"
        self._status.showMessage(f"Snap to grid: {snap_state}", 2000)

    # --- File operations ---

    def _on_new_project(self) -> None:
        if self._dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Create a new project anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        dialog = NewProjectDialog(self)
        if dialog.exec() == NewProjectDialog.DialogCode.Accepted:
            self._create_new_project(
                dialog.class_name, dialog.window_title,
                dialog.window_width, dialog.window_height
            )

    def _new_project_auto(self) -> None:
        """Create default new project without dialog."""
        self._create_new_project("MyApp", "CSSL Application", 800, 600)

    def _create_new_project(self, class_name: str, title: str,
                             width: int, height: int) -> None:
        self._scene_model.clear()
        self._command_history.clear()
        self._current_file = ""
        self._dirty = False

        self._scene_model.class_name = class_name

        # Create window widget
        window = WidgetModel(
            name="MainWindow",
            widget_type=CsslWidgetType.WIDGET,
            parent_id=None,
            x=0, y=0,
            width=width, height=height,
            z_order=0,
        )
        window.properties["title"] = title
        self._scene_model.add_widget(window)

        self._canvas.setup_window(width, height)
        self._widget_tree.rebuild()
        self._update_title()
        self._status.showMessage(f"New project: {class_name}", 3000)

    def _on_open_file(self) -> None:
        if self._dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Open a different file?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        path, _ = QFileDialog.getOpenFileName(
            self, "Open CSSL File", "",
            "CSSL Files (*.cssl);;All Files (*)"
        )
        if path:
            self._load_file(path)

    def _load_file(self, path: str) -> None:
        try:
            from .code_parser import CsslCodeParser
            parser = CsslCodeParser()
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()

            self._scene_model.clear()
            self._command_history.clear()
            parser.parse(code, self._scene_model)
            self._scene_model.source_file_path = path
            self._current_file = path

            self._canvas.refresh_all()
            self._widget_tree.rebuild()
            self._dirty = False
            self._update_title()
            self._status.showMessage(f"Loaded: {os.path.basename(path)}", 3000)
        except Exception as e:
            QMessageBox.critical(
                self, "Load Error",
                f"Failed to load file:\n{e}"
            )

    def _on_save_file(self) -> None:
        if self._current_file:
            self._save_to_file(self._current_file)
        else:
            self._on_save_file_as()

    def _on_save_file_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSSL File", "",
            "CSSL Files (*.cssl);;All Files (*)"
        )
        if path:
            if not path.endswith(".cssl"):
                path += ".cssl"
            self._save_to_file(path)

    def _save_to_file(self, path: str) -> None:
        try:
            from .code_generator import CsslCodeGenerator
            generator = CsslCodeGenerator()
            code = generator.generate(self._scene_model)

            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            self._current_file = path
            self._scene_model.source_file_path = path
            self._dirty = False
            self._update_title()
            self._status.showMessage(f"Saved: {os.path.basename(path)}", 3000)
        except Exception as e:
            QMessageBox.critical(
                self, "Save Error",
                f"Failed to save file:\n{e}"
            )

    def _on_preview_code(self) -> None:
        try:
            from .code_generator import CsslCodeGenerator
            generator = CsslCodeGenerator()
            code = generator.generate(self._scene_model)
            dialog = CodePreviewDialog(code, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(
                self, "Code Generation Error",
                f"Failed to generate code:\n{e}"
            )

    # --- Dirty tracking ---

    def _on_command_history_change(self, can_undo: bool, can_redo: bool) -> None:
        self._dirty = can_undo
        self._update_title()

    def _update_title(self) -> None:
        title = "CSSL GUI Builder"
        if self._current_file:
            title += f" - {os.path.basename(self._current_file)}"
        else:
            title += f" - {self._scene_model.class_name}"
        if self._dirty:
            title += " *"
        self.setWindowTitle(title)

    # --- Close event ---

    def closeEvent(self, event) -> None:
        if self._dirty:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Quit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
        event.accept()
