from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.role import ContainingScope, Role, RoleCollection, Securable

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.role._generated.api_client.ApiClient.request"
ROLE = Role(name="my_role")
OTHER_ROLE = Securable(name="my_role")


@pytest.fixture
def roles(fake_root):
    return RoleCollection(fake_root)


@pytest.fixture
def role(roles):
    return roles["my_role"]


def test_create_role(fake_root, roles):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/roles?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={"name": "my_role"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        role_res = roles.create(ROLE)
        assert role_res.name == "my_role"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = roles.create_async(ROLE)
        assert isinstance(op, PollingOperation)
        role_res = op.result()
        assert role_res.name == "my_role"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_role(fake_root, roles):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/roles",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = roles.iter()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = roles.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_role(fake_root, role):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/roles/my_role",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        role.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = role.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants", "grant_role"), ("grants:revoke", "revoke_role")])
def test_grant_revoke_role(fake_root, role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/roles/my_role/{method}",
    )
    kwargs = extra_params(
        body={
            "securable": {"name": "my_role"},
            "securable_type": "ROLE",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(role, fn)("ROLE", OTHER_ROLE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(role, fn + "_async")("ROLE", OTHER_ROLE)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants", "grant_privileges"), ("grants:revoke", "revoke_privileges")])
def test_grant_revoke_privileges(fake_root, role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/roles/my_role/{method}",
    )
    kwargs = extra_params(
        body={
            "securable_type": "database",
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(role, fn)(["USAGE"], "database")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(role, fn + "_async")(["USAGE"], "database")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants", "grant_privileges_on_all"),
                                        ("grants:revoke", "revoke_privileges_on_all"),
                                        ("future-grants", "grant_future_privileges"),
                                        ("future-grants:revoke", "revoke_future_privileges"),
                                        ])
def test_grant_revoke_future_privileges_on_all(fake_root, role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/roles/my_role/{method}",
    )
    kwargs = extra_params(
        body={
            "containing_scope": {"database": "my_db"},
            "securable_type": "database",
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(role, fn)(["USAGE"], "database", ContainingScope(database="my_db"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(role, fn + "_async")(["USAGE"], "database", ContainingScope(database="my_db"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_revoke_grant_option_for_privileges(fake_root, role):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/roles/my_role/grants:revoke",
    )
    kwargs = extra_params(
        body={
            "securable_type": "database",
            "grant_option": True,
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        role.revoke_grant_option_for_privileges(["USAGE"], "database")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = role.revoke_grant_option_for_privileges_async(["USAGE"], "database")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants:revoke", "revoke_grant_option_for_privileges_on_all"),
                                        ("future-grants:revoke", "revoke_grant_option_for_future_privileges"),
                                        ])
def test_revoke_grant_option_for_future_privileges_on_all(fake_root, role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/roles/my_role/{method}",
    )
    kwargs = extra_params(
        body={
            "containing_scope": {"database": "my_db"},
            "securable_type": "database",
            "grant_option": True,
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(role, fn)(["USAGE"], "database", ContainingScope(database="my_db"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(role, fn + "_async")(["USAGE"], "database", ContainingScope(database="my_db"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)



@pytest.mark.parametrize("method, fn", [("grants-of", "iter_grants_of"),
                                        ("grants-on", "iter_grants_on"),
                                        ("grants", "iter_grants_to"),
                                        ("future-grants", "iter_future_grants_to"),
                                        ])
def test_iter_grants_to(fake_root, role, method, fn):
    args = (
        fake_root,
        "GET",
        BASE_URL + f"/roles/my_role/{method}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        getattr(role, fn)()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = getattr(role, fn + "_async")()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
