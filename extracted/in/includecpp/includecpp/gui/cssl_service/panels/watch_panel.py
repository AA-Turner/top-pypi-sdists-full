"""
CSSL Service Manager - Watch Panel.
Live variable watch list with auto-polling and change detection.
"""
import tkinter as tk
from tkinter import ttk, simpledialog
import time
from typing import Dict, List, Optional
from .. import theme
from ..models import WatchVariable


class WatchPanel(ttk.Frame):
    """Watch panel for monitoring variable values in real-time."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._watches: Dict[str, WatchVariable] = {}
        self._poll_job = None
        self._polling = False
        self._build()

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  Watch", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM).pack(side="left")

        # Toolbar
        remove_btn = tk.Label(header, text="\u2212", font=(theme.FONT_FAMILY, 14),
                              bg=theme.CARD, fg=theme.RED, cursor="hand2", padx=4)
        remove_btn.pack(side="right")
        remove_btn.bind("<Button-1>", lambda e: self._remove_watch())

        add_btn = tk.Label(header, text="+", font=(theme.FONT_FAMILY, 14),
                           bg=theme.CARD, fg=theme.GREEN, cursor="hand2", padx=4)
        add_btn.pack(side="right")
        add_btn.bind("<Button-1>", lambda e: self._add_watch())

        # Poll toggle
        self.poll_btn = tk.Label(header, text="\u25B6 Poll", font=theme.FONT_SMALL,
                                 bg=theme.CARD, fg=theme.TEXT_MUTED, cursor="hand2", padx=4)
        self.poll_btn.pack(side="right")
        self.poll_btn.bind("<Button-1>", lambda e: self._toggle_polling())

        # ── Treeview ──
        tree_frame = ttk.Frame(self, style="Surface.TFrame")
        tree_frame.pack(fill="both", expand=True)

        columns = ("value", "type", "changes")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings",
                                  selectmode="browse", height=8)
        self.tree.heading("#0", text="Variable", anchor="w")
        self.tree.heading("value", text="Value", anchor="w")
        self.tree.heading("type", text="Type", anchor="w")
        self.tree.heading("changes", text="\u0394", anchor="e")
        self.tree.column("#0", width=100, minwidth=60)
        self.tree.column("value", width=140, minwidth=80)
        self.tree.column("type", width=70, minwidth=50)
        self.tree.column("changes", width=40, minwidth=30)

        # Tags for value changes
        self.tree.tag_configure("changed", background="#3d3000")
        self.tree.tag_configure("normal", background="")
        self.tree.tag_configure("error", foreground=theme.RED)

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Context menu
        self._menu = tk.Menu(self.tree, tearoff=0, bg=theme.CARD, fg=theme.TEXT,
                              activebackground=theme.BLUE, activeforeground=theme.TEXT)
        self._menu.add_command(label="Edit Value", command=self._edit_value)
        self._menu.add_command(label="Copy Value", command=self._copy_value)
        self._menu.add_command(label="View History", command=self._view_history)
        self._menu.add_separator()
        self._menu.add_command(label="Remove", command=self._remove_watch)
        self.tree.bind("<Button-3>", self._show_menu)

    # ── Watch Management ──────────────────────────────────────────
    def add_variable(self, name: str, runtime_id: str):
        """Add a variable to the watch list."""
        key = f"{runtime_id}:{name}"
        if key in self._watches:
            return  # Already watching

        watch = WatchVariable(name=name, runtime_id=runtime_id)
        self._watches[key] = watch
        self.tree.insert("", "end", iid=key, text=name,
                          values=("(pending)", "", "0"), tags=("normal",))
        self.app._log("info", "watch", f"Watching: {name}")

    def _add_watch(self):
        """Prompt user to add a variable."""
        name = simpledialog.askstring("Watch Variable",
                                       "Variable name or path:",
                                       parent=self)
        if name:
            # Use current console runtime or first available
            runtime_id = ""
            if hasattr(self.app, 'console_panel') and self.app.console_panel._connected_runtime:
                runtime_id = self.app.console_panel._connected_runtime
            elif self.app.runtimes:
                runtime_id = next(iter(self.app.runtimes))

            if runtime_id:
                self.add_variable(name, runtime_id)
            else:
                from ..widgets.toast import show_toast
                show_toast(self.app, "No runtime connected", "warning")

    def _remove_watch(self):
        """Remove selected variable from watch list."""
        sel = self.tree.selection()
        if sel:
            key = sel[0]
            if key in self._watches:
                del self._watches[key]
            self.tree.delete(key)

    # ── Polling ───────────────────────────────────────────────────
    def _toggle_polling(self):
        self._polling = not self._polling
        if self._polling:
            self.poll_btn.configure(text="\u25A0 Stop", fg=theme.GREEN)
            self._poll()
        else:
            self.poll_btn.configure(text="\u25B6 Poll", fg=theme.TEXT_MUTED)
            if self._poll_job:
                self.after_cancel(self._poll_job)
                self._poll_job = None

    def _poll(self):
        """Poll all watched variables."""
        if not self._polling:
            return

        for key, watch in self._watches.items():
            self._update_watch(key, watch)

        interval = self.app.preferences.watch_interval
        self._poll_job = self.after(interval, self._poll)

    def _update_watch(self, key: str, watch: WatchVariable):
        """Update a single watch variable value."""
        if not self.tree.exists(key):
            return

        # Try to get value from runtime
        info = self.app.runtimes.get(watch.runtime_id)
        if not info:
            self.tree.item(key, values=("(runtime gone)", "", str(watch.update_count)),
                           tags=("error",))
            return

        # For now, show simulated data (real IPC in future)
        # When IPC is connected, would use: ipc_client.get_variable(watch.name)
        new_value = watch.last_value  # placeholder
        new_type = watch.last_type

        if watch.update(new_value, new_type):
            # Value changed — flash highlight
            self.tree.item(key, values=(new_value[:100], new_type,
                                         str(watch.update_count)),
                           tags=("changed",))
            # Clear highlight after 1s
            self.after(1000, lambda k=key: (
                self.tree.item(k, tags=("normal",)) if self.tree.exists(k) else None
            ))
        else:
            self.tree.item(key, values=(watch.last_value[:100] if watch.last_value else "(pending)",
                                         watch.last_type, str(watch.update_count)),
                           tags=("normal",))

    # ── Context Menu Actions ──────────────────────────────────────
    def _show_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self._menu.tk_popup(event.x_root, event.y_root)

    def _edit_value(self):
        sel = self.tree.selection()
        if not sel:
            return
        key = sel[0]
        watch = self._watches.get(key)
        if watch:
            new_val = simpledialog.askstring("Edit Value",
                                              f"New value for '{watch.name}':",
                                              initialvalue=watch.last_value,
                                              parent=self)
            if new_val is not None:
                watch.last_value = new_val
                self.tree.item(key, values=(new_val[:100], watch.last_type,
                                             str(watch.update_count)))

    def _copy_value(self):
        sel = self.tree.selection()
        if sel:
            values = self.tree.item(sel[0], "values")
            if values:
                self.clipboard_clear()
                self.clipboard_append(values[0])

    def _view_history(self):
        sel = self.tree.selection()
        if not sel:
            return
        key = sel[0]
        watch = self._watches.get(key)
        if watch and watch.history:
            history_text = "\n".join(f"  {i+1}: {v}" for i, v in enumerate(watch.history[-20:]))
            tk.messagebox.showinfo(f"History: {watch.name}",
                                    f"Last {len(watch.history)} values:\n{history_text}")
        else:
            tk.messagebox.showinfo("History", "No history recorded yet.")

    def clear(self):
        """Clear all watches."""
        self._watches.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
