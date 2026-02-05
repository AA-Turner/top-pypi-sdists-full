"""
CSSL Service Manager - Instances Panel.
Left panel showing discovered runtimes as a treeview with context menu.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from .. import theme
from ..models import RuntimeInfo


class InstancesPanel(ttk.Frame):
    """Left panel with discovered runtimes tree + search + context menu."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._selected_id: Optional[str] = None
        self._build()

    def _build(self):
        # ── Search/Filter bar ──
        search_frame = tk.Frame(self, bg=theme.SURFACE)
        search_frame.pack(fill="x", padx=4, pady=(4, 2))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._filter())

        search_icon = tk.Label(search_frame, text="\U0001F50D", bg=theme.SURFACE,
                               fg=theme.TEXT_MUTED, font=theme.FONT_SMALL)
        search_icon.pack(side="left", padx=(2, 0))

        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                       font=theme.FONT_SMALL)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=4)

        clear_btn = tk.Label(search_frame, text="\u2715", bg=theme.SURFACE,
                             fg=theme.TEXT_MUTED, font=theme.FONT_SMALL, cursor="hand2")
        clear_btn.pack(side="right", padx=2)
        clear_btn.bind("<Button-1>", lambda e: self.search_var.set(""))

        # ── Toolbar ──
        toolbar = tk.Frame(self, bg=theme.SURFACE)
        toolbar.pack(fill="x", padx=4, pady=2)

        scan_btn = tk.Label(toolbar, text="\u21BB Scan", font=theme.FONT_SMALL,
                            bg=theme.CARD, fg=theme.BLUE, padx=6, pady=1,
                            cursor="hand2", relief="flat")
        scan_btn.pack(side="left", padx=(0, 4))
        scan_btn.bind("<Button-1>", lambda e: self.app.action_scan_all())
        scan_btn.bind("<Enter>", lambda e: scan_btn.configure(bg=theme.HOVER))
        scan_btn.bind("<Leave>", lambda e: scan_btn.configure(bg=theme.CARD))

        clear_btn2 = tk.Label(toolbar, text="\u2715 Clear", font=theme.FONT_SMALL,
                              bg=theme.CARD, fg=theme.TEXT_MUTED, padx=6, pady=1,
                              cursor="hand2")
        clear_btn2.pack(side="left", padx=2)
        clear_btn2.bind("<Button-1>", lambda e: self.app.action_clear_discovered())
        clear_btn2.bind("<Enter>", lambda e: clear_btn2.configure(bg=theme.HOVER))
        clear_btn2.bind("<Leave>", lambda e: clear_btn2.configure(bg=theme.CARD))

        # Count label
        self.count_label = tk.Label(toolbar, text="0 found", font=theme.FONT_SMALL,
                                    bg=theme.SURFACE, fg=theme.TEXT_MUTED)
        self.count_label.pack(side="right")

        # ── Treeview ──
        tree_frame = ttk.Frame(self, style="Surface.TFrame")
        tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        columns = ("status", "pid", "mem", "cpu")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings",
                                  selectmode="browse", height=20)

        self.tree.heading("#0", text="Name", anchor="w")
        self.tree.heading("status", text="Status", anchor="w")
        self.tree.heading("pid", text="PID", anchor="e")
        self.tree.heading("mem", text="Memory", anchor="e")
        self.tree.heading("cpu", text="CPU", anchor="e")

        self.tree.column("#0", width=140, minwidth=100)
        self.tree.column("status", width=70, minwidth=50)
        self.tree.column("pid", width=50, minwidth=40)
        self.tree.column("mem", width=60, minwidth=45)
        self.tree.column("cpu", width=45, minwidth=35)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ── Tree tags for coloring ──
        self.tree.tag_configure("running", foreground=theme.GREEN)
        self.tree.tag_configure("attached", foreground=theme.BLUE)
        self.tree.tag_configure("scanning", foreground=theme.YELLOW)
        self.tree.tag_configure("discovered", foreground=theme.TEXT_DIM)
        self.tree.tag_configure("dead", foreground=theme.RED)
        self.tree.tag_configure("cssl", foreground=theme.ACCENT)
        self.tree.tag_configure("python", foreground=theme.CYAN)

        # ── Bindings ──
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Button-3>", self._on_right_click)

        # ── Context Menu ──
        self._context_menu = self._build_context_menu()

    def _build_context_menu(self) -> tk.Menu:
        menu = tk.Menu(self.tree, tearoff=0, bg=theme.CARD, fg=theme.TEXT,
                       activebackground=theme.BLUE, activeforeground=theme.TEXT,
                       borderwidth=1, font=theme.FONT)

        menu.add_command(label="\u25B6  Catch in CSSL", command=self._ctx_catch,
                         font=(theme.FONT_FAMILY, theme.FONT_SIZE, "bold"))
        menu.add_separator()
        menu.add_command(label="\u2318  Scan API", command=self._ctx_scan_api)
        menu.add_command(label="\u2261  Get API", command=self._ctx_get_api)
        menu.add_separator()
        menu.add_command(label="\u2630  Inspect Memory", command=self._ctx_memory)
        menu.add_command(label="\u25CE  Watch Variables", command=self._ctx_watch)
        menu.add_command(label="\u2197  Metrics", command=self._ctx_metrics)
        menu.add_separator()
        menu.add_command(label="\u2398  Copy PID", command=self._ctx_copy_pid)
        menu.add_command(label="\u2398  Copy Details", command=self._ctx_copy_details)
        menu.add_separator()
        menu.add_command(label="\u2716  Detach", command=self._ctx_detach)
        menu.add_command(label="\u2620  Kill Process", command=self._ctx_kill,
                         foreground=theme.RED)
        return menu

    # ── Update ────────────────────────────────────────────────────
    def update_runtimes(self, runtimes: Dict[str, RuntimeInfo]):
        """Refresh the treeview with current runtime data."""
        # Preserve selection
        sel = self._selected_id

        # Get search filter
        query = self.search_var.get().strip().lower()

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        count = 0
        for rid, info in runtimes.items():
            # Filter by search
            if query:
                searchable = f"{info.name} {info.pid} {info.language} {info.cmdline}".lower()
                if query not in searchable:
                    continue

            # Status indicator
            dot = {
                "running": "\u25CF",
                "attached": "\u25CF",
                "scanning": "\u25D4",
                "discovered": "\u25CB",
                "dead": "\u25CF",
            }.get(info.status, "\u25CB")

            # Language tag
            tag = info.status
            if info.language == "CSSL" or info.language == "Python/CSSL":
                tag = "cssl"
            elif info.status == "discovered":
                tag = "python"

            # Insert into tree
            display_name = f"{dot}  {info.name}"
            self.tree.insert("", "end", iid=rid, text=display_name,
                             values=(info.status.capitalize(),
                                     str(info.pid),
                                     info.memory_str,
                                     f"{info.cpu_pct:.1f}%"),
                             tags=(tag,))
            count += 1

        self.count_label.configure(text=f"{count} found")

        # Restore selection
        if sel and self.tree.exists(sel):
            self.tree.selection_set(sel)

    def _filter(self):
        """Re-filter tree based on search."""
        if hasattr(self.app, 'runtimes'):
            self.update_runtimes(self.app.runtimes)

    # ── Events ────────────────────────────────────────────────────
    def _on_select(self, event):
        selection = self.tree.selection()
        self._selected_id = selection[0] if selection else None

    def _on_double_click(self, event):
        if self._selected_id:
            self.app.action_catch(self._selected_id)

    def _on_right_click(self, event):
        # Select the item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self._selected_id = item

            # Enable/disable Get API based on scan status
            info = self.app.runtimes.get(item)
            if info and info.api_scanned:
                self._context_menu.entryconfigure(3, state="normal")
            else:
                self._context_menu.entryconfigure(3, state="disabled")

            self._context_menu.tk_popup(event.x_root, event.y_root)

    # ── Context menu actions ──────────────────────────────────────
    def _ctx_catch(self):
        if self._selected_id:
            self.app.action_catch(self._selected_id)

    def _ctx_scan_api(self):
        if self._selected_id:
            self.app.action_scan_api(self._selected_id)

    def _ctx_get_api(self):
        if self._selected_id:
            self.app.action_get_api(self._selected_id)

    def _ctx_memory(self):
        if self._selected_id:
            self.app.action_inspect_memory(self._selected_id)

    def _ctx_watch(self):
        if self._selected_id:
            self.app.action_watch_vars(self._selected_id)

    def _ctx_metrics(self):
        if self._selected_id:
            self.app.action_metrics(self._selected_id)

    def _ctx_copy_pid(self):
        if self._selected_id:
            info = self.app.runtimes.get(self._selected_id)
            if info:
                self.clipboard_clear()
                self.clipboard_append(str(info.pid))

    def _ctx_copy_details(self):
        if self._selected_id:
            info = self.app.runtimes.get(self._selected_id)
            if info:
                details = (f"Name: {info.name}\n"
                           f"PID: {info.pid}\n"
                           f"Language: {info.language}\n"
                           f"Status: {info.status}\n"
                           f"Memory: {info.memory_str}\n"
                           f"CPU: {info.cpu_pct:.1f}%\n"
                           f"Uptime: {info.uptime_str}\n"
                           f"Command: {info.cmdline}")
                self.clipboard_clear()
                self.clipboard_append(details)

    def _ctx_detach(self):
        if self._selected_id:
            self.app.action_detach(self._selected_id)

    def _ctx_kill(self):
        if self._selected_id:
            self.app.action_kill(self._selected_id)
