from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.secret import PasswordSecret, SecretResource

from ...utils import BASE_URL, extra_params, mock_http_response


@pytest.fixture
def secrets(schema):
    return schema.secrets


@pytest.fixture
def secret(secrets):
    return secrets["my_secret"]


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
SECRET = PasswordSecret(
    name="my_secret",
    username="snowman",
    password="test",
    comment="Test secret",
)


def test_create_secret(fake_root, secrets):
    kwargs = extra_params(
        query_params=[],
        body={
            "name": "my_secret",
            "username": "snowman",
            "password": "test",
            "type": "PASSWORD",
            "comment": "Test secret",
        },
    )
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/secrets")

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        s_res = secrets.create(SECRET)
        assert isinstance(s_res, SecretResource)
        assert s_res.name == "my_secret"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = secrets.create_async(SECRET)
        assert isinstance(op, PollingOperation)
        s_res = op.result()
        assert s_res.name == "my_secret"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_secret(fake_root, secrets):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/secrets")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        secrets.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = secrets.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_show_limit_deprecation_warning(fake_root, secrets):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/secrets?showLimit=10",
    )
    kwargs = extra_params(query_params=[("showLimit", 10)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            list(secrets.iter(show_limit=10))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        with pytest.warns(DeprecationWarning, match="'show_limit' is deprecated, use 'limit' instead"):
            secrets.iter_async(show_limit=10).result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_limit_and_show_limit_conflict(secrets):
    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        list(secrets.iter(limit=10, show_limit=5))

    with pytest.raises(ValueError, match="Cannot specify both 'limit' and 'show_limit'"):
        secrets.iter_async(limit=10, show_limit=5).result()


def test_fetch_secret(fake_root, secret):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/secrets/my_secret")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SECRET.to_json())
        s = secret.fetch()
        assert s.to_dict() == SECRET.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SECRET.to_json())
        op = secret.fetch_async()
        assert isinstance(op, PollingOperation)
        s = op.result()
        assert s.to_dict() == SECRET.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_secret(fake_root, secret):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/secrets/my_secret")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        secret.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = secret.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
