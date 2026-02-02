"""
CSSL GUI Builder - Undo/Redo command pattern implementation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from .models import SceneModel, WidgetModel
from .constants import CsslWidgetType


class Command(ABC):
    """Base command for undo/redo system."""

    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...


class CommandHistory:
    """Linear undo/redo stack."""

    def __init__(self, max_size: int = 100):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._max_size = max_size
        self._listeners: List = []

    def add_listener(self, listener) -> None:
        if listener not in self._listeners:
            self._listeners.append(listener)

    def _notify(self) -> None:
        for listener in self._listeners:
            try:
                listener(self.can_undo(), self.can_redo())
            except Exception:
                pass

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()
        if len(self._undo_stack) > self._max_size:
            self._undo_stack.pop(0)
        self._notify()

    def undo(self) -> Optional[Command]:
        if not self._undo_stack:
            return None
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        self._notify()
        return command

    def redo(self) -> Optional[Command]:
        if not self._redo_stack:
            return None
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        self._notify()
        return command

    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    def clear(self) -> None:
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._notify()


class AddWidgetCommand(Command):
    """Add a widget to the scene."""

    def __init__(self, scene: SceneModel, widget: WidgetModel):
        self._scene = scene
        self._widget = widget

    def execute(self) -> None:
        self._scene.add_widget(self._widget)

    def undo(self) -> None:
        self._scene.remove_widget(self._widget.id)

    @property
    def description(self) -> str:
        return f"Add {self._widget.name}"


class RemoveWidgetCommand(Command):
    """Remove a widget from the scene."""

    def __init__(self, scene: SceneModel, widget_id: str):
        self._scene = scene
        self._widget_id = widget_id
        self._removed_widget: Optional[WidgetModel] = None
        self._removed_children: List[WidgetModel] = []

    def execute(self) -> None:
        self._removed_widget = self._scene.get_widget(self._widget_id)
        if self._removed_widget:
            self._removed_children = list(self._scene.get_children(self._widget_id))
            self._scene.remove_widget(self._widget_id)

    def undo(self) -> None:
        if self._removed_widget:
            self._scene.add_widget(self._removed_widget)
            for child in self._removed_children:
                self._scene.add_widget(child)

    @property
    def description(self) -> str:
        name = self._removed_widget.name if self._removed_widget else self._widget_id
        return f"Remove {name}"


class MoveWidgetCommand(Command):
    """Move a widget to a new position."""

    def __init__(self, scene: SceneModel, widget_id: str,
                 old_x: int, old_y: int, new_x: int, new_y: int):
        self._scene = scene
        self._widget_id = widget_id
        self._old_x = old_x
        self._old_y = old_y
        self._new_x = new_x
        self._new_y = new_y

    def execute(self) -> None:
        widget = self._scene.get_widget(self._widget_id)
        if widget:
            widget.x = self._new_x
            widget.y = self._new_y
            self._scene._notify("widget_moved", widget=widget)

    def undo(self) -> None:
        widget = self._scene.get_widget(self._widget_id)
        if widget:
            widget.x = self._old_x
            widget.y = self._old_y
            self._scene._notify("widget_moved", widget=widget)

    @property
    def description(self) -> str:
        return f"Move to ({self._new_x}, {self._new_y})"


class ResizeWidgetCommand(Command):
    """Resize a widget."""

    def __init__(self, scene: SceneModel, widget_id: str,
                 old_w: int, old_h: int, new_w: int, new_h: int,
                 old_x: int = 0, old_y: int = 0,
                 new_x: int = 0, new_y: int = 0):
        self._scene = scene
        self._widget_id = widget_id
        self._old_w = old_w
        self._old_h = old_h
        self._new_w = new_w
        self._new_h = new_h
        self._old_x = old_x
        self._old_y = old_y
        self._new_x = new_x
        self._new_y = new_y

    def execute(self) -> None:
        widget = self._scene.get_widget(self._widget_id)
        if widget:
            widget.width = self._new_w
            widget.height = self._new_h
            widget.x = self._new_x
            widget.y = self._new_y
            self._scene._notify("widget_resized", widget=widget)

    def undo(self) -> None:
        widget = self._scene.get_widget(self._widget_id)
        if widget:
            widget.width = self._old_w
            widget.height = self._old_h
            widget.x = self._old_x
            widget.y = self._old_y
            self._scene._notify("widget_resized", widget=widget)

    @property
    def description(self) -> str:
        return f"Resize to {self._new_w}x{self._new_h}"


class ChangePropertyCommand(Command):
    """Change a property value on a widget."""

    def __init__(self, scene: SceneModel, widget_id: str,
                 prop_name: str, old_value: Any, new_value: Any):
        self._scene = scene
        self._widget_id = widget_id
        self._prop_name = prop_name
        self._old_value = old_value
        self._new_value = new_value

    def execute(self) -> None:
        widget = self._scene.get_widget(self._widget_id)
        if widget:
            widget.set_property(self._prop_name, self._new_value)
            self._scene._notify("property_changed", widget=widget,
                                prop_name=self._prop_name)

    def undo(self) -> None:
        widget = self._scene.get_widget(self._widget_id)
        if widget:
            widget.set_property(self._prop_name, self._old_value)
            self._scene._notify("property_changed", widget=widget,
                                prop_name=self._prop_name)

    @property
    def description(self) -> str:
        return f"Change {self._prop_name}"


class RenameWidgetCommand(Command):
    """Rename a widget variable name."""

    def __init__(self, scene: SceneModel, widget_id: str,
                 old_name: str, new_name: str):
        self._scene = scene
        self._widget_id = widget_id
        self._old_name = old_name
        self._new_name = new_name

    def execute(self) -> None:
        self._scene.rename_widget(self._widget_id, self._new_name)

    def undo(self) -> None:
        self._scene.rename_widget(self._widget_id, self._old_name)

    @property
    def description(self) -> str:
        return f"Rename to {self._new_name}"


class BatchCommand(Command):
    """Group multiple commands into one undo/redo step."""

    def __init__(self, commands: List[Command], desc: str = "Batch"):
        self._commands = commands
        self._desc = desc

    def execute(self) -> None:
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        for cmd in reversed(self._commands):
            cmd.undo()

    @property
    def description(self) -> str:
        return self._desc
