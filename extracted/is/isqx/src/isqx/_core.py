from __future__ import annotations

import decimal
import math
import sys
from collections.abc import (
    Generator,
    Hashable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from dataclasses import dataclass, fields, replace
from decimal import Decimal
from fractions import Fraction
from functools import cache
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Final,
    Literal,
    NamedTuple,
    Protocol,
    SupportsAbs,
    SupportsFloat,
    Union,
    final,
    get_args,
    get_origin,
    get_type_hints,
    overload,
    runtime_checkable,
)

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias

    slots: dict[str, bool] = {}
else:
    from typing import TypeAlias

    slots: dict[str, bool] = {"slots": True}

if sys.version_info < (3, 11):
    from typing import NoReturn

    def assert_never(arg: NoReturn) -> NoReturn:
        raise AssertionError("expected code to be unreachable")
else:
    from typing import assert_never

if TYPE_CHECKING:
    from ._fmt import Formatter, _FormatSpec


@runtime_checkable
class SupportsDecimal(SupportsFloat, SupportsAbs[object], Protocol):
    def to_decimal(self, ctx: decimal.Context) -> Decimal: ...


ExprKind: TypeAlias = Literal["dimensionless", "unit", "dimension"]
Number: TypeAlias = Union[SupportsDecimal, Decimal, Fraction, float, int]
_ARGS_NUMBER = get_args(Number)
Name: TypeAlias = str
"""A unique slug to identify the expression. This is used by the default basic
formatter to display the expression and hence should not contain any spaces
to avoid ambiguity. For example, `meter`, `newton`, `reynolds`"""


@runtime_checkable
class Named(Protocol):
    name: Name


# NOTE: these mixins are separate from ExprBase because:
# - the `Alias` expression cannot wrap itself
# - all expressions are formattable, but in the future we also want `QtyKind`
#   (not an ExprBase) to be formattable.


class AliasMixin:
    def alias(self, name: Name, *, allow_prefix: bool = False) -> Aliased:
        """Wrap this expression with a name.

        :param name: Name of this alias, e.g. `newton`
        :param allow_prefix: Whether to allow [prefixes][isqx.Prefix] to be
        attached. This should only be true for some units like `liter`
        """
        return Aliased(self, name=name, allow_prefix=allow_prefix)  # type: ignore


class FormatMixin:
    def __format__(self, fmt: _FormatSpec | str | Formatter) -> str:
        from ._fmt import fmt as format_

        return format_(self, formatter=fmt)  # type: ignore

    def __str__(self) -> str:
        return self.__format__("basic")


class ExprBase(FormatMixin):
    """A base class for a "unit-like" expression.

    It may be of the following forms:

    | Type                                       | Example                   |
    | ------------------------------------------ | ------------------------- |
    | [dimensionless number][isqx.Dimensionless]¹ | `Reynolds`, `Prandtl`     |
    | [base dimension][isqx.BaseDimension]¹       | [length][isqx.DIM_LENGTH]  |
    | [base unit][isqx.BaseUnit]¹                 | [meter][isqx.M]            |
    | [expression raised to a power][isqx.Exp]²   | `Exp(M, 2)`               |
    | [product of expressions][isqx.Mul]²         | `Mul(A, S)`               |
    | [scaled expression][isqx.Scaled]²⁴          | `Scaled(M, 0.3048)`       |
    | [aliased][isqx.Aliased]¹                    | [newton][isqx.N] = kg m s⁻²|
    | [translated expression][isqx.Translated]³   | `Translated(K, -273.15)`  |
    | [logarithmic expression][isqx.Log]¹³        | [dB][isqx.DB]              |
    | [tagged][isqx.Tagged]⁵                      | true vs ground speed      |

    ¹ these expressions are associated with a [name][isqx.NamedExpr].
    ² these expressions can be [aliased with a name][isqx.Aliased].
    ³ these expressions are *terminal*, meaning it cannot be further
      [exponentiated][isqx.Exp], [multiplied][isqx.Mul], [scaled][isqx.Scaled],
      [translated][isqx.Translated] or [aliased][isqx.Aliased] to form a more
      complex expression. However, it can be further [tagged][isqx.Tagged]
      (e.g. surface temperature vs ISA temperature).
    ⁴ can be created by multiplying a [prefix][isqx.Prefix] (e.g. `milli`)
    ⁵ can be created by calling a [quantity kind][isqx.QtyKind] with a unit

    Operator overloading is provided for ergonomic expression construction.

    !!! note
        While dividing expressions is supported, it is strongly discouraged as
        it can lead to operator precedence ambiguity. For example, while Python
        interprets `J / KG / K` as `(J / KG) / K`, it is often clearer to
        represent it as `J * KG**-1 * K**-1`.
    """

    def __pow__(self, exponent: Exponent) -> Exp:
        return Exp(self, exponent)  # type: ignore

    @overload
    def __mul__(self, rhs: Expr) -> Mul: ...

    @overload
    def __mul__(self, rhs: LazyProduct | Number) -> Scaled: ...

    # NOTE: not allowing Prefix as rhs to avoid confusion
    def __mul__(self, rhs: Expr | LazyProduct | Number) -> Mul | Scaled:
        if isinstance(
            rhs, (LazyProduct, SupportsDecimal, Decimal, Fraction, float, int)
        ):
            return Scaled(self, rhs)  # type: ignore
        # make sure KG * M * S becomes flat, not Mul((Mul((KG, M)), S))
        terms_self = self.terms if isinstance(self, Mul) else (self,)
        terms_other = rhs.terms if isinstance(rhs, Mul) else (rhs,)
        return Mul(tuple([*terms_self, *terms_other]))

    def __rmul__(self, lhs: LazyProduct | Number | Prefix) -> Scaled:
        if isinstance(lhs, Prefix):
            return lhs.mul(self)  # type: ignore
        return Scaled(self, lhs)  # type: ignore

    @overload
    def __truediv__(self, rhs: Expr) -> Mul: ...

    @overload
    def __truediv__(self, rhs: LazyProduct | Number) -> Scaled: ...

    def __truediv__(self, rhs: Expr | LazyProduct | Number) -> Mul | Scaled:
        if not isinstance(
            rhs, (LazyProduct, SupportsDecimal, Decimal, Fraction, float, int)
        ):
            return self * rhs**-1

        return Scaled(
            self,  # type: ignore
            LazyProduct(tuple(f for f in _products_inverse(rhs))),
        )  # M / 2 => Scaled(M, Fraction(1, 2))

    def __getitem__(self, tags: tuple[Tag, ...] | Tag) -> Tagged:
        """Attach tags to this expresson."""
        t = tags if isinstance(tags, tuple) else (tags,)
        if isinstance(self, Tagged):
            return Tagged(self.reference, self.tags + t)
        return Tagged(self, t)  # type: ignore


# all expressions should be immutable. helper functions like `kind`, `dimension`
# simplify etc. rely on this fact to cache results.
@dataclass(frozen=True, **slots)
class Dimensionless(Named, ExprBase):
    name: Name
    """Name for the dimensionless number, e.g. `reynolds`, `prandtl`"""


@dataclass(frozen=True, **slots)
class BaseDimension(Named, ExprBase):
    name: Name
    """Name for the base dimension, e.g. `L`, `M`, `T`"""


@dataclass(frozen=True, **slots)
class BaseUnit(Named, ExprBase):
    _dimension: BaseDimension
    """Reference to the base dimension"""
    name: Name
    """Name for the unit, e.g. `m`, `kg`, `s`"""


Exponent: TypeAlias = Union[int, Fraction]
"""An exponent, generally small integers, which can be positive, negative,
or a fraction, but not zero"""


@dataclass(frozen=True, **slots)
class Exp(AliasMixin, ExprBase):
    """An expression raised to an exponent.
    For example, `BaseUnit("meter", Dimension("L")), 2)` is m².
    Can be recursively nested, e.g. `Exp(Exp(METER, 2), Fraction(1, 2))`
    """

    base: _ComposableExpr
    exponent: Exponent
    """Exponent. Avoid using zero to represent dimensionless numbers: 
    use [`isqx.Dimensionless`][] with a name instead."""

    def __post_init__(self) -> None:
        if not isinstance(self.exponent, (int, Fraction)):
            raise CompositionError(
                outer=Exp,
                inner=self.exponent,
                msg=(
                    "exponent must be an integer or a fraction, "
                    f"not {type(self.exponent).__name__}."
                ),
            )
        if self.exponent == 0:
            raise CompositionError(
                outer=Exp,
                inner=self.exponent,
                msg="exponent must not be zero.",
                help="use `Dimensionless` to represent a dimensionless quantity.",
            )
        ref = _unwrap_tagged_or_aliased(self.base)
        if isinstance(ref, Translated):
            raise CompositionError(
                outer=Exp,
                inner=ref,
                msg="translated units (like ℃) are terminal and cannot be exponentiated.",
                help=(
                    "did you mean to exponentiate its "
                    f"absolute reference `{ref.reference}` instead?"
                ),
            )  # prevent ℃². J ℃⁻¹ should be written as J K⁻¹


@dataclass(frozen=True, **slots)
class Mul(AliasMixin, ExprBase):
    """Products of powers of an expression."""

    terms: tuple[_ComposableExpr, ...]
    """A tuple of expressions to be multiplied, preserving the order."""

    def __post_init__(self) -> None:
        if not self.terms:
            raise CompositionError(
                outer=Mul,
                inner=self.terms,
                msg="`Mul` terms must not be empty.",
                help="use `Dimensionless` to represent a dimensionless quantity.",
            )
        current_kind: ExprKind | None = None
        for term in self.terms:
            ref = _unwrap_tagged_or_aliased(term)
            if isinstance(ref, Translated):
                raise CompositionError(
                    outer=Mul,
                    inner=ref,
                    msg="`Translated` units (like ℃) are terminal and cannot be part of a product.",
                    help=f"use its absolute reference `{ref.reference}` instead.",
                )  # prevent ℃ * ℃
            k = kind(term)
            if current_kind is None and k != "dimensionless":
                current_kind = k
            elif current_kind != k and k != "dimensionless":
                raise MixedKindError(terms=self.terms)  # prevent time * seconds


@dataclass(frozen=True, **slots)
class Scaled(AliasMixin, ExprBase):
    reference: BaseUnit | Exp | Mul | Scaled | Aliased | Tagged | Log
    """The unit or dimension that this unit or dimension is based on."""
    factor: Number | LazyProduct | Prefix
    """The exact factor to multiply to this unit to convert it to the reference.
    For example, `1 ft = 0.3048 m`, so the factor is 0.3048.
    """

    def __post_init__(self) -> None:
        if not isinstance(
            self.factor,
            (
                LazyProduct,
                SupportsDecimal,
                Decimal,
                Fraction,
                float,
                int,
                Prefix,
            ),
        ):
            raise CompositionError(
                outer=Scaled,
                inner=self.factor,
                msg=f"factor must be a number, not {type(self.factor).__name__}.",
            )
        ref = _unwrap_tagged_or_aliased(self.reference)
        if isinstance(ref, Translated):
            raise CompositionError(
                outer=Scaled,
                inner=self.reference,
                msg=f"`{type(self.factor).__name__} cannot be scaled.",
            )  # prevent 13 * ℃
        # TODO: prevent BaseDimension from being scaled


@dataclass(frozen=True, **slots)
class Log(AliasMixin, ExprBase):
    """The logarithm of a dimensionless expression [ISO 80000-2:2019 2-13.4]."""

    reference: Dimensionless | Tagged
    """A dimensionless expression"""
    # NOTE: while we should support Exp: log(a^b) = b * log(a), the latter is actually the more "simple" version
    # NOTE: we should also support Mul: log(a * a**-1) is fine, but again we must simplify before we know if its really dimensionless.
    base: Number
    """The base of the logarithm, e.g. 10 for bel, e for neper."""

    def __post_init__(self) -> None:
        ref = self.reference
        is_valid_ref = isinstance(ref, Dimensionless) or (
            isinstance(ref, Tagged) and isinstance(ref.reference, Dimensionless)
        )
        if not is_valid_ref:
            raise CompositionError(
                outer=Log,
                inner=ref,
                msg="`Log` can only wrap a `Dimensionless` expression",
                help="use the `isqx.ratio()` helper for logarithmic units like dB.",
            )


@dataclass(frozen=True, **slots)
class Aliased(Named, ExprBase):
    """An alias for an expression, used to give a more readable name.

    Note that unlike a [tagged][isqx.Tagged] expression,
    [simplification][isqx.simplify] will effectively elide this class.
    """

    reference: Exp | Mul | Scaled | Tagged | Log
    """Expression to be aliased, e.g. `Mul((KG, M, Exp(S, -2)))`"""
    name: Name
    """Name of this alias, e.g. `newton`"""
    allow_prefix: bool = False
    """Whether to allow [prefixes][isqx.Prefix] to be attached.
    This should only be true for some units like `liter`."""

    def __post_init__(self) -> None:
        if not isinstance(
            ref := self.reference, (Exp, Mul, Scaled, Tagged, Log)
        ):
            raise CompositionError(
                outer=Aliased,
                inner=ref,
                msg="`Aliased` can only wrap an `Exp`, `Mul`, `Scaled`, `Tagged`, or `Log` expression.",
            )


@dataclass(frozen=True, **slots)
class Translated(Named, ExprBase):
    """An expression offsetted from some reference unit."""

    reference: BaseUnit | Scaled | Aliased | Tagged
    """The expression that this expression is based on (e.g., `K` for `DEGC`)"""
    offset: Number
    """The exact offset to add to the reference to get this unit.
    For example, `℃ = K - 273.15`, so the offset is -273.15."""
    name: Name

    def __post_init__(self) -> None:
        ref = _unwrap_tagged_or_aliased(self.reference)
        if isinstance(ref, Translated):
            raise CompositionError(
                outer=Translated,
                inner=ref,
                msg="nesting `Translated` expressions is not allowed.",
            )
        if not isinstance(ref, (BaseUnit, Scaled)):
            raise CompositionError(
                outer=Translated,
                inner=ref,
                msg="`Translated` must have a `BaseUnit` or `Scaled` expression as its reference.",
            )


@dataclass(frozen=True, **slots)
class Tagged(AliasMixin, ExprBase):
    """An expression decorated with one of more semantic context tag.

    Similar to how:

    - `Annotated[T, M1, M2, ...]` attaches metadata to some type `T`,
    - `expr[C1, C2, ...]` attaches context to an [expression][isqx.Expr].

    This allows one to "disambiguate" between quantities that share the same
    physical dimension, but have different meanings, e.g.
    geopotential altitude vs. geometric altitude.
    """

    reference: _TaggedAllowedExpr
    tags: tuple[Tag, ...]

    def __post_init__(self) -> None:
        if isinstance(self.reference, Tagged):
            raise CompositionError(
                outer=Tagged,
                inner=self.reference,
                msg="nesting `Tagged` expressions is not allowed. use the `unit[tags]` syntax.",
            )
        for tag in self.tags:
            if isinstance(tag, HasTagValidation):
                tag.__validate_tag__(self.reference, self.tags)


@runtime_checkable
class HasTagValidation(Hashable, Protocol):
    def __validate_tag__(
        self,
        reference: Expr,
        tags: tuple[Tag, ...],
    ) -> None:
        """Check that this tag can be applied to the given expression.

        For example, this can be used to ensure:

        - `decibel` (log level) with log reference unit `voltage` but not
        - `reynolds number` with log reference unit `voltage`.

        :param reference: The expression to apply the tags to.
        :param tags: The tags being applied to the expression.
            This can be used to enforce complex rules (e.g. no duplicates)
        :raises CompositionError: if the tag cannot be applied to the expression
        """
        ...


# using sealed unions instead of ExprBase to facilitate static type checking
Expr: TypeAlias = Union[
    Dimensionless,
    BaseDimension,
    BaseUnit,
    Exp,
    Mul,
    Scaled,
    Aliased,
    Translated,
    Log,
    Tagged,
]
_ARGS_EXPR = get_args(Expr)
NamedExpr: TypeAlias = Union[
    Dimensionless, BaseDimension, BaseUnit, Aliased, Translated
]
_TaggedAllowedExpr: TypeAlias = Union[
    Dimensionless,
    BaseDimension,
    BaseUnit,
    Exp,
    Mul,
    Scaled,
    Aliased,
    Translated,
    Log,
]  # avoid nesting tags
_ComposableExpr: TypeAlias = Union[
    Dimensionless,
    BaseDimension,
    BaseUnit,
    Exp,
    Mul,
    Scaled,
    Aliased,
    Tagged,
    Log,  # dB/m and dB/Hz should be allowed, though with extra care in conversion
]  # avoid terminal (translated) from being further composed
PhysicalUnit: TypeAlias = Union[
    BaseUnit, Exp, Mul, Scaled, Aliased, Tagged
]  # for use in relative

#
# other objects that are not expressions but key to the system
#


@dataclass(frozen=True, **slots)
class Prefix:
    """A prefix, which when multiplied by a [base unit][isqx.BaseUnit] or
    [aliased unit][isqx.Aliased], returns a [scaled unit][isqx.Scaled].

    Note that this is not an [`isqx.Expr`][].
    """

    value: Number
    name: str
    """Name of this prefix, e.g. `milli`, `kibi`"""

    def mul(self, rhs: BaseUnit | Aliased | Tagged) -> Scaled:
        if not isinstance(rhs, (BaseUnit, Aliased, Tagged)):
            raise CompositionError(
                outer=Scaled,
                inner=rhs,
                msg=f"prefixes cannot be applied to `{type(rhs).__name__}`.",
            )  # this will prevent double prefixing

        if isinstance(rhs, BaseUnit):
            if rhs.name == "kilogram":
                raise CompositionError(
                    outer=Scaled,
                    inner=rhs,
                    msg="cannot prefix `kilogram`.",
                    help="apply the prefix to `gram` instead.",
                )
        elif isinstance(rhs, Aliased):
            if not rhs.allow_prefix:
                raise CompositionError(
                    outer=Scaled,
                    inner=rhs,
                    msg=f"The aliased unit `{rhs.name}` does not allow prefixes.",
                )
            if self.name == "kilo" and rhs.name == "gram":
                raise CompositionError(
                    outer=Scaled,
                    inner=rhs,
                    msg="cannot apply prefix `kilo` to `gram`.",
                    help="use the `KG` unit directly.",
                )
        elif isinstance(rhs, Tagged) and not isinstance(
            (ref := _unwrap_tagged_or_aliased(rhs)),
            (BaseUnit, Aliased),
        ):
            raise CompositionError(
                outer=Scaled,
                inner=rhs,
                msg="prefixes cannot be applied to this type of tagged expression.",
                help=f"the inner reference is `{type(ref).__name__}`, which cannot be prefixed.",
            )
        # TODO: robustly handle Scaled(Log())
        return Scaled(rhs, self)


@dataclass(frozen=True, **slots)
class QtyKind:
    r"""An abstract *kind of quantity* (ISO 80000-1) represents a "concept" (e.g.
    speed) *without* a specific unit tied to it.

    When called with a unit, it becomes a [concrete unit with tagged
    context][isqx.Tagged].
    """

    unit_si_coherent: _TaggedAllowedExpr
    """The coherent SI unit (i.e. no conversion factors involved, e.g.
    `M_PERS` for speed, not `KM_PERHOUR`)"""
    tags: tuple[Tag, ...] | None = None

    def si_coherent(self) -> Expr:
        """Return the SI coherent unit with tags."""
        if self.tags is None:
            return self.unit_si_coherent
        return self.unit_si_coherent[self.tags]

    def __getitem__(self, tags: tuple[Tag, ...] | Tag) -> QtyKind:
        """Attach additional tags to this quantity kind."""
        t = tags if isinstance(tags, tuple) else (tags,)
        if self.tags is not None:
            t = self.tags + t
        return replace(self, tags=t)

    def __call__(self, unit: _TaggedAllowedExpr) -> Expr:
        """Create a tagged unit from this quantity kind."""
        if unit is self.unit_si_coherent:
            return self.si_coherent()

        dim_unit = dimension(simplify(unit))
        dim_unit_self = dimension(simplify(self.unit_si_coherent))
        if dim_unit != dim_unit_self:
            raise UnitKindMismatchError(self, unit, dim_unit_self, dim_unit)
        if self.tags is None:
            return unit
        return unit[self.tags]


#
# special tags
# mathematical concepts [ISO 80000-2]
#


@dataclass(frozen=True, **slots)
class _Delta(HasTagValidation):
    """A tag to indicate the quantity as an interval or a difference, (a vector
    in affine space), rather than a particular point on the scale.

    It is independent of a specific origin alone, but when combined with
    [`isqx.OriginAt`][] it can represent a "deviation relative to a specific
    point on the scale".
    """

    kind: Literal["finite", "differential", "inexact_differential"] = "finite"

    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        _check_duplicate_tags(self, tags)

    # while frozen=True adds the hash, we define our own __hash__ because:
    # - py310's abc.Hashable checks before the dataclass decorator is applied
    # - mypy doesn't understand that frozen=True creates __hash__ dynamically
    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.kind))


DELTA = _Delta("finite")
r"""A tag to indicate a finite change in a quantity $\Delta Q$.

Example: [duration in time][isqx.DURATION]"""
DIFFERENTIAL = _Delta("differential")
r"""A tag to indicate an exact differential $dQ$ (whose integral is
path-independent).

Example: [volume element][isqx.VOLUME_ELEMENT]"""
INEXACT_DIFFERENTIAL = _Delta("inexact_differential")
r"""A tag to indicate an inexact differential $\delta Q$ (whose integral is
path-dependent).

Example: [inexact differential in heat][isqx.INEXACT_DIFFERENTIAL_HEAT]"""


# TODO: Substance (water), Solute, Solution
# TODO: StateOfMatter (solid, liquid, gas, plasma, different allotropes...)
# TODO: vacuum?


@dataclass(frozen=True, **slots)
class Quantity:
    """A simple data container for a value and its unit, for use in
    specifying the [origin of a point on the scale][isqx.OriginAt].

    !!! warning
        This is not an [`isqx.Expr`][] should not be further composed.
    """

    value: Number | LazyProduct
    unit: PhysicalUnit


@dataclass(frozen=True, **slots)
class OriginAt(HasTagValidation):
    """A tag to specify the origin for a point on the scale. Commonly combined
    with [`isqx.DELTA`][] to also represent a change in the quantity.

    Examples:

    - Unix epoch: `S[OriginAt("unix epoch")]`
    - difference in actual temperature and ISA temperature:
      `K[DELTA, OriginAt((15, CELSIUS))]`
    - difference in pressure: `Pa[DELTA, OriginAt((100, PSI))]`
    """

    location: Quantity | Hashable
    """The location of the "zero point" of the measurement.

    Can be a quantity (value + unit, e.g. `(100, PSI)`) or simply a hashable
    object (e.g. the string "unix epoch"). Hashable objects are useful for
    scenarios where the origin itself is contextual, for example:

    - the height above the ground is dependent on the geographic location
    - the stock price relative to yesterday's close
    - time elapsed relative to the engine ignition
    """

    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        if (
            isinstance(q := self.location, Quantity)
            and not isinstance(reference, Dimensionless)
            and q.unit != reference
        ):
            raise CompositionError(
                outer=OriginAt,
                inner=reference,
                msg=(
                    f"expression {reference} is not compatible with "
                    f"`OriginAt.location` of unit {q.unit}"
                ),
                help=f"`OriginAt.location` must be of unit {reference}",
            )
        _check_duplicate_tags(self, tags)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.location))


# TODO: add tag `AtCondition` (Delta pressure = 0, temperature = 293.15 K)
# TODO: add tag `Rotation`? clockwise/counterclockwise
# TODO: add tag `Direction`? into/out of system

_RATIO = Dimensionless("ratio")


def ratio(numerator: Expr, denominator: Expr | Quantity) -> Tagged:
    """Returns a dimensionless between two expressions of the same dimension.

    The denominator can be a [quantity (value + unit)][isqx.Quantity] to
    represent logarithmic units like [`isqx.DBW`][].

    See: https://en.wikipedia.org/wiki/Dimensionless_quantity#Ratios,_proportions,_and_angles"""
    return _RATIO[_RatioBetween(numerator, denominator)]


@dataclass(frozen=True, **slots)
class _RatioBetween(HasTagValidation):
    numerator: Expr
    denominator: Expr | Quantity

    def __post_init__(self) -> None:
        # TODO: enforce dimensionless:
        # we abuse numerator * (denominator.value * denominator.unit)**-1
        # and check we indeed get dimensionless or scaled dimensionless.
        pass

    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        if reference is not _RATIO:
            raise CompositionError(
                outer=_RatioBetween,
                inner=reference,
                msg="`RatioBetween` tag can only be applied to a ratio.",
                help="use the `isqx.ratio()` helper function.",
            )
        _check_duplicate_tags(self, tags)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.numerator, self.denominator))


@dataclass(frozen=True, **slots)
class _Tensor(HasTagValidation):
    rank: int

    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        _check_duplicate_tags(self, tags)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.rank))


# NOTE: `var: Annotated[T, x]` can be interpreted as "the numerical value of
# `var` is a measurement on the scale `x`". If `T` is a float, then it is a
# scalar; if `T` is numpy array, it can be a tensor.
# Use `_Tensor` to indicate that the quantity *can*, but does not have to,
# be a tensor.
VECTOR = _Tensor(rank=1)
"""A tag to indicate that the quantity can be a vector.
[ISO 80000-2:2019 2-18.1]. It is not restricted to three dimensions.

Examples:

- velocity vector: `M_PERS[VECTOR]`
- force vector: `F[VECTOR]`"""
TENSOR_SECOND_ORDER = _Tensor(rank=2)
"""A tag to indicate that the quantity can be a second-order tensor.

Examples:

- stress tensor: `(N * M**-2)["stress", TENSOR_SECOND_ORDER]`"""


@dataclass(frozen=True, **slots)
class _CoordinateSystem(HasTagValidation, Named):
    name: Literal["cartesian", "spherical", "cylindrical"] | str
    # NOTE: allowing arbitrary names for now because different game engines
    # don't agree to one (also ENU, NED...)

    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        _check_duplicate_tags(self, tags)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.name))


# coordinate systems, TODO: left handed systems.
CARTESIAN = _CoordinateSystem(name="cartesian")
r"""A tag to indicate that the quantity is expressed in Cartesian coordinates
($x$, $y$, $z$) [ISO 80000-2:2019 2-17.1].

The position vector is $\mathbf{r} = x \mathbf{e}_x + y \mathbf{e}_y +
z \mathbf{e}_z$, and its differential is $d\mathbf{r} = dx \mathbf{e}_x +
dy \mathbf{e}_y + dz \mathbf{e}_z$.
"""
CYLINDRICAL = _CoordinateSystem(name="cylindrical")
r"""A tag to indicate that the quantity is expressed in cylindrical coordinates
(radial distance $\rho$, azimuth $\varphi$, axial coordinate or height $z$)
[ISO 80000-2:2019 2-17.2].

The position vector is $\mathbf{r} = \rho \mathbf{e}_\rho(\varphi) +
z \mathbf{e}_z$, and its differential is $d\mathbf{r} =
d\rho \mathbf{e}_\rho(\varphi) + \rho d\varphi \mathbf{e}_\varphi(\varphi) +
dz \mathbf{e}_z$.

If $z = 0$, it is equivalent to polar coordinates.
"""
SPHERICAL = _CoordinateSystem(name="spherical")
r"""A tag to indicate that the quantity is expressed in spherical coordinates
(radial distance $r$, polar angle $\theta$, azimuthal angle $\varphi$)
[ISO 80000-2:2019 2-17.3].

The position vector is $\mathbf{r} = r \mathbf{e}_r(\theta, \varphi)$,
and its differential is $d\mathbf{r} = dr \mathbf{e}_r(\theta, \varphi) +
r d\theta \mathbf{e}_\theta(\theta, \varphi) + r \sin(\theta) d\varphi
\mathbf{e}_\varphi(\theta, \varphi)$.
"""

# TODO: while it is tempting to add a tag that "constrains" the quantity to be
# greater than zero, much like `annotated_types.Gt`, we need to be very careful
# because some quantities can be negative, e.g.
# negative thermodynamic temperatures or altitudes below sea level.
# https://github.com/mpusz/mp-units/issues/468


@dataclass(frozen=True, **slots)
class _Complex(HasTagValidation):
    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        _check_duplicate_tags(self, tags)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)


COMPLEX = _Complex()
"""A tag to indicate that the quantity is complex-valued."""


# iso/iec 80000-specific
@dataclass(frozen=True, **slots)
class PhotometricCondition(HasTagValidation):
    """Photometric condition [ISO 80000-7]. Can be:

    - [Photopic vision (cones in human vision, in daylight)](https://en.wikipedia.org/wiki/Photopic_vision)
    - [Scotopic vision (rods in human vision, at night)](https://en.wikipedia.org/wiki/Scotopic_vision)
    - [Mesopic/twilight vision (rods and cones in human vision)](https://en.wikipedia.org/wiki/Mesopic_vision)
    - CIE 1964 standard colorimetric observer (10° photopic photometric observer)
    - CIE 1988 modified 2° spectral luminous efficiency function for photopic vision
    - Any other custom condition.
    """

    kind: (
        Literal[
            "photopic",
            "scotopic",
            "mesopic",
            "photopic_cie_1964_10degree",
            "photopic_cie_1988_mod_2degree",
        ]
        | str
    )

    def __validate_tag__(self, reference: Expr, tags: tuple[Tag, ...]) -> None:
        _check_duplicate_tags(self, tags)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.kind))


def _check_duplicate_tags(
    tag: Tag,
    tags: tuple[Tag, ...],
) -> None:
    tag_type = type(tag)
    if sum(1 for t in tags if isinstance(t, tag_type)) > 1:
        raise CompositionError(
            outer=Tagged,
            inner=tag,
            msg=f"tag `{tag_type.__name__}` cannot be applied multiple times.",
        )


Tag: TypeAlias = Union[
    OriginAt,
    _RatioBetween,
    _Delta,
    _Tensor,
    _CoordinateSystem,
    _Complex,
    PhotometricCondition,
    HasTagValidation,
    Hashable,
]
"""A tag can be any hashable object (e.g. frozen dataclasses or strings)."""

#
# this ends the basic expression system used for documentation purposes.
# the rest of the code are *runtime* helpers that transform and manipulate
# the expressions.
#
# the `dimension` and `kind` helper is sometimes used in `__post_init__` to make
# invalid states unrepresentable. this comes with a minor performance
# penalty but is worth it.
#


@overload
def dimension(expr: Dimensionless) -> Dimensionless: ...
@overload
def dimension(expr: BaseDimension) -> BaseDimension: ...
@overload
def dimension(expr: BaseUnit) -> BaseDimension: ...
@overload
def dimension(expr: Exp) -> Exp: ...
@overload
def dimension(expr: Mul) -> Mul: ...
@overload
def dimension(expr: Log) -> Dimensionless: ...
@overload
def dimension(expr: Tagged) -> Tagged | Expr: ...
@overload
def dimension(expr: Aliased | Scaled | Translated) -> Expr: ...
@cache
def dimension(expr: Expr) -> Expr:
    """Return the dimension of this "unit-like" expression.
    Note that it does not perform simplification.

    Examples:

    - `Exp(M, 2)` -> `Exp(DIM_LENGTH, 2)`
    - `Mul(M, Exp(S, -1))` -> `Mul(DIM_LENGTH, Exp(DIM_TIME, -1))`
    """
    if isinstance(expr, (Dimensionless, BaseDimension)):
        return expr
    if isinstance(expr, BaseUnit):
        return expr._dimension
    if isinstance(expr, (Aliased, Scaled, Translated)):
        return dimension(expr.reference)
    if isinstance(expr, Exp):
        return Exp(dimension(expr.base), expr.exponent)  # type: ignore
    if isinstance(expr, Mul):
        return Mul(tuple(dimension(term) for term in expr.terms))  # type: ignore
    if isinstance(expr, Tagged):
        ref_dim = dimension(expr.reference)
        # note: log level's dimension is always dimensionless
        # so we need to strip away tags that dont make any more sense
        tags = []
        for tag in expr.tags:
            if isinstance(tag, HasTagValidation):
                try:
                    tag.__validate_tag__(ref_dim, expr.tags)
                except CompositionError:
                    continue
            tags.append(tag)
        if not tags:
            return ref_dim
        return ref_dim[tuple(tags)]
    if isinstance(expr, Log):
        return Dimensionless(f"log_{repr(expr.reference)}")
    assert_never(expr)


@overload
def kind(expr: Dimensionless | Log) -> Literal["dimensionless"]: ...
@overload
def kind(expr: BaseDimension) -> Literal["dimension"]: ...
@overload
def kind(expr: BaseUnit) -> Literal["unit"]: ...
@overload
def kind(
    expr: Exp | Mul | Scaled | Aliased | Translated | Tagged,
) -> ExprKind: ...
@cache
def kind(expr: Expr) -> ExprKind:
    """Whether this expression is a unit, dimension, or dimensionless."""
    if isinstance(expr, Dimensionless):
        return "dimensionless"
    if isinstance(expr, BaseDimension):
        return "dimension"
    if isinstance(expr, BaseUnit):
        return "unit"
    if isinstance(expr, Exp):
        return kind(expr.base)
    if isinstance(expr, (Scaled, Aliased, Translated, Tagged)):
        return kind(expr.reference)
    if isinstance(expr, Mul):
        # all terms have a consistent underlying kind (unit/dimension)
        for term in expr.terms:
            term_kind = kind(term)
            if term_kind != "dimensionless":
                return term_kind
        return "dimensionless"
        # everything left are dimensionless to the power of something
    if isinstance(expr, Log):
        return "dimensionless"
    assert_never(expr)


#
# simplify
#


SimplifiedExpr: TypeAlias = Union[
    Dimensionless,
    BaseDimension,
    BaseUnit,
    Exp,
    Mul,
    Scaled,
    Translated,
    Log,
    Tagged,
]  # no Aliased


@overload
def simplify(expr: Dimensionless) -> Dimensionless: ...
@overload
def simplify(expr: BaseDimension) -> BaseDimension: ...
@overload
def simplify(expr: BaseUnit) -> BaseUnit: ...
@overload
def simplify(expr: Aliased) -> SimplifiedExpr: ...
@overload
def simplify(expr: Translated) -> Translated: ...
@overload
def simplify(expr: Log) -> Log: ...
@overload
def simplify(expr: Tagged) -> Tagged: ...
@overload
def simplify(
    expr: Exp | Mul | Scaled,
) -> Union[
    Dimensionless,
    BaseDimension,
    BaseUnit,
    Exp,
    Mul,
    Scaled,
    Translated,
]: ...
@cache
def simplify(expr: Expr) -> SimplifiedExpr:
    if isinstance(expr, (Dimensionless, BaseDimension, BaseUnit)):
        return expr
    if isinstance(expr, Aliased):
        return simplify(expr.reference)
    if isinstance(expr, Translated):
        return Translated(
            simplify(expr.reference),  # type: ignore
            expr.offset,
            expr.name,
        )
    if isinstance(expr, Tagged):
        return Tagged(simplify(expr.reference), expr.tags)  # type: ignore
    base_exponent_pairs: dict[SimplifiedExpr, Exponent] = {}
    scaled_conversions: list[tuple[Scaled, Exponent]] = []
    _decompose_expr(expr, 1, base_exponent_pairs, scaled_conversions)
    return _build_canonical_expr(base_exponent_pairs, scaled_conversions)


# migrate to pattern matching when we drop support for py3.9
def _decompose_expr(
    expr: Expr,  # ‾
    exponent: Exponent,  # *
    base_exponent_pairs_mut: MutableMapping[SimplifiedExpr, Exponent],
    scaled_conversions_mut: MutableSequence[tuple[Scaled, Exponent]],  # ^
) -> None:
    """Recursively traverse an expression tree to flatten it.

    This is the first step of the simplification, example:

    - expr=Mul(Scaled(M, 0.3048, "FT"), Exp(S, -1)), exponent=2
        - expr=Scaled(M, 0.3048, "FT"), exponent=2
            - scaled_conversions_mut += [(Scaled(M, 0.3048, "FT"), 2)]
            - expr=M, exponent=2
                - base_exponent_pairs_mut[M] += 2
        - expr=Exp(S, -1), exponent=2
            - expr=Expr(S, -2), exponent=1
                - base_exponent_pairs_mut[S] += -2
    """
    if isinstance(expr, Aliased):
        _decompose_expr(
            expr.reference,
            exponent,
            base_exponent_pairs_mut,
            scaled_conversions_mut,
        )
    elif isinstance(
        expr,
        (Dimensionless, BaseDimension, BaseUnit, Tagged, Translated, Log),
    ):
        # we hit a fundamental-like unit (we treat tagged as unique bases).
        # add its accumulated exponent
        base_exponent_pairs_mut.setdefault(expr, 0)
        base_exponent_pairs_mut[expr] += exponent
    elif isinstance(expr, Exp):
        # (xᵃ)ᵇ -> xᵃᵇ
        # ‾‾‾‾*    ‾**
        _decompose_expr(
            expr.base,
            expr.exponent * exponent,
            base_exponent_pairs_mut,
            scaled_conversions_mut,
        )
    elif isinstance(expr, Mul):
        # (xyᵃ)ᵇ -> xᵇyᵃᵇ
        # ‾‾‾‾‾*    ‾*‾**
        for term in expr.terms:
            _decompose_expr(
                term,
                exponent,
                base_exponent_pairs_mut,
                scaled_conversions_mut,
            )
    elif isinstance(expr, Scaled):
        # (kx)ᵇ -> kᵇxᵇ
        # ‾‾‾‾*    ^^‾*
        scaled_conversions_mut.append((expr, exponent))
        _decompose_expr(
            expr.reference,
            exponent,
            base_exponent_pairs_mut,
            scaled_conversions_mut,
        )
    else:
        assert_never(expr)


__DIMENSIONLESS_SIMPLIFIED: Final[Dimensionless] = Dimensionless(
    name="from_simplified"
)


def _build_canonical_expr(
    base_exponent_pairs: Mapping[SimplifiedExpr, Exponent],
    scaled_conversions: list[tuple[Scaled, Exponent]],
) -> SimplifiedExpr:
    """Construct a canonical expression from flattened parts.

    This is second step of the simpification. Examples:

    - `{}` and `[]` -> dimensionless
    - `{M: 1}` and `[]` -> `M`
    - `{M: 2}` and `[]` -> `Exp(M, 2)`
    - `{M: 1, S: -2}` and `[]` -> `Mul(M, Exp(S, -2))`
    - `{...}` and `[(Scaled(M, 0.3048, "FT"), 2)]` -> result will be wrapped:
      `Scaled(reference=Mul(..., factor=LazyProduct(...)`
    """
    no_conversions_involved = not scaled_conversions
    simplified_expr: Expr
    # remove zero exponents and ensure canonical order by names
    base_exponent_pairs_sorted = sorted(
        filter(lambda item: item[1] != 0, base_exponent_pairs.items()),
        key=lambda item: repr(item[0]),
    )
    if not base_exponent_pairs_sorted:
        simplified_expr = __DIMENSIONLESS_SIMPLIFIED
    elif len(base_exponent_pairs_sorted) == 1:
        base, exponent = base_exponent_pairs_sorted[0]
        simplified_expr = base if exponent == 1 else Exp(base, exponent)  # type: ignore
    else:
        simplified_expr = Mul(
            tuple(
                base if exponent == 1 else Exp(base, exponent)  # type: ignore
                for base, exponent in base_exponent_pairs_sorted
            )
        )
    if no_conversions_involved:
        return simplified_expr

    return Scaled(
        reference=simplified_expr,  # type: ignore
        factor=LazyProduct.from_derived_conversions(scaled_conversions),
    )


# TODO: in the future, we want a as_basis() function that accepts set[Expr]
# why: we sometimes want to re-express some unit not in MKS, but CGS.
# that will require linear algebra to solve the dimensional exponents but
# we're leaving that as optional and far in the future.

#
# converter
#


def _converter_new(
    scale: Number, offset: Number
) -> Converter | NonAffineConverter:
    # unless conversions involve celsius/fahrenheit/log units, non-affine
    # conversions are rare
    if not offset:
        return Converter(scale=scale)
    return NonAffineConverter(scale=scale, offset=offset)


@runtime_checkable
class SupportsConversion(Protocol):
    def __call__(self, value):  # type: ignore
        """Convert a value in the origin unit to the target unit.

        :param value: An `int`, `float`, [fractions.Fraction][],
            or any other numeric type^.

            ^ If the converter was created with `exact=True`, the `scale`
            will be fractions and thus may not be compatible with many numeric
            libraries (e.g. `fractions.Fraction * numpy.array` fails).
            [decimal.Decimal][] inputs should be converted into
            [fractions.Fraction][].
        """


@dataclass(frozen=True, **slots)
class Converter(SupportsConversion):
    scale: Number

    def __call__(self, value):  # type: ignore
        return self.scale * value


@dataclass(frozen=True, **slots)
class NonAffineConverter(SupportsConversion):
    scale: Number
    offset: Number

    def __call__(self, value):  # type: ignore
        return value * self.scale + self.offset


class _LogInfo(NamedTuple):
    k: Number | LazyProduct
    b: Number
    q_measured_unit: PhysicalUnit
    q_ref: Quantity
    other_tags: tuple[Tag, ...]


def _get_log_info(info: _ConversionInfo) -> _LogInfo | None:
    if not isinstance(info.expr, Log):
        return None
    log_expr = info.expr
    if not isinstance(log_expr.reference, Tagged):
        return None
    ratio_between_tag = None
    other_tags: list[Tag] = []
    for tag in log_expr.reference.tags:
        if isinstance(tag, _RatioBetween):
            ratio_between_tag = tag
        else:
            other_tags.append(tag)
    if ratio_between_tag is None or (
        not isinstance(ratio_between_tag.denominator, Quantity)
    ):
        # pH, pKa isn't log(ratio), and
        # generic dB does not refer to a specific reference value
        return None
    # TODO: handle Log(Exp(ratio, 2))
    return _LogInfo(
        k=info.factor,
        b=log_expr.base,
        q_measured_unit=log_expr.reference,
        q_ref=ratio_between_tag.denominator,
        other_tags=tuple(other_tags),
    )


def convert(
    origin: Expr,
    target: Expr,
    *,
    exact: bool = False,
    ctx: decimal.Context | None = None,
) -> Converter | NonAffineConverter:
    """Create a new unit converter from one unit to another.

    Checks that the underlying dimension are compatible
    (e.g. `USD/year` and `HKD/hour`) and computes the total scaling factor.
    """
    ctx = ctx or decimal.getcontext()
    origin_simpl = simplify(origin)
    target_simpl = simplify(target)

    info_origin = _flatten(origin_simpl)
    info_target = _flatten(target_simpl)

    log_info_origin = _get_log_info(info_origin)
    log_info_target = _get_log_info(info_target)

    if log_info_origin and log_info_target:
        if not (
            log_info_origin.b == log_info_target.b
            and log_info_origin.q_measured_unit
            == log_info_target.q_measured_unit
            and log_info_origin.q_ref.unit == log_info_target.q_ref.unit
            and log_info_origin.other_tags == log_info_target.other_tags
        ):
            return _convert_logarithmic(
                log_info_origin, log_info_target, exact=exact, ctx=ctx
            )
        # if the underlying log unit is the same (same base and reference qty type),
        # then it's a simple linear scaling (e.g. Np -> dNp)
    elif log_info_origin or log_info_target:
        raise NonLinearConversionError(
            origin=origin,
            target=target,
        )  # e.g. V = V_ref * b**(L_dBV / k), L_dbV = k * log_b(V / V_ref)

    if (origin_kind := kind(origin_simpl)) != (
        target_kind := kind(target_simpl)
    ):
        raise KindMismatchError(
            origin_kind=origin_kind, target_kind=target_kind
        )

    origin_dim = dimension(info_origin.expr)
    target_dim = dimension(info_target.expr)
    origin_dim_terms = (
        origin_dim.terms if isinstance(origin_dim, Mul) else (origin_dim,)
    )
    target_dim_terms = (
        target_dim.terms if isinstance(target_dim, Mul) else (target_dim,)
    )
    if origin_dim_terms != target_dim_terms:
        raise DimensionMismatchError(origin, target, origin_dim, target_dim)
    # we have:
    #   v_abs = scale_origin * v_origin + offset_origin
    #   v_abs = scale_target * v_target + offset_target
    # then:
    #   v_target = (scale_origin / scale_target) * v_origin +
    #              (offset_origin - offset_target) / scale_target
    scale_origin = list(_products(info_origin.factor))

    inv_scale_target = tuple(f for f in _products_inverse(info_target.factor))
    scale = LazyProduct(tuple([*scale_origin, *inv_scale_target]))

    offset_numerator = _factor_to_fraction(
        info_origin.offset, ctx=ctx
    ) - _factor_to_fraction(info_target.offset, ctx=ctx)
    offset = LazyProduct(tuple([offset_numerator, *inv_scale_target]))

    return _converter_new(
        scale=scale.to_exact(ctx=ctx) if exact else scale.to_approx(),
        offset=offset.to_exact(ctx=ctx) if exact else offset.to_approx(),
    )


def _convert_logarithmic(
    origin_info: _LogInfo,
    target_info: _LogInfo,
    *,
    exact: bool,
    ctx: decimal.Context,
) -> Converter | NonAffineConverter:
    r"""
    With $L_1 = k_1 \log_{b_1}\left(\frac{Q}{Q_{\text{ref}_1}}\right)$,
    $L_2 = k_2 \log_{b_2}\left(\frac{Q}{Q_{\text{ref}_2}}\right)
    = \underbrace{\left(\frac{k_2}{k_1}\frac{\ln b_1}{\ln b_2}\right)}_\text{scale}
    L_1 + \underbrace{k_2 \log_{b_2}\left(\frac{Q_{\text{ref}_1}}
    {Q_{\text{ref}_2}}\right)}_\text{offset}$
    """
    if origin_info.other_tags != target_info.other_tags:
        raise DimensionMismatchError(
            origin_info.q_measured_unit,
            target_info.q_measured_unit,
            dimension(simplify(origin_info.q_measured_unit)),
            dimension(simplify(target_info.q_measured_unit)),
        )

    ref_converter = convert(
        origin=origin_info.q_ref.unit,
        target=target_info.q_ref.unit,
        exact=True,
        ctx=ctx,
    )
    if isinstance(ref_converter, NonAffineConverter):
        raise NonLinearConversionError(
            origin_info.q_ref.unit, target_info.q_ref.unit
        )

    k1 = _factor_to_fraction(origin_info.k, ctx=ctx)
    k2 = _factor_to_fraction(target_info.k, ctx=ctx)
    b1 = origin_info.b
    b2 = target_info.b
    ref_ratio_f = _factor_to_fraction(ref_converter.scale, ctx=ctx)
    k_ratio = k2 / k1

    if exact:
        b1_d = _fraction_to_decimal(_factor_to_fraction(b1, ctx=ctx))
        b2_d = _fraction_to_decimal(_factor_to_fraction(b2, ctx=ctx))
        ref_ratio_d = _fraction_to_decimal(ref_ratio_f)

        ln_b1_d = b1_d.ln(ctx)
        ln_b2_d = b2_d.ln(ctx)
        ln_ref_ratio_d = ref_ratio_d.ln(ctx)

        scale = k_ratio * Fraction(ln_b1_d) / Fraction(ln_b2_d)
        offset = k2 * Fraction(ln_ref_ratio_d) / Fraction(ln_b2_d)
        return _converter_new(scale, offset)
    else:
        ln_b2_fl = math.log(float(b2))
        scale_fl = float(k_ratio) * math.log(float(b1)) / ln_b2_fl
        offset_fl = float(k2) * math.log(float(ref_ratio_f)) / ln_b2_fl
        return _converter_new(scale_fl, offset_fl)


class _ConversionInfo(NamedTuple):
    expr: Expr
    """Absolute (non-translated, non-scaled) reference"""
    factor: Number | LazyProduct
    """Total scaling factor to convert from this unit to the absolute reference"""
    offset: Number | LazyProduct
    """Total offset to convert from this unit to the absolute reference"""
    tag_origin_at: OriginAt | None = None
    tag_delta: _Delta | None = None


def _flatten(
    expr_simpl: SimplifiedExpr,
) -> _ConversionInfo:
    """Recursively flattens an expression into its absolute base unit."""
    if isinstance(
        expr_simpl,
        (BaseUnit, BaseDimension, Dimensionless, Log, Exp, Mul),
    ):
        # since `Exp(Scaled(x, a), b)` → `Scaled(Exp(x, b), a * b)`
        # similarly, `Mul((Scaled(...),))` → `Scaled(Mul((...),),)`
        return _ConversionInfo(expr_simpl, 1, 0)
    elif isinstance(expr_simpl, Scaled):
        # so `Scaled` should always be pushed to outmost level.
        # furthermore, since nested `Scaled(Scaled(x, c), d)` would simplify to
        # `Scaled(x, c * d)`, we don't need to recursively get the factor.
        factor = f.value if isinstance(f := expr_simpl.factor, Prefix) else f
        return _ConversionInfo(expr_simpl.reference, factor, 0)
    elif isinstance(expr_simpl, Tagged):
        info_ref = _flatten(expr_simpl.reference)  # type: ignore
        tag_origin_at = None
        tag_delta = None
        for tag in expr_simpl.tags:
            if isinstance(tag, OriginAt):
                tag_origin_at = tag
            elif isinstance(tag, _Delta):
                tag_delta = tag
        return _ConversionInfo(
            info_ref.expr[expr_simpl.tags],
            info_ref.factor,
            info_ref.offset,
            tag_origin_at=tag_origin_at,
            tag_delta=tag_delta,
        )
    elif isinstance(expr_simpl, Translated):
        info_ref = _flatten(expr_simpl.reference)  # type: ignore
        assert info_ref.offset == 0, (
            f"inner reference of {expr_simpl=} should not have any offset"
        )
        # v_local = v_ref + offset_local
        #   v_abs = v_ref * factor_ref
        #         = v_local * factor_ref - offset_local * factor_ref
        new_offset = LazyProduct(
            (-1, expr_simpl.offset, *_products(info_ref.factor))
        )
        return _ConversionInfo(info_ref.expr, info_ref.factor, new_offset)
    else:
        assert_never(expr_simpl)


#
# utilities
#


def _unwrap_tagged_or_aliased(expr: Expr) -> Expr:
    # `Translated` and `Log` are terminal, this plugs a loophole
    # NOTE: while Aliased(Aliased(...)) and Tagged(Tagged(...)) are disallowed,
    # Aliased(Tagged(...)) is allowed, so we need to unwrap recursively.
    if isinstance(expr, (Tagged, Aliased)):
        return _unwrap_tagged_or_aliased(expr.reference)
    return expr


def _products(
    factor: Number | LazyProduct | Prefix,
) -> Generator[tuple[Number, Exponent] | Number]:
    if isinstance(factor, Prefix):
        yield factor.value
    elif isinstance(factor, LazyProduct):
        for product in factor.products:
            yield product
    else:
        yield factor


def _products_inverse(
    factor: Number | LazyProduct | Prefix,
) -> Generator[tuple[Number, Exponent] | Number]:
    for item in _products(factor):
        if isinstance(item, tuple):
            base, exponent = item
            yield (base, -exponent)
        else:
            yield (item, -1)


def _factor_to_fraction(
    factor: Number | LazyProduct | Prefix, *, ctx: decimal.Context
) -> Fraction:
    if isinstance(factor, Prefix):
        return _factor_to_fraction(factor.value, ctx=ctx)
    if isinstance(factor, LazyProduct):
        return Fraction(factor.to_exact(ctx=ctx))
    elif isinstance(factor, (Decimal, float, int)):
        return Fraction(factor)
    elif isinstance(factor, SupportsDecimal):
        return Fraction(factor.to_decimal(ctx=ctx))
    elif not isinstance(factor, Fraction):
        raise assert_never(factor)
    return factor


def _fraction_to_decimal(fraction: Fraction) -> Decimal:
    return fraction.numerator / Decimal(fraction.denominator)


@dataclass(frozen=True, **slots)
class LazyProduct(SupportsFloat):
    r"""Represents a lazy product of a sequence of numbers raised to an optional
    exponent, i.e. $\prod_i x_i$, or $\prod_i x_i^{e_i}$.

    Lazy evaluation allows the choice between evaluating it to an exact value
    (taking longer to compute, useful for financial calculations) or an
    approximate float.
    """  # TODO: support LazyProduct itself as the base

    products: tuple[tuple[Number, Exponent] | Number, ...]

    @classmethod
    def from_derived_conversions(
        cls,
        derived_conversions: Sequence[tuple[Scaled, Exponent]],
    ) -> LazyProduct:
        products: list[tuple[Number, Exponent] | Number] = []
        for scaled, exponent in derived_conversions:
            for inner_item in _products(scaled.factor):
                if isinstance(inner_item, tuple):
                    base, inner_exp = inner_item
                    products.append((base, inner_exp * exponent))
                else:
                    products.append((inner_item, exponent))
        return cls(tuple(products))

    def to_approx(self) -> float:
        """Reduce it to an approximate float value. Good enough for most
        applications."""
        product = 1.0
        for item in self.products:
            base, exponent = item if isinstance(item, tuple) else (item, 1)
            if base == 0:
                if exponent > 0:
                    return 0.0
                if exponent == 0:
                    continue  # 0 ** 0 = 1
            if base == 1:
                continue
            product *= float(base) ** float(exponent)
        return product

    # NOTE: not defining `__mul__` to avoid confusion.
    def __float__(self) -> float:
        return self.to_approx()

    def to_exact(self, ctx: decimal.Context) -> Fraction | Decimal:
        """Reduce it to an *exact* fraction or decimal.

        :param ctx: The decimal context (precision, rounding, etc.) to use.
            `decimal.getcontext()` can be used to get the current context.

        The return type depends on the items of each product:

        ```
                         +--------+-------+----------------+
                         |  None  |  int  | Fraction(p, q) | <- exponent
        +----------------+--------+-------+----------------+
        | Decimal        |   .    |   .   |       x        |
        | Fraction(a, b) |   .    |   .   |       *        |
        | float          |   .    |   x   |       x        |
        | int            |   .    |   .   |       ^        |
        +----------------+--------+-------+----------------+
          ^
          |_ base

        Can `base ** exponent` be represented exactly a `Fraction`?

        . Yes
        * Only if q > 0 and a^p and b^q are the perfect q-th power of an integer
          e.g. (8/27) ** (1/3) = 2/3
        ^ Sometimes, e.g. 4 ** (1/2)
        x No, decimal only
        ```

        For simplicity, only cases that can definitively be represented as a
        `Fraction` are returned as such. A `Decimal` is returned otherwise.
        """
        # accumulate products in two streams: if the "tripwire" for decimal
        # is hit, we must return Decimal.
        product_fraction = Fraction(1)
        product_decimal = Decimal(1)
        for item in self.products:
            if not isinstance(item, tuple):  # no exponent
                product_fraction *= _factor_to_fraction(item, ctx=ctx)
                continue
            base, exponent = item
            if base == 0:
                if exponent > 0:
                    return Fraction(0)
                if exponent < 0:
                    raise ZeroDivisionError
                continue  # 0 ** 0 = 1
            if base == 1:
                continue
            if isinstance(exponent, int):
                # most of the time, we can represent it as Fraction
                if isinstance(base, float):
                    base_decimal = ctx.create_decimal_from_float(base)
                    product_decimal *= base_decimal**exponent
                else:
                    base_fraction = _factor_to_fraction(base, ctx=ctx)
                    product_fraction *= base_fraction**exponent
            elif isinstance(exponent, Fraction):
                # but raising to a Fraction exponent requires decimal
                if isinstance(base, SupportsDecimal):
                    base_decimal = base.to_decimal(ctx=ctx)
                elif isinstance(base, Decimal):
                    base_decimal = base
                elif isinstance(base, Fraction):  # *
                    base_decimal = _fraction_to_decimal(base)
                elif isinstance(base, float):
                    base_decimal = ctx.create_decimal_from_float(base)
                elif isinstance(base, int):  # ^
                    base_decimal = Decimal(base, context=ctx)
                else:
                    assert_never(base)
                exponent_decimal = _fraction_to_decimal(exponent)
                product_decimal *= ctx.power(base_decimal, exponent_decimal)
            else:
                assert_never(exponent)
        if product_decimal == Decimal(1):
            return product_fraction
        return _fraction_to_decimal(product_fraction) * product_decimal


@dataclass(frozen=True, **slots)
class StdUncertainty:
    """Concise notation for the one-standard-deviation uncertainty of a
    numerical value.

    For example, the parentheses in `12.3456(89) kg` means:
    ```
         numerical value = 12.3456
    standard uncertainty =  0.0089
    ```
    Use `typing.Annotated` to attach the uncertainty information to the value:
    ```py
    from decimal import Decimal
    from typing import Annotated
    from isqx import KG, StdUncertainty

    CONST_FOO: Annotated[Decimal, KG, StdUncertainty(89)] = Decimal("12.3456")
    ```
    """

    # not really used anywhere - its for clarity only.
    # we could try to propagate errors for derived physical constants,
    # but that is overkill.

    value: int
    """The one-standard-deviation uncertainty expressed in the least
    significant digit(s) of the numerical value. Must be greater than zero."""


@final
class _E(SupportsDecimal):
    __slots__ = ()

    def to_decimal(self, ctx: decimal.Context) -> Decimal:
        return ctx.exp(Decimal(1))

    def __float__(self) -> float:
        return math.e

    def __abs__(self) -> _E:
        return self

    def __str__(self) -> str:
        return "𝑒"


@final
class _PI(SupportsDecimal):
    __slots__ = ()

    def to_decimal(self, ctx: decimal.Context) -> Decimal:
        # from: https://docs.python.org/3/library/decimal.html#recipes
        ctx.prec += 2  # extra digits for intermediate steps
        three = Decimal(3)
        lasts, t, s, n, na, d, da = Decimal(0), three, Decimal(3), 1, 0, 0, 24
        while s != lasts:
            lasts = s
            n, na = n + na, na + 8
            d, da = d + da, da + 32
            t = (t * n) / d
            s += t
        ctx.prec -= 2
        pi = +s  # unary plus applies the new precision
        return pi

    def __float__(self) -> float:
        return math.pi

    def __abs__(self) -> _PI:
        return self

    def __str__(self) -> str:
        return "π"


E: Final[_E] = _E()
"""The Euler number [ISO 80000-2:2019 2-13.1][isqx._citations.ISO_80000_2]."""
PI: Final[_PI] = _PI()
"""The ratio of the circumference of a circle to its diameter
[ISO 80000-2:2019 2-14.1][isqx._citations.ISO_80000_2]."""


#
# tools for introspecting `Annotated` (especially module attributes)
# where __doc__ is not available
#


@dataclass(frozen=True, **slots)
class AnnotatedMetadata:
    unit: Expr | None
    std_uncertainty: StdUncertainty | None

    @classmethod
    def from_args(cls, args: Sequence[Any]) -> AnnotatedMetadata:
        """Extract metadata from the args of an `Annotated` type.

        Example:
        ```pycon
        >>> from typing import Annotated
        >>> from isqx import KG, StdUncertainty
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Foo:
        ...     class_member: Annotated[float, KG, StdUncertainty(13)]
        ...
        >>> def bar(function_arg: Annotated[float, KG]) -> None:
        ...     ...
        ...
        >>> from isqx import AnnotatedMetadata
        >>> def print_metadata(obj) -> None:
        ...     for name, ann in get_type_hints(obj, include_extras=True).items():
        ...         print(f"{name}: {AnnotatedMetadata.from_args(get_args(ann))}")
        ...
        >>> print_metadata(Foo)
        class_member: AnnotatedMetadata(unit=kilogram, std_uncertainty=StdUncertainty(value=13))
        >>> print_metadata(bar)
        function_arg: AnnotatedMetadata(unit=kilogram)
        return: AnnotatedMetadata(unit=None)
        ```
        """
        unit: _TaggedAllowedExpr | None = None
        std_uncertainty: StdUncertainty | None = None
        for arg in args:
            if isinstance(arg, _ARGS_EXPR):
                if unit is not None:
                    raise DuplicateAnnotationError(args, arg)
                unit = arg
            elif isinstance(arg, StdUncertainty):
                if std_uncertainty is not None:
                    raise DuplicateAnnotationError(args, arg)
                std_uncertainty = arg
        return cls(unit=unit, std_uncertainty=std_uncertainty)

    def __str__(self) -> str:
        kv = []
        for field in fields(self):
            if (value := getattr(self, field.name)) is None:
                continue
            kv.append(f"{field.name}={value}")
        return f"{type(self).__name__}({', '.join(kv)})"


def module_attribute_metadata(
    module_rt: ModuleType,
) -> Generator[tuple[str, AnnotatedMetadata], None, None]:
    """Yields all (name, metadata) pairs for module attributes that are
    annotated with valid [unit expressions][isqx.Expr] and/or
    [standard uncertainties][isqx.StdUncertainty] in the given module.

    Effectively returns the units and uncertainties of all constants. Example:
    ```pycon
    >>> from isqx import module_attribute_metadata, iso80000
    >>> for name, metadata in module_attribute_metadata(iso80000):
    ...     print(f"{name}: {metadata}")
    ...
    CONST_SPEED_OF_LIGHT_VACUUM: AnnotatedMetadata(unit=meter · second⁻¹)
    CONST_PLANCK: AnnotatedMetadata(unit=joule · second
    - joule = newton · meter
    - newton = kilogram · meter · second⁻²)
    CONST_REDUCED_PLANCK: AnnotatedMetadata(unit=joule · second
    - joule = newton · meter
    - newton = kilogram · meter · second⁻²)
    ...
    ```
    """
    for name, anno in get_type_hints(module_rt, include_extras=True).items():
        if get_origin(anno) is not Annotated:
            continue
        metadata = AnnotatedMetadata.from_args(get_args(anno))
        yield name, metadata


@dataclass(frozen=True, **slots)
class Anchor:  # NOTE: not using namedtuple so json serialization works nicely
    """A simple wrapper over a text with an external link.

    It is used to:

    - yield a bare string or a "link" in [`isqx.BasicFormatter`][].
    - create a hyperlink in the [where clause of a definition][isqx.details.WhereFragment]
    - render a link in the [HTML documentation][isqx.mkdocs.extension.MkdocsFormatter].
    """

    text: str
    path: str


StrFragment: TypeAlias = Union[str, Anchor]

#
# errors
#


class IsqxError(Exception):
    """Base exception for all errors raised by the isqx library."""


@dataclass(frozen=True, **slots)
class CompositionError(IsqxError):
    outer: type
    inner: Any
    msg: str
    help: str | None = None

    def __str__(self) -> str:  # pragma: no cover
        outer_name = (
            self.outer.name
            if isinstance(self.outer, Prefix)
            else self.outer.__name__
        )
        inner_repr = f"`{self.inner}` (of type `{type(self.inner).__name__}`)"

        message = (
            f"invalid composition: cannot apply `{outer_name}` to {inner_repr}."
            f"\nreason: {self.msg}"
        )
        if self.help:
            message += f"\n= help: {self.help}"
        return message


@dataclass(frozen=True, **slots)
class MixedKindError(IsqxError):
    terms: tuple[Expr, ...]

    def __str__(self) -> str:  # pragma: no cover
        return (
            "cannot mix expressions of different kinds in a product."
            f"\n  found kinds: {', '.join(f'`{kind(t)}`' for t in self.terms)}"
            "\n= help: all terms in a `Mul` expression must be of the same kind "
            "(e.g., all units like `M` and `S`, or all dimensions like "
            "`DIM_LENGTH` and `DIM_TIME`)."
        )


# conversion
@dataclass(frozen=True, **slots)
class KindMismatchError(IsqxError):
    origin_kind: ExprKind
    target_kind: ExprKind

    def __str__(self) -> str:  # pragma: no cover
        return (
            "cannot convert between expressions of different kinds."
            f"\nnote: origin kind: `{self.origin_kind}`"
            f"\n      target kind: `{self.target_kind}`"
        )


@dataclass(frozen=True, **slots)
class DimensionMismatchError(IsqxError):
    origin: Expr
    target: Expr
    dim_origin: Expr
    dim_target: Expr

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"cannot convert from `{self.origin}` to `{self.target}`."
            "\n= help: expected compatible dimensions, but found:"
            f"\ndimension of origin: `{self.dim_origin}`"
            f"\ndimension of target: `{self.dim_target}`"
        )


@dataclass(frozen=True, **slots)
class UnitKindMismatchError(IsqxError):
    qtykind: QtyKind
    unit: Expr
    dim_kind: Expr
    dim_unit: Expr

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"cannot create tagged unit for kind `{self.qtykind.tags}` with "
            f"unit `{self.unit}`."
            f"\nexpected dimension of kind: `{self.dim_kind}`"
            f" (`{self.qtykind.unit_si_coherent}`)"
            f"\n   found dimension of unit: `{self.dim_unit}`"
            f" (`{self.unit}`)"
        )


@dataclass(frozen=True, **slots)
class NonLinearConversionError(IsqxError):
    origin: Expr
    target: Expr

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"cannot create a value-agnostic converter from `{self.origin}` "
            f"to `{self.target}`."
            "conversion between a logarithmic and a linear unit is non-linear."
            "\n= help: this requires a reference value (e.g., 1V for dBV), "
            "but the `isqx` library only performs value-agnostic conversions. "
            "perform the calculation manually instead."
        )


@dataclass(frozen=True, **slots)
class DuplicateAnnotationError(IsqxError):
    annotation_args: Sequence[Any]
    conflicting_arg: _TaggedAllowedExpr | StdUncertainty

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"duplicate annotation `{self.conflicting_arg}` found in "
            f"{', '.join(repr(arg) for arg in self.annotation_args)}."
            "\n= help: only one unit and one standard uncertainty can be "
            "applied."
        )
