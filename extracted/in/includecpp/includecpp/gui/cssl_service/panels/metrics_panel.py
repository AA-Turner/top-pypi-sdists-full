"""
CSSL Service Manager - Metrics Panel.
Canvas-based sparkline graphs for CPU, memory, objects, and call stats.
"""
import tkinter as tk
from tkinter import ttk
import time
from collections import deque
from typing import Dict, Optional
from .. import theme


class SparklineGraph(tk.Canvas):
    """Mini line graph (sparkline) for a single metric."""

    def __init__(self, parent, label: str, color: str, max_points: int = 60,
                 unit: str = "", **kwargs):
        super().__init__(parent, bg=theme.SURFACE, highlightthickness=0,
                         height=50, **kwargs)
        self.label = label
        self.color = color
        self.unit = unit
        self._data = deque(maxlen=max_points)
        self._max_val = 1.0

    def add_point(self, value: float):
        """Add a data point and redraw."""
        self._data.append(value)
        if value > self._max_val:
            self._max_val = value * 1.2
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 20 or h < 20 or not self._data:
            return

        padding_top = 14
        padding_bottom = 4
        graph_h = h - padding_top - padding_bottom

        # Label
        self.create_text(4, 2, text=self.label, anchor="nw",
                         fill=theme.TEXT_DIM, font=theme.FONT_CODE_SMALL)

        # Current value
        current = self._data[-1] if self._data else 0
        val_text = f"{current:.1f}{self.unit}"
        self.create_text(w - 4, 2, text=val_text, anchor="ne",
                         fill=self.color, font=theme.FONT_CODE_SMALL)

        # Draw line
        if len(self._data) < 2:
            return

        points = []
        n = len(self._data)
        for i, val in enumerate(self._data):
            x = (i / max(n - 1, 1)) * (w - 4) + 2
            y = padding_top + graph_h - (val / max(self._max_val, 0.001)) * graph_h
            points.append((x, y))

        # Fill area under line
        fill_points = list(points) + [(points[-1][0], h - padding_bottom),
                                        (points[0][0], h - padding_bottom)]
        fill_color = self._blend_color(self.color, theme.SURFACE, 0.15)
        self.create_polygon(fill_points, fill=fill_color, outline="")

        # Draw line
        if len(points) >= 2:
            flat_points = [coord for p in points for coord in p]
            self.create_line(flat_points, fill=self.color, width=1.5, smooth=True)

        # Grid lines (subtle)
        for i in range(1, 4):
            y = padding_top + (graph_h * i / 4)
            self.create_line(0, y, w, y, fill=theme.BORDER, dash=(2, 4))

    def _blend_color(self, color1: str, color2: str, ratio: float) -> str:
        """Blend two hex colors."""
        try:
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            r = int(r1 * ratio + r2 * (1 - ratio))
            g = int(g1 * ratio + g2 * (1 - ratio))
            b = int(b1 * ratio + b2 * (1 - ratio))
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return color1

    def clear(self):
        self._data.clear()
        self._max_val = 1.0
        self.delete("all")


class MetricsPanel(ttk.Frame):
    """Performance metrics panel with sparkline graphs and stats."""

    def __init__(self, parent, app):
        super().__init__(parent, style="Surface.TFrame")
        self.app = app
        self._current_runtime: Optional[str] = None
        self._update_job = None
        self._monitoring = False
        self._build()

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=theme.CARD, height=28)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="  Metrics", font=theme.FONT_BOLD,
                 bg=theme.CARD, fg=theme.TEXT_DIM).pack(side="left")

        self.monitor_btn = tk.Label(header, text="\u25B6 Monitor", font=theme.FONT_SMALL,
                                     bg=theme.CARD, fg=theme.TEXT_MUTED, cursor="hand2", padx=4)
        self.monitor_btn.pack(side="right")
        self.monitor_btn.bind("<Button-1>", lambda e: self._toggle_monitoring())

        # ── Graphs ──
        graphs_frame = ttk.Frame(self, style="Surface.TFrame")
        graphs_frame.pack(fill="both", expand=True, padx=4, pady=2)

        self.cpu_graph = SparklineGraph(graphs_frame, "CPU %", theme.BLUE, unit="%")
        self.cpu_graph.pack(fill="x", pady=1)

        self.mem_graph = SparklineGraph(graphs_frame, "Memory MB", theme.GREEN, unit="MB")
        self.mem_graph.pack(fill="x", pady=1)

        self.objects_graph = SparklineGraph(graphs_frame, "Objects", theme.ACCENT, unit="")
        self.objects_graph.pack(fill="x", pady=1)

        # ── Stats text ──
        stats_frame = tk.Frame(self, bg=theme.SURFACE)
        stats_frame.pack(fill="x", padx=4, pady=(2, 4))

        self.stats_labels = {}
        stats = [("Uptime", "0s"), ("Total Objects", "0"), ("GC Runs", "0")]
        for name, default in stats:
            row = tk.Frame(stats_frame, bg=theme.SURFACE)
            row.pack(fill="x")
            tk.Label(row, text=f"{name}:", font=theme.FONT_CODE_SMALL,
                     bg=theme.SURFACE, fg=theme.TEXT_DIM, width=14, anchor="w").pack(side="left")
            lbl = tk.Label(row, text=default, font=theme.FONT_CODE_SMALL,
                           bg=theme.SURFACE, fg=theme.TEXT, anchor="w")
            lbl.pack(side="left")
            self.stats_labels[name] = lbl

    def set_runtime(self, runtime_id: str):
        """Set the runtime to monitor."""
        self._current_runtime = runtime_id
        self.cpu_graph.clear()
        self.mem_graph.clear()
        self.objects_graph.clear()

    def _toggle_monitoring(self):
        self._monitoring = not self._monitoring
        if self._monitoring:
            self.monitor_btn.configure(text="\u25A0 Stop", fg=theme.GREEN)
            self._update_metrics()
        else:
            self.monitor_btn.configure(text="\u25B6 Monitor", fg=theme.TEXT_MUTED)
            if self._update_job:
                self.after_cancel(self._update_job)
                self._update_job = None

    def _update_metrics(self):
        """Fetch and display metrics."""
        if not self._monitoring:
            return

        if self._current_runtime:
            info = self.app.runtimes.get(self._current_runtime)
            if info:
                self.cpu_graph.add_point(info.cpu_pct)
                self.mem_graph.add_point(info.memory_mb)

                # Update stats
                self.stats_labels["Uptime"].configure(text=info.uptime_str)

        # Redraw graphs
        self.cpu_graph.event_generate("<Configure>")
        self.mem_graph.event_generate("<Configure>")
        self.objects_graph.event_generate("<Configure>")

        self._update_job = self.after(2000, self._update_metrics)

    def update_stats(self, data: dict):
        """Update stats from introspection data."""
        if "gc_counts" in data:
            counts = data["gc_counts"]
            self.stats_labels["GC Runs"].configure(text=str(sum(counts) if isinstance(counts, (list, tuple)) else counts))
        if "objects_tracked" in data:
            self.stats_labels["Total Objects"].configure(text=str(data["objects_tracked"]))
            self.objects_graph.add_point(data["objects_tracked"])

    def clear(self):
        self.cpu_graph.clear()
        self.mem_graph.clear()
        self.objects_graph.clear()
        for lbl in self.stats_labels.values():
            lbl.configure(text="0")
