"""
CSSL GUI Builder - Data models for the scene and widgets.
"""

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from .constants import CsslWidgetType, WIDGET_REGISTRY


@dataclass
class WidgetModel:
    """Runtime data model for a single widget on the canvas."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    widget_type: CsslWidgetType = CsslWidgetType.BUTTON
    parent_id: Optional[str] = None
    x: int = 0
    y: int = 0
    width: int = 100
    height: int = 30
    properties: Dict[str, Any] = field(default_factory=dict)
    z_order: int = 0
    locked: bool = False
    visible: bool = True

    def get_property(self, prop_name: str, default: Any = None) -> Any:
        return self.properties.get(prop_name, default)

    def set_property(self, prop_name: str, value: Any) -> None:
        self.properties[prop_name] = value

    def clone(self) -> 'WidgetModel':
        return WidgetModel(
            id=str(uuid.uuid4())[:8],
            name=self.name + "_copy",
            widget_type=self.widget_type,
            parent_id=self.parent_id,
            x=self.x + 20,
            y=self.y + 20,
            width=self.width,
            height=self.height,
            properties=dict(self.properties),
            z_order=self.z_order,
            locked=self.locked,
            visible=self.visible,
        )


class SceneModel:
    """Central data model for the entire GUI design."""

    def __init__(self):
        self.widgets: Dict[str, WidgetModel] = {}
        self.window: Optional[WidgetModel] = None
        self.class_name: str = "MyApp"
        self.includes: List[str] = ["cssl-gui"]
        self.backend_code: str = ""
        self.preserved_constructor_lines: List[str] = []
        self.preserved_methods: List[str] = []
        self.preserved_destructor_body: str = ""
        self.source_file_path: str = ""
        self._name_counters: Dict[str, int] = {}
        self._listeners: List = []

    def add_listener(self, listener) -> None:
        """Add a change listener that gets called on model changes."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)

    def _notify(self, event: str, **kwargs) -> None:
        for listener in self._listeners:
            try:
                listener(event, **kwargs)
            except Exception:
                pass

    def add_widget(self, widget: WidgetModel) -> None:
        self.widgets[widget.id] = widget
        if widget.widget_type == CsslWidgetType.WIDGET:
            self.window = widget
        self._notify("widget_added", widget=widget)

    def remove_widget(self, widget_id: str) -> Optional[WidgetModel]:
        widget = self.widgets.pop(widget_id, None)
        if widget:
            # Also remove children
            children = self.get_children(widget_id)
            for child in children:
                self.remove_widget(child.id)
            self._notify("widget_removed", widget=widget)
        return widget

    def get_widget(self, widget_id: str) -> Optional[WidgetModel]:
        return self.widgets.get(widget_id)

    def get_children(self, parent_id: str) -> List[WidgetModel]:
        return [w for w in self.widgets.values() if w.parent_id == parent_id]

    def get_all_widgets_ordered(self) -> List[WidgetModel]:
        """Get all widgets in z-order, window first."""
        widgets = sorted(self.widgets.values(), key=lambda w: w.z_order)
        # Ensure window is always first
        if self.window:
            widgets = [self.window] + [w for w in widgets if w.id != self.window.id]
        return widgets

    def generate_name(self, widget_type: CsslWidgetType) -> str:
        """Generate a unique widget name like Button1, Label2, etc."""
        type_def = WIDGET_REGISTRY.get(widget_type)
        base_name = type_def.display_name.replace(" ", "") if type_def else "Widget"
        counter_key = base_name
        if counter_key not in self._name_counters:
            self._name_counters[counter_key] = 0
        self._name_counters[counter_key] += 1
        count = self._name_counters[counter_key]
        return f"{base_name}{count}"

    def rename_widget(self, widget_id: str, new_name: str) -> bool:
        """Rename a widget. Returns False if name already exists."""
        existing = [w.name for w in self.widgets.values() if w.id != widget_id]
        if new_name in existing:
            return False
        widget = self.widgets.get(widget_id)
        if widget:
            old_name = widget.name
            widget.name = new_name
            self._notify("widget_renamed", widget=widget, old_name=old_name)
            return True
        return False

    def is_name_available(self, name: str, exclude_id: str = "") -> bool:
        for w in self.widgets.values():
            if w.id != exclude_id and w.name == name:
                return False
        return True

    def clear(self) -> None:
        self.widgets.clear()
        self.window = None
        self._name_counters.clear()
        self.backend_code = ""
        self.preserved_constructor_lines.clear()
        self.preserved_methods.clear()
        self.preserved_destructor_body = ""
        self.source_file_path = ""
        self._notify("scene_cleared")

    def get_next_z_order(self) -> int:
        if not self.widgets:
            return 0
        return max(w.z_order for w in self.widgets.values()) + 1
