"""Archive one project, or return an archived one to the listing."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class ProjectArchiveCommand(StrictCommand):
    """Hide a project and cancel what runs in it, keeping what it owns; ``unarchive`` lists it again."""

    def __init__(self, name: str, archived: bool) -> None:
        """Declare the project name and whether the command archives or restores it."""
        summary = (
            "Archive a project: hide it from `project list` and navigation and cancel its active runs and groups. "
            "Its runs, datasets, dashboards and memory stay readable by name; `project unarchive` lists it again."
            if archived
            else "Return an archived project to `project list` and navigation. `project list --archived` names them."
        )
        super().__init__(name, params=[click.Argument(["name"])], help=summary)
        self._archived = archived

    def invoke(self, ctx: click.Context) -> object:
        """Change the named project's archival state and report the project as the service now holds it."""
        name = str(ctx.params["name"])
        with ContextAccessor.current().client(project=name) as client:
            change = client.projects.archive if self._archived else client.projects.unarchive
            ResultWriter().write_dict(change(name).to_dict())
        return None
