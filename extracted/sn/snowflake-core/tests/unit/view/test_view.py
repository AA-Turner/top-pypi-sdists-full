from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.tag import TagValue
from snowflake.core.view import View, ViewColumn, ViewResource
from snowflake.core.view._generated import TagAssignment, TagReference

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
VIEW = View(name="my_view", columns=[ViewColumn(name="col1")], query="select col1 from my_tab")


@pytest.fixture
def views(schema):
    return schema.views


@pytest.fixture
def view(views):
    return views["my_view"]


def test_create_view(fake_root, views):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/views",
    )
    kwargs = extra_params(
        query_params=[],
        body={"name": "my_view", "columns": [{"name": "col1"}], "query": "select col1 from my_tab"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        view_res = views.create(VIEW)
        assert isinstance(view_res, ViewResource)
        assert view_res.name == "my_view"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = views.create_async(VIEW)
        assert isinstance(op, PollingOperation)
        view_res = op.result()
        assert view_res.name == "my_view"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_view(fake_root, views):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/views")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        views.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = views.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_view(fake_root, view):
    from snowflake.core.view._generated.models import View as ViewModel
    from snowflake.core.view._generated.models import ViewColumn as ViewColumnModel

    model = ViewModel(name="my_view", columns=[ViewColumnModel(name="col1")], query="select col1 from my_tab")
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/views/my_view")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        view.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = view.fetch_async()
        assert isinstance(op, PollingOperation)
        view = op.result()
        assert view.to_dict() == VIEW.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_view(fake_root, view):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/views/my_view")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        view.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = view.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, view, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/views/my_view:set-tags")
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
        view.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = view.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, view, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/views/my_view:unset-tags")
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
        view.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = view.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, view):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/views/my_view:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert view.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = view.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
