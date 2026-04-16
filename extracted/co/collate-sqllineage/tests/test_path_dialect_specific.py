import pytest

from collate_sqllineage.core.models import Location, Path
from .helpers import assert_table_lineage_equal


@pytest.mark.parametrize("dialect", ["postgres", "redshift"])
def test_copy_from_path(dialect: str):
    """
    https://www.postgresql.org/docs/current/sql-copy.html (Postgres)
    https://docs.aws.amazon.com/es_es/redshift/latest/dg/r_COPY.html (Redshift)
    """
    assert_table_lineage_equal(
        "COPY tab1 FROM 's3://mybucket/mypath'",
        {Path("s3://mybucket/mypath")},
        {"tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_path(dialect: str):
    """
    check following link for syntax reference:
        Snowflake: https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html
        Microsoft T-SQL: https://docs.microsoft.com/en-us/sql/t-sql/statements/copy-into-transact-sql?view=azure-sqldw-latest   # noqa
    FIXME: sqlfluff tsql dialect doesn't support parsing this yet
    """
    assert_table_lineage_equal(
        "COPY INTO tab1 FROM 's3://mybucket/mypath'",
        {Path("s3://mybucket/mypath")},
        {"tab1"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_stage_from_table(dialect: str):
    """
    Snowflake unload: COPY INTO @stage FROM table
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
    """
    assert_table_lineage_equal(
        "COPY INTO @STAGE_01 FROM SCHEMA_01.TABLE_01 FILE_FORMAT = (TYPE = CSV) OVERWRITE = TRUE",
        {"schema_01.table_01"},
        {Location("@STAGE_01")},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_stage(dialect: str):
    """
    Snowflake load: COPY INTO table FROM @stage
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO SCHEMA_01.TABLE_02 FROM @STAGE_01 FILE_FORMAT = (TYPE = CSV)",
        {Location("@STAGE_01")},
        {"schema_01.table_02"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_stage_qualified(dialect: str):
    """
    Snowflake unload with fully qualified stage: COPY INTO @db.schema.stage FROM table
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
    """
    assert_table_lineage_equal(
        "COPY INTO @MY_DB.MY_SCHEMA.MY_STAGE FROM MY_DB.MY_SCHEMA.TABLE_01",
        {"my_db.my_schema.table_01"},
        {Location("@MY_DB.MY_SCHEMA.MY_STAGE")},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_stage_from_subquery(dialect: str):
    """
    Snowflake unload from subquery: COPY INTO @stage FROM (SELECT ... FROM table)
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
    """
    assert_table_lineage_equal(
        "COPY INTO @STAGE_01 FROM (SELECT col1, col2 FROM TABLE_01 WHERE col1 > 10)",
        {"table_01"},
        {Location("@STAGE_01")},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_stage_with_pattern(dialect: str):
    """
    Snowflake load with PATTERN option: COPY INTO table FROM @stage PATTERN = '...'
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO SCHEMA_01.TABLE_02 FROM @STAGE_01 FILE_FORMAT = (TYPE = CSV) PATTERN = '.*[.]csv'",
        {Location("@STAGE_01")},
        {"schema_01.table_02"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_stage_with_subpath(dialect: str):
    """
    Snowflake load from stage with subpath: COPY INTO table FROM @stage/path/
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO SCHEMA_01.TABLE_02 FROM @STAGE_01/data/2024/ FILE_FORMAT = (TYPE = CSV)",
        {Location("@STAGE_01/data/2024/")},
        {"schema_01.table_02"},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_stage_with_subpath_from_table(dialect: str):
    """
    Snowflake unload to stage with subpath: COPY INTO @stage/path/ FROM table
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
    """
    assert_table_lineage_equal(
        "COPY INTO @STAGE_01/output/2024/ FROM SCHEMA_01.TABLE_01",
        {"schema_01.table_01"},
        {Location("@STAGE_01/output/2024/")},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_fully_qualified_table_from_stage(dialect: str):
    """
    Snowflake load with fully qualified table: COPY INTO db.schema.table FROM @stage
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO DB_01.SCHEMA_01.TABLE_02 FROM @STAGE_01 FILE_FORMAT = (TYPE = CSV)",
        {Location("@STAGE_01")},
        {"db_01.schema_01.table_02"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_qualified_stage(dialect: str):
    """
    Snowflake load from fully qualified stage: COPY INTO table FROM @db.schema.stage
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO DB_01.SCHEMA_01.TABLE_02 FROM @DB_01.SCHEMA_01.MY_STAGE",
        {Location("@DB_01.SCHEMA_01.MY_STAGE")},
        {"db_01.schema_01.table_02"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_qualified_stage_with_subpath(dialect: str):
    """
    Snowflake load from 3-part qualified stage with subpath and file extension.
    The ".csv" in the subpath must not be confused with a schema-level dot separator.
    COPY INTO table FROM (SELECT * FROM @db.schema.stage/path/file.csv)
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        """COPY INTO DB_01.SCHEMA_01.TABLE_02
FROM (
    SELECT *
    FROM @DB_01.SCHEMA_01.MY_STAGE/data/2024/export.csv
)
FILE_FORMAT = (TYPE = CSV)""",
        {Location("@DB_01.SCHEMA_01.MY_STAGE/data/2024/export.csv")},
        {"db_01.schema_01.table_02"},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_stage_from_subquery_with_join(dialect: str):
    """
    Snowflake unload from subquery with JOIN:
    COPY INTO @stage FROM (SELECT ... FROM t1 JOIN t2 ...)
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-location
    """
    assert_table_lineage_equal(
        "COPY INTO @STAGE_01 FROM (SELECT a.col1, b.col2 FROM TABLE_01 a JOIN TABLE_02 b ON a.id = b.id)",
        {"table_01", "table_02"},
        {Location("@STAGE_01")},
        dialect=dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_stage_named_file_format(dialect: str):
    """
    Snowflake load with named file format (not inline):
    COPY INTO table FROM @stage FILE_FORMAT = my_format
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO SCHEMA_01.TABLE_02 FROM @STAGE_01 FILE_FORMAT = my_csv_format",
        {Location("@STAGE_01")},
        {"schema_01.table_02"},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["snowflake"])
def test_copy_into_table_from_stage_multiple_options(dialect: str):
    """
    Snowflake load with multiple options (ON_ERROR, FORCE, etc.)
    https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
    """
    assert_table_lineage_equal(
        "COPY INTO SCHEMA_01.TABLE_02 FROM @STAGE_01 FILE_FORMAT = (TYPE = CSV) ON_ERROR = CONTINUE FORCE = TRUE",
        {Location("@STAGE_01")},
        {"schema_01.table_02"},
        dialect=dialect,
    )


@pytest.mark.parametrize("data_source", ["parquet", "json", "csv"])
@pytest.mark.parametrize("dialect", ["databricks", "sparksql"])
def test_select_from_files(data_source: str, dialect: str):
    """
    check following link for syntax reference:
        https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#run-sql-on-files-directly
    """
    assert_table_lineage_equal(
        f"SELECT * FROM {data_source}.`examples/src/main/resources/`",
        {Path("examples/src/main/resources/")},
        dialect=dialect,
    )


@pytest.mark.parametrize("dialect", ["databricks", "hive", "sparksql"])
def test_insert_overwrite_directory(dialect: str):
    """
    check following link for syntax reference:
        https://spark.apache.org/docs/latest/sql-ref-syntax-dml-insert-overwrite-directory.html
    """
    assert_table_lineage_equal(
        """INSERT OVERWRITE DIRECTORY 'hdfs://path/to/folder'
SELECT * FROM tab1""",
        {"tab1"},
        {Path("hdfs://path/to/folder")},
        dialect=dialect,
    )
