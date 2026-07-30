"""Code-side assertion evaluator.

This module contains the Assertion class (and its supporting enums/helpers)
that evaluates an assertion tree in pure Python, without any microservice call.

Ported from the Selenium condition evaluator implementation.

Selenium-driver references have been stripped — the evaluator operates only on
the assertion tree dict and the variable store, making it safe for both Playwright
and Selenium paths.
"""
from __future__ import annotations

import ast
import enum
import json
import re
import unicodedata
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
    colour, so ``equals`` must compare by colour value, not raw string.
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
    """Normalize a bool-vs-string equality pair, mirroring the Selenium runtime.

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


def _string_to_float(value: Any):
    """Currency-tolerant numeric parse, reproduced from V2 UIActions.string_to_float.

    An already-numeric value passes through. A plain ``float()`` handles
    scientific notation. On ``ValueError`` keep only digits and dots
    (so ``"$7"`` -> ``"7"``, ``"7a"`` -> ``"7"``, ``"abc"`` -> ``""`` -> ``0``)
    and negate if a ``'-'`` appears anywhere. A multi-dot residue like
    ``"v1.2.3"`` -> ``"1.2.3"`` re-raises ``ValueError`` uncaught -- V2 crashed
    here and the loud failure is the faithful behavior.
    """
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except ValueError:
        is_negative = "-" in value
        a = "".join(c for c in value if c.isdigit() or c == ".")
        if a == "":
            return 0
        result = float(a)
        return -result if is_negative else result


def _coerce_numeric_mixed(left: Any, right: Any):
    """V2 evaluate_assertion parity: coerce ONLY on mixed exact type.

    When exactly one operand is a real ``int``/``float`` and the other a ``str``,
    ``string_to_float`` BOTH so a numeric variable compares numerically to an
    authored numeric string. The check is an EXACT ``type`` test (bool is a
    subclass of int but ``type(True) is bool``, so bool is excluded). Two strings
    are left untouched, so ``"007" == "7"`` stays raw and case-sensitive.
    """
    lt, rt = type(left), type(right)
    if (lt in (int, float) and rt is str) or (lt is str and rt in (int, float)):
        return _string_to_float(left), _string_to_float(right)
    return left, right


_SMART_PUNCT_MAP = str.maketrans({
    "‘": "'", "’": "'",   # curly single quotes
    "“": '"', "”": '"',   # curly double quotes
    " ": " ",                  # non-breaking space
    "​": "", "‌": "", "‍": "", "﻿": "",  # zero-width / BOM
})


def _normalize_text(s: Any, case_insensitive: bool = False, ascii_fold: bool = True) -> str:
    """Canonicalize text for substring/prefix/suffix matching, matching the Selenium runtime.

    Folds accents/ligatures (NFKD + drop combining marks), maps smart
    punctuation and invisible characters, collapses whitespace, and optionally
    case-folds. So `contains`/`start_with`/`end_with` match the way the
    Selenium runtime evaluated them — e.g. "Café Menu" contains "cafe".
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
    """The length_equals assertion: a numeric operand is the number itself, else its len().

    The implementation checks ``str.isdigit()``; a numeric operand may arrive as a
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
    """The type_equals assertion: map type-name strings (incl. 'boolean'->bool) to types.

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


def _json_coerce(value: Any) -> Any:
    """Parse a stringified JSON operand, reproduced from V2 UIActions._json_obj/_json_arr.

    A real dict/list passes through untouched. A string is parsed with
    ``json.loads``; on ``json.JSONDecodeError`` it falls back to
    ``ast.literal_eval`` (so a Python-repr'd container like ``"{'a': 1}"`` is
    accepted too). Parse failures are deliberately NOT swallowed — they raise,
    matching V2, so a malformed operand fails loudly rather than silently.
    """
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return ast.literal_eval(value)
    return value


class AssertionCondition(enum.Enum):
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
    """Code-side assertion evaluator, ported from the Selenium condition implementation.

    Evaluates an operator/operand tree (produced by the code generator) in pure Python.
    No Selenium driver dependency — operates only on dict values and the variable
    store.
    """

    def __init__(
        self,
        assertion_operator: Union[AssertionCondition, List[AssertionCondition], ConcatenationOperator] = None,
        assertion_operands: Optional[List[ConcatenationOperator]] = None,
        left_operand: Any = None,
        right_operand: Any = None,
        operands: Optional[List["Assertion"]] = None,
        operator: Union[AssertionCondition, ConcatenationOperator] = None,
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
        self.operands = operands or []

        # v16 sub-check fields
        self.sub_results: list = sub_results or []
        self.sub_checks: list = sub_checks or []
        self.composite_operator: str = composite_operator or ""
        self.verification: str = verification or ""
        self.claim: str = claim or ""

    # ---------- helpers ----------

    def _resolve(self, value, variables: dict, get_variable_value: Callable, *args, **kwargs):
        if isinstance(value, str):
            if isinstance(get_variable_value, Callable) and get_variable_value is not None:
                # Return the resolved value with its native type intact. No
                # float coercion here: coercion is applied later in the compare
                # step, operator- and type-aware, so two strings like "007" and
                # "7" stay strings and compare raw (V2 parity).
                resolved = get_variable_value(value, variables, *args, **kwargs)
                return resolved, {value: resolved}
            s = value.strip()
            if s.startswith("{{") and s.endswith("}}"):
                key = s[2:-2].strip()
                resolved_value = self._access_nested_value(variables, key)
                return resolved_value, {key: resolved_value}
            if s.startswith("${") and s.endswith("}"):
                key = s[2:-1].strip()
                resolved_value = self._access_nested_value(variables, key)
                return resolved_value, {key: resolved_value}
            # Plain literal: keep as-is (no numeric coercion; see compare step).
            return value, {}
        return value, {}

    def _access_nested_value(self, variable_dump, name):
        """Access nested values in a dictionary using dot notation."""
        keys = name.split('.')
        value = variable_dump

        for key in keys:
            while '[' in key and ']' in key:
                base_key, index = key.split('[', 1)
                index = int(index.split(']')[0])
                value = value[base_key] if base_key else value
                value = value[index]
                key = key[key.index(']') + 1:]

            if key:
                value = value[key]
        return value

    def _eval_leaf_condition(self, cond: AssertionCondition, left, right) -> bool:
        if cond == AssertionCondition.EQUALS:
            left_color, right_color = _normalize_color(left), _normalize_color(right)
            if left_color is not None and right_color is not None:
                return left_color == right_color
            left, right = _coerce_numeric_mixed(left, right)
            l, r = _normalize_bool_str(left, right)
            return l == r
        if cond == AssertionCondition.NOT_EQUALS:
            left_color, right_color = _normalize_color(left), _normalize_color(right)
            if left_color is not None and right_color is not None:
                return left_color != right_color
            left, right = _coerce_numeric_mixed(left, right)
            l, r = _normalize_bool_str(left, right)
            return l != r
        # V2 applies the bool<->str lowering for EVERY operator (it runs before
        # _compare_atomic, outside any operator branch), so ordering compares
        # the lowered strings ("true" > "0") rather than raising on bool vs str.
        if cond == AssertionCondition.GREATER_THAN:
            left, right = _coerce_numeric_mixed(left, right)
            l, r = _normalize_bool_str(left, right)
            return l > r
        if cond == AssertionCondition.LESS_THAN:
            left, right = _coerce_numeric_mixed(left, right)
            l, r = _normalize_bool_str(left, right)
            return l < r
        if cond == AssertionCondition.GREATER_THAN_OR_EQUALS:
            left, right = _coerce_numeric_mixed(left, right)
            l, r = _normalize_bool_str(left, right)
            return l >= r
        if cond == AssertionCondition.LESS_THAN_OR_EQUALS:
            left, right = _coerce_numeric_mixed(left, right)
            l, r = _normalize_bool_str(left, right)
            return l <= r
        if cond == AssertionCondition.CONTAINS:
            return _normalize_text(right, case_insensitive=True) in _normalize_text(left, case_insensitive=True)
        if cond == AssertionCondition.NOT_CONTAINS:
            return _normalize_text(right, case_insensitive=True) not in _normalize_text(left, case_insensitive=True)
        if cond == AssertionCondition.STARTS_WITH:
            return _normalize_text(left, case_insensitive=True).startswith(_normalize_text(right, case_insensitive=True))
        if cond == AssertionCondition.ENDS_WITH:
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
            coerced = _json_coerce(left)  # V2 parity: accept stringified dict
            return isinstance(coerced, dict) and str(right) in coerced
        if cond == AssertionCondition.JSON_KEYS_COUNT:
            coerced = _json_coerce(left)  # V2 parity: accept stringified dict
            return isinstance(coerced, dict) and len(coerced.keys()) == int(right)
        if cond == AssertionCondition.JSON_ARRAY_LENGTH_EQUALS:
            coerced = _json_coerce(left)  # V2 parity: accept stringified list
            return isinstance(coerced, list) and len(coerced) == int(right)
        if cond == AssertionCondition.JSON_ARRAY_CONTAINS:
            coerced = _json_coerce(left)  # V2 parity: accept stringified list
            return isinstance(coerced, list) and right in coerced
        if cond == AssertionCondition.JSON_VALUE_EQUALS:
            coerced = _json_coerce(left)  # V2 parity: accept stringified dict
            return (
                isinstance(coerced, dict)
                and isinstance(right, (list, tuple))
                and len(right) == 2
                and coerced.get(str(right[0])) == right[1]
            )
        raise ValueError(f"Unsupported condition: {cond}")

    # ---------- public API ----------

    def evaluate(self, variables: dict, get_variable_value: Callable, *args, **kwargs) -> tuple:
        """Evaluate this node.

        Returns:
            (bool, dict) — (passed, used_variables)
        """
        # Logical group node
        if self.operands:
            if not self.assertion_operands:
                if len(self.assertion_operator) == 1 and isinstance(self.assertion_operator[0], ConcatenationOperator):
                    op = self.assertion_operator[0]
                else:
                    op = ConcatenationOperator.AND
            else:
                op = self.assertion_operands[0]

            # NOT is unary: negate the single child (e.g. "does not contain",
            # "is not integer" arrive as NOT[<leaf>]).
            if op == ConcatenationOperator.NOT:
                if len(self.operands) != 1:
                    raise ValueError(f"NOT requires exactly one operand, got {len(self.operands)}")
                result, used_variables = self.operands[0].evaluate(variables, get_variable_value, *args, **kwargs)
                return not result, used_variables

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
        used_variables = {}
        used_variables.update(left_variables)
        used_variables.update(right_variables)

        for cond in self.assertion_operator:
            if not self._eval_leaf_condition(cond, left, right):
                return False, used_variables
        return True, used_variables

    @classmethod
    def from_json(cls, json_data: dict) -> "Assertion":
        """Deserialize an assertion tree dict into an Assertion node."""
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
            concat = ConcatenationOperator(op_data)
            children = [cls.from_json(o) for o in json_data.get("operands", [])]
            return cls(
                assertion_operator=[],
                assertion_operands=[concat],
                operands=children,
                **v16_kwargs,
            )

        # Handle leaf nodes — both single operator string and list of operators
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
