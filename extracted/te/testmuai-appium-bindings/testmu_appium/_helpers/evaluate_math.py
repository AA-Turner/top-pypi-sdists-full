"""evaluate_math() — evaluate a recorded MathmaticAction.mathmatic_tree.

The tree is the V3 operator/operands shape the code generator emits:

    {"operator": "multiply",
     "operands": ["{{price}}", {"operator": "add", "operands": ["1", "2"]}]}

Operands are numeric literals, `{{var}}` / `${var}` placeholders, or nested trees.
Evaluation is inlined here so the binding has no runtime dependency on the code
generator.

Three rules differ deliberately from the selenium sibling's evaluator, each closing a
silent-wrong-answer path:

- `pow` is arity-checked like the other binary operators, so a three-operand pow tree
  raises instead of ignoring the extra operands.
- A tree with no `operator` key raises rather than defaulting to `add`.
- Operands resolve through `_vars.var()` rather than by indexing the variable store,
  so `${param}` reads test parameters here exactly as it does in `math()`.

`math(expression)` remains available for the flat-string form; this is the entry
point the generator emits against.
"""
import logging
import operator as _op
from functools import reduce

from testmu_appium._vars import set_var, var

_log = logging.getLogger("testmu_appium")

OPERATORS = frozenset({"add", "subtract", "multiply", "divide", "mod", "pow", "negate", "abs"})

#: Operators whose operand count is fixed, `pow` included. A recorded tree with the
#: wrong arity is a producer bug — evaluating it anyway would silently return a
#: plausible number.
_BINARY = ("subtract", "divide", "mod", "pow")
_UNARY = ("negate", "abs")

#: The two template spellings an operand may use. Both resolve through `_vars.var()`,
#: which is what makes `${param}` work here the way it does in `math()`.
_TEMPLATE_DELIMITERS = (("{{", "}}"), ("${", "}"))


def _as_number(value) -> float:
    if isinstance(value, bool):
        raise ValueError(f"Non-numeric operand encountered: {value!r}")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            raise ValueError(f"Non-numeric operand encountered: {value!r}") from None
    raise ValueError(f"Unsupported operand type: {type(value).__name__}")


def _resolve_operand(operand: str):
    """Resolve one template operand through `_vars.var()`.

    Going through `var()` rather than indexing the variable store directly is what
    makes `${param}` resolve here: `${...}` reads test_params first, which the store
    alone does not carry. `var()` also brings the namespace resolvers ({{global.*}},
    environment, TOTP) and dotted/bracket traversal.

    `var()` returns the template unchanged when it cannot resolve it; that is the
    miss, and it becomes a KeyError rather than the literal text "{{price}}" and then
    a non-numeric-operand error.
    """
    text = operand.strip()
    if not any(text.startswith(o) and text.endswith(c) for o, c in _TEMPLATE_DELIMITERS):
        return text
    resolved = var(text)
    if isinstance(resolved, str) and resolved == text:
        raise KeyError(f"Variable {text!r} not found in variables")
    return resolved


def _evaluate_tree(tree: dict) -> float:
    if "operator" not in tree:
        raise ValueError(
            f"math tree carries no operator: {tree!r}. Defaulting to 'add' would turn "
            f"a malformed tree into a plausible sum."
        )
    operator_name = tree["operator"]
    if operator_name not in OPERATORS:
        raise ValueError(f"Unsupported math operator: {operator_name!r}")

    resolved = []
    for operand in tree.get("operands", []):
        if isinstance(operand, dict) and "operator" in operand:
            resolved.append(_as_number(_evaluate_tree(operand)))
        elif isinstance(operand, str):
            resolved.append(_as_number(_resolve_operand(operand)))
        else:
            resolved.append(_as_number(operand))

    if operator_name in _BINARY and len(resolved) != 2:
        raise ValueError(
            f"{operator_name} requires exactly 2 operands, got {len(resolved)}"
        )
    if operator_name in _UNARY and len(resolved) != 1:
        raise ValueError(
            f"{operator_name} requires exactly 1 operand, got {len(resolved)}"
        )

    if operator_name == "add":
        return sum(resolved)
    if operator_name == "subtract":
        return resolved[0] - resolved[1]
    if operator_name == "multiply":
        return reduce(_op.mul, resolved, 1.0)
    if operator_name == "divide":
        if resolved[1] == 0:
            raise ZeroDivisionError("Division by zero")
        return resolved[0] / resolved[1]
    if operator_name == "mod":
        if resolved[1] == 0:
            raise ZeroDivisionError("Modulo by zero")
        return resolved[0] % resolved[1]
    if operator_name == "pow":
        return resolved[0] ** resolved[1]
    if operator_name == "negate":
        return -resolved[0]
    return abs(resolved[0])


def evaluate_math(*, tree: dict, output_variable: str = "", description: str = "") -> float:
    """Evaluate a recorded math tree against the current variable store.

    Args:
        tree: MathmaticAction.mathmatic_tree — `{"operator", "operands"}`, nestable.
        output_variable: When non-empty, the result is written via `set_var`.
        description: Step description (logging only).

    Returns:
        The numeric result as a float.

    Raises:
        ValueError: missing operator, unknown operator, wrong operand count, or a
            non-numeric operand.
        KeyError: an operand references a variable that cannot be resolved.
        ZeroDivisionError: division or modulo by zero.
    """
    if not isinstance(tree, dict):
        raise ValueError(f"evaluate_math requires a mathmatic_tree dict, got {tree!r}")

    _log.info(
        "[evaluate_math] operator=%s operands=%d",
        tree.get("operator", "?"), len(tree.get("operands", [])),
    )
    result = _evaluate_tree(tree)
    _log.info("[evaluate_math] result=%r", result)
    if output_variable:
        set_var(output_variable, result)
    return result
