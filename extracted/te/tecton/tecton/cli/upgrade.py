import click

from tecton import __version__
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonCommandCategory
from tecton.cli.printer import safe_print


@click.command(cls=TectonCommand, command_category=TectonCommandCategory.WORKSPACE)
def upgrade():
    """Instructions to upgrade feature repository to this Tecton SDK version."""
    safe_print(f"No code changes are necessary to upgrade to Tecton SDK version {__version__}.")
