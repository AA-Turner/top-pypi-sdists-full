"""Read one project with its ranking objectives and the apps that ran in it."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.exit_codes import ExitCodes
from labqoat.cli.output.cli_failure import CliFailure
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class ProjectShowCommand(EndpointCommand):
    """Default to the selected project and explain a project that nothing was written to yet."""

    def __init__(self) -> None:
        """Declare the optional project name."""
        super().__init__(
            "show",
            "/api/v1/projects/{name}",
            [click.Argument(["name"], required=False)],
            "Show a project's objectives and apps. NAME defaults to the selected project.",
        )

    def _write_response(self, client: ManagementClient, query: dict[str, object]) -> None:
        """Read the named or selected project; JSON keeps one document, people get facts and two tables."""
        context = ContextAccessor.current()
        named = query.get("name")
        selected = named if isinstance(named, str) and named else context.project_name()
        try:
            document = client.get(self._path, {"name": selected})
        except ApiError as error:
            if error.status != 404 or query.get("name") is not None:
                raise
            raise CliFailure(self.unused(selected), ExitCodes.DOMAIN_FAILURE, error.problem) from error
        writer = ResultWriter()
        if context.output_mode != "human":
            writer.write_dict(document)
            return
        tables = {"objectives": self.objectives(document.get("objectives")), "apps": document.get("apps")}
        writer.write_dict({name: value for name, value in document.items() if name not in tables})
        for name, rows in tables.items():
            if rows:
                writer.write_dict({name: rows})

    @staticmethod
    def unused(name: str) -> str:
        """Say why the selected project is missing and what creates it."""
        return (
            f"Project {name!r} has no work yet. It is created the first time a run, dataset, dashboard or memory "
            f"record is written under it, or now with `lab project create {name}`."
        )

    @staticmethod
    def objectives(value: JsonValue) -> list[JsonValue]:
        """Spell each objective's required setup as KEY=VALUE text so it fits a table cell."""
        rows: list[JsonValue] = []
        for raw in JsonDocument.expect_list(value or []):
            objective = JsonDocument.expect_dict(raw)
            require = JsonDocument.expect_dict(objective.get("require") or {})
            rows.append({**objective, "require": ", ".join(f"{key}={setting}" for key, setting in require.items())})
        return rows
