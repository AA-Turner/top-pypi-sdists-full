"""
Key Selector Dialog

Dialog for selecting keyboard key mappings with combo key support.
"""

from evdev import ecodes
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class KeySelectorDialog(QDialog):
    """Dialog for selecting key mappings with combo key support.

    Supports two return formats:
    - Simple: 'KEY_A' (when no modifiers selected)
    - Combo: {'keys': ['KEY_LEFTCTRL', 'KEY_A'], 'label': 'Copy'} (with modifiers)
    """

    def __init__(self, button_id: str, current_mapping: str | dict | None = None, parent=None):
        super().__init__(parent)
        self.button_id = button_id
        self.selected_key = None
        self._main_key = None
        self._current_mapping = current_mapping
        self._init_ui()
        self._load_current_mapping()

    def _init_ui(self):
        self.setWindowTitle(f"Map {self.button_id}")
        self.setMinimumSize(550, 500)

        layout = QVBoxLayout()

        # Title
        title = QLabel(f"Select key mapping for {self.button_id}")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Modifiers section
        mod_group = QGroupBox("Modifiers (for combo keys)")
        mod_layout = QHBoxLayout()

        self.ctrl_check = QCheckBox("Ctrl")
        self.alt_check = QCheckBox("Alt")
        self.shift_check = QCheckBox("Shift")
        self.meta_check = QCheckBox("Super")

        mod_layout.addWidget(self.ctrl_check)
        mod_layout.addWidget(self.alt_check)
        mod_layout.addWidget(self.shift_check)
        mod_layout.addWidget(self.meta_check)
        mod_layout.addStretch()

        mod_group.setLayout(mod_layout)
        layout.addWidget(mod_group)

        # Connect modifier changes to preview update
        for check in [self.ctrl_check, self.alt_check, self.shift_check, self.meta_check]:
            check.toggled.connect(self._update_preview)

        # Tabs for different key categories
        tabs = QTabWidget()

        # Tab 1: Common keys (excluding modifiers for cleaner selection)
        common_keys = [
            "KEY_1",
            "KEY_2",
            "KEY_3",
            "KEY_4",
            "KEY_5",
            "KEY_6",
            "KEY_7",
            "KEY_8",
            "KEY_9",
            "KEY_0",
            "KEY_A",
            "KEY_B",
            "KEY_C",
            "KEY_D",
            "KEY_E",
            "KEY_F",
            "KEY_G",
            "KEY_H",
            "KEY_I",
            "KEY_J",
            "KEY_K",
            "KEY_L",
            "KEY_M",
            "KEY_N",
            "KEY_O",
            "KEY_P",
            "KEY_Q",
            "KEY_R",
            "KEY_S",
            "KEY_T",
            "KEY_U",
            "KEY_V",
            "KEY_W",
            "KEY_X",
            "KEY_Y",
            "KEY_Z",
            "KEY_ENTER",
            "KEY_SPACE",
            "KEY_ESC",
            "KEY_TAB",
            "KEY_BACKSPACE",
            "KEY_DELETE",
            "KEY_HOME",
            "KEY_END",
            "KEY_PAGEUP",
            "KEY_PAGEDOWN",
            "KEY_UP",
            "KEY_DOWN",
            "KEY_LEFT",
            "KEY_RIGHT",
        ]
        tabs.addTab(self._create_key_list(common_keys), "Common Keys")

        # Tab 2: Function keys
        fn_keys = [f"KEY_F{i}" for i in range(1, 25)]
        tabs.addTab(self._create_key_list(fn_keys), "Function Keys")

        # Tab 3: Modifiers only (for single modifier mapping)
        modifier_keys = [
            "KEY_LEFTCTRL",
            "KEY_RIGHTCTRL",
            "KEY_LEFTSHIFT",
            "KEY_RIGHTSHIFT",
            "KEY_LEFTALT",
            "KEY_RIGHTALT",
            "KEY_LEFTMETA",
            "KEY_RIGHTMETA",
        ]
        tabs.addTab(self._create_key_list(modifier_keys), "Modifiers")

        # Tab 4: All keys
        all_keys = sorted([name for name in dir(ecodes) if name.startswith("KEY_")])
        tabs.addTab(self._create_key_list(all_keys), "All Keys")

        layout.addWidget(tabs)

        # Label for combo (optional)
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Label (optional):"))
        self.label_edit = QLineEdit()
        self.label_edit.setPlaceholderText("e.g., Copy, Paste, Save...")
        self.label_edit.textChanged.connect(self._update_preview)
        label_layout.addWidget(self.label_edit)
        layout.addLayout(label_layout)

        # Preview
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("Preview:"))
        self.preview_label = QLabel("(select a key)")
        self.preview_label.setStyleSheet(
            "font-weight: bold; color: #0af; padding: 4px; background: #333; border-radius: 4px;"
        )
        preview_layout.addWidget(self.preview_label)
        preview_layout.addStretch()
        layout.addLayout(preview_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        clear_btn = QPushButton("Clear Mapping")
        clear_btn.clicked.connect(self._clear_mapping)

        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _load_current_mapping(self):
        """Load current mapping into the dialog."""
        if self._current_mapping is None:
            return

        if isinstance(self._current_mapping, str):
            # Simple mapping
            self._main_key = self._current_mapping
            self._update_preview()
        elif isinstance(self._current_mapping, dict):
            # Combo mapping
            keys = self._current_mapping.get("keys", [])
            label = self._current_mapping.get("label", "")

            # Set modifiers
            for key in keys:
                if key in ("KEY_LEFTCTRL", "KEY_RIGHTCTRL"):
                    self.ctrl_check.setChecked(True)
                elif key in ("KEY_LEFTALT", "KEY_RIGHTALT"):
                    self.alt_check.setChecked(True)
                elif key in ("KEY_LEFTSHIFT", "KEY_RIGHTSHIFT"):
                    self.shift_check.setChecked(True)
                elif key in ("KEY_LEFTMETA", "KEY_RIGHTMETA"):
                    self.meta_check.setChecked(True)
                else:
                    # Non-modifier key is the main key
                    self._main_key = key

            self.label_edit.setText(label)
            self._update_preview()

    def _create_key_list(self, keys):
        """Create a searchable key list widget"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Search box
        search = QLineEdit()
        search.setPlaceholderText("Search keys...")
        layout.addWidget(search)

        # List
        list_widget = QListWidget()
        list_widget.addItems(keys)
        list_widget.itemDoubleClicked.connect(self._on_key_selected)
        list_widget.itemClicked.connect(self._on_key_selected)
        layout.addWidget(list_widget)

        # Search functionality
        def filter_list(text):
            list_widget.clear()
            filtered = [k for k in keys if text.upper() in k]
            list_widget.addItems(filtered)

        search.textChanged.connect(filter_list)

        widget.setLayout(layout)
        return widget

    def _on_key_selected(self, item):
        """Handle key selection"""
        self._main_key = item.text()
        self._update_preview()

    def _get_modifier_keys(self) -> list[str]:
        """Get list of selected modifier key codes."""
        mods = []
        if self.ctrl_check.isChecked():
            mods.append("KEY_LEFTCTRL")
        if self.alt_check.isChecked():
            mods.append("KEY_LEFTALT")
        if self.shift_check.isChecked():
            mods.append("KEY_LEFTSHIFT")
        if self.meta_check.isChecked():
            mods.append("KEY_LEFTMETA")
        return mods

    def _update_preview(self):
        """Update the preview label."""
        if not self._main_key:
            self.preview_label.setText("(select a key)")
            return

        mods = self._get_modifier_keys()
        label = self.label_edit.text().strip()

        if mods:
            # Combo key
            mod_names = []
            if self.ctrl_check.isChecked():
                mod_names.append("Ctrl")
            if self.alt_check.isChecked():
                mod_names.append("Alt")
            if self.shift_check.isChecked():
                mod_names.append("Shift")
            if self.meta_check.isChecked():
                mod_names.append("Super")

            key_name = self._main_key.replace("KEY_", "")
            combo_str = "+".join(mod_names + [key_name])

            if label:
                self.preview_label.setText(f"{combo_str} ({label})")
            else:
                self.preview_label.setText(combo_str)
        else:
            # Simple key
            key_name = self._main_key.replace("KEY_", "")
            if label:
                self.preview_label.setText(f"{key_name} ({label})")
            else:
                self.preview_label.setText(key_name)

    def accept(self):
        """Build the selected_key value and accept dialog."""
        if not self._main_key:
            self.selected_key = None
            super().accept()
            return

        mods = self._get_modifier_keys()
        label = self.label_edit.text().strip()

        if mods or label:
            # Return combo dict format
            keys = mods + [self._main_key]
            self.selected_key = {"keys": keys, "label": label}
        else:
            # Return simple string format
            self.selected_key = self._main_key

        super().accept()

    def _clear_mapping(self):
        """Clear the mapping"""
        self.selected_key = "KEY_RESERVED"
        super().accept()
