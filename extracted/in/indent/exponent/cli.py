import click
from click import Context, HelpFormatter

from exponent.commands.checkout_commands import checkout_cli
from exponent.commands.cloud_commands import cloud_cli
from exponent.commands.common import set_log_level
from exponent.commands.config_commands import config_cli
from exponent.commands.run_commands import run, run_cli
from exponent.commands.types import ExponentGroup, exponent_cli_group
from exponent.commands.upgrade import upgrade_cli
from exponent.utils.version import (
    get_installed_version,
)


@exponent_cli_group(invoke_without_command=True)
@click.version_option(get_installed_version(), prog_name="Indent CLI")
@click.pass_context
def cli(ctx: Context) -> None:
    """
    Indent: Your AI pair programmer.

    Run indent to start (or indent run)
    """
    set_log_level()

    # If no command is provided, invoke the 'run' command
    if ctx.invoked_subcommand is None:
        ctx.invoke(run)


sources: list[ExponentGroup] = [
    config_cli,  # Configuration commands
    run_cli,  # Run AI chat commands
    upgrade_cli,  # Upgrade-related commands
    cloud_cli,  # Cloud commands
    checkout_cli,  # Checkout commands
]

for source in sources:
    for command in source.commands.values():
        cli.add_command(command)


def format_commands(
    ctx: Context, formatter: HelpFormatter, include_hidden: bool = False
) -> None:
    commands = []
    hidden_commands = []
    for cmd_name in cli.list_commands(ctx):
        cmd = cli.get_command(ctx, cmd_name)
        if cmd is None:
            continue
        if cmd.hidden:
            hidden_commands.append((cmd_name, cmd))
        else:
            commands.append((cmd_name, cmd))

    if commands:
        max_cmd_length = (
            max(len(cmd_name) for cmd_name, _ in commands) if commands else 0
        )
        limit = (
            (formatter.width or 80) - 6 - max_cmd_length
        )  # Default width to 80 if None
        rows = []
        for cmd_name, cmd in commands:
            help_text = cmd.get_short_help_str(limit)
            rows.append((cmd_name, help_text))

        with formatter.section("Commands"):
            formatter.write_dl(rows)

    if include_hidden and hidden_commands:
        max_cmd_length = (
            max(len(cmd_name) for cmd_name, _ in hidden_commands)
            if hidden_commands
            else 0
        )
        limit = (
            (formatter.width or 80) - 6 - max_cmd_length
        )  # Default width to 80 if None
        hidden_rows = []
        for cmd_name, cmd in hidden_commands:
            help_text = cmd.get_short_help_str(limit)
            hidden_rows.append((cmd_name, help_text))

        with formatter.section("Hidden Commands"):
            formatter.write_dl(hidden_rows)


@cli.command(hidden=True)
@click.pass_context
def hidden(ctx: Context) -> None:
    """Show all commands, including hidden ones."""
    formatter = ctx.make_formatter()
    with formatter.section("Usage"):
        if ctx.parent and ctx.parent.command:
            formatter.write_usage(
                ctx.parent.command.name or "indent", "COMMAND [ARGS]..."
            )
    formatter.write_paragraph()
    with formatter.indentation():
        if cli.help:
            formatter.write_text(cli.help)
    formatter.write_paragraph()
    format_commands(ctx, formatter, include_hidden=True)
    click.echo(formatter.getvalue().rstrip("\n"))


if __name__ == "__main__":
    cli()
