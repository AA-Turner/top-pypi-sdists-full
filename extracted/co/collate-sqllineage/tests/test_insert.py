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


def test_insert_with_template_param():
    assert_table_lineage_equal(
        "INSERT INTO tab1 SELECT col1 FROM tab2 WHERE col2 = {{ start_date }}",
        {"tab2"},
        {"tab1"},
    )


def test_insert_with_join_and_template_param():
    assert_table_lineage_equal(
        "INSERT INTO tab1 SELECT a.col1, b.col2 FROM tab2 a JOIN tab3 b ON a.id = b.id WHERE a.dt > {{ start_date }}",
        {"tab2", "tab3"},
        {"tab1"},
    )
