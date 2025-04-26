# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.


from contextlib import suppress

import pytest

from snowflake.core._internal.utils import normalize_and_unquote_name
from snowflake.core.exceptions import NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_iter(warehouses):
    try:
        warehouse_name_1 = random_string(5, "test_warehouse_")
        warehouse_name_1 = f'"{warehouse_name_1}"'
        warehouse_name_2 = random_string(5, "test_warehouse_A")
        warehouse_name_3 = random_string(5, "test_warehouse_B")
        warehouse_refs = []
        warehouse_refs.append(warehouses.create(warehouse=Warehouse(name=warehouse_name_1)))
        warehouse_refs.append(warehouses.create(warehouse=Warehouse(name=warehouse_name_3)))
        warehouse_refs.append(warehouses.create(warehouse=Warehouse(name=warehouse_name_2)))
        test_warehouses = warehouses.iter(like="%test_warehouse_%")

        expected_warehouse_names = [
            normalize_and_unquote_name(warehouse_name_1),
            warehouse_name_2.upper(),
            warehouse_name_3.upper(),
        ]

        warehouse_list = []
        for warehouse in test_warehouses:
            if warehouse.name in expected_warehouse_names:
                warehouse_list.append(warehouse.name)

        assert len(warehouse_list) == 3
    finally:
        with suppress(NotFoundError):
            for warehouse_ref in warehouse_refs:
                warehouse_ref.drop()
