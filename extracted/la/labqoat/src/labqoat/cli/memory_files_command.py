"""One-command shared file tree transfers using existing asset credentials."""

from __future__ import annotations
from pathlib import Path
import click
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.memory_file_transfer import MemoryFileTransfer


class MemoryFilesCommand(StrictCommand):
    """Push authored trees or pull the selected project's current shared files."""

    def __init__(self, operation: str) -> None:
        """Declare attribution and local transfer paths."""
        params: list[click.Parameter] = []
        if operation == "push":
            params.extend(
                [
                    click.Argument(["sources"], nargs=-1, required=True, type=click.Path(path_type=Path, exists=True)),
                    click.Option(["--path"], help="Shared path for a single SOURCE; several keep their own paths."),
                    click.Option(["--agent"], required=True, envvar="LABQOAT_AGENT"),
                ]
            )
        else:
            params.extend(
                [
                    click.Argument(["path"], default=""),
                    click.Option(["--directory"], type=click.Path(path_type=Path), default="."),
                ]
            )
        super().__init__(operation, params=params, help=f"{operation.capitalize()} versioned project files.")
        self.operation = operation

    def invoke(self, ctx: click.Context) -> object:
        """Transfer through verified assets and report each saved or reused file."""
        values = ctx.params
        context = ContextAccessor.current()
        client = context.management(agent=values.get("agent"))
        assets = context.assets()
        transfer = MemoryFileTransfer(client, assets, context.project_name())
        try:
            if self.operation == "push":
                result = MemoryFilesCommand.push_all(transfer, values["sources"], values["path"])
            else:
                result = transfer.pull(values["path"], values["directory"])
            ResultWriter().write_dict(result)
        except (ValueError, OSError) as error:
            ErrorReporter.report_usage(str(error))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
            assets.close()
        return None

    @staticmethod
    def push_all(transfer: MemoryFileTransfer, sources: tuple[Path, ...], path: str | None) -> JsonDocument:
        """Push each source under its own shared path; --path names the one source it is given with."""
        if path is not None and len(sources) > 1:
            raise ValueError("--path names one SOURCE; push several without it so each keeps its own path")
        items: list[JsonValue] = []
        for source in sources:
            items.extend(JsonDocument.expect_list(transfer.push(source, path)["items"]))
        return JsonDocument({"items": items})
