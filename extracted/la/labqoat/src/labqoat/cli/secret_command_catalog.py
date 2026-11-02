"""Named credential bundle command group."""

import click

from labqoat.cli.commands.secret_command import SecretCommand
from labqoat.cli.group_help import GroupHelp


class SecretCommandCatalog:
    """Assemble metadata reads and write-only secret mutations."""

    @staticmethod
    def group() -> click.Group:
        """Build the secret group without inspecting local credentials."""
        group = click.Group(
            "secret",
            help="Manage encrypted credentials for runs.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        for operation in ("list", "get", "create", "update", "delete"):
            group.add_command(SecretCommand(operation))
        return group
