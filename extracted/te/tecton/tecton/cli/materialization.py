import sys
from datetime import datetime

import click

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton._internals.utils import can_be_stale
from tecton._internals.utils import format_materialization_attempts
from tecton._internals.utils import format_seconds_into_highest_unit
from tecton._internals.utils import get_all_freshness
from tecton.cli import printer
from tecton.cli import workspace_utils
from tecton.cli.cli_utils import display_table
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton.cli.workspace_utils import WorkspaceType
from tecton_core.fco_container import FcoContainer
from tecton_core.id_helper import IdHelper
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


@click.group(cls=TectonGroup, command_category=TectonCommandCategory.INFRA)
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

    display_table(column_names, materialization_status_rows)


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

    # Format freshness data for display_table
    timestamp_format = "%x %H:%M"
    headers = [
        "Feature View",
        "Materialized?",
        "Stale?",
        "Freshness",
        "Expected Freshness",
        "Created",
        "Stream?",
    ]

    freshness_data = [
        (
            ff_proto.feature_view_name,
            str(ff_proto.materialization_enabled),
            str(ff_proto.is_stale) if can_be_stale(ff_proto) else "-",
            format_seconds_into_highest_unit(ff_proto.freshness.seconds) if can_be_stale(ff_proto) else "-",
            format_seconds_into_highest_unit(ff_proto.expected_freshness.seconds) if can_be_stale(ff_proto) else "-",
            datetime.fromtimestamp(ff_proto.created_at.seconds).strftime(timestamp_format),
            str(ff_proto.is_stream),
        )
        for ff_proto in freshness_statuses
    ]

    # Sort data by stale status
    sort_order = {"True": 0, "False": 1, "-": 2}
    freshness_data = sorted(freshness_data, key=lambda row: sort_order[row[2]])

    display_table(headers, freshness_data)
