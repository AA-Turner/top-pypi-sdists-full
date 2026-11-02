"""Stable authentication receipts without credential material."""

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.json_writer import JsonWriter


class AuthOutput:
    """Keep existing concise human diagnostics alongside structured authentication results."""

    @staticmethod
    def status(username: str, message: str) -> None:
        """Report a verified username and connection without ever serializing a password."""
        context = ContextAccessor.current()
        if context.output_mode == "human":
            click.echo(message)
        else:
            JsonWriter().write(
                {
                    "profile": context.profile.name,
                    "base_url": context.profile.base_url,
                    "username": username,
                    "credentials_present": True,
                    "verified": True,
                }
            )

    @staticmethod
    def logout(removed: bool, message: str) -> None:
        """Acknowledge only the local credential removal."""
        context = ContextAccessor.current()
        if context.output_mode == "human":
            click.echo(message)
        else:
            JsonWriter().write({"profile": context.profile.name, "credentials_removed": removed})
