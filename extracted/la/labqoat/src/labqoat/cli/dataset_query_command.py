"""Validated governed dataset analytics queries."""

from __future__ import annotations

import json

import click

from labqoat.cli.analytics_failure import AnalyticsFailure
from labqoat.cli.analytics_waiter import AnalyticsWaiter
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument
from labqoat.cli.mutation_key import MutationKey
from labqoat.cli.observation_deadline import ObservationDeadline


class DatasetQueryCommand(StrictCommand):
    """Decode query JSON and submit it against an explicit dataset revision."""

    def __init__(self, name: str, params: list[click.Parameter], help_text: str) -> None:
        """Construct a strict analytics query command."""
        super().__init__(name, params=[*params, MutationKey.option(), ObservationDeadline.option()], help=help_text)

    def invoke(self, ctx: click.Context) -> object:
        """Validate query JSON before creating an authenticated client."""
        try:
            payload = JsonDocument.expect_dict(json.loads(str(ctx.params["query"])))
        except (TypeError, ValueError) as error:
            ErrorReporter.report_usage(f"query must be a JSON object: {error}")
        payload["dataset_revision_ref"] = str(ctx.params["dataset"])
        client = ContextAccessor.current().management()
        try:
            query = {"operation_key": MutationKey.resolve(ctx.params["key"])}
            submitted = client.post("/api/v1/analytics-queries", query, payload)
            with ObservationDeadline.current(str(submitted["id"])).watching():
                final = AnalyticsWaiter.wait(client, submitted)
            AnalyticsFailure.raise_for(final)
            ResultWriter().write_dict(final)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
