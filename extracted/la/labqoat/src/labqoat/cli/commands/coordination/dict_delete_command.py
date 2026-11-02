"""Remove one entry of a dict, or the whole dict."""

import click

from labqoat.cli.commands.coordination.stored_value import StoredValue
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class DictDeleteCommand(StrictCommand):
    """With a key, remove that entry and print its value; without one, delete the dict after confirmation."""

    def __init__(self) -> None:
        """Declare the dict, the optional key and the noninteractive confirmation."""
        super().__init__(
            "delete",
            params=[click.Argument(["name"]), click.Argument(["key"], required=False), ParameterFactory.yes()],
            help="Remove KEY and print its value, or delete the whole dict when no KEY is given.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Pop a key, or confirm and delete the dict."""
        name, key = str(ctx.params["name"]), ctx.params["key"]
        if key is None and not ctx.params["yes"]:
            click.confirm(f"Delete dict {name} and all its entries?", abort=True)
        with ContextAccessor.current().client() as client:
            if key is None:
                client.dicts.delete(name)
                ResultWriter().write_dict({"deleted": name})
                return None
            missing = object()
            value = client.dict(name).pop(str(key), missing)
        if value is missing:
            raise click.ClickException(f"Dict {name} has no key {key!r}.")
        ResultWriter().write_dict({"deleted": str(key), "value": StoredValue.show(value)})
        return None
