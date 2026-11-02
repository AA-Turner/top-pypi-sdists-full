"""Strict Click leaf backed by one explicit management endpoint."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class EndpointCommand(StrictCommand):
    """Forward validated arguments and options to a read-only endpoint."""

    def __init__(
        self,
        name: str,
        path: str,
        params: Sequence[click.Parameter],
        help_text: str,
        reference_name: str | None = None,
        fixed_query: Mapping[str, object] | None = None,
        query_renames: Mapping[str, str] | None = None,
        reader: bool = False,
    ) -> None:
        """Store endpoint metadata; reader commands send an optional agent label for read tracking."""
        agent = click.Option(["--agent"], envvar="LABQOAT_AGENT", help="Reader label, such as root or scout-2.")
        super().__init__(name, params=[*params, *([agent] if reader else [])], help=help_text)
        self._path = path
        self._reference_name = reference_name
        self._fixed_query = dict(fixed_query or {})
        self._query_renames = dict(query_renames or {})

    def invoke(self, ctx: click.Context) -> object:
        """Read and render one endpoint document."""
        query = dict(ctx.params)
        self.validate_time_windows(query, ctx)
        if self._reference_name is not None:
            query["ref"] = query.pop(self._reference_name)
        query = {self._query_renames.get(name, name): value for name, value in query.items()}
        query.update(self._fixed_query)
        agent = query.pop("agent", None)
        client = ContextAccessor.current().management(agent=None if agent is None else str(agent))
        try:
            self._write_response(client, query)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    def _write_response(self, client: ManagementClient, query: dict[str, object]) -> None:
        """Render the selected endpoint document."""
        ResultWriter().write_dict(client.get(self._path, query))

    @staticmethod
    def validate_time_windows(query: dict[str, object], ctx: click.Context) -> None:
        """Reject reversed creation and log timestamp windows."""
        for lower, upper in (("created_after", "created_before"), ("timestamp_after", "timestamp_before")):
            start = query.get(lower)
            end = query.get(upper)
            if isinstance(start, str) and isinstance(end, str):
                parsed_start = datetime.fromisoformat(start.replace("Z", "+00:00"))
                parsed_end = datetime.fromisoformat(end.replace("Z", "+00:00"))
                if parsed_start > parsed_end:
                    names = f"--{lower.replace('_', '-')} and --{upper.replace('_', '-')}"
                    raise click.UsageError(f"{names} form an invalid time window.", ctx)
