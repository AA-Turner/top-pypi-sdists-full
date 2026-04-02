#!/usr/bin/env python3
"""
Fray Stats — Payload database statistics and analysis.

Scans the payloads directory, counts payloads per category (JSON + TXT),
and prints a rich summary table with bar chart visualization.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from fray import PAYLOADS_DIR


@dataclass
class CategoryStats:
    """Statistics for a single payload category."""
    name: str
    json_payloads: int = 0
    txt_payloads: int = 0
    json_files: int = 0
    txt_files: int = 0
    subcategories: List[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.json_payloads + self.txt_payloads

    @property
    def files(self) -> int:
        return self.json_files + self.txt_files


@dataclass
class PayloadStats:
    """Aggregate statistics for the entire payload database."""
    categories: List[CategoryStats] = field(default_factory=list)
    payloads_dir: str = ""

    @property
    def total_payloads(self) -> int:
        return sum(c.total for c in self.categories)

    @property
    def total_files(self) -> int:
        return sum(c.files for c in self.categories)

    @property
    def total_categories(self) -> int:
        return len(self.categories)

    def to_dict(self) -> dict:
        return {
            "payloads_dir": self.payloads_dir,
            "total_payloads": self.total_payloads,
            "total_files": self.total_files,
            "total_categories": self.total_categories,
            "categories": [
                {
                    "name": c.name,
                    "total": c.total,
                    "json_payloads": c.json_payloads,
                    "txt_payloads": c.txt_payloads,
                    "files": c.files,
                    "subcategories": c.subcategories,
                }
                for c in self.categories
            ],
        }


def _count_json_payloads(filepath: Path) -> int:
    """Count payloads in a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict) and "payloads" in data:
            return len(data["payloads"])
        return 0
    except (json.JSONDecodeError, OSError):
        return 0


def _count_txt_payloads(filepath: Path) -> int:
    """Count payloads in a TXT file (one per line, skip blanks/comments)."""
    try:
        count = 0
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    count += 1
        return count
    except OSError:
        return 0


def collect_stats(payloads_dir: Optional[Path] = None) -> PayloadStats:
    """Scan payloads directory and collect per-category statistics."""
    base = payloads_dir or PAYLOADS_DIR
    stats = PayloadStats(payloads_dir=str(base))

    if not base.is_dir():
        return stats

    for entry in sorted(base.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        cat = CategoryStats(name=entry.name)

        for fp in sorted(entry.rglob("*")):
            if not fp.is_file():
                continue

            subcat = fp.stem

            if fp.suffix == ".json":
                count = _count_json_payloads(fp)
                cat.json_payloads += count
                cat.json_files += 1
                if subcat not in cat.subcategories:
                    cat.subcategories.append(subcat)
            elif fp.suffix == ".txt":
                count = _count_txt_payloads(fp)
                cat.txt_payloads += count
                cat.txt_files += 1
                if subcat not in cat.subcategories:
                    cat.subcategories.append(subcat)

        if cat.total > 0:
            stats.categories.append(cat)

    # Sort by total descending
    stats.categories.sort(key=lambda c: c.total, reverse=True)
    return stats


def print_stats(stats: PayloadStats) -> None:
    """Print payload statistics with rich formatting."""
    from fray.output import console
    from fray import __version__
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text

    if not stats.categories:
        console.print("[yellow]No payloads found.[/yellow]")
        return

    max_total = max(c.total for c in stats.categories)

    # ── Category table ──
    table = Table(show_lines=False, pad_edge=False, box=None)
    table.add_column("Category", min_width=22, style="bold")
    table.add_column("Payloads", width=8, justify="right")
    table.add_column("", min_width=30)  # bar
    table.add_column("Files", width=6, justify="right", style="dim")

    # Color palette by rank
    colors = [
        "bright_red", "red", "yellow", "bright_yellow", "green",
        "bright_green", "cyan", "bright_cyan", "blue", "bright_blue",
        "magenta", "bright_magenta", "white", "white", "white",
        "white", "white", "white", "white", "white", "white", "white",
    ]

    for i, cat in enumerate(stats.categories):
        bar_width = int(cat.total / max_total * 25) if max_total > 0 else 0
        color = colors[min(i, len(colors) - 1)]
        bar = Text("█" * bar_width + "░" * (25 - bar_width), style=color)
        count_txt = Text(f"{cat.total:,}", style=f"bold {color}")
        table.add_row(cat.name, count_txt, bar, str(cat.files))

    # ── Totals row ──
    table.add_row("", "", "", "")
    total_bar = Text("━" * 25, style="bold")
    table.add_row(
        Text("TOTAL", style="bold white"),
        Text(f"{stats.total_payloads:,}", style="bold white"),
        total_bar,
        Text(str(stats.total_files), style="bold white"),
    )

    console.print()
    console.print(Panel(
        table,
        title=f"[bold]Fray v{__version__} — Payload Database[/bold]",
        subtitle=f"[dim]{stats.total_categories} categories · {stats.total_files} files · {stats.total_payloads:,} payloads[/dim]",
        border_style="bright_cyan",
        expand=False,
    ))
    console.print()
