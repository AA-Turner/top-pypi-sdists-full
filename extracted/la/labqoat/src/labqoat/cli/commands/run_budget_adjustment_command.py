"""Explicit version-protected correction of one uncertain fit interval."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.strict_command import StrictCommand


class RunBudgetAdjustmentCommand(StrictCommand):
    """Apply retained evidence without changing original allowances or confirmed usage reports."""

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Require a complete correction request and allow exact operator replay keys."""
        return cls(
            "adjust-budget",
            help="Resolve one expired fit grant's uncertain consumption from retained evidence.",
            params=[
                click.Argument(["run_id"]),
                click.Option(["--request-file"], type=click.Path(exists=True, dir_okay=False), required=True),
                click.Option(["--operation-key"]),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Emit the immutable correction receipt and report conflicts without resubmitting changed intent."""
        from labqoat._generated.budget_adjustment_request import BudgetAdjustmentRequest
        from labqoat.cli.command_runner import CommandRunner
        from labqoat.cli.output.error_reporter import ErrorReporter
        from labqoat.cli.output.result_writer import ResultWriter

        client = ContextAccessor.current().management()
        try:
            document = CommandRunner.payload({"file": str(ctx.params["request_file"])})
            request = BudgetAdjustmentRequest.from_dict(document)
            receipt = client.runs.fit_budget.adjust(
                str(ctx.params["run_id"]), request, operation_key=ctx.params["operation_key"]
            )
            ResultWriter().write_dict(receipt.to_dict())
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
