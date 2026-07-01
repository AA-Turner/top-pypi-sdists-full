"""Shared overlay behavior for OptionList-based popup widgets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widgets import OptionList

if TYPE_CHECKING:
    from textual.events import Key


class OverlayMixin(OptionList):
    """Base class for popup OptionList overlays toggled via CSS class.

    Provides shared navigation, visibility, and dismissal behavior.
    Subclasses override ``select_highlighted`` for selection actions
    and ``move_highlight`` for wrapping navigation.
    """

    @property
    def is_visible(self) -> bool:
        return self.has_class("-visible")

    def hide(self) -> None:
        """Hide the overlay."""
        self.remove_class("-visible")

    def move_highlight(self, direction: int) -> None:
        """Move highlight up (-1) or down (+1), clamping at bounds."""
        if self.option_count == 0:
            return
        current = self.highlighted if self.highlighted is not None else 0
        self.highlighted = max(0, min(current + direction, self.option_count - 1))

    def select_highlighted(self) -> bool:
        """Select the highlighted option. Returns True if handled.

        Default returns False (read-only overlays). Override in
        subclasses that support selection.
        """
        return False

    def on_key(self, event: Key) -> bool:  # noqa: ARG002
        """Handle custom key events routed from the composer or app.

        Most overlays don't need custom key handling beyond navigation and
        selection, so the default is unhandled.
        """
        return False
