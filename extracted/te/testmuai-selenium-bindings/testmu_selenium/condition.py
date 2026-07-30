from __future__ import annotations

import ast
import enum
import json
import operator as _op
import re
import unicodedata
from functools import reduce
from typing import Any, Callable, List, Optional, Union


_HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_RGB_COLOR_RE = re.compile(
    r"^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$",
    re.IGNORECASE,
)


def _normalize_color(value: Any) -> Optional[tuple]:
    """Parse a CSS colour string into a canonical ``(r, g, b, alpha)`` tuple.

    Handles ``#rgb`` / ``#rgba`` / ``#rrggbb`` / ``#rrggbbaa`` and
    ``rgb(...)`` / ``rgba(...)``. Returns ``None`` for anything that isn't one
    of these, so callers fall back to plain comparison. Colour *names* are not
    normalized here — the runtime attribute paths emit hex/rgb, not names.

    Motivates: a ``background_color`` query returns the computed style
    ``rgb(245, 245, 245)`` while the authored expected is ``#f5f5f5`` — the same
    colour, so ``equals`` must compare by value, not raw string.
    """
    if not isinstance(value, str):
        return None
    s = value.strip()

    m = _HEX_COLOR_RE.match(s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        a = round(int(h[6:8], 16) / 255, 3) if len(h) == 8 else 1.0
        return (r, g, b, a)

    m = _RGB_COLOR_RE.match(s)
    if m:
        try:
            r, g, b = (int(round(float(m.group(i)))) for i in (1, 2, 3))
        except ValueError:
            return None
        if not all(0 <= c <= 255 for c in (r, g, b)):
            return None
        a = round(float(m.group(4)), 3) if m.group(4) is not None else 1.0
        return (r, g, b, a)

    return None


def _normalize_bool_str(left: Any, right: Any):
    """Normalize a bool-vs-string equality pair, mirroring V2.

    A JS step that returns a boolean is stored as Python ``True``/``False``,
    while the authored expected operand is the string ``'true'``/``'false'``.
    When exactly one side is a ``bool`` and the other a ``str``, compare them as
    lowercased strings so ``True == 'true'`` (and ``'True'``) holds. Returns the
    pair to compare, normalized only when applicable so all other comparisons
    are untouched.
    """
    if (isinstance(left, bool) and isinstance(right, str)) or (
        isinstance(left, str) and isinstance(right, bool)
    ):
        return str(left).lower(), str(right).lower()
    return left, right


def _try_parse_json(value: Any) -> Any:
    """Parse a JSON string into a Python object, returning the value unchanged otherwise.

    V2-parity: V2's _json_obj/_json_arr helpers first tried json.loads (then
    ast.literal_eval) on string operands so that a variable holding a serialised
    dict or list — e.g. get_cookies returning '{"key": "val"}' — would satisfy
    json_* assertion checks.  Parse failures are deliberately NOT swallowed — they
    raise, matching V2 (whose ast.literal_eval propagates) and the playwright-python
    / java / csharp siblings, so a malformed operand fails loudly rather than
    silently evaluating to False. A wrong-type-but-valid-JSON operand is handled by
    each branch's isinstance guard (returns False), not here.
    """
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return ast.literal_eval(value)
    return value


_SMART_PUNCT_MAP = str.maketrans({
    "‘": "'", "’": "'",   # curly single quotes
    "“": '"', "”": '"',   # curly double quotes
    " ": " ",                  # non-breaking space
    "​": "", "‌": "", "‍": "", "﻿": "",  # zero-width / BOM
})


def _normalize_text(s: Any, case_insensitive: bool = False, ascii_fold: bool = True) -> str:
    """Canonicalize text for substring/prefix/suffix matching, matching V2.

    Folds accents/ligatures (NFKD + drop combining marks), maps smart
    punctuation and invisible characters, collapses whitespace, and optionally
    case-folds. So `contains`/`start_with`/`end_with` match the way authoring
    (V2) evaluated them — e.g. "Café Menu" contains "cafe".
    """
    s = str(s)
    if not s:
        return s
    if ascii_fold:
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
    else:
        s = unicodedata.normalize("NFKC", s)
    s = s.translate(_SMART_PUNCT_MAP)
    s = re.sub(r"\s+", " ", s).strip()
    if case_insensitive:
        s = s.casefold()
    return s


def _are_lengths_equal(value1: str, value2: str) -> bool:
    """V2 length_equals: a numeric operand is the number itself, else its len().

    V2 keys on ``str.isdigit()``; under V3 a numeric operand may arrive as a
    float (``_resolve`` coerces ``"5"`` -> ``5.0``), so an integral-float string
    is treated as that number too — otherwise ``len("5.0")`` would mismatch.
    """
    def _length(val: str):
        s = str(val)
        try:
            f = float(s)
        except (TypeError, ValueError):
            return len(s)
        if f.is_integer():
            return int(f)
        return len(s)
    return _length(value1) == _length(value2)


_TYPE_NAME_MAP = {
    "int": int, "str": str, "float": float, "bool": bool, "boolean": bool,
    "list": list, "dict": dict, "tuple": tuple, "set": set,
}


def _are_types_equal(value1: str, value2: str) -> bool:
    """V2 type_equals: map type-name strings (incl. 'boolean'->bool) to types.

    'true'/'false' substrings imply bool. Otherwise recover the literal's type
    via ast.literal_eval (safe; never eval()), defaulting to str.
    """
    def _to_type(val: str):
        v = val.strip().lower()
        if "true" in v or "false" in v:
            return bool
        if v in _TYPE_NAME_MAP:
            return _TYPE_NAME_MAP[v]
        try:
            return type(ast.literal_eval(val))
        except Exception:
            return str
    return _to_type(value1) == _to_type(value2)


def _string_to_float(value: Any):
    """V2 string_to_float: currency-tolerant numeric coercion, reproduced verbatim.

    Already-numeric values pass through. A plain ``float()`` is tried first
    (handles scientific notation). On ValueError, keep only digits and ``.``,
    negating if a ``-`` appears anywhere; an all-non-numeric string yields 0. A
    multi-dot residue (e.g. ``"1.2.3"``) makes ``float()`` raise ValueError
    UNCAUGHT -- V2 crashed here and that loud failure is preserved.
    """
    if isinstance(value, (float, int)):
        return value
    try:
        return float(value)
    except ValueError:
        is_negative = "-" in value
        a = "".join(c for c in value if c.isdigit() or c == ".")
        if a == "":
            return 0
        result = float(a)
        if is_negative:
            result = -result
        return result


def _coerce_numeric_pair(left: Any, right: Any):
    """V2 mixed exact-type coercion: when EXACTLY one operand is a real int/float
    and the other a str, string_to_float BOTH so a number compares against its
    numeric string. An exact ``type()`` test excludes bool (an int subclass).
    Both-strings and both-numbers are returned untouched (no lexical coercion),
    so ``"007" != "7"`` and ``"1.0" != "1"``.
    """
    if (type(left) in (int, float) and type(right) is str) or (
        type(left) is str and type(right) in (int, float)
    ):
        return _string_to_float(left), _string_to_float(right)
    return left, right


class ResolvedCondition:
    def __init__(self, left_operand: str, operator: PossibleCondition, right_operand: str):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand


    def to_dict(self):
        return {
            "left_operand": self.left_operand,
            "operator": self.operator.value,
            "right_operand": self.right_operand,
        }

    @classmethod
    def from_string(cls, condition: str):
        # split the condition into left_operand, operator, right_operand
        # if the condition is not a string, return the condition
        left_operand, _operator, right_operand = condition.split()
        operator = PossibleCondition(_operator.strip())
        return cls(left_operand.strip(), operator, right_operand.strip())


    @classmethod
    def from_json(cls, json_data):
        return cls(
            left_operand = json_data.get('left_operand', ''),
            operator = PossibleCondition(json_data.get('operator', '')),
            right_operand = json_data.get('right_operand', ''),
        )

    @classmethod
    def create_string_from_condition(cls, conditions: list[ResolvedCondition], connectors: list[ConcatenationOperator]):
        condition_string = ""
        for idx, condition in enumerate(conditions):
            condition_string += str(condition)
            if idx < len(connectors):
                condition_string += connectors[idx].value
        return condition_string


    def __str__(self):
        return f"{self.left_operand} {self.operator.value} {self.right_operand}"

    def __eq__(self, other):
        if not isinstance(other, ResolvedCondition):
            return False
        return self.left_operand == other.left_operand and self.operator == other.operator and self.right_operand == other.right_operand

class Condition:
    def __init__(
        self,
        conditions: list[ResolvedCondition],
        connectors: list[ConcatenationOperator],
        is_v3: bool = False,
    ):
        self.connectors = connectors
        self.conditions = conditions
        # V3 mode: text ops are case-insensitive + unicode-folded; AND binds
        # tighter than OR (A OR B AND C == A OR (B AND C)).  Default False
        # preserves byte-identical V4 behavior for all non-V3 callers.
        self.is_v3 = is_v3

    def _resolve_placeholder(self, s: str, variables: dict, get_variable_value: Callable, *args, **kwargs):
        if get_variable_value is not None and isinstance(get_variable_value, Callable):
            result = get_variable_value(s, variables, *args, **kwargs)
            return result, {s: result}
        s = s.strip()
        if s.startswith("{{") and s.endswith("}}"):
            key = s[2:-2].strip()
            try:
                result = self._access_nested_value(variables, key)
                return result, {key: result}
            except (KeyError, TypeError, IndexError) as e:
                raise KeyError(f"Variable '{key}' not found in variables: {e}")
        if s.startswith("${") and s.endswith("}"):
            key = s[2:-1].strip()
            try:
                result = self._access_nested_value(variables, key)
                return result, {key: result}
            except (KeyError, TypeError, IndexError) as e:
                raise KeyError(f"Variable '{key}' not found in variables: {e}")
        return s, {}  # not a placeholder


    def _is_numeric(self, val):
        if isinstance(val, (int, float)):
            return True
        if isinstance(val, str):
            val = val.strip()
            if val.isdigit():
                return True
            try:
                float(val)
                return True
            except ValueError:
                return False
        return False

    def _to_numeric(self, val):
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            val = val.strip()
            # Try int first (so "10" becomes int, not float)
            try:
                return int(val)
            except ValueError:
                pass
            try:
                return float(val)
            except ValueError:
                return None
        return None

    def _clean_string(self, s: str) -> str:
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        return s

    def _is_typecast_required(self, left_operand: Any, right_operand: Any) -> tuple[Any, Any]:
        """Coerce mixed string/number operands so comparisons use values, not
        string forms (e.g. "100" > "99" or 5 == "5"). Ported from the V2
        condition parser for V3 parity. A genuinely
        non-numeric operand is left unchanged so an invalid ordering comparison
        still raises TypeError rather than passing silently.
        """
        left_is_str = isinstance(left_operand, str)
        right_is_str = isinstance(right_operand, str)
        left_is_numeric = self._is_numeric(left_operand)
        right_is_numeric = self._is_numeric(right_operand)

        if left_is_numeric and right_is_numeric:
            return self._to_numeric(left_operand), self._to_numeric(right_operand)

        if left_is_str:
            left_operand = self._clean_string(left_operand)
        if right_is_str:
            right_operand = self._clean_string(right_operand)

        if left_is_str and right_is_numeric:
            try:
                casted_left = float(left_operand.strip())
                if isinstance(right_operand, int) and casted_left.is_integer():
                    return int(casted_left), right_operand
                return casted_left, right_operand
            except (ValueError, AttributeError):
                return left_operand, right_operand

        if right_is_str and left_is_numeric:
            try:
                casted_right = float(right_operand.strip())
                if isinstance(left_operand, int) and casted_right.is_integer():
                    return left_operand, int(casted_right)
                return left_operand, casted_right
            except (ValueError, AttributeError):
                return left_operand, right_operand

        return left_operand, right_operand

    def _cmp(self, x: Any) -> str:
        """Normalize a text operand for substring/prefix/suffix comparison.

        V3 mode: accent-fold + case-fold (matches V2 ``_compare_atomic``).
        V4 mode: plain ``str()`` — byte-identical to the original behavior.
        """
        return _normalize_text(x, case_insensitive=True) if self.is_v3 else str(x)

    def _eval_condition(self, operator: PossibleCondition, left_operand: Any, right_operand: Any)->bool:
        # Coerce numeric-looking operands before comparing (V2 condition-parser parity) so
        # generated conditions compare values rather than their string forms.
        # left/right are deliberately Any: they hold runtime-resolved variable
        # values whose type is only known at evaluation time.
        left: Any
        right: Any
        left, right = self._is_typecast_required(left_operand, right_operand)
        if isinstance(left, bool) and isinstance(right, str):
            lowered = right.strip().lower()
            if lowered in ("true", "false"):
                right = lowered == "true"
        elif isinstance(right, bool) and isinstance(left, str):
            lowered = left.strip().lower()
            if lowered in ("true", "false"):
                left = lowered == "true"
        if operator == PossibleCondition.EQUALS:
            return left == right
        if operator == PossibleCondition.NOT_EQUALS:
            return left != right
        if operator == PossibleCondition.GREATER_THAN:
            return left > right
        if operator == PossibleCondition.LESS_THAN:
            return left < right
        if operator == PossibleCondition.GREATER_THAN_OR_EQUALS:
            return left >= right
        if operator == PossibleCondition.LESS_THAN_OR_EQUALS:
            return left <= right
        if operator == PossibleCondition.CONTAINS:
            return self._cmp(right) in self._cmp(left)
        if operator == PossibleCondition.NOT_CONTAINS:
            return self._cmp(right) not in self._cmp(left)
        if operator == PossibleCondition.STARTS_WITH:
            return self._cmp(left).startswith(self._cmp(right))
        if operator == PossibleCondition.ENDS_WITH:
            return self._cmp(left).endswith(self._cmp(right))
        raise ValueError(f"Unsupported condition: {operator}")

    def evaluate(self, variables: dict, get_variable_value: Callable, *args, **kwargs)->(bool, dict):
        used_variables = {}
        results = []
        for condition in self.conditions:
            _used_variables = {}
            _left_operand, left_operand_variables = self._resolve_placeholder(condition.left_operand, variables, get_variable_value, *args, **kwargs)
            _right_operand, right_operand_variables = self._resolve_placeholder(condition.right_operand, variables, get_variable_value, *args, **kwargs)
            result = self._eval_condition(condition.operator, _left_operand, _right_operand)
            _used_variables.update(left_operand_variables)
            _used_variables.update(right_operand_variables)
            used_variables.update(_used_variables)
            results.append(result)

        # V3 precedence fold: AND binds tighter than OR so
        # A OR B AND C == A OR (B AND C).  Accumulate AND-groups left-to-right;
        # each OR flushes the running group into or_groups and starts a new one.
        # any(or_groups) short-circuits like Python's built-in `or`.
        if self.is_v3:
            if not results:
                return True, used_variables
            current = results[0]
            or_groups: list = []
            for idx, connector in enumerate(self.connectors):
                operand = results[idx + 1] if (idx + 1) < len(results) else False
                if connector == ConcatenationOperator.AND:
                    current = current and operand
                elif connector == ConcatenationOperator.OR:
                    or_groups.append(current)
                    current = operand
                else:
                    raise ValueError(f"Unsupported connector: {connector}")
            or_groups.append(current)
            return any(or_groups), used_variables

        final_result = results[0] if results else True
        # final_result is seeded with results[0]; connector idx joins it with the
        # NEXT result (results[idx + 1]). Reading results[idx] here double-counts
        # results[0] and silently drops the last condition (only N-1 of N honoured).
        for idx, connector in enumerate(self.connectors):
            if connector == ConcatenationOperator.AND:
                final_result = final_result and results[idx + 1]
            elif connector == ConcatenationOperator.OR:
                final_result = final_result or results[idx + 1]
            else:
                raise ValueError(f"Unsupported connector: {connector}")
        return final_result, used_variables

    def to_dict(self):
        return {
            "connectors": [connector.value for connector in self.connectors],
            "conditions": [condition.to_dict() for condition in self.conditions],
        }

class PossibleCondition(enum.Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUALS = ">="
    LESS_THAN_OR_EQUALS = "<="
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"

    # No _missing_ fallback: an unrecognized operator must raise ValueError
    # rather than silently defaulting to EQUALS and producing a wrong verdict.

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, PossibleCondition):
            return False
        return self.value == other.value



class MathOperationOperator(enum.Enum):
    #add|subtract|multiply|divide|mod|pow|negate|abs
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    MODULUS = "mod"
    POWER = "pow"
    NEGATE = "negate"
    ABS = "abs"



class Mathmatic:
    def __init__(self, operator: MathOperationOperator, operands: list[Union[str, Mathmatic]]): # operator can be int (in form of string) or placeholder {{}} / ${} in form of string or MathOperation object
        self.operator = operator
        self.operands = operands
        # add validation check if operator is subtract or divide, then the length of operands should be 2
        if self.operator in [MathOperationOperator.SUBTRACT, MathOperationOperator.DIVIDE, MathOperationOperator.MODULUS]:
            if len(self.operands) != 2:
                raise ValueError("Subtract and Divide operators require exactly 2 operands")
        # add validation check if operator is negate, then the length of operands should be 1
        if self.operator == MathOperationOperator.NEGATE:
            if len(self.operands) != 1:
                raise ValueError("Negate operator require exactly 1 operand")
        # add validation check if operator is abs, then the length of operands should be 1
        if self.operator == MathOperationOperator.ABS:
            if len(self.operands) != 1:
                raise ValueError("Abs operator require exactly 1 operand")


    def to_dict(self):
        return {
            "operator": self.operator.value,
            "operands": [operand.to_dict() if isinstance(operand, Mathmatic) else operand for operand in self.operands],
        }


    def update_variable_scope(self, new_variable_reference: str, old_variable_reference: str):
        # update the variables referenced in expression tree
        for idx, operand in enumerate(self.operands):
            if isinstance(operand, Mathmatic):
                operand.update_variable_scope(new_variable_reference, old_variable_reference)
            else:
                if isinstance(operand, str) and old_variable_reference in operand:
                    self.operands[idx] = operand.replace(old_variable_reference, new_variable_reference)

    def _resolve_placeholder(self, s: str, variables: dict, get_variable_value: Callable, *args, **kwargs):
        if get_variable_value is not None and isinstance(get_variable_value, Callable):
            return get_variable_value(s, variables, *args, **kwargs)
        s = s.strip()
        if s.startswith("{{") and s.endswith("}}"):
            key = s[2:-2].strip()
            try:
                return self._access_nested_value(variables, key)
            except (KeyError, TypeError, IndexError) as e:
                raise KeyError(f"Variable '{key}' not found in variables: {e}")
        if s.startswith("${") and s.endswith("}"):
            key = s[2:-1].strip()
            try:
                return self._access_nested_value(variables, key)
            except (KeyError, TypeError, IndexError) as e:
                raise KeyError(f"Variable '{key}' not found in variables: {e}")
        return s  # not a placeholder

    def _resolve_placeholder_with_variables(self, s: str, variables: dict, get_variable_value: Callable, *args, **kwargs):
        if get_variable_value is not None and isinstance(get_variable_value, Callable):
            result = get_variable_value(s, variables, *args, **kwargs)
            return result, {s: result}
        s = s.strip()
        if s.startswith("{{") and s.endswith("}}"):
            key = s[2:-2].strip()
            try:
                result = self._access_nested_value(variables, key)
                return result, {key: result}
            except (KeyError, TypeError, IndexError) as e:
                raise KeyError(f"Variable '{key}' not found in variables: {e}")
        if s.startswith("${") and s.endswith("}"):
            key = s[2:-1].strip()
            try:
                result = self._access_nested_value(variables, key)
                return result, {key: result}
            except (KeyError, TypeError, IndexError) as e:
                raise KeyError(f"Variable '{key}' not found in variables: {e}")
        return s, {}  # not a placeholder

    def _access_nested_value(self, variable_dump, name):
        """
        Access nested values in a dictionary using dot notation.
        Handles keys like 'api_variablebe40.response_body.amount'
        """
        keys = name.split('.')
        value = variable_dump

        for key in keys:
            while '[' in key and ']' in key:
                # Handle nested list indexing
                base_key, index = key.split('[', 1)
                index = int(index.split(']')[0])
                value = value[base_key] if base_key else value
                value = value[index]
                key = key[key.index(']') + 1:]  # Move to the next part of the key

            if key:  # Handle any remaining dictionary key
                value = value[key]
        return value

    def _as_number(self, value):
        # Convert value to float if possible; raise if not numeric
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Try to parse numeric string
            try:
                return float(value.strip())
            except Exception:
                raise ValueError(f"Non-numeric operand encountered: {value!r}")
        raise ValueError(f"Unsupported operand type: {type(value).__name__}")

    def evaluate(self, variables: dict, get_variable_value: Callable, *args, **kwargs)->(float, dict):
        # Resolve all operands to numbers (recursively for nested operations, and resolving placeholders)
        resolved = []
        used_variables = {}

        for operand in self.operands:
            if isinstance(operand, Mathmatic):
                result, child_variables = operand.evaluate(variables, get_variable_value, *args, **kwargs)
                resolved.append(self._as_number(result))
                used_variables.update(child_variables)
            else:
                # Resolve placeholders if it's a string
                if isinstance(operand, str):
                    operand_value, operand_variables = self._resolve_placeholder_with_variables(operand, variables, get_variable_value, *args, **kwargs)
                    used_variables.update(operand_variables)
                    resolved.append(self._as_number(operand_value))
                else:
                    resolved.append(self._as_number(operand))

        if self.operator == MathOperationOperator.ADD:
            return sum(resolved), used_variables
        elif self.operator == MathOperationOperator.SUBTRACT:
            return resolved[0] - resolved[1], used_variables
        elif self.operator == MathOperationOperator.MULTIPLY:
            return reduce(_op.mul, resolved, 1.0), used_variables
        elif self.operator == MathOperationOperator.DIVIDE:
            if resolved[1] == 0:
                raise ZeroDivisionError("Division by zero")
            return resolved[0] / resolved[1], used_variables
        elif self.operator == MathOperationOperator.MODULUS:
            if resolved[1] == 0:
                raise ZeroDivisionError("Modulo by zero")
            return resolved[0] % resolved[1], used_variables
        elif self.operator == MathOperationOperator.POWER:
            return resolved[0] ** resolved[1], used_variables
        elif self.operator == MathOperationOperator.NEGATE:
            return -resolved[0], used_variables
        elif self.operator == MathOperationOperator.ABS:
            return abs(resolved[0]), used_variables
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")


    @classmethod
    def from_json(cls, json_data):
        """
        Create a MathOperation from JSON data.
        Handles nested operations by recursively creating MathOperation objects.
        """
        operator = MathOperationOperator(json_data.get('operator', 'add'))
        operands = []

        for operand in json_data.get('operands', []):
            if isinstance(operand, dict) and 'operator' in operand:
                # This is a nested MathOperation
                operands.append(cls.from_json(operand))
            else:
                # This is a simple operand (string, number, etc.)
                operands.append(operand)

        return cls(operator=operator, operands=operands)




class AssertionCondition(enum.Enum):
    #"equals|not_equals|greater_than|less_than|greater_than_or_equal|less_than_or_equal|starts_with|ends_with|contains|length_equals|type_equals|json_key_exists|json_keys_count|json_array_length_equals|json_array_contains|json_value_equals",
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUALS = "greater_than_or_equal"
    LESS_THAN_OR_EQUALS = "less_than_or_equal"
    STARTS_WITH = "start_with"
    ENDS_WITH = "end_with"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    LENGTH_EQUALS = "length_equals"
    TYPE_EQUALS = "type_equals"
    JSON_KEY_EXISTS = "json_key_exists"
    JSON_KEYS_COUNT = "json_keys_count"
    JSON_ARRAY_LENGTH_EQUALS = "json_array_length_equals"
    JSON_ARRAY_CONTAINS = "json_array_contains"
    JSON_VALUE_EQUALS = "json_value_equals"
    IN = "in"
    NOT_IN = "not_in"
    LOWER_CASE = "lower_case"
    UPPER_CASE = "upper_case"

    @classmethod
    def _missing_(cls, value):
        # V2 ``_compare_atomic`` accepts both spellings for these operators
        # (equals/equal, not_equals/not_equal, start_with/starts_with,
        # end_with/ends_with, contains/contain); resolve them case-insensitively
        # for parity. A genuinely unknown operator returns None, which makes the
        # enum raise ValueError -- never a silent EQUALS fallback that would
        # produce a wrong verdict.
        if not isinstance(value, str):
            return None
        normalized = value.strip().lower()
        for member in cls:
            if member.value == normalized:
                return member
        aliases = {
            "equal": cls.EQUALS,
            "equals": cls.EQUALS,
            "not_equal": cls.NOT_EQUALS,
            "not_equals": cls.NOT_EQUALS,
            "start_with": cls.STARTS_WITH,
            "starts_with": cls.STARTS_WITH,
            "end_with": cls.ENDS_WITH,
            "ends_with": cls.ENDS_WITH,
            "contain": cls.CONTAINS,
            "contains": cls.CONTAINS,
        }
        return aliases.get(normalized)

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, AssertionCondition):
            return False
        return self.value == other.value

class ConcatenationOperator(enum.Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class Assertion:
    def __init__(
        self,
        assertion_operator: Union[AssertionCondition, List[AssertionCondition], ConcatenationOperator] = None,  # leaf: equals, [equals], or group: AND/OR
        assertion_operands: Optional[List[ConcatenationOperator]] = None,   # group: [AND] or [OR] (usually one)
        left_operand: Any = None,
        right_operand: Any = None,
        operands: Optional[List[Assertion]] = None,                       # children for logical groups
        operator: Union[AssertionCondition, ConcatenationOperator] = None,  # alias for assertion_operator for backward compatibility
        sub_results: list = None,
        sub_checks: list = None,
        composite_operator: str = "",
        verification: str = "",
        claim: str = "",
    ):
        # Handle backward compatibility with 'operator' parameter
        if operator is not None and assertion_operator is None:
            assertion_operator = operator

        # Handle single operator vs list of operators
        if isinstance(assertion_operator, AssertionCondition):
            self.assertion_operator = [assertion_operator]
            self.assertion_operands = assertion_operands or []
        elif isinstance(assertion_operator, ConcatenationOperator):
            self.assertion_operator = []
            self.assertion_operands = [assertion_operator]
        elif isinstance(assertion_operator, list):
            self.assertion_operator = assertion_operator
            self.assertion_operands = assertion_operands or []
        else:
            self.assertion_operator = []
            self.assertion_operands = assertion_operands or []
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operands = operands or []   # if non-empty, this node is a logical group

        # v16 sub-check fields
        self.sub_results: list = sub_results or []
        self.sub_checks: list = sub_checks or []
        self.composite_operator: str = composite_operator or ""
        self.verification: str = verification or ""
        self.claim: str = claim or ""


    def update_variable_scope(self, new_variable_reference: str, old_variable_reference: str):
        # update the variables referenced in expression tree
        if isinstance(self.left_operand, str):
            self.left_operand = self.left_operand.replace(old_variable_reference, new_variable_reference)
        if isinstance(self.right_operand, str):
            self.right_operand = self.right_operand.replace(old_variable_reference, new_variable_reference)
        for operand in self.operands:
            operand.update_variable_scope(new_variable_reference, old_variable_reference)

    # ---------- helpers ----------
    def _resolve(self, value, variables: dict, get_variable_value: Callable, *args, **kwargs):
        if isinstance(value, str):
            if isinstance(get_variable_value, Callable) and get_variable_value is not None:
                # Preserve the resolved value's type verbatim (bool/int/float/str).
                # Numeric coercion happens in the compare step, and only when the
                # OTHER operand is a real number -- V2-parity, so two numeric
                # strings ("007" vs "7") stay strings and compare unequal.
                s = get_variable_value(value, variables, *args, **kwargs)
                return s, {value: s}
            s = value.strip()
            if s.startswith("{{") and s.endswith("}}"):
                key = s[2:-2].strip()
                resolved_value = self._access_nested_value(variables, key)
                return resolved_value, {key: resolved_value}
            if s.startswith("${") and s.endswith("}"):
                key = s[2:-1].strip()
                resolved_value = self._access_nested_value(variables, key)
                return resolved_value, {key: resolved_value}
            # V2 parity: leave a bare operand as a string; the compare step
            # coerces numerically only against a real-number operand.
            return s, {}
        return value, {}

    def _access_nested_value(self, variable_dump, name):
        """
        Access nested values in a dictionary using dot notation.
        Handles keys like 'api_variablebe40.response_body.amount'
        """
        keys = name.split('.')
        value = variable_dump

        for key in keys:
            while '[' in key and ']' in key:
                # Handle nested list indexing
                base_key, index = key.split('[', 1)
                index = int(index.split(']')[0])
                value = value[base_key] if base_key else value
                value = value[index]
                key = key[key.index(']') + 1:]  # Move to the next part of the key

            if key:  # Handle any remaining dictionary key
                value = value[key]
        return value

    def _eval_leaf_condition(self, cond: AssertionCondition, left, right) -> bool:
        if cond == AssertionCondition.EQUALS:
            left_color, right_color = _normalize_color(left), _normalize_color(right)
            if left_color is not None and right_color is not None:
                return left_color == right_color
            left, right = _coerce_numeric_pair(left, right)
            l, r = _normalize_bool_str(left, right)
            return l == r
        if cond == AssertionCondition.NOT_EQUALS:
            left_color, right_color = _normalize_color(left), _normalize_color(right)
            if left_color is not None and right_color is not None:
                return left_color != right_color
            left, right = _coerce_numeric_pair(left, right)
            l, r = _normalize_bool_str(left, right)
            return l != r
        # V2 applies the bool<->str lowering for EVERY operator (it runs before
        # _compare_atomic, outside any operator branch), so ordering compares
        # the lowered strings ("true" > "0") rather than raising on bool vs str.
        if cond == AssertionCondition.GREATER_THAN:
            left, right = _coerce_numeric_pair(left, right)
            l, r = _normalize_bool_str(left, right)
            return l > r
        if cond == AssertionCondition.LESS_THAN:
            left, right = _coerce_numeric_pair(left, right)
            l, r = _normalize_bool_str(left, right)
            return l < r
        if cond == AssertionCondition.GREATER_THAN_OR_EQUALS:
            left, right = _coerce_numeric_pair(left, right)
            l, r = _normalize_bool_str(left, right)
            return l >= r
        if cond == AssertionCondition.LESS_THAN_OR_EQUALS:
            left, right = _coerce_numeric_pair(left, right)
            l, r = _normalize_bool_str(left, right)
            return l <= r
        if cond == AssertionCondition.CONTAINS:
            return _normalize_text(right, case_insensitive=True) in _normalize_text(left, case_insensitive=True)
        if cond == AssertionCondition.NOT_CONTAINS:
            return _normalize_text(right, case_insensitive=True) not in _normalize_text(left, case_insensitive=True)
        if cond == AssertionCondition.STARTS_WITH:  # note: enum value is "start_with"
            return _normalize_text(left, case_insensitive=True).startswith(_normalize_text(right, case_insensitive=True))
        if cond == AssertionCondition.ENDS_WITH:    # enum value is "end_with"
            return _normalize_text(left, case_insensitive=True).endswith(_normalize_text(right, case_insensitive=True))
        if cond == AssertionCondition.LENGTH_EQUALS:
            return _are_lengths_equal(str(left), str(right))
        if cond == AssertionCondition.TYPE_EQUALS:
            return _are_types_equal(str(left), str(right))
        if cond == AssertionCondition.LOWER_CASE:
            return _normalize_text(left) == _normalize_text(left, case_insensitive=True)
        if cond == AssertionCondition.UPPER_CASE:
            return _normalize_text(left) == _normalize_text(left, case_insensitive=True).upper()
        if cond == AssertionCondition.IN:
            if isinstance(right, (list, tuple)):
                return left in right
            return _normalize_text(left, case_insensitive=True) in _normalize_text(right, case_insensitive=True)
        if cond == AssertionCondition.NOT_IN:
            if isinstance(right, (list, tuple)):
                return left not in right
            return _normalize_text(left, case_insensitive=True) not in _normalize_text(right, case_insensitive=True)
        if cond == AssertionCondition.JSON_KEY_EXISTS:
            left = _try_parse_json(left)  # V2 parity: accept stringified dict
            return isinstance(left, dict) and str(right) in left
        if cond == AssertionCondition.JSON_KEYS_COUNT:
            left = _try_parse_json(left)  # V2 parity: accept stringified dict
            return isinstance(left, dict) and len(left.keys()) == int(right)
        if cond == AssertionCondition.JSON_ARRAY_LENGTH_EQUALS:
            left = _try_parse_json(left)  # V2 parity: accept stringified list
            return isinstance(left, list) and len(left) == int(right)
        if cond == AssertionCondition.JSON_ARRAY_CONTAINS:
            left = _try_parse_json(left)  # V2 parity: accept stringified list
            return isinstance(left, list) and right in left
        if cond == AssertionCondition.JSON_VALUE_EQUALS:
            # Expect right as [key, value]. Only the LEFT (container) operand is
            # coerced -- the pair is type-checked by the isinstance guard below,
            # never re-parsed. Parsing it too would diverge from the
            # playwright-python / java / csharp siblings, which all coerce the
            # container operand alone: a stringified '["k", "v"]' would satisfy
            # the guard here but not there, and a non-JSON right operand would
            # raise out of ast.literal_eval instead of returning False.
            left = _try_parse_json(left)  # V2 parity: accept stringified dict
            return isinstance(left, dict) and isinstance(right, (list, tuple)) and len(right) == 2 and left.get(str(right[0])) == right[1]
        raise ValueError(f"Unsupported condition: {cond}")

    # ---------- public API ----------
    def evaluate(self, variables: dict, get_variable_value: Callable, *args, **kwargs) -> (bool, dict):
        # Logical group node
        if self.operands:
            # If we have operands but no assertion_operands, check if we have a single operator
            if not self.assertion_operands:
                # Check if we have a single operator in assertion_operator (for backward compatibility)
                if len(self.assertion_operator) == 1 and isinstance(self.assertion_operator[0], ConcatenationOperator):
                    op = self.assertion_operator[0]
                else:
                    # Default to AND if no operator specified
                    op = ConcatenationOperator.AND
            else:
                # Use the first operator from assertion_operands
                op = self.assertion_operands[0]

            # NOT is unary: negate the single child (e.g. "does not contain",
            # "is not integer" arrive as NOT[<leaf>]).
            if op == ConcatenationOperator.NOT:
                if len(self.operands) != 1:
                    raise ValueError(f"NOT requires exactly one operand, got {len(self.operands)}")
                result, used_variables = self.operands[0].evaluate(variables, get_variable_value, *args, **kwargs)
                return not result, used_variables

            # fold with the operator between children
            result, used_variables = self.operands[0].evaluate(variables, get_variable_value, *args, **kwargs)
            for idx in range(1, len(self.operands)):
                val, child_variables = self.operands[idx].evaluate(variables, get_variable_value, *args, **kwargs)
                used_variables.update(child_variables)
                if op == ConcatenationOperator.AND:
                    result = result and val
                elif op == ConcatenationOperator.OR:
                    result = result or val
                else:
                    raise ValueError(f"Unsupported logical operator: {op}")
            return result, used_variables

        # Leaf comparison node: all listed conditions must hold (logical AND)
        left, left_variables = self._resolve(self.left_operand, variables, get_variable_value, *args, **kwargs)
        right, right_variables = self._resolve(self.right_operand, variables, get_variable_value, *args, **kwargs)
        # Combine all used variables
        used_variables = {}
        used_variables.update(left_variables)
        used_variables.update(right_variables)

        for cond in self.assertion_operator:
            if not self._eval_leaf_condition(cond, left, right):
                return False, used_variables
        return True, used_variables

    def to_dict(self) -> dict:
        d = {
            "operator": [op.value for op in self.assertion_operator],
            "assertion_operands": [op.value for op in self.assertion_operands],
            "left_operand": self.left_operand,
            "right_operand": self.right_operand,
            "operands": [child.to_dict() for child in self.operands] if self.operands else []
        }
        if self.sub_results:
            d["sub_results"] = self.sub_results
        if self.sub_checks:
            d["sub_checks"] = self.sub_checks
        if self.composite_operator:
            d["composite_operator"] = self.composite_operator
        if self.verification:
            d["verification"] = self.verification
        if self.claim:
            d["claim"] = self.claim
        return d


    @classmethod
    def from_json(cls, json_data: dict) -> Assertion:
        # v16 sub-check fields (common to all branches)
        v16_kwargs = dict(
            sub_results=json_data.get("sub_results", []),
            sub_checks=json_data.get("sub_checks", []),
            composite_operator=json_data.get("composite_operator", ""),
            verification=json_data.get("verification", ""),
            claim=json_data.get("claim", ""),
        )

        # Check if this is a logical group by looking at assertion_operands first (new format)
        assertion_operands = json_data.get("assertion_operands", [])
        if assertion_operands and assertion_operands[0] in ConcatenationOperator._value2member_map_:
            # This is a logical group (new format)
            concat = ConcatenationOperator(assertion_operands[0])
            children = [cls.from_json(o) for o in json_data.get("operands", [])]
            return cls(
                assertion_operator=[],
                assertion_operands=[concat],
                operands=children,
                **v16_kwargs,
            )

        # Check if this is a logical group by looking at operator field (old format)
        op_data = json_data.get("operator", [])
        if isinstance(op_data, str) and op_data in ConcatenationOperator._value2member_map_:
            # This is a logical group (old format)
            concat = ConcatenationOperator(op_data)
            children = [cls.from_json(o) for o in json_data.get("operands", [])]
            return cls(
                assertion_operator=[],
                assertion_operands=[concat],
                operands=children,
                **v16_kwargs,
            )

        # Handle leaf nodes - both single operator string and list of operators
        if isinstance(op_data, list):
            conditions = [AssertionCondition(op) for op in op_data] if op_data else [AssertionCondition.EQUALS]
        else:
            conditions = [AssertionCondition(op_data)] if op_data else [AssertionCondition.EQUALS]

        return cls(
            assertion_operator=conditions,
            left_operand=json_data.get("left_operand"),
            right_operand=json_data.get("right_operand"),
            **v16_kwargs,
        )
