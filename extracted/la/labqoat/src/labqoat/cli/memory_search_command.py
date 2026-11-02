"""``lab memory search WORDS...``: unquoted words are the query."""

from __future__ import annotations

import click

from labqoat.cli.endpoint_command import EndpointCommand


class MemorySearchCommand(EndpointCommand):
    """Search research; words after the command form the query, so they need no quoting."""

    def invoke(self, ctx: click.Context) -> object:
        """Fold the words into --query, refusing both at once, then search."""
        words = [str(word) for word in ctx.params.pop("words", ())]
        if words and ctx.params.get("query") is not None:
            raise click.UsageError("Give the words or --query, not both.", ctx)
        if words:
            ctx.params["query"] = " ".join(words)
        return super().invoke(ctx)
