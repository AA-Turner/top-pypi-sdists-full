"""Tests for the async-path eager-first-batch skip on the Redshift Data API cursor.

The DB-API ``Cursor.execute`` normally fetches the first ``GetStatementResult``
page during ``execute`` to resolve column metadata (``DescribeStatement`` does not
return it). The async path reads rows later by ``statement_id`` with a fresh
client, so that eager page is a pure duplicate download -- heavy for large
results. ``Connection._skip_eager_result_load`` opts the cursor out of it while
still capturing ``statement_id``/metadata.
"""

import unittest
from unittest import mock

from sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.cursor import Cursor


class _FakeConnection:
    """Minimal stand-in for the DB-API Connection the cursor holds."""

    def __init__(self, skip_eager=False):
        self._skip_eager_result_load = skip_eager
        self._session_id = None


def _make_cursor(skip_eager, *, execute_result, batch_result=None):
    """Build a Cursor with a mocked StatementExecutor.

    ``execute_result`` is returned by ``execute_statement``; ``batch_result`` (if
    given) by ``get_statement_result`` (the eager/lazy page fetch).
    """
    with mock.patch(
        "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.cursor.StatementExecutor"
    ):
        cursor = Cursor(_FakeConnection(skip_eager=skip_eager))
    cursor._executor = mock.MagicMock()
    cursor._executor.execute_statement.return_value = execute_result
    cursor._executor.get_statement_result.return_value = batch_result or {
        "Records": [],
        "ColumnMetadata": [],
        "NextToken": None,
    }
    return cursor


# A FINISHED result-bearing statement WITHOUT column metadata (the real-world
# shape: DescribeStatement carries no ColumnMetadata), which is exactly what
# triggers the eager-first-batch fallback.
_RESULT_NO_META = {
    "statement_id": "stmt-123",
    "has_result_set": True,
    "records_updated": 0,
    "result_metadata": None,
    "result_rows": 42,
    "result_size": 8500,
}

_FIRST_PAGE = {
    "Records": [[{"stringValue": "a"}]],
    "ColumnMetadata": [{"name": "col", "typeName": "varchar"}],
    "NextToken": None,
}


class RedshiftCursorEagerSkipTest(unittest.TestCase):
    def test_skip_flag_suppresses_eager_first_batch(self):
        """With the opt-out set, execute() must NOT fetch the first page."""
        cursor = _make_cursor(True, execute_result=_RESULT_NO_META, batch_result=_FIRST_PAGE)
        cursor.execute("SELECT 1")
        cursor._executor.get_statement_result.assert_not_called()
        # statement_id/metadata were still captured for the async reader.
        self.assertEqual(cursor._statement_id, "stmt-123")
        self.assertTrue(cursor._has_result_set)
        meta = cursor.get_execution_metadata()
        self.assertEqual(meta["statement_id"], "stmt-123")

    def test_default_still_eager_loads(self):
        """Without the opt-out, execute() keeps the original eager-fetch behavior."""
        cursor = _make_cursor(False, execute_result=_RESULT_NO_META, batch_result=_FIRST_PAGE)
        cursor.execute("SELECT 1")
        cursor._executor.get_statement_result.assert_called_once()
        # Eager load resolved the real column metadata (not the placeholder).
        self.assertEqual(cursor.description[0][0], "col")

    def test_missing_flag_defaults_to_eager(self):
        """A connection without the attribute at all must still eager-load."""
        with mock.patch(
            "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.cursor.StatementExecutor"
        ):
            cursor = Cursor(object())  # no _skip_eager_result_load attribute
        cursor._executor = mock.MagicMock()
        cursor._executor.execute_statement.return_value = _RESULT_NO_META
        cursor._executor.get_statement_result.return_value = _FIRST_PAGE
        cursor.execute("SELECT 1")
        cursor._executor.get_statement_result.assert_called_once()

    def test_fetchone_lazy_loads_after_skip(self):
        """After skipping the eager load, fetchone() still lazily fetches rows."""
        cursor = _make_cursor(True, execute_result=_RESULT_NO_META, batch_result=_FIRST_PAGE)
        cursor.execute("SELECT 1")
        cursor._executor.get_statement_result.assert_not_called()
        row = cursor.fetchone()
        # Lazy path fired exactly when a row was actually requested.
        cursor._executor.get_statement_result.assert_called_once()
        self.assertEqual(row, ["a"])
        self.assertEqual(cursor.description[0][0], "col")

    def test_present_column_metadata_never_fetches_regardless_of_flag(self):
        """When DescribeStatement DID carry column metadata, neither path fetches."""
        result_with_meta = dict(_RESULT_NO_META)
        result_with_meta["result_metadata"] = {"ColumnMetadata": [{"name": "c", "typeName": "int"}]}
        for skip in (True, False):
            cursor = _make_cursor(skip, execute_result=result_with_meta)
            cursor.execute("SELECT 1")
            cursor._executor.get_statement_result.assert_not_called()
            self.assertEqual(cursor.description[0][0], "c")


class RedshiftConnectionSkipFlagDefaultTest(unittest.TestCase):
    def test_connection_defaults_skip_eager_to_false(self):
        """A freshly constructed Connection must default the opt-out to False, so the
        eager-fetch behavior is unchanged unless the async path explicitly opts out."""
        with mock.patch(
            "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.create_connection_params",
            return_value={},
        ), mock.patch(
            "sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection.RedshiftDataAPIClient"
        ):
            from sagemaker_studio.sql_engine._sqlalchemy_redshift_data_api.dbapi.connection import (
                Connection,
            )

            conn = Connection(database_name="dev", workgroup_name="wg")
        self.assertFalse(conn._skip_eager_result_load)


if __name__ == "__main__":
    unittest.main()
