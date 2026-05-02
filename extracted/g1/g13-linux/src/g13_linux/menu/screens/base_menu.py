"""
Base Menu Screen

Reusable menu screen with navigation support.
"""

from ...lcd.canvas import Canvas
from ...lcd.fonts import FONT_4X6, FONT_5X7
from ..items import MenuItem
from ..screen import InputEvent, Screen


class MenuScreen(Screen):
    """
    Base class for menu screens with item navigation.

    Provides standard up/down navigation, selection, and back button handling.
    """

    # Display constants
    TITLE_HEIGHT = 10
    ITEM_HEIGHT = 8
    VISIBLE_ITEMS = 4
    SCROLL_INDICATOR_WIDTH = 4

    def __init__(self, manager, title: str, items: list[MenuItem]):
        """
        Initialize menu screen.

        Args:
            manager: ScreenManager instance
            title: Menu title
            items: List of menu items
        """
        super().__init__(manager)
        self.title = title
        self.items = items
        self.selected_index = 0
        self.scroll_offset = 0

    def on_input(self, event: InputEvent) -> bool:
        """Handle navigation input."""
        if event == InputEvent.STICK_UP:
            self._move_selection(-1)
            return True
        elif event == InputEvent.STICK_DOWN:
            self._move_selection(1)
            return True
        elif event == InputEvent.STICK_PRESS:
            self._select_current()
            return True
        elif event == InputEvent.BUTTON_BD:
            self.manager.pop()
            return True
        return False

    def _move_selection(self, delta: int):
        """
        Move selection by delta items.

        Args:
            delta: Direction to move (-1 up, +1 down)
        """
        if not self.items:
            return

        # Move selection with wrapping
        self.selected_index = (self.selected_index + delta) % len(self.items)

        # Adjust scroll to keep selection visible
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.VISIBLE_ITEMS:
            self.scroll_offset = self.selected_index - self.VISIBLE_ITEMS + 1

        self.mark_dirty()

    def _select_current(self):
        """Activate current selection."""
        if not self.items:
            return

        item = self.items[self.selected_index]

        if not item.enabled:
            return

        if item.submenu:
            # Open submenu
            submenu = item.submenu()
            self.manager.push(submenu)
        elif item.action:
            # Execute action
            item.action()
            self.mark_dirty()

    def _render_item(self, canvas: Canvas, item: MenuItem, y: int, is_selected: bool):
        """Render a single menu item."""
        on = not is_selected  # Invert text color for selected items

        if is_selected:
            canvas.draw_rect(
                0,
                y - 1,
                canvas.WIDTH - self.SCROLL_INDICATOR_WIDTH,
                self.ITEM_HEIGHT,
                filled=True,
            )

        x = 2
        if item.icon:
            x += 10

        label = f"[{item.label}]" if not item.enabled else item.label
        canvas.draw_text(x, y, label, FONT_4X6, on=on)

        value = item.get_display_value()
        if value:
            value_width = len(value) * 5
            vx = canvas.WIDTH - self.SCROLL_INDICATOR_WIDTH - value_width - 4
            canvas.draw_text(vx, y, value, FONT_4X6, on=on)

        if item.submenu:
            arrow_x = canvas.WIDTH - self.SCROLL_INDICATOR_WIDTH - 6
            canvas.draw_text(arrow_x, y, ">", FONT_4X6, on=on)

    def render(self, canvas: Canvas):
        """Render menu to canvas."""
        canvas.draw_text(0, 0, self.title.upper(), FONT_5X7)
        canvas.draw_hline(0, 9, canvas.WIDTH)

        y = self.TITLE_HEIGHT + 2
        for i in range(self.VISIBLE_ITEMS):
            item_idx = self.scroll_offset + i
            if item_idx >= len(self.items):
                break
            self._render_item(canvas, self.items[item_idx], y, item_idx == self.selected_index)
            y += self.ITEM_HEIGHT

        self._draw_scroll_indicators(canvas)

    def _draw_scroll_indicators(self, canvas: Canvas):
        """Draw scroll bar/indicators on right side."""
        if len(self.items) <= self.VISIBLE_ITEMS:
            return

        # Scroll area
        scroll_x = canvas.WIDTH - 3
        scroll_y = self.TITLE_HEIGHT + 2
        scroll_height = self.VISIBLE_ITEMS * self.ITEM_HEIGHT

        # Draw track
        canvas.draw_vline(scroll_x, scroll_y, scroll_height)

        # Draw thumb
        thumb_height = max(4, scroll_height * self.VISIBLE_ITEMS // len(self.items))
        thumb_offset = (
            (scroll_height - thumb_height)
            * self.scroll_offset
            // (len(self.items) - self.VISIBLE_ITEMS)
        )

        canvas.draw_rect(scroll_x - 1, scroll_y + thumb_offset, 3, thumb_height, filled=True)
