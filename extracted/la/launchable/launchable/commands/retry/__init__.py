import click

from launchable.utils.click import GroupWithAlias

from .flake_detection import flake_detection


@click.group(cls=GroupWithAlias)
def retry():
    pass


retry.add_command(flake_detection, 'flake-detection')
