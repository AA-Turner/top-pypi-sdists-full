"""
CSSL Service Manager - Preferences Dialog.
Settings for scan interval, ports, theme, font, etc.
"""
import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
from typing import Optional
from .. import theme
from ..models import Preferences


def _prefs_path() -> Path:
    """Get preferences file path."""
    import os
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    else:
        base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
    return base / 'IncludeCPP' / 'service_manager_prefs.json'


def load_preferences() -> Preferences:
    """Load preferences from disk."""
    path = _prefs_path()
    if path.exists():
        try:
            with open(path, 'r') as f:
                return Preferences.from_dict(json.load(f))
        except Exception:
            pass
    return Preferences()


def save_preferences(prefs: Preferences):
    """Save preferences to disk."""
    path = _prefs_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(prefs.to_dict(), f, indent=2)


class PreferencesDialog(tk.Toplevel):
    """Preferences settings dialog."""

    def __init__(self, parent, preferences: Preferences):
        super().__init__(parent)
        self.title("Preferences")
        self.geometry("480x520")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.configure(bg=theme.BG)
        self.prefs = preferences
        self.result: Optional[Preferences] = None

        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        # Title
        tk.Label(self, text="Preferences", font=theme.FONT_TITLE,
                 bg=theme.BG, fg=theme.TEXT).pack(pady=(16, 8))

        # Notebook for sections
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=16, pady=8)

        # ── General Tab ──
        general = tk.Frame(notebook, bg=theme.SURFACE)
        notebook.add(general, text=" General ")

        self._add_spinbox(general, "Scan Interval (seconds):", "scan_interval",
                          1, 300, self.prefs.scan_interval)
        self._add_checkbox(general, "Auto-Scan on Startup:", "auto_scan",
                           self.prefs.auto_scan)
        self._add_checkbox(general, "Show Dead Processes:", "show_dead",
                           self.prefs.show_dead_processes)
        self._add_checkbox(general, "Confirm Before Kill:", "confirm_kill",
                           self.prefs.confirm_kill)
        self._add_checkbox(general, "Log IPC Messages:", "log_ipc",
                           self.prefs.log_ipc)

        # ── Network Tab ──
        network = tk.Frame(notebook, bg=theme.SURFACE)
        notebook.add(network, text=" Network ")

        self._add_spinbox(network, "IPC Port Start:", "port_start",
                          1024, 65535, self.prefs.ipc_port_start)
        self._add_spinbox(network, "IPC Port End:", "port_end",
                          1024, 65535, self.prefs.ipc_port_end)

        # ── Display Tab ──
        display = tk.Frame(notebook, bg=theme.SURFACE)
        notebook.add(display, text=" Display ")

        self._add_spinbox(display, "Font Size:", "font_size",
                          8, 24, self.prefs.font_size)
        self._add_spinbox(display, "Watch Poll Interval (ms):", "watch_interval",
                          100, 10000, self.prefs.watch_interval)
        self._add_spinbox(display, "Max History Entries:", "max_history",
                          10, 1000, self.prefs.max_history)

        # ── Buttons ──
        btn_frame = tk.Frame(self, bg=theme.BG)
        btn_frame.pack(fill="x", padx=16, pady=(8, 16))

        ttk.Button(btn_frame, text="Cancel", style="TButton",
                   command=self.destroy).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="Save", style="Accent.TButton",
                   command=self._save).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="Reset Defaults", style="TButton",
                   command=self._reset).pack(side="left")

    def _add_spinbox(self, parent, label: str, key: str,
                     min_val: int, max_val: int, current: int):
        row = tk.Frame(parent, bg=theme.SURFACE)
        row.pack(fill="x", padx=12, pady=6)

        tk.Label(row, text=label, font=theme.FONT, bg=theme.SURFACE,
                 fg=theme.TEXT, width=24, anchor="w").pack(side="left")

        var = tk.IntVar(value=current)
        spin = tk.Spinbox(row, from_=min_val, to=max_val, textvariable=var,
                          width=8, font=theme.FONT, bg=theme.CARD, fg=theme.TEXT,
                          buttonbackground=theme.CARD, insertbackground=theme.TEXT,
                          selectbackground=theme.HOVER)
        spin.pack(side="right")

        setattr(self, f"_var_{key}", var)

    def _add_checkbox(self, parent, label: str, key: str, current: bool):
        row = tk.Frame(parent, bg=theme.SURFACE)
        row.pack(fill="x", padx=12, pady=4)

        var = tk.BooleanVar(value=current)
        ttk.Checkbutton(row, text=label, variable=var).pack(side="left")

        setattr(self, f"_var_{key}", var)

    def _save(self):
        self.prefs.scan_interval = self._var_scan_interval.get()
        self.prefs.auto_scan = self._var_auto_scan.get()
        self.prefs.show_dead_processes = self._var_show_dead.get()
        self.prefs.confirm_kill = self._var_confirm_kill.get()
        self.prefs.log_ipc = self._var_log_ipc.get()
        self.prefs.ipc_port_start = self._var_port_start.get()
        self.prefs.ipc_port_end = self._var_port_end.get()
        self.prefs.font_size = self._var_font_size.get()
        self.prefs.watch_interval = self._var_watch_interval.get()
        self.prefs.max_history = self._var_max_history.get()

        save_preferences(self.prefs)
        self.result = self.prefs
        self.destroy()

    def _reset(self):
        defaults = Preferences()
        self._var_scan_interval.set(defaults.scan_interval)
        self._var_auto_scan.set(defaults.auto_scan)
        self._var_show_dead.set(defaults.show_dead_processes)
        self._var_confirm_kill.set(defaults.confirm_kill)
        self._var_log_ipc.set(defaults.log_ipc)
        self._var_port_start.set(defaults.ipc_port_start)
        self._var_port_end.set(defaults.ipc_port_end)
        self._var_font_size.set(defaults.font_size)
        self._var_watch_interval.set(defaults.watch_interval)
        self._var_max_history.set(defaults.max_history)
