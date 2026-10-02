"""math() — safe evaluation of an arithmetic expression string.

The V4 mobile export bakes a math step as a plain arithmetic expression string
(e.g. ``"{{price}} * {{qty}} + 5"``) rather than the operator/operands tree the V3
selenium/playwright siblings evaluate. ``{{var}}``/``${var}`` tokens are resolved
via ``_vars.var()`` first; the resulting text is parsed as a Python expression AST
and walked with an operator allow-list (``+ - * / % **``, unary ``+``/``-``,
numeric literals and parentheses only) — never handed to ``eval()``. Any other
syntax (names, calls, subscripts, comprehensions, ...) is rejected.
"""
import ast
import logging
import operator
from numbers import Real
from typing import Union

from testmu_appium._vars import set_var, var

_log = logging.getLogger("testmu_appium")

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_ZERO_DIVISOR_OPS = (ast.Div, ast.Mod)
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

#: Ceiling on the decimal digit count of an INTEGER power.
#:
#: Python's int ** int is exact and unbounded, so it does not overflow — it
#: allocates. `9 ** 9 ** 9` asks for a ~370-million-digit integer, which pegs a core
#: and grows memory until the process is killed; there is no exception to catch and
#: no timeout to hit, so a recorded expression could wedge a whole test run.
#: Anything a recorded arithmetic step legitimately computes fits inside this.
#: Float powers are not bounded here — they overflow to an exception in constant
#: time, which is already a clean failure.
_MAX_POW_RESULT_DIGITS = 100


def _guarded_pow(left, right, expression: str):
    """`left ** right`, refusing integer powers whose result would be enormous."""
    if isinstance(left, int) and isinstance(right, int) and right > 0 and abs(left) > 1:
        # log10 of the magnitude, without materialising the result: an integer's
        # bit_length gives its size directly.
        digits = right * (abs(left).bit_length() - 1) * 0.30103
        if digits > _MAX_POW_RESULT_DIGITS:
            raise ValueError(
                f"math(): exponentiation in {expression!r} would produce a number with "
                f"roughly {int(digits)} digits, over the {_MAX_POW_RESULT_DIGITS}-digit "
                f"limit; refusing to evaluate it"
            )
    try:
        return operator.pow(left, right)
    except OverflowError as exc:
        raise ValueError(
            f"math(): exponentiation in {expression!r} overflowed: {exc}"
        ) from exc


def _eval_node(node: ast.AST, expression: str) -> Union[int, float]:
    """Recursively evaluate one allow-listed AST node. Raises ValueError on
    anything outside the arithmetic subset, ZeroDivisionError on a literal
    zero divisor for ``/`` or ``%``."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, expression)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, Real):
            raise ValueError(
                f"math(): non-numeric literal {node.value!r} in expression {expression!r}"
            )
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left = _eval_node(node.left, expression)
        right = _eval_node(node.right, expression)
        if type(node.op) in _ZERO_DIVISOR_OPS and right == 0:
            raise ZeroDivisionError(
                f"math(): division/modulo by zero in expression {expression!r}"
            )
        if isinstance(node.op, ast.Pow):
            return _guarded_pow(left, right, expression)
        return _BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand, expression))
    raise ValueError(
        f"math(): unsupported expression syntax in {expression!r} "
        f"(only + - * / % ** and parentheses over numeric literals are allowed)"
    )


def _safe_eval_arithmetic(expression: str) -> Union[int, float]:
    """Parse ``expression`` as a restricted arithmetic AST and evaluate it."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(
            f"math(): not a valid arithmetic expression: {expression!r}"
        ) from exc
    return _eval_node(tree, expression)


def math(expression: str, *, output_variable: str = "", description: str = "") -> Union[float, int]:
    """Evaluate an arithmetic expression against the current variable store.

    ``{{var}}``/``${var}`` tokens in ``expression`` are resolved via ``var()``
    first. A whole-string single template (e.g. ``"{{x}}"``) resolves to its
    native stored value directly; anything else is treated as text and parsed
    as a restricted arithmetic expression (numeric literals, ``+ - * / % **``,
    unary sign, parentheses — never ``eval()``).

    Args:
        expression: Arithmetic expression, optionally containing ``{{var}}``/
            ``${var}`` tokens.
        output_variable: When non-empty, the result is written via
            ``set_var(output_variable, result)``.
        description: Human-readable step description (logging only).

    Returns:
        The numeric result — ``int`` when every operation stayed integral,
        ``float`` once a division or a float literal is involved (native
        Python numeric promotion).

    Raises:
        ValueError: ``expression`` is not a valid arithmetic expression, resolves
            to a non-numeric value, or asks for an integer power whose result
            would exceed ``_MAX_POW_RESULT_DIGITS`` digits.
        ZeroDivisionError: ``expression`` divides or mods by a literal zero.
    """
    resolved = var(expression)

    if isinstance(resolved, bool) or not isinstance(resolved, (int, float, str)):
        raise ValueError(f"math(): non-numeric variable value {resolved!r}")

    result = resolved if isinstance(resolved, (int, float)) else _safe_eval_arithmetic(resolved)

    _log.info("[math] expression=%r result=%r", expression, result)
    if output_variable:
        set_var(output_variable, result)
    return result
