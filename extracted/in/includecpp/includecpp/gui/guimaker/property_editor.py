"""
CSSL GUI Builder - Property editor panel (right sidebar).
Context-sensitive property editing with type-specific editors.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox,
                              QComboBox, QScrollArea, QFrame, QGroupBox,
                              QGridLayout, QPushButton, QColorDialog,
                              QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from .models import SceneModel, WidgetModel
from .constants import (CsslWidgetType, PropertyDef, WidgetTypeDef,
                         WIDGET_REGISTRY)
from .commands import (CommandHistory, ChangePropertyCommand, MoveWidgetCommand,
                       ResizeWidgetCommand, RenameWidgetCommand)
from . import theme


class ColorButton(QPushButton):
    """Button that shows a color and opens a color picker on click."""
    color_changed = pyqtSignal(str)

    def __init__(self, color: str = "", parent: QWidget = None):
        super().__init__(parent)
        self._color = color
        self.setFixedSize(60, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self._pick_color)
        self._update_style()

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value
        self._update_style()

    def _update_style(self) -> None:
        bg = self._color if self._color else "#ffffff"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border: 1px solid {theme.DARK_BORDER};
                border-radius: 3px;
            }}
            QPushButton:hover {{
                border-color: {theme.TEXT_MUTED};
            }}
        """)
        self.setToolTip(self._color or "No color set")

    def _pick_color(self) -> None:
        initial = QColor(self._color) if self._color else QColor("#ffffff")
        color = QColorDialog.getColor(initial, self, "Choose Color")
        if color.isValid():
            self._color = color.name()
            self._update_style()
            self.color_changed.emit(self._color)


class ItemsEditor(QWidget):
    """Editor for list-type properties (items, columns)."""
    items_changed = pyqtSignal(list)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._items: list[str] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Input + Add button
        row = QHBoxLayout()
        row.setSpacing(4)
        self._input = QLineEdit()
        self._input.setPlaceholderText("Add item...")
        self._input.setFixedHeight(24)
        self._input.returnPressed.connect(self._add_item)
        row.addWidget(self._input)

        self._add_btn = QPushButton("+")
        self._add_btn.setFixedSize(24, 24)
        self._add_btn.clicked.connect(self._add_item)
        self._add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.SELECTION_COLOR};
                color: #ffffff;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #5b9cf6;
            }}
        """)
        row.addWidget(self._add_btn)
        layout.addLayout(row)

        # Items list
        self._items_container = QWidget()
        self._items_layout = QVBoxLayout(self._items_container)
        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(2)
        layout.addWidget(self._items_container)

    def set_items(self, items: list) -> None:
        self._items = list(items) if items else []
        self._rebuild_list()

    def _add_item(self) -> None:
        text = self._input.text().strip()
        if text:
            self._items.append(text)
            self._input.clear()
            self._rebuild_list()
            self.items_changed.emit(self._items)

    def _remove_item(self, index: int) -> None:
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self._rebuild_list()
            self.items_changed.emit(self._items)

    def _rebuild_list(self) -> None:
        # Clear existing
        while self._items_layout.count():
            child = self._items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i, item in enumerate(self._items):
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(4)

            label = QLabel(str(item))
            label.setStyleSheet(f"""
                QLabel {{
                    background-color: {theme.DARK_CARD};
                    border: 1px solid {theme.DARK_BORDER};
                    border-radius: 3px;
                    padding: 2px 6px;
                    color: {theme.TEXT_SECONDARY};
                    font-size: 11px;
                }}
            """)
            rl.addWidget(label, 1)

            remove_btn = QPushButton("\u00d7")
            remove_btn.setFixedSize(20, 20)
            remove_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {theme.TEXT_MUTED};
                    border: none;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    color: {theme.ERROR_COLOR};
                }}
            """)
            idx = i
            remove_btn.clicked.connect(lambda checked, x=idx: self._remove_item(x))
            rl.addWidget(remove_btn)

            self._items_layout.addWidget(row)


class ToolbarSlotsEditor(QWidget):
    """Editor for toolbar slots (list of {tooltip, id} dicts)."""
    slots_changed = pyqtSignal(list)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._slots: list[dict] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        add_btn = QPushButton("+ Add Slot")
        add_btn.setFixedHeight(26)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.SELECTION_COLOR};
                color: #ffffff;
                border: none;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #5b9cf6; }}
        """)
        add_btn.clicked.connect(self._add_slot)
        layout.addWidget(add_btn)

        self._slots_container = QWidget()
        self._slots_layout = QVBoxLayout(self._slots_container)
        self._slots_layout.setContentsMargins(0, 0, 0, 0)
        self._slots_layout.setSpacing(4)
        layout.addWidget(self._slots_container)

    def set_slots(self, slots: list) -> None:
        self._slots = [dict(s) for s in slots] if slots else []
        self._rebuild()

    def _add_slot(self) -> None:
        self._slots.append({"tooltip": f"Slot {len(self._slots) + 1}", "id": ""})
        self._rebuild()
        self.slots_changed.emit(self._slots)

    def _remove_slot(self, index: int) -> None:
        if 0 <= index < len(self._slots):
            self._slots.pop(index)
            self._rebuild()
            self.slots_changed.emit(self._slots)

    def _on_field_changed(self) -> None:
        self.slots_changed.emit(self._slots)

    def _rebuild(self) -> None:
        while self._slots_layout.count():
            child = self._slots_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i, slot in enumerate(self._slots):
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(3)

            tooltip_edit = QLineEdit(slot.get("tooltip", ""))
            tooltip_edit.setPlaceholderText("Tooltip")
            tooltip_edit.setFixedHeight(22)
            idx = i
            tooltip_edit.textChanged.connect(
                lambda text, x=idx: self._update_field(x, "tooltip", text)
            )
            rl.addWidget(tooltip_edit, 2)

            id_edit = QLineEdit(slot.get("id", ""))
            id_edit.setPlaceholderText("ID")
            id_edit.setFixedHeight(22)
            id_edit.setFixedWidth(50)
            id_edit.textChanged.connect(
                lambda text, x=idx: self._update_field(x, "id", text)
            )
            rl.addWidget(id_edit)

            rm_btn = QPushButton("\u00d7")
            rm_btn.setFixedSize(20, 22)
            rm_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {theme.TEXT_MUTED};
                    border: none; font-size: 14px;
                }}
                QPushButton:hover {{ color: {theme.ERROR_COLOR}; }}
            """)
            rm_btn.clicked.connect(lambda checked, x=idx: self._remove_slot(x))
            rl.addWidget(rm_btn)

            self._slots_layout.addWidget(row)

    def _update_field(self, index: int, field: str, value: str) -> None:
        if 0 <= index < len(self._slots):
            self._slots[index][field] = value
            self._on_field_changed()


class MenuStructureEditor(QWidget):
    """Editor for menu bar structure (list of {label, items} dicts)."""
    menus_changed = pyqtSignal(list)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._menus: list[dict] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        add_btn = QPushButton("+ Add Menu")
        add_btn.setFixedHeight(26)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.SELECTION_COLOR};
                color: #ffffff;
                border: none;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #5b9cf6; }}
        """)
        add_btn.clicked.connect(self._add_menu)
        layout.addWidget(add_btn)

        self._menus_container = QWidget()
        self._menus_layout = QVBoxLayout(self._menus_container)
        self._menus_layout.setContentsMargins(0, 0, 0, 0)
        self._menus_layout.setSpacing(6)
        layout.addWidget(self._menus_container)

    def set_menus(self, menus: list) -> None:
        self._menus = []
        for m in (menus or []):
            if isinstance(m, dict):
                self._menus.append({
                    "label": m.get("label", "Menu"),
                    "items": list(m.get("items", []))
                })
        self._rebuild()

    def _add_menu(self) -> None:
        self._menus.append({"label": f"Menu{len(self._menus) + 1}", "items": []})
        self._rebuild()
        self.menus_changed.emit(self._menus)

    def _remove_menu(self, index: int) -> None:
        if 0 <= index < len(self._menus):
            self._menus.pop(index)
            self._rebuild()
            self.menus_changed.emit(self._menus)

    def _add_menu_item(self, menu_idx: int) -> None:
        if 0 <= menu_idx < len(self._menus):
            self._menus[menu_idx]["items"].append(
                {"type": "item", "label": "New Item"}
            )
            self._rebuild()
            self.menus_changed.emit(self._menus)

    def _add_separator(self, menu_idx: int) -> None:
        if 0 <= menu_idx < len(self._menus):
            self._menus[menu_idx]["items"].append({"type": "separator"})
            self._rebuild()
            self.menus_changed.emit(self._menus)

    def _remove_menu_item(self, menu_idx: int, item_idx: int) -> None:
        if 0 <= menu_idx < len(self._menus):
            items = self._menus[menu_idx]["items"]
            if 0 <= item_idx < len(items):
                items.pop(item_idx)
                self._rebuild()
                self.menus_changed.emit(self._menus)

    def _on_changed(self) -> None:
        self.menus_changed.emit(self._menus)

    def _rebuild(self) -> None:
        while self._menus_layout.count():
            child = self._menus_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for mi, menu in enumerate(self._menus):
            group = QWidget()
            group.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme.DARK_CARD};
                    border: 1px solid {theme.DARK_BORDER};
                    border-radius: 4px;
                }}
            """)
            gl = QVBoxLayout(group)
            gl.setContentsMargins(6, 6, 6, 6)
            gl.setSpacing(3)

            # Menu header: label + remove
            header = QHBoxLayout()
            header.setSpacing(4)
            label_edit = QLineEdit(menu.get("label", ""))
            label_edit.setPlaceholderText("Menu label")
            label_edit.setFixedHeight(22)
            menu_idx = mi
            label_edit.textChanged.connect(
                lambda text, x=menu_idx: self._update_menu_label(x, text)
            )
            header.addWidget(label_edit, 1)

            rm_btn = QPushButton("\u00d7")
            rm_btn.setFixedSize(20, 22)
            rm_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {theme.TEXT_MUTED};
                    border: none; font-size: 14px;
                }}
                QPushButton:hover {{ color: {theme.ERROR_COLOR}; }}
            """)
            rm_btn.clicked.connect(
                lambda checked, x=menu_idx: self._remove_menu(x)
            )
            header.addWidget(rm_btn)
            gl.addLayout(header)

            # Menu items
            for ii, item in enumerate(menu.get("items", [])):
                item_row = QHBoxLayout()
                item_row.setSpacing(3)

                if item.get("type") == "separator":
                    sep_label = QLabel("--- separator ---")
                    sep_label.setStyleSheet(f"""
                        QLabel {{
                            color: {theme.TEXT_MUTED}; font-size: 10px;
                            padding-left: 12px; background: transparent;
                            border: none;
                        }}
                    """)
                    item_row.addWidget(sep_label, 1)
                else:
                    item_edit = QLineEdit(item.get("label", ""))
                    item_edit.setPlaceholderText("Item label")
                    item_edit.setFixedHeight(20)
                    item_edit.setStyleSheet("margin-left: 12px;")
                    item_idx = ii
                    item_edit.textChanged.connect(
                        lambda text, mx=menu_idx, ix=item_idx:
                            self._update_item_label(mx, ix, text)
                    )
                    item_row.addWidget(item_edit, 1)

                rm_item = QPushButton("\u00d7")
                rm_item.setFixedSize(18, 20)
                rm_item.setStyleSheet(f"""
                    QPushButton {{
                        background: transparent; color: {theme.TEXT_MUTED};
                        border: none; font-size: 12px;
                    }}
                    QPushButton:hover {{ color: {theme.ERROR_COLOR}; }}
                """)
                item_idx2 = ii
                rm_item.clicked.connect(
                    lambda checked, mx=menu_idx, ix=item_idx2:
                        self._remove_menu_item(mx, ix)
                )
                item_row.addWidget(rm_item)
                gl.addLayout(item_row)

            # Add item / separator buttons
            btns = QHBoxLayout()
            btns.setSpacing(4)
            add_item_btn = QPushButton("+ Item")
            add_item_btn.setFixedHeight(20)
            add_item_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {theme.TEXT_MUTED};
                    border: 1px solid {theme.DARK_BORDER}; border-radius: 2px;
                    font-size: 10px; padding: 0 6px;
                }}
                QPushButton:hover {{ color: {theme.TEXT_PRIMARY}; }}
            """)
            add_item_btn.clicked.connect(
                lambda checked, x=menu_idx: self._add_menu_item(x)
            )
            btns.addWidget(add_item_btn)

            add_sep_btn = QPushButton("+ Separator")
            add_sep_btn.setFixedHeight(20)
            add_sep_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {theme.TEXT_MUTED};
                    border: 1px solid {theme.DARK_BORDER}; border-radius: 2px;
                    font-size: 10px; padding: 0 6px;
                }}
                QPushButton:hover {{ color: {theme.TEXT_PRIMARY}; }}
            """)
            add_sep_btn.clicked.connect(
                lambda checked, x=menu_idx: self._add_separator(x)
            )
            btns.addWidget(add_sep_btn)
            btns.addStretch()
            gl.addLayout(btns)

            self._menus_layout.addWidget(group)

    def _update_menu_label(self, index: int, text: str) -> None:
        if 0 <= index < len(self._menus):
            self._menus[index]["label"] = text
            self._on_changed()

    def _update_item_label(self, menu_idx: int, item_idx: int, text: str) -> None:
        if 0 <= menu_idx < len(self._menus):
            items = self._menus[menu_idx]["items"]
            if 0 <= item_idx < len(items):
                items[item_idx]["label"] = text
                self._on_changed()


class PropertyEditor(QWidget):
    """Right sidebar panel for editing selected widget properties."""

    def __init__(self, scene_model: SceneModel, command_history: CommandHistory,
                 parent: QWidget = None):
        super().__init__(parent)
        self._scene_model = scene_model
        self._command_history = command_history
        self._current_widget_id: str | None = None
        self._editors: dict[str, QWidget] = {}
        self._updating = False  # Prevents feedback loops
        self._commit_timer = QTimer()
        self._commit_timer.setSingleShot(True)
        self._commit_timer.setInterval(300)

        self._setup_ui()
        self._scene_model.add_listener(self._on_model_change)

    def _setup_ui(self) -> None:
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # No selection label
        self._empty_label = QLabel("Select a widget to\nedit its properties")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.setStyleSheet(f"""
            QLabel {{
                color: {theme.TEXT_MUTED};
                font-size: 12px;
                padding: 40px 20px;
            }}
        """)
        self._main_layout.addWidget(self._empty_label)

        # Scroll area for properties
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self._scroll.setVisible(False)

        self._props_widget = QWidget()
        self._props_layout = QVBoxLayout(self._props_widget)
        self._props_layout.setContentsMargins(8, 8, 8, 8)
        self._props_layout.setSpacing(12)
        self._scroll.setWidget(self._props_widget)

        self._main_layout.addWidget(self._scroll, 1)

    def set_widget(self, widget_id: str | None) -> None:
        """Set the currently edited widget."""
        self._current_widget_id = widget_id
        self._rebuild_editors()

    def clear_selection(self) -> None:
        self._current_widget_id = None
        self._rebuild_editors()

    def _rebuild_editors(self) -> None:
        """Rebuild all property editors for the current widget."""
        self._editors.clear()

        # Clear existing props layout
        while self._props_layout.count():
            child = self._props_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        widget = None
        if self._current_widget_id:
            widget = self._scene_model.get_widget(self._current_widget_id)

        if not widget:
            self._scroll.setVisible(False)
            self._empty_label.setVisible(True)
            return

        self._empty_label.setVisible(False)
        self._scroll.setVisible(True)

        # Widget info header
        self._add_info_section(widget)

        # Position & Size section
        self._add_geometry_section(widget)

        # Widget-specific properties
        type_def = WIDGET_REGISTRY.get(widget.widget_type)
        if type_def and type_def.properties:
            self._add_properties_section(widget, type_def)

        self._props_layout.addStretch()

    def _add_info_section(self, widget: WidgetModel) -> None:
        """Add widget info (type, name) section."""
        group = self._create_section("Widget")

        grid = QGridLayout()
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setSpacing(6)

        # Type (read-only)
        grid.addWidget(self._make_label("Type"), 0, 0)
        type_label = QLabel(widget.widget_type.value)
        type_label.setStyleSheet(f"color: {theme.TEXT_MUTED}; font-size: 12px;")
        grid.addWidget(type_label, 0, 1)

        # Variable name (editable) - maps to this->VarName in code
        grid.addWidget(self._make_label("Var Name"), 1, 0)
        name_edit = QLineEdit(widget.name)
        name_edit.setFixedHeight(26)
        name_edit.setToolTip("Variable name in generated code (this->VarName)")
        name_edit.editingFinished.connect(
            lambda: self._on_name_changed(name_edit.text())
        )
        grid.addWidget(name_edit, 1, 1)
        self._editors["__name__"] = name_edit

        # ID (read-only)
        grid.addWidget(self._make_label("ID"), 2, 0)
        id_label = QLabel(widget.id)
        id_label.setStyleSheet(f"color: {theme.TEXT_MUTED}; font-size: 11px; font-family: monospace;")
        grid.addWidget(id_label, 2, 1)

        group.setLayout(grid)
        self._props_layout.addWidget(group)

    def _add_geometry_section(self, widget: WidgetModel) -> None:
        """Add position (x, y) and size (w, h) section."""
        group = self._create_section("Geometry")

        grid = QGridLayout()
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setSpacing(6)

        # X
        grid.addWidget(self._make_label("X"), 0, 0)
        x_spin = QSpinBox()
        x_spin.setRange(-10000, 10000)
        x_spin.setValue(widget.x)
        x_spin.setFixedHeight(26)
        x_spin.valueChanged.connect(lambda v: self._on_position_changed())
        grid.addWidget(x_spin, 0, 1)
        self._editors["__x__"] = x_spin

        # Y
        grid.addWidget(self._make_label("Y"), 0, 2)
        y_spin = QSpinBox()
        y_spin.setRange(-10000, 10000)
        y_spin.setValue(widget.y)
        y_spin.setFixedHeight(26)
        y_spin.valueChanged.connect(lambda v: self._on_position_changed())
        grid.addWidget(y_spin, 0, 3)
        self._editors["__y__"] = y_spin

        # Width
        grid.addWidget(self._make_label("W"), 1, 0)
        w_spin = QSpinBox()
        w_spin.setRange(10, 10000)
        w_spin.setValue(widget.width)
        w_spin.setFixedHeight(26)
        w_spin.valueChanged.connect(lambda v: self._on_size_changed())
        grid.addWidget(w_spin, 1, 1)
        self._editors["__w__"] = w_spin

        # Height
        grid.addWidget(self._make_label("H"), 1, 2)
        h_spin = QSpinBox()
        h_spin.setRange(10, 10000)
        h_spin.setValue(widget.height)
        h_spin.setFixedHeight(26)
        h_spin.valueChanged.connect(lambda v: self._on_size_changed())
        grid.addWidget(h_spin, 1, 3)
        self._editors["__h__"] = h_spin

        group.setLayout(grid)
        self._props_layout.addWidget(group)

    def _add_properties_section(self, widget: WidgetModel, type_def: WidgetTypeDef) -> None:
        """Add widget-specific properties."""
        group = self._create_section("Properties")

        grid = QGridLayout()
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setSpacing(6)

        row = 0
        for prop_def in type_def.properties:
            grid.addWidget(self._make_label(prop_def.display_name), row, 0)
            editor = self._create_property_editor(prop_def, widget)
            if editor:
                grid.addWidget(editor, row, 1)
                self._editors[prop_def.name] = editor
            row += 1

        group.setLayout(grid)
        self._props_layout.addWidget(group)

    def _create_property_editor(self, prop_def: PropertyDef,
                                 widget: WidgetModel) -> QWidget | None:
        """Create the appropriate editor widget for a property type."""
        current_value = widget.get_property(prop_def.name, prop_def.default)

        if prop_def.prop_type == "string":
            editor = QLineEdit(str(current_value) if current_value else "")
            editor.setFixedHeight(26)
            editor.editingFinished.connect(
                lambda name=prop_def.name, ed=editor:
                    self._on_property_changed(name, ed.text())
            )
            return editor

        elif prop_def.prop_type == "int":
            editor = QSpinBox()
            editor.setFixedHeight(26)
            min_v = int(prop_def.min_val) if prop_def.min_val is not None else -100000
            max_v = int(prop_def.max_val) if prop_def.max_val is not None else 100000
            editor.setRange(min_v, max_v)
            editor.setValue(int(current_value) if current_value else 0)
            editor.valueChanged.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type == "float":
            editor = QDoubleSpinBox()
            editor.setFixedHeight(26)
            editor.setDecimals(2)
            min_v = float(prop_def.min_val) if prop_def.min_val is not None else -100000.0
            max_v = float(prop_def.max_val) if prop_def.max_val is not None else 100000.0
            editor.setRange(min_v, max_v)
            editor.setValue(float(current_value) if current_value else 0.0)
            editor.valueChanged.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type == "bool":
            editor = QCheckBox()
            editor.setChecked(bool(current_value))
            editor.toggled.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type == "color":
            editor = ColorButton(str(current_value) if current_value else "")
            editor.color_changed.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type == "choice":
            editor = QComboBox()
            editor.setFixedHeight(26)
            for choice in prop_def.choices:
                editor.addItem(choice)
            if current_value:
                idx = editor.findText(str(current_value))
                if idx >= 0:
                    editor.setCurrentIndex(idx)
            editor.currentTextChanged.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type in ("items", "list"):
            editor = ItemsEditor()
            editor.set_items(current_value if isinstance(current_value, list) else [])
            editor.items_changed.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type == "toolbar_slots":
            editor = ToolbarSlotsEditor()
            editor.set_slots(current_value if isinstance(current_value, list) else [])
            editor.slots_changed.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        elif prop_def.prop_type == "menu_structure":
            editor = MenuStructureEditor()
            editor.set_menus(current_value if isinstance(current_value, list) else [])
            editor.menus_changed.connect(
                lambda v, name=prop_def.name: self._on_property_changed(name, v)
            )
            return editor

        return None

    # --- Change handlers ---

    def _on_name_changed(self, new_name: str) -> None:
        if self._updating or not self._current_widget_id:
            return
        new_name = new_name.strip()
        if not new_name:
            return
        widget = self._scene_model.get_widget(self._current_widget_id)
        if widget and widget.name != new_name:
            if self._scene_model.is_name_available(new_name, self._current_widget_id):
                cmd = RenameWidgetCommand(
                    self._scene_model, self._current_widget_id,
                    widget.name, new_name
                )
                self._command_history.execute(cmd)

    def _on_position_changed(self) -> None:
        if self._updating or not self._current_widget_id:
            return
        widget = self._scene_model.get_widget(self._current_widget_id)
        if not widget:
            return
        x_spin = self._editors.get("__x__")
        y_spin = self._editors.get("__y__")
        if x_spin and y_spin:
            new_x = x_spin.value()
            new_y = y_spin.value()
            if new_x != widget.x or new_y != widget.y:
                cmd = MoveWidgetCommand(
                    self._scene_model, self._current_widget_id,
                    widget.x, widget.y, new_x, new_y
                )
                self._command_history.execute(cmd)

    def _on_size_changed(self) -> None:
        if self._updating or not self._current_widget_id:
            return
        widget = self._scene_model.get_widget(self._current_widget_id)
        if not widget:
            return
        w_spin = self._editors.get("__w__")
        h_spin = self._editors.get("__h__")
        if w_spin and h_spin:
            new_w = w_spin.value()
            new_h = h_spin.value()
            if new_w != widget.width or new_h != widget.height:
                cmd = ResizeWidgetCommand(
                    self._scene_model, self._current_widget_id,
                    widget.width, widget.height, new_w, new_h,
                    widget.x, widget.y, widget.x, widget.y
                )
                self._command_history.execute(cmd)

    def _on_property_changed(self, prop_name: str, value) -> None:
        if self._updating or not self._current_widget_id:
            return
        widget = self._scene_model.get_widget(self._current_widget_id)
        if not widget:
            return
        old_value = widget.get_property(prop_name)
        if old_value != value:
            cmd = ChangePropertyCommand(
                self._scene_model, self._current_widget_id,
                prop_name, old_value, value
            )
            self._command_history.execute(cmd)

    # --- Model change listener ---

    def _on_model_change(self, event: str, **kwargs) -> None:
        widget = kwargs.get("widget")
        if not widget or not self._current_widget_id:
            return
        if widget.id != self._current_widget_id:
            return

        if event in ("widget_moved", "widget_resized"):
            self._refresh_geometry()
        elif event == "property_changed":
            self._refresh_property(kwargs.get("prop_name", ""))
        elif event == "widget_renamed":
            self._refresh_name()
        elif event == "widget_removed":
            self.clear_selection()

    def _refresh_geometry(self) -> None:
        """Update geometry spinboxes from model without triggering commands."""
        widget = self._scene_model.get_widget(self._current_widget_id)
        if not widget:
            return
        self._updating = True
        try:
            x_spin = self._editors.get("__x__")
            y_spin = self._editors.get("__y__")
            w_spin = self._editors.get("__w__")
            h_spin = self._editors.get("__h__")
            if x_spin:
                x_spin.setValue(widget.x)
            if y_spin:
                y_spin.setValue(widget.y)
            if w_spin:
                w_spin.setValue(widget.width)
            if h_spin:
                h_spin.setValue(widget.height)
        finally:
            self._updating = False

    def _refresh_property(self, prop_name: str) -> None:
        """Update a specific property editor from model."""
        widget = self._scene_model.get_widget(self._current_widget_id)
        if not widget:
            return
        editor = self._editors.get(prop_name)
        if not editor:
            return

        self._updating = True
        try:
            value = widget.get_property(prop_name)
            if isinstance(editor, QLineEdit):
                editor.setText(str(value) if value else "")
            elif isinstance(editor, QSpinBox):
                editor.setValue(int(value) if value else 0)
            elif isinstance(editor, QDoubleSpinBox):
                editor.setValue(float(value) if value else 0.0)
            elif isinstance(editor, QCheckBox):
                editor.setChecked(bool(value))
            elif isinstance(editor, QComboBox):
                idx = editor.findText(str(value))
                if idx >= 0:
                    editor.setCurrentIndex(idx)
            elif isinstance(editor, ColorButton):
                editor.color = str(value) if value else ""
            elif isinstance(editor, ItemsEditor):
                editor.set_items(value if isinstance(value, list) else [])
            elif isinstance(editor, ToolbarSlotsEditor):
                editor.set_slots(value if isinstance(value, list) else [])
            elif isinstance(editor, MenuStructureEditor):
                editor.set_menus(value if isinstance(value, list) else [])
        finally:
            self._updating = False

    def _refresh_name(self) -> None:
        """Update name editor from model."""
        widget = self._scene_model.get_widget(self._current_widget_id)
        if not widget:
            return
        name_edit = self._editors.get("__name__")
        if name_edit and isinstance(name_edit, QLineEdit):
            self._updating = True
            name_edit.setText(widget.name)
            self._updating = False

    # --- Helpers ---

    @staticmethod
    def _create_section(title: str) -> QGroupBox:
        group = QGroupBox(title)
        group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {theme.DARK_BORDER};
                border-radius: 4px;
                margin-top: 14px;
                padding-top: 14px;
                color: {theme.TEXT_SECONDARY};
                font-weight: bold;
                font-size: 11px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: {theme.TEXT_MUTED};
            }}
        """)
        return group

    @staticmethod
    def _make_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("propertyLabel")
        label.setFixedWidth(70)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return label
