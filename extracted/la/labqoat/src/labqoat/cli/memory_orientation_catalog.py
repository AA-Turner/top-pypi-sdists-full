"""Commands that orient an agent and record steps whose bookkeeping memory derives for it."""

from __future__ import annotations

import click

from labqoat.cli.core_command_catalog import CoreCommandCatalog
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.memory_mutation_command import MemoryMutationCommand


class MemoryOrientationCatalog:
    """Frontier, attention, catch-up, decisions and experiment starts."""

    @staticmethod
    def add(group: click.Group) -> None:
        """Register orientation reads and step shortcuts on the memory group."""
        group.add_command(
            EndpointCommand(
                "frontier",
                "/api/v1/memory/frontier",
                [click.Option(["--metric"]), click.Option(["--limit"], type=click.IntRange(1, 50))],
                "Rank current results under each project objective, best first, with the setup keys in use; "
                "the source of truth for 'what is the best result', never brief prose.",
            )
        )
        group.add_command(
            EndpointCommand(
                "attention",
                "/api/v1/memory/attention",
                [],
                "List finished experiments, untested or undecided hypotheses, unlinked results, revised "
                "evidence, decision fallout and handoff files, each with the command that resolves it.",
            )
        )
        group.add_command(
            EndpointCommand(
                "catchup",
                "/api/v1/memory/catchup",
                [
                    click.Option(["--since"], type=click.IntRange(min=0)),
                    click.Option(["--limit"], type=click.IntRange(1, 200)),
                ],
                "Summarize research changed since --since or since this --agent last read; replaces handoff files.",
                reader=True,
            )
        )
        group.add_command(MemoryOrientationCatalog.decide())
        group.add_command(MemoryOrientationCatalog.experiments())

    @staticmethod
    def decide() -> MemoryMutationCommand:
        """Record a consequential choice and the active records it makes obsolete."""
        return MemoryMutationCommand(
            "decide",
            "decide",
            [
                click.Option(["--title"], required=True),
                click.Option(["--rationale"], required=True),
                click.Option(["--summary"]),
                click.Option(["--alternative"], multiple=True, help="Rejected alternative; repeatable."),
                click.Option(
                    ["--affects"], multiple=True, help="Node this decision parks, drops or redirects; repeatable."
                ),
                click.Option(["--supersedes"], help="Earlier decision this one replaces."),
            ],
            "Record a decision node; attention flags each --affects record until its status changes.",
        )

    @staticmethod
    def experiments() -> click.Group:
        """Experiment lifecycle shortcuts that keep run state and research state together."""
        group = CoreCommandCatalog.group("experiment", "Track experiments against the runs that execute them.")
        group.add_command(
            MemoryMutationCommand(
                "start",
                "experiment-start",
                [
                    click.Option(["--node"], required=True, help="Experiment node ID."),
                    click.Option(["--run"], required=True, help="Run executing the experiment."),
                    click.Option(["--note"]),
                ],
                "Mark an experiment running and link its run in one commit; attention flags it when the run ends.",
            )
        )
        return group
