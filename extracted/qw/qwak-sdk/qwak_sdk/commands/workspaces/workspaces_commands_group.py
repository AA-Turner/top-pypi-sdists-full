import click

from qwak_sdk.commands.workspaces.create.ui import create_workspace
from qwak_sdk.commands.workspaces.delete.ui import delete_workspace
from qwak_sdk.commands.workspaces.start.ui import start_workspace
from qwak_sdk.commands.workspaces.stop.ui import stop_workspace
from qwak_sdk.commands.workspaces.update.ui import update_workspace


@click.group(
    "workspaces",
    help="Commands for interacting with workspaces",
)
def workspaces_commands_group():
    # Click commands group injection
    pass


workspaces_commands_group.add_command(create_workspace)
workspaces_commands_group.add_command(update_workspace)
workspaces_commands_group.add_command(start_workspace)
workspaces_commands_group.add_command(delete_workspace)
workspaces_commands_group.add_command(stop_workspace)
