import click
import os
from .utils import get_quam_state_path


@click.group()
def cli():
    """A CLI tool for managing CQC QuAM state."""
    pass


@cli.command()
def set():
    """Set a configuration value."""
    click.echo("Set command called")
    # Add your set logic here


@cli.command()
def info():
    """Display information."""
    click.echo("Info command called")
    # Add your info logic here


@cli.command()
def load():
    """Load data or configuration."""
    # Run `cqc-quam-state load`
    # Get QuAM state path using the utility function
    quam_state_path = str(get_quam_state_path())
    # print(f"QuAM state path: {type(quam_state_path)}")

    click.echo(f"export QUAM_STATE_PATH={quam_state_path}")


if __name__ == "__main__":
    cli()
