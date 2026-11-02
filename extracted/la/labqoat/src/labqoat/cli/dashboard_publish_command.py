"""Publish one dashboard definition from a JSON document."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument
from labqoat.cli.mutation_key import MutationKey


class DashboardPublishCommand(StrictCommand):
    """Publish a dashboard version from a JSON definition file."""

    def __init__(self, params: Sequence[click.Parameter]) -> None:
        """Construct the strict dashboard publication command."""
        super().__init__(
            name="publish", params=[*params, MutationKey.option()], help="Publish a dashboard version from a JSON file."
        )

    def invoke(self, ctx: click.Context) -> object:
        """Load the definition file and publish one dashboard version."""
        try:
            payload = DashboardPublishCommand.load(str(ctx.params["definition"]))
        except (TypeError, ValueError) as error:
            ErrorReporter.report_usage(str(error))
        client = ContextAccessor.current().management()
        try:
            query: dict[str, object] = {"operation_key": MutationKey.resolve(ctx.params["key"])}
            ResultWriter().write_dict(client.post("/api/v1/dashboards", query, payload))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def load(definition: str) -> JsonDocument:
        """Read and validate a dashboard definition document."""
        raw = json.loads(Path(definition).read_text(encoding="utf-8"))
        return JsonDocument.expect_dict(raw)
