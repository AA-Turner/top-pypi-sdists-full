"""List what a volume holds at a path."""

from datetime import UTC, datetime

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonValue
from labqoat.volumes.volume_entry import VolumeEntry


class VolumeLsCommand(StrictCommand):
    """Show a directory's children, everything below it with ``--recursive``, or the one entry a path names."""

    def __init__(self) -> None:
        """Declare the volume, the path and the recursive switch."""
        super().__init__(
            "ls",
            params=[
                click.Argument(["name"]),
                click.Argument(["path"], required=False, default=""),
                click.Option(["--recursive", "-r"], is_flag=True, help="List everything below the path."),
            ],
            help="List a volume's files and directories at PATH (the root by default).",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Read the entries and print one row each."""
        with ContextAccessor.current().client() as client:
            version, entries = client.volumes.entries(
                str(ctx.params["name"]), str(ctx.params["path"]), recursive=bool(ctx.params["recursive"])
            )
        items: list[JsonValue] = [self.row(entry) for entry in entries]
        ResultWriter().write_dict({"version": version, "items": items})
        return None

    @staticmethod
    def row(entry: VolumeEntry) -> dict[str, JsonValue]:
        """One entry as a listing shows it; directories carry no size or time."""
        row: dict[str, JsonValue] = {"path": entry.path, "kind": entry.kind}
        if entry.kind == "file":
            row["size"] = entry.size
            row["modified"] = datetime.fromtimestamp(entry.mtime, UTC).isoformat().replace("+00:00", "Z")
        if entry.kind == "symlink":
            row["target"] = entry.target
        return row
