"""Eager offline version output for every CLI entrypoint."""

from __future__ import annotations

import click


class VersionOption(click.Option):
    """Print package identity before configuration or command execution."""

    def __init__(self) -> None:
        """Declare a root flag that exits without entering the command tree."""
        super().__init__(
            ["--version"],
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=self.show,
            help="Show the installed version and local checkout details, then exit.",
        )

    @staticmethod
    def show(context: click.Context, _parameter: click.Parameter, value: bool) -> None:
        """Load version metadata only for an explicit, non-completion invocation."""
        if not value or context.resilient_parsing:
            return
        from labqoat.cli.version_info import VersionInfo

        click.echo(f"labqoat {VersionInfo.label()}")
        context.exit()
