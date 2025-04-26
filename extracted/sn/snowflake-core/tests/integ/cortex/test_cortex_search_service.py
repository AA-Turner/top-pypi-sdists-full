#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.cortex.search_service import QueryRequest


TEST_SERVICE_NAME = "SNOWPY_TEST_SERVICE"

API_NOT_ENABLED = "Cortex Search API is not enabled"

@pytest.fixture(autouse=True)
def setup_cortex_search_service(connection, database, schema, warehouse, backup_warehouse_fixture):
    del backup_warehouse_fixture
    _database_name = database.name
    _schema_name = schema.name
    with connection.cursor() as cursor:
        cursor.execute(f"use warehouse {warehouse.name}").fetchone()

        test_table_name = f"{_database_name}.{_schema_name}.SNOWPY_TEST_TABLE"
        # Base Table
        cursor.execute(
            f"CREATE OR REPLACE TABLE {test_table_name} (id NUMBER AUTOINCREMENT, col1 VARCHAR, col2 VARCHAR)",
        )

        rows = ",".join(["('hi', 'hello')"] * 20)
        cursor.execute(
            f"INSERT INTO {test_table_name} (col1, col2) VALUES {rows}",
        )

        # Cortex Search Service
        cursor.execute(
            f"CREATE OR REPLACE CORTEX SEARCH SERVICE {_database_name}.{_schema_name}.{TEST_SERVICE_NAME} "
            f"ON col1 TARGET_LAG='1 minute' WAREHOUSE={warehouse.name} "
            f"AS SELECT id, col1, col2 FROM {test_table_name}",
        )

        try:
            yield
        finally:
            cursor.execute(f"DROP CORTEX SEARCH SERVICE {_database_name}.{_schema_name}.{TEST_SERVICE_NAME}")
            cursor.execute(f"DROP TABLE {test_table_name}")


@pytest.fixture(autouse=True)
def precheck_cortex_search_enabled(cortex_search_services, setup_cortex_search_service):
    del setup_cortex_search_service
    try:
        cortex_search_services[TEST_SERVICE_NAME].search("hi", ["col1", "col2"], limit=5)
    except Exception as err:
        if API_NOT_ENABLED in err.body:
            pytest.xfail(API_NOT_ENABLED)
        raise


@pytest.mark.flaky
def test_search(cortex_search_services):
    resp = cortex_search_services[TEST_SERVICE_NAME].search("hi", ["col1", "col2"], limit=5)
    assert len(resp.results) == 5
    for row in resp.results:
        assert row["col1"] is not None
        assert row["col2"] is not None


@pytest.mark.flaky
def test_search_collection(cortex_search_services):
    resp = cortex_search_services.search(
        TEST_SERVICE_NAME,
        QueryRequest.from_dict({"query": "hi", "columns": ["col1", "col2"], "limit": 5}),
    )

    assert len(resp.results) == 5
    for row in resp.results:
        assert row["col1"] is not None
        assert row["col2"] is not None


@pytest.mark.flaky
def test_experimental_arg(cortex_search_services) -> None:
    resp = cortex_search_services[TEST_SERVICE_NAME].search(
        "hi", ["col1", "col2"], limit=5, experimental={"debug": True},
    )
    assert len(resp.results) == 5
    print(resp)
    for row in resp.results:
        assert row["col1"] is not None
        assert row["col2"] is not None
        assert "@DEBUG_PER_RESULT" in row
        assert "TopicalityScore" in row["@DEBUG_PER_RESULT"]
