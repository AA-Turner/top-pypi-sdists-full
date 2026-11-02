"""Manage secret metadata and securely sourced credential values."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.commands.secret_input import SecretInput
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class SecretCommand(StrictCommand):
    """Expose named bundle operations while printing only public metadata."""

    def __init__(self, operation: str) -> None:
        """Declare a direct value argument and optional credential sources."""
        params: list[click.Parameter] = []
        if operation != "list":
            params.append(click.Argument(["name"]))
        if operation in {"create", "update"}:
            params.extend(
                [
                    click.Argument(["value"], required=False),
                    click.Option(["--env", "environment"], multiple=True, help="Read an environment variable by name."),
                    click.Option(
                        ["--file", "files"], multiple=True, help="Read a value from KEY=PATH, preserving newlines."
                    ),
                ]
            )
        super().__init__(operation, params=params, help=f"{operation.capitalize()} a platform secret.")
        self._operation = operation

    def invoke(self, ctx: click.Context) -> object:
        """Use the host credential boundary and close the transport on every outcome."""
        values = self._values(ctx)
        with ContextAccessor.current().client() as client:
            secrets = client.secrets
            name = str(ctx.params.get("name", ""))
            if self._operation == "delete":
                secrets.delete(name)
                ResultWriter().write_dict({"deleted": name})
            elif self._operation in {"create", "update"}:
                method = secrets.create if self._operation == "create" else secrets.update
                ResultWriter().write_dict(method(name, values).to_dict())
            else:
                result = secrets.list() if self._operation == "list" else secrets.get(name)
                ResultWriter().write_dict(result.to_dict())
        return None

    def _values(self, ctx: click.Context) -> dict[str, str]:
        """Read sources before creating a network client."""
        if self._operation not in {"create", "update"}:
            return {}
        return SecretInput.read(ctx.params["name"], ctx.params["value"], ctx.params["environment"], ctx.params["files"])
