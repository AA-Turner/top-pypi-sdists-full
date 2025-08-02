import click
from gable.cli.commands.data_asset_check import check_data_asset
from gable.cli.commands.data_asset_check_plugin import (
    check_click_command_for_asset_plugin,
)
from gable.cli.commands.data_asset_create_contracts import create_data_asset_contracts
from gable.cli.commands.data_asset_delete import delete_data_asset
from gable.cli.commands.data_asset_list import list_data_assets
from gable.cli.commands.data_asset_register import register_data_asset
from gable.cli.commands.data_asset_register_plugin import (
    asset_plugins,
    register_click_command_for_asset_plugin,
)
from gable.cli.commands.data_asset_show import show_data_asset
from gable.cli.options import global_options


@click.group(name="data-asset")
@global_options()
def data_asset():
    """Commands for data assets"""


data_asset.add_command(list_data_assets)
data_asset.add_command(register_data_asset)
data_asset.add_command(check_data_asset)
data_asset.add_command(create_data_asset_contracts)
data_asset.add_command(delete_data_asset)
data_asset.add_command(show_data_asset)


# Add hidden new register subcommand for plugins as we migrate
@click.group(name="register-new", hidden=True)
def register_new():
    """Register new data assets"""


# Add hidden new check subcommand for plugins as we migrate
@click.group(name="check-new", hidden=True)
def check_new():
    """Register new data assets"""


for plugin in asset_plugins:
    register_new.add_command(register_click_command_for_asset_plugin(plugin))
    check_new.add_command(check_click_command_for_asset_plugin(plugin))

data_asset.add_command(register_new)
data_asset.add_command(check_new)
