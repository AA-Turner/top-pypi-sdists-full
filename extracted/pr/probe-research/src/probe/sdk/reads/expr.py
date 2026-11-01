"""Build an expression-view spec — the thing an agent writes.

Expression views are computed at READ time from series already logged on a run:
no points stored, nothing paid until viewed, always current. The dashboard renders
and deletes them but never authors one; this module and `probe views create` are
the authoring surface (an agent session or a script):

    from probe import expr

    spec = expr.series("train/loss") / expr.series("train/entropy")
    spec = expr.log(expr.series("eval/val_loss")) * 2
    spec = expr.series("train/loss").ema(factor=0.9)
    run.create_view("train/loss_ratio", spec)

Operators coerce bare numbers to constants (``expr.series("eval/accuracy") * 100``).
A raw dict is accepted anywhere an ``Expr`` is (agents that emit JSON), and every
path validates through the generated ``MetricViewSpec`` before the wire, so a
malformed spec fails HERE naming the field, not as a server 422.

The grammar is deliberately closed (series | const | binary | unary | smooth, plus
the node kinds below), not a general language. Anything else (cumulative integral,
bootstrap CI, custom scorer) belongs to :meth:`probe.Run.log_derived`, which
computes in Python and stores a derived series. Read-time formula vs computed-and-
stored is the whole design; do not widen this AST.
"""

from __future__ import annotations

from typing import Any

from ...models import MetricViewSpec

__all__ = [
    "Expr",
    "acos", "asin", "atan", "atan2",
    "cbrt", "ceil", "clamp", "cmp", "coalesce", "cond", "const", "cos", "cosh",
    "ema", "exp", "expm1",
    "floor", "hypot",
    "log", "log10", "log1p", "log2",
    "max_", "min_", "mod", "neg",
    "pow_", "reciprocal", "relu", "round_",
    "cummax", "cummin", "cumprod", "cumsum", "delta",
    "normalize", "reduce", "rolling_max", "rolling_min", "rolling_std",
    "scan", "series", "shift", "sigmoid", "sign", "sin", "sinh", "sma", "spec",
    "sqrt", "tan", "tanh", "trunc", "window", "zscore",
]

# Server-side names, mirrored so a typo fails here, not as a 422.
_BINARY = {"add", "sub", "mul", "div", "pow", "mod", "min", "max", "hypot", "atan2"}
_UNARY = {
    "log", "log10", "log2", "log1p", "exp", "expm1",
    "sqrt", "cbrt", "abs", "neg", "sign", "reciprocal",
    "floor", "ceil", "round", "trunc",
    "sigmoid", "tanh", "relu",
    "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh",
}
_CMP = {"gt", "gte", "lt", "lte", "eq", "ne"}
_SCAN = {"cumsum", "cumprod", "cummax", "cummin", "delta"}
_WINDOW = {"mean", "std", "var", "min", "max", "median"}
_REDUCE = {"sum", "mean", "median", "std", "var", "min", "max", "first", "last", "count"}


def _node(value: "Expr | dict | int | float") -> dict:
    """Coerce an operand to a node dict; bare numbers become constants."""
    if isinstance(value, Expr):
        return value.node
    if isinstance(value, dict):
        return value
    if isinstance(value, bool):
        # bool is an int subclass; True silently becoming const(1.0) is confusing to debug.
        raise TypeError("expression operands are numbers or expressions, not bool")
    if isinstance(value, (int, float)):
        return {"op": "const", "value": float(value)}
    raise TypeError(
        f"cannot use {type(value).__name__} in an expression; "
        "use expr.series(...), a number, or a node dict"
    )


class Expr:
    """One node of an expression tree, with arithmetic that builds more of it.

    Immutable: every operator returns a new ``Expr``, so sub-expressions are safely shared across views.
    """

    __slots__ = ("_node",)

    def __init__(self, node: dict):
        self._node = node

    @property
    def node(self) -> dict:
        """The raw AST node. A shallow copy — mutating it cannot corrupt this Expr."""
        return dict(self._node)

    def spec(self) -> dict:
        """The full ``{"expression": ...}`` view spec, validated."""
        return spec(self)

    # -- arithmetic ---------------------------------------------------------
    def _binary(self, fn: str, other: Any, *, flip: bool = False) -> "Expr":
        left, right = (_node(other), self._node) if flip else (self._node, _node(other))
        return Expr({"op": "binary", "fn": fn, "left": left, "right": right})

    def __add__(self, other: Any) -> "Expr":
        return self._binary("add", other)

    def __radd__(self, other: Any) -> "Expr":
        return self._binary("add", other, flip=True)

    def __sub__(self, other: Any) -> "Expr":
        return self._binary("sub", other)

    def __rsub__(self, other: Any) -> "Expr":
        return self._binary("sub", other, flip=True)

    def __mul__(self, other: Any) -> "Expr":
        return self._binary("mul", other)

    def __rmul__(self, other: Any) -> "Expr":
        return self._binary("mul", other, flip=True)

    def __truediv__(self, other: Any) -> "Expr":
        return self._binary("div", other)

    def __rtruediv__(self, other: Any) -> "Expr":
        return self._binary("div", other, flip=True)

    def __pow__(self, other: Any) -> "Expr":
        return self._binary("pow", other)

    def __rpow__(self, other: Any) -> "Expr":
        return self._binary("pow", other, flip=True)

    def __mod__(self, other: Any) -> "Expr":
        return self._binary("mod", other)

    def __rmod__(self, other: Any) -> "Expr":
        return self._binary("mod", other, flip=True)

    def __neg__(self) -> "Expr":
        return neg(self)

    def __abs__(self) -> "Expr":
        return _unary("abs", self)

    # -- smoothing (chaining reads better than nesting for this one) ---------
    def ema(self, factor: float = 0.6) -> "Expr":
        """Exponential moving average over the ALIGNED result — ``EMA(a / b)``,
        which is not the same curve as ``EMA(a) / EMA(b)``."""
        return ema(self, factor=factor)

    def sma(self, window: int = 10) -> "Expr":
        """Simple moving average over the aligned result."""
        return sma(self, window=window)

    # -- comparison -------------------------------------------------------
    # These build MASK nodes (a 0/1 curve for `cond` or multiplying), so Expr is
    # deliberately non-boolean: `if a > b` would be a bug, hence __bool__ raises.
    def __gt__(self, other: Any) -> "Expr":
        return cmp("gt", self, other)

    def __ge__(self, other: Any) -> "Expr":
        return cmp("gte", self, other)

    def __lt__(self, other: Any) -> "Expr":
        return cmp("lt", self, other)

    def __le__(self, other: Any) -> "Expr":
        return cmp("lte", self, other)

    def __eq__(self, other: Any) -> "Expr":  # type: ignore[override]
        return cmp("eq", self, other)

    def __ne__(self, other: Any) -> "Expr":  # type: ignore[override]
        return cmp("ne", self, other)

    __hash__ = None  # type: ignore[assignment]

    def __bool__(self) -> bool:
        raise TypeError(
            "an Expr is a curve, not a condition: `a > b` builds a 0/1 mask, so "
            "`if a > b` cannot work. Use expr.cond(a > b, then, otherwise)."
        )

    # -- guards -----------------------------------------------------------
    def clamp(self, lo: Any, hi: Any) -> "Expr":
        """Bound this curve to [lo, hi]."""
        return clamp(self, lo, hi)

    def coalesce(self, fallback: Any) -> "Expr":
        """Replace non-finite results (a divide-by-zero) with `fallback`,
        keeping the step instead of dropping it."""
        return coalesce(self, fallback)

    def __repr__(self) -> str:
        return f"Expr({self._node!r})"


def _unary(fn: str, operand: "Expr | dict") -> Expr:
    if fn not in _UNARY:
        raise ValueError(f"unknown unary fn {fn!r}; one of {sorted(_UNARY)}")
    return Expr({"op": "unary", "fn": fn, "operand": _node(operand)})


def series(key: str, *, kind: str = "model", dimensions: dict | None = None) -> Expr:
    """One logged series of the run.

    ``key`` is the metric key exactly as logged (``"train/loss"``; the slash is part of
    the key, not a kind prefix); ``kind`` matches :meth:`probe.Run.log`'s, default
    ``"model"``.

    ``dimensions`` pins WHICH series when a key has several dimension variants
    (``{"rank": 0}``). None is valid only while ``(kind, key)`` has one variant: the
    server rejects an ambiguous leaf, so a distributed run's per-rank loss needs the pin.
    """
    node: dict = {"op": "series", "kind": kind, "key": key}
    if dimensions is not None:
        node["dimensions"] = dimensions
    return Expr(node)


def const(value: float) -> Expr:
    """A scalar. Rarely needed directly — operators coerce bare numbers."""
    return Expr({"op": "const", "value": float(value)})


def log(operand: "Expr | dict") -> Expr:
    """Natural log."""
    return _unary("log", operand)


def log10(operand: "Expr | dict") -> Expr:
    return _unary("log10", operand)


def exp(operand: "Expr | dict") -> Expr:
    return _unary("exp", operand)


def sqrt(operand: "Expr | dict") -> Expr:
    return _unary("sqrt", operand)


def neg(operand: "Expr | dict") -> Expr:
    """Negation. ``-expr.series("train/loss")`` is the same thing."""
    return _unary("neg", operand)


def ema(operand: "Expr | dict", *, factor: float = 0.6) -> Expr:
    return Expr({"op": "smooth", "fn": "ema", "factor": factor, "operand": _node(operand)})


def sma(operand: "Expr | dict", *, window: int = 10) -> Expr:
    return Expr({"op": "smooth", "fn": "sma", "window": window, "operand": _node(operand)})


def log2(operand: "Expr | dict") -> Expr:
    return _unary("log2", operand)


def log1p(operand: "Expr | dict") -> Expr:
    """log(1 + x), accurate for small x — where a converged loss lives."""
    return _unary("log1p", operand)


def expm1(operand: "Expr | dict") -> Expr:
    """exp(x) − 1, accurate for small x."""
    return _unary("expm1", operand)


def cbrt(operand: "Expr | dict") -> Expr:
    """Cube root. Defined for negatives, unlike sqrt."""
    return _unary("cbrt", operand)


def reciprocal(operand: "Expr | dict") -> Expr:
    return _unary("reciprocal", operand)


def sign(operand: "Expr | dict") -> Expr:
    return _unary("sign", operand)


def floor(operand: "Expr | dict") -> Expr:
    return _unary("floor", operand)


def ceil(operand: "Expr | dict") -> Expr:
    return _unary("ceil", operand)


def round_(operand: "Expr | dict") -> Expr:
    """Trailing underscore: `round` is a builtin worth not shadowing."""
    return _unary("round", operand)


def trunc(operand: "Expr | dict") -> Expr:
    return _unary("trunc", operand)


def sigmoid(operand: "Expr | dict") -> Expr:
    """1/(1+e^-x) — a logit series is only readable once squashed."""
    return _unary("sigmoid", operand)


def tanh(operand: "Expr | dict") -> Expr:
    return _unary("tanh", operand)


def relu(operand: "Expr | dict") -> Expr:
    return _unary("relu", operand)


def sin(operand: "Expr | dict") -> Expr:
    return _unary("sin", operand)


def cos(operand: "Expr | dict") -> Expr:
    return _unary("cos", operand)


def tan(operand: "Expr | dict") -> Expr:
    return _unary("tan", operand)


def asin(operand: "Expr | dict") -> Expr:
    return _unary("asin", operand)


def acos(operand: "Expr | dict") -> Expr:
    return _unary("acos", operand)


def atan(operand: "Expr | dict") -> Expr:
    return _unary("atan", operand)


def sinh(operand: "Expr | dict") -> Expr:
    return _unary("sinh", operand)


def cosh(operand: "Expr | dict") -> Expr:
    return _unary("cosh", operand)


def _binary_fn(fn: str, left: Any, right: Any) -> Expr:
    if fn not in _BINARY:
        raise ValueError(f"unknown binary fn {fn!r}; one of {sorted(_BINARY)}")
    return Expr({"op": "binary", "fn": fn, "left": _node(left), "right": _node(right)})


def min_(left: Any, right: Any) -> Expr:
    """Trailing underscore: `min`/`max` are builtins worth not shadowing."""
    return _binary_fn("min", left, right)


def max_(left: Any, right: Any) -> Expr:
    return _binary_fn("max", left, right)


def mod(left: Any, right: Any) -> Expr:
    return _binary_fn("mod", left, right)


def hypot(left: Any, right: Any) -> Expr:
    return _binary_fn("hypot", left, right)


def atan2(left: Any, right: Any) -> Expr:
    return _binary_fn("atan2", left, right)


def pow_(left: Any, right: Any) -> Expr:
    """`a ** b` builds this too."""
    return _binary_fn("pow", left, right)


def cmp(fn: str, left: Any, right: Any) -> Expr:
    """A comparison as a 0/1 mask. Built by `a > b` and friends."""
    if fn not in _CMP:
        raise ValueError(f"unknown cmp fn {fn!r}; one of {sorted(_CMP)}")
    return Expr({"op": "cmp", "fn": fn, "left": _node(left), "right": _node(right)})


def cond(when: Any, then: Any, otherwise: Any) -> Expr:
    """Piecewise selection — the divide-by-zero guard:

        expr.cond(b != 0, a / b, 0)

    keeps the step at 0 instead of dropping it as non-finite.
    """
    return Expr(
        {
            "op": "cond",
            "when": _node(when),
            "then": _node(then),
            "otherwise": _node(otherwise),
        }
    )


def clamp(operand: Any, lo: Any, hi: Any) -> Expr:
    """Bound a curve to [lo, hi]. Inverted bounds evaluate to NaN, not a
    silently chosen edge."""
    return Expr(
        {"op": "clamp", "operand": _node(operand), "lo": _node(lo), "hi": _node(hi)}
    )


def coalesce(operand: Any, fallback: Any) -> Expr:
    """Replace a non-finite result with `fallback` — the only node that stops
    NaN propagating."""
    return Expr(
        {"op": "coalesce", "operand": _node(operand), "fallback": _node(fallback)}
    )


# -- non-pointwise: running values, windows, whole-curve statistics ---------
def scan(fn: str, operand: Any) -> Expr:
    """A running value over the step axis."""
    if fn not in _SCAN:
        raise ValueError(f"unknown scan fn {fn!r}; one of {sorted(_SCAN)}")
    return Expr({"op": "scan", "fn": fn, "operand": _node(operand)})


def cumsum(operand: Any) -> Expr:
    """Running total — tokens consumed, cumulative reward."""
    return scan("cumsum", operand)


def cumprod(operand: Any) -> Expr:
    return scan("cumprod", operand)


def cummax(operand: Any) -> Expr:
    """Best so far. The most-asked-for derived curve."""
    return scan("cummax", operand)


def cummin(operand: Any) -> Expr:
    """Worst so far."""
    return scan("cummin", operand)


def delta(operand: Any) -> Expr:
    """Step-over-step change. The first step has no predecessor and is NaN."""
    return scan("delta", operand)


def window(fn: str, operand: Any, *, size: int = 10) -> Expr:
    """A trailing-window statistic. Partial windows at the start use what is
    available; non-finite values are excluded from the windows they touch."""
    if fn not in _WINDOW:
        raise ValueError(f"unknown window fn {fn!r}; one of {sorted(_WINDOW)}")
    return Expr({"op": "window", "fn": fn, "window": size, "operand": _node(operand)})


def rolling_std(operand: Any, *, size: int = 10) -> Expr:
    return window("std", operand, size=size)


def rolling_min(operand: Any, *, size: int = 10) -> Expr:
    return window("min", operand, size=size)


def rolling_max(operand: Any, *, size: int = 10) -> Expr:
    return window("max", operand, size=size)


def shift(operand: Any, by: int) -> Expr:
    """Move a curve along the step axis. Positive `by` looks BACK (x[i-by]).
    Steps with no counterpart are NaN — never wrapped, never clamped."""
    return Expr({"op": "shift", "by": int(by), "operand": _node(operand)})


def reduce(fn: str, operand: Any) -> Expr:
    """Collapse the whole curve to one number, broadcast over every step.

    Makes normalization expressible (:func:`zscore`, :func:`normalize`). Non-finite
    values are excluded from the statistic.

    SCOPE: the statistic covers the ALIGNED grid (inner join across every series the
    expression names), not the operand's whole stored curve: `zscore(a)` alone uses
    all of `a`; add a sparse `b` and it uses the steps they share. Same for
    :func:`scan` and :func:`window`."""
    if fn not in _REDUCE:
        raise ValueError(f"unknown reduce fn {fn!r}; one of {sorted(_REDUCE)}")
    return Expr({"op": "reduce", "fn": fn, "operand": _node(operand)})


def zscore(operand: Any) -> Expr:
    """Standardize against the curve's own mean and spread.

    Sugar over `(x - reduce(mean, x)) / reduce(std, x)`."""
    node = _node(operand)
    return (Expr(node) - reduce("mean", node)) / reduce("std", node)


def normalize(operand: Any) -> Expr:
    """Rescale to [0, 1] against the curve's own min and max."""
    node = _node(operand)
    low = reduce("min", node)
    return (Expr(node) - low) / (reduce("max", node) - low)


def spec(expression: "Expr | dict") -> dict:
    """Wrap an expression as a view spec and validate it.

    Accepts an ``Expr``, a bare node dict, or an already-wrapped
    ``{"expression": ...}`` (agent JSON, a spec file, a builder chain). Built through
    the generated ``MetricViewSpec``, so a bad node fails naming the field, not as a 422.
    """
    if isinstance(expression, dict) and "expression" in expression and "op" not in expression:
        body = expression
    else:
        body = {"expression": _node(expression)}
    return MetricViewSpec.model_validate(body).model_dump(mode="json", exclude_none=True)
