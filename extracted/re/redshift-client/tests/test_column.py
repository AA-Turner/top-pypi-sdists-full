from redshift_client.core.id_objs import (
    ColumnId,
    Identifier,
)


def test_column_equality() -> None:
    col_1 = ColumnId(Identifier.new("TheRow"))
    col_2 = ColumnId(Identifier.new("THErow"))
    assert col_1 == col_2
