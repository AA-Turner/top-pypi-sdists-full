from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.database_role import ContainingScope, DatabaseRole, DatabaseRoleCollection, Securable

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.database_role._generated.api_client.ApiClient.request"
DB_ROLE = DatabaseRole(name="my_db_role")
ROLE = Securable(name="my_role")


@pytest.fixture
def database_roles(db, fake_root):
    return DatabaseRoleCollection(db, fake_root)


@pytest.fixture
def database_role(database_roles):
    return database_roles["my_db_role"]


def test_create_database_role(fake_root, database_roles):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/database-roles?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={"name": "my_db_role"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db_role_res = database_roles.create(DB_ROLE)
        assert db_role_res.name == "my_db_role"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = database_roles.create_async(DB_ROLE)
        assert isinstance(op, PollingOperation)
        db_role_res = op.result()
        assert db_role_res.name == "my_db_role"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_database_role(fake_root, database_roles):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/database-roles",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = database_roles.iter()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = database_roles.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_database_role(fake_root, database_role):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/database-roles/my_db_role",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        database_role.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = database_role.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants", "grant_role"), ("grants:revoke", "revoke_role")])
def test_grant_revoke_role(fake_root, database_role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/databases/my_db/database-roles/my_db_role/{method}",
    )
    kwargs = extra_params(
        body={
            "securable": {"name": "my_role"},
            "securable_type": "DATABASE_ROLE",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(database_role, fn)("DATABASE_ROLE", ROLE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(database_role, fn + "_async")("DATABASE_ROLE", ROLE)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants", "grant_privileges"), ("grants:revoke", "revoke_privileges")])
def test_grant_revoke_privileges(fake_root, database_role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/databases/my_db/database-roles/my_db_role/{method}",
    )
    kwargs = extra_params(
        body={
            "securable_type": "database",
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(database_role, fn)(["USAGE"], "database")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(database_role, fn + "_async")(["USAGE"], "database")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants", "grant_privileges_on_all"),
                                        ("grants:revoke", "revoke_privileges_on_all"),
                                        ("future-grants", "grant_future_privileges"),
                                        ("future-grants:revoke", "revoke_future_privileges"),
                                        ])
def test_grant_revoke_future_privileges_on_all(fake_root, database_role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/databases/my_db/database-roles/my_db_role/{method}",
    )
    kwargs = extra_params(
        body={
            "containing_scope": {"database": "my_db"},
            "securable_type": "database",
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        getattr(database_role, fn)(["USAGE"], "database", ContainingScope(database="my_db"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(database_role, fn + "_async")(["USAGE"], "database", ContainingScope(database="my_db"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_revoke_grant_option_for_privileges(fake_root, database_role):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/database-roles/my_db_role/grants:revoke",
    )
    kwargs = extra_params(
        body={
            "securable_type": "database",
            "grant_option": True,
            "privileges": ["USAGE"],
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        database_role.revoke_grant_option_for_privileges(["USAGE"], "database")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = database_role.revoke_grant_option_for_privileges_async(["USAGE"], "database")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


@pytest.mark.parametrize("method, fn", [("grants:revoke", "revoke_grant_option_for_privileges_on_all"),
                                        ("future-grants:revoke", "revoke_grant_option_for_future_privileges"),
                                        ])
def test_revoke_grant_option_for_future_privileges_on_all(fake_root, database_role, method, fn):
    args = (
        fake_root,
        "POST",
        BASE_URL + f"/databases/my_db/database-roles/my_db_role/{method}",
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
        getattr(database_role, fn)(["USAGE"], "database", ContainingScope(database="my_db"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = getattr(database_role, fn + "_async")(["USAGE"], "database", ContainingScope(database="my_db"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)



@pytest.mark.parametrize("method, fn", [("grants", "iter_grants_to"),
                                        ("future-grants", "iter_future_grants_to"),
                                        ])
def test_iter_grants_to(fake_root, database_role, method, fn):
    args = (
        fake_root,
        "GET",
        BASE_URL + f"/databases/my_db/database-roles/my_db_role/{method}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        getattr(database_role, fn)()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = getattr(database_role, fn + "_async")()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
