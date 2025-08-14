import shutil

import click

from gable.cli.helpers.jsonpickle import register_jsonpickle_handlers
from gable.cli.helpers.logging import configure_default_click_logging
from gable.cli.options import global_options
from gable.cli.version import print_version

from .commands.auth import auth
from .commands.contract import contract
from .commands.data_asset import data_asset
from .commands.debug import debug
from .commands.lineage import lineage
from .commands.ping import ping
from .commands.ui import ui

# Configure default logging which uses click.echo(), this will be replaced if the --debug flag is passed
# to the CLI
configure_default_click_logging()
# Configure jsonpickle's custom serialization handlers
register_jsonpickle_handlers()


# Click normally wraps text at 80 characters, but this is too narrow and makes the help text difficult to read.
# This sets the max width to the width of the terminal, which is a better default.
@click.group(
    add_help_option=False,
    context_settings={"max_content_width": shutil.get_terminal_size().columns},
)
@global_options()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show the version and exit.",
)
def cli():
    pass


cli.add_command(auth)
cli.add_command(debug)
cli.add_command(lineage)
cli.add_command(contract)
cli.add_command(data_asset)
cli.add_command(ping)
cli.add_command(ui)


if __name__ == "__main__":
    cli()
