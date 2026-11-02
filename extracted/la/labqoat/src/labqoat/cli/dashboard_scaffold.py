"""Cross-run comparison dashboard definitions built from one run name and its metric names."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from labqoat.json_document import JsonValue


@dataclass(frozen=True, kw_only=True)
class DashboardScaffold:
    """Describe an optional goal trade-off, headline numbers, a ranked run table and one curve per metric.

    Computed columns are formulas over the chosen metrics and arguments; the service evaluates them per run.
    """

    run_name: str
    metrics: Sequence[str]
    axis: str | None = None
    label: str | None = None
    arguments: Sequence[str] = ()
    rank: str | None = None
    frontier: str | None = None
    derived: Sequence[tuple[str, str]] = ()
    exclude_tags: Sequence[str] = ()

    def definition(self, title: str | None = None) -> dict[str, JsonValue]:
        """Return the dashboard document: the goal trade-off first, then numbers, the table and the curves."""
        blocks = [*self._tradeoff(), *self._numbers(), (self._table(), 12, 5)]
        blocks += [(self._curve(index, metric), 6, 4) for index, metric in enumerate(self.metrics)]
        panels: list[JsonValue] = [panel for panel, _width, _height in blocks]
        name = title or f"{self.run_name} comparison"
        return {"name": name, "parameters": [], "panels": panels, "layout": DashboardScaffold._place(blocks)}

    @staticmethod
    def _place(blocks: Sequence[tuple[dict[str, JsonValue], int, int]]) -> list[JsonValue]:
        """Pack blocks left to right on the twelve-column grid, starting a row when one is full."""
        layout: list[JsonValue] = []
        x, y, row = 0, 0, 0
        for panel, width, height in blocks:
            if x + width > 12:
                x, y, row = 0, y + row, 0
            layout.append({"panel_id": panel["id"], "x": x, "y": y, "width": width, "height": height})
            x, row = x + width, max(row, height)
        return layout

    def _source(self, query: dict[str, JsonValue]) -> dict[str, JsonValue]:
        """Select every run of the function, with the panel's own columns and the computed ones."""
        selected: dict[str, JsonValue] = {**self._rule(), **query}
        if self.derived:
            selected["metrics"] = list(self.metrics)
            selected["derived"] = [{"name": name, "expression": expression} for name, expression in self.derived]
        return {"kind": "run_summaries", "query": selected}

    def _rule(self) -> dict[str, JsonValue]:
        """Match every run of the function, leaving out runs that carry an excluded tag."""
        rule: dict[str, JsonValue] = {"name": self.run_name}
        if self.exclude_tags:
            rule["exclude_tags"] = list(self.exclude_tags)
        return rule

    def _numbers(self) -> list[tuple[dict[str, JsonValue], int, int]]:
        """Count the matching runs and, when a ranking is chosen, show its best value."""
        source = self._source({"metrics": list(self.metrics)})
        runs: dict[str, JsonValue] = {"type": "stat", "value": "runs"}
        count: dict[str, JsonValue] = {"id": "runs", "title": "Runs", "source": source, "chart": runs}
        numbers = [(count, 3, 2)]
        if self.rank is not None:
            metric, _separator, direction = self.rank.rpartition(":")
            best: dict[str, JsonValue] = {
                "type": "stat",
                "column": metric,
                "reduce": "max" if direction == "desc" else "min",
            }
            numbers.append(({"id": "best", "title": f"Best {metric}", "source": source, "chart": best}, 3, 2))
        return numbers

    def _table(self) -> dict[str, JsonValue]:
        """Show each run's arguments and latest metric values before its bookkeeping columns."""
        query: dict[str, JsonValue] = {"metrics": list(self.metrics)}
        if self.arguments:
            query["arguments"] = list(self.arguments)
        if self.rank is not None:
            query["rank"] = self.rank
        computed = [name for name, _expression in self.derived]
        columns: list[JsonValue] = [
            *self.arguments,
            *self.metrics,
            *computed,
            "status",
            "created_by",
            "inserted_at",
            "id",
        ]
        chart: dict[str, JsonValue] = {"type": "table", "columns": columns}
        return {"id": "summary", "title": "Runs", "source": self._source(query), "chart": chart}

    def _tradeoff(self) -> list[tuple[dict[str, JsonValue], int, int]]:
        """Plot two metrics against each other and mark the runs nothing else beats on both."""
        if self.frontier is None:
            return []
        (x, x_goal), (y, y_goal) = (part.rpartition(":")[::2] for part in self.frontier.split(","))
        query: dict[str, JsonValue] = {"metrics": [x, y], "state": "completed"}
        chart: dict[str, JsonValue] = {"type": "scatter", "x": x, "y": y, "frontier": {"x": x_goal, "y": y_goal}}
        if self.label is not None:
            query["arguments"] = [self.label]
            chart["label"] = self.label
        title = f"{y} against {x}"
        return [({"id": "tradeoff", "title": title, "source": self._source(query), "chart": chart}, 12, 5)]

    def _curve(self, index: int, metric: str) -> dict[str, JsonValue]:
        """Plot one metric for the most recent matching runs on the chosen coordinate."""
        query: dict[str, JsonValue] = {**self._rule(), "metric": metric}
        if self.axis is not None:
            query["axis"] = self.axis
        if self.label is not None:
            query["label"] = self.label
        source: dict[str, JsonValue] = {"kind": "run_curves", "query": query}
        chart: dict[str, JsonValue] = {"type": "line", "x": "x", "y": "value", "series": "series"}
        return {"id": f"metric-{index + 1}", "title": metric, "source": source, "chart": chart}
