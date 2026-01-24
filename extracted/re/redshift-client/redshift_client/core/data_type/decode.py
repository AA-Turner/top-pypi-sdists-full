from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

from fa_purity import (
    Coproduct,
    FrozenDict,
    Maybe,
    ResultE,
    cast_exception,
)

from redshift_client.core.data_type.alias import (
    NON_STC_ALIAS_MAP,
    STC_ALIAS_MAP,
)
from redshift_client.core.data_type.core import (
    DataType,
    DecimalType,
    NonStcDataTypes,
    PrecisionType,
    PrecisionTypes,
    ScaleTypes,
    StaticTypes,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def _get_enum(cast: Callable[[_T], _R], val: _T) -> Maybe[_R]:
    try:
        return Maybe.some(cast(val))
    except ValueError:
        return Maybe.empty()


@dataclass(frozen=True)
class TypeDecoder:
    static_aliases: FrozenDict[str, DataType]
    non_static_aliases: FrozenDict[str, NonStcDataTypes]

    def decode_static(self, raw: str) -> ResultE[DataType]:
        _raw = raw.upper()
        from_alias = Maybe.from_optional(self.static_aliases.get(_raw))
        std_type = lambda: _get_enum(StaticTypes, _raw).map(DataType)
        return (
            from_alias.lash(std_type)
            .to_result()
            .alt(lambda _: ValueError(f"`{raw}` is not an static type"))
        )

    def decode_non_static_type(self, raw: str) -> ResultE[NonStcDataTypes]:
        _raw = raw.upper()
        from_alias = Maybe.from_optional(self.non_static_aliases.get(_raw))
        from_precision: Callable[
            [],
            Maybe[NonStcDataTypes],
        ] = lambda: _get_enum(PrecisionTypes, _raw).map(
            lambda p: NonStcDataTypes(Coproduct.inl(p)),
        )
        from_scale = lambda: _get_enum(ScaleTypes, _raw).map(
            lambda p: NonStcDataTypes(Coproduct.inr(p)),
        )
        return (
            from_alias.lash(lambda: from_precision().lash(from_scale))
            .to_result()
            .alt(lambda _: ValueError(f"`{raw}` is not an non-static type"))
        )

    def decode_non_static(
        self,
        raw: str,
        precision: Maybe[int],
        scale: Maybe[int],
    ) -> ResultE[DataType]:
        require_precision = (
            precision.to_result().alt(lambda _: ValueError("precision is None")).alt(cast_exception)
        )
        require_scale = (
            scale.to_result().alt(lambda _: ValueError("scale is None")).alt(cast_exception)
        )
        return self.decode_non_static_type(raw).bind(
            lambda t: t.value.map(
                lambda p: require_precision.map(
                    lambda precision: PrecisionType(p, precision),
                ).map(DataType),
                lambda _: require_precision.bind(
                    lambda precision: require_scale.map(
                        lambda scale: DecimalType(precision, scale),
                    ),
                ).map(DataType),
            ),
        )

    def decode_type(
        self,
        raw: str,
        precision: Maybe[int],
        scale: Maybe[int],
    ) -> ResultE[DataType]:
        _raw = raw.upper()
        return self.decode_static(_raw).lash(
            lambda _: self.decode_non_static(_raw, precision, scale),
        )

    @staticmethod
    def with_default_aliases() -> TypeDecoder:
        return TypeDecoder(
            STC_ALIAS_MAP,
            NON_STC_ALIAS_MAP,
        )
