"""
Idle Screen

Default status screen showing profile and quick info.
"""

from datetime import datetime

from ...lcd.canvas import Canvas
from ...lcd.fonts import FONT_4X6, FONT_5X7, FONT_8X8
from ..screen import InputEvent, Screen


class IdleScreen(Screen):
    """
    Default idle screen showing current profile and status.

    Shows:
    - Current profile name
    - Current time
    - M-key mode indicator
    - Optional: first few keybinds
    """

    def __init__(self, manager, profile_manager=None, settings_manager=None):
        """
        Initialize idle screen.

        Args:
            manager: ScreenManager instance
            profile_manager: Profile manager for current profile
            settings_manager: Settings manager for display preferences
        """
        super().__init__(manager)
        self.profile_manager = profile_manager
        self.settings_manager = settings_manager
        self._last_second = -1

    def on_input(self, event: InputEvent) -> bool:
        """
        Handle input - most events open menu.

        Args:
            event: Input event

        Returns:
            True if handled
        """
        # Stick press opens menu (handled by NavigationController)
        # Other events are not handled here
        return False

    def update(self, dt: float):
        """Update time display based on settings."""
        now = datetime.now()
        # Update every second if showing seconds, else every minute
        show_seconds = True
        if self.settings_manager:
            show_seconds = self.settings_manager.clock_show_seconds

        if show_seconds:
            if now.second != self._last_second:
                self._last_second = now.second
                self.mark_dirty()
        else:
            if now.minute != self._last_second:
                self._last_second = now.minute
                self.mark_dirty()

    def render(self, canvas: Canvas):
        """Render idle screen."""
        # Get current profile name
        profile_name = "No Profile"
        m_state = 1

        if self.profile_manager:
            if hasattr(self.profile_manager, "current"):
                profile = self.profile_manager.current
                if profile:
                    profile_name = getattr(profile, "name", "Unknown")
                    m_state = getattr(profile, "m_state", 1)
            elif hasattr(self.profile_manager, "current_name"):
                profile_name = self.profile_manager.current_name or "No Profile"

        # Header: Profile name and time
        canvas.draw_text(0, 0, profile_name[:18], FONT_5X7)

        # Time on right side (respects clock settings)
        time_str = self._format_time()
        time_width = len(time_str) * 6
        canvas.draw_text(canvas.WIDTH - time_width, 0, time_str, FONT_5X7)

        # Separator line
        canvas.draw_hline(0, 9, canvas.WIDTH)

        # Center area - could show keybinds or status
        if self.manager.daemon:
            # Show daemon status
            uptime = getattr(self.manager.daemon, "uptime", "0:00")
            key_count = getattr(self.manager.daemon, "key_count", 0)

            canvas.draw_text(4, 14, f"Uptime: {uptime}", FONT_4X6)
            canvas.draw_text(4, 22, f"Keys: {key_count:,}", FONT_4X6)
        else:
            # Show hint
            canvas.draw_text_centered(18, "Press stick for menu", FONT_4X6)

        # Footer: M-key indicators
        y = 35
        for i in range(1, 4):
            x = 10 + (i - 1) * 50
            if i == m_state:
                # Active mode - draw inverted
                canvas.draw_rect(x - 2, y - 1, 20, 8, filled=True)
                canvas.draw_text(x, y, f"M{i}", FONT_4X6, on=False)
            else:
                canvas.draw_text(x, y, f"M{i}", FONT_4X6)

    def _format_time(self) -> str:
        """Format current time based on settings."""
        now = datetime.now()

        # Get settings
        use_24h = True
        show_seconds = True
        if self.settings_manager:
            use_24h = self.settings_manager.clock_format == "24h"
            show_seconds = self.settings_manager.clock_show_seconds

        # Build format string
        if use_24h:
            fmt = "%H:%M:%S" if show_seconds else "%H:%M"
        else:
            fmt = "%I:%M:%S %p" if show_seconds else "%I:%M %p"

        return now.strftime(fmt)


class ClockScreen(Screen):
    """
    Large clock display screen.

    Alternative idle screen showing just the time in large font.
    """

    def __init__(self, manager, show_seconds: bool = True, show_date: bool = True):
        """
        Initialize clock screen.

        Args:
            manager: ScreenManager instance
            show_seconds: Whether to show seconds
            show_date: Whether to show date
        """
        super().__init__(manager)
        self.show_seconds = show_seconds
        self.show_date = show_date
        self._last_second = -1

    def on_input(self, event: InputEvent) -> bool:
        """Any input returns to previous screen."""
        if event == InputEvent.STICK_PRESS:
            self.manager.pop()
            return True
        return False

    def update(self, dt: float):
        """Update every second if showing seconds."""
        now = datetime.now()
        if self.show_seconds:
            if now.second != self._last_second:
                self._last_second = now.second
                self.mark_dirty()
        else:
            if now.minute != self._last_second:
                self._last_second = now.minute
                self.mark_dirty()

    def render(self, canvas: Canvas):
        """Render large clock."""
        now = datetime.now()

        # Time format
        if self.show_seconds:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%H:%M")

        # Draw centered time in large font
        canvas.draw_text_centered(12, time_str, FONT_8X8)

        # Date below
        if self.show_date:
            date_str = now.strftime("%a %b %d")
            canvas.draw_text_centered(30, date_str, FONT_5X7)
