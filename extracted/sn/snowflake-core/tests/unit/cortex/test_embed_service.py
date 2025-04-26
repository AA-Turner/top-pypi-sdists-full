from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.cortex.embed_service import CortexEmbedService

from ...utils import BASE_URL, extra_params


API_CLIENT_REQUEST = "snowflake.core.cortex.embed_service._generated.api_client.ApiClient.request"


@pytest.fixture
def embed_service(fake_root):
    return CortexEmbedService(fake_root)


def test_embed(fake_root, embed_service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/cortex/inference:embed",
    )
    kwargs = extra_params(
        body={
            "model": "my_model",
            "text": ["xyz"],
        }
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = embed_service.embed_async("my_model", ["xyz"])
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
