"""Move existing runs, apps, dashboards and datasets into another project."""

from __future__ import annotations

from typing import ClassVar

import click

from labqoat.cli.mutation_spec import MutationSpec
from labqoat.cli.payload_command import PayloadCommand
from labqoat.json_document import JsonDocument


class ProjectMoveCommand(PayloadCommand):
    """Send every repeated selector as one list and require at least one of them."""

    selectors: ClassVar[dict[str, str]] = {
        "run": "runs",
        "app": "apps",
        "dashboard": "dashboards",
        "dataset": "datasets",
    }

    def __init__(self) -> None:
        """Declare the destination project and the repeatable selectors."""
        params: list[click.Parameter] = [
            click.Option(["--to"], required=True, help="Destination project; created when missing."),
            click.Option(["--run"], multiple=True, help="Run or group ID; moves with every run it started."),
            click.Option(["--app"], multiple=True, help="App name; moves its runs out of the selected project."),
            click.Option(["--dashboard"], multiple=True, help="Dashboard ID."),
            click.Option(["--dataset"], multiple=True, help="Dataset repository name."),
        ]
        spec = MutationSpec("/api/v1/projects/{name}/moves", query_names=("to",), query_renames={"to": "name"})
        super().__init__(
            "move", spec, params, "Move existing work into a project. Selectors are repeatable and combine."
        )

    def payload(self, values: dict[str, object]) -> JsonDocument:
        """Keep only the selectors that were given, under their plural request names."""
        document = JsonDocument()
        for option, field in self.selectors.items():
            chosen = values.get(option)
            if isinstance(chosen, tuple) and chosen:
                document[field] = [str(item) for item in chosen]
        if not document:
            raise ValueError("Select what to move with at least one --run, --app, --dashboard or --dataset.")
        return document
