"""List the selected project's dicts or queues."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class StoreListCommand(StrictCommand):
    """Show every dict, with its entries, or every queue, with its values."""

    def __init__(self, kind: str) -> None:
        """Name which collection, ``dict`` or ``queue``, this command lists."""
        counted = "entries" if kind == "dict" else "values in all partitions"
        super().__init__("list", help=f"List the project's {kind}s with their {counted}.")
        self._kind = kind

    def invoke(self, ctx: click.Context) -> object:
        """Read the collection and print it."""
        with ContextAccessor.current().client() as client:
            stores = client.dicts.list() if self._kind == "dict" else client.queues.list()
            ResultWriter().write_dict({"items": [store.to_dict() for store in stores]})
        return None
