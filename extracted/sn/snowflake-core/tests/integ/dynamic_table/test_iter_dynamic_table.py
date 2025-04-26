import pytest

from pydantic import ValidationError

from tests.integ.dynamic_table.util import assert_dynamic_table


@pytest.mark.min_sf_ver("8.27.0")
def test_iter_like(dynamic_tables, dynamic_table_handle, table_handle, database, schema, db_parameters):
    listed_tables_deep = list(dynamic_tables.iter(like=dynamic_table_handle.name, deep=True))
    assert_dynamic_table(
        listed_tables_deep[0], dynamic_table_handle.name, table_handle, database, schema, db_parameters, True
    )

    listed_tables_not_deep = list(dynamic_tables.iter(like=dynamic_table_handle.name, deep=False))
    assert_dynamic_table(
        listed_tables_not_deep[0], dynamic_table_handle.name, table_handle, database, schema, db_parameters, False
    )


@pytest.mark.min_sf_ver("8.27.0")
def test_iter_starts_with(dynamic_tables, dynamic_table_handle, table_handle, database, schema, db_parameters):
    listed_tables_deep = list(dynamic_tables.iter(starts_with=dynamic_table_handle.name.upper(), deep=True))
    assert len(listed_tables_deep) == 1
    assert_dynamic_table(
        listed_tables_deep[0], dynamic_table_handle.name, table_handle, database, schema, db_parameters, True
    )

    listed_tables_deep = list(dynamic_tables.iter(starts_with="zzz", deep=True))
    assert len(listed_tables_deep) == 0


def test_iter_limit(dynamic_tables, dynamic_table_handle):
    data = list(dynamic_tables.iter(limit=10))
    assert 0 < len(data) <= 10
    assert len(list(dynamic_tables.iter(limit=10, from_name='zzzzzzzzzzzz'))) == 0

    with pytest.raises(
        ValidationError,
    ):
        data = list(dynamic_tables.iter(limit=10001))
