"""Print a cross-run comparison dashboard definition ready for publication."""

from __future__ import annotations

import json
import re

import click

from labqoat.cli.dashboard_scaffold import DashboardScaffold
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class DashboardInitCommand(StrictCommand):
    """Write a dashboard definition comparing every run of one function across chosen metrics."""

    def __init__(self) -> None:
        """Declare the run name, its metrics and the optional comparison choices."""
        super().__init__(
            name="init",
            params=[
                ParameterFactory.argument("run_name"),
                click.Option(["--metric", "metrics"], multiple=True, required=True, help="Metric to compare; repeat."),
                click.Option(
                    ["--argument", "arguments"], multiple=True, help="Run argument shown as a column; repeat."
                ),
                click.Option(
                    ["--derive", "derived"],
                    multiple=True,
                    help="Computed column as NAME=EXPRESSION over [metric] references, such as "
                    "'val/score=([val/accuracy] + [val/f1]) / 2'; repeat, later ones may use earlier names.",
                ),
                click.Option(
                    ["--exclude-tag", "exclude_tags"],
                    multiple=True,
                    help="Leave out runs carrying this tag, such as tainted; repeat.",
                ),
                ParameterFactory.text_option("axis"),
                ParameterFactory.text_option("label"),
                ParameterFactory.text_option("rank"),
                ParameterFactory.text_option("frontier"),
                ParameterFactory.text_option("title"),
            ],
            help="Print a cross-run dashboard definition for RUN_NAME (app/function); save it and publish.",
        )

    @staticmethod
    def default_rank(metrics: tuple[str, ...]) -> str | None:
        """Rank by validation loss, the main validation score, whenever it is among the chosen metrics."""
        return "val/loss:asc" if "val/loss" in metrics else None

    @staticmethod
    def derivations(ctx: click.Context) -> tuple[tuple[str, str], ...]:
        """Split each NAME=EXPRESSION at its first equals sign; the service checks the formula itself."""
        pairs = tuple(tuple(part.strip() for part in text.partition("=")[::2]) for text in ctx.params["derived"])
        if len(pairs) > 8 or any(not name or not expression for name, expression in pairs):
            raise click.UsageError("Write --derive as NAME=EXPRESSION, at most eight times.", ctx)
        return tuple((name, expression) for name, expression in pairs)

    def invoke(self, ctx: click.Context) -> object:
        """Build the definition offline and print it as indented JSON."""
        metrics = tuple(ctx.params["metrics"])
        if len(metrics) > 12:
            raise click.UsageError("At most 12 metrics fit one dashboard.", ctx)
        frontier = ctx.params["frontier"]
        if frontier is not None and re.fullmatch(r"[^,:]+:(min|max),[^,:]+:(min|max)", frontier) is None:
            raise click.UsageError("Write --frontier as X_METRIC:min|max,Y_METRIC:min|max.", ctx)
        scaffold = DashboardScaffold(
            run_name=str(ctx.params["run_name"]),
            metrics=metrics,
            axis=ctx.params["axis"],
            label=ctx.params["label"],
            arguments=tuple(ctx.params["arguments"]),
            rank=ctx.params["rank"] or DashboardInitCommand.default_rank(metrics),
            frontier=frontier,
            derived=DashboardInitCommand.derivations(ctx),
            exclude_tags=tuple(ctx.params["exclude_tags"]),
        )
        click.echo(json.dumps(scaffold.definition(ctx.params["title"]), indent=2))
        return None
