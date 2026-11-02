"""Bounded per-descendant status and metric rows for a live terminal overview."""

from collections import Counter, OrderedDict
import re
from typing import TYPE_CHECKING

from labqoat.cli.console.console_entry import ConsoleEntry

if TYPE_CHECKING:
    from rich.table import Table


class ChildOverview:
    """Keep the newest 128 logical paths without conflating sibling attempts or root outcome."""

    def __init__(self) -> None:
        """Allocate rows only as child evidence arrives."""
        self.rows: OrderedDict[str, tuple[str, str]] = OrderedDict()

    def accept(self, entry: ConsoleEntry) -> bool:
        """Update run states and sampled measurements; bookkeeping events and raw output stay out."""
        path = entry.path()
        if not path or "." in entry.kind or not (entry.kind or entry.source == "metric"):
            return False
        status, metrics = self.rows.get(path, ("pending", ""))
        if entry.source == "metric":
            metrics = entry.content
        else:
            status = entry.kind.replace("submission.", "").replace(".", " ").replace("_", " ")
        self.rows[path] = (status, metrics)
        self.rows.move_to_end(path)
        if len(self.rows) > 128:
            self.rows.popitem(last=False)
        return True

    def table(self) -> "Table":
        """Use fixed semantic columns and let Rich handle terminal width and truncation."""
        from rich.table import Table

        table = Table(box=None, padding=(0, 1), expand=True)
        table.add_column("Run", ratio=2, overflow="ellipsis")
        table.add_column("State", ratio=1, overflow="ellipsis")
        table.add_column("Latest metrics", ratio=4, overflow="ellipsis")
        for path, status, metrics in self.display_rows():
            table.add_row(path, status, metrics)
        return table

    def display_rows(self) -> list[tuple[str, str, str]]:
        """Collapse large numeric map groups without guessing a total for unseen children."""
        groups: dict[str, list[tuple[str, str, str]]] = {}
        for path, (status, metrics) in self.rows.items():
            key = re.sub(r"/[0-9]+$", "/*", path)
            groups.setdefault(key, []).append((path, status, metrics))
        output = []
        for key, rows in groups.items():
            if len(rows) < 8:
                output.extend(rows)
            else:
                counts = Counter(row[1] for row in rows)
                states = ", ".join(f"{count} {state}" for state, count in sorted(counts.items()))
                output.append((key, f"{len(rows)} observed", states))
        return output
