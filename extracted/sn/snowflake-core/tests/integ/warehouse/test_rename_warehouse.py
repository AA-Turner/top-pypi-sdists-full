# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_rename(warehouses, session):
    warehouse_name = random_string(5, "test_rename_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)

    warehouse_new_name = random_string(5, "test_new_name_warehouse_")
    assert warehouse_name != warehouse_new_name

    warehouse_ref = None
    try:
        # Rename the warehouse to a new name.
        warehouse_ref = warehouses.create(test_warehouse)
        warehouse_ref.rename(warehouse_new_name)
        result1 = warehouses.iter(like=warehouse_name)
        result2 = warehouses.iter(like=warehouse_new_name)
        assert len(list(result1)) == 0 and len(list(result2)) == 1

        # Change the warehouse name back.
        warehouses[warehouse_new_name].rename(warehouse_name)
        result1 = warehouses.iter(like=warehouse_name)
        result2 = warehouses.iter(like=warehouse_new_name)
        assert len(list(result1)) == 1 and len(list(result2)) == 0

        warehouse_ref.drop()

        # Should not error.
        warehouse_ref.rename(warehouse_new_name, if_exists=True)
    finally:
        with suppress(NotFoundError):
            warehouse_ref.drop()
