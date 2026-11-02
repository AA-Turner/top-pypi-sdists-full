"""Concise research memory commands for shared content, statuses and evidence."""

from __future__ import annotations
import click
from labqoat.cli.core_command_catalog import CoreCommandCatalog
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.memory_mutation_command import MemoryMutationCommand
from labqoat.cli.memory_orientation_catalog import MemoryOrientationCatalog
from labqoat.cli.memory_retrieval_catalog import MemoryRetrievalCatalog
from labqoat.cli.memory_document_catalog import MemoryDocumentCatalog


class MemoryCommandCatalog:
    """Expose research knowledge without an agent control plane."""

    kinds = ("question", "source", "hypothesis", "experiment", "result", "conclusion", "decision", "note")

    @staticmethod
    def group() -> click.Group:
        """Build the complete memory command tree."""
        group = CoreCommandCatalog.group(
            "memory", "Record and retrieve the selected project's shared research knowledge."
        )
        group.add_command(MemoryCommandCatalog.nodes())
        MemoryRetrievalCatalog.add(group)
        MemoryOrientationCatalog.add(group)
        group.add_command(MemoryDocumentCatalog.brief())
        group.add_command(MemoryDocumentCatalog.files())
        group.add_command(
            MemoryMutationCommand(
                "publish",
                "publish",
                [click.Argument(["definition"])],
                "Atomically publish one research step from a JSON file or stdin (-): nodes, links, statuses "
                "and a brief edit applied last. Links and statuses may reference new nodes as $client_id.\n\n"
                "\b\nExample step.json:\n"
                '{"nodes": [{"client_id": "res", "kind": "result", "title": "Width 24 reaches 0.81 accuracy",\n'
                '            "parents": [{"node_id": "EXPERIMENT_ID"}],\n'
                '            "properties": {"metric": "val/accuracy", "value": 0.81, "run_id": "RUN_ID"}}],\n'
                ' "links": [{"from_node_id": "$res", "kind": "cites", "target": "run:RUN_ID"}],\n'
                ' "statuses": [{"node_id": "EXPERIMENT_ID", "status": "done"}]}\n\n'
                "Node kinds, properties and link kinds are in the labqoat-memory skill.",
            )
        )
        MemoryCommandCatalog.relationships(group)
        return group

    @staticmethod
    def relationships(group: click.Group) -> None:
        """Make status changes and relationships short, attributable writes."""
        group.add_command(
            MemoryMutationCommand(
                "set-status",
                "status",
                [
                    click.Argument(["node"]),
                    click.Argument(["status"]),
                    click.Option(["--by"]),
                    click.Option(["--evidence"]),
                    click.Option(["--note"]),
                ],
                "Change research status without creating a content revision.",
            )
        )
        group.add_command(
            MemoryMutationCommand(
                "link",
                "link",
                [
                    click.Argument(["from_node_id"]),
                    click.Argument(
                        ["kind"],
                        type=click.Choice(
                            ("supports", "contradicts", "tests", "answers", "supersedes", "cites", "related")
                        ),
                    ),
                    click.Argument(["target"]),
                    click.Option(["--note"]),
                ],
                "Connect nodes; cite files:path, asset:id or run:id.",
            )
        )

    @staticmethod
    def nodes() -> click.Group:
        """Create, inspect and revise stable node identities."""
        group = CoreCommandCatalog.group("node", "Create, inspect and revise research nodes.")
        scope = [click.Argument(["node"])]
        create = [
            click.Option(["--type"], type=click.Choice(MemoryCommandCatalog.kinds), required=True),
            click.Option(
                ["--parent"],
                multiple=True,
                help="Actual derivation parent; use semantic links for evidence relationships.",
            ),
            click.Option(["--supersedes"]),
            click.Option(
                ["--link"],
                multiple=True,
                help="KIND:TARGET link from the new node, e.g. supports:<hypothesis> or cites:files:path; repeatable.",
            ),
            click.Option(["--experiment"], help="Experiment this result came from; adds a cites link."),
            *MemoryCommandCatalog.content_params(True),
        ]
        group.add_command(
            MemoryMutationCommand(
                "create",
                "node",
                create,
                "Create a distinct claim, investigation or finding; optionally supersede an older node.",
            )
        )
        group.add_command(
            EndpointCommand(
                "show",
                "/api/v1/memory/nodes/item",
                [*scope, click.Option(["--revision"])],
                "Read content, evidence and links.",
            )
        )
        group.add_command(
            EndpointCommand(
                "history",
                "/api/v1/memory/nodes/history",
                [*scope, click.Option(["--before"], type=click.IntRange(min=1))],
                "Read immutable content revisions.",
            )
        )
        group.add_command(
            MemoryMutationCommand(
                "revise",
                "revise",
                [*scope, click.Option(["--expected-revision"]), *MemoryCommandCatalog.content_params()],
                "Correct or clarify the same finding; create a node for a distinct claim or new measurement.",
            )
        )
        return group

    @staticmethod
    def content_params(required_title: bool = False) -> list[click.Parameter]:
        """Keep Markdown prose and structured properties in authored files."""
        return [
            click.Option(["--title"], required=required_title),
            click.Option(["--body-file"]),
            click.Option(["--summary"], help="Short claim and scope shown in research previews."),
            click.Option(["--properties-file"]),
            click.Option(["--client-label"]),
            click.Option(["--run", "run_id"]),
            click.Option(["--attempt", "attempt_id"]),
            click.Option(["--attach"], multiple=True, help="Upload and attach a file; repeat for additional files."),
        ]
