"""
CSSL Service Manager - Attach to Process Dialog.
Manual connection by PID or host:port.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple
from .. import theme


class AttachDialog(tk.Toplevel):
    """Dialog to manually attach to a process by PID or host:port."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Attach to Process")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=theme.BG)

        self.result: Optional[dict] = None
        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        tk.Label(self, text="Attach to Process", font=theme.FONT_TITLE,
                 bg=theme.BG, fg=theme.TEXT).pack(pady=(16, 8))

        tk.Label(self, text="Connect to a running CSSL/Python runtime",
                 font=theme.FONT_SMALL, bg=theme.BG, fg=theme.TEXT_MUTED).pack(pady=(0, 12))

        # Mode selection
        self.mode_var = tk.StringVar(value="pid")

        mode_frame = tk.Frame(self, bg=theme.SURFACE)
        mode_frame.pack(fill="x", padx=24, pady=4)

        ttk.Radiobutton(mode_frame, text="By Process ID (PID)",
                         variable=self.mode_var, value="pid",
                         command=self._toggle_mode).pack(anchor="w", padx=8, pady=4)
        ttk.Radiobutton(mode_frame, text="By Network Address (host:port)",
                         variable=self.mode_var, value="network",
                         command=self._toggle_mode).pack(anchor="w", padx=8, pady=4)

        # Input fields
        input_frame = tk.Frame(self, bg=theme.SURFACE)
        input_frame.pack(fill="x", padx=24, pady=8)

        # PID input
        self.pid_frame = tk.Frame(input_frame, bg=theme.SURFACE)
        self.pid_frame.pack(fill="x", padx=8, pady=4)

        tk.Label(self.pid_frame, text="PID:", font=theme.FONT,
                 bg=theme.SURFACE, fg=theme.TEXT, width=8, anchor="w").pack(side="left")
        self.pid_var = tk.StringVar()
        ttk.Entry(self.pid_frame, textvariable=self.pid_var,
                  font=theme.FONT, width=12).pack(side="left", padx=4)

        # Network input
        self.net_frame = tk.Frame(input_frame, bg=theme.SURFACE)

        row1 = tk.Frame(self.net_frame, bg=theme.SURFACE)
        row1.pack(fill="x", pady=2)
        tk.Label(row1, text="Host:", font=theme.FONT,
                 bg=theme.SURFACE, fg=theme.TEXT, width=8, anchor="w").pack(side="left")
        self.host_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(row1, textvariable=self.host_var,
                  font=theme.FONT, width=20).pack(side="left", padx=4)

        row2 = tk.Frame(self.net_frame, bg=theme.SURFACE)
        row2.pack(fill="x", pady=2)
        tk.Label(row2, text="Port:", font=theme.FONT,
                 bg=theme.SURFACE, fg=theme.TEXT, width=8, anchor="w").pack(side="left")
        self.port_var = tk.StringVar(value="45000")
        ttk.Entry(row2, textvariable=self.port_var,
                  font=theme.FONT, width=8).pack(side="left", padx=4)

        # Buttons
        btn_frame = tk.Frame(self, bg=theme.BG)
        btn_frame.pack(fill="x", padx=24, pady=(12, 16))

        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="Attach", style="Accent.TButton",
                   command=self._attach).pack(side="right", padx=4)

    def _toggle_mode(self):
        if self.mode_var.get() == "pid":
            self.net_frame.pack_forget()
            self.pid_frame.pack(fill="x", padx=8, pady=4)
        else:
            self.pid_frame.pack_forget()
            self.net_frame.pack(fill="x", padx=8, pady=4)

    def _attach(self):
        mode = self.mode_var.get()
        if mode == "pid":
            try:
                pid = int(self.pid_var.get().strip())
                self.result = {"mode": "pid", "pid": pid}
            except ValueError:
                tk.messagebox.showerror("Invalid PID", "Please enter a valid process ID.",
                                         parent=self)
                return
        else:
            host = self.host_var.get().strip()
            try:
                port = int(self.port_var.get().strip())
                self.result = {"mode": "network", "host": host, "port": port}
            except ValueError:
                tk.messagebox.showerror("Invalid Port", "Please enter a valid port number.",
                                         parent=self)
                return

        self.destroy()
