"""
CSSL Service Manager - Menu bar with all tool menus.
"""
import tkinter as tk
from . import theme


class MenuBar(tk.Menu):
    """Full menu bar for the CSSL Service Manager."""

    def __init__(self, app):
        super().__init__(app, bg=theme.CARD, fg=theme.TEXT,
                         activebackground=theme.HOVER, activeforeground=theme.TEXT,
                         borderwidth=0, relief="flat")
        self.app = app
        self._runtime_menu = None
        self._view_checks = {}
        self._build()

    def _menu(self, label: str) -> tk.Menu:
        """Create a submenu with dark styling."""
        m = tk.Menu(self, tearoff=0, bg=theme.CARD, fg=theme.TEXT,
                    activebackground=theme.BLUE, activeforeground=theme.TEXT,
                    borderwidth=1, relief="flat",
                    disabledforeground=theme.TEXT_MUTED)
        self.add_cascade(label=label, menu=m)
        return m

    def _build(self):
        self._build_file()
        self._build_scan()
        self._build_runtimes()
        self._build_view()
        self._build_tools()
        self._build_help()

    # ── File ──────────────────────────────────────────────────────
    def _build_file(self):
        m = self._menu("File")
        m.add_command(label="New Local Runtime", command=self.app.action_new_runtime,
                      accelerator="Ctrl+N")
        m.add_command(label="Attach to Process...", command=self.app.action_attach,
                      accelerator="Ctrl+Shift+A")
        m.add_separator()

        # Export submenu
        export = tk.Menu(m, tearoff=0, bg=theme.CARD, fg=theme.TEXT,
                         activebackground=theme.BLUE, activeforeground=theme.TEXT)
        export.add_command(label="Export API...  (JSON / HTML / Markdown)",
                           command=lambda: self.app.action_export("api"))
        export.add_command(label="Export Logs...  (TXT / CSV)",
                           command=lambda: self.app.action_export("logs"))
        export.add_command(label="Export Snapshot...  (Full State JSON)",
                           command=lambda: self.app.action_export("snapshot"))
        m.add_cascade(label="Export", menu=export)
        m.add_separator()
        m.add_command(label="Preferences", command=self.app.action_preferences,
                      accelerator="Ctrl+,")
        m.add_separator()
        m.add_command(label="Exit", command=self.app.action_exit, accelerator="Alt+F4")

    # ── Scan ──────────────────────────────────────────────────────
    def _build_scan(self):
        m = self._menu("Scan")
        m.add_command(label="Scan All", command=self.app.action_scan_all,
                      accelerator="Ctrl+R")
        m.add_command(label="Scan Python Runtimes",
                      command=lambda: self.app.action_scan("python"))
        m.add_command(label="Scan CSSL Runtimes",
                      command=lambda: self.app.action_scan("cssl"))
        m.add_separator()
        m.add_command(label="Quick Scan (Markers Only)",
                      command=lambda: self.app.action_scan("markers"))
        m.add_command(label="Deep Scan (Process Inspection)",
                      command=lambda: self.app.action_scan("deep"))
        m.add_separator()

        self._auto_scan_var = tk.BooleanVar(value=True)
        m.add_checkbutton(label="Auto-Scan", variable=self._auto_scan_var,
                          command=self.app.action_toggle_auto_scan)
        m.add_separator()
        m.add_command(label="Clear Discovered", command=self.app.action_clear_discovered)

    # ── Runtimes (dynamic) ────────────────────────────────────────
    def _build_runtimes(self):
        self._runtime_menu = self._menu("Runtimes")
        self._runtime_menu.add_command(label="(no runtimes discovered)",
                                       state="disabled")

    def update_runtimes_menu(self, runtimes: dict):
        """Rebuild the Runtimes menu with discovered runtime entries."""
        self._runtime_menu.delete(0, "end")
        if not runtimes:
            self._runtime_menu.add_command(label="(no runtimes discovered)",
                                           state="disabled")
            return

        for rid, info in runtimes.items():
            sub = tk.Menu(self._runtime_menu, tearoff=0,
                          bg=theme.CARD, fg=theme.TEXT,
                          activebackground=theme.BLUE, activeforeground=theme.TEXT)

            status_dot = {"running": "\u25CF", "attached": "\u25CF",
                          "scanning": "\u25CF", "dead": "\u25CF",
                          "discovered": "\u25CB"}.get(info.status, "\u25CB")

            sub.add_command(label="Catch in CSSL",
                            command=lambda r=rid: self.app.action_catch(r))
            sub.add_command(label="Scan API",
                            command=lambda r=rid: self.app.action_scan_api(r))
            sub.add_command(label="Get API",
                            command=lambda r=rid: self.app.action_get_api(r),
                            state="normal" if info.api_scanned else "disabled")
            sub.add_separator()
            sub.add_command(label="Inspect Memory",
                            command=lambda r=rid: self.app.action_inspect_memory(r))
            sub.add_command(label="Watch Variables",
                            command=lambda r=rid: self.app.action_watch_vars(r))
            sub.add_command(label="Metrics",
                            command=lambda r=rid: self.app.action_metrics(r))
            sub.add_separator()
            sub.add_command(label="Detach",
                            command=lambda r=rid: self.app.action_detach(r))
            sub.add_command(label="Kill Process",
                            command=lambda r=rid: self.app.action_kill(r))

            self._runtime_menu.add_cascade(
                label=f"  {status_dot}  {info.display_name}", menu=sub)

    # ── View ──────────────────────────────────────────────────────
    def _build_view(self):
        m = self._menu("View")
        panels = [
            ("Instances", "instances"),
            ("Console", "console"),
            ("API Browser", "api_browser"),
            ("Memory Inspector", "memory"),
            ("Watch Panel", "watch"),
            ("Output / Logs", "logs"),
            ("Metrics", "metrics"),
        ]
        for label, key in panels:
            var = tk.BooleanVar(value=True)
            self._view_checks[key] = var
            m.add_checkbutton(label=label, variable=var,
                              command=lambda k=key: self.app.action_toggle_panel(k))
        m.add_separator()
        m.add_command(label="Reset Layout", command=self.app.action_reset_layout)

    # ── Tools ─────────────────────────────────────────────────────
    def _build_tools(self):
        m = self._menu("Tools")
        m.add_command(label="CSSL Playground", command=self.app.action_playground)
        m.add_command(label="Python Shell", command=self.app.action_python_shell)
        m.add_separator()
        m.add_command(label="Address Lookup", command=self.app.action_address_lookup)
        m.add_command(label="Object Graph", command=self.app.action_object_graph)
        m.add_separator()
        m.add_command(label="Function Profiler", command=self.app.action_profiler)
        m.add_command(label="Event Monitor", command=self.app.action_event_monitor)
        m.add_command(label="Garbage Collector", command=self.app.action_gc)

    # ── Help ──────────────────────────────────────────────────────
    def _build_help(self):
        m = self._menu("Help")
        m.add_command(label="Documentation", command=self.app.action_docs)
        m.add_command(label="CSSL Reference", command=self.app.action_cssl_ref)
        m.add_command(label="Keyboard Shortcuts", command=self.app.action_shortcuts,
                      accelerator="Ctrl+?")
        m.add_separator()
        m.add_command(label="About", command=self.app.action_about)

    @property
    def auto_scan(self) -> bool:
        return self._auto_scan_var.get()

    @auto_scan.setter
    def auto_scan(self, value: bool):
        self._auto_scan_var.set(value)
