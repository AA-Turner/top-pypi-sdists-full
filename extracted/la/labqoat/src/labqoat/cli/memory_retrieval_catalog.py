"""Search research and resume a finite stream of compact changes."""

from __future__ import annotations
import click
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.memory_search_command import MemorySearchCommand


class MemoryRetrievalCatalog:
    """Expose research search and finite change pages."""

    @staticmethod
    def add(group: click.Group) -> None:
        """Register reads of the selected project."""
        group.add_command(
            MemorySearchCommand(
                "search",
                "/api/v1/memory/search",
                [
                    click.Argument(["words"], nargs=-1),
                    click.Option(["--query"], help="Research question or keywords; omit for recent records."),
                    click.Option(["--kind"], help="Restrict to a research node type or file."),
                    click.Option(
                        ["--after"], help="Resume a frozen search within seven days; retain query and filters."
                    ),
                    click.Option(["--run", "run_id"]),
                    click.Option(["--node"]),
                    click.Option(["--all"], is_flag=True, flag_value="true", default="false"),
                    click.Option(
                        ["--limit"], type=click.IntRange(1, 50), help="Results per page; the server default is 8."
                    ),
                    click.Option(
                        ["--mode"],
                        type=click.Choice(["hybrid", "lexical", "semantic"]),
                        default="hybrid",
                        show_default=True,
                        help="Hybrid combines keyword and semantic matches; embedding failures fall back to lexical.",
                    ),
                    click.Option(
                        ["--depth"],
                        type=click.IntRange(0, 4),
                        default=2,
                        show_default=True,
                        help="Evidence-link hops; zero disables expansion.",
                    ),
                    click.Option(
                        ["--max-bytes"],
                        type=click.IntRange(8_192, 262_144),
                        help="Response context budget in bytes (server default 20480); omissions are reported.",
                    ),
                ],
                "Search research with pinned evidence: lab memory search WORDS..., or --query. "
                "Superseded and dropped nodes are hidden unless --all. "
                "Inspect retrieval.mode and warnings for fallback or incomplete indexing. "
                "An unrelated query returns nothing with no_confident_match. "
                "Search retains at most 200 candidates; narrow capped queries for broader coverage.",
            )
        )
        group.add_command(
            EndpointCommand(
                "changes",
                "/api/v1/memory/changes",
                [
                    click.Option(["--after"], type=click.IntRange(min=0), default=0),
                    click.Option(["--limit"], type=click.IntRange(1, 500), default=100),
                ],
                "Read compact changes; next_cursor is null at the end.",
            )
        )
