import pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_drop_warehouse(warehouses):
    warehouse_name = random_string(5, "test_create_warehouse_")
    test_warehouse = Warehouse(
        name=warehouse_name,
        warehouse_size="SMALL",
        auto_suspend=500,
    )

    warehouse_ref = None
    try:
        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.error_if_exists)
        warehouse = warehouse_ref.fetch()
        assert warehouse_name.upper() == warehouse.name.upper()
        warehouse_ref.drop()

        with pytest.raises(NotFoundError):
            warehouse_ref.fetch()

        with pytest.raises(NotFoundError):
            warehouse_ref.drop()

        # Should not error
        warehouse_ref.drop(if_exists=True)

        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.error_if_exists)
        warehouse = warehouse_ref.fetch()
        assert warehouse_name.upper() == warehouse.name.upper()
    finally:
        warehouse_ref.drop()
