"""Deployment of web server functions as endpoints, their management and their tokens."""

import click

from labqoat.cli.commands.serving.deploy_command import DeployCommand
from labqoat.cli.commands.serving.endpoint_command import EndpointAdminCommand
from labqoat.cli.commands.serving.endpoint_token_command import EndpointTokenCommand
from labqoat.cli.group_help import GroupHelp


class ServingCommandCatalog:
    """Add ``deploy`` and the ``endpoint`` group to the root command."""

    @staticmethod
    def add(root: click.Group) -> None:
        """Register commands without loading authored files or credentials."""
        root.add_command(DeployCommand())
        group = click.Group(
            "endpoint",
            help="Read and stop deployed endpoints and manage the tokens that call them.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        for operation in ("list", "get", "delete"):
            group.add_command(EndpointAdminCommand(operation))
        tokens = click.Group(
            "token",
            help="Create, list and revoke bearer tokens for the project's endpoints.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        for operation in ("create", "list", "delete"):
            tokens.add_command(EndpointTokenCommand(operation))
        group.add_command(tokens)
        root.add_command(group)
