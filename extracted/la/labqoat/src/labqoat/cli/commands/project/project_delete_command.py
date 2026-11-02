"""Confirmed deletion of one empty project."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class ProjectDeleteCommand(StrictCommand):
    """Delete a project by name; the service refuses one that still owns runs, datasets or dashboards."""

    def __init__(self) -> None:
        """Declare the project name and the noninteractive confirmation flag."""
        super().__init__(
            "delete",
            params=[click.Argument(["name"]), ParameterFactory.yes()],
            help="Delete an empty project. Move its runs, datasets and dashboards out first with `project move`.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Confirm, delete and report the removed name."""
        name = str(ctx.params["name"])
        if not ctx.params["yes"]:
            click.confirm(f"Delete project {name}?", abort=True)
        with ContextAccessor.current().client(project=name) as client:
            client.projects.delete(name)
        ResultWriter().write_dict({"deleted": name})
        return None
