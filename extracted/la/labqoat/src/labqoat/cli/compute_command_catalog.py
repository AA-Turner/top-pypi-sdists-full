"""``compute`` group: shared limits, usage, offerings, location policy, connected hosts and sites."""

from __future__ import annotations

import click

from labqoat.cli.compute.compute_read_command import ComputeReadCommand
from labqoat.cli.compute.offerings_command import OfferingsCommand
from labqoat.cli.compute.quotas_command import QuotasCommand
from labqoat.cli.compute.host_enroll_command import HostEnrollCommand
from labqoat.cli.compute.host_remove_command import HostRemoveCommand
from labqoat.cli.compute.host_share_command import HostShareCommand
from labqoat.cli.compute.location_set_command import LocationSetCommand
from labqoat.cli.compute.settings_group import SettingsGroup
from labqoat.cli.compute.site_remove_command import SiteRemoveCommand
from labqoat.cli.group_help import GroupHelp


class ComputeCommandCatalog:
    """Assemble the administrator compute command tree."""

    @staticmethod
    def group() -> click.Group:
        """Build the complete compute group."""
        group = ComputeCommandCatalog._group("compute", "Manage shared compute limits, locations and connected hosts.")
        group.add_command(SettingsGroup.group())
        group.add_command(ComputeReadCommand("usage", "usage", "Show held, draining and lifecycle compute usage."))
        group.add_command(OfferingsCommand())
        group.add_command(QuotasCommand())
        group.add_command(ComputeCommandCatalog._location())
        group.add_command(ComputeCommandCatalog._hosts())
        group.add_command(ComputeCommandCatalog._sites())
        return group

    @staticmethod
    def _location() -> click.Group:
        """Build location policy reads and updates."""
        group = ComputeCommandCatalog._group("location", "Inspect or change one location's hardware policy.")
        group.add_command(ComputeReadCommand("get", "location", "Show a location's policy.", ["location_id"]))
        group.add_command(LocationSetCommand())
        return group

    @staticmethod
    def _hosts() -> click.Group:
        """Build connected-host enrollment, inspection, share and removal commands."""
        group = ComputeCommandCatalog._group("hosts", "Enroll and manage existing machines.")
        group.add_command(ComputeReadCommand("list", "hosts", "List connected hosts."))
        group.add_command(ComputeReadCommand("get", "host", "Show one connected host.", ["host_id"]))
        group.add_command(HostEnrollCommand())
        group.add_command(HostShareCommand())
        group.add_command(HostRemoveCommand())
        return group

    @staticmethod
    def _sites() -> click.Group:
        """Build existing-machine site removal."""
        group = ComputeCommandCatalog._group("sites", "Remove existing-machine sites.")
        group.add_command(SiteRemoveCommand())
        return group

    @staticmethod
    def _group(name: str, help_text: str) -> click.Group:
        """Create one help-first group."""
        return click.Group(name, help=help_text, callback=GroupHelp.show, invoke_without_command=True)
