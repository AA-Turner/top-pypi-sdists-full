from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.notification_integration import (
    NotificationEmail,
    NotificationIntegration,
    NotificationIntegrationCollection,
    NotificationIntegrationResource,
)
from snowflake.core.notification_integration._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
NOTIFICATION_INTEGRATION = NotificationIntegration(name="my_int", notification_hook=NotificationEmail())


@pytest.fixture
def notification_integrations(fake_root):
    return NotificationIntegrationCollection(fake_root)


@pytest.fixture
def notification_integration(notification_integrations):
    return notification_integrations["my_int"]


def test_create_notification_integration(fake_root, notification_integrations):
    args = (fake_root, "POST", BASE_URL + "/notification-integrations")
    kwargs = extra_params(query_params=[], body={"name": "my_int", "notification_hook": {"type": "EMAIL"}})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        ni_res = notification_integrations.create(NOTIFICATION_INTEGRATION)
        assert isinstance(ni_res, NotificationIntegrationResource)
        assert ni_res.name == "my_int"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notification_integrations.create_async(NOTIFICATION_INTEGRATION)
        assert isinstance(op, PollingOperation)
        ni_res = op.result()
        assert ni_res.name == "my_int"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_notification_integration(fake_root, notification_integrations):
    args = (fake_root, "GET", BASE_URL + "/notification-integrations")
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
    args = (fake_root, "GET", BASE_URL + "/notification-integrations/my_int")
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
    args = (fake_root, "DELETE", BASE_URL + "/notification-integrations/my_int")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notification_integration.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notification_integration.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, notification_integration, tag):
    args = (fake_root, "POST", BASE_URL + "/notification-integrations/my_int:set-tags")
    tags = {tag: TagValue(value="value")}
    kwargs = extra_params(
        body=[
            TagAssignment(
                tag_value=v.value, tag_name=k.name, tag_schema=k.schema.name, tag_database=k.database.name
            ).to_dict()
            for k, v in tags.items()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notification_integration.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notification_integration.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, notification_integration, tag):
    args = (fake_root, "POST", BASE_URL + "/notification-integrations/my_int:unset-tags")
    tag_resources = {tag}
    kwargs = extra_params(
        body=[
            TagReference(
                tag_name=tag_res.name, tag_schema=tag_res.schema.name, tag_database=tag_res.database.name
            ).to_dict()
            for tag_res in tag_resources
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        notification_integration.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = notification_integration.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, notification_integration):
    args = (fake_root, "GET", BASE_URL + "/notification-integrations/my_int:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert notification_integration.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = notification_integration.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
