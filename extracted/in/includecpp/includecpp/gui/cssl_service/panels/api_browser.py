"""
CSSL Service Manager - API Browser Panel.
Searchable tree of runtime API (functions, classes, variables, modules) with documentation viewer.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
from .. import theme
from ..widgets.searchable_tree import SearchableTree
from ..widgets.syntax_text import SyntaxText


class APIBrowserPanel(ttk.Frame):
    """API browser with searchable tree and documentation viewer."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._current_api: Optional[Dict] = None
        self._current_runtime: Optional[str] = None
        self._build()

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  API Browser", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM).pack(side="left")

        self.runtime_label = tk.Label(header, text="", font=theme.FONT_SMALL,
                                      bg=theme.CARD, fg=theme.TEXT_MUTED)
        self.runtime_label.pack(side="left", padx=(8, 0))

        # Refresh button
        refresh_btn = tk.Label(header, text="\u21BB Refresh", font=theme.FONT_SMALL,
                               bg=theme.CARD, fg=theme.BLUE, cursor="hand2", padx=6)
        refresh_btn.pack(side="right")
        refresh_btn.bind("<Button-1>", lambda e: self._refresh())
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.configure(bg=theme.HOVER))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.configure(bg=theme.CARD))

        # ── Main content: paned (tree left | docs right) ──
        content_pane = tk.PanedWindow(self, orient="horizontal",
                                       bg=theme.BORDER, sashwidth=3,
                                       sashrelief="flat", borderwidth=0)
        content_pane.pack(fill="both", expand=True)

        # Left: searchable tree
        self.api_tree = SearchableTree(
            content_pane,
            columns=[("type", "Type", 80), ("signature", "Signature", 200)],
            show_filter=True,
            on_select=self._on_select,
            on_double_click=self._on_double_click,
        )
        content_pane.add(self.api_tree, width=400, minsize=200)

        # Right: documentation viewer
        doc_frame = ttk.Frame(content_pane, style="Surface.TFrame")
        content_pane.add(doc_frame, width=300, minsize=150)

        doc_header = tk.Frame(doc_frame, bg=theme.CARD, height=24)
        doc_header.pack(fill="x")
        doc_header.pack_propagate(False)
        tk.Label(doc_header, text="  Documentation", font=theme.FONT_SMALL,
                 bg=theme.CARD, fg=theme.TEXT_MUTED).pack(side="left")

        self.doc_view = SyntaxText(doc_frame, readonly=True)
        self.doc_view.pack(fill="both", expand=True)
        self.doc_view.append_line("Select an item to view documentation.", "dim")

        # Right-click context menu
        self._context_menu = tk.Menu(self.api_tree.tree, tearoff=0,
                                      bg=theme.CARD, fg=theme.TEXT,
                                      activebackground=theme.BLUE,
                                      activeforeground=theme.TEXT)
        self._context_menu.add_command(label="Copy Name", command=self._ctx_copy_name)
        self._context_menu.add_command(label="Copy Signature", command=self._ctx_copy_sig)
        self._context_menu.add_command(label="Insert in Console", command=self._ctx_insert)
        self._context_menu.add_separator()
        self._context_menu.add_command(label="Watch Variable", command=self._ctx_watch)

        self.api_tree.tree.bind("<Button-3>", self._on_right_click)

    # ── Data Loading ──────────────────────────────────────────────
    def load_api(self, runtime_id: str, api_data: Dict):
        """Load API data from a scan result."""
        self._current_runtime = runtime_id
        self._current_api = api_data

        info = self.app.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self.runtime_label.configure(text=f"\u25CF {name}")

        items = self._build_tree_items(api_data)
        self.api_tree.populate(items)

    def _build_tree_items(self, api_data: Dict) -> List[dict]:
        """Convert API data to tree items."""
        items = []

        # Builtins
        builtins = api_data.get("functions", {})
        builtin_items = []
        for name, info in sorted(builtins.items()):
            if info.get("type") == "builtin":
                builtin_items.append({
                    "name": name,
                    "kind": "builtin",
                    "values": ("builtin", info.get("signature", f"{name}()")),
                    "icon": "B",
                })

        if builtin_items:
            items.append({
                "name": f"Builtins ({len(builtin_items)})",
                "kind": "category",
                "values": ("", ""),
                "icon": "\u25B8",
                "open": False,
                "children": builtin_items,
            })

        # User functions
        user_funcs = []
        for name, info in sorted(builtins.items()):
            if info.get("type") != "builtin":
                user_funcs.append({
                    "name": name,
                    "kind": "function",
                    "values": ("function", info.get("signature", f"{name}()")),
                    "icon": "f",
                })

        if user_funcs:
            items.append({
                "name": f"Functions ({len(user_funcs)})",
                "kind": "category",
                "values": ("", ""),
                "icon": "\u25B8",
                "open": True,
                "children": user_funcs,
            })

        # Modules
        modules = api_data.get("modules", {})
        if modules:
            mod_items = []
            for name, info in sorted(modules.items()):
                members = info.get("members", [])
                child_items = []
                for member in sorted(members):
                    child_items.append({
                        "name": member,
                        "kind": "method",
                        "values": ("member", ""),
                        "icon": "m",
                    })
                mod_items.append({
                    "name": f"@{name}",
                    "kind": "module",
                    "values": ("module", f"{len(members)} members"),
                    "icon": "M",
                    "children": child_items,
                    "open": False,
                })
            items.append({
                "name": f"Modules ({len(modules)})",
                "kind": "category",
                "values": ("", ""),
                "icon": "\u25B8",
                "open": True,
                "children": mod_items,
            })

        # Classes
        classes = api_data.get("classes", {})
        if classes:
            class_items = []
            for name, info in sorted(classes.items()):
                class_items.append({
                    "name": name,
                    "kind": "class",
                    "values": ("class", info.get("name", name)),
                    "icon": "C",
                })
            items.append({
                "name": f"Classes ({len(classes)})",
                "kind": "category",
                "values": ("", ""),
                "icon": "\u25B8",
                "open": True,
                "children": class_items,
            })

        # Variables
        variables = api_data.get("variables", {})
        if variables:
            var_items = []
            for name, info in sorted(variables.items()):
                val_repr = info.get("value", "")
                type_name = info.get("type", "")
                var_items.append({
                    "name": name,
                    "kind": "variable",
                    "values": (type_name, val_repr[:100]),
                    "icon": "v",
                })
            items.append({
                "name": f"Variables ({len(variables)})",
                "kind": "category",
                "values": ("", ""),
                "icon": "\u25B8",
                "open": True,
                "children": var_items,
            })

        return items

    def _refresh(self):
        """Re-scan API for current runtime."""
        if self._current_runtime:
            self.app.action_scan_api(self._current_runtime)

    # ── Selection ─────────────────────────────────────────────────
    def _on_select(self, item: dict):
        """Show documentation for selected item."""
        self.doc_view.clear()

        text = item.get("text", "").strip()
        values = item.get("values", ())
        tags = item.get("tags", ())

        kind = values[0] if len(values) > 0 else ""
        sig = values[1] if len(values) > 1 else ""

        # Clean name (remove icon prefix)
        name = text.lstrip("BfmCvM\u25B8 ").strip()

        self.doc_view.append_line(f"{name}", "accent")
        self.doc_view.append_line("\u2500" * 40, "dim")

        if kind:
            self.doc_view.append_line(f"Type: {kind}", "info")
        if sig:
            self.doc_view.append_line(f"Signature: {sig}", "output")

        self.doc_view.append_line("", "system")

        # Show additional info from API data
        if self._current_api and name:
            for section in ("functions", "variables", "classes", "modules"):
                data = self._current_api.get(section, {})
                if name in data or name.lstrip('@') in data:
                    info = data.get(name, data.get(name.lstrip('@'), {}))
                    if isinstance(info, dict):
                        for key, val in info.items():
                            if key not in ("type", "signature", "name"):
                                self.doc_view.append_line(f"{key}: {val}", "dim")
                    break

    def _on_double_click(self, item: dict):
        """Insert function/variable name into console."""
        text = item.get("text", "").strip()
        name = text.lstrip("BfmCvM\u25B8 ").strip()
        if name and hasattr(self.app, 'console_panel'):
            current = self.app.console_panel.input_var.get()
            self.app.console_panel.input_var.set(current + name)
            self.app.console_panel.input_entry.focus_set()

    # ── Context Menu ──────────────────────────────────────────────
    def _on_right_click(self, event):
        item = self.api_tree.tree.identify_row(event.y)
        if item:
            self.api_tree.tree.selection_set(item)
            self._context_menu.tk_popup(event.x_root, event.y_root)

    def _get_selected_name(self) -> str:
        sel = self.api_tree.get_selected()
        if sel:
            text = sel.get("text", "").strip()
            return text.lstrip("BfmCvM\u25B8 ").strip()
        return ""

    def _ctx_copy_name(self):
        name = self._get_selected_name()
        if name:
            self.clipboard_clear()
            self.clipboard_append(name)

    def _ctx_copy_sig(self):
        sel = self.api_tree.get_selected()
        if sel:
            values = sel.get("values", ())
            sig = values[1] if len(values) > 1 else ""
            if sig:
                self.clipboard_clear()
                self.clipboard_append(sig)

    def _ctx_insert(self):
        name = self._get_selected_name()
        if name and hasattr(self.app, 'console_panel'):
            current = self.app.console_panel.input_var.get()
            self.app.console_panel.input_var.set(current + name)

    def _ctx_watch(self):
        name = self._get_selected_name()
        if name and self._current_runtime:
            self.app.action_watch_vars(self._current_runtime)

    def clear(self):
        """Clear the API browser."""
        self.api_tree.clear()
        self.doc_view.clear()
        self._current_api = None
        self._current_runtime = None
        self.runtime_label.configure(text="")
