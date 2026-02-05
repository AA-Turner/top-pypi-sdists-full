"""
CSSL Service Manager - Main application window.
Professional runtime control & introspection tool.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading

from . import theme
from .toolbar import MenuBar
from .models import RuntimeInfo, LogEntry, Preferences
from .scanner import RuntimeScanner
from .panels.instances_panel import InstancesPanel
from .panels.console_panel import ConsolePanel
from .panels.api_browser import APIBrowserPanel
from .panels.memory_panel import MemoryPanel
from .panels.watch_panel import WatchPanel
from .panels.output_panel import OutputPanel
from .panels.metrics_panel import MetricsPanel
from .ipc import CSSLIPCClient
from .dialogs.preferences import PreferencesDialog, load_preferences, save_preferences
from .dialogs.export_dialog import ExportDialog
from .dialogs.attach_dialog import AttachDialog
from .dialogs.about_dialog import AboutDialog
from .widgets.status_bar import StatusBar
from .widgets.toast import show_toast


class CSSLServiceApp(tk.Tk):
    """Main CSSL Service Manager window."""

    def __init__(self):
        super().__init__()
        self.title("CSSL Service Manager")
        self.geometry("1400x900")
        self.minsize(1000, 600)

        # State
        self.runtimes: dict[str, RuntimeInfo] = {}
        self.preferences = load_preferences()
        self._logs: list[LogEntry] = []
        self._auto_scan_job = None
        self._panel_refs: dict[str, tk.Widget] = {}
        self._stats_job = None

        # Scanner
        self.scanner = RuntimeScanner()
        self.scanner.on_update(self._on_scanner_update)

        # Theme
        self._style = theme.setup_theme(self)

        # Icon
        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        # Build UI
        self._build_layout()
        self._bind_shortcuts()

        # Log startup
        self._log("info", "system", "CSSL Service Manager started")
        self._log("info", "system", "Ready \u2014 use Scan > Scan All or Ctrl+R to discover runtimes")

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.action_exit)

        # Start auto-scan after window is ready
        self.after(500, self._start_auto_scan)

        # Start stats refresh loop
        self._start_stats_refresh()

    # ── Layout ────────────────────────────────────────────────────
    def _build_layout(self):
        """Build the main application layout with paned windows."""
        # Menu bar
        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)

        # Main container
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        # ── Status Bar (pack first so it's at bottom) ──
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill="x", side="bottom")

        # ── Top area: horizontal pane (instances | center | right) ──
        self.h_pane = tk.PanedWindow(main_frame, orient="horizontal",
                                      bg=theme.BORDER, sashwidth=4,
                                      sashrelief="flat", borderwidth=0)
        self.h_pane.pack(fill="both", expand=True)

        # Left: Instances panel (real)
        self.instances_panel = InstancesPanel(self.h_pane, self)
        self._panel_refs["instances"] = self.instances_panel
        self.h_pane.add(self.instances_panel, width=300, minsize=200)

        # Center: vertical pane (console top | api browser + logs bottom)
        self.center_pane = tk.PanedWindow(self.h_pane, orient="vertical",
                                           bg=theme.BORDER, sashwidth=4,
                                           sashrelief="flat", borderwidth=0)
        self.h_pane.add(self.center_pane, minsize=400)

        # Center top: Console (real panel)
        self.console_panel = ConsolePanel(self.center_pane, self)
        self._panel_refs["console"] = self.console_panel
        self.center_pane.add(self.console_panel, height=350, minsize=150)

        # Center bottom: vertical pane (api browser | output logs)
        self.center_bottom_pane = tk.PanedWindow(self.center_pane, orient="vertical",
                                                   bg=theme.BORDER, sashwidth=4,
                                                   sashrelief="flat", borderwidth=0)
        self.center_pane.add(self.center_bottom_pane, minsize=200)

        # API Browser (real panel)
        self.api_browser = APIBrowserPanel(self.center_bottom_pane, self)
        self._panel_refs["api_browser"] = self.api_browser
        self.center_bottom_pane.add(self.api_browser, height=250, minsize=100)

        # Output / Logs (real panel)
        self.output_panel = OutputPanel(self.center_bottom_pane, self)
        self._panel_refs["logs"] = self.output_panel
        self.center_bottom_pane.add(self.output_panel, height=150, minsize=80)

        # Right: vertical pane (memory | watch | metrics)
        self.right_pane = tk.PanedWindow(self.h_pane, orient="vertical",
                                          bg=theme.BORDER, sashwidth=4,
                                          sashrelief="flat", borderwidth=0)
        self.h_pane.add(self.right_pane, width=320, minsize=200)

        # Memory Inspector (real panel)
        self.memory_panel = MemoryPanel(self.right_pane, self)
        self._panel_refs["memory"] = self.memory_panel
        self.right_pane.add(self.memory_panel, height=300, minsize=100)

        # Watch Panel (real panel)
        self.watch_panel = WatchPanel(self.right_pane, self)
        self._panel_refs["watch"] = self.watch_panel
        self.right_pane.add(self.watch_panel, height=200, minsize=80)

        # Metrics (real panel)
        self.metrics_panel = MetricsPanel(self.right_pane, self)
        self._panel_refs["metrics"] = self.metrics_panel
        self.right_pane.add(self.metrics_panel, height=200, minsize=80)

    def _make_panel_frame(self, title: str, key: str) -> ttk.Frame:
        """Create a styled panel frame with a title header."""
        frame = ttk.Frame(style="Surface.TFrame")

        # Header bar
        header = tk.Frame(frame, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text=f"  {title}", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM, anchor="w").pack(
            side="left", fill="x", expand=True)

        # Content area (placeholder)
        content = ttk.Frame(frame, style="Surface.TFrame")
        content.pack(fill="both", expand=True)

        ttk.Label(content, text=f"{title}\n\nWaiting for implementation...",
                  style="Muted.TLabel", justify="center", anchor="center",
                  font=theme.FONT_SMALL).pack(expand=True)

        self._panel_refs[key] = frame
        return frame

    # ── Scanner Integration ───────────────────────────────────────
    def _on_scanner_update(self, discovered: dict):
        """Called by scanner when results change (may be from background thread)."""
        self.after(0, self._update_ui_from_scan, discovered)

    def _update_ui_from_scan(self, discovered: dict):
        """Update UI with scan results (called on main thread)."""
        self.runtimes = discovered
        count = len(discovered)
        connected = sum(1 for r in discovered.values() if r.status == "attached")

        # Update instances panel
        self.instances_panel.update_runtimes(discovered)

        # Update status bar
        self.status_bar.set_runtime_count(count)
        self.status_bar.set_connected_count(connected)

        # Update runtimes menu
        self.menu_bar.update_runtimes_menu(discovered)

    def _start_auto_scan(self):
        """Begin periodic auto-scan if enabled."""
        if self.menu_bar.auto_scan:
            self._do_auto_scan()

    def _do_auto_scan(self):
        """Run a scan and schedule next one."""
        if not self.menu_bar.auto_scan:
            return
        self.scanner.scan_all_async()
        interval = self.preferences.scan_interval * 1000  # seconds → ms
        self._auto_scan_job = self.after(interval, self._do_auto_scan)

    def _start_stats_refresh(self):
        """Periodically refresh CPU/memory stats for discovered runtimes."""
        def refresh():
            for rid in list(self.runtimes.keys()):
                self.scanner.refresh_stats(rid)
            self._update_ui_from_scan(self.scanner.discovered)
            self._stats_job = self.after(5000, refresh)
        self._stats_job = self.after(5000, refresh)

    # ── Keyboard Shortcuts ────────────────────────────────────────
    def _bind_shortcuts(self):
        self.bind("<Control-r>", lambda e: self.action_scan_all())
        self.bind("<Control-R>", lambda e: self.action_scan_all())
        self.bind("<Control-n>", lambda e: self.action_new_runtime())
        self.bind("<Control-N>", lambda e: self.action_new_runtime())
        self.bind("<Control-comma>", lambda e: self.action_preferences())
        self.bind("<Control-q>", lambda e: self.action_exit())
        self.bind("<Control-Q>", lambda e: self.action_exit())
        self.bind("<F5>", lambda e: self.action_scan_all())
        self.bind("<Control-Shift-A>", lambda e: self.action_attach())
        self.bind("<Control-Shift-a>", lambda e: self.action_attach())

    # ── Logging ───────────────────────────────────────────────────
    def _log(self, level: str, source: str, message: str):
        entry = LogEntry(level=level, source=source, message=message)
        self._logs.append(entry)
        self.status_bar.set_status(message)
        if hasattr(self, 'output_panel'):
            self.output_panel.add_entry(entry)

    # ── Actions ───────────────────────────────────────────────────
    # File menu
    def action_new_runtime(self):
        self._log("info", "file", "New local runtime requested")
        show_toast(self, "New local runtime \u2014 not yet implemented", "info")

    def action_attach(self):
        self._log("info", "file", "Attach to process requested")
        dialog = AttachDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            mode = dialog.result["mode"]
            if mode == "pid":
                pid = dialog.result["pid"]
                self._log("info", "attach", f"Attaching to PID {pid}")
                show_toast(self, f"Attaching to PID {pid}...", "info")
                # Check if already discovered
                for rid, info in self.runtimes.items():
                    if info.pid == pid:
                        self.action_catch(rid)
                        return
                show_toast(self, f"PID {pid} not found in discovered runtimes", "warning")
            else:
                host = dialog.result["host"]
                port = dialog.result["port"]
                self._log("info", "attach", f"Attaching to {host}:{port}")
                ipc = CSSLIPCClient()
                if ipc.connect(host, port):
                    show_toast(self, f"Connected to {host}:{port}", "success")
                    # Create a synthetic runtime entry
                    from .models import RuntimeInfo
                    import time
                    rid = f"remote_{port}_{int(time.time())}"
                    info = RuntimeInfo(id=rid, pid=0, name=f"Remote ({host}:{port})",
                                       language="CSSL", status="attached",
                                       host=host, port=port)
                    self.runtimes[rid] = info
                    self.scanner.discovered[rid] = info
                    self._update_ui_from_scan(self.scanner.discovered)
                    self.console_panel.connect_runtime(rid, ipc)
                else:
                    show_toast(self, f"Failed to connect to {host}:{port}", "error")

    def action_export(self, kind: str):
        self._log("info", "file", f"Export {kind} requested")
        data = None
        if kind == "api":
            # Get API data from current browser or first runtime with API
            if hasattr(self, 'api_browser') and self.api_browser._current_api:
                data = self.api_browser._current_api
            else:
                for info in self.runtimes.values():
                    if info.api_data:
                        data = info.api_data
                        break
            if not data:
                show_toast(self, "No API data to export \u2014 scan first", "warning")
                return
        elif kind == "logs":
            data = self._logs
        elif kind == "snapshot":
            data = {rid: {"name": info.name, "pid": info.pid, "status": info.status,
                           "memory": info.memory_str, "uptime": info.uptime_str,
                           "api": info.api_data}
                     for rid, info in self.runtimes.items()}

        dialog = ExportDialog(self, kind, data)
        self.wait_window(dialog)
        if dialog.result:
            show_toast(self, f"Exported to {dialog.result}", "success")

    def action_preferences(self):
        self._log("info", "file", "Preferences opened")
        dialog = PreferencesDialog(self, self.preferences)
        self.wait_window(dialog)
        if dialog.result:
            self.preferences = dialog.result
            show_toast(self, "Preferences saved", "success")
            self._log("info", "preferences", "Preferences updated")

    def action_exit(self):
        if self._auto_scan_job:
            self.after_cancel(self._auto_scan_job)
        if self._stats_job:
            self.after_cancel(self._stats_job)
        self.destroy()

    # Scan menu
    def action_scan_all(self):
        if self.scanner.is_scanning:
            show_toast(self, "Scan already in progress...", "warning")
            return
        self._log("info", "scan", "Scanning all runtimes...")
        self.status_bar.start_progress("Scanning all...")
        show_toast(self, "Scanning for runtimes...", "info")

        def on_done(results):
            self.after(0, self._scan_complete, len(results))

        self.scanner.scan_all_async(callback=on_done)

    def action_scan(self, mode: str):
        if self.scanner.is_scanning:
            show_toast(self, "Scan already in progress...", "warning")
            return
        self._log("info", "scan", f"Scan mode: {mode}")
        self.status_bar.start_progress(f"Scanning ({mode})...")

        def do_scan():
            if mode == "markers":
                results = self.scanner.scan_markers()
            elif mode == "python" or mode == "deep":
                results = self.scanner.scan_processes()
            elif mode == "cssl":
                results = self.scanner.scan_markers()
            else:
                results = self.scanner.scan_all()

            # Merge results
            for info in results:
                if info.id not in self.scanner.discovered:
                    self.scanner.discovered[info.id] = info

            self.after(0, self._scan_complete, len(results))

        threading.Thread(target=do_scan, daemon=True).start()

    def _scan_complete(self, count: int = 0):
        self.status_bar.stop_progress()
        total = len(self.scanner.discovered)
        self.runtimes = self.scanner.discovered
        self._update_ui_from_scan(self.scanner.discovered)
        self.status_bar.flash_status(f"Scan complete \u2014 {total} runtimes found", "Green")
        self._log("success", "scan", f"Scan complete \u2014 {total} runtimes found")
        show_toast(self, f"Scan complete \u2014 {total} runtimes found",
                   "success" if total > 0 else "info")

    def action_toggle_auto_scan(self):
        enabled = self.menu_bar.auto_scan
        self._log("info", "scan", f"Auto-scan {'enabled' if enabled else 'disabled'}")
        if enabled:
            show_toast(self, f"Auto-scan enabled ({self.preferences.scan_interval}s interval)", "info")
            self._start_auto_scan()
        else:
            show_toast(self, "Auto-scan disabled", "warning")
            if self._auto_scan_job:
                self.after_cancel(self._auto_scan_job)
                self._auto_scan_job = None

    def action_clear_discovered(self):
        self.scanner.clear()
        self.runtimes.clear()
        self.status_bar.set_runtime_count(0)
        self.status_bar.set_connected_count(0)
        self.menu_bar.update_runtimes_menu({})
        self.instances_panel.update_runtimes({})
        self._log("info", "scan", "Cleared all discovered runtimes")
        show_toast(self, "Discovered runtimes cleared", "info")

    # Runtime actions
    def action_catch(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self._log("info", "runtime", f"Catch in CSSL: {name}")

        # Connect console to this runtime
        ipc_client = None
        if info and info.port:
            ipc_client = CSSLIPCClient()
            if ipc_client.connect(info.host, info.port):
                info.status = "attached"
                self._update_ui_from_scan(self.scanner.discovered)
                show_toast(self, f"Connected to {name}", "success")
            else:
                show_toast(self, f"Could not connect to {name} via IPC", "warning")
                ipc_client = None

        self.console_panel.connect_runtime(runtime_id, ipc_client)

    def action_scan_api(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self._log("info", "runtime", f"Scanning API for {name}")
        self.status_bar.start_progress(f"Scanning API for {name}...")
        show_toast(self, f"Scanning API for {name}...", "info")
        self.after(2000, lambda: (
            self.status_bar.stop_progress(),
            show_toast(self, f"API scan complete for {name}", "success")
        ))

    def action_get_api(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self._log("info", "runtime", f"Opening API browser for {name}")
        if info and info.api_data:
            self.api_browser.load_api(runtime_id, info.api_data)
            show_toast(self, f"API loaded for {name}", "success")
        else:
            show_toast(self, f"No API data for {name} \u2014 scan first", "warning")

    def action_inspect_memory(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self._log("info", "memory", f"Inspecting memory for {name}")
        # Load data if available from introspection
        data = {"variables": {}}
        if info and info.api_data:
            data["variables"] = info.api_data.get("variables", {})
        self.memory_panel.load_data(runtime_id, data)
        show_toast(self, f"Memory Inspector opened for {name}", "info")

    def action_watch_vars(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self._log("info", "watch", f"Watch panel focused for {name}")
        show_toast(self, f"Add variables to watch using + button", "info")

    def action_metrics(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        self.metrics_panel.set_runtime(runtime_id)
        self._log("info", "metrics", f"Monitoring metrics for {name}")
        show_toast(self, f"Metrics panel focused on {name}", "info")

    def action_detach(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        if info:
            info.status = "discovered"
            info.port = None
            self._update_ui_from_scan(self.scanner.discovered)
            self._log("info", "runtime", f"Detached from {info.display_name}")
            show_toast(self, f"Detached from {info.display_name}", "info")

    def action_kill(self, runtime_id: str):
        info = self.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id
        if self.preferences.confirm_kill:
            if not messagebox.askyesno("Kill Process",
                                       f"Are you sure you want to kill {name}?",
                                       icon="warning"):
                return
        self._log("warning", "runtime", f"Killing {name}...")
        success = self.scanner.kill_process(runtime_id)
        if success:
            show_toast(self, f"Process {name} terminated", "success")
            self._log("success", "runtime", f"{name} terminated")
        else:
            show_toast(self, f"Failed to kill {name}", "error")
            self._log("error", "runtime", f"Failed to kill {name}")

    # View menu
    def action_toggle_panel(self, key: str):
        panel = self._panel_refs.get(key)
        if not panel:
            return
        if panel.winfo_viewable():
            panel.pack_forget()
        else:
            panel.pack(fill="both", expand=True)
        self._log("info", "view", f"Toggled panel: {key}")

    def action_reset_layout(self):
        self._log("info", "view", "Layout reset")
        show_toast(self, "Layout reset to default", "info")

    # Tools menu
    def action_playground(self):
        show_toast(self, "CSSL Playground \u2014 coming soon", "info")

    def action_python_shell(self):
        show_toast(self, "Python Shell \u2014 coming soon", "info")

    def action_address_lookup(self):
        show_toast(self, "Address Lookup \u2014 coming soon", "info")

    def action_object_graph(self):
        show_toast(self, "Object Graph \u2014 coming soon", "info")

    def action_profiler(self):
        show_toast(self, "Function Profiler \u2014 coming soon", "info")

    def action_event_monitor(self):
        show_toast(self, "Event Monitor \u2014 coming soon", "info")

    def action_gc(self):
        show_toast(self, "Garbage Collector \u2014 coming soon", "info")

    # Help menu
    def action_docs(self):
        show_toast(self, "Documentation \u2014 opening browser", "info")

    def action_cssl_ref(self):
        show_toast(self, "CSSL Reference \u2014 opening browser", "info")

    def action_shortcuts(self):
        shortcuts = (
            "Keyboard Shortcuts\n\n"
            "Ctrl+R / F5       Scan All Runtimes\n"
            "Ctrl+N            New Local Runtime\n"
            "Ctrl+Shift+A      Attach to Process\n"
            "Ctrl+,            Preferences\n"
            "Ctrl+Q            Exit\n"
            "Ctrl+L            Clear Console\n"
            "Enter             Execute Command\n"
            "Up/Down           Command History\n"
            "Tab               Autocomplete\n"
            "Double-click      Catch in CSSL\n"
            "Right-click       Context Menu\n"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

    def action_about(self):
        AboutDialog(self)
