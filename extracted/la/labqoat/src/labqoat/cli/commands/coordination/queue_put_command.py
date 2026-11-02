"""Append values to a queue."""

import click

from labqoat.cli.commands.coordination.stored_value import StoredValue
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class QueuePutCommand(StrictCommand):
    """Append JSON values, or text with --text, in the order given; the first put creates the queue."""

    def __init__(self) -> None:
        """Declare the queue, the values and where and how long they go."""
        super().__init__(
            "put",
            params=[
                click.Argument(["name"]),
                click.Argument(["values"], nargs=-1, required=True),
                click.Option(["--partition"], help="Put into this partition instead of the default one."),
                click.Option(
                    ["--ttl"],
                    type=click.IntRange(min=1, max=604_800),
                    default=86_400,
                    show_default=True,
                    help="Seconds after this put until the partition is cleared.",
                ),
                click.Option(["--text"], is_flag=True, help="Store each VALUE as text instead of reading it as JSON."),
            ],
            help="Append VALUES (JSON, or text with --text) to the queue; fails at once when the partition is full.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Parse every value before connecting, then put them all."""
        values = [StoredValue.parse(str(text), bool(ctx.params["text"])) for text in ctx.params["values"]]
        name = str(ctx.params["name"])
        with ContextAccessor.current().client() as client:
            store = client.queue(name)
            store.put_many(values, block=False, partition=ctx.params["partition"], partition_ttl=int(ctx.params["ttl"]))
        ResultWriter().write_dict({"name": name, "put": len(values)})
        return None
