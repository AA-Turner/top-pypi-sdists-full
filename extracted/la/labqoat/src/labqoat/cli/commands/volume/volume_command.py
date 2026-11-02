"""Create, list and remove volumes of the selected project."""

from typing import ClassVar

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.strict_command import StrictCommand


class VolumeCommand(StrictCommand):
    """One of ``create``, ``list`` and ``delete``, printing the volume's public summary."""

    HELP: ClassVar[dict[str, str]] = {
        "create": "Create an empty volume. Functions mounting a volume that does not exist create it too.",
        "list": "List the project's volumes with their versions, file counts and sizes.",
        "delete": "Delete a volume and everything in it. Its name is free again at once.",
    }

    def __init__(self, operation: str) -> None:
        """Declare the volume name where the operation needs one."""
        params: list[click.Parameter] = [] if operation == "list" else [click.Argument(["name"])]
        if operation == "delete":
            params.append(ParameterFactory.yes())
        super().__init__(operation, params=params, help=self.HELP[operation])
        self._operation = operation

    def invoke(self, ctx: click.Context) -> object:
        """Perform the operation through the selected project's client."""
        name = str(ctx.params.get("name", ""))
        if self._operation == "delete" and not ctx.params["yes"]:
            click.confirm(f"Delete volume {name} and everything in it?", abort=True)
        with ContextAccessor.current().client() as client:
            volumes = client.volumes
            if self._operation == "list":
                ResultWriter().write_dict(volumes.list().to_dict())
            elif self._operation == "create":
                ResultWriter().write_dict(volumes.create(name).to_dict())
            else:
                volumes.delete(name)
                ResultWriter().write_dict({"deleted": name})
        return None
