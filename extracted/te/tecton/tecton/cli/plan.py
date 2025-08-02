from __future__ import annotations

import datetime
import json
import sys
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import click
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import tecton_core.tecton_pendulum as pendulum
from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton.cli.engine_renderer import PlanRenderingClient
from tecton_core.errors import TectonNotFoundError
from tecton_core.id_helper import IdHelper
from tecton_core.specs.utils import get_timestamp_field_or_none
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


def _format_date(datetime: Optional[pendulum.DateTime]):
    if datetime:
        if datetime.year == 1970:
            return ""
        return datetime.strftime("%Y-%m-%d %H:%M:%S %Z")


def _format_snake_case_property(property_name: str) -> str:
    if property_name in ("url", "id"):
        return property_name.upper()
    words = property_name.split("_")
    formatted_words = []
    for word in words:
        if word in ("id", "url", "sdk"):
            formatted_words.append(word.upper())
        else:
            formatted_words.append(word.capitalize())
    return " ".join(formatted_words)


@dataclass
class IntegrationTestSummaries:
    # This is a map of FeatureViewName to the list of integration test statuses for all integration tests
    #   run for that FeatureView as part of the Plan Integration Tests.
    statuses: Dict[str, List[state_update_pb2.IntegrationTestJobStatus]]

    def has_integration_tests(self):
        return bool(self.all_test_statuses())

    def all_test_statuses(self):
        all_test_statuses = []
        for _, status_list in self.statuses.items():
            all_test_statuses.extend(status_list)
        return all_test_statuses

    @staticmethod
    def _summarize_status(integration_status_list: List) -> str:
        """Given a list of integration test statuses, summarize the state of the entire bunch."""
        if not integration_status_list:
            return "No Tests"
        elif all(
            integration_status == state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_SUCCEED
            for integration_status in integration_status_list
        ):
            return "Succeeded"
        elif any(
            integration_status == state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_FAILED
            for integration_status in integration_status_list
        ):
            return "Failed"
        elif any(
            integration_status == state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_CANCELLED
            for integration_status in integration_status_list
        ):
            return "Canceled"
        elif any(
            integration_status == state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_RUNNING
            for integration_status in integration_status_list
        ):
            return "Running"
        elif any(
            integration_status == state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_NOT_STARTED
            for integration_status in integration_status_list
        ):
            return "Not Started"
        else:
            return "Unknown Status"

    def summarize_status_for_all_tests(self):
        return self._summarize_status(self.all_test_statuses())

    def summarize_status_by_fv(self):
        return {fv_name: self._summarize_status(status_list) for fv_name, status_list in self.statuses.items()}

    @classmethod
    def from_protobuf(cls, successful_plan_output: state_update_pb2.SuccessfulPlanOutput):
        statuses = {}
        for test_summary in successful_plan_output.test_summaries:
            test_job_statuses = [job_summary.status for job_summary in test_summary.job_summaries]
            statuses[test_summary.feature_view_name] = test_job_statuses
        return cls(statuses=statuses)


def _format_principal_for_output(
    principal_dict: Optional[Dict[str, str]], is_json_output: bool
) -> Union[Optional[Dict[str, str]], str]:
    """
    Format principal information for either JSON or table output.

    Args:
        principal_dict: The principal dictionary with principal, principal_type, and display_name
        is_json_output: True for JSON output (excludes display_name), False for table output (returns display_name)

    Returns:
        For JSON: Dictionary without display_name field, or None if no principal
        For table: Display name string, or empty string if no principal
    """
    if not principal_dict:
        return None if is_json_output else ""

    if is_json_output:
        return {k: v for k, v in principal_dict.items() if k != "display_name"}
    else:
        return principal_dict.get("display_name", "")


def _parse_principal_info(proto_obj, field_name: str, default_name: str = "") -> Optional[Dict[str, str]]:
    """
    Helper function to parse principal information from protobuf objects.

    Args:
        proto_obj: The protobuf object containing principal information
        field_name: The field name to extract principal information from (e.g. "created_by", "applied_by")
        default_name: Default name to use if no principal info is found

    Returns:
        Dict with "principal", "principal_type", and "display_name" keys, or None if no principal info
    """
    principal_info = None
    principal_field_name = f"{field_name}_principal"
    if proto_obj.HasField(principal_field_name):
        principal_proto = getattr(proto_obj, principal_field_name)
        principal_data = cli_utils.parse_principal_for_json(principal_proto, getattr(proto_obj, field_name))
        display_name = cli_utils.display_principal(principal_proto)
        principal_info = {
            "principal": principal_data["name"],
            "principal_type": principal_data["type"],
            "display_name": display_name,
        }
    elif getattr(proto_obj, field_name):
        fallback_name = getattr(proto_obj, field_name)
        principal_info = {"principal": fallback_name, "principal_type": "", "display_name": fallback_name}
    return principal_info


@dataclass
class PlanListItem:
    plan_id: str
    applied_by: Optional[Dict[str, str]]
    applied_at: Optional[pendulum.DateTime]
    created_by: Optional[Dict[str, str]]
    created_at: pendulum.DateTime
    workspace: str
    sdk_version: str
    integration_test_statuses: IntegrationTestSummaries
    success: bool

    @property
    def is_applied(self):
        return self.applied_by and self.applied_by.get("principal")

    @property
    def applied(self):
        if self.applied_by and self.applied_by.get("principal"):
            return "Applied"
        else:
            return "Created"

    @classmethod
    def from_proto(cls, state_update_entry: state_update_pb2.StateUpdateEntry):
        applied_by = _parse_principal_info(state_update_entry, "applied_by")
        created_by = _parse_principal_info(state_update_entry, "created_by")

        applied_at = get_timestamp_field_or_none(state_update_entry, "applied_at")
        created_at = get_timestamp_field_or_none(state_update_entry, "created_at")
        return cls(
            # commit_id is called plan_id in public facing UX. Re-aliasing here.
            plan_id=state_update_entry.commit_id,
            applied_by=applied_by,
            applied_at=applied_at,
            created_by=created_by,
            created_at=created_at,
            workspace=state_update_entry.workspace or "prod",
            sdk_version=state_update_entry.sdk_version,
            integration_test_statuses=IntegrationTestSummaries.from_protobuf(state_update_entry.successful_plan_output),
            success=state_update_entry.HasField("successful_plan_output"),
        )


@dataclass
class PlanSummary:
    applied_at: Optional[datetime.datetime]
    applied_by: Optional[Dict[str, str]]
    applied: bool
    created_at: datetime.datetime
    created_by: Optional[Dict[str, str]]
    workspace: str
    sdk_version: str
    plan_url: str
    integration_test_statuses: IntegrationTestSummaries
    original_proto: metadata_service_pb2.QueryStateUpdateResponseV2

    @classmethod
    def from_proto(cls, query_state_update_response: metadata_service_pb2.QueryStateUpdateResponseV2):
        applied_at = get_timestamp_field_or_none(query_state_update_response, "applied_at")
        applied_by = _parse_principal_info(query_state_update_response, "applied_by")
        created_by = _parse_principal_info(query_state_update_response, "created_by")

        applied = bool(applied_at)
        created_at = get_timestamp_field_or_none(query_state_update_response, "created_at")
        return cls(
            applied=applied,
            applied_at=applied_at,
            applied_by=applied_by,
            created_at=created_at,
            created_by=created_by,
            workspace=query_state_update_response.workspace or "prod",
            sdk_version=query_state_update_response.sdk_version,
            plan_url=query_state_update_response.successful_plan_output.plan_url,
            integration_test_statuses=IntegrationTestSummaries.from_protobuf(
                query_state_update_response.successful_plan_output
            ),
            original_proto=query_state_update_response,
        )


def get_plans_list_items(workspace: str, limit: int, applied_filter: Optional[str] = None):
    request = metadata_service_pb2.GetStateUpdatePlanListRequest(workspace=workspace, limit=limit)
    if applied_filter is not None:
        if applied_filter == "APPLIED":
            request.applied_filter = metadata_service_pb2.AppliedFilter.APPLIED_FILTER_APPLIED
        elif applied_filter == "UNAPPLIED":
            request.applied_filter = metadata_service_pb2.AppliedFilter.APPLIED_FILTER_UNAPPLIED
    response = metadata_service.instance().GetStateUpdatePlanList(request)
    return [PlanListItem.from_proto(entry) for entry in response.entries]


def get_plan(workspace: str, plan_id: str):
    try:
        plan_id = IdHelper.from_string(plan_id)
        request = metadata_service_pb2.QueryStateUpdateRequestV2(
            state_id=plan_id, workspace=workspace, no_color=False, json_output=True, suppress_warnings=False
        )
        response = metadata_service.instance().QueryStateUpdateV2(request)
    except ValueError:
        printer.safe_print(f'Invalid plan id "{plan_id}". Run `tecton plan-info list` to see list of available plans.')
        sys.exit(1)
    except TectonNotFoundError:
        printer.safe_print(
            f'Plan id "{plan_id}" not found in workspace {workspace}. Run `tecton plan-info list` to see list of '
            f"available plans."
        )
        sys.exit(1)
    return PlanSummary.from_proto(response.response_proto)


@click.group("plan-info", cls=TectonGroup, command_category=TectonCommandCategory.WORKSPACE)
def plan_info():
    r"""View info about plans."""


@plan_info.command(uses_workspace=True)
@click.option("--limit", default=10, type=int, help="Number of log entries to return.")
@click.option("--json-out", default=None, type=str, help="Write output in JSON format to a file.")
@click.option("--applied-filter", type=click.Choice(["APPLIED", "UNAPPLIED"]), help="Filter plans by applied status.")
def list(limit, json_out, applied_filter):
    """List previous plans created for this workspace."""
    workspace = tecton_context.get_current_workspace()
    entries = get_plans_list_items(workspace, limit, applied_filter=applied_filter)

    entries = [entry for entry in entries if entry.success]

    entries_data = []
    for entry in entries:
        created_by_value = _format_principal_for_output(entry.created_by, json_out is not None)
        applied_by_value = _format_principal_for_output(entry.applied_by, json_out is not None)

        entry_data = {
            "plan_id": entry.plan_id,
            "plan_status": entry.applied,
            "test_status": entry.integration_test_statuses.summarize_status_for_all_tests(),
            "created_by": created_by_value if created_by_value is not None else "",
            "creation_date": _format_date(entry.created_at),
            "applied_by": applied_by_value if entry.is_applied and applied_by_value is not None else "",
            "applied_date": _format_date(entry.applied_at) if entry.is_applied else "",
            "sdk_version": entry.sdk_version,
        }

        entries_data.append(entry_data)

    if json_out is not None:
        json_data = {"workspace": workspace, "plans": entries_data}
        cli_utils.write_json_to_file(json_data, json_out)
    else:
        # Use hardcoded field names to ensure consistent ordering and avoid potential issues
        field_names = [
            "plan_id",
            "plan_status",
            "test_status",
            "created_by",
            "creation_date",
            "applied_by",
            "applied_date",
            "sdk_version",
        ]

        headings = [_format_snake_case_property(field_name) for field_name in field_names]
        rows = []
        for entry_data in entries_data:
            row = tuple(entry_data.get(field_name, "") for field_name in field_names)
            rows.append(row)

        cli_utils.display_table(headings, rows)


@plan_info.command()
@click.argument("plan-id", required=True, metavar="PLAN_ID")
@click.option("--diff", default=False, is_flag=True, help="Include detailed plan diff.")
@click.option("--json-out", default=None, type=str, help="Write output in JSON format to a file.")
def show(plan_id, diff, json_out):
    """Show detailed info about a plan."""
    workspace = tecton_context.get_current_workspace()
    plan = get_plan(plan_id=plan_id, workspace=workspace)

    created_by_value = _format_principal_for_output(plan.created_by, json_out is not None)
    applied_by_value = _format_principal_for_output(plan.applied_by, json_out is not None)

    plan_info = {
        "id": plan_id,
        "created_by": created_by_value if created_by_value is not None else "",
        "started_at": _format_date(plan.created_at),
        "plan_applied": str(plan.applied),
    }

    if plan.applied:
        plan_info["applied_date"] = _format_date(plan.applied_at)
        plan_info["applied_by"] = applied_by_value if applied_by_value is not None else ""

    test_statuses = plan.integration_test_statuses
    plan_info["integration_test_status"] = test_statuses.summarize_status_for_all_tests()
    if test_statuses.has_integration_tests():
        plan_info["integration_tests"] = {}
        for fv, status in test_statuses.summarize_status_by_fv().items():
            plan_info["integration_tests"][fv] = status

    if plan.plan_url:
        plan_info["url"] = plan.plan_url
    else:
        plan_info["status"] = f"Plan {plan_id} failed due to errors."

    plan_rendering_client = PlanRenderingClient(plan.original_proto)

    if json_out is None:
        metadata_table = Table(show_header=False, box=None)
        metadata_table.add_column("Property", justify="left")
        metadata_table.add_column("Value", justify="left")

        for property_name, value in plan_info.items():
            metadata_table.add_row(_format_snake_case_property(property_name), str(value))

        printer.rich_print(Panel(metadata_table, title="Plan Summary", expand=False))

        if diff:
            rendered_plan = plan_rendering_client.render_plan_to_string()
            rendered_plan_text = Text.from_ansi(rendered_plan)

            printer.rich_print(Panel(rendered_plan_text, title="Plan Diff", expand=False))
    else:
        if diff:
            json_blob = json.loads(plan_rendering_client.get_json_plan_output())
            plan_info["plan"] = json_blob
        cli_utils.write_json_to_file(plan_info, json_out)
