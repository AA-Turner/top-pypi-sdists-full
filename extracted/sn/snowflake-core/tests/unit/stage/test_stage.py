from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.stage import Stage

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.stage._generated.api_client.ApiClient.request"


@pytest.fixture
def stages(schema):
    return schema.stages


@pytest.fixture
def stage(stages):
    return stages["my_stage"]


def test_create_stage(fake_root, stages):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/stages?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_stage",
            "kind": "PERMANENT",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        stages.create(Stage(name="my_stage"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = stages.create_async(Stage(name="my_stage"))
        assert isinstance(op, PollingOperation)
        stage_res = op.result()
        assert stage_res.name == "my_stage"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_stage(fake_root, stages):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/stages",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        stages.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = stages.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_stage(fake_root, stage):
    from snowflake.core.stage._generated.models import Stage as StageModel

    model = StageModel(name="my_stage")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/stages/my_stage",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        stage.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = stage.fetch_async()
        assert isinstance(op, PollingOperation)
        stage = op.result()
        assert stage.to_dict() == Stage(name="my_stage").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_stage(fake_root, stage):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/stages/my_stage",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        stage.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = stage.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_list_files(fake_root, stage):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/stages/my_stage/files",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        stage.list_files()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = stage.list_files_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)
