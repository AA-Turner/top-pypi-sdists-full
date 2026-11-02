"""ASCII summary box renderer for aggregate statistics."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

from textcharts.base import ChartBase, ChartOptions, TerminalColors


@dataclass
class SummaryStats:
    """Aggregate statistics for a summary box.

    For single-run summaries, only the primary fields are used.
    For comparison summaries, both baseline and comparison fields are used.
    """

    title: str = "Summary"

    # Aggregate metrics
    primary_value: float | None = None
    secondary_value: float | None = None
    total_value: float | None = None

    # Comparison metrics (only for two-run comparisons)
    primary_baseline: float | None = None
    primary_comparison: float | None = None
    total_baseline: float | None = None
    total_comparison: float | None = None
    baseline_name: str = "Baseline"
    comparison_name: str = "Comparison"

    # Counts
    num_items: int = 0
    num_improved: int = 0
    num_stable: int = 0
    num_regressed: int = 0

    # Best/worst items
    best_items: list[tuple[str, float]] = field(default_factory=list)
    worst_items: list[tuple[str, float]] = field(default_factory=list)

    # Configurable rendered labels
    primary_label: str = "Primary"
    secondary_label: str = "Secondary"
    total_label: str = "Total"
    count_label: str = "Items"

    # Unit label for metric values (e.g. "ms", "ops", "requests")
    metric_label: str = "ms"

    # Optional callback for custom value formatting; overrides built-in formatting
    value_formatter: Callable[[float], str] | None = None

    # Whether lower metric values are better (True for latency, False for throughput)
    lower_is_better: bool = True

    # System environment info (displayed in middle column)
    environment: dict[str, str] | None = None

    # Platform/run configuration (displayed in right column)
    platform_config: dict[str, str] | None = None

    @property
    def is_comparison(self) -> bool:
        """Whether this is a comparison summary (two runs)."""
        return self.primary_baseline is not None or self.total_baseline is not None


class SummaryBox(ChartBase):
    """Bordered summary panel with aggregate statistics.

    Displays key metrics in a box-drawing bordered panel. Supports
    both single-run and comparison summaries.

    Example output:
    ```
    ┌──────────────────────────────────────┐
    │            Summary                   │
    ├──────────────────────────────────────┤
    │  Primary:  142.3ms → 98.7ms  -30.6% │
    │  Total:    3.2s → 2.1s       -34.4% │
    ├──────────────────────────────────────┤
    │  5 improved  12 stable  5 regressed  │
    ├──────────────────────────────────────┤
    │  Best:  Q6 (-57.2%), Q14 (-38.1%)   │
    │  Worst: Q21 (+726%), Q17 (+23.4%)   │
    └──────────────────────────────────────┘
    ```
    """

    def __init__(
        self,
        stats: SummaryStats,
        options: ChartOptions | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
    ):
        super().__init__(options, subtitle=subtitle, subject=subject)
        self.stats = stats
        if subject and stats.title == "Summary":
            self.stats.title = f"{subject} Summary"

    # Minimum inner width required for two-column layout
    _MIN_TWO_COL_INNER = 56
    # Minimum inner width required for three-column layout
    _MIN_THREE_COL_INNER = 80

    def render(self) -> str:
        """Render the summary box as a string."""
        self._detect_capabilities()

        colors = self.options.get_colors()
        box = self.options.get_box_chars()
        width = self.options.get_effective_width()

        inner = max(20, width - 4)
        three_col = self.stats.environment and self.stats.platform_config and inner >= self._MIN_THREE_COL_INNER
        two_col = self.stats.environment and inner >= self._MIN_TWO_COL_INNER

        lines: list[str] = []

        # Top border + title
        lines.append(f"{box['tl']}{box['h'] * (inner + 2)}{box['tr']}")
        title_text = self._truncate_label(self.stats.title, inner)
        bold_title = colors.bold() + title_text.center(inner) + colors.reset()
        lines.append(f"{box['v']} {bold_title} {box['v']}")

        if self.subtitle:
            sub_text = self._sanitize_text(self.subtitle)
            sub_text = self._truncate_label(sub_text, inner)
            dim_sub = colors.colorize(sub_text.center(inner), fg_color="#666666")
            lines.append(f"{box['v']} {dim_sub} {box['v']}")

        # Metrics section
        if three_col:
            lines.extend(self._render_three_col_metrics(box, colors, inner))
        elif two_col:
            lines.extend(self._render_two_col_metrics(box, colors, inner))
        else:
            lines.append(f"{box['lm']}{box['h'] * (inner + 2)}{box['rm']}")
            if self.stats.is_comparison:
                lines.extend(self._render_comparison_metrics(box, colors, inner))
            else:
                lines.extend(self._render_single_metrics(box, colors, inner))

        # Comparison counts
        if self.stats.is_comparison and self.stats.num_items > 0:
            lines.extend(self._render_counts_row(box, colors, inner, two_col or three_col))

        # Best/worst queries
        lines.extend(self._render_best_worst(box, colors, inner, two_col or three_col))

        # Bottom border
        lines.append(f"{box['bl']}{box['h'] * (inner + 2)}{box['br']}")

        return "\n".join(lines)

    def _render_two_col_metrics(self, box: dict[str, str], colors: TerminalColors, inner: int) -> list[str]:
        """Render metrics in a two-column layout with environment info."""
        assert self.stats.environment is not None
        lines: list[str] = []
        left_width = inner * 5 // 9
        right_width = inner - left_width - 1

        lines.append(f"{box['lm']}{box['h'] * (left_width + 1)}{box['tm']}{box['h'] * (right_width + 1)}{box['rm']}")

        if self.stats.is_comparison:
            metric_lines = self._build_metric_texts_comparison(colors)
        else:
            metric_lines = self._build_metric_texts_single()
        env_lines = self._build_env_lines(colors)
        env_lines_visible = self._build_env_lines_visible()
        # Merge platform config into environment column when 3-col isn't available
        if self.stats.platform_config:
            env_lines.extend(self._build_config_lines(colors))
            env_lines_visible.extend(self._build_config_lines_visible())

        row_count = max(len(metric_lines), len(env_lines))
        while len(metric_lines) < row_count:
            metric_lines.append("")
        while len(env_lines) < row_count:
            env_lines.append("")
            env_lines_visible.append("")

        for left_text, right_text, right_visible_text in zip(metric_lines, env_lines, env_lines_visible):
            left_visible_text = self._sanitize_text(left_text)
            if len(left_visible_text) > left_width:
                left_visible_text = self._truncate_label(left_visible_text, left_width)
                left_text = left_visible_text
            if len(right_visible_text) > right_width:
                right_visible_text = self._truncate_label(right_visible_text, right_width)
                right_text = right_visible_text
            left_pad = max(0, left_width - len(left_visible_text))
            right_pad = max(0, right_width - len(right_visible_text))
            lines.append(f"{box['v']} {left_text}{' ' * left_pad}{box['v']} {right_text}{' ' * right_pad}{box['v']}")

        lines.append(f"{box['lm']}{box['h'] * (left_width + 1)}{box['bm']}{box['h'] * (right_width + 1)}{box['rm']}")
        return lines

    def _render_three_col_metrics(self, box: dict[str, str], colors: TerminalColors, inner: int) -> list[str]:
        """Render metrics in a three-column layout: metrics | environment | config."""
        assert self.stats.environment is not None
        assert self.stats.platform_config is not None
        lines: list[str] = []

        col1_w = inner * 4 // 10
        col2_w = inner * 3 // 10
        col3_w = inner - col1_w - col2_w - 3  # -3 for two internal column separators (┬ + space each)

        # Separator after title: ├────┬────┬────┤
        lines.append(
            f"{box['lm']}{box['h'] * (col1_w + 1)}{box['tm']}"
            f"{box['h'] * (col2_w + 1)}{box['tm']}"
            f"{box['h'] * (col3_w + 1)}{box['rm']}"
        )

        if self.stats.is_comparison:
            metric_lines = self._build_metric_texts_comparison(colors)
        else:
            metric_lines = self._build_metric_texts_single()
        env_lines = self._build_env_lines(colors)
        env_visible = self._build_env_lines_visible()
        cfg_lines = self._build_config_lines(colors)
        cfg_visible = self._build_config_lines_visible()

        row_count = max(len(metric_lines), len(env_lines), len(cfg_lines))
        while len(metric_lines) < row_count:
            metric_lines.append("")
        while len(env_lines) < row_count:
            env_lines.append("")
            env_visible.append("")
        while len(cfg_lines) < row_count:
            cfg_lines.append("")
            cfg_visible.append("")

        for m_text, e_text, e_vis, c_text, c_vis in zip(metric_lines, env_lines, env_visible, cfg_lines, cfg_visible):
            m_vis = self._sanitize_text(m_text)
            if len(m_vis) > col1_w:
                m_vis = self._truncate_label(m_vis, col1_w)
                m_text = m_vis
            if len(e_vis) > col2_w:
                e_vis = self._truncate_label(e_vis, col2_w)
                e_text = e_vis
            if len(c_vis) > col3_w:
                c_vis = self._truncate_label(c_vis, col3_w)
                c_text = c_vis
            m_pad = max(0, col1_w - len(m_vis))
            e_pad = max(0, col2_w - len(e_vis))
            c_pad = max(0, col3_w - len(c_vis))
            lines.append(
                f"{box['v']} {m_text}{' ' * m_pad}"
                f"{box['v']} {e_text}{' ' * e_pad}"
                f"{box['v']} {c_text}{' ' * c_pad}{box['v']}"
            )

        # Bottom separator: ├────┴────┴────┤
        lines.append(
            f"{box['lm']}{box['h'] * (col1_w + 1)}{box['bm']}"
            f"{box['h'] * (col2_w + 1)}{box['bm']}"
            f"{box['h'] * (col3_w + 1)}{box['rm']}"
        )
        return lines

    def _render_counts_row(self, box: dict[str, str], colors: TerminalColors, inner: int, two_col: bool) -> list[str]:
        """Render the improved/stable/regressed counts row."""
        lines: list[str] = []
        no_color = not self.options.use_color
        if not two_col:
            lines.append(f"{box['lm']}{box['h'] * (inner + 2)}{box['rm']}")

        down_arrow = "\u2193" if self.options.use_unicode else "v"
        up_arrow = "\u2191" if self.options.use_unicode else "^"
        improved_text = f"{self.stats.num_improved} improved"
        regressed_text = f"{self.stats.num_regressed} regressed"
        if no_color:
            improved_text = f"{down_arrow}{improved_text}"
            regressed_text = f"{up_arrow}{regressed_text}"
        imp_color = "#66a61e" if self.stats.lower_is_better else "#d95f02"
        reg_color = "#d95f02" if self.stats.lower_is_better else "#66a61e"
        improved = colors.colorize(improved_text, fg_color=imp_color)
        regressed = colors.colorize(regressed_text, fg_color=reg_color)
        counts_text = f"{improved}  {self.stats.num_stable} stable  {regressed}"
        visible_len = len(improved_text) + 2 + len(f"{self.stats.num_stable} stable") + 2 + len(regressed_text)
        padding = max(0, inner - visible_len)
        lines.append(f"{box['v']} {counts_text}{' ' * padding} {box['v']}")
        return lines

    def _render_best_worst(self, box: dict[str, str], colors: TerminalColors, inner: int, two_col: bool) -> list[str]:
        """Render the best and worst item rows."""
        if not self.stats.best_items and not self.stats.worst_items:
            return []

        lines: list[str] = []
        no_color = not self.options.use_color

        if not (two_col and not self.stats.is_comparison):
            lines.append(f"{box['lm']}{box['h'] * (inner + 2)}{box['rm']}")

        if self.stats.best_items:
            lines.append(
                self._render_query_line(
                    self.stats.best_items,
                    "Best",
                    "#66a61e",
                    box,
                    colors,
                    inner,
                    no_color,
                    is_down=True,
                )
            )

        if self.stats.worst_items:
            lines.append(
                self._render_query_line(
                    self.stats.worst_items,
                    "Worst",
                    "#d95f02",
                    box,
                    colors,
                    inner,
                    no_color,
                    is_down=False,
                )
            )

        return lines

    def _render_query_line(
        self,
        queries: list[tuple[str, float]],
        label_text: str,
        color: str,
        box: dict[str, str],
        colors: TerminalColors,
        inner: int,
        no_color: bool,
        *,
        is_down: bool,
    ) -> str:
        """Render a single best/worst query line."""
        items = ", ".join(
            f"{q} ({v:+.1f}%)" if self.stats.is_comparison else f"{q} ({self._format_metric(v)})"
            for q, v in queries[:3]
        )
        arrow = (
            ("\u2193" if self.options.use_unicode else "v")
            if is_down
            else ("\u2191" if self.options.use_unicode else "^")
        )
        label = f"{arrow}{label_text}: " if no_color else f"{label_text}: "
        items = self._truncate_label(items, max(0, inner - len(label)))
        visible_len = len(label) + len(items)
        padding = max(0, inner - visible_len)
        colored_label = colors.colorize(label, fg_color=color) + items
        return f"{box['v']} {colored_label}{' ' * padding} {box['v']}"

    def _label_width(self) -> int:
        """Compute padding width from the longest configured label."""
        labels = [
            self.stats.primary_label,
            self.stats.secondary_label,
            self.stats.total_label,
            self.stats.count_label,
        ]
        return max(len(lbl) for lbl in labels) + 1  # +1 for the colon

    def _render_comparison_metrics(
        self,
        box: dict[str, str],
        colors: TerminalColors,
        inner: int,
    ) -> list[str]:
        """Render comparison metrics (two runs)."""
        lines: list[str] = []
        lw = self._label_width()

        if self.stats.primary_baseline is not None and self.stats.primary_comparison is not None:
            b_val = self.stats.primary_baseline
            c_val = self.stats.primary_comparison
            pct = ((c_val - b_val) / b_val * 100) if b_val != 0 else 0.0
            arrow = "\u2192" if self.options.use_unicode else "->"
            label_part = f"{self.stats.primary_label}:".ljust(lw + 1)
            metric_text = (
                f"{label_part}{self._format_value(b_val)}{self.stats.metric_label}"
                f" {arrow} {self._format_value(c_val)}{self.stats.metric_label}"
            )
            pct_text = self._format_pct_colored(pct, colors)
            visible_len = len(metric_text) + len(self._format_pct_visible(pct))
            padding = max(0, inner - visible_len)
            leader = self._dot_leader(padding, colors)
            lines.append(f"{box['v']} {metric_text}{leader}{pct_text} {box['v']}")

        if self.stats.total_baseline is not None and self.stats.total_comparison is not None:
            b_val = self.stats.total_baseline
            c_val = self.stats.total_comparison
            pct = ((c_val - b_val) / b_val * 100) if b_val != 0 else 0.0
            arrow = "\u2192" if self.options.use_unicode else "->"
            b_str = self._format_metric(b_val)
            c_str = self._format_metric(c_val)
            label_part = f"{self.stats.total_label}:".ljust(lw + 1)
            metric_text = f"{label_part}{b_str} {arrow} {c_str}"
            pct_text = self._format_pct_colored(pct, colors)
            visible_len = len(metric_text) + len(self._format_pct_visible(pct))
            padding = max(0, inner - visible_len)
            leader = self._dot_leader(padding, colors)
            lines.append(f"{box['v']} {metric_text}{leader}{pct_text} {box['v']}")

        if self.stats.num_items > 0:
            label_part = f"{self.stats.count_label}:".ljust(lw + 1)
            queries_text = f"{label_part}{self.stats.num_items}"
            padding = max(0, inner - len(queries_text))
            lines.append(f"{box['v']} {queries_text}{' ' * padding} {box['v']}")

        return lines

    def _render_single_metrics(
        self,
        box: dict[str, str],
        colors: TerminalColors,
        inner: int,
    ) -> list[str]:
        """Render single-run metrics."""
        lines: list[str] = []
        lw = self._label_width()

        if self.stats.primary_value is not None:
            label_part = f"{self.stats.primary_label}:".ljust(lw + 1)
            text = f"{label_part}{self._format_value(self.stats.primary_value)}{self.stats.metric_label}"
            padding = max(0, inner - len(text))
            lines.append(f"{box['v']} {text}{' ' * padding} {box['v']}")

        if self.stats.secondary_value is not None:
            label_part = f"{self.stats.secondary_label}:".ljust(lw + 1)
            text = f"{label_part}{self._format_value(self.stats.secondary_value)}{self.stats.metric_label}"
            padding = max(0, inner - len(text))
            lines.append(f"{box['v']} {text}{' ' * padding} {box['v']}")

        if self.stats.total_value is not None:
            label_part = f"{self.stats.total_label}:".ljust(lw + 1)
            text = f"{label_part}{self._format_metric(self.stats.total_value)}"
            padding = max(0, inner - len(text))
            lines.append(f"{box['v']} {text}{' ' * padding} {box['v']}")

        if self.stats.num_items > 0:
            label_part = f"{self.stats.count_label}:".ljust(lw + 1)
            text = f"{label_part}{self.stats.num_items}"
            padding = max(0, inner - len(text))
            lines.append(f"{box['v']} {text}{' ' * padding} {box['v']}")

        return lines

    def _build_metric_texts_single(self) -> list[str]:
        """Build plain metric text lines for single-run (no borders)."""
        texts: list[str] = []
        lw = self._label_width()
        if self.stats.primary_value is not None:
            label_part = f"{self.stats.primary_label}:".ljust(lw + 1)
            texts.append(f"{label_part}{self._format_value(self.stats.primary_value)}{self.stats.metric_label}")
        if self.stats.secondary_value is not None:
            label_part = f"{self.stats.secondary_label}:".ljust(lw + 1)
            texts.append(f"{label_part}{self._format_value(self.stats.secondary_value)}{self.stats.metric_label}")
        if self.stats.total_value is not None:
            label_part = f"{self.stats.total_label}:".ljust(lw + 1)
            texts.append(f"{label_part}{self._format_metric(self.stats.total_value)}")
        if self.stats.num_items > 0:
            label_part = f"{self.stats.count_label}:".ljust(lw + 1)
            texts.append(f"{label_part}{self.stats.num_items}")
        return texts

    def _build_metric_texts_comparison(self, colors: TerminalColors) -> list[str]:
        """Build plain metric text lines for comparison (no borders)."""
        texts: list[str] = []
        lw = self._label_width()
        arrow = "\u2192" if self.options.use_unicode else "->"
        if self.stats.primary_baseline is not None and self.stats.primary_comparison is not None:
            b, c = self.stats.primary_baseline, self.stats.primary_comparison
            pct = ((c - b) / b * 100) if b != 0 else 0.0
            pct_text = self._format_pct_colored(pct, colors)
            label_part = f"{self.stats.primary_label}:".ljust(lw + 1)
            texts.append(
                f"{label_part}{self._format_value(b)}{self.stats.metric_label}"
                f" {arrow} {self._format_value(c)}{self.stats.metric_label}"
                f" {pct_text}"
            )
        if self.stats.total_baseline is not None and self.stats.total_comparison is not None:
            b, c = self.stats.total_baseline, self.stats.total_comparison
            b_str, c_str = self._format_metric(b), self._format_metric(c)
            pct = ((c - b) / b * 100) if b != 0 else 0.0
            pct_text = self._format_pct_colored(pct, colors)
            label_part = f"{self.stats.total_label}:".ljust(lw + 1)
            texts.append(f"{label_part}{b_str} {arrow} {c_str} {pct_text}")
        if self.stats.num_items > 0:
            label_part = f"{self.stats.count_label}:".ljust(lw + 1)
            texts.append(f"{label_part}{self.stats.num_items}")
        return texts

    def _build_env_lines(self, colors: TerminalColors) -> list[str]:
        """Build environment info text lines for the right column."""
        if not self.stats.environment:
            return []
        lines: list[str] = []
        dim = colors.colorize
        for key, value in self.stats.environment.items():
            lines.append(f"{dim(f'{key}:', fg_color='#666666')} {value}")
        return lines

    def _build_env_lines_visible(self) -> list[str]:
        """Build environment lines with visible lengths (no ANSI) for width calculations."""
        if not self.stats.environment:
            return []
        return [f"{key}: {value}" for key, value in self.stats.environment.items()]

    def _build_config_lines(self, colors: TerminalColors) -> list[str]:
        """Build platform config text lines for the right column."""
        if not self.stats.platform_config:
            return []
        dim = colors.colorize
        return [f"{dim(f'{key}:', fg_color='#666666')} {value}" for key, value in self.stats.platform_config.items()]

    def _build_config_lines_visible(self) -> list[str]:
        """Build config lines with visible lengths (no ANSI) for width calculations."""
        if not self.stats.platform_config:
            return []
        return [f"{key}: {value}" for key, value in self.stats.platform_config.items()]

    def _dot_leader(self, width: int, colors: TerminalColors) -> str:
        """Create a dot-leader string for visual tracing between values.

        Uses middle dot (·) in Unicode mode, period (.) in ASCII mode,
        with 1-char space gap on each side for readability.
        """
        if width <= 2:
            return " " * width
        dot_char = "·" if self.options.use_unicode else "."
        dots = dot_char * (width - 2)
        leader = f" {dots} "
        return colors.colorize(leader, fg_color="#666666")

    def _format_pct_visible(self, pct: float) -> str:
        """Format a percentage for visible-width calculations."""
        text = f"{pct:+.1f}%"
        no_color = not self.options.use_color
        if pct < -2:
            if no_color:
                arrow = "\u2193" if self.options.use_unicode else "v"
                return f"{text}{arrow}"
        elif pct > 2 and no_color:
            arrow = "\u2191" if self.options.use_unicode else "^"
            return f"{text}{arrow}"
        return text

    def _format_pct_colored(self, pct: float, colors: TerminalColors) -> str:
        """Format a percentage with color (green for improvement, red for regression)."""
        text = self._format_pct_visible(pct)
        no_color = not self.options.use_color
        lib = self.stats.lower_is_better
        if pct < -2:
            if no_color:
                return text
            color = "#66a61e" if lib else "#d95f02"
            return colors.colorize(text, fg_color=color)
        elif pct > 2:
            if no_color:
                return text
            color = "#d95f02" if lib else "#66a61e"
            return colors.colorize(text, fg_color=color)
        return text

    def _format_metric(self, value: float) -> str:
        """Format a metric value using the configured formatter or built-in dispatch.

        Dispatch order: value_formatter callback → _format_time() (when
        metric_label is "ms") → _format_value() + metric_label.
        """
        if self.stats.value_formatter is not None:
            return self.stats.value_formatter(value)
        if self.stats.metric_label.strip().lower() == "ms":
            return self._format_time(value)
        return f"{self._format_value(value)}{self.stats.metric_label}"

    def _format_time(self, ms: float) -> str:
        """Format milliseconds into a human-readable time string."""
        if not math.isfinite(ms):
            return "N/A"
        if ms >= 60_000:
            return f"{ms / 60_000:.1f}min"
        if ms >= 1_000:
            return f"{ms / 1_000:.1f}s"
        return f"{ms:.1f}ms"
