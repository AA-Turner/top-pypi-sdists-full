import json

from unittest import mock
from urllib.parse import quote

import pytest

from snowflake.core import PollingOperation
from snowflake.core.function import ServiceFunction
from snowflake.core.version import __version__ as VERSION

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.function._generated.api_client.ApiClient.request"
FUNCTION = ServiceFunction(name="my_fn", arguments=[], service="my_service", endpoint="", path="/path/to/myapp")


@pytest.fixture
def functions(schema):
    return schema.functions


@pytest.fixture
def function(functions):
    return functions["my_fn()"]


def test_create_function(fake_root, functions):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/functions?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_fn",
            "arguments": [],
            "returns": "TEXT",
            "service": "my_service",
            "endpoint": "",
            "path": "/path/to/myapp",
            "function_type": "service-function",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        functions.create(FUNCTION)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = functions.create_async(FUNCTION)
        assert isinstance(op, PollingOperation)
        fn_res = op.result()
        assert fn_res.name_with_args == "my_fn()"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_function(fake_root, functions):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/functions",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        functions.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = functions.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_function(fake_root, function):
    from snowflake.core.function._generated.models import ServiceFunction as ServiceFunctionModel

    model = ServiceFunctionModel(name="my_fn", arguments=[], service="my_service", endpoint="", path="/path/to/myapp")
    args = (
        fake_root,
        "GET",
        BASE_URL + f"/databases/my_db/schemas/my_schema/functions/{quote('my_fn()')}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        function.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = function.fetch_async()
        assert isinstance(op, PollingOperation)
        fn = op.result()
        assert fn.to_dict() == FUNCTION.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_function(fake_root, function):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + f"/databases/my_db/schemas/my_schema/functions/{quote('my_fn()')}?ifExists=False",
    )
    kwargs = extra_params(query_params=[("ifExists", False)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        function.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = function.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_function(fake_root, function):
    from snowflake.core.function._generated.models import ServiceFunction as ServiceFunctionModel

    model = ServiceFunctionModel(name="my_fn", arguments=[], service="my_service", endpoint="", path="/path/to/myapp")
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/functions/my_fn:execute",
    )
    kwargs = extra_params(
        headers={
            "Accept": "application/json",
            "User-Agent": "python_api/" + VERSION,
            "Content-Type": "application/json",
        }
    )
    fetch_response = mock_http_response(model.to_json())
    execute_response = mock_http_response(json.dumps({"result": 1}))

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.side_effect = [fetch_response, execute_response]
        function.execute()
    mocked_request.assert_called_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.side_effect = [fetch_response, execute_response]
        op = function.execute_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_with(*args, **kwargs)
