from unittest import mock

import pytest

from snowflake.core import PollingOperation, Root
from snowflake.core.streamlit import (
    AddVersionFromGitStreamlitRequest,
    AddVersionStreamlitRequest,
    Streamlit,
    StreamlitPushOptions,
    StreamlitResource,
    StreamlitVersionForGit,
)
from snowflake.core.streamlit._generated.models import Streamlit as StreamlitModel

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
STREAMLIT = Streamlit(name="my_streamlit", main_file="app.py", query_warehouse="wh", source_location="@stage/app")


@pytest.fixture
def streamlits(schema):
    return schema.streamlits


@pytest.fixture
def streamlit(streamlits):
    return streamlits["my_streamlit"]


def test_create_streamlit(fake_root, streamlits):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits",
    )
    kwargs = extra_params(body=STREAMLIT.to_dict())

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        res = streamlits.create(STREAMLIT)
        assert isinstance(res, StreamlitResource)
        assert res.name == "my_streamlit"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlits.create_async(STREAMLIT)
        assert isinstance(op, PollingOperation)
        res = op.result()
        assert res.name == "my_streamlit"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_streamlit(fake_root, streamlits):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/streamlits")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        streamlits.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = streamlits.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_streamlit_with_parameters(fake_root, streamlits):
    args = (
        fake_root,
        "GET",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/streamlits?like=test%&startsWith=test&showLimit=100&fromName=start_name",
    )
    kwargs = extra_params(
        query_params=[
            ("like", "test%"),
            ("startsWith", "test"),
            ("showLimit", 100),
            ("fromName", "start_name"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        streamlits.iter(like="test%", starts_with="test", limit=100, from_name="start_name")
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, streamlits):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/streamlits?showLimit=10")
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(streamlits.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            streamlits.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(streamlits):
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(streamlits.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        streamlits.iter_async(limit=10, show_limit=5).result()


def test_fetch_streamlit(fake_root, streamlit):
    model = StreamlitModel(
        name="my_streamlit",
        main_file="app.py",
        query_warehouse="wh",
        source_location="@stage/app",
    )
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        streamlit.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = streamlit.fetch_async()
        assert isinstance(op, PollingOperation)
        obj = op.result()
        assert obj.to_dict() == STREAMLIT.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit",
    )
    kwargs = extra_params(query_params=[])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_streamlit_with_if_exists(fake_root, streamlit):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit?ifExists=True",
    )
    kwargs = extra_params(query_params=[("ifExists", True)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.drop(if_exists=True)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.drop_async(if_exists=True)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_streamlit(fake_root, streamlit, streamlits):
    def format_args(streamlit_name: str) -> tuple[Root, str, str]:
        return (
            fake_root,
            "POST",
            BASE_URL
            + f"/databases/my_db/schemas/my_schema/streamlits/{streamlit_name}:rename?"
            + "targetName=new_streamlit",
        )

    kwargs = extra_params(
        query_params=[
            ("targetName", "new_streamlit"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.rename("new_streamlit")
        assert streamlit.name == "new_streamlit"
    mocked_request.assert_called_once_with(*format_args("my_streamlit"), **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        other = streamlits["another_streamlit"]
        op = other.rename_async("new_streamlit")
        assert isinstance(op, PollingOperation)
        op.result()
        assert other.name == "new_streamlit"
    mocked_request.assert_called_once_with(*format_args("another_streamlit"), **kwargs)

    assert streamlits["my_streamlit"].name == "my_streamlit"
    assert streamlits["new_streamlit"].name == "new_streamlit"


def test_rename_streamlit_with_target_database_and_schema(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:rename?"
        + "targetDatabase=target_db&targetSchema=target_schema&targetName=new_streamlit",
    )
    kwargs = extra_params(
        query_params=[
            ("targetDatabase", "target_db"),
            ("targetSchema", "target_schema"),
            ("targetName", "new_streamlit"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.rename("new_streamlit", target_database="target_db", target_schema="target_schema")
        assert streamlit.name == "new_streamlit"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_streamlit_with_if_exists(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:rename?"
        + "ifExists=True&targetName=new_streamlit",
    )
    kwargs = extra_params(
        query_params=[
            ("ifExists", True),
            ("targetName", "new_streamlit"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.rename("new_streamlit", if_exists=True)
        assert streamlit.name == "new_streamlit"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_commit_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:commit",
    )
    kwargs = extra_params(body=None)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.commit()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.commit_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_add_live_version_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:add-live-version",
    )
    kwargs = extra_params(body=None)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.add_live_version()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.add_live_version_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_add_version_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:add-version",
    )
    req = AddVersionStreamlitRequest(source_location="@stage/app", version=None)
    kwargs = extra_params(body=req.to_dict())

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.add_version(req)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.add_version_async(req)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_add_version_from_git_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:add-version-from-git",
    )
    body = AddVersionFromGitStreamlitRequest(
        version=StreamlitVersionForGit(name="v1"), git_ref="refs/tags/v1"
    ).to_dict()
    kwargs = extra_params(body=body)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.add_version_from_git(
            AddVersionFromGitStreamlitRequest(version=StreamlitVersionForGit(name="v1"), git_ref="refs/tags/v1")
        )
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.add_version_from_git_async(
            AddVersionFromGitStreamlitRequest(version=StreamlitVersionForGit(name="v1"), git_ref="refs/tags/v1")
        )
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_pull_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:pull",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.pull()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.pull_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_push_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:push",
    )
    body = StreamlitPushOptions(force=True).to_dict()
    kwargs = extra_params(body=body)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.push(StreamlitPushOptions(force=True))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.push_async(StreamlitPushOptions(force=True))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_streamlit(fake_root, streamlit):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/streamlits/my_streamlit:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        streamlit.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = streamlit.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
