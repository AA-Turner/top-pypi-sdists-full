"""Read one entry of a dict, or its first entries."""

import itertools

import click

from labqoat.cli.commands.coordination.stored_value import StoredValue
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonValue


class DictGetCommand(StrictCommand):
    """Print the value under a key, or the dict's entries in key order when no key is given."""

    def __init__(self) -> None:
        """Declare the dict, the optional key and how many entries a listing shows."""
        super().__init__(
            "get",
            params=[
                click.Argument(["name"]),
                click.Argument(["key"], required=False),
                click.Option(["--limit"], type=click.IntRange(min=1), default=100, show_default=True),
            ],
            help="Print the value under KEY, or the dict's first entries in key order. Bytes print as base64.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Read and print; a missing key is an error."""
        name, key = str(ctx.params["name"]), ctx.params["key"]
        with ContextAccessor.current().client() as client:
            store = client.dict(name)
            if key is None:
                entries = itertools.islice(store.items(), int(ctx.params["limit"]))
                items: list[JsonValue] = [{"key": k, "value": StoredValue.show(v)} for k, v in entries]
                ResultWriter().write_dict({"name": name, "items": items})
                return None
            missing = object()
            value = store.get(str(key), missing)
        if value is missing:
            raise click.ClickException(f"Dict {name} has no key {key!r}.")
        ResultWriter().write_dict({"key": str(key), "value": StoredValue.show(value)})
        return None
