"""Math evaluation helper — deterministic evaluation of math expression trees.

Inlines the math tree evaluation logic so that testmu has zero dependency
on the code generator at runtime.
"""

import logging
import re
from functools import reduce
import operator as _op

_log = logging.getLogger("testmu_selenium")

# Supported operators
_OPERATORS = frozenset(
    {"add", "subtract", "multiply", "divide", "mod", "pow", "negate", "abs"}
)

_BRACKET_RE = re.compile(r"(\w+)\[(\d+)\]")


def _as_number(value):
    """Convert value to float; raise ValueError if not numeric."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except Exception:
            raise ValueError(f"Non-numeric operand encountered: {value!r}")
    raise ValueError(f"Unsupported operand type: {type(value).__name__}")


def _access_nested_value(variable_dump, name):
    """Access nested values using dot/bracket notation (matches Mathmatic._access_nested_value)."""
    keys = name.split(".")
    value = variable_dump

    for key in keys:
        while "[" in key and "]" in key:
            base_key, index = key.split("[", 1)
            index = int(index.split("]")[0])
            value = value[base_key] if base_key else value
            value = value[index]
            key = key[key.index("]") + 1 :]

        if key:
            value = value[key]
    return value


def _resolve_operand(operand_str, variables):
    """Resolve a placeholder string to its value, returning (resolved_value, used_variables_dict)."""
    s = operand_str.strip()
    if s.startswith("{{") and s.endswith("}}"):
        key = s[2:-2].strip()
        try:
            result = _access_nested_value(variables, key)
            return result, {key: result}
        except (KeyError, TypeError, IndexError) as e:
            raise KeyError(f"Variable '{key}' not found in variables: {e}")
    if s.startswith("${") and s.endswith("}"):
        key = s[2:-1].strip()
        try:
            result = _access_nested_value(variables, key)
            return result, {key: result}
        except (KeyError, TypeError, IndexError) as e:
            raise KeyError(f"Variable '{key}' not found in variables: {e}")
    return s, {}


def _evaluate_tree(tree, variables):
    """Recursively evaluate a math expression tree.

    Args:
        tree: dict with 'operator' and 'operands' keys. Operands can be
              numeric strings, {{var}} placeholders, or nested tree dicts.
        variables: dict for placeholder resolution.

    Returns:
        (float_result, used_variables_dict)
    """
    op = tree.get("operator", "add")
    if op not in _OPERATORS:
        raise ValueError(f"Unsupported math operator: {op!r}")

    raw_operands = tree.get("operands", [])
    resolved = []
    used_variables = {}

    for operand in raw_operands:
        if isinstance(operand, dict) and "operator" in operand:
            # Nested tree
            result, child_vars = _evaluate_tree(operand, variables)
            resolved.append(_as_number(result))
            used_variables.update(child_vars)
        elif isinstance(operand, str):
            operand_value, operand_vars = _resolve_operand(operand, variables)
            used_variables.update(operand_vars)
            resolved.append(_as_number(operand_value))
        else:
            resolved.append(_as_number(operand))

    # Validate operand counts for operators that require specific counts
    if op in ("subtract", "divide", "mod") and len(resolved) != 2:
        raise ValueError(f"{op} requires exactly 2 operands, got {len(resolved)}")
    if op in ("negate", "abs") and len(resolved) != 1:
        raise ValueError(f"{op} requires exactly 1 operand, got {len(resolved)}")

    if op == "add":
        return sum(resolved), used_variables
    elif op == "subtract":
        return resolved[0] - resolved[1], used_variables
    elif op == "multiply":
        return reduce(_op.mul, resolved, 1.0), used_variables
    elif op == "divide":
        if resolved[1] == 0:
            raise ZeroDivisionError("Division by zero")
        return resolved[0] / resolved[1], used_variables
    elif op == "mod":
        if resolved[1] == 0:
            raise ZeroDivisionError("Modulo by zero")
        return resolved[0] % resolved[1], used_variables
    elif op == "pow":
        return resolved[0] ** resolved[1], used_variables
    elif op == "negate":
        return -resolved[0], used_variables
    elif op == "abs":
        return abs(resolved[0]), used_variables
    else:
        raise ValueError(f"Unsupported operator: {op}")


def evaluate_math(mathmatic_tree: dict) -> float:
    """Evaluate a math expression tree against the current variable store.

    Args:
        mathmatic_tree: Dict with 'operator' and 'operands' (may be nested).
            Operands can be numeric strings, {{var}} placeholders, or
            nested math dicts.

    Returns:
        Numeric result as a float.
    """
    from testmu_selenium._vars import _variable_store

    _log.info("    [evaluate_math] operator=%s operands=%d",
              mathmatic_tree.get("operator", "?"),
              len(mathmatic_tree.get("operands", [])))
    result, _ = _evaluate_tree(mathmatic_tree, _variable_store)
    _log.info("    [evaluate_math] result=%r", result)
    return result
