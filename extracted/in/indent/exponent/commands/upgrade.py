import click

from exponent.commands.types import exponent_cli_group
from exponent.utils.version import check_exponent_version, upgrade_exponent


@exponent_cli_group()
def upgrade_cli() -> None:
    """Manage Indent version upgrades."""
    pass


@upgrade_cli.command()
@click.option(
    "--force",
    is_flag=True,
    help="Upgrade without prompting for confirmation, if a new version is available.",
)
def upgrade(force: bool = False) -> None:
    """Upgrade Indent to the latest version."""
    if result := check_exponent_version():
        installed_version, latest_version = result
        upgrade_exponent(
            current_version=installed_version,
            new_version=latest_version,
            force=force,
        )
    else:
        click.echo("Indent is already up to date.")
