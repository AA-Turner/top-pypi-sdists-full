"""
Menu Items

Data structures for menu entries.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..lcd.icons import Icon
    from .screen import Screen


@dataclass
class MenuItem:
    """
    Menu item definition.

    Can represent a simple action, a submenu, or a value display.
    """

    id: str
    label: str
    icon: "Icon | None" = None
    action: Callable[[], None] | None = None  # For leaf actions
    submenu: Callable[[], "Screen"] | None = None  # Factory for submenu screen
    value_getter: Callable[[], str] | None = None  # Display current value
    enabled: bool = True
    shortcut: str | None = None  # Key shortcut hint (e.g., "M1")

    def get_display_value(self) -> str | None:
        """Get current value to display, if any."""
        if self.value_getter:
            try:
                return self.value_getter()
            except Exception:
                return "?"
        return None

    def is_selectable(self) -> bool:
        """Check if item can be selected."""
        return self.enabled and (self.action is not None or self.submenu is not None)


@dataclass
class MenuSeparator:
    """Visual separator in menu."""

    label: str = ""  # Optional section label


@dataclass
class MenuGroup:
    """Group of related menu items."""

    title: str
    items: list[MenuItem] = field(default_factory=list)
