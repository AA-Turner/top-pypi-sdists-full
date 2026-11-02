"""Confirmed deletion command for one management endpoint."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.mutation_key import MutationKey


class DeleteEndpointCommand(StrictCommand):
    """Confirm and delete one explicitly selected resource."""

    def __init__(
        self,
        name: str,
        path: str,
        reference_name: str,
        params: Sequence[click.Parameter],
        help_text: str,
        fixed_query: Mapping[str, object] | None = None,
    ) -> None:
        """Store the deletion endpoint and selector name."""
        super().__init__(name, params=[*params, MutationKey.option()], help=help_text)
        self._path = path
        self._reference_name = reference_name
        self._fixed_query = dict(fixed_query or {})

    def invoke(self, ctx: click.Context) -> object:
        """Confirm, delete, and render one resource."""
        reference = str(ctx.params[self._reference_name])
        if not ctx.params["yes"]:
            click.confirm(f"Delete {reference}?", abort=True)
        client = ContextAccessor.current().management()
        try:
            query: dict[str, object] = {"ref": reference, "operation_key": MutationKey.resolve(ctx.params["key"])}
            query.update(self._fixed_query)
            ResultWriter().write_dict(client.delete(self._path, query))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
