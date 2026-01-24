from fa_purity import (
    FrozenDict,
    Unsafe,
)

from redshift_client.core.column import (
    Column,
)
from redshift_client.core.data_type.core import (
    DataType,
    StaticTypes,
)
from redshift_client.core.id_objs import (
    ColumnId,
    Identifier,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client._factory import (
    DbPrimitiveFactory,
)

_column_1 = ColumnId(Identifier.new("column_1"))
_column_2 = ColumnId(Identifier.new("column_2"))
_mock_type = Column(
    DataType(StaticTypes.BOOLEAN),
    False,
    DbPrimitiveFactory.from_raw(None),
)


def test_missing_order() -> None:
    assert (
        Table.new(
            (_column_2,),
            FrozenDict({_column_1: _mock_type}),
            frozenset([]),
        )
        .map(
            lambda _: Unsafe.raise_exception(ValueError("Should not success")),
        )
        .to_union()
    )


def test_duplicated_order() -> None:
    assert (
        Table.new(
            (_column_2, _column_2, _column_1),
            FrozenDict({_column_1: _mock_type, _column_2: _mock_type}),
            frozenset([]),
        )
        .map(
            lambda _: Unsafe.raise_exception(ValueError("Should not success")),
        )
        .to_union()
    )


def test_missing_columns() -> None:
    assert (
        Table.new(
            (_column_2, _column_1),
            FrozenDict({_column_2: _mock_type}),
            frozenset([]),
        )
        .map(
            lambda _: Unsafe.raise_exception(ValueError("Should not success")),
        )
        .to_union()
    )


def test_invalid_key() -> None:
    assert (
        Table.new(
            (_column_1,),
            FrozenDict({_column_1: _mock_type}),
            frozenset([_column_2]),
        )
        .map(
            lambda _: Unsafe.raise_exception(ValueError("Should not success")),
        )
        .to_union()
    )


def test_valid() -> None:
    assert (
        Table.new(
            (_column_2, _column_1),
            FrozenDict({_column_1: _mock_type, _column_2: _mock_type}),
            frozenset([_column_2]),
        )
        .alt(Unsafe.raise_exception)
        .to_union()
    )
