"""Operator-visible retry identity retained before the first mutating request."""

from uuid import uuid4

import sys

import click

from labqoat.cli.output.output_style import OutputStyle


class MutationKey:
    """Validate explicit keys and announce newly generated keys before remote side effects."""

    @staticmethod
    def option() -> click.Option:
        """Expose the shared spelling without leaking it into authored request payloads."""
        return click.Option(["--key"], type=str, help="Replay an identical mutation with this operation key.")

    @staticmethod
    def resolve(value: object = None) -> str:
        """Keep the chosen identity available to structured failure reporting."""
        key = str(uuid4()) if value is None else str(value)
        if not 1 <= len(key.encode()) <= 200:
            raise click.UsageError("Operation keys must contain 1-200 UTF-8 bytes.")
        context = click.get_current_context(silent=True)
        if context is not None:
            context.meta["mutation_key"] = key
        if value is None and OutputStyle.current(sys.stderr) == "compact":
            click.echo(f"key {key}", err=True)
        return key
