"""Canonical dataset API and project-workspace command tree."""

from __future__ import annotations

import click

from labqoat.cli.analytics_payload_command import AnalyticsPayloadCommand
from labqoat.cli.commands.dataset_import_command import DatasetImportCommand
from labqoat.cli.dataset_local_command import DatasetLocalCommand
from labqoat.cli.dataset_materialize_command import DatasetMaterializeCommand
from labqoat.cli.dataset_query_command import DatasetQueryCommand
from labqoat.cli.dataset_tag_create_command import DatasetTagCreateCommand
from labqoat.cli.delete_endpoint_command import DeleteEndpointCommand
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.mutation_spec import MutationSpec
from labqoat.cli.parameter_factory import ParameterFactory


class DatasetCommandCatalog:
    """Assemble all strict canonical dataset leaves and nested groups."""

    @staticmethod
    def group() -> click.Group:
        """Build the complete dataset command group."""
        group = DatasetCommandCatalog._group("dataset", "Inspect, import, and mount datasets.")
        DatasetCommandCatalog._add_local(group)
        DatasetCommandCatalog._add_remote(group)
        group.add_command(DatasetImportCommand())
        group.add_command(DatasetCommandCatalog._imports())
        group.add_command(DatasetCommandCatalog._revisions())
        group.add_command(DatasetCommandCatalog._tags())
        return group

    @staticmethod
    def _imports() -> click.Group:
        """Expose durable import inspection without coupling it to a local project."""
        from labqoat.cli.commands.dataset_import_read_command import DatasetImportReadCommand

        group = DatasetCommandCatalog._group("import", "Inspect backend dataset imports.")
        group.add_command(DatasetImportReadCommand())
        return group

    @staticmethod
    def _group(name: str, help_text: str) -> click.Group:
        """Create one help-first dataset group."""
        return click.Group(name, help=help_text, callback=GroupHelp.show, invoke_without_command=True)

    @staticmethod
    def _add_local(group: click.Group) -> None:
        """Register project-local view commands."""
        argument = ParameterFactory.argument
        group.add_command(DatasetLocalCommand("path", [argument("dataset")], "Show a local view path."))
        group.add_command(DatasetLocalCommand("mounts", [], "List managed local dataset views."))
        group.add_command(DatasetLocalCommand("unmount", [argument("dataset")], "Remove a managed local view."))

    @staticmethod
    def _add_remote(group: click.Group) -> None:
        """Register remote reads, deletion, analytics, pins, and views."""
        reference = [ParameterFactory.argument("repository_ref")]
        group.add_command(
            EndpointCommand(
                "list", "/api/v1/dataset-repositories", DatasetCommandCatalog._repo_filters(), "List datasets."
            )
        )
        group.add_command(
            EndpointCommand("get", "/api/v1/dataset-repositories/item", reference, "Get a dataset.", "repository_ref")
        )
        group.add_command(
            DeleteEndpointCommand(
                "delete",
                "/api/v1/dataset-repositories/item",
                "repository_ref",
                [*reference, ParameterFactory.yes()],
                "Delete an empty dataset repository.",
            )
        )
        DatasetCommandCatalog._add_revision_reads(group)
        DatasetCommandCatalog._add_analytics(group)
        dataset: list[click.Parameter] = [ParameterFactory.argument("dataset")]
        for name in ("mount", "materialize"):
            params = [
                *dataset,
                click.Option(["--include"], multiple=True, help="Include logical paths matching a glob; repeatable."),
            ]
            group.add_command(DatasetMaterializeCommand(name, params, f"Create a managed {name} dataset view."))

    @staticmethod
    def _add_revision_reads(group: click.Group) -> None:
        """Register lineage and validation reads."""
        revision = [ParameterFactory.argument("revision_ref")]
        group.add_command(
            EndpointCommand(
                "lineage", "/api/v1/dataset-revisions/lineage", revision, "Read revision lineage.", "revision_ref"
            )
        )
        group.add_command(
            EndpointCommand(
                "validation",
                "/api/v1/dataset-revisions/validation",
                revision,
                "Read revision validation evidence.",
                "revision_ref",
            )
        )

    @staticmethod
    def _add_analytics(group: click.Group) -> None:
        """Register governed sample and query commands."""
        dataset = ParameterFactory.argument("dataset")
        group.add_command(
            AnalyticsPayloadCommand(
                "sample",
                MutationSpec("/api/v1/analytics-queries", renames={"dataset": "dataset_revision_ref"}),
                [dataset, ParameterFactory.limit(default=10, maximum=None)],
                "Return governed sample rows.",
            )
        )
        group.add_command(
            DatasetQueryCommand(
                "query",
                [dataset, ParameterFactory.argument("query")],
                "Run a validated analytics query against a dataset revision.",
            )
        )

    @staticmethod
    def _revisions() -> click.Group:
        """Build revision list, get, and delete leaves."""
        group = DatasetCommandCatalog._group("revision", "Inspect immutable dataset revisions.")
        reference = [ParameterFactory.argument("revision_ref")]
        group.add_command(
            EndpointCommand(
                "list", "/api/v1/dataset-revisions", DatasetCommandCatalog._revision_filters(), "List revisions."
            )
        )
        group.add_command(
            EndpointCommand("get", "/api/v1/dataset-revisions/item", reference, "Get a revision.", "revision_ref")
        )
        group.add_command(
            DeleteEndpointCommand(
                "delete",
                "/api/v1/dataset-revisions/item",
                "revision_ref",
                [*reference, ParameterFactory.yes()],
                "Delete an unreferenced revision.",
            )
        )
        return group

    @staticmethod
    def _tags() -> click.Group:
        """Build immutable tag list and create leaves."""
        group = DatasetCommandCatalog._group("tag", "Discover and create immutable revision tags.")
        group.add_command(
            EndpointCommand("list", "/api/v1/dataset-tags", DatasetCommandCatalog._tag_filters(), "List dataset tags.")
        )
        group.add_command(
            DatasetTagCreateCommand([ParameterFactory.argument("revision_ref"), ParameterFactory.argument("tag_name")])
        )
        return group

    @staticmethod
    def _repo_filters() -> list[click.Parameter]:
        """Declare dataset repository paging and filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("prefix"),
            ParameterFactory.text_option("owner"),
            ParameterFactory.text_option("schema_digest"),
            ParameterFactory.choice_option("archived", ["true", "false"]),
            ParameterFactory.choice_option("sort", ["name:asc", "name:desc"], "name:asc"),
            ParameterFactory.all_projects(),
        ]

    @staticmethod
    def _revision_filters() -> list[click.Parameter]:
        """Declare repository-scoped revision paging and time bounds."""
        return [
            ParameterFactory.argument("repository_ref"),
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.time_option("created_after"),
            ParameterFactory.time_option("created_before"),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:asc"),
        ]

    @staticmethod
    def _tag_filters() -> list[click.Parameter]:
        """Declare repository-scoped tag paging and filters."""
        return [
            ParameterFactory.argument("repository_ref"),
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("prefix"),
            ParameterFactory.choice_option("sort", ["name:asc", "name:desc"], "name:asc"),
        ]
