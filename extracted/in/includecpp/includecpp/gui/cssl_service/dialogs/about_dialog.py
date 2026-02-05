"""
CSSL Service Manager - About Dialog.
"""
import tkinter as tk
from .. import theme


class AboutDialog(tk.Toplevel):
    """About dialog with version and credits."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("About CSSL Service Manager")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=theme.BG)

        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        # Logo / Title
        tk.Label(self, text="\u2699", font=(theme.FONT_FAMILY, 40),
                 bg=theme.BG, fg=theme.ACCENT).pack(pady=(24, 4))

        tk.Label(self, text="CSSL Service Manager", font=theme.FONT_TITLE,
                 bg=theme.BG, fg=theme.TEXT).pack()

        tk.Label(self, text="v4.9.11", font=theme.FONT,
                 bg=theme.BG, fg=theme.ACCENT).pack(pady=(2, 12))

        # Description
        tk.Label(self, text="Professional runtime control & introspection tool\n"
                           "for CSSL and Python runtimes.",
                 font=theme.FONT, bg=theme.BG, fg=theme.TEXT_DIM,
                 justify="center").pack(pady=(0, 12))

        # Separator
        tk.Frame(self, bg=theme.BORDER, height=1).pack(fill="x", padx=40, pady=8)

        # Info
        info_frame = tk.Frame(self, bg=theme.BG)
        info_frame.pack(pady=4)

        infos = [
            ("Part of", "IncludeCPP"),
            ("License", "MIT"),
            ("Python", "3.8+"),
            ("Platform", "Windows / Linux / macOS"),
        ]
        for label, value in infos:
            row = tk.Frame(info_frame, bg=theme.BG)
            row.pack(fill="x")
            tk.Label(row, text=f"{label}:", font=theme.FONT_SMALL,
                     bg=theme.BG, fg=theme.TEXT_MUTED, width=12, anchor="e").pack(side="left")
            tk.Label(row, text=value, font=theme.FONT_SMALL,
                     bg=theme.BG, fg=theme.TEXT, anchor="w").pack(side="left", padx=(4, 0))

        # Link
        link = tk.Label(self, text="pypi.org/project/IncludeCPP",
                        font=theme.FONT_SMALL, bg=theme.BG, fg=theme.BLUE,
                        cursor="hand2")
        link.pack(pady=(12, 0))

        # Close button
        tk.Button(self, text="Close", command=self.destroy,
                  bg=theme.CARD, fg=theme.TEXT, font=theme.FONT,
                  relief="flat", padx=20, pady=4, cursor="hand2",
                  activebackground=theme.HOVER, activeforeground=theme.TEXT,
                  bd=0).pack(pady=(16, 16))
