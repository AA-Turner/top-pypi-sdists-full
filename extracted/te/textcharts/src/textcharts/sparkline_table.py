"""ASCII sparkline table for compact multi-metric comparison."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

from textcharts.base import ChartBase, ChartOptions, ColorMode

logger = logging.getLogger(__name__)

# Vertical block characters for sparkline bars (ascending height)
_SPARK_BLOCKS_UNICODE = (" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇")
_SPARK_BLOCKS_ASCII = (" ", ".", ":", "|")


@dataclass
class SparklineColumn:
    """A single metric column in the sparkline table."""

    name: str
    values: dict[str, float]  # row name -> value
    higher_is_better: bool = False  # True for success rate, False for latency


@dataclass
class SparklineTableData:
    """Complete data for a sparkline table."""

    rows: list[str]
    columns: list[SparklineColumn] = field(default_factory=list)


class SparklineTable(ChartBase):
    """Sparkline table showing compact multi-metric comparison.

    Each row is an entry, each column is a metric with an inline sparkline
    bar showing the relative value. Best values are highlighted.

    Example output:
    ```
    Comparison Overview
    ──────────────────────────────────────────────────────────────
    Row        Total(ms)   GeoMean    P99(ms)   Load(s)   Success
    DuckDB     ▇  1,240    ▇  56      ▅ 120     ▂  2.1    ████ 100%
    Polars     ▆  1,580    ▆  72      ▇ 310     ▁  1.2    ████ 100%
    SQLite     ▃  4,820    ▃ 219      ▃ 450     ▅  8.4    ███░  95%
    ```
    """

    def __init__(
        self,
        data: SparklineTableData,
        title: str | None = None,
        options: ChartOptions | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
    ):
        super().__init__(options, subtitle=subtitle, title=title, subject=subject)
        self.data = data
        self.title = self._compose_title("Comparison Overview")

    def render(self) -> str:
        """Render the sparkline table as a string."""
        self._detect_capabilities()

        if not self.data.rows or not self.data.columns:
            return "No data to display"

        colors = self.options.get_colors()
        width = self.options.get_effective_width()
        use_unicode = self.options.use_unicode

        blocks = _SPARK_BLOCKS_UNICODE if use_unicode else _SPARK_BLOCKS_ASCII

        min_metric_col_width = 10
        max_row_col_width = max(9, width - min_metric_col_width)
        row_col_width = min(max_row_col_width, max(len(p) for p in self.data.rows) + 1)

        visible_columns = self._select_visible_columns(width, row_col_width)

        lines: list[str] = []

        # Title and subtitle
        lines.append(self._render_title(self.title, width))
        subtitle = self._render_subtitle(width)
        if subtitle:
            lines.append(subtitle)
        lines.append(self._render_horizontal_line(width))

        # Header row
        header = "Row".ljust(row_col_width)
        for col, col_width in visible_columns:
            header += col.name.center(col_width)
        lines.append(header)

        # Normalize each column
        col_normalized, col_best, col_worst = self._normalize_columns(visible_columns)

        # Data rows
        no_color = not self.options.use_color
        row_labels = self._build_row_labels(self.data.rows, row_col_width - 1)
        for row_name in self.data.rows:
            row = row_labels.get(row_name, self._truncate_label(row_name, row_col_width - 1)).ljust(
                row_col_width
            )

            for i, (col, col_width) in enumerate(visible_columns):
                cell = self._render_sparkline_cell(
                    row_name,
                    col,
                    col_width,
                    col_normalized[i],
                    col_best[i],
                    col_worst[i],
                    blocks,
                    no_color,
                    colors,
                )
                row += cell

            lines.append(row)

        lines.append(self._render_horizontal_line(width))

        best_block = blocks[-1] if blocks else "#"
        worst_block = blocks[1] if len(blocks) > 1 else "."
        if colors.color_mode != ColorMode.NONE:
            best_block = colors.colorize(best_block, fg_color="#1b9e77")
            worst_block = colors.colorize(worst_block, fg_color="#d95f02")
        lines.append(f"{best_block}=best  {worst_block}=worst  (bars scaled per column)")

        return "\n".join(lines)

    def _normalize_columns(
        self, visible_columns: list[tuple[SparklineColumn, int]]
    ) -> tuple[list[dict[str, float]], list[str | None], list[str | None]]:
        """Normalize values for each visible column and identify best/worst rows."""
        col_normalized: list[dict[str, float]] = []
        col_best: list[str | None] = []
        col_worst: list[str | None] = []

        for col, _ in visible_columns:
            vals = {p: col.values.get(p, 0) for p in self.data.rows}
            valid_vals = [v for v in vals.values() if isinstance(v, (int, float)) and math.isfinite(v)]
            if not valid_vals:
                col_normalized.append(dict.fromkeys(self.data.rows, 0.0))
                col_best.append(None)
                col_worst.append(None)
                continue

            min_v, max_v = min(valid_vals), max(valid_vals)
            rng = max_v - min_v if max_v > min_v else 1.0

            normalized = {}
            for p in self.data.rows:
                v = vals.get(p, 0)
                if not isinstance(v, (int, float)) or not math.isfinite(v):
                    normalized[p] = 0.0
                    continue
                norm = (v - min_v) / rng if rng > 0 else 0.5
                if not col.higher_is_better:
                    norm = 1.0 - norm
                normalized[p] = norm

            col_normalized.append(normalized)

            finite_rows = [p for p in self.data.rows if isinstance(vals[p], (int, float)) and math.isfinite(vals[p])]
            if col.higher_is_better:
                col_best.append(max(finite_rows, key=lambda p: vals[p]))
                col_worst.append(min(finite_rows, key=lambda p: vals[p]))
            else:
                col_best.append(min(finite_rows, key=lambda p: vals[p]))
                col_worst.append(max(finite_rows, key=lambda p: vals[p]))

        return col_normalized, col_best, col_worst

    def _render_sparkline_cell(
        self,
        row_name: str,
        col: SparklineColumn,
        col_width: int,
        normalized: dict[str, float],
        best: str | None,
        worst: str | None,
        blocks: tuple[str, ...] | list[str],
        no_color: bool,
        colors: object,
    ) -> str:
        """Render a single sparkline table cell with block char and value."""
        norm = normalized.get(row_name, 0)
        if not math.isfinite(norm):
            norm = 0.0
        val = col.values.get(row_name, 0)

        block_idx = min(len(blocks) - 1, max(0, int(norm * (len(blocks) - 1))))
        block_char = blocks[block_idx]
        val_str = self._format_compact_value(val)

        if no_color and row_name == best:
            cell = f"{block_char}+{val_str}"
        elif no_color and row_name == worst:
            cell = f"{block_char}-{val_str}"
        else:
            cell = f"{block_char} {val_str}"
        padded_cell = cell.ljust(col_width)
        if row_name == best:
            padded_cell = colors.colorize(padded_cell, fg_color="#1b9e77")
        elif row_name == worst:
            padded_cell = colors.colorize(padded_cell, fg_color="#d95f02")

        return padded_cell

    def _select_visible_columns(self, width: int, row_col_width: int) -> list[tuple[SparklineColumn, int]]:
        """Select which columns fit within the terminal width."""
        available = width - row_col_width
        min_col_width = 10
        result: list[tuple[SparklineColumn, int]] = []

        for col in self.data.columns:
            # Calculate needed width: max of header and value widths
            col_width = max(min_col_width, len(col.name) + 2)
            if available >= col_width:
                result.append((col, col_width))
                available -= col_width

        return result

    def _build_row_labels(self, rows: list[str], max_label_len: int) -> dict[str, str]:
        """Build visible row labels and disambiguate truncation collisions."""
        labels = {row: self._truncate_label(row, max_label_len) for row in rows}

        buckets: dict[str, list[str]] = {}
        for row, label in labels.items():
            buckets.setdefault(label, []).append(row)

        for label, names in buckets.items():
            if len(names) <= 1:
                continue

            # Resolve collisions deterministically: reserve space for a suffix
            # and keep as much of each original name as possible.
            for i, row in enumerate(sorted(names), start=1):
                suffix = f"~{i}"
                base_len = max(1, max_label_len - len(suffix))
                base = self._truncate_label(row, base_len)
                labels[row] = (base + suffix)[:max_label_len]

        return labels

    @staticmethod
    def _format_compact_value(val: float) -> str:
        """Format a value compactly for table display."""
        if not math.isfinite(val):
            return "N/A"
        if val == 0:
            return "0"
        if val >= 10_000:
            return f"{val / 1_000:.0f}k"
        if val >= 1_000:
            return f"{val:,.0f}"
        if val >= 100:
            return f"{val:.0f}"
        if val >= 10:
            return f"{val:.1f}"
        if val >= 1:
            return f"{val:.2f}"
        return f"{val:.3f}"


def from_data(
    rows: list[str],
    metrics: list[tuple[str, dict[str, float], bool]],
    title: str | None = None,
    options: ChartOptions | None = None,
    subject: str | None = None,
) -> SparklineTable:
    """Create SparklineTable from metric data.

    Args:
        rows: List of row names.
        metrics: List of (metric_name, {row: value}, higher_is_better) tuples.
        title: Optional chart title.
        options: Chart rendering options.

    Returns:
        Configured SparklineTable instance.
    """
    columns = [SparklineColumn(name=name, values=values, higher_is_better=hib) for name, values, hib in metrics]
    data = SparklineTableData(rows=rows, columns=columns)
    return SparklineTable(data=data, title=title, options=options, subject=subject)
