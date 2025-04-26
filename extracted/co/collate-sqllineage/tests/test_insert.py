from .helpers import assert_table_lineage_equal


def test_insert_into():
    assert_table_lineage_equal("INSERT INTO tab1 VALUES (1, 2)", set(), {"tab1"})


def test_insert_into_select():
    assert_table_lineage_equal(
        "INSERT INTO tab1 SELECT * FROM tab2;",
        {"tab2"},
        {"tab1"},
    )


def test_insert_into_select_join():
    assert_table_lineage_equal(
        "INSERT INTO tab1 SELECT * FROM (tab2 a join tab3 b on a.id = b.id);",
        {"tab2", "tab3"},
        {"tab1"},
        test_sqlparse=False,
    )
