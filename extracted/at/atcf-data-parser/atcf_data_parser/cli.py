"""A command line interface for the atcf-data-parser package."""
from __future__ import annotations

import click

from atcf_data_parser import get_dataframe, get_gzipped_url


@click.group()
def cli():
    """Parse “a-deck” data posted online by the Automated Tropical Cyclone Forecasting System."""
    pass


@cli.command()
@click.argument("url", type=str)
def get_fixed_width_data(url: str):
    """Download a fixed-width file from a URL and print its contents."""
    # Read in the  URL
    content = get_gzipped_url(url)

    # Print the file contents
    for line in content.split("\n"):
        click.echo(line)


@cli.command()
@click.argument("url", type=str)
def get_comma_delimited_data(url: str):
    """Download a comma-delimited file from a URL and print its contents."""
    # Get the data as a dataframe
    df = get_dataframe(url)

    # Print the file contents
    click.echo(df.to_csv(index=False))


if __name__ == "__main__":
    cli()
