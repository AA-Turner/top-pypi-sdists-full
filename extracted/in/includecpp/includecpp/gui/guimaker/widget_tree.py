"""
CSSL GUI Builder - Widget hierarchy tree panel.
Displays the widget tree structure with context menu support.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                              QMenu, QInputDialog, QMessageBox, QAbstractItemView,
                              QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QAction

from .models import SceneModel, WidgetModel
from .constants import CsslWidgetType, WIDGET_REGISTRY
from .commands import CommandHistory, RemoveWidgetCommand, RenameWidgetCommand
from . import theme


class WidgetTreePanel(QWidget):
    """Bottom/side panel showing the widget hierarchy tree."""

    widget_selected = pyqtSignal(str)   # widget_id
    widget_deselected = pyqtSignal()

    def __init__(self, scene_model: SceneModel, command_history: CommandHistory,
                 parent: QWidget = None):
        super().__init__(parent)
        self._scene_model = scene_model
        self._command_history = command_history
        self._items_map: dict[str, QTreeWidgetItem] = {}
        self._updating = False

        self._setup_ui()
        self._scene_model.add_listener(self._on_model_change)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Widget", "Type"])
        self._tree.setColumnCount(2)
        self._tree.setRootIsDecorated(True)
        self._tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._show_context_menu)
        self._tree.currentItemChanged.connect(self._on_selection_changed)
        self._tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Column sizing
        header = self._tree.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self._tree)

    def rebuild(self) -> None:
        """Rebuild the entire tree from the scene model."""
        self._updating = True
        self._tree.clear()
        self._items_map.clear()

        # Add window as root if exists
        if self._scene_model.window:
            self._add_widget_item(self._scene_model.window, None)

        # Add orphan widgets (shouldn't normally happen, but safety)
        for widget in self._scene_model.get_all_widgets_ordered():
            if widget.id not in self._items_map:
                self._add_widget_item(widget, None)

        self._tree.expandAll()
        self._updating = False

    def _add_widget_item(self, widget: WidgetModel,
                          parent_item: QTreeWidgetItem | None) -> QTreeWidgetItem:
        """Add a widget and its children to the tree."""
        type_def = WIDGET_REGISTRY.get(widget.widget_type)
        icon = type_def.icon if type_def else ""
        display_name = f"{icon} {widget.name}" if widget.name else f"{icon} {widget.widget_type.value}"

        item = QTreeWidgetItem()
        item.setText(0, display_name)
        item.setText(1, widget.widget_type.value)
        item.setData(0, Qt.ItemDataRole.UserRole, widget.id)

        # Style based on widget type
        if widget.widget_type == CsslWidgetType.WIDGET:
            item.setFont(0, QFont("Segoe UI", 11, QFont.Weight.Bold))
        else:
            item.setFont(0, QFont("Segoe UI", 10))

        if parent_item:
            parent_item.addChild(item)
        else:
            self._tree.addTopLevelItem(item)

        self._items_map[widget.id] = item

        # Add children
        children = self._scene_model.get_children(widget.id)
        for child in sorted(children, key=lambda w: w.z_order):
            self._add_widget_item(child, item)

        return item

    def select_widget(self, widget_id: str) -> None:
        """Select a widget in the tree by ID."""
        item = self._items_map.get(widget_id)
        if item:
            self._updating = True
            self._tree.setCurrentItem(item)
            self._updating = False

    def deselect_all(self) -> None:
        self._updating = True
        self._tree.clearSelection()
        self._tree.setCurrentItem(None)
        self._updating = False

    # --- Signals ---

    def _on_selection_changed(self, current: QTreeWidgetItem,
                               previous: QTreeWidgetItem) -> None:
        if self._updating:
            return
        if current:
            widget_id = current.data(0, Qt.ItemDataRole.UserRole)
            if widget_id:
                self.widget_selected.emit(widget_id)
        else:
            self.widget_deselected.emit()

    # --- Context menu ---

    def _show_context_menu(self, pos) -> None:
        item = self._tree.itemAt(pos)
        if not item:
            return
        widget_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not widget_id:
            return
        widget = self._scene_model.get_widget(widget_id)
        if not widget:
            return

        menu = QMenu(self)

        # Rename
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self._rename_widget(widget_id))
        menu.addAction(rename_action)

        # Delete (not for window)
        if widget.widget_type != CsslWidgetType.WIDGET:
            menu.addSeparator()
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self._delete_widget(widget_id))
            menu.addAction(delete_action)

        menu.exec(self._tree.mapToGlobal(pos))

    def _rename_widget(self, widget_id: str) -> None:
        widget = self._scene_model.get_widget(widget_id)
        if not widget:
            return

        new_name, ok = QInputDialog.getText(
            self, "Rename Widget", "New name:",
            text=widget.name
        )
        if ok and new_name.strip():
            new_name = new_name.strip()
            if self._scene_model.is_name_available(new_name, widget_id):
                cmd = RenameWidgetCommand(
                    self._scene_model, widget_id,
                    widget.name, new_name
                )
                self._command_history.execute(cmd)
            else:
                QMessageBox.warning(self, "Name Taken",
                                    f"The name '{new_name}' is already in use.")

    def _delete_widget(self, widget_id: str) -> None:
        widget = self._scene_model.get_widget(widget_id)
        if not widget or widget.widget_type == CsslWidgetType.WIDGET:
            return

        children = self._scene_model.get_children(widget_id)
        msg = f"Delete '{widget.name}'?"
        if children:
            msg += f"\nThis will also remove {len(children)} child widget(s)."

        reply = QMessageBox.question(
            self, "Delete Widget", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            cmd = RemoveWidgetCommand(self._scene_model, widget_id)
            self._command_history.execute(cmd)

    # --- Model change listener ---

    def _on_model_change(self, event: str, **kwargs) -> None:
        if event == "widget_added":
            self.rebuild()
        elif event == "widget_removed":
            self.rebuild()
        elif event == "widget_renamed":
            widget = kwargs.get("widget")
            if widget and widget.id in self._items_map:
                type_def = WIDGET_REGISTRY.get(widget.widget_type)
                icon = type_def.icon if type_def else ""
                self._items_map[widget.id].setText(
                    0, f"{icon} {widget.name}"
                )
        elif event == "scene_cleared":
            self._tree.clear()
            self._items_map.clear()
