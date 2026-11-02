"""Count the values of a queue."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class QueueLenCommand(StrictCommand):
    """Count one partition's values, or all partitions' together with --total."""

    def __init__(self) -> None:
        """Declare the queue, the partition and the total switch."""
        super().__init__(
            "len",
            params=[
                click.Argument(["name"]),
                click.Option(["--partition"], help="Count this partition instead of the default one."),
                click.Option(["--total"], is_flag=True, help="Count every partition together."),
            ],
            help="Count the values waiting in the queue.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Count and print."""
        name = str(ctx.params["name"])
        with ContextAccessor.current().client() as client:
            count = client.queue(name).len(partition=ctx.params["partition"], total=bool(ctx.params["total"]))
        ResultWriter().write_dict({"name": name, "items": count})
        return None
