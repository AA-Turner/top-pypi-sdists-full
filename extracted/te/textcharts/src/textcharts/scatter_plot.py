"""ASCII scatter plot for two-dimensional data."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

from textcharts.base import ChartBase, ChartOptions, ColorMode, robust_p95

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass
class ScatterPoint:
    """Data point for scatter plot."""

    name: str
    x: float
    y: float
    is_pareto: bool = False


class ScatterPlot(ChartBase):
    """ASCII scatter plot for two-dimensional data visualization.

    Example output:
    ```
    Cost vs Performance
    ────────────────────────────────────────
    Perf │
    (qph)│                           * DuckDB
     300 │                     ◆ Polars
         │               ─────────────*
     200 │         * Pandas      Pareto frontier
         │    * SQLite
     100 │
         │
       0 └───────────────────────────────────
         $0      $50     $100    $150    $200
                      Cost (USD)

    Legend: * = platform, ◆ = Pareto optimal
    ```
    """

    # Point markers follow the same rotating pattern used by CDF/Line charts.
    MARKERS = ("*", "+", "o", "x", "^", "v", "#", "@")
    MARKER_FRONTIER = "─"

    def __init__(
        self,
        points: Sequence[ScatterPoint],
        title: str | None = None,
        x_label: str = "X",
        y_label: str = "Y",
        show_pareto: bool = True,
        options: ChartOptions | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
    ):
        super().__init__(options, subtitle=subtitle, title=title, subject=subject)
        self.points = list(points)
        self.title = self._compose_title("Scatter Plot")
        self.x_label = x_label
        self.y_label = y_label
        self.show_pareto = show_pareto
        self._truncation_active = False
        self._x_cap: float = float("inf")
        self._y_cap: float = float("inf")

    def render(self) -> str:
        """Render the scatter plot as a string."""
        self._detect_capabilities()

        if not self.points:
            return "No data to display"

        colors = self.options.get_colors()
        box_chars = self.options.get_box_chars()
        width = self.options.get_effective_width()

        # Compute Pareto frontier if requested
        pareto_points = self._compute_pareto() if self.show_pareto else []
        pareto_names = {p.name for p in pareto_points}

        # Update is_pareto flags
        for p in self.points:
            p.is_pareto = p.name in pareto_names

        # Find data bounds (filter NaN/Inf)
        x_values = [p.x for p in self.points if math.isfinite(p.x)]
        y_values = [p.y for p in self.points if math.isfinite(p.y)]
        if not x_values or not y_values:
            return "No data to display"

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        # Cap axes at P95×2 so one extreme point doesn't waste plot area
        self._truncation_active = False
        self._x_cap = float("inf")
        self._y_cap = float("inf")
        explicit_x = self._resolve_outlier_cap(x_max)
        explicit_y = self._resolve_outlier_cap(y_max)
        if explicit_x is not None:
            x_max, x_truncated = explicit_x
            if x_truncated:
                self._x_cap = x_max
                self._truncation_active = True
        elif len(self.points) >= 5:
            p95_x = robust_p95(x_values)
            if p95_x > 0 and x_max > p95_x * 3:
                x_max = p95_x * 2
                self._x_cap = x_max
                self._truncation_active = True
        if explicit_y is not None:
            y_max, y_truncated = explicit_y
            if y_truncated:
                self._y_cap = y_max
                self._truncation_active = True
        elif len(self.points) >= 5:
            p95_y = robust_p95(y_values)
            if p95_y > 0 and y_max > p95_y * 3:
                y_max = p95_y * 2
                self._y_cap = y_max
                self._truncation_active = True

        # Add padding
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        x_min -= x_range * 0.05
        x_max += x_range * 0.05
        y_min -= y_range * 0.05
        y_max += y_range * 0.05

        lines: list[str] = []

        # Title and subtitle
        if self.options.title or self.title:
            lines.append(self._render_title(self.options.title or self.title, width))
            subtitle = self._render_subtitle(width)
            if subtitle:
                lines.append(subtitle)
            lines.append(self._render_horizontal_line(width))

        # Plot dimensions
        y_axis_width = 8  # Space for y-axis labels
        plot_width = width - y_axis_width - 2
        plot_height = 15  # Fixed height for now

        if plot_width < 20:
            plot_width = 20

        # Create plot grid
        grid: list[list[str]] = [[" " for _ in range(plot_width)] for _ in range(plot_height)]

        # Pareto frontier line character follows the configured character set
        frontier_mark = self.MARKER_FRONTIER if self.options._has_unicode() else "-"

        # Helper to convert data coords to grid coords
        def to_grid(x: float, y: float) -> tuple[int, int]:
            gx = int((x - x_min) / (x_max - x_min) * (plot_width - 1))
            gy = int((y - y_min) / (y_max - y_min) * (plot_height - 1))
            # Invert y since grid row 0 is top
            gy = plot_height - 1 - gy
            return max(0, min(plot_width - 1, gx)), max(0, min(plot_height - 1, gy))

        palette = list(self.options.get_palette())
        point_styles = {
            point.name: (
                self.MARKERS[i % len(self.MARKERS)],
                palette[i % len(palette)],
            )
            for i, point in enumerate(self.points)
        }

        # Plot Pareto frontier line first (so points overlay it)
        finite_pareto = [p for p in pareto_points if math.isfinite(p.x) and math.isfinite(p.y)]
        if self.show_pareto and len(finite_pareto) >= 2:
            sorted_pareto = sorted(finite_pareto, key=lambda p: p.x)
            for i in range(len(sorted_pareto) - 1):
                p1 = sorted_pareto[i]
                p2 = sorted_pareto[i + 1]
                gx1, gy1 = to_grid(p1.x, p1.y)
                gx2, gy2 = to_grid(p2.x, p2.y)

                # Draw simple line between points
                steps = max(abs(gx2 - gx1), abs(gy2 - gy1), 1)
                for step in range(steps + 1):
                    t = step / steps
                    lx = int(gx1 + t * (gx2 - gx1))
                    ly = int(gy1 + t * (gy2 - gy1))
                    if 0 <= lx < plot_width and 0 <= ly < plot_height:
                        if grid[ly][lx] == " ":
                            grid[ly][lx] = frontier_mark

        # Plot points (skip NaN/Inf)
        point_positions: dict[tuple[int, int], list[ScatterPoint]] = {}
        for point in self.points:
            if not math.isfinite(point.x) or not math.isfinite(point.y):
                continue
            gx, gy = to_grid(point.x, point.y)
            key = (gx, gy)
            if key not in point_positions:
                point_positions[key] = []
            point_positions[key].append(point)

        for (gx, gy), pts in point_positions.items():
            # Use first point's properties for marker
            marker, _ = point_styles[pts[0].name]
            grid[gy][gx] = marker

        # Build output with y-axis
        y_step = (y_max - y_min) / max(1, plot_height - 1)

        for row_idx, row in enumerate(grid):
            y_val = y_max - row_idx * y_step
            y_label = self._format_value(y_val).rjust(y_axis_width - 1)

            if row_idx == 0:
                axis_char = box_chars["tr"]
            elif row_idx == plot_height - 1:
                axis_char = box_chars["br"]
            else:
                axis_char = box_chars["v"]

            # Colorize grid cells individually to avoid str.replace() collisions
            if colors.color_mode != ColorMode.NONE:
                colored_cells = []
                for cell in row:
                    marker_match = next((style for style in point_styles.values() if style[0] == cell), None)
                    if marker_match is not None:
                        _, color = marker_match
                        colored_cells.append(colors.colorize(cell, fg_color=color))
                    elif cell == frontier_mark:
                        colored_cells.append(colors.colorize(cell, fg_color="#666666"))
                    else:
                        colored_cells.append(cell)
                row_content = "".join(colored_cells)
            else:
                row_content = "".join(row)

            lines.append(f"{y_label}{axis_char}{row_content}")

        # X-axis
        x_axis = " " * y_axis_width + box_chars["bl"] + box_chars["h"] * plot_width
        lines.append(x_axis)

        # X-axis labels
        x_labels_line = " " * y_axis_width + " "
        x_step = (x_max - x_min) / 4
        for i in range(5):
            x_val = x_min + i * x_step
            label = self._format_value(x_val)
            pos = int(i * (plot_width - 1) / 4)
            # Center label at position
            start = pos - len(label) // 2
            if start >= 0:
                x_labels_line = (
                    x_labels_line[: y_axis_width + 1 + start]
                    + label
                    + x_labels_line[y_axis_width + 1 + start + len(label) :]
                )

        # Ensure x_labels_line is right length
        x_labels_line = x_labels_line[:width]
        lines.append(x_labels_line)

        # Axis labels
        lines.append("")
        lines.append(self._render_compact_axis_labels(self.y_label, self.x_label, width))

        # Legend with point names
        lines.append("")
        lines.append("Points:")
        for point in self.points:
            marker, color = point_styles[point.name]
            if colors.color_mode != ColorMode.NONE:
                marker_colored = colors.colorize(marker, fg_color=color)
            else:
                marker_colored = marker
            pareto_note = " (Pareto optimal)" if point.is_pareto else ""
            is_truncated = self._truncation_active and (point.x > self._x_cap or point.y > self._y_cap)
            truncated_note = f" {self._truncation_marker()}" if is_truncated else ""
            x_val = self._format_value(point.x)
            y_val = self._format_value(point.y)
            lines.append(f"  {marker_colored} {point.name}: x={x_val}, y={y_val}{pareto_note}{truncated_note}")

        return "\n".join(lines)

    def _compute_pareto(self) -> list[ScatterPoint]:
        """Compute Pareto frontier (higher y is better, lower x is better)."""
        finite = [p for p in self.points if math.isfinite(p.x) and math.isfinite(p.y)]
        sorted_points = sorted(finite, key=lambda p: (p.x, -p.y))
        frontier: list[ScatterPoint] = []
        best_y = float("-inf")

        for point in sorted_points:
            if point.y >= best_y:
                frontier.append(point)
                best_y = point.y

        return frontier


def from_points(
    points: Sequence,
    title: str | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    show_pareto: bool = True,
    options: ChartOptions | None = None,
    subject: str | None = None,
) -> ScatterPlot:
    """Create ScatterPlot from objects with name/x/y attributes."""
    converted: list[ScatterPoint] = []
    for item in points:
        if isinstance(item, ScatterPoint):
            converted.append(item)
        else:
            converted.append(
                ScatterPoint(
                    name=getattr(item, "name", str(item)),
                    x=getattr(item, "x", 0),
                    y=getattr(item, "y", 0),
                )
            )

    return ScatterPlot(
        points=converted,
        title=title,
        x_label=x_label,
        y_label=y_label,
        show_pareto=show_pareto,
        options=options,
        subject=subject,
    )
