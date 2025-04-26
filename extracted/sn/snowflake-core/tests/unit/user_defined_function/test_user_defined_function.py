from unittest import mock
from urllib.parse import quote

import pytest

from snowflake.core import PollingOperation, Root
from snowflake.core.user_defined_function import ReturnDataType, SQLFunction, UserDefinedFunction

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.user_defined_function._generated.api_client.ApiClient.request"
UDF = UserDefinedFunction(
    name="my_udf",
    arguments=[],
    return_type=ReturnDataType(datatype="VARCHAR"),
    language_config=SQLFunction(),
)


@pytest.fixture
def user_defined_functions(schema):
    return schema.user_defined_functions


@pytest.fixture
def user_defined_function(user_defined_functions):
    return user_defined_functions["my_udf()"]


def test_create_user_defined_function(fake_root, user_defined_functions):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/user-defined-functions" + \
            "?createMode=errorIfExists&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)],
        body={
            "name": "my_udf",
            "arguments": [],
            "return_type": {"datatype": "VARCHAR", "type": "DATATYPE"},
            "language_config": {"language": "SQL"},
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user_defined_functions.create(UDF)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = user_defined_functions.create_async(UDF)
        assert isinstance(op, PollingOperation)
        udf_res = op.result()
        assert udf_res.name_with_args == "my_udf()"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_user_defined_function(fake_root, user_defined_functions):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/user-defined-functions",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        user_defined_functions.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = user_defined_functions.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_user_defined_function(fake_root, user_defined_function):
    from snowflake.core.user_defined_function._generated.models import ReturnDataType as ReturnDataTypeModel
    from snowflake.core.user_defined_function._generated.models import SQLFunction as SQLFunctionModel
    from snowflake.core.user_defined_function._generated.models import UserDefinedFunction as UserDefinedFunctionModel

    model = UserDefinedFunctionModel(
        name="my_udf",
        arguments=[],
        return_type=ReturnDataTypeModel(datatype="VARCHAR"),
        language_config=SQLFunctionModel(),
    )
    args = (
        fake_root,
        "GET",
        BASE_URL + f"/databases/my_db/schemas/my_schema/user-defined-functions/{quote('my_udf()')}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        user_defined_function.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = user_defined_function.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == UDF.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_user_defined_function(fake_root, user_defined_function):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + f"/databases/my_db/schemas/my_schema/user-defined-functions/{quote('my_udf()')}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user_defined_function.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = user_defined_function.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_user_defined_function(fake_root, user_defined_function, user_defined_functions):
    def format_args(udf_name: str) -> tuple[Root, str, str]:
        return (
            fake_root,
            "POST",
            BASE_URL + f"/databases/my_db/schemas/my_schema/user-defined-functions/{quote(udf_name)}:rename?" + \
            "targetDatabase=my_db&targetSchema=my_schema&targetName=new_udf",
        )
    kwargs = extra_params(
        query_params=[("targetDatabase", "my_db"), ("targetSchema", "my_schema"), ("targetName", "new_udf")]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user_defined_function.rename("new_udf")
        assert user_defined_function.name_with_args == "new_udf()"
    mocked_request.assert_called_once_with(*format_args("my_udf()"), **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        udf_res2 = user_defined_functions["my_udf2()"]
        op = udf_res2.rename_async("new_udf")
        assert isinstance(op, PollingOperation)
        op.result()
        assert udf_res2.name_with_args == "new_udf()"
    mocked_request.assert_called_once_with(*format_args("my_udf2()"), **kwargs)
