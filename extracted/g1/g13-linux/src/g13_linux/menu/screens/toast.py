"""
Toast Screen

Temporary notification overlay.
"""

from ...lcd.canvas import Canvas
from ...lcd.fonts import FONT_4X6
from ...lcd.icons import Icon
from ..screen import InputEvent, Screen


class ToastScreen(Screen):
    """
    Toast notification overlay.

    Displays a temporary message, dismissed by any input or timeout.
    """

    def __init__(self, manager, message: str, icon: Icon | None = None):
        """
        Initialize toast.

        Args:
            manager: ScreenManager instance
            message: Message to display
            icon: Optional icon to show
        """
        super().__init__(manager)
        self.message = message
        self.icon = icon

    def on_input(self, event: InputEvent) -> bool:
        """Any input dismisses toast."""
        self.manager.dismiss_overlay()
        return True

    def render(self, canvas: Canvas):
        """Render toast notification."""
        # Calculate box dimensions
        msg_width = len(self.message) * 5  # Approximate width with small font
        box_padding = 8
        box_width = min(msg_width + box_padding * 2, canvas.WIDTH - 10)
        box_height = 18
        box_x = (canvas.WIDTH - box_width) // 2
        box_y = (canvas.HEIGHT - box_height) // 2

        # Clear area (draw black box)
        canvas.draw_rect(box_x, box_y, box_width, box_height, filled=True)

        # Draw border (inverts to white on black background)
        canvas.draw_rect(
            box_x + 1, box_y + 1, box_width - 2, box_height - 2, filled=False, on=False
        )

        # Draw text centered in box (inverted - black on white)
        text_x = box_x + box_padding
        text_y = box_y + (box_height - 6) // 2

        if self.icon:
            canvas.draw_icon(text_x, text_y - 1, self.icon, on=False)
            text_x += 10

        canvas.draw_text(text_x, text_y, self.message, FONT_4X6, on=False)


class ConfirmDialog(Screen):
    """
    Confirmation dialog.

    Shows a yes/no prompt.
    """

    def __init__(self, manager, message: str, on_confirm: callable, on_cancel: callable = None):
        """
        Initialize confirmation dialog.

        Args:
            manager: ScreenManager instance
            message: Question to ask
            on_confirm: Callback when confirmed
            on_cancel: Callback when cancelled (optional)
        """
        super().__init__(manager)
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.selected = 0  # 0 = No, 1 = Yes

    def on_input(self, event: InputEvent) -> bool:
        """Handle input."""
        if event in (InputEvent.STICK_LEFT, InputEvent.STICK_RIGHT):
            self.selected = 1 - self.selected
            self.mark_dirty()
            return True
        elif event == InputEvent.STICK_PRESS:
            if self.selected == 1:
                self.on_confirm()
            elif self.on_cancel:
                self.on_cancel()
            self.manager.dismiss_overlay()
            return True
        elif event == InputEvent.BUTTON_BD:
            if self.on_cancel:
                self.on_cancel()
            self.manager.dismiss_overlay()
            return True
        return False

    def render(self, canvas: Canvas):
        """Render confirmation dialog."""
        # Box dimensions
        box_width = 140
        box_height = 30
        box_x = (canvas.WIDTH - box_width) // 2
        box_y = (canvas.HEIGHT - box_height) // 2

        # Draw box
        canvas.draw_rect(box_x, box_y, box_width, box_height, filled=True)
        canvas.draw_rect(
            box_x + 1, box_y + 1, box_width - 2, box_height - 2, filled=False, on=False
        )

        # Draw message
        canvas.draw_text(box_x + 5, box_y + 4, self.message[:20], FONT_4X6, on=False)

        # Draw buttons
        btn_y = box_y + 18
        btn_width = 30

        # No button
        no_x = box_x + 30
        if self.selected == 0:
            canvas.draw_rect(no_x - 2, btn_y - 2, btn_width, 10, filled=False, on=False)
        canvas.draw_text(no_x, btn_y, "No", FONT_4X6, on=False)

        # Yes button
        yes_x = box_x + 80
        if self.selected == 1:
            canvas.draw_rect(yes_x - 2, btn_y - 2, btn_width, 10, filled=False, on=False)
        canvas.draw_text(yes_x, btn_y, "Yes", FONT_4X6, on=False)
