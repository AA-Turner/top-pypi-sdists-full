from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.cortex.chat_service import ChatRequest, CortexChatService

from ...utils import BASE_URL, extra_params


API_CLIENT_REQUEST = "snowflake.core.cortex.chat_service._generated.api_client.ApiClient.request"


@pytest.fixture
def chat_service(fake_root):
    return CortexChatService(fake_root)


def test_chat(fake_root, chat_service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/cortex/chat",
    )
    kwargs = extra_params(
        body={"query": ""},
        _preload_content=False,
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = chat_service.chat_async(ChatRequest(query=""))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
