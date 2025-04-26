from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.alert import Alert, MinutesSchedule

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.alert._generated.api_client.ApiClient.request"
ALERT = Alert(name="my_alert", schedule=MinutesSchedule(minutes=60), condition="", action="select 1")


@pytest.fixture()
def alerts(schema):
    return schema.alerts


@pytest.fixture()
def alert(alerts):
    return alerts["my_alert"]


def test_create_async(fake_root, alerts):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/alerts?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_alert",
            "schedule": {"minutes": 60, "schedule_type": "SCHEDULE_TYPE"},
            "condition": "",
            "action": "select 1",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        alert_res = alerts.create(ALERT)
        assert alert_res.name == "my_alert"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = alerts.create_async(ALERT)
        assert isinstance(op, PollingOperation)
        alert_res = op.result()
        assert alert_res.name == "my_alert"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_async_clone(fake_root, alerts):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/alerts/clone_alert:clone?" + \
        "createMode=errorIfExists&targetDatabase=my_db&targetSchema=my_schema",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("targetDatabase", "my_db"), ("targetSchema", "my_schema")],
        body={"name": "my_alert"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        alert_res = alerts.create("my_alert", clone_alert="clone_alert")
        assert alert_res.name == "my_alert"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = alerts.create_async("my_alert", clone_alert="clone_alert")
        assert isinstance(op, PollingOperation)
        alert_res = op.result()
        assert alert_res.name == "my_alert"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_async(fake_root, alerts):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/alerts",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = alerts.iter()
        assert list(it) == []

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = alerts.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_async(fake_root, alert):
    from snowflake.core.alert._generated.models import Alert as AlertModel
    from snowflake.core.alert._generated.models import MinutesSchedule as MinutesScheduleModel

    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/alerts/my_alert",
    )
    kwargs = extra_params()
    model = AlertModel(name="my_alert", schedule=MinutesScheduleModel(minutes=60), condition="", action="select 1")

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        my_alert = alert.fetch()
        assert my_alert.to_dict() == ALERT.to_dict()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = alert.fetch_async()
        assert isinstance(op, PollingOperation)
        my_alert = op.result()
        assert my_alert.to_dict() == ALERT.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_async(fake_root, alert):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/alerts/my_alert?ifExists=False",
    )
    kwargs = extra_params(query_params=[("ifExists", False)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        alert.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = alert.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_async(fake_root, alert):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/alerts/my_alert:execute",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        alert.execute()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = alert.execute_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
