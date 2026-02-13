from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.stream import Stream, StreamResource, StreamSourceTable
from snowflake.core.stream._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
STREAM = Stream(name="my_stream", stream_source=StreamSourceTable(name="my_tab"))


@pytest.fixture
def streams(schema):
    return schema.streams


@pytest.fixture
def stream(streams):
    return streams["my_stream"]


def test_create_stream(fake_root, streams):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streams?createMode=errorIfExists&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)],
        body={"name": "my_stream", "stream_source": {"name": "my_tab", "src_type": "table"}},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        stream_res = streams.create(STREAM)
        assert isinstance(stream_res, StreamResource)
        assert stream_res.name == "my_stream"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streams.create_async(STREAM)
        assert isinstance(op, PollingOperation)
        stream_res = op.result()
        assert stream_res.name == "my_stream"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_stream_clone(fake_root, streams):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/streams/clone_stream:clone?"
        + "createMode=errorIfExists&targetDatabase=my_db&targetSchema=my_schema&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[
            ("createMode", "errorIfExists"),
            ("targetDatabase", streams.database.name),
            ("targetSchema", streams.schema.name),
            ("copyGrants", False),
        ],
        body={"name": "my_stream"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streams.create("my_stream", clone_stream="clone_stream")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streams.create_async("my_stream", clone_stream="clone_stream")
        assert isinstance(op, PollingOperation)
        stream_res = op.result()
        assert stream_res.name == "my_stream"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_stream(fake_root, streams):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/streams")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        streams.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = streams.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, streams):
    """Test that show_limit parameter triggers deprecation warning."""
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/streams?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(streams.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            streams.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit(fake_root, streams):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/streams?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        list(streams.iter(limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        streams.iter_async(limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(streams):
    """Test that providing both limit and show_limit raises ValueError."""
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(streams.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        streams.iter_async(limit=10, show_limit=5).result()


def test_fetch_stream(fake_root, stream):
    from snowflake.core.stream._generated.models import Stream as StreamModel
    from snowflake.core.stream._generated.models import StreamSourceTable as StreamSourceTableModel

    model = StreamModel(name="my_stream", stream_source=StreamSourceTableModel(name="my_tab"))
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/streams/my_stream")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        stream.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = stream.fetch_async()
        assert isinstance(op, PollingOperation)
        stream = op.result()
        assert stream.to_dict() == STREAM.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_stream(fake_root, stream):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/streams/my_stream")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        stream.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = stream.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, stream, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/streams/my_stream:set-tags")
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
        stream.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = stream.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, stream, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/streams/my_stream:unset-tags")
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
        stream.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = stream.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, stream):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/streams/my_stream:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert stream.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = stream.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
