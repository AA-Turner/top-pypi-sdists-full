"""System tray icon for GhostPC.

Shows connection status and provides quick actions.
Green = connected, Red = disconnected, Yellow = processing.
"""

from __future__ import annotations

import threading
from collections.abc import Callable

from PIL import Image, ImageDraw


def create_icon_image(color: str, size: int = 64) -> Image.Image:
    """Create a simple colored circle icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 4, size - 4], fill=color, outline="white", width=2)
    # G letter in center
    draw.text((size // 2 - 6, size // 2 - 10), "G", fill="white")
    return img


class GhostTray:
    """System tray icon manager."""

    def __init__(
        self,
        on_pause: Callable | None = None,
        on_quit: Callable | None = None,
        dashboard_url: str | None = None,
    ):
        self.on_pause = on_pause
        self.on_quit = on_quit
        self.dashboard_url = dashboard_url
        self._icon = None
        self._connected = False
        self._processing = False

    def start(self) -> None:
        """Start the tray icon in a background thread."""
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        """Create and run the tray icon (blocks the thread)."""
        try:
            import pystray

            menu_items = [
                pystray.MenuItem("GhostPC", None, enabled=False),
                pystray.Menu.SEPARATOR,
            ]
            if self.dashboard_url:
                menu_items.append(pystray.MenuItem("Open Dashboard", self._handle_open_dashboard))
            menu_items.extend(
                [
                    pystray.MenuItem("Pause", self._handle_pause),
                    pystray.MenuItem("Quit", self._handle_quit),
                ]
            )
            menu = pystray.Menu(*menu_items)

            self._icon = pystray.Icon(
                "ghost-pc",
                create_icon_image("gray"),
                "GhostPC — Starting...",
                menu,
            )
            self._icon.run()
        except Exception:
            pass  # Tray not available (headless, WSL, etc.)

    def set_connected(self, connected: bool) -> None:
        """Update tray icon to show connection status."""
        self._connected = connected
        if self._icon:
            color = "green" if connected else "red"
            self._icon.icon = create_icon_image(color)
            self._icon.title = f"GhostPC — {'Connected' if connected else 'Disconnected'}"

    def set_processing(self, processing: bool) -> None:
        """Update tray icon to show processing status."""
        self._processing = processing
        if self._icon:
            if processing:
                self._icon.icon = create_icon_image("yellow")
                self._icon.title = "GhostPC — Processing..."
            elif self._connected:
                self.set_connected(True)

    def notify(self, message: str, title: str = "GhostPC") -> None:
        """Show a system notification."""
        if self._icon:
            try:
                self._icon.notify(message, title)
            except Exception:
                pass

    def stop(self) -> None:
        """Remove tray icon."""
        if self._icon:
            self._icon.stop()

    def _handle_open_dashboard(self, icon, item) -> None:
        if self.dashboard_url:
            import webbrowser

            webbrowser.open(self.dashboard_url)

    def _handle_pause(self, icon, item) -> None:
        if self.on_pause:
            self.on_pause()

    def _handle_quit(self, icon, item) -> None:
        if self.on_quit:
            self.on_quit()
        icon.stop()
