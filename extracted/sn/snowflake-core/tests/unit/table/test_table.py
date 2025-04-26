from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.table import Table

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.table._generated.api_client.ApiClient.request"
TABLE = Table(name="my_tab", kind="TRANSIENT")


@pytest.fixture
def table(tables):
    return tables["my_tab"]


def test_create_table(fake_root, tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables?createMode=errorIfExists&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)],
        body={
            "name": "my_tab",
            "kind": "TRANSIENT",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tables.create(TABLE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tables.create_async(TABLE)
        assert isinstance(op, PollingOperation)
        table_res = op.result()
        assert table_res.name == "my_tab"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_table_clone(fake_root, tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/clone_table:clone?" + \
            "createMode=errorIfExists&copyGrants=False&targetDatabase=my_db&targetSchema=my_schema",
    )
    kwargs = extra_params(
        query_params=[
            ("createMode", "errorIfExists"),
            ("copyGrants", False),
            ("targetDatabase", tables.database.name),
            ("targetSchema", tables.schema.name),
        ],
        body={
            "name": "my_tab",
            "kind": "PERMANENT",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tables.create("my_tab", clone_table="clone_table")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tables.create_async("my_tab", clone_table="clone_table")
        assert isinstance(op, PollingOperation)
        table_res = op.result()
        assert table_res.name == "my_tab"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_table_as_select(fake_root, tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables:as-select?" + \
            "createMode=errorIfExists&copyGrants=False&query=SELECT 1",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False), ("query", "SELECT 1")],
        body={"name": "my_tab"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tables.create(TABLE, as_select="SELECT 1")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tables.create_async(TABLE, as_select="SELECT 1")
        assert isinstance(op, PollingOperation)
        table_res = op.result()
        assert table_res.name == "my_tab"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tables.create("my_tab", as_select="SELECT 1")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tables.create_async("my_tab", as_select="SELECT 1")
        assert isinstance(op, PollingOperation)
        table_res = op.result()
        assert table_res.name == "my_tab"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_table_like(fake_root, tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/temp_table:create-like?" + \
            "createMode=errorIfExists&copyGrants=False",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)],
        body={"name": "my_tab"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tables.create(TABLE, like_table="temp_table")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tables.create_async(TABLE, like_table="temp_table")
        assert isinstance(op, PollingOperation)
        table_res = op.result()
        assert table_res.name == "my_tab"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_table_using_template(fake_root, tables):
    template = "select array_agg(object_construct(*)) "
    "from table(infer_schema(location=>'@table_test_stage', "
    "file_format=>'table_test_csv_format', "
    "files=>'testCSVheader.csv'))"
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables:using-template?" + \
            f"createMode=errorIfExists&copyGrants=False&query={template}",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False), ("query", template)],
        body={"name": "my_tab"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        tables.create("my_tab", template=template)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tables.create_async("my_tab", template=template)
        assert isinstance(op, PollingOperation)
        table_res = op.result()
        assert table_res.name == "my_tab"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_table(fake_root, table):
    args = (
        fake_root,
        "PUT",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/my_tab",
    )
    kwargs = extra_params(
        body={
            "name": "my_tab",
            "kind": "TRANSIENT",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        table.create_or_alter(TABLE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = table.create_or_alter_async(TABLE)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_table(fake_root, tables):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables?history=False&deep=False",
    )
    kwargs = extra_params(query_params=[("history", False), ("deep", False)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        tables.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = tables.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_table(fake_root, table):
    from snowflake.core.table._generated.models import Table as TableModel

    model = TableModel(name="my_tab", kind="TRANSIENT")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/my_tab",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        table.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = table.fetch_async()
        assert isinstance(op, PollingOperation)
        table = op.result()
        assert table.to_dict() == TABLE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_table(fake_root, table):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/my_tab",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        table.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = table.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_table(fake_root, table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/my_tab:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        table.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = table.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_suspend_recluster_table(fake_root, table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/my_tab:suspend-recluster",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        table.suspend_recluster()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = table.suspend_recluster_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_resume_recluster_table(fake_root, table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tables/my_tab:resume-recluster",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        table.resume_recluster()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = table.resume_recluster_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
