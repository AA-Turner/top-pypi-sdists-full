"""Canonical published dashboard command tree."""

from __future__ import annotations

import click

from labqoat.cli.dashboard_init_command import DashboardInitCommand
from labqoat.cli.dashboard_publish_command import DashboardPublishCommand
from labqoat.cli.dashboard_watch_command import DashboardWatchCommand
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.parameter_factory import ParameterFactory


class DashboardCommandCatalog:
    """Assemble all strict published dashboard reads and publication."""

    @staticmethod
    def group() -> click.Group:
        """Build the complete published dashboard group."""
        group = click.Group(
            "dashboard",
            help="Publish and inspect immutable dashboard versions.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        DashboardCommandCatalog._add_publish(group)
        DashboardCommandCatalog._add_reads(group)
        return group

    @staticmethod
    def _add_publish(group: click.Group) -> None:
        """Register offline definition scaffolding and publication from a JSON definition file."""
        group.add_command(DashboardInitCommand())
        group.add_command(
            DashboardPublishCommand([ParameterFactory.path_argument("definition", exists=True, file_only=True)])
        )

    @staticmethod
    def _add_reads(group: click.Group) -> None:
        """Register dashboard collection, item, and history reads."""
        group.add_command(
            EndpointCommand("list", "/api/v1/dashboards", DashboardCommandCatalog.list_filters(), "List dashboards.")
        )
        group.add_command(
            EndpointCommand(
                "get",
                "/api/v1/dashboards/item",
                [ParameterFactory.argument("dashboard_ref"), ParameterFactory.text_option("version")],
                "Get a published dashboard version.",
                "dashboard_ref",
            )
        )
        group.add_command(
            EndpointCommand(
                "versions",
                "/api/v1/dashboards/item/versions",
                DashboardCommandCatalog.version_params(),
                "List one dashboard's immutable versions.",
                "dashboard_ref",
            )
        )
        group.add_command(
            EndpointCommand(
                "changes",
                "/api/v1/dashboards/item/changes",
                [*DashboardCommandCatalog.version_params(), DashboardWatchCommand.panel_option()],
                "List recorded leader and frontier changes, newest first.",
                "dashboard_ref",
            )
        )
        group.add_command(DashboardWatchCommand())

    @staticmethod
    def list_filters() -> list[click.Parameter]:
        """Declare exact dashboard collection filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("name"),
            ParameterFactory.all_projects(),
        ]

    @staticmethod
    def version_params() -> list[click.Parameter]:
        """Declare one dashboard selector plus bounded page controls."""
        return [
            ParameterFactory.argument("dashboard_ref"),
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
        ]
