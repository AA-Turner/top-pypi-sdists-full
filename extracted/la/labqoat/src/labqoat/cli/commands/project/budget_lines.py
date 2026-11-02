"""A project's budget as short lines: what is used of each limit, then the advice it earns."""

from __future__ import annotations

import click

from labqoat._generated.project_budget import ProjectBudget
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.json_document import JsonDocument


class BudgetLines:
    """Spell the same budget for a person reading a terminal and for an agent reading a log."""

    @staticmethod
    def hints(budget: ProjectBudget) -> list[str]:
        """One line per hint, led by its direction: more, steady, less or stop."""
        lines = []
        for raw in budget.hints:
            hint = JsonDocument.expect_dict(raw)
            lines.append(f"budget {hint['direction']}: {hint['message']}")
        return lines

    @staticmethod
    def lines(budget: ProjectBudget) -> list[str]:
        """Name the project, each stated limit with what is used of it, and every hint."""
        limits = budget.limits
        facts = [
            ("money", budget.spent, limits.spend, "USD {:.2f} spent of USD {:.2f}"),
            ("rate", budget.spent_last_hour, limits.spend_per_hour, "USD {:.2f} in the last hour of USD {:.2f}/hour"),
            ("time", budget.elapsed_hours, limits.hours, "{:.1f} h gone of {:.1f} h"),
        ]
        stated = [
            f"{label}: {template.format(used, limit)}"
            for label, used, limit, template in facts
            if used is not None and limit is not None
        ]
        if budget.spend_rate is not None:
            stated.append(f"spending: USD {budget.spend_rate:.2f}/hour now")
        if not stated:
            stated = ["budget: none. State one with `lab project budget set`."]
        return [f"project: {budget.project}", *stated, *BudgetLines.hints(budget)]

    @staticmethod
    def write(budget: ProjectBudget) -> None:
        """Write one JSON document in the JSON modes and plain lines otherwise."""
        if ContextAccessor.current().output_mode != "human":
            ResultWriter().write_dict(dict(budget.to_dict()))
            return
        for line in BudgetLines.lines(budget):
            click.echo(line)
