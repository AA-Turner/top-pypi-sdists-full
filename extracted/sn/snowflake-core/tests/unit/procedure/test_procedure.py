import json

from unittest import mock
from urllib.parse import quote

import pytest

from snowflake.core import PollingOperation
from snowflake.core.procedure import CallArgumentList, Procedure, ReturnDataType, SQLFunction

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.procedure._generated.api_client.ApiClient.request"
PROCEDURE = Procedure(
    name="my_proc",
    arguments=[],
    return_type=ReturnDataType(datatype="VARCHAR"),
    language_config=SQLFunction(),
    body = "SELECT 'xyz'"
)


@pytest.fixture
def procedures(schema):
    return schema.procedures


@pytest.fixture
def procedure(procedures):
    return procedures["my_proc()"]


def test_create_procedure(fake_root, procedures):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/procedures?createMode=errorIfExists&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)],
        body={
            "name": "my_proc",
            "arguments": [],
            "return_type": {"datatype": "VARCHAR", "type": "DATATYPE"},
            "language_config": {"language": "SQL"},
            "body": "SELECT 'xyz'",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        proc_res = procedures.create(PROCEDURE)
        assert proc_res.name_with_args == "my_proc()"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = procedures.create_async(PROCEDURE)
        assert isinstance(op, PollingOperation)
        proc_res = op.result()
        assert proc_res.name_with_args == "my_proc()"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_procedure(fake_root, procedures):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/procedures",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = procedures.iter()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = procedures.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_procedure(fake_root, procedure):
    from snowflake.core.procedure._generated.models import Procedure as ProcedureModel
    from snowflake.core.procedure._generated.models import ReturnDataType as ReturnDataTypeModel
    from snowflake.core.procedure._generated.models import SQLFunction as SQLFunctionModel

    model = ProcedureModel(
        name="my_proc",
        arguments=[],
        return_type=ReturnDataTypeModel(datatype="VARCHAR"),
        language_config=SQLFunctionModel(),
        body="SELECT 'xyz'"
    )
    args = (
        fake_root,
        "GET",
        BASE_URL + f"/databases/my_db/schemas/my_schema/procedures/{quote('my_proc()')}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        my_proc = procedure.fetch()
        assert my_proc.to_dict() == PROCEDURE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = procedure.fetch_async()
        assert isinstance(op, PollingOperation)
        my_proc = op.result()
        assert my_proc.to_dict() == PROCEDURE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_procedure(fake_root, procedure):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + f"/databases/my_db/schemas/my_schema/procedures/{quote('my_proc()')}?ifExists=False",
    )
    kwargs = extra_params(query_params=[("ifExists", False)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        procedure.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = procedure.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_call_procedure(fake_root, procedure):
    from snowflake.core.procedure._generated.models import Procedure as ProcedureModel
    from snowflake.core.procedure._generated.models import ReturnDataType as ReturnDataTypeModel
    from snowflake.core.procedure._generated.models import SQLFunction as SQLFunctionModel

    model = ProcedureModel(
        name="my_proc",
        arguments=[],
        return_type=ReturnDataTypeModel(datatype="VARCHAR"),
        language_config=SQLFunctionModel(),
        body="SELECT 'xyz'"
    )
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/procedures/my_proc:call",
    )
    kwargs = extra_params(body={"call_arguments": []})
    fetch_response = mock_http_response(model.to_json())
    call_response = mock_http_response(json.dumps([{"result": "xyz"}]))

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.side_effect = [fetch_response, call_response]
        procedure.call(call_argument_list=CallArgumentList(call_arguments=[]))
    mocked_request.assert_called_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.side_effect = [fetch_response, call_response]
        op = procedure.call_async(call_argument_list=CallArgumentList(call_arguments=[]))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_with(*args, **kwargs)
