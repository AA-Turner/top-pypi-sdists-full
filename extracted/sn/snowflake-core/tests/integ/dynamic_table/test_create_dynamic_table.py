import time

from contextlib import suppress

import pytest

from snowflake.core import Clone, PointOfTimeOffset
from snowflake.core.dynamic_table import (
    DownstreamLag,
    DynamicTable,
    DynamicTableClone,
    DynamicTableColumn,
    UserDefinedLag,
)
from snowflake.core.exceptions import NotFoundError
from snowflake.core.schema import Schema
from tests.utils import random_string


def test_create_from_model_create_mode(dynamic_tables, db_parameters, table_handle):
    table_name = '"' + random_string(10, "test_table_ INTEGRATION_") + '"'
    created_handle = dynamic_tables.create(
        DynamicTable(
            name=table_name,
            columns=[
                DynamicTableColumn(name="c1", comment="column comment"),
                DynamicTableColumn(name='"cc2"', datatype="varchar", comment="column comment"),
            ],
            warehouse=db_parameters["warehouse"],
            refresh_mode="FULL",
            initialize="ON_CREATE",
            comment="test comment",
            target_lag=UserDefinedLag(seconds=60),
            query=f"SELECT * FROM {table_handle.name}",
        ),
        mode="errorifexists",
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == UserDefinedLag(seconds=60)
        assert created_handle.fetch().comment == "test comment"
        assert created_handle.fetch().refresh_mode == "FULL"
        assert created_handle.fetch().initialize == "ON_CREATE"
        assert created_handle.fetch().query == f"SELECT * FROM {table_handle.name}"
        assert created_handle.fetch().warehouse.replace('"', "") == db_parameters["warehouse"].upper().replace('"', "")
        assert created_handle.fetch().columns[0].name.lower() == 'c1'
        assert created_handle.fetch().columns[0].comment == "column comment"
        assert created_handle.fetch().columns[1].comment == "column comment"
        assert "VARCHAR" in created_handle.fetch().columns[1].datatype
        assert created_handle.fetch().columns[1].name.lower() == 'cc2'
    finally:
        with suppress(Exception):
            created_handle.drop()


@pytest.mark.min_sf_ver("8.27.0")
def test_create_clone(dynamic_tables, dynamic_table_handle, session):
    table_name = random_string(10, "test_table_")
    created_handle = dynamic_tables.create(
        table_name, clone_table=f"{dynamic_table_handle.name}", copy_grants=True, mode="errorifexists"
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == DownstreamLag()
    finally:
        with suppress(Exception):
            created_handle.drop()

    time.sleep(1)
    table_name = random_string(10, "test_table_")
    created_handle = dynamic_tables.create(
        DynamicTableClone(
            name=table_name,
            target_lag=UserDefinedLag(seconds=120),
        ),
        clone_table=Clone(
            source=f"{dynamic_table_handle.name}", point_of_time=PointOfTimeOffset(reference="before", when="-1")
        ),
        copy_grants=True,
        mode="errorifexists",
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == UserDefinedLag(seconds=120)
    finally:
        with suppress(Exception):
            created_handle.drop()

    table_name = random_string(10, "test_table_")
    with pytest.raises(
        NotFoundError,
    ):
        dynamic_tables.create(table_name, clone_table="non_existant_name", copy_grants=True, mode="errorifexists")


def test_create_clone_across_schemas(dynamic_table_handle, temp_schema):
    # clone <current_schema>.dynamic_table to temp_schema.table_name
    table_name = random_string(10, "test_clone_table_across_schema_")
    created_handle = temp_schema.dynamic_tables.create(
        DynamicTableClone(
            name=table_name,
            target_lag=UserDefinedLag(seconds=120),
        ),
        clone_table=Clone(
            source=f"{dynamic_table_handle.schema.name}.{dynamic_table_handle.name}"
        ),
        mode="errorifexists",
    )

    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == UserDefinedLag(seconds=120)
        assert created_handle.fetch().schema_name.upper() == temp_schema.name.upper()
    finally:
        with suppress(Exception):
            created_handle.drop()


def test_create_clone_across_database(dynamic_table_handle, temp_db):
    # clone <current_db>.<current_schema>.dynamic_table to temp_db.created_schema.table_name
    schema_name = random_string(10, "test_create_clone_across_database_schema_")
    created_schema = temp_db.schemas.create(Schema(name=schema_name))
    table_name = random_string(10, "test_table_clone_across_database_table_")

    try:
        created_handle = created_schema.dynamic_tables.create(
            DynamicTableClone(
                name=table_name,
                target_lag=UserDefinedLag(seconds=120),
            ),
            clone_table=Clone(
                source=f"{dynamic_table_handle.database.name}.{dynamic_table_handle.schema.name}.{dynamic_table_handle.name}"
            ),
            mode="errorifexists",
        )

        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == UserDefinedLag(seconds=120)
        assert created_handle.fetch().schema_name.upper() == created_schema.name.upper()
        assert created_handle.fetch().database_name.upper() == temp_db.name.upper()
    finally:
        with suppress(Exception):
            created_schema.drop()
