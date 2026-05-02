"""
Info Screen

System information display.
"""

from ...lcd.canvas import Canvas
from ...lcd.fonts import FONT_4X6, FONT_5X7
from ..screen import InputEvent, Screen


class InfoScreen(Screen):
    """
    System information screen.

    Shows:
    - Version
    - Profile name
    - Uptime
    - Key count
    """

    VERSION = "1.0.0"

    def __init__(self, manager):
        """
        Initialize info screen.

        Args:
            manager: ScreenManager instance
        """
        super().__init__(manager)
        self.daemon = getattr(manager, "daemon", None)
        self.profile_manager = getattr(manager, "profile_manager", None)

    def on_input(self, event: InputEvent) -> bool:
        """Any press returns to menu."""
        if event in (InputEvent.BUTTON_BD, InputEvent.STICK_PRESS):
            self.manager.pop()
            return True
        return False

    def render(self, canvas: Canvas):
        """Render info screen."""
        # Title
        canvas.draw_text(0, 0, f"G13 Linux v{self.VERSION}", FONT_5X7)
        canvas.draw_hline(0, 9, canvas.WIDTH)

        y = 14

        # Profile
        profile_name = "None"
        if self.profile_manager:
            if hasattr(self.profile_manager, "current_name"):
                profile_name = self.profile_manager.current_name or "None"
            elif hasattr(self.profile_manager, "current"):
                profile = self.profile_manager.current
                if profile:
                    profile_name = getattr(profile, "name", "Unknown")

        canvas.draw_text(0, y, f"Profile: {profile_name[:12]}", FONT_4X6)
        y += 8

        # Uptime
        uptime = "N/A"
        if self.daemon and hasattr(self.daemon, "uptime"):
            uptime = self.daemon.uptime
        canvas.draw_text(0, y, f"Uptime: {uptime}", FONT_4X6)
        y += 8

        # Key count
        keys = 0
        if self.daemon and hasattr(self.daemon, "key_count"):
            keys = self.daemon.key_count
        canvas.draw_text(0, y, f"Keys: {keys:,}", FONT_4X6)
        y += 8

        # LED status
        led = getattr(self.manager, "led_controller", None)
        if led:
            color = led.current_color.to_hex()
            effect = led.current_effect.value if led.current_effect else "None"
            canvas.draw_text(0, y, f"LED: {color} ({effect})", FONT_4X6)
