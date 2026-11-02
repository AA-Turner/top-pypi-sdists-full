"""Strict offline commands for one local dataset workspace."""

from __future__ import annotations

from collections.abc import Sequence

import click

from labqoat.cli.dataset_workspace import DatasetWorkspace
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument


class DatasetLocalCommand(StrictCommand):
    """Perform one declared project-local dataset operation."""

    def __init__(self, name: str, params: Sequence[click.Parameter], help_text: str) -> None:
        """Store the operation name in a strict Click command."""
        super().__init__(name, params=list(params), help=help_text)

    def invoke(self, ctx: click.Context) -> object:
        """Discover the project, execute locally, and render JSON."""
        try:
            workspace = DatasetWorkspace.discover()
            ResultWriter().write_dict(self._execute(workspace, ctx.params))
        except (OSError, TypeError, ValueError) as error:
            ErrorReporter.report_generic(str(error))
        return None

    def _execute(self, workspace: DatasetWorkspace, values: dict[str, object]) -> JsonDocument:
        """Route one of the small offline workspace operations."""
        if self.name == "path":
            return JsonDocument({"path": str(workspace.mount_path(str(values["dataset"])))})
        if self.name == "mounts":
            return workspace.mounts()
        if self.name == "unmount":
            return workspace.unmount(str(values["dataset"]))
        raise ValueError(f"unsupported local dataset operation: {self.name}")
