"""Write one entry of a dict."""

import click

from labqoat.cli.commands.coordination.stored_value import StoredValue
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class DictPutCommand(StrictCommand):
    """Store a JSON value, or text with --text, under a key; the first write creates the dict."""

    def __init__(self) -> None:
        """Declare the dict, key and value, and how the value is read."""
        super().__init__(
            "put",
            params=[
                click.Argument(["name"]),
                click.Argument(["key"]),
                click.Argument(["value"]),
                click.Option(["--text"], is_flag=True, help="Store VALUE as text instead of reading it as JSON."),
                click.Option(["--skip-if-exists"], is_flag=True, help="Leave a key that already holds a value."),
            ],
            help="Store VALUE (JSON, or text with --text) under KEY.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Parse the value before connecting, then write it."""
        value = StoredValue.parse(str(ctx.params["value"]), bool(ctx.params["text"]))
        with ContextAccessor.current().client() as client:
            store = client.dict(str(ctx.params["name"]))
            written = store.put(str(ctx.params["key"]), value, skip_if_exists=bool(ctx.params["skip_if_exists"]))
        ResultWriter().write_dict({"key": str(ctx.params["key"]), "written": written})
        return None
