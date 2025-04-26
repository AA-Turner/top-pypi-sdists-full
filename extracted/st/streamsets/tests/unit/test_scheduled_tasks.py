#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk import ControlHub
from streamsets.sdk.sch_models import ScheduledTask

from .resources.scheduled_tasks_data import (
    DUMMY_CREATE_SCHEDULED_TASK_FAILURE_RESPONSE_JSON, DUMMY_INVALID_SCHEDULED_TASK_JSON,
)

# fmt: on


class MockControlHub(ControlHub):
    def __init__(self, *args, **kwargs):
        self.api_client = MockApiClient()
        pass


class MockApiClient:
    def __init__(self, *args, **kwargs):
        pass

    def create_scheduled_task(self, data, api_version=2):
        # return a JSON response for publishing a scheduled task, either for a valid task or an invalid task
        if 'INVALID' in data['data']['messages']:
            return MockCommand(dummy_create_scheduled_task_failure_response())


class MockCommand:
    def __init__(self, json_response):
        self._response = json_response

    @property
    def response(self):
        return MockResponse(self._response)


class MockResponse:
    def __init__(self, json_response):
        self.response = json_response

    def json(self):
        return self.response


def dummy_create_scheduled_task_failure_response():
    data = deepcopy(DUMMY_CREATE_SCHEDULED_TASK_FAILURE_RESPONSE_JSON)
    return data


@pytest.fixture(scope="function")
def dummy_invalid_scheduled_task_json():
    data = deepcopy(DUMMY_INVALID_SCHEDULED_TASK_JSON)
    return data


def test_add_scheduled_task_error_handling(dummy_invalid_scheduled_task_json):
    sch = MockControlHub()
    task = ScheduledTask(dummy_invalid_scheduled_task_json, control_hub=sch)
    with pytest.raises(Exception) as error_info:
        sch.add_scheduled_task(task)
        assert 'caused by' in str(error_info)
