"""Print the selected project and what selected it, without any network request."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class ProjectCurrentCommand(StrictCommand):
    """Answer which project the next command acts on: the flag, the variable, a pinned file, or none."""

    def __init__(self) -> None:
        """Declare a command without parameters."""
        super().__init__(
            "current",
            params=[],
            help="Print the selected project and its source. The source is --project, LABQOAT_PROJECT, the nearest "
            "pyproject.toml that pins one; with none, project is null. Uses no network.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Render the resolved name, the kind of source and the flag, variable or file behind it."""
        selection = ContextAccessor.current().selection()
        ResultWriter().write_dict(
            {"project": selection.name, "source": selection.source, "selected_by": selection.origin()}
        )
        return None
