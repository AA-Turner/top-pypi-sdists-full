from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)

from fa_purity._core.coproduct import (
    UnionFactory,
)
from fa_purity._core.result import (
    Result,
    ResultE,
)
from fa_purity._core.utils import (
    cast_exception,
)
from fa_purity.json._core.primitive import (
    JsonPrimitive,
    Primitive,
)


@dataclass(frozen=True)
class JsonPrimitiveUnfolder:
    """Common transforms to unfold `JsonPrimitive` objects."""

    @staticmethod
    def to_str(item: JsonPrimitive) -> ResultE[str]:
        fail: ResultE[str] = Result.failure(
            TypeError("Unfolded `JsonPrimitive` is not `str`"),
            str,
        ).alt(cast_exception)
        return item.map(
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_int(item: JsonPrimitive) -> ResultE[int]:
        fail: ResultE[int] = Result.failure(
            TypeError("Unfolded `JsonPrimitive` is not `int`"),
            int,
        ).alt(cast_exception)
        return item.map(
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_float(item: JsonPrimitive) -> ResultE[float]:
        fail: ResultE[float] = Result.failure(
            TypeError("Unfolded `JsonPrimitive` is not `float`"),
            float,
        ).alt(cast_exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_decimal(item: JsonPrimitive) -> ResultE[Decimal]:
        fail: ResultE[Decimal] = Result.failure(
            TypeError("Unfolded `JsonPrimitive` is not `Decimal`"),
            Decimal,
        ).alt(cast_exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_bool(item: JsonPrimitive) -> ResultE[bool]:
        fail: ResultE[bool] = Result.failure(
            TypeError("Unfolded `JsonPrimitive` is not `bool`"),
            bool,
        ).alt(cast_exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
            lambda: fail,
        )

    @staticmethod
    def to_none(item: JsonPrimitive) -> ResultE[None]:
        fail: ResultE[None] = Result.failure(
            TypeError("Unfolded `JsonPrimitive` is not `None`"),
            type(None),
        ).alt(cast_exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda: Result.success(None),
        )

    @classmethod
    def to_opt_str(cls, item: JsonPrimitive) -> ResultE[str | None]:
        factory: UnionFactory[str, None] = UnionFactory()
        return cls.to_str(item).map(factory.inl).lash(lambda _: cls.to_none(item).map(factory.inr))

    @classmethod
    def to_opt_int(cls, item: JsonPrimitive) -> ResultE[int | None]:
        factory: UnionFactory[int, None] = UnionFactory()
        return cls.to_int(item).map(factory.inl).lash(lambda _: cls.to_none(item).map(factory.inr))

    @classmethod
    def to_opt_float(cls, item: JsonPrimitive) -> ResultE[float | None]:
        factory: UnionFactory[float, None] = UnionFactory()
        return (
            cls.to_float(item).map(factory.inl).lash(lambda _: cls.to_none(item).map(factory.inr))
        )

    @classmethod
    def to_opt_decimal(cls, item: JsonPrimitive) -> ResultE[Decimal | None]:
        factory: UnionFactory[Decimal, None] = UnionFactory()
        return (
            cls.to_decimal(item).map(factory.inl).lash(lambda _: cls.to_none(item).map(factory.inr))
        )

    @classmethod
    def to_opt_bool(cls, item: JsonPrimitive) -> ResultE[bool | None]:
        factory: UnionFactory[bool, None] = UnionFactory()
        return cls.to_bool(item).map(factory.inl).lash(lambda _: cls.to_none(item).map(factory.inr))

    @staticmethod
    def to_raw(item: JsonPrimitive) -> Primitive:
        """Transform to raw primitive object."""

        def _cast(item: Primitive) -> Primitive:
            # cast used for helping mypy to infer the correct return type
            return item

        return item.map(
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda x: _cast(x),
            lambda: _cast(None),
        )
