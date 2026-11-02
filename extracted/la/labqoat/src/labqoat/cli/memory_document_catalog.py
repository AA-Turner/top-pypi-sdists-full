"""The project brief and shared file tree command groups."""

from __future__ import annotations
import click
from labqoat.cli.core_command_catalog import CoreCommandCatalog
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.memory_mutation_command import MemoryMutationCommand
from labqoat.cli.memory_files_command import MemoryFilesCommand
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.memory_brief_reads import MemoryBriefReads
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter


class MemoryDocumentCatalog:
    """Read the selected project in one call and maintain its shared documents."""

    @staticmethod
    def brief() -> click.Group:
        """Show the brief by default, with edit and history subcommands."""
        group = click.Group(
            "brief",
            callback=MemoryDocumentCatalog.read,
            invoke_without_command=True,
            help="Read the written intent plus derived frontier, decisions, open work, staleness and attention. "
            "Pass the same --agent you write with: it records what you read and reports what you missed.",
            params=[
                click.Option(["--all", "include_all"], is_flag=True),
                click.Option(
                    ["--limit"], type=click.IntRange(1, 100), help="Rows per section; the server default is 8."
                ),
                click.Option(
                    ["--max-bytes"],
                    type=click.IntRange(8192, 262144),
                    help="Byte ceiling; the server default is 24 KiB.",
                ),
                click.Option(["--agent"], envvar="LABQOAT_AGENT", help="Reader label, such as root or scout-2."),
            ],
        )
        group.add_command(
            MemoryMutationCommand(
                "edit",
                "brief",
                [
                    click.Option(["--body-file"], required=True),
                    click.Option(
                        ["--expected-version"],
                        type=click.IntRange(min=0),
                        help="Brief version this edit builds on; defaults to the version you last read.",
                    ),
                ],
                "Replace the written intent (at most 4096 bytes): goal, strategy and next steps. "
                "Record findings and decisions as nodes; prefer `publish` with a brief applied last.",
            )
        )
        group.add_command(
            EndpointCommand(
                "history",
                "/api/v1/memory/brief/history",
                [click.Option(["--before"], type=click.IntRange(min=1))],
                "Read brief revisions.",
            )
        )
        return group

    @staticmethod
    def read(include_all: bool, limit: int | None, max_bytes: int | None, agent: str | None) -> None:
        """Render the default brief unless a subcommand was chosen, remembering the version read."""
        if click.get_current_context().invoked_subcommand is not None:
            return
        context = ContextAccessor.current()
        client = context.management(agent=agent)
        try:
            chosen = {"limit": limit, "max_bytes": max_bytes}
            query = {
                "all": str(include_all).lower(),
                **{key: value for key, value in chosen.items() if value is not None},
            }
            document = client.get("/api/v1/memory/brief", query)
            project = context.project_name()
            key = MemoryBriefReads.key(context.profile.base_url, context.profile.environment, project, agent)
            MemoryBriefReads().record(key, document.get("brief"))
            ResultWriter().write_dict(document)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()

    @staticmethod
    def files() -> click.Group:
        """Push, pull and inspect shared path versions."""
        group = CoreCommandCatalog.group(
            "files", "Version detailed evidence; link independently useful findings from research nodes."
        )
        group.add_command(MemoryFilesCommand("push"))
        group.add_command(MemoryFilesCommand("pull"))
        group.add_command(
            EndpointCommand(
                "ls",
                "/api/v1/memory/files",
                [
                    click.Argument(["path"], default=""),
                    click.Option(["--after"]),
                    click.Option(["--limit"], type=click.IntRange(1, 500), default=100),
                ],
                "List shared files.",
            )
        )
        group.add_command(
            EndpointCommand(
                "log",
                "/api/v1/memory/files/history",
                [click.Argument(["path"]), click.Option(["--before"], type=click.IntRange(min=1))],
                "Read versions of a shared path.",
            )
        )
        return group
