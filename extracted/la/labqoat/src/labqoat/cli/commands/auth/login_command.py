"""Verify and optionally store API credentials."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click
from labqoat.cli.output.auth_output import AuthOutput

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.errors.api_error import ApiError

if TYPE_CHECKING:
    from labqoat.cli.cli_context import CliContext
    from labqoat.client import Client


class LoginCommand:
    """Prompt for credentials, verify them, and optionally save."""

    name = "login"

    @staticmethod
    def callback(username: str | None, save: bool) -> None:
        """Verify credentials against the status resource."""
        context = ContextAccessor.current()
        credentials = context.resolver.resolve(context.profile, username=username, prompt=True)
        LoginCommand.verify(context, credentials.username, credentials.password)
        if save:
            LoginCommand.persist(context, credentials.username, credentials.password)
            AuthOutput.status(credentials.username, f"Saved credentials for {credentials.username}.")
        else:
            AuthOutput.status(credentials.username, "Verified credentials without saving them.")

    @staticmethod
    def verify(context: CliContext, username: str, password: str) -> None:
        """Check credentials without creating a server session."""
        from labqoat.client import Client

        client: Client = Client(
            context.profile.base_url,
            username,
            password,
            timeout_seconds=context.profile.timeout_seconds,
            environment=context.profile.environment,
        )
        try:
            client.status()
        except ApiError as error:
            ErrorReporter.report(error)
        finally:
            client.close()

    @staticmethod
    def persist(context: CliContext, username: str, password: str) -> None:
        """Save the verified password through the configured store."""
        context.resolver.store_password(context.profile, username, password)
        LoginCommand.merge_username(context, username)

    @staticmethod
    def merge_username(context: CliContext, username: str) -> None:
        """Record the verified username in non-secret profile settings."""
        from labqoat.cli.config.profile import Profile

        stored = context.profiles.load(context.profile.name)
        context.profiles.save(
            Profile(
                name=stored.name,
                base_url=context.profile.base_url,
                username=username,
                timeout_seconds=stored.timeout_seconds,
                environment=context.profile.environment,
            )
        )

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Build the Click command with named class callbacks."""
        return click.Command(
            cls.name,
            callback=cls.callback,
            help="Verify credentials and optionally save them.",
            params=[
                click.Option(["--username"], type=str, default=None, help="Username to verify."),
                click.Option(
                    ["--save/--no-save"],
                    default=True,
                    show_default=True,
                    help="Save the password in the OS keyring.",
                ),
            ],
        )
