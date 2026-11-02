"""Canonical asset, build, and checkpoint command groups."""

from __future__ import annotations

import click

from labqoat.cli.delete_endpoint_command import DeleteEndpointCommand
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.log_feed_command import LogFeedCommand
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.build_watch_command import BuildWatchCommand


class CoreCommandCatalog:
    """Assemble the foundational remote-management command groups."""

    @staticmethod
    def add(root: click.Group) -> None:
        """Register every foundational group on the root command."""
        root.add_command(CoreCommandCatalog.assets())
        root.add_command(CoreCommandCatalog.builds())
        root.add_command(CoreCommandCatalog.checkpoints())

    @staticmethod
    def group(name: str, help_text: str) -> click.Group:
        """Create one help-first canonical group."""
        return click.Group(name, help=help_text, callback=GroupHelp.show, invoke_without_command=True)

    @staticmethod
    def assets() -> click.Group:
        """Build strict asset inspection and transfer commands."""
        from labqoat.cli.commands.assets.cat_command import CatCommand
        from labqoat.cli.commands.assets.download_command import DownloadCommand
        from labqoat.cli.commands.assets.upload_command import UploadCommand

        group = CoreCommandCatalog.group("asset", "Inspect and transfer immutable assets.")
        group.add_command(
            EndpointCommand("list", "/api/v1/asset-records", CoreCommandCatalog.asset_filters(), "List assets.")
        )
        reference = [ParameterFactory.argument("reference")]
        group.add_command(EndpointCommand("get", "/api/v1/asset-records/item", reference, "Get an asset.", "reference"))
        group.add_command(UploadCommand.as_click_command())
        group.add_command(DownloadCommand.as_click_command())
        group.add_command(CatCommand.as_click_command())
        return group

    @staticmethod
    def asset_filters() -> list[click.Parameter]:
        """Declare the exact asset collection filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("media_type"),
            ParameterFactory.choice_option("availability", ["pending", "available", "deleting", "deleted"]),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:desc"),
        ]

    @staticmethod
    def builds() -> click.Group:
        """Build strict build catalog and progress commands."""
        group = CoreCommandCatalog.group("build", "Inspect source builds.")
        group.add_command(EndpointCommand("list", "/api/v1/builds", CoreCommandCatalog.build_filters(), "List builds."))
        reference = [ParameterFactory.argument("build_ref")]
        group.add_command(EndpointCommand("get", "/api/v1/builds/item", reference, "Get a build.", "build_ref"))
        group.add_command(
            EndpointCommand("progress", "/api/v1/builds/item", reference, "Get build progress.", "build_ref")
        )
        group.add_command(
            LogFeedCommand(
                "/api/v1/builds/item/logs",
                [
                    ParameterFactory.argument("build_ref"),
                    ParameterFactory.limit(),
                    ParameterFactory.text_option("cursor"),
                ],
                "Read or follow build logs.",
                "build_ref",
            )
        )
        group.add_command(BuildWatchCommand(reference))
        return group

    @staticmethod
    def build_filters() -> list[click.Parameter]:
        """Declare the exact build collection filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.choice_option("state", ["upload_pending", "queued", "building", "succeeded", "failed"]),
            ParameterFactory.choice_option("kind", ["compute", "import", "training"]),
            ParameterFactory.text_option("family_name"),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:desc"),
        ]

    @staticmethod
    def checkpoints() -> click.Group:
        """Build strict checkpoint catalog commands."""
        group = CoreCommandCatalog.group("checkpoint", "Inspect and delete training checkpoints.")
        group.add_command(
            EndpointCommand(
                "list",
                "/api/v1/checkpoints",
                CoreCommandCatalog.checkpoint_filters(),
                "List checkpoints.",
                query_renames={"run": "run_id"},
            )
        )
        reference = [ParameterFactory.argument("checkpoint_ref")]
        group.add_command(
            EndpointCommand("get", "/api/v1/checkpoints/item", reference, "Get a checkpoint.", "checkpoint_ref")
        )
        deletion = [ParameterFactory.argument("resource_id"), ParameterFactory.yes()]
        group.add_command(
            DeleteEndpointCommand("delete", "/api/v1/checkpoints/item", "resource_id", deletion, "Delete a checkpoint.")
        )
        return group

    @staticmethod
    def checkpoint_filters() -> list[click.Parameter]:
        """Declare the exact checkpoint collection filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("run"),
            ParameterFactory.text_option("execution_digest"),
            ParameterFactory.text_option("schema_digest"),
            ParameterFactory.integer_option("step_min"),
            ParameterFactory.integer_option("step_max"),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:desc"),
        ]
