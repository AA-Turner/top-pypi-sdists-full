"""Remove every entry of a dict."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class DictClearCommand(StrictCommand):
    """Empty a dict after confirmation and keep its name."""

    def __init__(self) -> None:
        """Declare the dict and the noninteractive confirmation."""
        super().__init__(
            "clear",
            params=[click.Argument(["name"]), ParameterFactory.yes()],
            help="Remove every entry of the dict.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Confirm, then clear."""
        name = str(ctx.params["name"])
        if not ctx.params["yes"]:
            click.confirm(f"Remove every entry of dict {name}?", abort=True)
        with ContextAccessor.current().client() as client:
            client.dict(name).clear()
        ResultWriter().write_dict({"cleared": name})
        return None
