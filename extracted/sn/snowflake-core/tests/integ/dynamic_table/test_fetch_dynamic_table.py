import pytest

from tests.integ.dynamic_table.util import assert_dynamic_table


@pytest.mark.min_sf_ver("8.27.0")
def test_fetch(dynamic_table_handle, table_handle, database, schema, db_parameters):
    dynamic_table = dynamic_table_handle.fetch()
    assert_dynamic_table(dynamic_table, dynamic_table_handle.name, table_handle, database, schema, db_parameters, True)
