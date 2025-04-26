from collate_sqllineage.core.models import DataFunction, Schema
from .helpers import assert_table_lineage_equal


def test_insert_into_select():
    assert_table_lineage_equal(
        "INSERT INTO tab1 SELECT * FROM generate_data_func();",
        {DataFunction("generate_data_func")},
        {"tab1"},
    )


def test_nested_functions():
    assert_table_lineage_equal(
        "create view v1 as select * from my_db.my_schema.get_test_data"
        "(my_schema.get_test_data2(),my_schema.get_test_data3());",
        {
            DataFunction("get_test_data", schema=Schema("my_db.my_schema")),
            DataFunction("get_test_data2", schema=Schema("my_schema")),
            DataFunction("get_test_data3", schema=Schema("my_schema")),
        },
        {"v1"},
    )


def test_nested_functions_union_table():
    assert_table_lineage_equal(
        "create view v1 as select * from my_db.my_schema.get_test_data()"
        " UNION select * from real_table",
        {
            DataFunction("get_test_data", schema=Schema("my_db.my_schema")),
            "real_table",
        },
        {"v1"},
    )


def test_reserved_function():
    assert_table_lineage_equal(
        "create view v1 as select * from table(my_db.my_schema.get_test_data())",
        {DataFunction("get_test_data", schema=Schema("my_db.my_schema"))},
        {"v1"},
    )


def test_source_only():
    assert_table_lineage_equal(
        "select * from table(my_db.my_schema.get_test_data())",
        {DataFunction("get_test_data", schema=Schema("my_db.my_schema"))},
    )


def test_source_only_join():
    assert_table_lineage_equal(
        "select * from table(my_db.my_schema.get_test_data()) a"
        " join table(my_db.my_schema.get_test_data2()) b on a.id = b.id",
        {
            DataFunction("get_test_data", schema=Schema("my_db.my_schema")),
            DataFunction("get_test_data2", schema=Schema("my_db.my_schema")),
        },
    )
