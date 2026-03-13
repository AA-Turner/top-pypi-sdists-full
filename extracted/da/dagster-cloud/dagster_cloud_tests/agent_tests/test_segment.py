from unittest import mock

from dagster_cloud.api.dagster_cloud_api import (
    DagsterCloudUploadLocationData,
    DagsterCloudUploadWorkspaceEntry,
)
from dagster_cloud.instance import DagsterCloudAgentInstance
from dagster_cloud_backend.analytics.events import AnalyticsEvent
from dagster_cloud_cli.core.workspace import CodeLocationDeployData


def test_add_location_adds_segment_event(
    agent_instance_local_ursula: DagsterCloudAgentInstance,
    host_instance,
    segment_analytics,  # (fixture)
) -> None:
    # Verify that the agent reconciling and uploading a new location triggers Segment

    agent_instance = agent_instance_local_ursula

    user_code_launcher = agent_instance.user_code_launcher

    code_location_deploy_data = CodeLocationDeployData(
        python_file=__file__, image="dagster/test_image:bar"
    )

    host_instance.cloud_storage.add_location(
        "foo", code_location_deploy_data=code_location_deploy_data
    )

    user_code_launcher._update_workspace_entry(  # noqa: SLF001
        "sandbox",
        DagsterCloudUploadWorkspaceEntry(
            location_name="foo",
            code_location_deploy_data=code_location_deploy_data,
            upload_location_data=DagsterCloudUploadLocationData(
                upload_repository_datas=[],
                container_image=None,
                executable_path=None,
            ),
            serialized_error_info=None,
        ),
        server_or_error=mock.MagicMock(),
    )

    assert len(segment_analytics.track_calls) == 1
    assert segment_analytics.track_calls[0]["user_id"] != "agent"
    assert segment_analytics.track_calls[0]["event"] == AnalyticsEvent.CODE_LOCATION_ADD
    assert (
        segment_analytics.track_calls[0]["properties"]["groupId"] == host_instance.organization_id
    )
