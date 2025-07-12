import sys
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

import click
from rich.console import Console
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from tecton.cli import printer


T = TypeVar("T")


class InteractiveMenu:
    """
    A reusable interactive menu component using Rich for polished CLI interfaces.

    Supports keyboard navigation with arrow keys, Enter to select, and Escape/Ctrl+C to cancel.
    Can display items in a flat list or organized by categories.

    Args:
        title: The menu title to display
        items: List of items to display in the menu (ignored if categories provided)
        categories: Dict mapping category names to lists of items (overrides items if provided)
        item_formatter: Function to format items for display (defaults to str())
        item_display_formatter: Function to format items with selection state (overrides item_formatter)
        category_formatter: Function to format category headers (defaults to bold styling)
        subtitle: Optional subtitle text
        allow_empty_selection: Whether to allow canceling without selection
        current_item: The currently active/selected item to highlight
        current_item_matcher: Function to compare items (defaults to ==)
        no_selection_message: Message to show when canceling with a current item
    """

    def __init__(
        self,
        title: str,
        items: Optional[List[T]] = None,
        categories: Optional[Dict[str, List[T]]] = None,
        item_formatter: Optional[Callable[[T], str]] = None,
        item_display_formatter: Optional[Callable[[T, bool], str]] = None,
        category_formatter: Optional[Callable[[str], Text]] = None,
        subtitle: Optional[str] = None,
        allow_empty_selection: bool = False,
        current_item: Optional[T] = None,
        current_item_matcher: Optional[Callable[[T, T], bool]] = None,
        no_selection_message: Optional[str] = None,
    ):
        self.title = title
        self.categories = categories
        self.item_formatter = item_formatter or str
        self.item_display_formatter = item_display_formatter
        self.category_formatter = category_formatter or (lambda cat: Text(f"{cat}:", style="bold"))
        self.subtitle = subtitle
        self.allow_empty_selection = allow_empty_selection
        self.current_item = current_item
        self.current_item_matcher = current_item_matcher or (lambda a, b: a == b)
        self.no_selection_message = no_selection_message
        self.selected_index = 0
        self.console = Console()

        if categories:
            self.items = []
            for category_items in categories.values():
                self.items.extend(category_items)
        else:
            self.items = items or []

    def _is_current_item(self, item: T) -> bool:
        """Check if the given item is the current item."""
        if self.current_item is None:
            return False
        return self.current_item_matcher(item, self.current_item)

    def _format_item(self, item: T, is_selected: bool) -> str:
        """Format an item for display, handling selection state."""
        if self.item_display_formatter:
            return self.item_display_formatter(item, is_selected)

        return self.item_formatter(item)

    def _render_flat_menu(self, menu_text: Text, selected_prefix: Text, not_selected_prefix: Text) -> None:
        """Render a flat menu without categories."""
        for i, item in enumerate(self.items):
            is_selected = i == self.selected_index
            is_current = self._is_current_item(item)
            item_text = self._format_item(item, is_selected)

            if is_selected:
                style = "bold yellow" if is_current else "bold green"
                styled_text = Text(item_text, style=style)
                menu_text.append(Text.assemble(selected_prefix, styled_text))
            else:
                style = "yellow" if is_current else None
                styled_text = Text(item_text, style=style)
                menu_text.append(Text.assemble(not_selected_prefix, styled_text))

            if i < len(self.items) - 1:
                menu_text.append("\n")

    def _render_categorized_menu(self, menu_text: Text, selected_prefix: Text, not_selected_prefix: Text) -> None:
        """Render a categorized menu with section headers."""
        current_index = 0

        for category_name, category_items in self.categories.items():
            if not category_items:
                continue

            category_header = self.category_formatter(category_name)
            menu_text.append(category_header)
            menu_text.append("\n")

            for item in category_items:
                is_selected = current_index == self.selected_index
                is_current = self._is_current_item(item)
                item_text = self._format_item(item, is_selected)

                if is_selected:
                    style = "bold yellow" if is_current else "bold green"
                    styled_text = Text(item_text, style=style)
                    menu_text.append(Text.assemble(selected_prefix, styled_text))
                else:
                    style = "yellow" if is_current else None
                    styled_text = Text(item_text, style=style)
                    menu_text.append(Text.assemble(not_selected_prefix, styled_text))

                menu_text.append("\n")
                current_index += 1

            menu_text.append("\n")

    @property
    def _render_menu(self) -> Group:
        """Create the menu display with current selection."""
        menu_text = Text()

        if self.subtitle:
            if isinstance(self.subtitle, Text):
                menu_text.append(self.subtitle)
            else:
                menu_text.append(str(self.subtitle))
            menu_text.append("\n\n")

        selected_prefix = Text("▶ ", style="bold green")
        not_selected_prefix = Text("  ")

        if self.categories:
            self._render_categorized_menu(menu_text, selected_prefix, not_selected_prefix)
        else:
            self._render_flat_menu(menu_text, selected_prefix, not_selected_prefix)

        instructions = "Use ↑/↓ to navigate, Enter to select"
        if self.allow_empty_selection:
            instructions += ", Escape to cancel"
        menu_text.append(Text(instructions, style="dim italic"))

        panel = Panel(
            menu_text,
            title=Text(self.title, style="bold white"),
            border_style="white",
            padding=(0, 1),
        )

        return Group(panel)

    def show(self) -> Optional[T]:
        """
        Display the menu and return the selected item.

        Returns:
            The selected item, or None if canceled (when allow_empty_selection=True)
        """
        if not self.items:
            printer.safe_print("No items available to select from.")
            return None

        result = None
        canceled = False

        try:
            with Live(self._render_menu, auto_refresh=False, screen=False) as live:
                while True:
                    key = click.getchar()
                    if key == "\r":
                        result = self.items[self.selected_index]
                        break
                    elif key in ("\x1b", "\x03"):
                        if self.allow_empty_selection:
                            canceled = True
                            break
                        else:
                            sys.exit(1)
                    elif key == "\x1b[A":
                        self.selected_index = (self.selected_index - 1) % len(self.items)
                        live.update(self._render_menu, refresh=True)
                    elif key == "\x1b[B":
                        self.selected_index = (self.selected_index + 1) % len(self.items)
                        live.update(self._render_menu, refresh=True)

        except (KeyboardInterrupt, EOFError):
            if self.allow_empty_selection:
                canceled = True
            else:
                sys.exit(1)

        if canceled and self.current_item and self.no_selection_message:
            printer.safe_print(self.no_selection_message)

        return result


def create_workspace_menu(workspaces: List, current_workspace: Optional[str] = None) -> InteractiveMenu:
    """
    Create a specialized menu for workspace selection with enhanced current workspace display.

    Args:
        workspaces: List of workspace objects with .name and .capabilities attributes
        current_workspace: Name of the currently selected workspace

    Returns:
        Configured InteractiveMenu for workspace selection
    """
    live_workspaces = [w for w in workspaces if w.capabilities.materializable]
    dev_workspaces = [w for w in workspaces if not w.capabilities.materializable]

    categories = {}
    if live_workspaces:
        categories["Live Workspaces"] = live_workspaces
    if dev_workspaces:
        categories["Development Workspaces"] = dev_workspaces

    def format_workspace(workspace, is_selected: bool = False) -> str:
        """Format workspace for display with current indicator."""
        is_current = workspace.name == current_workspace

        if is_current:
            return f"★ {workspace.name} [CURRENT]"
        else:
            return f"{workspace.name}"

    def format_category(category_name: str) -> Text:
        """Format category headers with appropriate styling."""
        if category_name == "Live Workspaces":
            return Text(f"{category_name}:", style="bold blue")
        elif category_name == "Development Workspaces":
            return Text(f"{category_name}:", style="bold orange3")
        else:
            return Text(f"{category_name}:", style="bold")

    subtitle = Text("Choose a workspace to switch to:")
    if current_workspace:
        subtitle.append(" - Currently in: ", style="dim italic")
        subtitle.append(current_workspace, style="bold yellow")

    no_selection_msg = None
    if current_workspace:
        no_selection_msg = f"Staying in current workspace: {current_workspace}"
    else:
        no_selection_msg = "No workspace selected."

    return InteractiveMenu(
        title="Select Tecton Workspace",
        categories=categories,
        item_display_formatter=format_workspace,
        category_formatter=format_category,
        subtitle=subtitle,
        allow_empty_selection=True,
        current_item=current_workspace,
        current_item_matcher=lambda ws, current_name: ws.name == current_name,
        no_selection_message=no_selection_msg,
    )
