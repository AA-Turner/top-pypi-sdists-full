#!/usr/bin/env python3

import click
import click_completion
click_completion.init()

from adam import batch
from adam.cli_group import cli
from adam.utils import display_help
from . import __version__, repl

@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))

@cli.command()
def help():
    """Show help message and exit."""
    display_help(True)

if __name__ == "__main__":
    cli()
