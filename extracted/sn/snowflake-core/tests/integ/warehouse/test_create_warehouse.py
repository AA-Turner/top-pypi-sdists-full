# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.


import pytest

from snowflake.core._common import CreateMode
from snowflake.core._internal.utils import normalize_and_unquote_name
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_create(warehouses, session):
    warehouse_name = random_string(5, "test_create_warehouse_")
    test_warehouse = Warehouse(
        name=warehouse_name,
        warehouse_size="SMALL",
        auto_suspend=500,
    )

    warehouse_ref = None
    try:
        # Test warehouse create.
        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.error_if_exists)
        warehouse = warehouse_ref.fetch()
        assert warehouse_name.upper() == warehouse.name.upper()
        assert warehouse.size.upper() == "SMALL"
        assert warehouse.auto_suspend == 500
    finally:
        warehouse_ref.drop()

    test_warehouse = Warehouse(
        name=warehouse_name,
        warehouse_size="SMALL",
        auto_suspend=300,
    )

    try:
        # Test warehouse create.
        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.or_replace)
        warehouse = warehouse_ref.fetch()
        assert warehouse_name.upper() == warehouse.name.upper()
        assert warehouse.size.upper() == "SMALL"
        assert warehouse.auto_suspend == 300
    finally:
        warehouse_ref.drop()

    warehouse_name = random_string(5, "test_create_warehouse_")
    warehouse_name = f'"{warehouse_name}"'
    test_warehouse = Warehouse(
        name=warehouse_name,
        warehouse_size="SMALL",
        auto_suspend=500,
    )

    warehouse_ref = None
    try:
        # Test warehouse create.
        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.error_if_exists)
        warehouse = warehouse_ref.fetch()
        assert normalize_and_unquote_name(warehouse_name) == warehouse.name
        assert warehouse.size.upper() == "SMALL"
        assert warehouse.auto_suspend == 500
    finally:
        warehouse_ref.drop()
