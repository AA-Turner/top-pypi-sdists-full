"""Remove values from a queue, or the whole queue."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class QueueClearCommand(StrictCommand):
    """Empty one partition or all of them with ``clear``, or delete the queue with ``delete``, after confirmation."""

    def __init__(self, operation: str) -> None:
        """Declare ``clear`` with its partition choices, or ``delete``."""
        params: list[click.Parameter] = [click.Argument(["name"]), ParameterFactory.yes()]
        if operation == "clear":
            params += [
                click.Option(["--partition"], help="Clear this partition instead of the default one."),
                click.Option(["--all", "all_partitions"], is_flag=True, help="Clear every partition."),
            ]
        summary = "Remove the values of a partition." if operation == "clear" else "Delete the queue and its values."
        super().__init__(operation, params=params, help=summary)
        self._operation = operation
        self._done = "cleared" if operation == "clear" else "deleted"

    def invoke(self, ctx: click.Context) -> object:
        """Confirm, then clear or delete."""
        name = str(ctx.params["name"])
        if not ctx.params["yes"]:
            click.confirm(f"{self._operation.capitalize()} queue {name}?", abort=True)
        with ContextAccessor.current().client() as client:
            if self._operation == "delete":
                client.queues.delete(name)
            else:
                client.queue(name).clear(
                    partition=ctx.params["partition"], all_partitions=bool(ctx.params["all_partitions"])
                )
        ResultWriter().write_dict({self._done: name})
        return None
