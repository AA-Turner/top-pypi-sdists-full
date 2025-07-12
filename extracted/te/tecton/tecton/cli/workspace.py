import logging
import sys

import click
from colorama import Fore
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Confirm
from rich.text import Text

from tecton import tecton_context
from tecton.cli import printer
from tecton.cli import repo
from tecton.cli import workspace_utils
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton.cli.engine import update_tecton_state
from tecton.cli.infra_commands import interactive_create_ingest_server_group
from tecton.cli.infra_commands import interactive_create_transform_server_group
from tecton.cli.interactive_menu import create_workspace_menu
from tecton.cli.workspace_utils import WorkspaceType
from tecton.cli.workspace_utils import switch_to_workspace
from tecton_proto.common import compute_identity__client_pb2 as compute_identity_pb2


logger = logging.getLogger(__name__)

PROD_WORKSPACE_NAME = "prod"


def _interactive_workspace_selection():
    """Common interactive workspace selection logic."""
    current_workspace = tecton_context.get_current_workspace()
    workspaces = workspace_utils.list_workspaces()

    if not workspaces:
        printer.safe_print("No workspaces available.")
        return

    menu = create_workspace_menu(workspaces, current_workspace)
    selected_workspace = menu.show()

    if selected_workspace is not None:
        switch_to_workspace(selected_workspace.name)


@click.group("workspace", cls=TectonGroup, command_category=TectonCommandCategory.WORKSPACE)
def workspace():
    """Manage Tecton Workspaces."""


@workspace.command()
@click.argument("workspace", type=WorkspaceType(), required=False)
def select(workspace):
    """Select Tecton Workspace. If no workspace is specified, shows an interactive menu."""
    if workspace is not None:
        workspace_utils.check_workspace_exists(workspace)
        switch_to_workspace(workspace)
    else:
        _interactive_workspace_selection()


@workspace.command()
def list():
    """List available Tecton Workspaces."""
    current_workspace = tecton_context.get_current_workspace()
    workspaces = workspace_utils.list_workspaces()
    materializable = [w.name for w in workspaces if w.capabilities.materializable]
    nonmaterializable = [w.name for w in workspaces if not w.capabilities.materializable]

    panels = []

    if materializable:
        live_content = Text()
        for i, name in enumerate(materializable):
            marker = "● " if name == current_workspace else "○ "
            style = "bold green" if name == current_workspace else "white"
            if i > 0:
                live_content.append("\n")
            live_content.append(f"{marker}{name}", style=style)

        live_panel = Panel(
            live_content, title="[bold blue]Live Workspaces[/bold blue]", border_style="blue", padding=(1, 2)
        )
        panels.append(live_panel)

    if nonmaterializable:
        dev_content = Text()
        for i, name in enumerate(nonmaterializable):
            marker = "● " if name == current_workspace else "○ "
            style = "bold green" if name == current_workspace else "white"
            if i > 0:
                dev_content.append("\n")
            dev_content.append(f"{marker}{name}", style=style)

        dev_panel = Panel(
            dev_content,
            title="[bold orange3]Development Workspaces[/bold orange3]",
            border_style="orange3",
            padding=(1, 2),
        )
        panels.append(dev_panel)

    if panels:
        if len(panels) == 2:
            printer.rich_print(Columns(panels, equal=True, expand=True))
        else:
            printer.rich_print(panels[0])
    else:
        printer.safe_print("No workspaces available.")


@workspace.command()
def show():
    """Show active Workspace."""
    workspace_name = tecton_context.get_current_workspace()
    workspace = workspace_utils.get_workspace(workspace_name)
    workspace_type = "Live" if workspace.capabilities.materializable else "Development"
    printer.safe_print(f"{workspace_name} ({workspace_type})")

    compute_identities = workspace.compute_identities
    if len(compute_identities) > 0:
        printer.safe_print("Compute identity:")
    for i, compute_identity in enumerate(compute_identities):
        marker = "*" if i == 0 else " "
        compute_identity_type = compute_identity.WhichOneof("compute_identity")
        if compute_identity_type == "databricks_service_principal":
            printer.safe_print(f"{marker} {compute_identity.databricks_service_principal.application_id}")


@workspace.command()
@click.argument("workspace")
@click.option(
    "--live/--no-live",
    # Kept for backwards compatibility
    "--automatic-materialization-enabled/--automatic-materialization-disabled",
    default=False,
    help="Create a live Workspace, which enables materialization and online serving.",
)
@click.option(
    "--skip-server-groups",
    is_flag=True,
    default=False,
    help="Skip server group creation when creating a live workspace.",
)
def create(workspace, live, skip_server_groups):
    """Create a new Tecton Workspace."""
    # There is a check for this on the server side too, but we optimistically validate
    # here as well to show a pretty error message.
    workspace_names = {w.name for w in workspace_utils.list_workspaces()}
    if workspace in workspace_names:
        printer.safe_print(f"Workspace {workspace} already exists", file=sys.stderr)
        sys.exit(1)

    workspace_utils.create_workspace(workspace, live)

    switch_to_workspace(workspace)

    if live and not skip_server_groups:
        printer.rich_print(
            Panel(
                Text.assemble(
                    ("Transform Server Groups: ", "bold blue"),
                    (
                        "Used to execute user defined transformations for streaming and realtime feature computations.\n",
                        "",
                    ),
                    ("Ingest Server Groups: ", "bold green"),
                    ("Used to ingest streaming data for Tecton's Stream Ingest API.\n\n", ""),
                    (
                        "These server groups provide the compute infrastructure needed for realtime and streaming features.",
                        "dim",
                    ),
                ),
                title="Create Server Groups",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        create_tsg = Confirm.ask("Would you like to create a Transform Server Group?", default=False)
        if create_tsg:
            tsg = interactive_create_transform_server_group(
                workspace, show_description=False, provide_name_defaults=True
            )
            if tsg:
                printer.safe_print()

        create_isg = Confirm.ask("Would you like to create an Ingest Server Group?", default=False)
        if create_isg:
            isg = interactive_create_ingest_server_group(workspace, show_description=False, provide_name_defaults=True)
            if isg:
                printer.safe_print()

    printer.safe_print(
        """
You have created a new workspace. Workspaces let
you create and manage an isolated feature repository.
Running "tecton plan" will compare your local repository
against the remote repository, which is initially empty.
    """
    )


@workspace.command()
@click.argument("workspace", required=True)
@click.option(
    "--id",
    required=True,
    help="Add a new Databricks service principal to the allowlist of the workspace",
)
@click.option(
    "--set-default",
    default=False,
    is_flag=True,
    help="Whether to set the new Databricks service principal as the default compute identity of the workspace",
)
def add_databricks_service_principal(workspace, id, set_default):
    workspace_utils.check_workspace_exists(workspace)
    ws = workspace_utils.get_workspace(workspace)
    compute_identities = ws.compute_identities

    if id in [db_principal.databricks_service_principal.application_id for db_principal in compute_identities]:
        printer.safe_print(
            f"Databricks service principal {id} already exists in the allowlist of workspace {workspace}"
        )
        sys.exit(0)

    new_db_principal = compute_identity_pb2.ComputeIdentity(
        databricks_service_principal=compute_identity_pb2.DatabricksServicePrincipal(application_id=id)
    )
    if set_default:
        compute_identities.insert(0, new_db_principal)
    else:
        compute_identities.append(new_db_principal)
    workspace_utils.update_workspace(workspace, ws.capabilities, compute_identities)

    printer.safe_print(f"Successfully added Databricks service principal {id} to workspace {workspace}")


@workspace.command()
@click.argument("workspace", required=True)
@click.option(
    "--id",
    required=True,
    help="Remove an existing Databricks service principal to the allowlist of the workspace",
)
def remove_databricks_service_principal(workspace, id):
    workspace_utils.check_workspace_exists(workspace)
    ws = workspace_utils.get_workspace(workspace)
    compute_identities = ws.compute_identities

    if id not in [db_principal.databricks_service_principal.application_id for db_principal in compute_identities]:
        printer.safe_print(
            f"Databricks service principal {id} does not exist in the allowlist of workspace {workspace}"
        )
        sys.exit(0)

    compute_identities.remove(
        compute_identity_pb2.ComputeIdentity(
            databricks_service_principal=compute_identity_pb2.DatabricksServicePrincipal(application_id=id)
        )
    )
    workspace_utils.update_workspace(workspace, ws.capabilities, compute_identities)

    printer.safe_print(f"Successfully removed Databricks service principal {id} from workspace {workspace}")


@workspace.command()
@click.argument("workspace", required=True)
@click.option(
    "--id",
    required=True,
    help="Set the Databricks service principal as the default compute identity of the workspace",
)
def set_default_databricks_service_principal(workspace, id):
    workspace_utils.check_workspace_exists(workspace)
    ws = workspace_utils.get_workspace(workspace)
    compute_identities = ws.compute_identities

    if id in [db_principal.databricks_service_principal.application_id for db_principal in compute_identities]:
        compute_identities.remove(
            compute_identity_pb2.ComputeIdentity(
                databricks_service_principal=compute_identity_pb2.DatabricksServicePrincipal(application_id=id)
            )
        )

    compute_identities.insert(
        0,
        compute_identity_pb2.ComputeIdentity(
            databricks_service_principal=compute_identity_pb2.DatabricksServicePrincipal(application_id=id)
        ),
    )
    workspace_utils.update_workspace(workspace, ws.capabilities, compute_identities)

    printer.safe_print(
        f"Successfully set Databricks service principal {id} as the default compute identity of the workspace {workspace}"
    )


@workspace.command()
@click.argument("workspace", type=WorkspaceType())
@click.option("--yes", "-y", is_flag=True)
def delete(workspace, yes):
    """Delete a Tecton Workspace."""
    if workspace == PROD_WORKSPACE_NAME:
        printer.safe_print(f"Deleting Workspace '{PROD_WORKSPACE_NAME}' not allowed.")
        sys.exit(1)

    is_live = workspace_utils.is_live_workspace(workspace)

    confirmation = "y" if yes else None
    while confirmation not in ("y", "n", ""):
        confirmation_text = f'Are you sure you want to delete the workspace "{workspace}"? (y/N)'
        if is_live:
            confirmation_text = f"{Fore.RED}Warning{Fore.RESET}: This will delete any materialized data in this workspace.\n{confirmation_text}"
        confirmation = input(confirmation_text).lower().strip()
    if confirmation == "n" or confirmation == "":
        printer.safe_print("Cancelling delete action.")
        sys.exit(1)

    # archive all fcos in the remote state unconditionally.
    # This will need to be updated when workspaces support materialization.
    update_tecton_state(
        objects=[],
        repo_root="",
        repo_config=None,
        repo_files=[],
        apply=True,
        # Set interactive to False to avoid duplicate confirmation.
        # Confirmation of this action is handled above already.
        interactive=False,
        upgrade_all=False,
        workspace_name=workspace,
    )

    workspace_utils.delete_workspace(workspace)

    if workspace == tecton_context.get_current_workspace():
        switch_to_workspace(PROD_WORKSPACE_NAME)


workspace.add_command(repo.restore)
