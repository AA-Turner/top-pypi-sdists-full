"""Tags put on and taken off runs after the fact."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.strict_command import StrictCommand

if TYPE_CHECKING:
    from labqoat._generated.run import Run
    from labqoat.json_document import JsonValue
    from labqoat.runs_client import RunsClient


class RunTagCommand(StrictCommand):
    """Tag finished or active runs so listings and dashboards can select or leave them out."""

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Take any number of runs and the tags to put on or take off each of them."""
        return cls(
            "tag",
            help="Add or remove tags on runs, finished or not. `run list` and dashboard queries filter by tag, "
            "so a run found to be tainted is tagged once and left out everywhere by rule.",
            params=[
                click.Argument(["run_refs"], nargs=-1, required=True),
                click.Option(["--add", "added"], multiple=True, help="Tag to add; repeat."),
                click.Option(["--remove", "removed"], multiple=True, help="Tag to remove; repeat."),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Apply every change to every run and print each run's resulting tags."""
        from labqoat.cli.output.error_reporter import ErrorReporter
        from labqoat.cli.output.result_writer import ResultWriter

        added, removed = tuple(ctx.params["added"]), tuple(ctx.params["removed"])
        if not added and not removed:
            raise click.UsageError("Give at least one --add or --remove.", ctx)
        client = ContextAccessor.current().management()
        try:
            runs = [RunTagCommand.apply(client.runs, str(ref), added, removed) for ref in ctx.params["run_refs"]]
            ResultWriter().write_dict({"items": [RunTagCommand.row(run) for run in runs]})
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def apply(runs: RunsClient, ref: str, added: Sequence[str], removed: Sequence[str]) -> Run:
        """Add then remove the chosen tags on one run and return it as the service last described it."""
        changes = [(runs.add_tag, tag) for tag in added] + [(runs.remove_tag, tag) for tag in removed]
        results = [change(ref, tag) for change, tag in changes]
        return results[-1]

    @staticmethod
    def row(run: Run) -> dict[str, JsonValue]:
        """Keep the fields that identify a run and show what it now carries."""
        return {"id": run.id, "name": run.name, "status": run.status, "tags": list(run.tags or [])}
