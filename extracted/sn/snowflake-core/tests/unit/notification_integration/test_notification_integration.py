from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.notification_integration import (
    NotificationEmail,
    NotificationIntegration,
    NotificationIntegrationCollection,
)

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.notification_integration._generated.api_client.ApiClient.request"
NOTIFICATION_INTEGRATION = NotificationIntegration(name="my_int", notification_hook=NotificationEmail())

@pytest.fixture
def notification_integrations(fake_root):
    return NotificationIntegrationCollection(fake_root)


@pytest.fixture
def notification_integration(notification_integrations):
    return notification_integrations["my_int"]


def test_create_notification_integration(fake_root, notification_integrations):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/notification-integrations?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_int",
            "notification_hook": {"type": "EMAIL"},
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notification_integrations.create(NOTIFICATION_INTEGRATION)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notification_integrations.create_async(NOTIFICATION_INTEGRATION)
        assert isinstance(op, PollingOperation)
        ni_res = op.result()
        assert ni_res.name == "my_int"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_notification_integration(fake_root, notification_integrations):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/notification-integrations",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        notification_integrations.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = notification_integrations.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_notification_integration(fake_root, notification_integration):
    from snowflake.core.notification_integration._generated.models import NotificationEmail as NotificationEmailModel
    from snowflake.core.notification_integration._generated.models import (
        NotificationIntegration as NotificationIntegrationModel,
    )

    model = NotificationIntegrationModel(name="my_int", notification_hook=NotificationEmailModel())
    args = (
        fake_root,
        "GET",
        BASE_URL + "/notification-integrations/my_int",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        notification_integration.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = notification_integration.fetch_async()
        assert isinstance(op, PollingOperation)
        ni = op.result()
        assert ni.to_dict() == NOTIFICATION_INTEGRATION.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)



def test_drop_notification_integration(fake_root, notification_integration):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/notification-integrations/my_int",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notification_integration.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notification_integration.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
