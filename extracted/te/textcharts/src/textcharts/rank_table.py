"""ASCII rank table chart for competitive ranking."""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from textcharts.base import ChartBase, ChartOptions

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@dataclass
class RankTableData:
    """Data for a rank table chart."""

    items: list[str]
    groups: list[str]
    values: dict[tuple[str, str], float]  # (group, item) -> numeric value


class RankTable(ChartBase):
    """Rank table showing per-item competitive rankings across groups.

    Each cell shows the ordinal rank (1st, 2nd, 3rd...) of each platform
    for each query, with aggregate win/loss tallies and geometric mean rank.

    Example output:
    ```
    Query Rankings (1st = fastest)
    ──────────────────────────────────────
    Query    DuckDB  Polars  SQLite  Pandas
    Q1        1st     2nd     3rd     4th
    Q2        2nd     1st     3rd     4th
    ──────────────────────────────────────
    1st wins    15      5       2       0
    GeoRank   1.2    1.8     2.8     3.9
    ```
    """

    def __init__(
        self,
        data: RankTableData,
        title: str | None = None,
        options: ChartOptions | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
    ):
        super().__init__(options, subtitle=subtitle, title=title, subject=subject)
        self.data = data
        self.title = self._compose_title("Rankings (1st = best)")

    def render(self) -> str:
        """Render the rank table as a string."""
        self._detect_capabilities()

        if not self.data.items or not self.data.groups:
            return "No data to display"

        colors = self.options.get_colors()
        width = self.options.get_effective_width()

        # Sort items naturally
        items = sorted(self.data.items, key=self._natural_sort_key)
        groups = self.data.groups

        # Compute rankings for each item
        rankings: dict[str, dict[str, int]] = {}  # item -> {group -> rank}
        for item in items:
            # Get values for this item (skip missing and non-finite values,
            # which cannot be ranked; they render as "-")
            item_values: list[tuple[str, float]] = []
            for group in groups:
                val = self.data.values.get((group, item))
                if val is not None and math.isfinite(val):
                    item_values.append((group, val))

            # Sort by value ascending (lower = better rank)
            item_values.sort(key=lambda x: x[1])

            # Assign ranks with tie handling
            item_ranks: dict[str, int] = {}
            i = 0
            while i < len(item_values):
                # Find all tied groups
                j = i
                while j < len(item_values) and item_values[j][1] == item_values[i][1]:
                    j += 1
                rank = i + 1
                for k in range(i, j):
                    item_ranks[item_values[k][0]] = rank
                i = j

            rankings[item] = item_ranks

        # Calculate column widths
        item_col_width = max(5, max(len(q) for q in items) + 1)
        group_col_width = max(6, max(len(p) for p in groups) + 1)

        # Check if table fits; if not, truncate groups
        total_width = item_col_width + len(groups) * group_col_width
        if total_width > width:
            group_col_width = max(5, (width - item_col_width) // len(groups))

        n_groups = len(groups)

        lines: list[str] = []

        # Title and subtitle
        lines.append(self._render_title(self.title, width))
        subtitle = self._render_subtitle(width)
        if subtitle:
            lines.append(subtitle)
        lines.append(self._render_horizontal_line(width))

        # Header row
        header = "Item".ljust(item_col_width)
        for group in groups:
            header += self._truncate_label(group, group_col_width - 1).center(group_col_width)
        lines.append(header)

        # Data rows
        for item in items:
            row = item.ljust(item_col_width)
            item_ranks = rankings.get(item, {})
            max_rank = max(item_ranks.values()) if item_ranks else n_groups
            for group in groups:
                rank = item_ranks.get(group)
                if rank is None:
                    cell = "-"
                else:
                    cell = self._ordinal(rank)

                # Pad BEFORE colorizing to avoid ANSI codes breaking alignment
                padded_cell = cell.center(group_col_width)
                # Color: 1st green, worst rank red
                if rank == 1:
                    padded_cell = colors.colorize(padded_cell, fg_color="#1b9e77")
                elif rank is not None and rank == max_rank and max_rank > 1:
                    padded_cell = colors.colorize(padded_cell, fg_color="#d95f02")

                row += padded_cell
            lines.append(row)

        lines.append(self._render_horizontal_line(width))

        # Footer: win tallies
        wins_row = "Wins".ljust(item_col_width)
        all_ranks: dict[str, list[int]] = {g: [] for g in groups}

        for item in items:
            for group in groups:
                rank = rankings.get(item, {}).get(group)
                if rank is not None:
                    all_ranks[group].append(rank)

        win_counts = {g: sum(1 for r in ranks if r == 1) for g, ranks in all_ranks.items()}
        for group in groups:
            count_str = str(win_counts.get(group, 0))
            wins_row += count_str.center(group_col_width)
        lines.append(wins_row)

        # Footer: geometric mean rank
        georank_row = "GeoRank".ljust(item_col_width)
        for group in groups:
            ranks = all_ranks.get(group, [])
            if ranks:
                geo_mean = math.exp(sum(math.log(r) for r in ranks) / len(ranks))
                georank_row += f"{geo_mean:.1f}".center(group_col_width)
            else:
                georank_row += "-".center(group_col_width)
        lines.append(georank_row)

        return "\n".join(lines)

    @staticmethod
    def _ordinal(n: int) -> str:
        """Convert integer to ordinal string (1st, 2nd, 3rd, 4th...)."""
        if 11 <= (n % 100) <= 13:
            return f"{n}th"
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    @staticmethod
    def _natural_sort_key(s: str):
        """Natural sort key for item IDs (Q1, Q2, Q10 not Q1, Q10, Q2)."""
        import re

        return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", s)]


def from_matrix(
    matrix: Sequence[Sequence[float]],
    items: Sequence[str],
    groups: Sequence[str],
    title: str | None = None,
    options: ChartOptions | None = None,
    subject: str | None = None,
) -> RankTable:
    """Create RankTable from the same matrix format as Heatmap.

    Args:
        matrix: 2D matrix of numeric values [item_idx][group_idx].
        items: Item labels (row labels).
        groups: Group labels (column labels).
        title: Optional chart title.
        options: Chart rendering options.

    Returns:
        Configured RankTable instance.
    """
    if len(matrix) != len(items):
        raise ValueError("items length must match the number of matrix rows")

    expected_cols = len(groups)
    for row_idx, row in enumerate(matrix, start=1):
        if len(row) != expected_cols:
            raise ValueError(
                f"matrix row {row_idx} has {len(row)} columns but expected {expected_cols} to match groups"
            )

    values: dict[tuple[str, str], float] = {}
    for qi, item in enumerate(items):
        for pi, group in enumerate(groups):
            values[(group, item)] = matrix[qi][pi]

    data = RankTableData(
        items=list(items),
        groups=list(groups),
        values=values,
    )
    return RankTable(data=data, title=title, options=options, subject=subject)
