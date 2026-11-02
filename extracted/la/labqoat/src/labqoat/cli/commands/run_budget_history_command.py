"""Explicit version-protected establishment of historical scientific usage."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.strict_command import StrictCommand


class RunBudgetHistoryCommand(StrictCommand):
    """Reconcile unknown history without permitting allowance edits."""

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Require an exact evidence-backed request and support retry-safe operator keys."""
        return cls(
            "reconcile-budget",
            help="Establish unknown historical fit consumption from retained evidence under the original allowance.",
            params=[
                click.Argument(["run_id"]),
                click.Option(["--request-file"], type=click.Path(exists=True, dir_okay=False), required=True),
                click.Option(["--operation-key"]),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Preserve exact intent, report reconciliation conflicts and emit stable budget evidence."""
        from labqoat._generated.budget_reconciliation_request import BudgetReconciliationRequest
        from labqoat.cli.command_runner import CommandRunner
        from labqoat.cli.output.error_reporter import ErrorReporter
        from labqoat.cli.output.result_writer import ResultWriter

        client = ContextAccessor.current().management()
        try:
            document = CommandRunner.payload({"file": str(ctx.params["request_file"])})
            request = BudgetReconciliationRequest.from_dict(document)
            budget = client.runs.fit_budget.establish(
                str(ctx.params["run_id"]), request, operation_key=ctx.params["operation_key"]
            )
            ResultWriter().write_dict(budget.to_dict())
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
