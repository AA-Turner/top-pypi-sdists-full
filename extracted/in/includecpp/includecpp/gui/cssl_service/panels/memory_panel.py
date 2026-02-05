"""
CSSL Service Manager - Memory Inspector Panel.
Three tabs: Variables, Objects, Addresses.
"""
import tkinter as tk
from tkinter import ttk, simpledialog
from typing import Dict, Optional
from .. import theme


class MemoryPanel(ttk.Frame):
    """Memory inspector with Variables, Objects, and Addresses tabs."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._current_runtime: Optional[str] = None
        self._build()

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  Memory Inspector", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM).pack(side="left")

        # Auto-refresh toggle
        self._auto_refresh_var = tk.BooleanVar(value=False)
        self.auto_btn = tk.Label(header, text="\u21BB Auto", font=theme.FONT_SMALL,
                                 bg=theme.CARD, fg=theme.TEXT_MUTED, cursor="hand2", padx=4)
        self.auto_btn.pack(side="right")
        self.auto_btn.bind("<Button-1>", lambda e: self._toggle_auto_refresh())

        refresh_btn = tk.Label(header, text="\u21BB Refresh", font=theme.FONT_SMALL,
                               bg=theme.CARD, fg=theme.BLUE, cursor="hand2", padx=6)
        refresh_btn.pack(side="right")
        refresh_btn.bind("<Button-1>", lambda e: self.refresh())

        # ── Notebook with 3 tabs ──
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Variables
        self.vars_frame = ttk.Frame(self.notebook, style="Surface.TFrame")
        self.notebook.add(self.vars_frame, text=" Variables ")
        self._build_vars_tab()

        # Tab 2: Objects
        self.objects_frame = ttk.Frame(self.notebook, style="Surface.TFrame")
        self.notebook.add(self.objects_frame, text=" Objects ")
        self._build_objects_tab()

        # Tab 3: Addresses
        self.addr_frame = ttk.Frame(self.notebook, style="Surface.TFrame")
        self.notebook.add(self.addr_frame, text=" Addresses ")
        self._build_addresses_tab()

    def _build_vars_tab(self):
        """Build the variables tab with editable values."""
        columns = ("value", "type")
        self.vars_tree = ttk.Treeview(self.vars_frame, columns=columns,
                                       show="tree headings", selectmode="browse")
        self.vars_tree.heading("#0", text="Name", anchor="w")
        self.vars_tree.heading("value", text="Value", anchor="w")
        self.vars_tree.heading("type", text="Type", anchor="w")
        self.vars_tree.column("#0", width=120, minwidth=80)
        self.vars_tree.column("value", width=200, minwidth=100)
        self.vars_tree.column("type", width=80, minwidth=60)

        scroll = ttk.Scrollbar(self.vars_frame, orient="vertical",
                                command=self.vars_tree.yview)
        self.vars_tree.configure(yscrollcommand=scroll.set)
        self.vars_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Double-click to edit
        self.vars_tree.bind("<Double-1>", self._edit_variable)

        # Context menu
        self._vars_menu = tk.Menu(self.vars_tree, tearoff=0, bg=theme.CARD,
                                   fg=theme.TEXT, activebackground=theme.BLUE,
                                   activeforeground=theme.TEXT)
        self._vars_menu.add_command(label="Edit Value", command=self._edit_selected_var)
        self._vars_menu.add_command(label="Watch Variable", command=self._watch_selected_var)
        self._vars_menu.add_separator()
        self._vars_menu.add_command(label="Copy Name", command=self._copy_var_name)
        self._vars_menu.add_command(label="Copy Value", command=self._copy_var_value)
        self.vars_tree.bind("<Button-3>", self._show_vars_menu)

    def _build_objects_tab(self):
        """Build the objects registry tab."""
        columns = ("type", "repr", "address")
        self.objects_tree = ttk.Treeview(self.objects_frame, columns=columns,
                                          show="tree headings", selectmode="browse")
        self.objects_tree.heading("#0", text="ID", anchor="w")
        self.objects_tree.heading("type", text="Type", anchor="w")
        self.objects_tree.heading("repr", text="Repr", anchor="w")
        self.objects_tree.heading("address", text="Address", anchor="w")
        self.objects_tree.column("#0", width=60, minwidth=40)
        self.objects_tree.column("type", width=100, minwidth=60)
        self.objects_tree.column("repr", width=180, minwidth=80)
        self.objects_tree.column("address", width=100, minwidth=60)

        scroll = ttk.Scrollbar(self.objects_frame, orient="vertical",
                                command=self.objects_tree.yview)
        self.objects_tree.configure(yscrollcommand=scroll.set)
        self.objects_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Context menu
        self._obj_menu = tk.Menu(self.objects_tree, tearoff=0, bg=theme.CARD,
                                  fg=theme.TEXT, activebackground=theme.BLUE,
                                  activeforeground=theme.TEXT)
        self._obj_menu.add_command(label="Reflect", command=self._reflect_object)
        self._obj_menu.add_command(label="Copy Address", command=self._copy_address)
        self._obj_menu.add_separator()
        self._obj_menu.add_command(label="Destroy", command=self._destroy_object,
                                    foreground=theme.RED)
        self.objects_tree.bind("<Button-3>", self._show_obj_menu)

    def _build_addresses_tab(self):
        """Build the address browser tab."""
        # Search bar
        search_frame = tk.Frame(self.addr_frame, bg=theme.SURFACE)
        search_frame.pack(fill="x", padx=4, pady=4)

        tk.Label(search_frame, text="Address:", font=theme.FONT_SMALL,
                 bg=theme.SURFACE, fg=theme.TEXT_DIM).pack(side="left")

        self.addr_search_var = tk.StringVar()
        addr_entry = ttk.Entry(search_frame, textvariable=self.addr_search_var,
                                font=theme.FONT_CODE_SMALL, width=16)
        addr_entry.pack(side="left", padx=4)
        addr_entry.bind("<Return>", lambda e: self._search_address())

        tk.Label(search_frame, text="Lookup", font=theme.FONT_SMALL,
                 bg=theme.CARD, fg=theme.BLUE, cursor="hand2", padx=6
                 ).pack(side="left")

        # Results
        columns = ("type", "value")
        self.addr_tree = ttk.Treeview(self.addr_frame, columns=columns,
                                       show="tree headings", selectmode="browse")
        self.addr_tree.heading("#0", text="Address", anchor="w")
        self.addr_tree.heading("type", text="Type", anchor="w")
        self.addr_tree.heading("value", text="Value", anchor="w")
        self.addr_tree.column("#0", width=120, minwidth=80)
        self.addr_tree.column("type", width=100, minwidth=60)
        self.addr_tree.column("value", width=200, minwidth=100)

        scroll = ttk.Scrollbar(self.addr_frame, orient="vertical",
                                command=self.addr_tree.yview)
        self.addr_tree.configure(yscrollcommand=scroll.set)
        self.addr_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # ── Data Loading ──────────────────────────────────────────────
    def load_data(self, runtime_id: str, data: Dict):
        """Load memory data for a runtime."""
        self._current_runtime = runtime_id

        # Clear existing
        for item in self.vars_tree.get_children():
            self.vars_tree.delete(item)
        for item in self.objects_tree.get_children():
            self.objects_tree.delete(item)

        # Populate variables
        variables = data.get("variables", {})
        for name, info in sorted(variables.items()):
            val = info.get("value", "")
            vtype = info.get("type", "")
            self.vars_tree.insert("", "end", text=name,
                                   values=(val[:150], vtype))

    def refresh(self):
        """Refresh data from the current runtime."""
        if self._current_runtime:
            self.app.action_inspect_memory(self._current_runtime)

    def _toggle_auto_refresh(self):
        val = not self._auto_refresh_var.get()
        self._auto_refresh_var.set(val)
        self.auto_btn.configure(fg=theme.GREEN if val else theme.TEXT_MUTED)

    # ── Variable Editing ──────────────────────────────────────────
    def _edit_variable(self, event):
        item = self.vars_tree.identify_row(event.y)
        if not item:
            return
        name = self.vars_tree.item(item, "text")
        old_val = self.vars_tree.item(item, "values")[0]
        new_val = simpledialog.askstring("Edit Variable",
                                          f"New value for '{name}':",
                                          initialvalue=old_val,
                                          parent=self)
        if new_val is not None and new_val != old_val:
            self.vars_tree.item(item, values=(new_val, self.vars_tree.item(item, "values")[1]))
            # Send to runtime via IPC (if available)
            self.app._log("info", "memory", f"Set {name} = {new_val}")

    def _edit_selected_var(self):
        sel = self.vars_tree.selection()
        if sel:
            self._edit_variable(type('Event', (), {'y': 0})())

    def _watch_selected_var(self):
        sel = self.vars_tree.selection()
        if sel:
            name = self.vars_tree.item(sel[0], "text")
            if self._current_runtime:
                self.app.action_watch_vars(self._current_runtime)

    def _copy_var_name(self):
        sel = self.vars_tree.selection()
        if sel:
            self.clipboard_clear()
            self.clipboard_append(self.vars_tree.item(sel[0], "text"))

    def _copy_var_value(self):
        sel = self.vars_tree.selection()
        if sel:
            self.clipboard_clear()
            self.clipboard_append(self.vars_tree.item(sel[0], "values")[0])

    def _show_vars_menu(self, event):
        item = self.vars_tree.identify_row(event.y)
        if item:
            self.vars_tree.selection_set(item)
            self._vars_menu.tk_popup(event.x_root, event.y_root)

    # ── Objects ───────────────────────────────────────────────────
    def _reflect_object(self):
        sel = self.objects_tree.selection()
        if sel:
            addr = self.objects_tree.item(sel[0], "values")[2]
            self.app._log("info", "memory", f"Reflect: {addr}")

    def _copy_address(self):
        sel = self.objects_tree.selection()
        if sel:
            self.clipboard_clear()
            self.clipboard_append(self.objects_tree.item(sel[0], "values")[2])

    def _destroy_object(self):
        sel = self.objects_tree.selection()
        if sel:
            addr = self.objects_tree.item(sel[0], "values")[2]
            if tk.messagebox.askyesno("Destroy Object",
                                       f"Destroy object at {addr}?"):
                self.app._log("warning", "memory", f"Destroy: {addr}")

    def _show_obj_menu(self, event):
        item = self.objects_tree.identify_row(event.y)
        if item:
            self.objects_tree.selection_set(item)
            self._obj_menu.tk_popup(event.x_root, event.y_root)

    def _search_address(self):
        addr = self.addr_search_var.get().strip()
        if addr:
            self.app._log("info", "memory", f"Address lookup: {addr}")
