"""
CSSL Service Manager - Status bar with indicators and progress.
"""
import tkinter as tk
from tkinter import ttk
from .. import theme


class StatusBar(ttk.Frame):
    """Bottom status bar with status text, counters, and progress indicator."""

    def __init__(self, parent):
        super().__init__(parent, style="Surface.TFrame")
        self._build()

    def _build(self):
        # Left: status message
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var,
                                      style="Status.TLabel", width=30, anchor="w")
        self.status_label.pack(side="left", padx=(8, 4), pady=2)

        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=4, pady=4)

        # Runtime count
        self.runtime_var = tk.StringVar(value="Runtimes: 0")
        ttk.Label(self, textvariable=self.runtime_var,
                  style="Status.TLabel").pack(side="left", padx=4, pady=2)

        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=4, pady=4)

        # Connected count
        self.connected_var = tk.StringVar(value="Connected: 0")
        ttk.Label(self, textvariable=self.connected_var,
                  style="Status.TLabel").pack(side="left", padx=4, pady=2)

        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", padx=4, pady=4)

        # Scan indicator
        self.scan_var = tk.StringVar(value="")
        self.scan_label = ttk.Label(self, textvariable=self.scan_var,
                                    style="Yellow.TLabel", font=theme.FONT_SMALL)
        self.scan_label.pack(side="left", padx=4, pady=2)

        # Right: progress bar (hidden by default)
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=120)
        self._progress_visible = False

        # Right: version
        ttk.Label(self, text="CSSL Service v4.9.11", style="Muted.TLabel",
                  font=theme.FONT_SMALL).pack(side="right", padx=8, pady=2)

    def set_status(self, text: str):
        self.status_var.set(text)

    def set_runtime_count(self, count: int):
        self.runtime_var.set(f"Runtimes: {count}")

    def set_connected_count(self, count: int):
        self.connected_var.set(f"Connected: {count}")

    def start_progress(self, text: str = "Scanning..."):
        self.scan_var.set(text)
        if not self._progress_visible:
            self.progress.pack(side="right", padx=8, pady=2)
            self._progress_visible = True
        self.progress.start(15)

    def stop_progress(self):
        self.progress.stop()
        if self._progress_visible:
            self.progress.pack_forget()
            self._progress_visible = False
        self.scan_var.set("")

    def flash_status(self, text: str, color: str = "Green", duration: int = 3000):
        """Show temporary status message that auto-clears."""
        old = self.status_var.get()
        self.status_var.set(text)
        self.status_label.configure(style=f"{color}.TLabel" if color != "Status" else "Status.TLabel")
        self.after(duration, lambda: (
            self.status_var.set(old if self.status_var.get() == text else self.status_var.get()),
            self.status_label.configure(style="Status.TLabel")
        ))
