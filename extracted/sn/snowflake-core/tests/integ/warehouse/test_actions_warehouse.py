# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import time

from contextlib import suppress

import pytest

from snowflake.core.exceptions import APIError, NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse_fixture")


def test_use_warehouse(warehouses, backup_warehouse_fixture, cursor):
    warehouse_name = random_string(5, "test_use_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)
    warehouse_ref = None

    try:
        warehouse_ref = warehouses.create(test_warehouse)

        # Creating a warehouse may set the active warehouse to the new warehouse; set it back to the original,
        # if one was already active.
        if backup_warehouse_fixture is not None:
            warehouses[backup_warehouse_fixture].use_warehouse()
            cur_warehouse = cursor.execute("SELECT current_warehouse()").fetchone()[0]
            assert cur_warehouse.upper() == backup_warehouse_fixture.upper()

        # Test use warehouse on the new warehouse
        warehouse_ref.use_warehouse()

        cur_warehouse = cursor.execute("SELECT current_warehouse()").fetchone()[0]
        assert cur_warehouse.upper() == warehouse_name.upper()

    finally:
        with suppress(NotFoundError):
            warehouse_ref.drop()


def test_abort_all_queries(warehouses, session):
    warehouse_name = random_string(5, "test_abort_all_queries_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)

    warehouse_ref = None
    try:
        warehouse_ref = warehouses.create(test_warehouse)
        result = next(warehouses.iter(like=warehouse_name))
        time.sleep(5)
        warehouse_ref.abort_all_queries()
        time.sleep(5)
        result = next(warehouses.iter(like=warehouse_name))
        assert result.running == 0 and result.queued == 0

        warehouse_ref.drop()
        warehouse_ref.abort_all_queries(if_exists=True)

    finally:
        with suppress(NotFoundError):
            warehouse_ref.drop()


def test_suspend_and_resume(warehouses):
    warehouse_name = random_string(5, "test_suspend_and_resume_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)

    warehouse_ref = None
    try:
        warehouse_ref = warehouses.create(test_warehouse)
        # Test warehouse suspend from default state
        warehouse_ref.suspend()
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("SUSPENDED", "SUSPENDING")

        # Test warehouse resume from suspended state
        warehouse_ref.resume()
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("STARTING", "STARTED", "RESUMING")

        # suspend again from resumed state
        warehouse_ref.suspend()
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("SUSPENDED", "SUSPENDING")

        # suspend when it is already suspended
        with pytest.raises(APIError):
            warehouse_ref.suspend()

        warehouse_ref.drop()

        # These should not error
        warehouse_ref.suspend(if_exists=True)
        warehouse_ref.resume(if_exists=True)

        warehouse_ref = warehouses.create(test_warehouse)
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("STARTING", "STARTED", "RESUMING")

        # resume from default state - a warehoue cannot be resumed if it is not in suspended state
        # TODO(SNOW-1362454) - Please uncomment this once you have this bug resolved
        # with pytest.raises(APIError):
        #     warehouse_ref.resume()

    finally:
        with suppress(NotFoundError):
            warehouse_ref.drop()
