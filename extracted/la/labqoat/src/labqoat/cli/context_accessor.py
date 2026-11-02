"""Access to the active CLI invocation context."""

from __future__ import annotations

import click

from labqoat.cli.cli_context import CliContext


class ContextAccessor:
    """Fetch the configured context for command callbacks."""

    @staticmethod
    def current() -> CliContext:
        """Return the active invocation context."""
        context = click.get_current_context().find_root().obj
        if not isinstance(context, CliContext):
            raise click.UsageError("CLI context is not configured.")
        return context
