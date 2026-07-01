"""[Dimensionless quantities][isqx.Dimensionless] and
[quantity kinds][isqx.QtyKind] themselves do not store the precise definition
of how it is derived.

This module contains **optional** details that "link" them together. It is
stored in a [dictionary of expressions to its details][isqx.details.Details]. A
detail can contain multiple [equations][isqx.details.Equation] or [common
symbols][isqx.details.Symbol].

Our [mkdocs plugin][isqx.mkdocs.plugin] reads dictionaries from this module to
"inject" information into docstrings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol, Union, runtime_checkable

from typing_extensions import TypeAlias, get_args

from .._core import (
    Dimensionless,
    LazyProduct,
    Number,
    QtyKind,
    Scaled,
    StrFragment,
    Tagged,
    slots,
)


@dataclass(frozen=True)
class _RefSelf:
    __slots__ = ()


SELF = _RefSelf()
"""A special marker to represent a reference to "itself" in the meaning of a
[definition's where clause][isqx.details.Equation.where]."""

RefDetail: TypeAlias = Union[
    QtyKind, Dimensionless, Tagged, LazyProduct, Number
]
"""A reference to a quantity kind, dimensionless number, a numerical constant,
or a string"""
WhereFragment: TypeAlias = Union[_RefSelf, RefDetail, StrFragment]
# allow factories: Callable[..., RefDetail]
WhereValue: TypeAlias = Union[WhereFragment, tuple[WhereFragment, ...]]
Where: TypeAlias = dict[str, WhereValue]
# allow the key of the where to allow a symbol, e.g. m(X) where X is a substance
# but this will be very complicated.


@dataclass(frozen=True, **slots)
class Wikidata:
    """Stores the Wikidata Q-code for a quantity kind."""

    qcode: str


# isolating into a protocol to help with static analysis in griffe
@runtime_checkable
class HasKaTeXWhere(Protocol):
    katex: str
    r"""A $\KaTeX$ string"""
    where: Where | None
    r"""A mapping of the symbols in the $\KaTeX$ string to their meanings."""


@dataclass(frozen=True, **slots)
class Symbol(HasKaTeXWhere):
    """Stores a common symbol for a quantity kind.

    Since the [equation][isqx.details.Equation] class already contains the
    symbol, adding the symbol is not necessary. However, it is useful when the
    quantity kind is not defined by an equation.
    """

    katex: str
    where: Where | None = None
    remarks: str | None = None
    """A description of when this symbol should be used, e.g. for mole fraction,
    `x_X` is used for condensed phase and `y_X` is used for gaseous mixtures."""


@dataclass(frozen=True, **slots)
class Equation(HasKaTeXWhere):
    """Stores the equation for a quantity kind."""

    katex: str
    where: Where | None = None
    assumptions: set[StrFragment | tuple[StrFragment, ...]] | None = None
    """A set of assumptions under which the definition is valid."""


DetailKey: TypeAlias = Union[
    QtyKind, Dimensionless, Tagged, Scaled, LazyProduct, Number
]
# support adding symbols to tagged(dimensionless) and -1 * Log...
_ARGS_DETAIL_KEY = get_args(DetailKey)
Detail: TypeAlias = Union[Wikidata, Symbol, Equation]
Details: TypeAlias = dict[
    Union[DetailKey, Callable[..., DetailKey]],
    Union[Detail, tuple[Detail, ...]],
]
