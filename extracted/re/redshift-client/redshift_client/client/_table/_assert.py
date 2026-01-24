from fa_purity import (
    FrozenList,
    Maybe,
    Result,
    ResultE,
    ResultFactory,
    cast_exception,
)
from fa_purity.json import (
    JsonPrimitiveUnfolder,
)

from redshift_client import (
    _utils,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
)
from redshift_client.core.data_type.decode import (
    TypeDecoder,
)
from redshift_client.core.id_objs import (
    Identifier,
)
from redshift_client.sql_client import (
    DbPrimitive,
)


def _decode_str(value: DbPrimitive) -> ResultE[str]:
    return value.map(
        lambda p: JsonPrimitiveUnfolder.to_str(p),
        lambda _: Result.failure(
            TypeError("Expected `JsonPrimitive` but got `datetime`"),
            str,
        ).alt(cast_exception),
    )


def _decode_opt_int(value: DbPrimitive) -> ResultE[Maybe[int]]:
    factory: ResultFactory[Maybe[int], Exception] = ResultFactory()
    return value.map(
        lambda p: JsonPrimitiveUnfolder.to_opt_int(p).map(
            lambda v: Maybe.from_optional(v),
        ),
        lambda _: factory.failure(
            TypeError("Expected `JsonPrimitive` but got `datetime`"),
        ),
    )


def to_column(
    raw: FrozenList[DbPrimitive],
) -> ResultE[tuple[ColumnId, Column]]:
    _name = _utils.get_index(raw, 1).bind(_decode_str)
    _type = _utils.get_index(raw, 2).bind(_decode_str)
    _precision = _utils.get_index(raw, 3).bind(_decode_opt_int)
    _scale = _utils.get_index(raw, 4).bind(_decode_opt_int)
    _nullable = _utils.get_index(raw, 5).bind(_decode_str).map(lambda v: v.upper() == "YES")
    _default = _utils.get_index(raw, 6)
    _decoder = TypeDecoder.with_default_aliases()
    _data_type = _type.bind(
        lambda t: _precision.bind(
            lambda p: _scale.bind(lambda s: _decoder.decode_type(t, p, s)),
        ),
    )
    _column = _data_type.bind(
        lambda dt: _nullable.bind(
            lambda n: _default.map(lambda d: Column(dt, n, d)),
        ),
    )
    return _name.bind(
        lambda n: _column.map(lambda c: (ColumnId(Identifier.new(n)), c)),
    )
