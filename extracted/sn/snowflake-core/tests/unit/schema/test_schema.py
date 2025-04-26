from unittest import mock

from snowflake.core import PollingOperation
from snowflake.core.schema import Schema

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.schema._generated.api_client.ApiClient.request"


def test_create_schema(fake_root, schemas):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_schema",
            "kind": "PERMANENT",
            "managed_access": False,
            "dropped_on": None,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        schemas.create(Schema(name="my_schema"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = schemas.create_async(Schema(name="my_schema"))
        assert isinstance(op, PollingOperation)
        et_res = op.result()
        assert et_res.name == "my_schema"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_schema(fake_root, schemas):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        schemas.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = schemas.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_schema(fake_root, schema):
    args = (
        fake_root,
        "PUT",
        BASE_URL + "/databases/my_db/schemas/my_schema",
    )
    kwargs = extra_params(
        body={
            "name": "my_schema",
            "kind": "PERMANENT",
            "managed_access": False,
            "dropped_on": None,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        schema.create_or_alter(Schema(name="my_schema"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = schema.create_or_alter_async(Schema(name="my_schema"))
        assert isinstance(op, PollingOperation)
        schema_res = op.result()
        assert schema_res.name == "my_schema"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_schema(fake_root, schema):
    from snowflake.core.schema._generated.models import ModelSchema

    model = ModelSchema(name="my_schema")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        schema.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = schema.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == Schema(name="my_schema").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_schema(fake_root, schema):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        schema.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = schema.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_schema(fake_root, schema):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        schema.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = schema.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
