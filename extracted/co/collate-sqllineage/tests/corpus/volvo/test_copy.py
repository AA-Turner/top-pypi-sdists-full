"""Tests for Volvo Snowflake COPY INTO stage lineage queries."""

from tests.helpers import assert_table_lineage_equal

from collate_sqllineage.core.models import Location


def test_volvo_copy_into_table_from_qualified_stage_subquery():
    """Snowflake COPY INTO <table> FROM (SELECT metadata_col, $1 FROM @<qualified_stage>)."""
    sql = """
COPY INTO PROD_VIDA_DB.TRF.MR_PERFLOG_RAW_FILES (SRC_FILE_NAME, XML_DATA)
FROM (
    SELECT METADATA$FILENAME, $1
    FROM @PROD_VIDA_DB.STAGING.STG_PERFLOGS_ROOT_MR
)
FILE_FORMAT = (FORMAT_NAME = 'PROD_VIDA_DB.TRF.FF_XML_PROD')
ON_ERROR = 'CONTINUE';
"""
    assert_table_lineage_equal(
        sql,
        {Location("@PROD_VIDA_DB.STAGING.STG_PERFLOGS_ROOT_MR")},
        {"prod_vida_db.trf.mr_perflog_raw_files"},
        dialect="snowflake",
        # SqlParse adds an intermediate SubQuery node for the COPY FROM subquery; lineage is correct in all parsers.
        skip_graph_check=True,
    )


def test_volvo_copy_into_table_from_stage_with_subpath_and_pattern():
    """Snowflake COPY INTO <table> FROM (SELECT * FROM @<stage>/<subpath>/<file>.csv) with PATTERN and named FILE_FORMAT."""
    sql = """
COPY INTO LOAD."FACT_HUB_RETAIL_DELIVERY_DETAIL"
FROM (
    SELECT *
    FROM @LOAD.STG_DPTSNOPRODOWEU/CDL/FACT_HUB_RETAIL_DELIVERY_DETAIL/2026/04/11/FACT_HUB_RETAIL_DELIVERY_DETAIL_20260411_135837.csv
)
PATTERN = '.*.csv'
FILE_FORMAT = LOAD.CSV_FORMAT
ON_ERROR = CONTINUE;
"""
    assert_table_lineage_equal(
        sql,
        {
            Location(
                "@LOAD.STG_DPTSNOPRODOWEU/CDL/FACT_HUB_RETAIL_DELIVERY_DETAIL/"
                "2026/04/11/FACT_HUB_RETAIL_DELIVERY_DETAIL_20260411_135837.csv"
            )
        },
        {"load.fact_hub_retail_delivery_detail"},
        dialect="snowflake",
        # SqlParse adds an intermediate SubQuery node for the COPY FROM subquery; lineage is correct in all parsers.
        skip_graph_check=True,
    )
