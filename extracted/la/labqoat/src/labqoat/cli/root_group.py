"""Root Click group accepting selected global options anywhere."""

from __future__ import annotations

from typing import ClassVar

import click
from labqoat.cli.command_hints import CommandHints
from labqoat.cli.output.cli_failure import CliFailure


class RootGroup(click.Group):
    """Move global presentation options ahead of the selected command."""

    movable = frozenset({"--json", "--pretty", "--endpoint", "--environment", "--project", "--no-color", "--select"})
    valued = frozenset({"--endpoint", "--environment", "--project", "--select"})
    sections: ClassVar[dict[str, tuple[str, ...]]] = {
        "Run": ("init", "project", "run", "deploy", "endpoint", "build", "worker", "checkpoint", "import"),
        "Data": ("dataset", "volume", "asset", "dashboard", "memory", "dict", "queue", "secret"),
        "Compute": ("compute", "locations", "pool", "node"),
        "Setup": ("auth", "doctor", "platform", "skills", "agent", "completion"),
    }

    # Names agents reach for that mean exactly one command; they run it rather than fail with a hint.
    aliases: ClassVar[dict[str, str]] = {
        "artifact": "asset",
        "artifacts": "asset",
        "assets": "asset",
        "runs": "run",
        "datasets": "dataset",
        "projects": "project",
        "workers": "worker",
        "checkpoints": "checkpoint",
        "dashboards": "dashboard",
        "volumes": "volume",
    }

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        """Resolve a command by its name or by a plural or synonym that means only it."""
        return super().get_command(ctx, cmd_name) or super().get_command(ctx, self.aliases.get(cmd_name, cmd_name))

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """List commands by what they are for; anything unplaced and not hidden stays visible under its own heading."""
        placed = [name for names in self.sections.values() for name in names]
        other = tuple(name for name in self.list_commands(ctx) if name not in placed and not self.commands[name].hidden)
        for title, names in {**self.sections, "Other": other}.items():
            rows = [(name, self.commands[name].get_short_help_str(80)) for name in names if name in self.commands]
            if rows:
                with formatter.section(title):
                    formatter.write_dl(rows)

    def invoke(self, ctx: click.Context) -> object:
        """Apply one common error boundary around every CLI leaf."""
        from labqoat.cli.output.error_reporter import ErrorReporter

        try:
            return super().invoke(ctx)
        except CliFailure:
            raise
        except KeyboardInterrupt as error:
            raise CliFailure("Interrupted. Accepted work continues.", 130) from error
        except click.Abort as error:
            if isinstance(error.__cause__, KeyboardInterrupt):
                raise CliFailure("Interrupted. Accepted work continues.", 130) from error
            raise CliFailure("Aborted.", 1) from error
        except click.ClickException as error:
            raise CliFailure(CommandHints.explain(error), error.exit_code) from error
        except Exception as error:
            ErrorReporter.report(error)

    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        """Hoist global options while preserving all other argument order."""
        relevant = self._global_tokens(args)
        ctx.meta["output_mode"] = "pretty" if "--pretty" in relevant else "json" if "--json" in relevant else "human"
        try:
            return self._parse(ctx, args)
        except click.ClickException as error:
            raise CliFailure(error.format_message(), error.exit_code) from error

    @staticmethod
    def _global_tokens(args: list[str]) -> list[str]:
        """Stop root flag interpretation at an authored file's parameter boundary."""
        for index, token in enumerate(args):
            if "run" in args[:index] and ".py" in token and not token.startswith("-"):
                return args[:index]
        return args

    def _parse(self, ctx: click.Context, args: list[str]) -> list[str]:
        """Move shared options without consuming authored parameters."""
        global_args: list[str] = []
        command_args: list[str] = []
        seen: set[str] = set()
        index = 0
        while index < len(args):
            token = args[index]
            if "run" in command_args and ".py" in token and not token.startswith("-"):
                command_args.extend(args[index:])
                break
            option = token.partition("=")[0]
            if option not in self.movable:
                command_args.append(token)
                index += 1
                continue
            if option in seen:
                raise click.UsageError(f"Option {option!r} was provided more than once.", ctx)
            seen.add(option)
            global_args.append(token)
            if option in self.valued and "=" not in token:
                if index + 1 >= len(args) or args[index + 1].startswith("-"):
                    raise click.UsageError(f"Option '{option}' requires an argument.", ctx)
                index += 1
                global_args.append(args[index])
            index += 1
        return super().parse_args(ctx, [*global_args, *command_args])
