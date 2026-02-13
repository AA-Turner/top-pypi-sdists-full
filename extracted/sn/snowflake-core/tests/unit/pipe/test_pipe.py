from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.pipe import Pipe, PipeResource
from snowflake.core.pipe._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
PIPE = Pipe(name="my_pipe", copy_statement="copy into my_tab")


@pytest.fixture
def pipes(schema):
    return schema.pipes


@pytest.fixture
def pipe(pipes):
    return pipes["my_pipe"]


def test_create_pipe(fake_root, pipes):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/pipes")
    kwargs = extra_params(query_params=[], body={"name": "my_pipe", "copy_statement": "copy into my_tab"})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        pipe_res = pipes.create(PIPE)
        assert isinstance(pipe_res, PipeResource)
        assert pipe_res.name == "my_pipe"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = pipes.create_async(PIPE)
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_pipe"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_pipe(fake_root, pipes):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/pipes")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        pipes.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = pipes.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_pipe(fake_root, pipe):
    from snowflake.core.pipe._generated.models import Pipe as PipeModel

    model = PipeModel(name="my_pipe", copy_statement="copy into my_tab")
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/pipes/my_pipe")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        pipe.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = pipe.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == PIPE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_pipe(fake_root, pipe):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/pipes/my_pipe")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        pipe.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = pipe.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_refresh_pipe(fake_root, pipe):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/pipes/my_pipe:refresh")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        pipe.refresh()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = pipe.refresh_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, pipe, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/pipes/my_pipe:set-tags")
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
        pipe.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = pipe.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, pipe, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/pipes/my_pipe:unset-tags")
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
        pipe.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = pipe.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, pipe):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/pipes/my_pipe:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert pipe.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = pipe.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
