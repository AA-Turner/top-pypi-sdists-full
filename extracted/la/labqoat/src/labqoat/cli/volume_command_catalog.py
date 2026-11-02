"""Volume command group."""

import click

from labqoat.cli.commands.volume.volume_command import VolumeCommand
from labqoat.cli.commands.volume.volume_ls_command import VolumeLsCommand
from labqoat.cli.commands.volume.volume_transfer_command import VolumeTransferCommand
from labqoat.cli.group_help import GroupHelp


class VolumeCommandCatalog:
    """Assemble volume management, listing and file transfer commands."""

    @staticmethod
    def group() -> click.Group:
        """Build the volume group without contacting the platform."""
        group = click.Group(
            "volume",
            help="Manage the project's volumes: filesystems runs mount, kept in platform storage.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        for operation in ("create", "list", "delete"):
            group.add_command(VolumeCommand(operation))
        group.add_command(VolumeLsCommand())
        for operation in ("put", "get", "rm"):
            group.add_command(VolumeTransferCommand(operation))
        return group
