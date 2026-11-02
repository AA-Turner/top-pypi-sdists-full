"""Take values from a queue."""

import queue

import click

from labqoat.cli.commands.coordination.stored_value import StoredValue
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonValue


class QueueGetCommand(StrictCommand):
    """Remove and print the oldest values; they are gone from the queue for every other taker."""

    def __init__(self) -> None:
        """Declare the queue, how many values, from where and how long to wait for the first."""
        super().__init__(
            "get",
            params=[
                click.Argument(["name"]),
                click.Option(["-n", "--count"], type=click.IntRange(min=1, max=1_000), default=1, show_default=True),
                click.Option(["--partition"], help="Take from this partition instead of the default one."),
                click.Option(
                    ["--timeout"],
                    type=click.FloatRange(min=0),
                    default=0.0,
                    show_default=True,
                    help="Seconds to wait for a first value; without it an empty queue prints no values.",
                ),
            ],
            help="Remove and print up to COUNT of the oldest values. Bytes print as base64.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Take and print; an empty queue prints an empty list."""
        name = str(ctx.params["name"])
        timeout = float(ctx.params["timeout"])
        with ContextAccessor.current().client() as client:
            store = client.queue(name)
            try:
                taken = store.get_many(
                    int(ctx.params["count"]), block=timeout > 0, timeout=timeout, partition=ctx.params["partition"]
                )
            except queue.Empty:
                taken = []
        values: list[JsonValue] = [StoredValue.show(value) for value in taken]
        ResultWriter().write_dict({"name": name, "values": values})
        return None
