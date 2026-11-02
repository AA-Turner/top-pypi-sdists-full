"""Strict read-only leaf rendering one compute management document."""

from __future__ import annotations

from collections.abc import Sequence

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class ComputeReadCommand(StrictCommand):
    """Call one named ComputeClient read, passing positional identifiers in declaration order."""

    def __init__(self, name: str, operation: str, help_text: str, arguments: Sequence[str] = ()) -> None:
        """Declare the operation and its required positional identifiers."""
        params: list[click.Parameter] = [click.Argument([argument], type=str, required=True) for argument in arguments]
        super().__init__(name, params=params, help=help_text)
        self._operation = operation
        self._arguments = tuple(arguments)

    def invoke(self, ctx: click.Context) -> object:
        """Read and render the selected document, always closing the client."""
        client = ContextAccessor.current().compute()
        try:
            values = [str(ctx.params[argument]) for argument in self._arguments]
            ResultWriter().write_dict(getattr(client, self._operation)(*values))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
