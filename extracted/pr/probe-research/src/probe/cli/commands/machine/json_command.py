"""agent/src/probe/cli/main.py."""

from __future__ import annotations

import typer

#: `--json`'s help, on `install` and `wizard` alike.
_JSON_HELP = (
    "for a program: stdout carries only NDJSON events (step, device_prompt, "
    "onboarding_required, result, error, done); everything else goes to stderr"
)


class _JsonCommand(typer.core.TyperCommand):
    """`--json` promises a `done` line however the run ends -- including when
    its arguments do not parse, which happens before the command (and its
    event session) ever runs. `--help` is not a run: it prints its help and no
    events. `install`, `wizard` and its `setup` alias all use this."""

    def parse_args(self, ctx, args):  # type: ignore[override]
        wants_json = "--json" in args
        try:
            return super().parse_args(ctx, args)
        except UsageError as exc:  # Typer's own click's (module top), never `import click`
            if wants_json:
                from probe.core import events as json_events

                json_events.done_events(
                    code=json_events.ErrorCode.USAGE,
                    message=exc.format_message(),
                    exit_code=exc.exit_code or 2,
                )
            raise
from probe.cli.commands.commands import UsageError  # noqa: E402 -- pieces need each other; the front door loads this one first
