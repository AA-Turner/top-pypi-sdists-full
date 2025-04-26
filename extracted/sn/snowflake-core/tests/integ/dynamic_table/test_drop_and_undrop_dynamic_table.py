import pytest as pytest

from snowflake.core.exceptions import NotFoundError


def test_drop_and_undrop(dynamic_table_handle, dynamic_tables):
    dynamic_tables["dummy___table"].drop(if_exists=True)
    dynamic_table_handle.drop()
    with pytest.raises(NotFoundError):
        dynamic_table_handle.fetch()
    dynamic_table_handle.drop(if_exists=True)
    dynamic_table_handle.undrop()
    dynamic_table_handle.fetch()
