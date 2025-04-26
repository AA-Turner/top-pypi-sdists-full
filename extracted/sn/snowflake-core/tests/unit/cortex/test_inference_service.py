from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.cortex.inference_service import (
    CompleteRequest,
    CompleteRequestMessagesInner,
    CortexInferenceService,
)

from ...utils import BASE_URL, extra_params


API_CLIENT_REQUEST = "snowflake.core.cortex.inference_service._generated.api_client.ApiClient.request"


@pytest.fixture
def inference_service(fake_root):
    return CortexInferenceService(fake_root)


def test_complete(fake_root, inference_service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/cortex/inference:complete",
    )
    kwargs = extra_params(
        body={
            "model": "my_model",
            "messages": [{"role": "user", "content": "xyz"}],
            "top_p": 1.0,
            "max_tokens": 4096,
            "stream": True,
            "temperature": None,
            "max_output_tokens": None,
            "response_format": None,
            "guardrails": None,
            "tool_choice": None,
            "provisioned_throughput_id": None,
        },
        _preload_content=False,
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = inference_service.complete_async(
            CompleteRequest(model="my_model", messages=[CompleteRequestMessagesInner(content="xyz")]))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
