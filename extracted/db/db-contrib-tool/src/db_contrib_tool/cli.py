"""Command-line entry-point into db-contrib-tool."""

import click
from multiprocessing import freeze_support
from db_contrib_tool.evg_aware_bisect.cli import bisect
from db_contrib_tool.setup_mongot_repro_env.cli import setup_mongot_repro_env
from db_contrib_tool.setup_repro_env.cli import setup_repro_env
from db_contrib_tool.symbolizer.cli import symbolize
from db_contrib_tool.usage_analytics import CommandUsage

_PLUGINS = [
    setup_repro_env,
    setup_mongot_repro_env,
    symbolize,
    bisect,
]


@click.group(context_settings=dict(show_default=True, max_content_width=120))
@click.pass_context
def cli(ctx: click.Context) -> None:  # noqa: D401
    """
    The db-contrib-tool - MongoDB's tool for contributors.

    For more information, see the help message for each subcommand.
    For example: db-contrib-tool setup-repro-env --help
    """
    ctx.obj = CommandUsage(command=ctx.invoked_subcommand)


for plugin in _PLUGINS:
    cli.add_command(plugin)


if __name__ == "__main__":
    freeze_support()  # Required for multiprocessing support in a frozen (i.e. PyInstaller) application
    cli(obj=CommandUsage())
