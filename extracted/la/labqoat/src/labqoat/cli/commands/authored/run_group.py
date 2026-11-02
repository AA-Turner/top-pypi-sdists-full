"""Run catalog with dynamic authored-file entrypoints."""

import sys
from contextlib import redirect_stdout
from typing import ClassVar

import click
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.console.console_options import ConsoleOptions


class RunGroup(click.Group):
    """Resolve an authored target only when explicitly selected by the operator."""

    aliases: ClassVar[dict[str, str]] = {"show": "get", "inspect": "get", "describe": "get"}

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        """Keep management help static and load selected files for generated argument help."""
        command = super().get_command(ctx, self.aliases.get(cmd_name, cmd_name))
        if command is not None or ".py" not in cmd_name:
            return command
        from labqoat.cli.commands.authored.authored_target import AuthoredTarget
        from labqoat.cli.commands.authored.launch_command import LaunchCommand
        from labqoat.cli.commands.authored.source_module import SourceModule

        filename, _, name = cmd_name.partition("::")
        source = SourceModule(filename)
        ctx.call_on_close(source.close)
        with redirect_stdout(sys.stderr):
            module = source.load()
        return LaunchCommand(AuthoredTarget.select(module, name))

    @staticmethod
    def launch_options() -> list[click.Parameter]:
        """Place launch controls before the target so authored option names cannot collide."""
        return [
            *ConsoleOptions.parameters(),
            ObservationDeadline.option(),
            click.Option(["--detach"], is_flag=True, help="Return after durable acceptance instead of following work."),
            click.Option(["--seed"], type=click.IntRange(0, 2**32 - 1), default=0, help="Remote root Run seed."),
            click.Option(["--key"], type=str, help="Optional retry-safe remote submission key."),
        ]
