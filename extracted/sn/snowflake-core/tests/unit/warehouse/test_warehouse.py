from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.warehouse import Warehouse, WarehouseCollection

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.warehouse._generated.api_client.ApiClient.request"


@pytest.fixture
def warehouses(fake_root):
    return WarehouseCollection(fake_root)


@pytest.fixture
def warehouse(warehouses):
    return warehouses["my_wh"]


def test_create_warehouse(fake_root, warehouses):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/warehouses?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={"name": "my_wh"},
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouses.create(Warehouse(name="my_wh"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouses.create_async(Warehouse(name="my_wh"))
        assert isinstance(op, PollingOperation)
        wh_res = op.result()
        assert wh_res.name == "my_wh"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_warehouse(fake_root, warehouses):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/warehouses",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        warehouses.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = warehouses.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_warehouse(fake_root, warehouse):
    args = (
        fake_root,
        "PUT",
        BASE_URL + "/warehouses/my_wh",
    )
    kwargs = extra_params(body={"name": "my_wh"})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.create_or_alter(Warehouse(name="my_wh"))
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.create_or_alter_async(Warehouse(name="my_wh"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)



def test_suspend_warehouse(fake_root, warehouse):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/warehouses/my_wh:suspend",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.suspend()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.suspend_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_resume_warehouse(fake_root, warehouse):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/warehouses/my_wh:resume",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.resume()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.resume_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)



def test_fetch_warehouse(fake_root, warehouse):
    from snowflake.core.warehouse._generated.models import Warehouse as WarehouseModel

    model = WarehouseModel(name="my_wh")
    args = (
        fake_root,
        "GET",
        BASE_URL + "/warehouses/my_wh",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        warehouse.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = warehouse.fetch_async()
        assert isinstance(op, PollingOperation)
        tab = op.result()
        assert tab.to_dict() == Warehouse(name="my_wh").to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_warehouse(fake_root, warehouse):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/warehouses/my_wh",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_warehouse(fake_root, warehouse):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/warehouses/my_wh:rename",
    )
    kwargs = extra_params(body={"name": "new_wh"})

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.rename("new_wh")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.rename_async("new_wh")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_abort_all_queries(fake_root, warehouse):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/warehouses/my_wh:abort",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.abort_all_queries()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.abort_all_queries_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_use_warehouse(fake_root, warehouse):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/warehouses/my_wh:use",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        warehouse.use_warehouse()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = warehouse.use_warehouse_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
