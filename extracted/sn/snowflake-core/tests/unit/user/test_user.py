from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.user import Securable, User, UserCollection

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.user._generated.api_client.ApiClient.request"

@pytest.fixture
def users(fake_root):
    return UserCollection(fake_root)


@pytest.fixture
def user(users):
    return users["admin"]


def test_create_user(fake_root, users):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/users?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "admin",
            "default_secondary_roles": "ALL",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        users.create(User(name="admin"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = users.create_async(User(name="admin"))
        assert isinstance(op, PollingOperation)
        user_res = op.result()
        assert user_res.name == "admin"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_user(fake_root, users):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/users",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        users.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = users.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_user(fake_root, user):
    args = (
        fake_root,
        "PUT",
        BASE_URL + "/users/admin",
    )
    kwargs = extra_params(
        body={
            "name": "admin",
            "default_secondary_roles": "ALL",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user.create_or_alter(User(name="admin"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = user.create_or_alter_async(User(name="admin"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_user(fake_root, user):
    from snowflake.core.user._generated.models import User as UserModel

    model = UserModel(name="admin")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/users/admin",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        user.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = user.fetch_async()
        assert isinstance(op, PollingOperation)
        user = op.result()
        assert user.to_dict() == User(name="admin").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_user(fake_root, user):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/users/admin",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = user.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_grant_role_user(fake_root, user):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/users/admin/grants",
    )
    kwargs = extra_params(
        body={
            "securable": {"name": "test_role"},
            "securable_type": "ROLE",
        }
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user.grant_role("ROLE", Securable(name="test_role"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = user.grant_role_async("ROLE", Securable(name="test_role"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_revoke_role_user(fake_root, user):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/users/admin/grants:revoke",
    )
    kwargs = extra_params(
        body={
            "securable": {"name": "test_role"},
            "securable_type": "ROLE",
        }
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        user.revoke_role("ROLE", Securable(name="test_role"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = user.revoke_role_async("ROLE", Securable(name="test_role"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_grants_to_user(fake_root, user):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/users/admin/grants",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = user.iter_grants_to()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = user.iter_grants_to_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)
