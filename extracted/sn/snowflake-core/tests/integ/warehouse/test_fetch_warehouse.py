# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.


import pytest

from snowflake.core._common import CreateMode
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_fetch(warehouses):
    warehouse_name = random_string(5, "test_create_warehouse_")
    test_warehouse = Warehouse(
        name=warehouse_name,
        warehouse_size="SMALL",
        auto_suspend=500,
        warehouse_type="STANDARD",
        auto_resume="false",
        initially_suspended="true",
        comment="This IS a COmment",
        max_concurrency_level=2,
        statement_queued_timeout_in_seconds=4,
        statement_timeout_in_seconds=2,
    )

    warehouse_ref = None
    try:
        # Test warehouse create.
        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.error_if_exists)
        warehouse = warehouse_ref.fetch()
        assert warehouse_name.upper() == warehouse.name.upper()
        assert warehouse.size.upper() == "SMALL"
        assert warehouse.auto_suspend == 500
        assert warehouse.type == "STANDARD"
        assert warehouse.auto_resume.upper() == "FALSE"
        # assert warehouse.initially_suspended == "TRUE"
        assert warehouse.comment == "This IS a COmment"
        assert warehouse.max_concurrency_level == 2
        assert warehouse.statement_queued_timeout_in_seconds == 4
        assert warehouse.statement_timeout_in_seconds == 2
        # assert warehouse.tags=="{\"additionalProp1\":\"hello\"}"
    finally:
        warehouse_ref.drop()
