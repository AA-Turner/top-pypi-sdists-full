"""Read and stop the selected project's endpoints."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonValue

HELP = {
    "list": "List the project's endpoints with their URLs, scaling and replicas.",
    "get": "Show one endpoint with its URL, scaling, replicas and last failure.",
    "delete": "Stop an endpoint: cancel its replicas and free its name.",
}


class EndpointAdminCommand(StrictCommand):
    """One operation on the project's endpoints, printing each with the URL it is called at."""

    def __init__(self, operation: str) -> None:
        """Take a name for every operation but list."""
        params: list[click.Parameter] = [] if operation == "list" else [click.Argument(["name"])]
        super().__init__(operation, params=params, help=HELP[operation])
        self._operation = operation

    def invoke(self, ctx: click.Context) -> object:
        """Call the platform and close the client on every outcome."""
        context = ContextAccessor.current()
        base = context.profile.base_url.rstrip("/")
        with context.client() as client:
            endpoints = client.endpoints
            if self._operation == "list":
                items: list[JsonValue] = [
                    {**item.to_dict(), "url": base + item.path + "/"} for item in endpoints.list().items
                ]
                ResultWriter().write_dict({"items": items})
            elif self._operation == "get":
                endpoint = endpoints.get(ctx.params["name"])
                ResultWriter().write_dict({**endpoint.to_dict(), "url": base + endpoint.path + "/"})
            else:
                endpoints.delete(ctx.params["name"])
                ResultWriter().write_dict({"deleted": ctx.params["name"]})
        return None
