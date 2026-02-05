"""
CSSL Service Manager - Console Panel.
Interactive CSSL REPL connected to a runtime instance.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from .. import theme
from ..widgets.syntax_text import SyntaxText


class ConsolePanel(ttk.Frame):
    """Interactive CSSL console / REPL panel."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._history: List[str] = []
        self._history_idx = -1
        self._connected_runtime: Optional[str] = None
        self._ipc_client = None
        self._build()

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  Console", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM).pack(side="left")

        self.runtime_label = tk.Label(header, text="  (no runtime connected)",
                                      font=theme.FONT_SMALL, bg=theme.CARD,
                                      fg=theme.TEXT_MUTED)
        self.runtime_label.pack(side="left", padx=(8, 0))

        # Toolbar buttons (right side)
        clear_btn = tk.Label(header, text="\u239A Clear", font=theme.FONT_SMALL,
                             bg=theme.CARD, fg=theme.TEXT_MUTED, cursor="hand2", padx=6)
        clear_btn.pack(side="right")
        clear_btn.bind("<Button-1>", lambda e: self.clear())
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(fg=theme.TEXT))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(fg=theme.TEXT_MUTED))

        # ── Output area ──
        output_frame = ttk.Frame(self, style="Surface.TFrame")
        output_frame.pack(fill="both", expand=True)

        self.output = SyntaxText(output_frame, readonly=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical",
                                   command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)

        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Welcome message
        self.output.append_line("CSSL Service Manager Console", "accent")
        self.output.append_line("=" * 40, "dim")
        self.output.append_line("Connect to a runtime to begin.", "system")
        self.output.append_line("Right-click a runtime \u2192 'Catch in CSSL'", "system")
        self.output.append_line("", "system")

        # ── Input area ──
        input_frame = tk.Frame(self, bg=theme.CARD)
        input_frame.pack(fill="x", side="bottom")

        prompt_label = tk.Label(input_frame, text=" cssl\u276F ", font=theme.FONT_CODE,
                                bg=theme.CARD, fg=theme.GREEN)
        prompt_label.pack(side="left")

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var,
                                     font=theme.FONT_CODE, bg=theme.SURFACE,
                                     fg=theme.TEXT, insertbackground=theme.TEXT,
                                     relief="flat", borderwidth=0,
                                     selectbackground=theme.HOVER,
                                     selectforeground=theme.TEXT)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 4), pady=4)

        send_btn = tk.Label(input_frame, text=" \u25B6 ", font=theme.FONT_CODE,
                            bg=theme.BLUE, fg=theme.TEXT, cursor="hand2", padx=4)
        send_btn.pack(side="right", padx=4, pady=4)
        send_btn.bind("<Button-1>", lambda e: self._execute())

        # ── Bindings ──
        self.input_entry.bind("<Return>", lambda e: self._execute())
        self.input_entry.bind("<Up>", lambda e: self._history_prev())
        self.input_entry.bind("<Down>", lambda e: self._history_next())
        self.input_entry.bind("<Control-l>", lambda e: self.clear())
        self.input_entry.bind("<Control-L>", lambda e: self.clear())
        self.input_entry.bind("<Tab>", self._autocomplete)

    # ── Runtime Connection ────────────────────────────────────────
    def connect_runtime(self, runtime_id: str, ipc_client=None):
        """Connect console to a specific runtime."""
        self._connected_runtime = runtime_id
        self._ipc_client = ipc_client

        info = self.app.runtimes.get(runtime_id)
        name = info.display_name if info else runtime_id

        self.runtime_label.configure(text=f"  \u25CF {name}", fg=theme.GREEN)
        self.output.append_line("", "system")
        self.output.append_line(f"\u2500\u2500 Connected to {name} \u2500\u2500", "success")
        self.output.append_line("Type CSSL commands below. Press Enter to execute.", "system")
        self.output.append_line("", "system")
        self.input_entry.focus_set()

    def disconnect(self):
        """Disconnect from current runtime."""
        self._connected_runtime = None
        if self._ipc_client:
            self._ipc_client.disconnect()
            self._ipc_client = None
        self.runtime_label.configure(text="  (no runtime connected)", fg=theme.TEXT_MUTED)
        self.output.append_line("\u2500\u2500 Disconnected \u2500\u2500", "warning")

    # ── Command Execution ─────────────────────────────────────────
    def _execute(self):
        """Execute the current input command."""
        cmd = self.input_var.get().strip()
        if not cmd:
            return

        # Add to history
        if not self._history or self._history[-1] != cmd:
            self._history.append(cmd)
        self._history_idx = -1

        # Clear input
        self.input_var.set("")

        # Echo command
        self.output.append_text("cssl\u276F ", "dim")
        self.output.append_line(cmd, "command")

        # Handle built-in commands
        if cmd.lower() in ('clear', 'cls'):
            self.clear()
            return
        if cmd.lower() in ('exit', 'quit', 'disconnect'):
            self.disconnect()
            return
        if cmd.lower() == 'help':
            self._show_help()
            return
        if cmd.lower() == 'history':
            for i, h in enumerate(self._history):
                self.output.append_line(f"  {i+1}: {h}", "dim")
            return

        # Execute via IPC or local
        if not self._connected_runtime:
            self.output.append_line("Error: No runtime connected", "error")
            self.output.append_line("Right-click a runtime \u2192 'Catch in CSSL' to connect", "system")
            return

        if self._ipc_client and self._ipc_client.connected:
            self._execute_remote(cmd)
        else:
            self._execute_local(cmd)

    def _execute_remote(self, cmd: str):
        """Execute command via IPC."""
        try:
            result = self._ipc_client.execute(cmd)
            if result.get("ok"):
                output = result.get("output", "")
                if output:
                    for line in output.rstrip('\n').split('\n'):
                        self.output.append_line(line, "output")
                ret = result.get("result")
                if ret and ret != "None":
                    self.output.append_line(f"\u2192 {ret}", "accent")
            else:
                error = result.get("error", "Unknown error")
                self.output.append_line(f"Error: {error}", "error")
        except Exception as e:
            self.output.append_line(f"IPC Error: {e}", "error")

    def _execute_local(self, cmd: str):
        """Execute command on a local in-process runtime."""
        info = self.app.runtimes.get(self._connected_runtime)
        if not info:
            self.output.append_line("Error: Runtime not found", "error")
            return

        # For now, show that remote execution is not yet available
        self.output.append_line("(Local execution \u2014 IPC not yet connected)", "warning")
        self.output.append_line(f"Would execute: {cmd}", "dim")

    # ── History ───────────────────────────────────────────────────
    def _history_prev(self):
        if not self._history:
            return
        if self._history_idx == -1:
            self._history_idx = len(self._history) - 1
        elif self._history_idx > 0:
            self._history_idx -= 1
        self.input_var.set(self._history[self._history_idx])
        self.input_entry.icursor("end")

    def _history_next(self):
        if not self._history or self._history_idx == -1:
            return
        if self._history_idx < len(self._history) - 1:
            self._history_idx += 1
            self.input_var.set(self._history[self._history_idx])
        else:
            self._history_idx = -1
            self.input_var.set("")
        self.input_entry.icursor("end")

    # ── Autocomplete ──────────────────────────────────────────────
    def _autocomplete(self, event):
        """Basic autocomplete from API data."""
        text = self.input_var.get()
        if not text:
            return "break"

        # Get completions from connected runtime's API
        info = self.app.runtimes.get(self._connected_runtime or "")
        completions = []

        if info and info.api_data:
            api = info.api_data
            for section in ("functions", "classes", "variables", "modules"):
                for name in api.get(section, {}):
                    if name.startswith(text):
                        completions.append(name)

        # Also try built-in CSSL names
        builtin_names = [
            'print', 'println', 'printl', 'typeof', 'sizeof', 'len', 'range',
            'true', 'false', 'null', 'undefined', 'for', 'while', 'if', 'else',
            'function', 'class', 'return', 'break', 'continue', 'import',
        ]
        for name in builtin_names:
            if name.startswith(text) and name not in completions:
                completions.append(name)

        if len(completions) == 1:
            self.input_var.set(completions[0])
            self.input_entry.icursor("end")
        elif len(completions) > 1:
            self.output.append_line("Completions:", "dim")
            self.output.append_line("  " + "  ".join(sorted(completions)[:20]), "info")

        return "break"

    # ── Helpers ───────────────────────────────────────────────────
    def clear(self):
        """Clear the output area."""
        self.output.clear()
        self.output.append_line("Console cleared.", "system")

    def _show_help(self):
        self.output.append_line("Console Commands:", "accent")
        self.output.append_line("  help         Show this help", "dim")
        self.output.append_line("  clear/cls    Clear console output", "dim")
        self.output.append_line("  history      Show command history", "dim")
        self.output.append_line("  disconnect   Disconnect from runtime", "dim")
        self.output.append_line("", "system")
        self.output.append_line("Shortcuts:", "accent")
        self.output.append_line("  Up/Down      Navigate command history", "dim")
        self.output.append_line("  Tab          Autocomplete", "dim")
        self.output.append_line("  Ctrl+L       Clear console", "dim")
        self.output.append_line("  Enter        Execute command", "dim")

    def write_output(self, text: str, tag: str = "output"):
        """Public method to write output from external sources."""
        self.output.append_line(text, tag)
