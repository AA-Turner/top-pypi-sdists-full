"""Unit tests for the Workday Data Connect Cursor class.

Tests DB-API 2.0 cursor interface delegation to the underlying trino cursor.
"""

from unittest.mock import Mock

import pytest

from ...dbapi.cursor import Cursor


@pytest.fixture
def mock_trino_cursor():
    cursor = Mock()
    cursor.description = [
        ("id", "INTEGER", None, None, None, None, None),
        ("name", "VARCHAR", None, None, None, None, None),
    ]
    cursor.rowcount = 42
    cursor.arraysize = 1
    return cursor


@pytest.fixture
def cursor(mock_trino_cursor):
    return Cursor(mock_trino_cursor)


class TestCursorProperties:
    """Test cursor property access."""

    def test_description(self, cursor, mock_trino_cursor):
        assert cursor.description == mock_trino_cursor.description

    def test_rowcount(self, cursor):
        assert cursor.rowcount == 42

    def test_arraysize_get(self, cursor):
        assert cursor.arraysize == 1

    def test_arraysize_set(self, cursor, mock_trino_cursor):
        cursor.arraysize = 100
        mock_trino_cursor.arraysize = 100


class TestCursorExecute:
    """Test cursor execute methods."""

    def test_execute_without_params(self, cursor, mock_trino_cursor):
        cursor.execute("SELECT 1")
        mock_trino_cursor.execute.assert_called_once_with("SELECT 1", None)

    def test_execute_with_params(self, cursor, mock_trino_cursor):
        cursor.execute("SELECT * FROM t WHERE id = %s", (1,))
        mock_trino_cursor.execute.assert_called_once_with("SELECT * FROM t WHERE id = %s", (1,))

    def test_execute_returns_result(self, cursor, mock_trino_cursor):
        mock_trino_cursor.execute.return_value = mock_trino_cursor
        result = cursor.execute("SELECT 1")
        assert result == mock_trino_cursor

    def test_executemany(self, cursor, mock_trino_cursor):
        params = [(1,), (2,), (3,)]
        cursor.executemany("INSERT INTO t VALUES (%s)", params)
        mock_trino_cursor.executemany.assert_called_once_with("INSERT INTO t VALUES (%s)", params)


class TestCursorFetch:
    """Test cursor fetch methods."""

    def test_fetchone(self, cursor, mock_trino_cursor):
        mock_trino_cursor.fetchone.return_value = (1, "Alice")
        result = cursor.fetchone()
        assert result == (1, "Alice")
        mock_trino_cursor.fetchone.assert_called_once()

    def test_fetchone_no_rows(self, cursor, mock_trino_cursor):
        mock_trino_cursor.fetchone.return_value = None
        assert cursor.fetchone() is None

    def test_fetchmany_default_size(self, cursor, mock_trino_cursor):
        mock_trino_cursor.fetchmany.return_value = [(1, "Alice")]
        result = cursor.fetchmany()
        assert result == [(1, "Alice")]
        mock_trino_cursor.fetchmany.assert_called_once_with(1)  # arraysize default

    def test_fetchmany_custom_size(self, cursor, mock_trino_cursor):
        mock_trino_cursor.fetchmany.return_value = [(1, "A"), (2, "B")]
        result = cursor.fetchmany(size=2)
        assert result == [(1, "A"), (2, "B")]
        mock_trino_cursor.fetchmany.assert_called_once_with(2)

    def test_fetchall(self, cursor, mock_trino_cursor):
        mock_trino_cursor.fetchall.return_value = [(1, "A"), (2, "B"), (3, "C")]
        result = cursor.fetchall()
        assert result == [(1, "A"), (2, "B"), (3, "C")]
        mock_trino_cursor.fetchall.assert_called_once()

    def test_fetchall_empty(self, cursor, mock_trino_cursor):
        mock_trino_cursor.fetchall.return_value = []
        assert cursor.fetchall() == []


class TestCursorClose:
    """Test cursor close."""

    def test_close(self, cursor, mock_trino_cursor):
        cursor.close()
        mock_trino_cursor.close.assert_called_once()


class TestCursorIteration:
    """Test cursor iteration protocol."""

    def test_iter(self, cursor, mock_trino_cursor):
        mock_trino_cursor.__iter__ = Mock(return_value=iter([(1,), (2,)]))
        results = list(cursor)
        assert results == [(1,), (2,)]

    def test_next(self, cursor, mock_trino_cursor):
        mock_trino_cursor.__next__ = Mock(return_value=(1,))
        assert next(cursor) == (1,)


class TestCursorNoOps:
    """Test no-op methods required by DB-API 2.0."""

    def test_setinputsizes(self, cursor):
        # Should not raise
        cursor.setinputsizes([100, 200])

    def test_setoutputsize(self, cursor):
        # Should not raise
        cursor.setoutputsize(1000)
        cursor.setoutputsize(1000, column=0)
