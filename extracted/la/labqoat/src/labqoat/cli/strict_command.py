"""Click command that rejects repeated long-form options."""

from __future__ import annotations

from collections.abc import Sequence

import click


class StrictCommand(click.Command):
    """Reject duplicate options before callbacks can cause side effects."""

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        """Validate repeated long options, then use Click's normal parser."""
        known = StrictCommand.long_options(self.params)
        identities = {
            option: parameter.name
            for parameter in self.params
            if isinstance(parameter, click.Option)
            for option in (*parameter.opts, *parameter.secondary_opts)
        }
        seen: set[str] = set()
        for token in args:
            option = token.partition("=")[0]
            if option not in known or option == "--help":
                continue
            identity = str(identities[option])
            if identity in seen:
                raise click.UsageError(f"Option {option!r} was provided more than once.", ctx)
            seen.add(identity)
        return super().parse_args(ctx, args)

    @staticmethod
    def long_options(params: Sequence[click.Parameter]) -> set[str]:
        """Return every declared long-form option spelling."""
        options: set[str] = set()
        for parameter in params:
            if isinstance(parameter, click.Option) and not parameter.multiple:
                options.update(option for option in parameter.opts if option.startswith("--"))
                options.update(option for option in parameter.secondary_opts if option.startswith("--"))
        return options
