"""Copy files into a volume, out of it, or remove them from it."""

import time
from pathlib import Path
from typing import ClassVar

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonValue


class VolumeTransferCommand(StrictCommand):
    """``put``, ``get`` or ``rm``; transfers say how long they took."""

    HELP: ClassVar[dict[str, str]] = {
        "put": "Copy a local file, or a directory's contents, into a volume at REMOTE (the root by default). "
        "A file goes into REMOTE when it ends with '/'. Repeating an interrupted put resumes it.",
        "get": "Copy a file or directory of a volume to LOCAL. Files already there with the same content are "
        "skipped and a partly downloaded file resumes.",
        "rm": "Remove a file or directory from a volume; a directory that holds anything needs --recursive.",
    }

    def __init__(self, operation: str) -> None:
        """Declare the arguments of the operation."""
        params: list[click.Parameter] = [click.Argument(["name"])]
        if operation == "put":
            params += [click.Argument(["local"]), click.Argument(["remote"], required=False, default="")]
        elif operation == "get":
            params += [click.Argument(["remote"]), click.Argument(["local"], required=False, default=".")]
        else:
            params += [
                click.Argument(["remote"]),
                click.Option(["--recursive", "-r"], is_flag=True, help="Remove a directory and everything in it."),
            ]
        super().__init__(operation, params=params, help=self.HELP[operation])
        self._operation = operation

    def invoke(self, ctx: click.Context) -> object:
        """Run the transfer and report what it did."""
        name, remote = str(ctx.params["name"]), str(ctx.params["remote"])
        started = time.monotonic()
        with ContextAccessor.current().client() as client:
            volumes = client.volumes
            if self._operation == "put":
                result: dict[str, JsonValue] = {"version": volumes.put(name, Path(str(ctx.params["local"])), remote)}
            elif self._operation == "get":
                result = {"files": volumes.download(name, remote, Path(str(ctx.params["local"])))}
            else:
                result = {"version": volumes.remove(name, remote, recursive=bool(ctx.params["recursive"]))}
        seconds = round(time.monotonic() - started, 2)
        ResultWriter().write_dict({"volume": name, "path": remote, **result, "seconds": seconds})
        return None
