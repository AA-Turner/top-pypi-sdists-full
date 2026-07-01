from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import IntEnum, auto
from fractions import Fraction
from typing import (
    Callable,
    Generator,
    Literal,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from typing_extensions import TypeAlias, assert_never

from ._core import (
    DELTA,
    DIFFERENTIAL,
    INEXACT_DIFFERENTIAL,
    Aliased,
    Anchor,
    BaseDimension,
    BaseUnit,
    Dimensionless,
    Exp,
    Exponent,
    Expr,
    LazyProduct,
    Log,
    Mul,
    Name,
    NamedExpr,
    Number,
    OriginAt,
    Prefix,
    Quantity,
    Scaled,
    StrFragment,
    Tagged,
    Translated,
    _RatioBetween,
)
from ._core import (
    E as _E,
)

_FormatSpec: TypeAlias = Literal["basic"]
_DefinableExpr: TypeAlias = Union[Aliased, Translated, Log, Tagged]


def fmt(expr: Expr, formatter: Formatter | _FormatSpec | str = "basic") -> str:
    if isinstance(formatter, Formatter):
        return "".join(
            item.text if isinstance(item, Anchor) else item
            for item in formatter.fmt(expr)
        )
    if formatter == "" or formatter == "basic":
        return fmt(expr, DEFAULT_FORMATTER)
    raise NotImplementedError(f"unknown format {formatter=}")


@runtime_checkable
class Formatter(Protocol):
    def fmt(self, expr: Expr) -> Generator[StrFragment, None, None]: ...


class Precedence(IntEnum):
    NONE = auto()
    """Virtual precedence, not a Python expression.
    
    Use this when the parent already is in a parenthesised group and you want to
    guarantee that the child will not add any additional parentheses."""
    MUL = auto()
    SCALED = auto()
    LOG = auto()
    TAGGED = auto()
    EXP = auto()
    ATOM = auto()


PRECEDENCE: dict[type[Expr], Precedence] = {
    Mul: Precedence.MUL,
    Scaled: Precedence.SCALED,
    Log: Precedence.LOG,
    Tagged: Precedence.TAGGED,
    Exp: Precedence.EXP,
    BaseUnit: Precedence.ATOM,
    BaseDimension: Precedence.ATOM,
    Dimensionless: Precedence.ATOM,
    Aliased: Precedence.ATOM,
    Translated: Precedence.ATOM,
}


_VisitorState = TypeVar("_VisitorState", contravariant=True)
_VisitorResult = TypeVar("_VisitorResult", covariant=True)


class Visitor(Protocol[_VisitorState, _VisitorResult]):
    def visit_named(
        self, expr: NamedExpr, state: _VisitorState
    ) -> _VisitorResult: ...

    def visit_exp(self, expr: Exp, state: _VisitorState) -> _VisitorResult: ...

    def visit_mul(self, expr: Mul, state: _VisitorState) -> _VisitorResult: ...

    def visit_scaled(
        self, expr: Scaled, state: _VisitorState
    ) -> _VisitorResult: ...

    def visit_tagged(
        self, expr: Tagged, state: _VisitorState
    ) -> _VisitorResult: ...

    def visit_translated(
        self, expr: Translated, state: _VisitorState
    ) -> _VisitorResult: ...

    def visit_log(self, expr: Log, state: _VisitorState) -> _VisitorResult: ...


def visit_expr(
    visitor: Visitor[_VisitorState, _VisitorResult],
    expr: Expr,
    state: _VisitorState,
) -> _VisitorResult:
    if isinstance(expr, (Dimensionless, BaseDimension, BaseUnit, Aliased)):
        return visitor.visit_named(expr, state)
    elif isinstance(expr, Exp):
        return visitor.visit_exp(expr, state)
    elif isinstance(expr, Mul):
        return visitor.visit_mul(expr, state)
    elif isinstance(expr, Scaled):
        return visitor.visit_scaled(expr, state)
    elif isinstance(expr, Tagged):
        return visitor.visit_tagged(expr, state)
    elif isinstance(expr, Translated):
        return visitor.visit_translated(expr, state)
    elif isinstance(expr, Log):
        return visitor.visit_log(expr, state)
    else:
        assert_never(expr)


_BASIC_EXPONENT_MAP = str.maketrans("0123456789-/", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⸍")
_BASIC_SUBSCRIPT_MAP = str.maketrans("0123456789-/", "₀₁₂₃₄₅₆₇₈₉₋⸝")


@dataclass
class _BasicFormatterState:
    parent_precedence: Precedence = Precedence.NONE
    definitions: dict[str, _DefinableExpr] = field(default_factory=dict)

    @contextmanager
    def _set_parent_precedence(
        self, precedence_expr: Precedence
    ) -> Generator[None, None, None]:
        old_precedence = self.parent_precedence
        self.parent_precedence = precedence_expr
        try:
            yield
        finally:
            self.parent_precedence = old_precedence


@dataclass(frozen=True)
class BasicFormatter(
    Visitor[_BasicFormatterState, Generator[StrFragment, None, None]],
    Formatter,
):
    overrides: dict[Name, str] = field(default_factory=dict)
    verbose: bool = False
    infix_mul: str = " · "

    def fmt(self, expr: Expr) -> Generator[StrFragment, None, None]:
        state = _BasicFormatterState()
        yield from self.visit(expr, state)

        if self.verbose and state.definitions:
            seen_definitions: set[str] = set()
            for name, expr in state.definitions.items():
                yield from self._fmt_definition(
                    name,
                    expr,
                    seen_definitions=seen_definitions,
                    depth=0,
                )

    def _fmt_definition(
        self,
        name: str,
        expr: _DefinableExpr,
        *,
        seen_definitions: set[str],
        depth: int,
    ) -> Generator[StrFragment, None, None]:
        if name in seen_definitions:
            return
        seen_definitions.add(name)
        yield f"\n{'  ' * depth}- {name} = "

        state = _BasicFormatterState()
        if isinstance(expr, Translated):
            yield from self.visit(expr.reference, state)
            yield (
                f" + {o}" if float(o := expr.offset) >= 0 else f" - {abs(o)}"
            )
        else:
            yield from self.visit(expr.reference, state)

        for sub_name, sub_expr in state.definitions.items():
            yield from self._fmt_definition(
                sub_name,
                sub_expr,
                seen_definitions=seen_definitions,
                depth=depth + 1,
            )

    def visit(
        self, expr: Expr, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        precedence_expr = PRECEDENCE[type(expr)]
        needs_parentheses = state.parent_precedence >= precedence_expr
        if needs_parentheses:
            yield "("
        yield from visit_expr(self, expr, state)
        if needs_parentheses:
            yield ")"

    # for named (including tagged), do not "expand" the inner references,
    # but add them to the state, so they can be formatted later.
    def visit_named(
        self, expr: NamedExpr, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        name = expr.name
        name_formatted = self.overrides.get(name, name)
        yield name_formatted
        if (
            isinstance(expr, (Aliased, Translated))
            and name_formatted not in state.definitions
        ):
            state.definitions[name_formatted] = expr

    def visit_tagged(
        self, expr: Tagged, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        precedence_expr = PRECEDENCE[Tagged]
        with state._set_parent_precedence(precedence_expr):
            yield from self.visit(expr.reference, state)
        yield "["
        num_tags = len(expr.tags)
        for i, tag in enumerate(expr.tags):
            if isinstance(tag, _RatioBetween):
                yield "`"
                with state._set_parent_precedence(Precedence.NONE):
                    yield from self.visit(tag.numerator, state)
                yield "` to `"
                if isinstance(q := tag.denominator, Quantity):
                    yield from _format_factor(
                        q.value,
                        infix_mul=self.infix_mul,
                        format_product=self._fmt_product,
                    )
                    with state._set_parent_precedence(Precedence.NONE):
                        yield from self.visit(q.unit, state)
                else:
                    with state._set_parent_precedence(Precedence.NONE):
                        yield from self.visit(q, state)
                yield "`"
            elif isinstance(tag, OriginAt):
                yield "relative to `"
                if isinstance(loc := tag.location, Quantity):
                    yield from _format_factor(
                        loc.value,
                        infix_mul=self.infix_mul,
                        format_product=self._fmt_product,
                    )
                    with state._set_parent_precedence(precedence_expr):
                        yield from self.visit(loc.unit, state)
                else:  # hashable
                    yield repr(tag.location)
                yield "`"
            elif tag is DELTA:
                yield "Δ"
            elif tag is DIFFERENTIAL:
                yield "differential"
            elif tag is INEXACT_DIFFERENTIAL:
                yield "inexact differential"
            else:
                yield repr(tag)
            if i < num_tags - 1:
                yield ", "
        yield "]"

    def visit_exp(
        self, expr: Exp, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        with state._set_parent_precedence(PRECEDENCE[Exp]):
            yield from self.visit(expr.base, state)
        yield str(expr.exponent).translate(_BASIC_EXPONENT_MAP)

    def visit_mul(
        self, expr: Mul, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        precedence_expr = PRECEDENCE[Mul]
        for i, term in enumerate(expr.terms):
            with state._set_parent_precedence(precedence_expr):
                yield from self.visit(term, state)
            if i < len(expr.terms) - 1:
                yield self.infix_mul

    def visit_scaled(
        self, expr: Scaled, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        yield from _format_factor(
            expr.factor,
            infix_mul=self.infix_mul,
            format_product=self._fmt_product,
        )
        with state._set_parent_precedence(PRECEDENCE[Scaled]):
            yield from self.visit(expr.reference, state)

    def visit_translated(
        self, expr: Translated, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        yield from self.visit_named(expr, state)

    def visit_log(
        self, expr: Log, state: _BasicFormatterState
    ) -> Generator[StrFragment, None, None]:
        if expr.base is _E:
            yield "ln"
        else:
            yield "log"
            yield str(expr.base).translate(_BASIC_SUBSCRIPT_MAP)
        yield "("
        with state._set_parent_precedence(PRECEDENCE[Log]):
            yield from self.visit(expr.reference, state)
        yield ")"

    @staticmethod
    def _fmt_product(term: Number | tuple[Number, Exponent]) -> str:
        if isinstance(term, tuple):
            base, exponent = term
            if exponent == 1:
                return str(base)
            base_formatted = (
                f"({base})" if isinstance(base, Fraction) else str(base)
            )
            return f"{base_formatted}{str(exponent).translate(_BASIC_EXPONENT_MAP)}"
        return str(term)


def _format_factor(
    factor: Number | LazyProduct | Prefix,
    *,
    infix_mul: str,
    format_product: Callable[[Number | tuple[Number, Exponent]], str],
) -> Generator[str, None, None]:
    if isinstance(factor, Prefix):
        yield str(factor.name)
        return  # prefixes are not followed with mul
        # TODO: in verbose mode, might want to show centi = 1/100 etc
    elif isinstance(factor, LazyProduct):
        n_products = len(factor.products)
        for i, p in enumerate(factor.products):
            yield format_product(p)
            if i < n_products - 1:
                yield infix_mul
    else:
        yield str(factor)
    yield infix_mul


DEFAULT_FORMATTER = BasicFormatter(verbose=True)
