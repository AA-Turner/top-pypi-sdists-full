from collate_sqllineage.core.holders import StatementLineageHolder


def test_dummy():
    assert str(StatementLineageHolder()) == repr(StatementLineageHolder())
