from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.tag import Tag, TagResource

from ...utils import BASE_URL, extra_params, mock_http_response


@pytest.fixture
def tags(schema):
    return schema.tags


@pytest.fixture
def tag(tags):
    return tags["my_tag"]


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
TAG = Tag(
    name="my_tag",
    allowed_values=["value1", "value2", "value3"],
    comment="Test tag",
    propagate="ON_DEPENDENCY",
    on_conflict="ALLOWED_VALUES_SEQUENCE",
)


def test_create_tag(fake_root, tags):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/tags")
    kwargs = extra_params(
        query_params=[],
        body={
            "allowed_values": ["value1", "value2", "value3"],
            "comment": "Test tag",
            "name": "my_tag",
            "propagate": "ON_DEPENDENCY",
            "on_conflict": "ALLOWED_VALUES_SEQUENCE",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag_res = tags.create(TAG)
        assert isinstance(tag_res, TagResource)
        assert tag_res.name == "my_tag"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tags.create_async(TAG)
        assert isinstance(op, PollingOperation)
        tag_res = op.result()
        assert tag_res.name == "my_tag"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_tag(fake_root, tags):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        tags.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = tags.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_tag(fake_root, tag):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/tags/my_tag")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(TAG.to_json())
        tag.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(TAG.to_json())
        op = tag.fetch_async()
        assert isinstance(op, PollingOperation)
        fetched_tag = op.result()
        assert fetched_tag.to_dict() == TAG.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_tag(fake_root, tag):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/tags/my_tag")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tag.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_tag(fake_root, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/tags/my_tag:undrop")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tag.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_tag(fake_root, tag):
    args = (fake_root, "PUT", BASE_URL + "/databases/my_db/schemas/my_schema/tags/my_tag")
    kwargs = extra_params(
        query_params=[],
        body={
            "allowed_values": ["value1", "value2", "value3"],
            "comment": "Test tag",
            "name": "my_tag",
            "propagate": "ON_DEPENDENCY",
            "on_conflict": "ALLOWED_VALUES_SEQUENCE",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag.create_or_alter(TAG)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tag.create_or_alter_async(TAG)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_tag(fake_root, tag, tags):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tags/my_tag:rename?targetName=new_tag",
    )
    kwargs = extra_params(query_params=[("targetName", "new_tag")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag.rename("new_tag")
        assert tag.name == "new_tag"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag_res = tags["another_tag"]
        op = tag_res.rename_async("new_tag")
        assert isinstance(op, PollingOperation)
        op.result()
        assert tag_res.name == "new_tag"
    args2 = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tags/another_tag:rename?targetName=new_tag",
    )
    mocked_request.assert_called_once_with(*args2, **kwargs)


def test_rename_tag_with_options(fake_root, tag):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/tags/my_tag:rename?ifExists=True&targetDatabase=other_db&targetSchema=other_schema&targetName=new_tag",
    )
    kwargs = extra_params(
        query_params=[
            ("ifExists", True),
            ("targetDatabase", "other_db"),
            ("targetSchema", "other_schema"),
            ("targetName", "new_tag"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tag.rename("new_tag", target_database="other_db", target_schema="other_schema", if_exists=True)
        assert tag.name == "new_tag"
    mocked_request.assert_called_once_with(*args, **kwargs)
