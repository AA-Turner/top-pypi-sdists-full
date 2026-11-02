"""Deploy a file's web server functions as endpoints, like ``modal deploy``."""

import sys
from contextlib import redirect_stdout
from types import ModuleType

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.compute.function import Function
from labqoat.compute.web_servers import WebServer
from labqoat.json_document import JsonValue


class DeployCommand(StrictCommand):
    """Publish every ``@web_server`` function of a file, or the one named, and print where each is called."""

    def __init__(self) -> None:
        """Take one FILE.py or FILE.py::NAME target."""
        super().__init__(
            "deploy",
            params=[click.Argument(["target"])],
            help="Deploy a file's @web_server functions as endpoints: lab deploy app.py or app.py::chat.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Load the file, then publish each web server and serve it under its name."""
        from labqoat.cli.commands.authored.source_module import SourceModule

        filename, _, name = str(ctx.params["target"]).partition("::")
        source = SourceModule(filename)
        ctx.call_on_close(source.close)
        with redirect_stdout(sys.stderr):
            servers = DeployCommand.servers(source.load(), name)
        context = ContextAccessor.current()
        base = context.profile.base_url.rstrip("/")
        with context.client() as client:
            deployed = [client.endpoints.deploy(function) for function in servers]
        for endpoint in deployed:
            click.echo(f"Deployed {endpoint.name} at {base}{endpoint.path}/", err=True)
        items: list[JsonValue] = [{**endpoint.to_dict(), "url": base + endpoint.path + "/"} for endpoint in deployed]
        ResultWriter().write_dict({"items": items})
        return None

    @staticmethod
    def servers(module: ModuleType, name: str) -> list[Function[..., object]]:
        """The module's web server functions, or the one named, refusing anything else."""
        found = {
            key: value
            for key, value in vars(module).items()
            if isinstance(value, Function) and value.local in WebServer.declared
        }
        if name:
            if name not in found:
                raise click.UsageError(
                    f"{name!r} is not a @web_server function. Available: {', '.join(found) or 'none'}"
                )
            return [found[name]]
        if not found:
            raise click.UsageError("The file declares no @web_server function under @app.function.")
        return list(found.values())
