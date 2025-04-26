from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.dynamic_table import DownstreamLag, DynamicTable, DynamicTableColumn

from ...utils import BASE_URL, extra_params, mock_http_response


@pytest.fixture
def dynamic_tables(schema):
    return schema.dynamic_tables


@pytest.fixture
def dynamic_table(dynamic_tables):
    return dynamic_tables["my_table"]


API_CLIENT_REQUEST = "snowflake.core.dynamic_table._generated.api_client.ApiClient.request"
DYNAMIC_TABLE = DynamicTable(
    name="my_table",
    target_lag=DownstreamLag(),
    warehouse="wh",
    columns=[
        DynamicTableColumn(name="c1", datatype="int"),
    ],
    query="SELECT * FROM foo",
)

def test_create_dynamic_table(fake_root, dynamic_tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_table",
            "kind": "PERMANENT",
            "target_lag": {"type": "DOWNSTREAM"},
            "warehouse": "wh",
            "columns": [{"name": "c1", "datatype": "int"}],
            "query": "SELECT * FROM foo",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_tables.create(DYNAMIC_TABLE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_tables.create_async(DYNAMIC_TABLE)
        assert isinstance(op, PollingOperation)
        dt_res = op.result()
        assert dt_res.name == "my_table"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_dynamic_table_clone(fake_root, dynamic_tables):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/temp_clone_table:clone?" + \
        "createMode=errorIfExists&copyGrants=False&targetDatabase=my_db&targetSchema=my_schema",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False), ("targetDatabase", "my_db"),
                      ("targetSchema", "my_schema")],
        body={"name": "my_table"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_tables.create("my_table", clone_table="temp_clone_table")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_tables.create_async("my_table", clone_table="temp_clone_table")
        assert isinstance(op, PollingOperation)
        dt_res = op.result()
        assert dt_res.name == "my_table"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_dynamic_table(fake_root, dynamic_tables):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables?deep=False",
    )
    kwargs = extra_params(query_params=[("deep", False)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        dynamic_tables.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = dynamic_tables.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_dynamic_table(fake_root, dynamic_table):
    from snowflake.core.dynamic_table._generated.models import DynamicTable as DynamicTableModel
    model = DynamicTableModel(
        name="my_table",
        target_lag=DownstreamLag(),
        warehouse="wh",
        columns=[
            DynamicTableColumn(name="c1", datatype="int"),
        ],
        query="SELECT * FROM foo",
    )

    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        dynamic_table.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = dynamic_table.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == DYNAMIC_TABLE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_undrop_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:undrop",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.undrop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.undrop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_suspend_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:suspend",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.suspend()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.suspend_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_resume_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:resume",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.resume()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.resume_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_refresh_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:refresh",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.refresh()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.refresh_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_swap_with_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:swap-with" + \
        "?targetName=other_db.other_schema.other_table",
    )
    kwargs = extra_params(query_params=[("targetName", "other_db.other_schema.other_table")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.swap_with("other_db.other_schema.other_table")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.swap_with_async("other_db.other_schema.other_table")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_suspend_recluster_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:suspend-recluster",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.suspend_recluster()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.suspend_recluster_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_resume_recluster_dynamic_table(fake_root, dynamic_table):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/dynamic-tables/my_table:resume-recluster",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        dynamic_table.resume_recluster()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = dynamic_table.resume_recluster_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
