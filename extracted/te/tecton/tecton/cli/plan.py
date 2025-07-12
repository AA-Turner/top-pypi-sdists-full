from __future__ import annotations

import datetime
import sys
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

import click
from rich.panel import Panel

import tecton_core.tecton_pendulum as pendulum
from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton_core.errors import TectonNotFoundError
from tecton_core.id_helper import IdHelper
from tecton_core.specs.utils import get_timestamp_field_or_none
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


def _format_date(datetime: Optional[pendulum.DateTime]):
    if datetime:
        return datetime.strftime("%Y-%m-%d %H:%M:%S %Z")


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


@dataclass
class PlanListItem:
    plan_id: str
    applied_by: Optional[str]
    applied_at: Optional[pendulum.DateTime]
    created_by: str
    created_at: pendulum.DateTime
    workspace: str
    sdk_version: str
    integration_test_statuses: IntegrationTestSummaries

    @property
    def applied(self):
        if bool(self.applied_by):
            return "Applied"
        else:
            return "Created"

    @classmethod
    def from_proto(cls, state_update_entry: state_update_pb2.StateUpdateEntry):
        applied_by = cli_utils.display_principal(state_update_entry.applied_by_principal, state_update_entry.applied_by)
        applied_at = get_timestamp_field_or_none(state_update_entry, "applied_at")
        created_at = get_timestamp_field_or_none(state_update_entry, "created_at")
        return cls(
            # commit_id is called plan_id in public facing UX. Re-aliasing here.
            plan_id=state_update_entry.commit_id,
            applied_by=applied_by,
            applied_at=applied_at,
            created_by=state_update_entry.created_by,
            created_at=created_at,
            workspace=state_update_entry.workspace or "prod",
            sdk_version=state_update_entry.sdk_version,
            integration_test_statuses=IntegrationTestSummaries.from_protobuf(state_update_entry.successful_plan_output),
        )


@dataclass
class PlanSummary:
    applied_at: Optional[datetime.datetime]
    applied_by: Optional[str]
    applied: bool
    created_at: datetime.datetime
    created_by: str
    workspace: str
    sdk_version: str
    plan_url: str
    integration_test_statuses: IntegrationTestSummaries

    @classmethod
    def from_proto(cls, query_state_update_response: metadata_service_pb2.QueryStateUpdateResponseV2):
        applied_at = get_timestamp_field_or_none(query_state_update_response, "applied_at")
        applied_by = cli_utils.display_principal(
            query_state_update_response.applied_by_principal, query_state_update_response.applied_by
        )
        applied = bool(applied_at)
        created_at = get_timestamp_field_or_none(query_state_update_response, "created_at")
        return cls(
            applied=applied,
            applied_at=applied_at,
            applied_by=applied_by,
            created_at=created_at,
            created_by=query_state_update_response.created_by,
            workspace=query_state_update_response.workspace or "prod",
            sdk_version=query_state_update_response.sdk_version,
            plan_url=query_state_update_response.successful_plan_output.plan_url,
            integration_test_statuses=IntegrationTestSummaries.from_protobuf(
                query_state_update_response.successful_plan_output
            ),
        )


def get_plans_list_items(workspace: str, limit: int):
    request = metadata_service_pb2.GetStateUpdatePlanListRequest(workspace=workspace, limit=limit)
    response = metadata_service.instance().GetStateUpdatePlanList(request)
    return [PlanListItem.from_proto(entry) for entry in response.entries if entry.HasField("successful_plan_output")]


def get_plan(workspace: str, plan_id: str):
    try:
        plan_id = IdHelper.from_string(plan_id)
        request = metadata_service_pb2.QueryStateUpdateRequestV2(
            state_id=plan_id, workspace=workspace, no_color=True, json_output=False, suppress_warnings=False
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
def list(limit):
    """List previous plans created for this workspace."""
    workspace = tecton_context.get_current_workspace()
    entries = get_plans_list_items(workspace, limit)

    headings = ["Plan ID", "Plan Status", "Test Status", "Created by", "Creation Date", "SDK Version"]

    rows = []
    for entry in entries:
        rows.append(
            (
                entry.plan_id,
                entry.applied,
                entry.integration_test_statuses.summarize_status_for_all_tests(),
                entry.created_by,
                _format_date(entry.created_at),
                entry.sdk_version,
            )
        )

    cli_utils.display_table(headings, rows)


@plan_info.command()
@click.argument("plan-id", required=True, metavar="PLAN_ID")
def show(plan_id):
    """Show detailed info about a plan."""
    workspace = tecton_context.get_current_workspace()
    plan = get_plan(plan_id=plan_id, workspace=workspace)

    content = f"""Plan Started At: {_format_date(plan.created_at)}
Plan Created By: {plan.created_by}
Plan Applied: {plan.applied}"""
    if plan.applied:
        content += f"""
Applied At: {_format_date(plan.applied_at)}
Applied By: {plan.applied_by}"""

    test_statuses = plan.integration_test_statuses
    content += f"""
Integration Test Status: {test_statuses.summarize_status_for_all_tests()}"""
    if test_statuses.has_integration_tests():
        content += "\nStatus by Feature View:"
        for fv, status in test_statuses.summarize_status_by_fv().items():
            content += f"\n  {fv}: {status}"

    if plan.plan_url:
        content += f"\n\nView your plan in the Web UI: {plan.plan_url}"
    else:
        content += f"\n\nPlan {plan_id} failed due to errors. Please review and fix the issues."

    printer.get_console().print(Panel(content, title=f"Showing current status for Plan {plan_id}", expand=False))
