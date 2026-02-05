"""
CSSL Service Manager - Output / Logs Panel.
Timestamped log entries with severity filtering.
"""
import tkinter as tk
from tkinter import ttk
import time
from typing import List
from .. import theme
from ..widgets.syntax_text import SyntaxText
from ..models import LogEntry


class OutputPanel(ttk.Frame):
    """Output/logs panel with severity filtering and timestamped entries."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._entries: List[LogEntry] = []
        self._filter = "all"
        self._build()

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  Output / Logs", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM).pack(side="left")

        # Filter buttons
        btn_frame = tk.Frame(header, bg=theme.CARD)
        btn_frame.pack(side="left", padx=(12, 0))

        self._filter_btns = {}
        filters = [
            ("All", "all", theme.TEXT_DIM),
            ("Info", "info", theme.BLUE),
            ("Warn", "warn", theme.YELLOW),
            ("Error", "error", theme.RED),
        ]
        for label, key, color in filters:
            btn = tk.Label(btn_frame, text=f" {label} ", font=theme.FONT_SMALL,
                           bg=theme.CARD if key != "all" else theme.HOVER,
                           fg=color, cursor="hand2", padx=2)
            btn.pack(side="left", padx=1)
            btn.bind("<Button-1>", lambda e, k=key: self._set_filter(k))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=theme.HOVER))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.configure(
                bg=theme.HOVER if k == self._filter else theme.CARD))
            self._filter_btns[key] = btn

        # Clear button
        clear_btn = tk.Label(header, text="\u2715 Clear", font=theme.FONT_SMALL,
                             bg=theme.CARD, fg=theme.TEXT_MUTED, cursor="hand2", padx=6)
        clear_btn.pack(side="right")
        clear_btn.bind("<Button-1>", lambda e: self.clear())
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(fg=theme.TEXT))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(fg=theme.TEXT_MUTED))

        # Export button
        export_btn = tk.Label(header, text="\u2B07 Export", font=theme.FONT_SMALL,
                              bg=theme.CARD, fg=theme.TEXT_MUTED, cursor="hand2", padx=6)
        export_btn.pack(side="right")
        export_btn.bind("<Button-1>", lambda e: self.app.action_export("logs"))

        # ── Output text ──
        output_frame = ttk.Frame(self, style="Surface.TFrame")
        output_frame.pack(fill="both", expand=True)

        self.output = SyntaxText(output_frame, readonly=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical",
                                   command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)

        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Context menu
        self._menu = tk.Menu(self.output, tearoff=0, bg=theme.CARD, fg=theme.TEXT,
                              activebackground=theme.BLUE, activeforeground=theme.TEXT)
        self._menu.add_command(label="Copy", command=self._copy_selection)
        self._menu.add_command(label="Copy All", command=self._copy_all)
        self._menu.add_separator()
        self._menu.add_command(label="Clear", command=self.clear)
        self._menu.add_command(label="Export...", command=lambda: self.app.action_export("logs"))
        self.output.bind("<Button-3>", lambda e: self._menu.tk_popup(e.x_root, e.y_root))

    # ── Log Entry Management ──────────────────────────────────────
    def add_entry(self, entry: LogEntry):
        """Add a log entry to the output."""
        self._entries.append(entry)

        # Check filter
        if self._filter != "all" and entry.level != self._filter:
            return

        self._render_entry(entry)

    def _render_entry(self, entry: LogEntry):
        """Render a single log entry."""
        # Tag mapping
        level_tags = {
            "info": "info",
            "warn": "warning",
            "error": "error",
            "debug": "dim",
            "success": "success",
        }
        tag = level_tags.get(entry.level, "output")

        # Level indicator
        level_icons = {
            "info": "\u2139",
            "warn": "\u26A0",
            "error": "\u2717",
            "debug": "\u2022",
            "success": "\u2713",
        }
        icon = level_icons.get(entry.level, "\u2022")

        self.output.append_text(f"[{entry.time_str}] ", "timestamp")
        self.output.append_text(f"{icon} ", tag)
        if entry.source:
            self.output.append_text(f"[{entry.source}] ", "dim")
        self.output.append_line(entry.message, tag)

    def _set_filter(self, filter_key: str):
        """Set the log level filter."""
        self._filter = filter_key

        # Update button highlights
        for key, btn in self._filter_btns.items():
            btn.configure(bg=theme.HOVER if key == filter_key else theme.CARD)

        # Re-render
        self.output.clear()
        for entry in self._entries:
            if filter_key == "all" or entry.level == filter_key:
                self._render_entry(entry)

    def clear(self):
        """Clear all log entries."""
        self._entries.clear()
        self.output.clear()

    def _copy_selection(self):
        try:
            text = self.output.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(text)
        except tk.TclError:
            pass

    def _copy_all(self):
        text = self.output.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)

    def get_entries(self) -> List[LogEntry]:
        return list(self._entries)
