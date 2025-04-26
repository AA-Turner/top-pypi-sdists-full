import pytest as pytest

from snowflake.core.exceptions import ConflictError, NotFoundError


def test_drop_and_undrop(tables, table_handle):
    table_handle.drop()
    with pytest.raises(NotFoundError):
        table_handle.fetch()

    # if exist is true, no error is raised
    table_handle.drop(if_exists=True)

    table_handle.undrop()
    assert table_handle.fetch() is not None

    with pytest.raises(ConflictError):
        table_handle.undrop()


def test_delete_deprecated(tables, table_handle):
    with pytest.warns(DeprecationWarning, match="method is deprecated; use"):
        table_handle.delete()
        with pytest.raises(NotFoundError):
            table_handle.fetch()


def test_undelete_deprecated(tables, table_handle):
    with pytest.warns(DeprecationWarning, match="method is deprecated; use"):
        table_handle.drop()
        table_handle.undelete()
