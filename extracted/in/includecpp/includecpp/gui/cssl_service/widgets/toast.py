"""
CSSL Service Manager - Non-blocking toast notification popups.
"""
import tkinter as tk
from .. import theme


class Toast(tk.Toplevel):
    """A non-blocking notification popup that auto-dismisses."""

    _active_toasts = []
    _toast_offset = 0

    def __init__(self, parent, message: str, level: str = "info", duration: int = 3000):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        colors = {
            "info": (theme.CARD, theme.TEXT, theme.BLUE),
            "success": (theme.CARD, theme.TEXT, theme.GREEN),
            "warning": (theme.CARD, theme.TEXT, theme.YELLOW),
            "error": (theme.CARD, theme.TEXT, theme.RED),
        }
        bg, fg, accent = colors.get(level, colors["info"])

        self.configure(bg=accent)

        inner = tk.Frame(self, bg=bg, padx=1, pady=1)
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        # Icon
        icons = {"info": "\u2139", "success": "\u2713", "warning": "\u26A0", "error": "\u2717"}
        icon_text = icons.get(level, "\u2139")

        header = tk.Frame(inner, bg=bg)
        header.pack(fill="x", padx=8, pady=(6, 2))

        tk.Label(header, text=icon_text, font=(theme.FONT_FAMILY, 12), bg=bg, fg=accent
                 ).pack(side="left")
        tk.Label(header, text=level.upper(), font=theme.FONT_BOLD, bg=bg, fg=accent
                 ).pack(side="left", padx=(6, 0))

        # Close button
        close_btn = tk.Label(header, text="\u2715", font=theme.FONT_SMALL, bg=bg, fg=theme.TEXT_MUTED,
                             cursor="hand2")
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: self._dismiss())

        # Message
        tk.Label(inner, text=message, font=theme.FONT, bg=bg, fg=fg,
                 wraplength=300, justify="left", anchor="w"
                 ).pack(fill="x", padx=8, pady=(0, 8))

        # Position: top-right of parent, stacked
        self.update_idletasks()
        Toast._active_toasts.append(self)
        idx = len(Toast._active_toasts) - 1

        pw = parent.winfo_width()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        tw = self.winfo_reqwidth()

        x = px + pw - tw - 16
        y = py + 48 + idx * (self.winfo_reqheight() + 8)
        self.geometry(f"+{x}+{y}")

        # Auto-dismiss
        self._dismiss_id = self.after(duration, self._dismiss)

    def _dismiss(self):
        try:
            self.after_cancel(self._dismiss_id)
        except Exception:
            pass
        if self in Toast._active_toasts:
            Toast._active_toasts.remove(self)
        try:
            self.destroy()
        except Exception:
            pass


def show_toast(parent, message: str, level: str = "info", duration: int = 3000):
    """Convenience function to show a toast notification."""
    return Toast(parent, message, level, duration)
