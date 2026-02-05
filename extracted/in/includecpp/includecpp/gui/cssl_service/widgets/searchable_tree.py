"""
CSSL Service Manager - Treeview with integrated search/filter bar.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Optional, Tuple
from .. import theme


class SearchableTree(ttk.Frame):
    """A Treeview widget with an integrated search bar and type filter."""

    def __init__(self, parent, columns: List[Tuple[str, str, int]],
                 show_filter: bool = True, on_select: Optional[Callable] = None,
                 on_double_click: Optional[Callable] = None, **kwargs):
        """
        Args:
            columns: List of (column_id, heading, width) tuples.
            show_filter: Whether to show the type filter combobox.
            on_select: Callback when item is selected.
            on_double_click: Callback when item is double-clicked.
        """
        super().__init__(parent, style="Surface.TFrame")
        self._columns = columns
        self._show_filter = show_filter
        self._on_select = on_select
        self._on_double_click = on_double_click
        self._all_items: List[dict] = []  # All items for filtering
        self._build()

    def _build(self):
        # ── Search bar ──
        search_frame = tk.Frame(self, bg=theme.SURFACE)
        search_frame.pack(fill="x", padx=4, pady=(4, 2))

        # Filter combobox
        if self._show_filter:
            self.filter_var = tk.StringVar(value="All")
            self.filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var,
                                              values=["All", "Functions", "Classes",
                                                       "Variables", "Modules", "Builtins"],
                                              width=10, state="readonly",
                                              font=theme.FONT_SMALL)
            self.filter_combo.pack(side="left", padx=(0, 4))
            self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())

        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._apply_filter())

        search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                  font=theme.FONT_SMALL)
        search_entry.pack(side="left", fill="x", expand=True, padx=2)

        # Result count
        self.count_label = tk.Label(search_frame, text="", font=theme.FONT_SMALL,
                                    bg=theme.SURFACE, fg=theme.TEXT_MUTED)
        self.count_label.pack(side="right", padx=4)

        # ── Treeview ──
        tree_frame = ttk.Frame(self, style="Surface.TFrame")
        tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        col_ids = [c[0] for c in self._columns]
        self.tree = ttk.Treeview(tree_frame, columns=col_ids, show="tree headings",
                                  selectmode="browse")

        self.tree.heading("#0", text="Name", anchor="w")
        self.tree.column("#0", width=200, minwidth=120)

        for col_id, heading, width in self._columns:
            self.tree.heading(col_id, text=heading, anchor="w")
            self.tree.column(col_id, width=width, minwidth=max(40, width // 2))

        # Tags
        self.tree.tag_configure("function", foreground=theme.SYNTAX["function"])
        self.tree.tag_configure("builtin", foreground=theme.SYNTAX["builtin"])
        self.tree.tag_configure("class", foreground=theme.SYNTAX["type"])
        self.tree.tag_configure("variable", foreground=theme.GREEN)
        self.tree.tag_configure("module", foreground=theme.ACCENT)
        self.tree.tag_configure("method", foreground=theme.CYAN)
        self.tree.tag_configure("category", foreground=theme.TEXT_DIM)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bindings
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", self._on_tree_double_click)

    def populate(self, items: List[dict]):
        """Populate tree with items.

        Each item dict: {
            'name': str, 'kind': str, 'values': tuple,
            'parent': str (iid or ''), 'children': list[dict]
        }
        """
        self._all_items = items
        self._apply_filter()

    def _apply_filter(self):
        """Apply search and type filter."""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip().lower()
        type_filter = self.filter_var.get().lower() if self._show_filter else "all"

        count = 0
        for item in self._all_items:
            if self._matches(item, query, type_filter):
                self._insert_item(item)
                count += 1
            elif item.get('children'):
                # Check if any child matches
                matching_children = [c for c in item['children']
                                     if self._matches(c, query, type_filter)]
                if matching_children:
                    parent_iid = self._insert_item(item)
                    for child in matching_children:
                        self._insert_item(child, parent_iid)
                        count += 1

        self.count_label.configure(text=f"{count} items")

    def _matches(self, item: dict, query: str, type_filter: str) -> bool:
        name = item.get('name', '').lower()
        kind = item.get('kind', '').lower()

        if query and query not in name:
            return False

        if type_filter != "all":
            filter_map = {
                "functions": ("function", "method"),
                "classes": ("class",),
                "variables": ("variable",),
                "modules": ("module",),
                "builtins": ("builtin",),
            }
            allowed = filter_map.get(type_filter, ())
            if kind not in allowed:
                return False

        return True

    def _insert_item(self, item: dict, parent: str = "") -> str:
        """Insert an item into the tree, return its iid."""
        name = item.get('name', '')
        kind = item.get('kind', 'variable')
        values = item.get('values', ())
        icon = item.get('icon', '')

        display = f"{icon}  {name}" if icon else name
        iid = self.tree.insert(parent, "end", text=display, values=values,
                                tags=(kind,), open=item.get('open', False))
        return iid

    def _on_tree_select(self, event):
        if self._on_select:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                self._on_select(item)

    def _on_tree_double_click(self, event):
        if self._on_double_click:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                self._on_double_click(item)

    def get_selected(self) -> Optional[dict]:
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])
        return None

    def clear(self):
        self._all_items.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.count_label.configure(text="")
