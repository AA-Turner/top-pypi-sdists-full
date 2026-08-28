"""A closed arithmetic grammar for ``derived[].expr`` — parse at load, evaluate per window.

Normative references:

* ``_contracts/08-tobe-app-manifest.md`` §3  — ``metrics:`` and what a source may name
* ``_contracts/09-tobe-engine-architecture.md`` §3 §6 — primitives, and the escape hatches
* ``_migration/wave-d1/group3-custom-logic/PORT_REPORT.md`` §5 item 3 — the gap this closes

**Why a parser and not ``eval``.**  A manifest is data that ships in a customer-authored zip
and is read by a long-lived server process.  ``eval``/``exec`` over it — even with a stripped
``__builtins__`` — hands that zip the interpreter; every published sandbox of that shape has
been escaped through attribute walks off a literal.  There is no reason to take the risk here:
the whole requirement is four infix operators over named numbers, which is 200 lines of
recursive descent.  The grammar is *closed* — no names, no attributes, no calls, no
subscripts, no comparisons — so there is nothing to escape *to*::

    expr    := term (("+" | "-") term)*
    term    := factor (("*" | "/") factor)*
    factor  := ("+" | "-")? primary
    primary := NUMBER | SOURCE | "(" expr ")"
    NUMBER  := 12 | 12.5 | 1e3            (non-negative; unary minus is a factor)
    SOURCE  := <stage>.<value>            e.g. detect.person.count, unique_count.new

The backend already evaluates operator-only formulas over metric variables with ``govaluate``
(``be-analytics`` instant metrics), so an expression over named numbers is an established
shape in the product; this is the same idea one layer earlier, with a much smaller grammar.

**Two numeric rules, both load-bearing:**

1. **A zero denominator is *undefined*, not NaN, not Infinity, and not an error.**
   :meth:`DerivedExpression.evaluate` returns ``None``, and the caller treats an undefined
   reading as *no sample* — which for a whole window publishes ``0.0``
   (:func:`~matrice_analytics.engine.runtime.window.collapse` of no samples).  That is
   exactly what all four legacy producers of a rate do
   (``legacy_analytics_bridge.py``:2444 ``defect_rate``, :2461 ``violation_rate``,
   :2562 ``loitering_percentage``, :2618 ``mask_violation_rate`` — every one of them
   ``if denominator > 0: … else: return 0.0``), so the number the dashboard has been
   showing does not change on migration.  It is also the only answer that cannot reach the
   wire as ``NaN``: the contract rejects non-finite values outright (finding **F1** —
   ``json.dumps`` emits the bare token ``NaN``, Go's ``encoding/json`` refuses it, and the
   backend drops **the whole 60-second window** with no error).

2. **Every intermediate result is checked finite.**  An operand a primitive published as
   ``inf``, or an overflow in ``1e308 * 10``, raises :class:`EvaluationError` rather than
   travelling on.  The caller skips the metric and says so in the log: a visible gap in a
   series is diagnosable, and **F1** is not.

Undefined propagates: any sub-expression that is undefined makes the whole expression
undefined.  ``a / b + 5`` with ``b == 0`` is undefined, not ``5``, because the reading it
would publish is not a reading of anything.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Final

__all__ = [
    "MAX_EXPRESSION_DEPTH",
    "MAX_EXPRESSION_LENGTH",
    "DerivedExpression",
    "EvaluationError",
    "ExpressionError",
    "parse_expression",
]


class ExpressionError(ValueError):
    """The expression text is not in the grammar. Raised at **load** time only."""


class EvaluationError(ValueError):
    """A parsed expression cannot produce a finite number from these values.

    A missing operand, a non-finite operand, or an arithmetic overflow.  Never a zero
    denominator — that is ``None`` (undefined), which is a reading, not a fault.
    """


#: Longest accepted expression.  A derived metric is one line of arithmetic; anything past
#: this is either generated or an attempt to find a parser bug.
MAX_EXPRESSION_LENGTH: Final[int] = 512

#: Deepest accepted parenthesis nesting.  ``primary`` recurses, so an unbounded nest is a
#: stack overflow — a ``RecursionError`` out of a *validator* is a crash the loader cannot
#: explain, where a rejection names the manifest and the line.
MAX_EXPRESSION_DEPTH: Final[int] = 32

_GRAMMAR_HINT: Final[str] = (
    "An expression is numbers and '<stage>.<value>' sources combined with + - * / and "
    "parentheses — nothing else. There are no function calls, no comparisons and no "
    "variables: it is deliberately the smallest grammar that expresses a rate."
)

_TOKEN_RE: Final[re.Pattern[str]] = re.compile(
    r"""
      (?P<space>\s+)
    | (?P<number>\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)
    | (?P<name>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)
    | (?P<op>[+\-*/])
    | (?P<lparen>\()
    | (?P<rparen>\))
    """,
    re.VERBOSE,
)


@dataclass(frozen=True, slots=True)
class _Token:
    kind: str
    text: str
    position: int

    def describe(self) -> str:
        return f"{self.text!r} at position {self.position}"


def _tokenise(text: str) -> list[_Token]:
    tokens: list[_Token] = []
    index = 0
    while index < len(text):
        match = _TOKEN_RE.match(text, index)
        if match is None:
            raise ExpressionError(
                f"unexpected character {text[index]!r} at position {index} in "
                f"{text!r}. {_GRAMMAR_HINT}"
            )
        index = match.end()
        kind = match.lastgroup or ""
        if kind == "space":
            continue
        tokens.append(_Token(kind=kind, text=match.group(), position=match.start()))
    return tokens


# ---------------------------------------------------------------------------
# The AST — four node types, each a frozen dataclass with no behaviour but its own
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _Number:
    value: float

    def evaluate(self, values: Mapping[str, float]) -> float | None:
        del values  # a literal reads nothing; the signature is the node protocol
        return self.value

    def sources(self) -> tuple[str, ...]:
        return ()


@dataclass(frozen=True, slots=True)
class _Source:
    """A ``<stage>.<value>`` operand. Resolved against the pipeline at load time.

    :attr:`name` is a **dictionary key**, never a Python attribute path: the dots are part of
    the output name (``detect.person.count`` is one key published by one stage).  Nothing in
    this module performs attribute access, calls anything, or looks at a builtin, so a name
    such as ``a.__class__`` is only ever a lookup that fails to resolve at load time.
    """

    name: str

    def evaluate(self, values: Mapping[str, float]) -> float | None:
        if self.name not in values:
            raise EvaluationError(
                f"operand {self.name!r} has no value. The manifest resolved it against the "
                f"pipeline, so either the stage did not run in this zone or its output names "
                f"have drifted from its config model."
            )
        raw = values[self.name]
        number = float(raw)
        if not isfinite(number):
            raise EvaluationError(
                f"operand {self.name!r} is {raw!r}, which is not a finite number. A "
                f"non-finite value cannot reach the wire (contract finding F1): Go's "
                f"encoding/json rejects the bare NaN/Infinity token and the backend loses "
                f"the whole window."
            )
        return number

    def sources(self) -> tuple[str, ...]:
        return (self.name,)


@dataclass(frozen=True, slots=True)
class _Negate:
    operand: _Node

    def evaluate(self, values: Mapping[str, float]) -> float | None:
        inner = self.operand.evaluate(values)
        return None if inner is None else -inner

    def sources(self) -> tuple[str, ...]:
        return self.operand.sources()


@dataclass(frozen=True, slots=True)
class _Binary:
    operator: str
    left: _Node
    right: _Node

    def evaluate(self, values: Mapping[str, float]) -> float | None:
        left = self.left.evaluate(values)
        right = self.right.evaluate(values)
        if left is None or right is None:
            return None  # undefined propagates — see the module docstring

        if self.operator == "/":
            if right == 0.0:
                # THE rule. Not NaN (F1), not an exception, not a fabricated 100%:
                # "no denominator" means "no reading", and the caller turns that into
                # the 0.0 every legacy producer of a rate already publishes.
                return None
            result = left / right
        elif self.operator == "*":
            result = left * right
        elif self.operator == "+":
            result = left + right
        else:  # "-"
            result = left - right

        if not isfinite(result):
            raise EvaluationError(
                f"{left!r} {self.operator} {right!r} is not finite. Non-finite numbers "
                f"cannot reach the wire (contract finding F1); the metric is skipped rather "
                f"than published as NaN, which would cost the whole window."
            )
        return result

    def sources(self) -> tuple[str, ...]:
        return self.left.sources() + self.right.sources()


#: The node union.  Declared after the four classes and referenced only from string
#: annotations (``from __future__ import annotations``), so the forward reference costs nothing.
_Node = _Number | _Source | _Negate | _Binary


# ---------------------------------------------------------------------------
# The parser — recursive descent, one method per production
# ---------------------------------------------------------------------------


class _Parser:
    """Recursive descent over :func:`_tokenise`'s output. One instance per parse."""

    def __init__(self, text: str, tokens: list[_Token]) -> None:
        self._text = text
        self._tokens = tokens
        self._index = 0

    # -- token access ------------------------------------------------------

    def _peek(self) -> _Token | None:
        return self._tokens[self._index] if self._index < len(self._tokens) else None

    def _take(self) -> _Token:
        token = self._peek()
        if token is None:  # pragma: no cover - every caller checks _peek first
            raise ExpressionError(f"expression {self._text!r} ended unexpectedly. {_GRAMMAR_HINT}")
        self._index += 1
        return token

    # -- productions -------------------------------------------------------

    def parse(self) -> _Node:
        node = self._expr(depth=0)
        trailing = self._peek()
        if trailing is not None:
            raise ExpressionError(
                f"unexpected {trailing.describe()} in {self._text!r} — the expression already "
                f"ended before it. {_GRAMMAR_HINT}"
            )
        return node

    def _expr(self, depth: int) -> _Node:
        node = self._term(depth)
        while True:
            token = self._peek()
            if token is None or token.kind != "op" or token.text not in "+-":
                return node
            self._take()
            node = _Binary(operator=token.text, left=node, right=self._term(depth))

    def _term(self, depth: int) -> _Node:
        node = self._factor(depth)
        while True:
            token = self._peek()
            if token is None or token.kind != "op" or token.text not in "*/":
                return node
            self._take()
            node = _Binary(operator=token.text, left=node, right=self._factor(depth))

    def _factor(self, depth: int) -> _Node:
        token = self._peek()
        if token is not None and token.kind == "op" and token.text in "+-":
            self._take()
            inner = self._factor(depth)
            return _Negate(operand=inner) if token.text == "-" else inner
        return self._primary(depth)

    def _primary(self, depth: int) -> _Node:
        if depth >= MAX_EXPRESSION_DEPTH:
            raise ExpressionError(
                f"expression {self._text!r} nests parentheses more than "
                f"{MAX_EXPRESSION_DEPTH} deep. A derived metric is one line of arithmetic; "
                f"if it genuinely needs this, it needs a 'custom' pipeline stage instead."
            )
        token = self._peek()
        if token is None:
            raise ExpressionError(
                f"expression {self._text!r} ends where a number, a '<stage>.<value>' source "
                f"or '(' was expected. {_GRAMMAR_HINT}"
            )

        if token.kind == "number":
            self._take()
            return _Number(value=float(token.text))

        if token.kind == "name":
            self._take()
            if "." not in token.text:
                raise ExpressionError(
                    f"operand {token.text!r} in {self._text!r} is not a source reference. An "
                    f"operand is '<stage>.<value>' — the same thing metrics[].source names, "
                    f"e.g. 'unique_count.new' or 'detect.person.count'. A bare name is not a "
                    f"metric key either: an expression reads pipeline outputs, not other "
                    f"metrics, so that a derived value and its inputs can never disagree "
                    f"about which number they came from."
                )
            return _Source(name=token.text)

        if token.kind == "lparen":
            self._take()
            inner = self._expr(depth + 1)
            closing = self._peek()
            if closing is None or closing.kind != "rparen":
                raise ExpressionError(
                    f"unclosed '(' at position {token.position} in {self._text!r}."
                )
            self._take()
            return inner

        raise ExpressionError(
            f"unexpected {token.describe()} in {self._text!r}, where a number, a "
            f"'<stage>.<value>' source or '(' was expected. {_GRAMMAR_HINT}"
        )


# ---------------------------------------------------------------------------
# The public object
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DerivedExpression:
    """A parsed ``derived[].expr``: its text, its operands, and how to evaluate it.

    Immutable and cheap to keep: the manifest parses once at load and the runtime evaluates
    the same object every window, so no text is ever re-parsed on the hot path.
    """

    text: str
    _root: _Node

    @property
    def operands(self) -> tuple[str, ...]:
        """Every ``<stage>.<value>`` the expression reads, first-appearance order, no repeats.

        This is what the manifest resolves against the pipeline — an operand that does not
        resolve is a load error, exactly like a bad ``metrics[].source``.
        """
        seen: dict[str, None] = {}
        for name in self._root.sources():
            seen.setdefault(name, None)
        return tuple(seen)

    def evaluate(self, values: Mapping[str, float]) -> float | None:
        """The expression's value, or ``None`` when it is **undefined**.

        Args:
            values: ``<stage>.<value>`` → number.  Must contain every name in
                :attr:`operands`; a missing one is an :class:`EvaluationError` rather than a
                zero, because a metric that reads zero forever is indistinguishable from a
                quiet camera (``09`` §3).

        Returns:
            A finite float, or ``None`` when a denominator was zero anywhere in the
            expression.  ``None`` means "no reading" — the caller publishes no sample for it,
            which over a whole window is the ``0.0`` every legacy rate publishes.

        Raises:
            EvaluationError: An operand is missing or non-finite, or the arithmetic
                overflowed.  Never for a zero denominator.
        """
        return self._root.evaluate(values)

    def __str__(self) -> str:
        return self.text


def parse_expression(text: str) -> DerivedExpression:
    """Parse ``text`` into a :class:`DerivedExpression`, or raise :class:`ExpressionError`.

    Pure syntax: the operands are *not* checked against a pipeline here (the grammar does not
    know what a pipeline is).  :meth:`AppManifest._check_derived` does that with
    :func:`~matrice_analytics.engine.manifest.models.resolve_source`, so an operand and a
    ``metrics[].source`` fail the same way with the same message.
    """
    if not isinstance(text, str):
        raise ExpressionError(
            f"expression must be a string, got {type(text).__name__}. {_GRAMMAR_HINT}"
        )
    stripped = text.strip()
    if not stripped:
        raise ExpressionError(f"expression is empty. {_GRAMMAR_HINT}")
    if len(stripped) > MAX_EXPRESSION_LENGTH:
        raise ExpressionError(
            f"expression is {len(stripped)} characters, over the {MAX_EXPRESSION_LENGTH} "
            f"limit. A derived metric is one line of arithmetic over pipeline outputs; "
            f"anything longer belongs in a 'custom' pipeline stage, where it can be tested."
        )
    return DerivedExpression(text=stripped, _root=_Parser(stripped, _tokenise(stripped)).parse())
