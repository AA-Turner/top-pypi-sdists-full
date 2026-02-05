"""
CSSL Service Manager - Export Dialog.
Export API, logs, or snapshots to JSON/HTML/CSV/TXT.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import time
from typing import Optional
from .. import theme


class ExportDialog(tk.Toplevel):
    """Export dialog with format selection."""

    def __init__(self, parent, export_type: str, data=None):
        super().__init__(parent)
        self.title(f"Export {export_type.title()}")
        self.geometry("420x340")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=theme.BG)

        self.export_type = export_type
        self.data = data
        self.result: Optional[str] = None

        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        # Title
        tk.Label(self, text=f"Export {self.export_type.title()}", font=theme.FONT_TITLE,
                 bg=theme.BG, fg=theme.TEXT).pack(pady=(16, 8))

        # Format selection
        format_frame = tk.Frame(self, bg=theme.SURFACE)
        format_frame.pack(fill="x", padx=24, pady=8)

        tk.Label(format_frame, text="Format:", font=theme.FONT,
                 bg=theme.SURFACE, fg=theme.TEXT).pack(anchor="w", padx=8, pady=(8, 4))

        self.format_var = tk.StringVar(value="json")
        formats = self._get_formats()

        for fmt, label, desc in formats:
            row = tk.Frame(format_frame, bg=theme.SURFACE)
            row.pack(fill="x", padx=8, pady=2)
            ttk.Radiobutton(row, text=label, value=fmt,
                            variable=self.format_var).pack(side="left")
            tk.Label(row, text=desc, font=theme.FONT_SMALL,
                     bg=theme.SURFACE, fg=theme.TEXT_MUTED).pack(side="left", padx=(8, 0))

        # Options
        options_frame = tk.Frame(self, bg=theme.SURFACE)
        options_frame.pack(fill="x", padx=24, pady=8)

        self.include_timestamp = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include timestamps",
                         variable=self.include_timestamp).pack(anchor="w", padx=8, pady=2)

        self.pretty_print = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Pretty print (JSON/HTML)",
                         variable=self.pretty_print).pack(anchor="w", padx=8, pady=2)

        # Buttons
        btn_frame = tk.Frame(self, bg=theme.BG)
        btn_frame.pack(fill="x", padx=24, pady=(16, 16))

        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(btn_frame, text="Export...", style="Accent.TButton",
                   command=self._export).pack(side="right", padx=4)

    def _get_formats(self):
        if self.export_type == "api":
            return [
                ("json", "JSON", "Structured data format"),
                ("html", "HTML", "Viewable in browser"),
                ("md", "Markdown", "Documentation format"),
            ]
        elif self.export_type == "logs":
            return [
                ("txt", "Plain Text", "Simple log output"),
                ("csv", "CSV", "Spreadsheet compatible"),
                ("json", "JSON", "Structured data format"),
            ]
        else:  # snapshot
            return [
                ("json", "JSON", "Full state snapshot"),
            ]

    def _export(self):
        fmt = self.format_var.get()
        ext_map = {"json": ".json", "html": ".html", "md": ".md",
                    "txt": ".txt", "csv": ".csv"}
        ext = ext_map.get(fmt, ".json")

        filepath = filedialog.asksaveasfilename(
            parent=self,
            title=f"Export {self.export_type.title()}",
            defaultextension=ext,
            filetypes=[
                (f"{fmt.upper()} files", f"*{ext}"),
                ("All files", "*.*"),
            ],
            initialfile=f"cssl_{self.export_type}_{int(time.time())}{ext}",
        )

        if not filepath:
            return

        try:
            content = self._generate_content(fmt)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.result = filepath
            messagebox.showinfo("Export Complete",
                                f"Exported to:\n{filepath}",
                                parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Export Error",
                                 f"Failed to export:\n{e}",
                                 parent=self)

    def _generate_content(self, fmt: str) -> str:
        if self.data is None:
            return "{}" if fmt == "json" else ""

        if fmt == "json":
            indent = 2 if self.pretty_print.get() else None
            if isinstance(self.data, list):
                # Logs
                entries = []
                for entry in self.data:
                    d = {"level": entry.level, "source": entry.source,
                         "message": entry.message}
                    if self.include_timestamp.get():
                        d["time"] = entry.time_str
                    entries.append(d)
                return json.dumps(entries, indent=indent, ensure_ascii=False)
            else:
                return json.dumps(self.data, indent=indent, ensure_ascii=False,
                                   default=str)

        elif fmt == "html":
            return self._to_html()

        elif fmt == "md":
            return self._to_markdown()

        elif fmt == "txt":
            lines = []
            if isinstance(self.data, list):
                for entry in self.data:
                    ts = f"[{entry.time_str}] " if self.include_timestamp.get() else ""
                    lines.append(f"{ts}[{entry.level.upper()}] [{entry.source}] {entry.message}")
            return "\n".join(lines)

        elif fmt == "csv":
            lines = ["time,level,source,message"]
            if isinstance(self.data, list):
                for entry in self.data:
                    msg = entry.message.replace('"', '""')
                    lines.append(f'"{entry.time_str}","{entry.level}","{entry.source}","{msg}"')
            return "\n".join(lines)

        return str(self.data)

    def _to_html(self) -> str:
        html = ['<!DOCTYPE html><html><head>',
                '<meta charset="utf-8">',
                f'<title>CSSL {self.export_type.title()} Export</title>',
                '<style>body{background:#0a0a0a;color:#fff;font-family:Consolas,monospace;padding:20px}',
                'h1{color:#a78bfa}table{border-collapse:collapse;width:100%}',
                'th{background:#1a1a1a;color:#888;padding:8px;text-align:left;border-bottom:1px solid #2a2a2a}',
                'td{padding:6px 8px;border-bottom:1px solid #1a1a1a}',
                '.function{color:#61afef}.variable{color:#4ade80}.class{color:#e5c07b}.module{color:#a78bfa}',
                '</style></head><body>',
                f'<h1>CSSL {self.export_type.title()} Export</h1>',
                f'<p style="color:#888">Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}</p>']

        if isinstance(self.data, dict):
            for section, items in self.data.items():
                if isinstance(items, dict) and items:
                    html.append(f'<h2>{section.title()}</h2><table><tr><th>Name</th><th>Type</th><th>Details</th></tr>')
                    for name, info in items.items():
                        cls = section.rstrip('s')
                        details = ""
                        if isinstance(info, dict):
                            details = info.get('signature', info.get('value', ''))
                            kind = info.get('type', '')
                        else:
                            kind = str(info)
                        html.append(f'<tr><td class="{cls}">{name}</td><td>{kind}</td><td>{details}</td></tr>')
                    html.append('</table>')

        html.append('</body></html>')
        return '\n'.join(html)

    def _to_markdown(self) -> str:
        lines = [f"# CSSL {self.export_type.title()} Export",
                 f"\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"]

        if isinstance(self.data, dict):
            for section, items in self.data.items():
                if isinstance(items, dict) and items:
                    lines.append(f"\n## {section.title()}\n")
                    lines.append("| Name | Type | Details |")
                    lines.append("|------|------|---------|")
                    for name, info in items.items():
                        if isinstance(info, dict):
                            kind = info.get('type', '')
                            details = info.get('signature', info.get('value', ''))
                        else:
                            kind = str(info)
                            details = ''
                        lines.append(f"| `{name}` | {kind} | {details} |")

        return "\n".join(lines)
