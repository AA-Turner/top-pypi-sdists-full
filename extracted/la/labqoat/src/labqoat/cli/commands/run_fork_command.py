"""Explicit changed-work capture with retained source and scientific consumption lineage."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.strict_command import StrictCommand


class RunForkCommand(StrictCommand):
    """Create a new run from a complete, version-protected fork request."""

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Require an explicit captured request file and optionally follow the new execution."""
        return cls(
            "fork",
            help="Create changed work under a new run ID, retaining checkpoint and inherited usage lineage.",
            params=[
                click.Argument(["run_id"]),
                click.Option(["--request-file"], type=click.Path(exists=True, dir_okay=False), required=True),
                click.Option(["--operation-key"]),
                click.Option(["--wait"], is_flag=True),
                ObservationDeadline.option(),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Accept exact file intent and emit stable lineage even when waiting for the new run."""
        from labqoat._generated.fork_request import ForkRequest
        from labqoat.cli.command_runner import CommandRunner
        from labqoat.cli.output.error_reporter import ErrorReporter
        from labqoat.cli.output.result_writer import ResultWriter

        client = ContextAccessor.current().management()
        try:
            document = CommandRunner.payload({"file": str(ctx.params["request_file"])})
            request = ForkRequest.from_dict(document)
            lineage = client.runs.fork(str(ctx.params["run_id"]), request, operation_key=ctx.params["operation_key"])
            ResultWriter().write_dict(lineage.to_dict())
            if ctx.params["wait"]:
                with ObservationDeadline.current(lineage.run_id).watching():
                    client.runs.wait(lineage.run_id)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
