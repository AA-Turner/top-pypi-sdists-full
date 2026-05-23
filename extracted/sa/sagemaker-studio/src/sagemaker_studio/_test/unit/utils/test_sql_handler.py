"""Unit tests for sagemaker_studio.utils.sql_handler."""

import unittest
import unittest.mock

from sagemaker_studio.utils.sql_handler import (
    _extract_all_qualified_table_names,
    _extract_from_context_comment,
    _extract_from_use_statements,
    _remove_comments,
    _remove_comments_and_strings,
    get_execution_context,
)
from sagemaker_studio.utils.sqlutils import sql


def _mock_connection(connection_type):
    """Create a mock connection with the given type."""
    conn = unittest.mock.MagicMock()
    conn.type = connection_type
    return conn


class TestTransform(unittest.TestCase):
    """Tests for sql() with connection type routing."""

    def test_empty_query_returns_none(self):
        self.assertIsNone(sql(""))

    def test_whitespace_only_returns_none(self):
        self.assertIsNone(sql("   "))

    def test_none_query_returns_none(self):
        self.assertIsNone(sql(None))

    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._ensure_spark")
    def test_spark_connect_single_line(self, mock_ensure_spark):
        mock_spark = unittest.mock.MagicMock()
        mock_spark.sql.return_value = "spark_result"
        mock_ensure_spark.return_value = mock_spark
        result = sql("SELECT 1", connection={"type": "spark"})
        mock_spark.sql.assert_called_once_with("SELECT 1")
        self.assertEqual(result, "spark_result")

    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._ensure_spark")
    def test_spark_connect_multi_line(self, mock_ensure_spark):
        mock_spark = unittest.mock.MagicMock()
        mock_spark.sql.return_value = "spark_result"
        mock_ensure_spark.return_value = mock_spark
        query = "SELECT\n  1"
        result = sql(query, connection={"type": "spark"})
        mock_spark.sql.assert_called_once_with(query)
        self.assertEqual(result, "spark_result")

    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._ensure_sql_executor")
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._get_or_create_connection")
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._resolve_connection")
    def test_athena_routes_to_engine(self, mock_resolve, mock_get_or_create, mock_executor):
        mock_conn = unittest.mock.MagicMock()
        mock_conn.type = "ATHENA"
        mock_resolve.return_value = mock_conn
        mock_managed = unittest.mock.MagicMock()
        mock_managed.engine = unittest.mock.MagicMock()
        mock_managed.engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_managed.connection = None
        mock_get_or_create.return_value = mock_managed
        mock_exec_result = unittest.mock.MagicMock()
        mock_exec_result.result = "mock_df"
        mock_executor.return_value.execute.return_value = iter([mock_exec_result])
        result = sql("SELECT 1", connection_id="athena-conn")
        mock_resolve.assert_called_once()
        self.assertEqual(result, "mock_df")

    @unittest.mock.patch("sagemaker_studio.utils.sqlutils.get_engine", return_value=None)
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._ensure_duckdb")
    def test_default_connection_calls_duckdb(self, mock_duckdb, mock_get_engine):
        mock_result = unittest.mock.MagicMock()
        mock_result.df.return_value = "mock_df"
        mock_duckdb.return_value.sql.return_value = mock_result
        result = sql("SELECT 1")
        mock_duckdb.return_value.sql.assert_called_once_with("SELECT 1")
        self.assertEqual(result, "mock_df")

    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._ensure_sql_executor")
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._get_or_create_connection")
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._resolve_connection")
    def test_athena_passes_connection_id(self, mock_resolve, mock_get_or_create, mock_executor):
        mock_conn = unittest.mock.MagicMock()
        mock_conn.type = "ATHENA"
        mock_resolve.return_value = mock_conn
        mock_managed = unittest.mock.MagicMock()
        mock_managed.engine = unittest.mock.MagicMock()
        mock_managed.engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_managed.connection = None
        mock_get_or_create.return_value = mock_managed
        mock_exec_result = unittest.mock.MagicMock()
        mock_exec_result.result = "mock_df"
        mock_executor.return_value.execute.return_value = iter([mock_exec_result])
        result = sql("SELECT 1", connection_id="conn-123")
        mock_resolve.assert_called_once_with("conn-123", None)
        self.assertEqual(result, "mock_df")

    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._ensure_sql_executor")
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._get_or_create_connection")
    @unittest.mock.patch("sagemaker_studio.utils.sqlutils._resolve_connection")
    def test_athena_without_connection_id(self, mock_resolve, mock_get_or_create, mock_executor):
        mock_conn = unittest.mock.MagicMock()
        mock_conn.type = "ATHENA"
        mock_resolve.return_value = mock_conn
        mock_managed = unittest.mock.MagicMock()
        mock_managed.engine = unittest.mock.MagicMock()
        mock_managed.engine.get_execution_options.return_value = {"connection_type": "ATHENA"}
        mock_managed.connection = None
        mock_get_or_create.return_value = mock_managed
        mock_exec_result = unittest.mock.MagicMock()
        mock_exec_result.result = "mock_df"
        mock_executor.return_value.execute.return_value = iter([mock_exec_result])
        result = sql("SELECT 1", connection_name="project.athena")
        mock_resolve.assert_called_once_with(None, "project.athena")
        self.assertEqual(result, "mock_df")

    @unittest.mock.patch(
        "sagemaker_studio.utils.sqlutils._ensure_spark",
        side_effect=RuntimeError("Spark session not initialized"),
    )
    def test_spark_connect_raises_without_session(self, mock_ensure_spark):
        with self.assertRaises(RuntimeError):
            sql("SELECT 1", connection={"type": "spark"})


class TestGetExecutionContext(unittest.TestCase):
    """Tests for get_execution_context."""

    def test_empty_string(self):
        result = get_execution_context("")
        self.assertIsNone(result["catalog"])
        self.assertIsNone(result["database"])

    def test_none_input(self):
        result = get_execution_context(None)
        self.assertIsNone(result["catalog"])
        self.assertIsNone(result["database"])

    def test_plain_select(self):
        result = get_execution_context("SELECT * FROM table")
        self.assertIsNone(result["catalog"])
        self.assertIsNone(result["database"])

    def test_context_comment(self):
        sql = "/* @catalog: my_cat, @database: my_db */ SELECT 1"
        result = get_execution_context(sql)
        self.assertEqual(result["catalog"], "my_cat")
        self.assertEqual(result["database"], "my_db")

    def test_use_statements(self):
        sql = "USE CATALOG my_cat; USE DATABASE my_db; SELECT 1"
        result = get_execution_context(sql)
        self.assertEqual(result["catalog"], "my_cat")
        self.assertEqual(result["database"], "my_db")

    def test_three_part_table_name(self):
        sql = "SELECT * FROM my_cat.my_db.my_table"
        result = get_execution_context(sql)
        self.assertEqual(result["catalog"], "my_cat")
        self.assertEqual(result["database"], "my_db")

    def test_context_comment_takes_priority_over_use(self):
        sql = "/* @catalog: comment_cat, @database: comment_db */ USE CATALOG use_cat; SELECT 1"
        result = get_execution_context(sql)
        self.assertEqual(result["catalog"], "comment_cat")
        self.assertEqual(result["database"], "comment_db")

    def test_use_takes_priority_over_table_name(self):
        sql = "USE CATALOG use_cat; USE DATABASE use_db; SELECT * FROM other_cat.other_db.tbl"
        result = get_execution_context(sql)
        self.assertEqual(result["catalog"], "use_cat")
        self.assertEqual(result["database"], "use_db")


class TestExtractFromContextComment(unittest.TestCase):
    """Tests for _extract_from_context_comment."""

    def test_both_catalog_and_database(self):
        sql = "/* @catalog: cat1, @database: db1 */ SELECT 1"
        result = _extract_from_context_comment(sql)
        self.assertEqual(result["catalog"], "cat1")
        self.assertEqual(result["database"], "db1")

    def test_catalog_only(self):
        sql = "/* @catalog: cat1 */ SELECT 1"
        result = _extract_from_context_comment(sql)
        self.assertEqual(result["catalog"], "cat1")
        self.assertIsNone(result["database"])

    def test_no_annotations(self):
        sql = "/* just a comment */ SELECT 1"
        result = _extract_from_context_comment(sql)
        self.assertIsNone(result["catalog"])
        self.assertIsNone(result["database"])

    def test_no_comment(self):
        result = _extract_from_context_comment("SELECT 1")
        self.assertIsNone(result["catalog"])
        self.assertIsNone(result["database"])


class TestExtractFromUseStatements(unittest.TestCase):
    """Tests for _extract_from_use_statements."""

    def test_use_catalog_and_database(self):
        sql = "USE CATALOG my_cat; USE DATABASE my_db;"
        result = _extract_from_use_statements(sql)
        self.assertEqual(result["catalog"], "my_cat")
        self.assertEqual(result["database"], "my_db")

    def test_use_catalog_only(self):
        sql = "USE CATALOG my_cat; SELECT 1"
        result = _extract_from_use_statements(sql)
        self.assertEqual(result["catalog"], "my_cat")

    def test_case_insensitive(self):
        sql = "use catalog MY_CAT; use database MY_DB;"
        result = _extract_from_use_statements(sql)
        self.assertEqual(result["catalog"], "MY_CAT")
        self.assertEqual(result["database"], "MY_DB")

    def test_no_use_statements(self):
        result = _extract_from_use_statements("SELECT 1")
        self.assertIsNone(result["catalog"])
        self.assertIsNone(result["database"])


class TestExtractAllQualifiedTableNames(unittest.TestCase):
    """Tests for _extract_all_qualified_table_names."""

    def test_three_part_name(self):
        sql = "SELECT * FROM cat.db.tbl"
        result = _extract_all_qualified_table_names(sql)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["catalog"], "cat")
        self.assertEqual(result[0]["database"], "db")

    def test_two_part_name(self):
        sql = "SELECT * FROM db.tbl"
        result = _extract_all_qualified_table_names(sql)
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]["catalog"])
        self.assertEqual(result[0]["database"], "db")

    def test_backtick_quoted_identifiers(self):
        sql = "SELECT * FROM `my-cat`.`my-db`.`my-tbl`"
        result = _extract_all_qualified_table_names(sql)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["catalog"], "my-cat")
        self.assertEqual(result[0]["database"], "my-db")

    def test_no_qualified_names(self):
        result = _extract_all_qualified_table_names("SELECT 1")
        self.assertEqual(result, [])


class TestRemoveComments(unittest.TestCase):
    """Tests for _remove_comments."""

    def test_removes_block_comment(self):
        result = _remove_comments("SELECT /* comment */ 1")
        self.assertNotIn("comment", result)
        self.assertIn("SELECT", result)

    def test_removes_line_comment(self):
        result = _remove_comments("SELECT 1 -- comment")
        self.assertNotIn("comment", result)
        self.assertIn("SELECT 1", result)

    def test_no_comments(self):
        self.assertIn("SELECT 1", _remove_comments("SELECT 1"))


class TestRemoveCommentsAndStrings(unittest.TestCase):
    """Tests for _remove_comments_and_strings."""

    def test_removes_string_literals(self):
        result = _remove_comments_and_strings("SELECT 'hello'")
        self.assertNotIn("hello", result)

    def test_preserves_double_quoted_identifiers(self):
        result = _remove_comments_and_strings('SELECT "my_col"')
        self.assertIn("my_col", result)


if __name__ == "__main__":
    unittest.main()
