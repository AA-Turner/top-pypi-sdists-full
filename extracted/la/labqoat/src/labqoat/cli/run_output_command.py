"""Validated authored result retrieval for an exact successful Run."""

from __future__ import annotations

from collections.abc import Sequence

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class RunOutputCommand(StrictCommand):
    """Read the authoritative authored result without exposing transport metadata as result fields."""

    def __init__(
        self,
        name: str,
        params: Sequence[click.Parameter],
        expected_kind: str | None = None,
    ) -> None:
        """Store the public command name and workload constraint."""
        super().__init__(name, params=list(params), help="Read the validated authored result of a completed Run.")
        self._expected_kind = expected_kind

    def invoke(self, ctx: click.Context) -> object:
        """Require backend result validation and print the exact workload result document."""
        client = ContextAccessor.current().management()
        try:
            result = client.runs.result(str(ctx.params["run_ref"]), expected_kind=self._expected_kind)
            ResultWriter().write_dict(result)
        except (KeyError, TypeError, ValueError) as error:
            ErrorReporter.report_generic(str(error))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
