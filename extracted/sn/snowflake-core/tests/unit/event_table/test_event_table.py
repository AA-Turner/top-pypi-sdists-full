from unittest import mock

import pytest

from snowflake.core import PollingOperation, Root
from snowflake.core.event_table import EventTable, EventTableResource
from snowflake.core.event_table._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


@pytest.fixture
def event_tables(schema):
    return schema.event_tables


@pytest.fixture
def event_table(event_tables):
    return event_tables["my_table"]


def test_create_event_table(fake_root, event_tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/event-tables?createMode=errorIfExists&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)], body={"name": "my_table"}
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        et_res = event_tables.create(EventTable(name="my_table"))
        assert isinstance(et_res, EventTableResource)
        assert et_res.name == "my_table"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = event_tables.create_async(EventTable(name="my_table"))
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_table"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_event_table(fake_root, event_tables):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/event-tables")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        event_tables.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = event_tables.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_event_table(fake_root, event_table):
    from snowflake.core.event_table._generated.models import EventTable as EventTableModel

    model = EventTableModel(name="my_table")
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/event-tables/my_table")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        event_table.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = event_table.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == EventTable(name="my_table").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_event_table(fake_root, event_table):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/event-tables/my_table")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        event_table.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = event_table.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_event_table(fake_root, event_table, event_tables):
    def format_args(table_name: str) -> tuple[Root, str, str]:
        return (
            fake_root,
            "POST",
            BASE_URL + f"/databases/my_db/schemas/my_schema/event-tables/{table_name}:rename?targetName=new_table",
        )

    kwargs = extra_params(query_params=[("targetName", "new_table")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        event_table.rename("new_table")
        assert event_table.name == "new_table"
    mocked_request.assert_called_once_with(*format_args("my_table"), **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        et_res = event_tables["another_table"]
        op = et_res.rename_async("new_table")
        assert isinstance(op, PollingOperation)
        op.result()
        assert et_res.name == "new_table"
    mocked_request.assert_called_once_with(*format_args("another_table"), **kwargs)


def test_set_tags(fake_root, event_table, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/event-tables/my_table:set-tags")
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
        event_table.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = event_table.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, event_table, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/event-tables/my_table:unset-tags")
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
        event_table.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = event_table.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, event_table):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/event-tables/my_table:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert event_table.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = event_table.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
