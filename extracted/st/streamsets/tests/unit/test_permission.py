# Copyright 2024 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.sch_models import Permission

# fmt: on


class MockControlHub:
    def __init__(self):
        self.api_client = MockApiClient()


class MockApiClient:
    def update_job_permissions(self, *args, **kwargs):
        return True

    def update_pipeline_permissions(self, *args, **kwargs):
        return True

    def update_sdc_permissions(self, *args, **kwargs):
        return True

    def update_report_definition_permissions(self, *args, **kwargs):
        return True

    def update_connection_permissions(self, *args, **kwargs):
        return True

    def update_topology_permissions(self, *args, **kwargs):
        return True

    def update_subscription_permissions(self, *args, **kwargs):
        return True

    def update_legacy_deployment_permissions(self, *args, **kwargs):
        return True

    def update_deployment_permissions(self, *args, **kwargs):
        return True

    def update_environment_permissions(self, *args, **kwargs):
        return True

    def update_scheduled_task_permissions(self, *args, **kwargs):
        return True

    def update_alert_permissions(self, *args, **kwargs):
        return True


@pytest.fixture(scope="function")
def dummy_permission():
    return Permission(
        {
            'resourceId': '1fd7acec-817f-4ee4-b0cc-7046a06744e7:35be715e-e8e9-11ec-8e84-93331d4150d4',
            'subjectId': '2cfced39-e8e9-11ec-8e84-d7b86be914f5@35be715e-e8e9-11ec-8e84-93331d4150d4',
            'subjectType': 'USER',
            'lastModifiedBy': '2cfced39-e8e9-11ec-8e84-d7b86be914f5@35be715e-e8e9-11ec-8e84-93331d4150d4',
            'lastModifiedOn': 1721317112806,
            'actions': ['READ', 'WRITE'],
        },
        resource_type="CSP_DEPLOYMENT",
        api_client=MockApiClient(),
    )


def test_update_permission_action(dummy_permission):
    valid_permission_actions = [["READ"], ["READ", "WRITE"], ["WRITE", "READ"], ["EXECUTE", "READ"]]
    for action in valid_permission_actions:
        dummy_permission.actions = action
        assert dummy_permission.actions == action


def test_update_permission_action_fails(dummy_permission):
    invalid_permission_actions = [["EAD"], ["WRITE"], ["WRITE", "EXECUTE"], ["EXECUTE", "RAD"]]
    for action in invalid_permission_actions:
        with pytest.raises(ValueError):
            dummy_permission.actions = action
