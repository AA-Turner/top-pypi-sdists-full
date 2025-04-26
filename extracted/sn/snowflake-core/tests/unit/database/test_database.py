from unittest import mock

from snowflake.core import PollingOperation
from snowflake.core.database import Database

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.database._generated.api_client.ApiClient.request"

def test_create_database(fake_root, dbs):
    database = Database(
        name="sophie_db",
        kind="TRANSIENT",
        comment="This is Sophie's database",
        trace_level="always",
    )
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "sophie_db",
            "kind": "TRANSIENT",
            "comment": "This is Sophie's database",
            "trace_level": "always",
            "dropped_on": None,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db_res = dbs.create(database)
        assert db_res.name == database.name
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dbs.create_async(database)
        assert isinstance(op, PollingOperation)
        db_res = op.result()
        assert db_res.name == database.name
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_database(fake_root, dbs):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = dbs.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        BASE_URL + "/databases",
        **extra_params()
    )


def test_fetch_database(fake_root, db):
    from snowflake.core.database._generated.models import Database as DatabaseModel

    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(DatabaseModel(name="my_db").to_json())
        database = db.fetch()
        assert database.to_dict() == Database("my_db").to_dict()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(DatabaseModel(name="my_db").to_json())
        op = db.fetch_async()
        assert isinstance(op, PollingOperation)
        database = op.result()
        assert database.to_dict() == Database("my_db").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_database(fake_root, db):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_database(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_enable_replication(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/replication:enable?ignore_edition_check=False",
    )
    kwargs = extra_params(
        query_params=[("ignore_edition_check", False)],
        body={"accounts": ["acc"]},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.enable_replication(["acc"])
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.enable_replication_async(["acc"])
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_disable_replication(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/replication:disable",
    )
    kwargs = extra_params(body={"accounts": []})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.disable_replication()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.disable_replication_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_refresh_replication(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/replication:refresh",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.refresh_replication()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.refresh_replication_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_enable_failover(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/failover:enable",
    )
    kwargs = extra_params(body={"accounts": ["acc"]})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.enable_failover(["acc"])
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.enable_failover_async(["acc"])
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_disable_failover(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/failover:disable",
    )
    kwargs = extra_params(body={"accounts": []})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.disable_failover()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.disable_failover_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_promote_to_primary_failover(fake_root, db):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/failover:primary",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        db.promote_to_primary_failover()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = db.promote_to_primary_failover_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
