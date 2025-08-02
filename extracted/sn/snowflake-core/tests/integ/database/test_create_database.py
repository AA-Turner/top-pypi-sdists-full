#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import copy
import json
import time

import pytest

from snowflake.core import Clone, CreateMode, PointOfTimeOffset
from snowflake.core.database import Database, DatabaseCollection
from snowflake.core.exceptions import APIError, ConflictError, UnauthorizedError
from tests.utils import random_string, unquote


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_create_database(databases: DatabaseCollection):
    new_db_def = Database(name=random_string(3, "test_database_$12create_"), kind="TRANSIENT")
    new_db_def.comment = "database first"
    database = databases.create(new_db_def)
    try:
        created_database = database.fetch()
        assert created_database.name == new_db_def.name.upper()
        assert created_database.kind == "TRANSIENT"
        assert created_database.comment == new_db_def.comment

        with pytest.raises(ConflictError):
            databases.create(new_db_def, mode=CreateMode.error_if_exists)

        new_db_def_1 = copy.deepcopy(new_db_def)
        new_db_def_1.comment = "databse second"
        new_db_def_1.kind = None
        database = databases.create(new_db_def_1, mode=CreateMode.if_not_exists)

        created_database = database.fetch()
        assert created_database.name == new_db_def.name.upper()
        assert created_database.kind == "TRANSIENT"
        assert created_database.comment == new_db_def.comment
    finally:
        database.drop()

    try:
        database = databases.create(new_db_def_1, mode=CreateMode.or_replace)

        created_database = database.fetch()
        assert created_database.name == new_db_def_1.name.upper()
        assert created_database.kind == "PERMANENT"
        assert created_database.comment == new_db_def_1.comment
    finally:
        database.drop()

    try:
        database_name = random_string(10, "test_database_INT_test_")
        database_name_case_sensitive = '"' + database_name + '"'
        new_db_def = Database(name=database_name_case_sensitive)
        database = databases.create(new_db_def)
        created_database = database.fetch()
        assert created_database.name == unquote(new_db_def.name)
    finally:
        database.drop()

    try:
        database_name = random_string(10, 'test_database_""INT""_test_#_')
        database_name_case_sensitive = '"' + database_name + '"'
        new_db_def = Database(name=database_name_case_sensitive)
        database = databases.create(new_db_def)
        created_database = database.fetch()
        assert created_database.name == unquote(new_db_def.name)
    finally:
        database.drop()


@pytest.mark.min_sf_ver("9.8.0")
def test_create_clone(databases: DatabaseCollection):
    database_name = random_string(3, "test_database_")
    database_def = Database(name=database_name, kind="TRANSIENT")

    new_database_name = random_string(3, "test_database_clone_")
    new_database_def = Database(name=new_database_name)

    # error because Database does not exist
    with pytest.raises(APIError):
        databases.create(
            new_database_def,
            clone=Clone(source=database_name, point_of_time=PointOfTimeOffset(reference="before", when="-5")),
            mode=CreateMode.or_replace,
        )

    databases.create(database_def)
    with pytest.raises(APIError, match="transient object cannot be cloned to a permanent object"):
        databases.create(
            new_database_def,
            clone=Clone(source=database_name, point_of_time=PointOfTimeOffset(reference="before", when="-1")),
            mode=CreateMode.or_replace,
        )

    # can clone transient to transient
    new_database_def.kind = "TRANSIENT"
    # sleep is needed due to using point_of_time in clone
    time.sleep(2)
    databases.create(
        new_database_def,
        clone=Clone(source=database_name, point_of_time=PointOfTimeOffset(reference="at", when="-1")),
        mode=CreateMode.or_replace,
    )

    # replaced transient to permanent database
    new_database_def.kind = database_def.kind = "PERMANENT"
    databases.create(database_def, mode=CreateMode.or_replace)
    db = databases.create(new_database_def, clone=Clone(source=database_name), mode=CreateMode.or_replace)
    try:
        db.fetch()
    finally:
        db.drop()

    # clone database setting optional attributes on the clone
    new_database_def.serverless_task_min_statement_size = "SMALL"
    new_database_def.serverless_task_max_statement_size = "MEDIUM"
    new_database_def.user_task_managed_initial_warehouse_size = "SMALL"
    new_database_def.suspend_task_after_num_failures = 2
    new_database_def.user_task_timeout_ms = 20000
    databases.create(database_def, mode=CreateMode.or_replace)
    db = databases.create(new_database_def, clone=Clone(source=database_name), mode=CreateMode.or_replace)
    try:
        fetched_db = db.fetch()
        assert fetched_db.serverless_task_min_statement_size == "SMALL"
        assert fetched_db.serverless_task_max_statement_size == "MEDIUM"
        assert fetched_db.user_task_managed_initial_warehouse_size == "SMALL"
        assert fetched_db.suspend_task_after_num_failures == 2
        assert fetched_db.user_task_timeout_ms == 20000
    finally:
        db.drop()


@pytest.mark.usefixtures("shared_database_available")
def test_create_from_share(databases: DatabaseCollection):
    new_db_name = random_string(3, "test_db_from_share_")

    try:
        db = databases.create(Database(name=new_db_name), from_share='SFSALESSHARED.SFC_SAMPLES_PROD3."SAMPLE_DATA"')

        try:
            assert db.fetch().is_current
        finally:
            db.drop()

    except UnauthorizedError as err:
        # We can't import this more than once if another test has already imported it.
        # So, catch that case and pass if that is detected.
        assert "importing more than once is not supported" in json.loads(err.body)["message"]
        pytest.skip("Test was not run because of database was already shared.")
