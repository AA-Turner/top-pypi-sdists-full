"""Check saved credentials against the status resource."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.auth_output import AuthOutput


class AuthStatusCommand:
    """Report whether the selected credentials are accepted."""

    name = "status"

    @staticmethod
    def callback() -> None:
        """Verify without displaying secrets."""
        context = ContextAccessor.current()
        credentials = context.resolver.resolve(context.profile, prompt=False)
        from labqoat.cli.commands.auth.login_command import LoginCommand

        LoginCommand.verify(context, credentials.username, credentials.password)
        AuthOutput.status(credentials.username, f"Authenticated as {credentials.username}.")

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Build the Click command with named class callbacks."""
        return click.Command(cls.name, callback=cls.callback, help="Check saved credentials.")
