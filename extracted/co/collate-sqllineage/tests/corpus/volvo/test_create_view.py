"""Tests for create view."""

import pytest

from tests.helpers import (
    TestColumnQualifierTuple,
    assert_column_lineage_equal,
    assert_table_lineage_equal,
)


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_create_view(dialect: str):
    sql = """create or replace view STG_METERING_HISTORY(
    SERVICE_TYPE,
    START_TIME,
    END_TIME,
    ENTITY_ID,
    ENTITY_TYPE,
    NAME,
    DATABASE_ID,
    DATABASE_NAME,
    SCHEMA_ID,
    SCHEMA_NAME,
    CREDITS_USED_COMPUTE,
    CREDITS_USED_CLOUD_SERVICES,
    CREDITS_USED,
    BYTES,
    "ROWS",
    FILES
) as (
    with source as (
select
   *
from SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
),

final as (
    select * from source
)

select * from final
  );"""
    assert_table_lineage_equal(
        sql,
        {"snowflake.account_usage.metering_history"},  # source_tables
        {"<default>.stg_metering_history"},  # target_tables
        dialect=dialect,
        test_sqlparse=False,  # doesn't recognize lineage
    )

    assert_column_lineage_equal(
        sql,
        [
            (
                TestColumnQualifierTuple(
                    "*", "snowflake.account_usage.metering_history"
                ),
                TestColumnQualifierTuple("*", "<default>.stg_metering_history"),
            )
        ],
        dialect=dialect,
        # SqlGlot and SqlParse doesn't recognize column lineage from this query
        # TODO: Fix SqlGlot to handle columns expansion correctly in CTEs
        test_sqlglot=False,
        test_sqlparse=False,
    )
