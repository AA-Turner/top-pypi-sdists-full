"""Forget locally saved credentials."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.auth_output import AuthOutput

if TYPE_CHECKING:
    from labqoat.cli.cli_context import CliContext


class LogoutCommand:
    """Remove saved passwords without touching the server."""

    name = "logout"

    @staticmethod
    def callback() -> None:
        """Delete the stored password for the selected profile."""
        context = ContextAccessor.current()
        username = LogoutCommand.selected_username(context)
        if username is None:
            AuthOutput.logout(False, "No username configured for this profile.")
            return
        LogoutCommand.delete_saved(context, username)
        AuthOutput.logout(True, f"Forgot saved credentials for {username}.")
        if os.environ.get("LABQOAT_PASSWORD"):
            click.echo("Note: LABQOAT_PASSWORD is still set in the environment.", err=True)

    @staticmethod
    def selected_username(context: CliContext) -> str | None:
        """Return the configured username, if any."""
        return context.profile.username or None

    @staticmethod
    def delete_saved(context: CliContext, username: str) -> None:
        """Remove the password from the configured store."""
        context.resolver.delete_password(context.profile, username)

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Build the Click command with named class callbacks."""
        return click.Command(cls.name, callback=cls.callback, help="Forget saved credentials.")
