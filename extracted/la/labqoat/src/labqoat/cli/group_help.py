"""Shared callback for help-first command groups."""

from __future__ import annotations

import click


class GroupHelp:
    """Print group help when no subcommand was selected."""

    @staticmethod
    def show(**_values: object) -> None:
        """Render help for an otherwise empty group invocation."""
        context = click.get_current_context()
        if context.invoked_subcommand is None:
            click.echo(context.get_help())
