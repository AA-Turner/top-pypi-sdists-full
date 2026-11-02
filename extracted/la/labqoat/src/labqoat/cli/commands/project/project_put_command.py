"""Create a project, and for ``init`` also pin it for the current working directory."""

from __future__ import annotations

from pathlib import Path

import click

from labqoat._generated.project_attributes import ProjectAttributes
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.init.project_scaffold import ProjectScaffold
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.version_info import VersionInfo
from labqoat.json_document import JsonValue
from labqoat.projects.project_names import ProjectNames
from labqoat.projects.project_pin import ProjectPin


class ProjectPutCommand(StrictCommand):
    """Create the named project idempotently; ``init`` then makes it the directory's selected project."""

    def __init__(self, name: str, pin: bool) -> None:
        """Declare the project name and its optional description."""
        params: list[click.Parameter] = [click.Argument(["name"]), click.Option(["--description"], type=str)]
        summary = (
            "Create a project and pin it for this directory. Writes [tool.labqoat] project to ./pyproject.toml, "
            "so every command run from here acts on it, and adds this SDK to the dev group for local tests."
            if pin
            else "Create a project or update its description. Repeating the command is safe."
        )
        super().__init__(name, params=params, help=summary)
        self._pin = pin

    def invoke(self, ctx: click.Context) -> object:
        """Validate the name locally, create the project, then pin it when initializing a directory."""
        try:
            name = ProjectNames.project(ctx.params["name"], "the NAME argument")
        except ValueError as error:
            ErrorReporter.report_usage(str(error))
        attributes = ProjectAttributes(description=ctx.params["description"])
        with ContextAccessor.current().client(project=name) as client:
            document: dict[str, JsonValue] = dict(client.projects.put(name, attributes).to_dict())
        if self._pin:
            document["pinned"] = str(ProjectPin.write(Path.cwd(), name))
            scaffold = ProjectScaffold(Path.cwd(), name, ProcessRunner(timeout_seconds=120.0))
            document["sdk"] = scaffold.sdk(VersionInfo.installed_version())
        ResultWriter().write_dict(document)
        return None
