import sys

import click

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton._internals.utils import format_freshness_table
from tecton._internals.utils import format_materialization_attempts
from tecton._internals.utils import get_all_freshness
from tecton.cli import printer
from tecton.cli import workspace_utils
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonGroup
from tecton.cli.workspace_utils import WorkspaceType
from tecton_core.fco_container import FcoContainer
from tecton_core.id_helper import IdHelper
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


@click.group(cls=TectonGroup)
def materialization():
    """View Feature View materialization information."""


@materialization.command(cls=TectonCommand)
@click.argument("feature_view_name")
@click.option("--limit", default=100, type=int, help="Set the maximum limit of results.")
@click.option("--errors-only/--no-errors-only", default=False, help="Only show errors.")
@click.option(
    "--workspace",
    default=None,
    type=WorkspaceType(),
    help="Name of the workspace containing FEATURE_VIEW_NAME. Defaults to the currently selected workspace.",
)
@click.option("--all-columns", is_flag=True, help="Display extra detail columns in the output table.")
def status(feature_view_name, limit, errors_only, workspace, all_columns):
    """Print materialization status for a specified Feature View in the current workspace."""
    # Fetch FeatureView
    workspace_name = workspace if workspace else tecton_context.get_current_workspace()
    workspace_utils.check_workspace_exists(workspace_name)
    fv_request = metadata_service_pb2.GetFeatureViewRequest(
        version_specifier=feature_view_name, workspace=workspace_name
    )
    fv_response = metadata_service.instance().GetFeatureView(fv_request)
    fco_container = FcoContainer.from_proto(fv_response.fco_container)
    fv_spec = fco_container.get_single_root()
    if fv_spec is None:
        printer.safe_print(f"Feature view '{feature_view_name}' not found.")
        sys.exit(1)
    fv_id = IdHelper.from_string(fv_spec.id)

    # Fetch Materialization Status
    status_request = metadata_service_pb2.GetMaterializationStatusRequest(
        feature_package_id=fv_id, workspace=workspace_name
    )
    status_response = metadata_service.instance().GetMaterializationStatus(status_request)

    column_names, materialization_status_rows = format_materialization_attempts(
        status_response.materialization_status.materialization_attempts,
        verbose=all_columns,
        limit=limit,
        errors_only=errors_only,
    )

    # Setting `max_width=0` creates a table with an unlimited width.
    table = Displayable.from_table(headings=column_names, rows=materialization_status_rows, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(column_names))])
    printer.safe_print(table)


@materialization.command(cls=TectonCommand)
@click.option(
    "--workspace",
    default=None,
    type=WorkspaceType(),
    help="Name of the workspace to query. Defaults to the currently selected workspace.",
)
def freshness(workspace):
    """Print feature freshness for Feature Views in the current workspace."""
    # TODO: use GetAllFeatureFreshnessRequest once we implement Chronosphere based API.
    workspace_name = workspace if workspace else tecton_context.get_current_workspace()
    workspace_utils.check_workspace_exists(workspace_name)
    freshness_statuses = get_all_freshness(workspace_name)
    num_fvs = len(freshness_statuses)
    if num_fvs == 0:
        printer.safe_print("No Feature Views found in this workspace.")
        return

    printer.safe_print(format_freshness_table(freshness_statuses))
