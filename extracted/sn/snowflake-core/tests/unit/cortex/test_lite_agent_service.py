from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.cortex.lite_agent_service import AgentRunRequest, CortexAgentService

from ...utils import BASE_URL, extra_params


API_CLIENT_REQUEST = "snowflake.core.cortex.lite_agent_service._generated.api_client.ApiClient.request"


@pytest.fixture
def agent_service(fake_root):
    return CortexAgentService(fake_root)


def test_run(fake_root, agent_service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/cortex/agent:run",
    )
    kwargs = extra_params(
        body={
            "model": "my_model",
            "messages": [{"role": "", "content": []}],
            "tool_choice": None,
        },
        _preload_content=False,
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = agent_service.run_async(AgentRunRequest(model="my_model", messages=[{"role": "", "content": []}]))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
