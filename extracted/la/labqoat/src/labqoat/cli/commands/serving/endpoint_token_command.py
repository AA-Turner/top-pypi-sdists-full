"""Manage the bearer tokens that call the selected project's private endpoints."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand

HELP = {
    "create": "Create a token for the project's endpoints; its secret is printed only now.",
    "list": "List the project's endpoint tokens without their secrets.",
    "delete": "Revoke a token; calls with it are refused from now on.",
}


class EndpointTokenCommand(StrictCommand):
    """One operation on the project's endpoint tokens."""

    def __init__(self, operation: str) -> None:
        """Take a name for every operation but list."""
        params: list[click.Parameter] = [] if operation == "list" else [click.Argument(["name"])]
        super().__init__(operation, params=params, help=HELP[operation])
        self._operation = operation

    def invoke(self, ctx: click.Context) -> object:
        """Call the platform and close the client on every outcome."""
        with ContextAccessor.current().client() as client:
            endpoints = client.endpoints
            if self._operation == "create":
                ResultWriter().write_dict(endpoints.create_token(ctx.params["name"]).to_dict())
            elif self._operation == "list":
                ResultWriter().write_dict(endpoints.list_tokens().to_dict())
            else:
                endpoints.delete_token(ctx.params["name"])
                ResultWriter().write_dict({"deleted": ctx.params["name"]})
        return None
