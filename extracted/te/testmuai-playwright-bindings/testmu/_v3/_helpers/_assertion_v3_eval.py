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
import operator as _op
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


def _numeric_list_contains(left, right) -> "bool | None":
    """Element-wise numeric membership for ``list CONTAINS number``.

    Returns ``None`` when this path does not apply, so the caller falls through
    to the existing substring semantics.

    Without it both operands are stringified and the test becomes a SUBSTRING
    match on the list's repr — ``[12, 3]`` "contains" ``2`` and ``[10, 20]``
    "contains" ``0``, both false positives that make a failing assertion pass
    silently (the Pepsico sub-division report).

    Integer-shaped values are compared as ints rather than floats so adjacent
    integers above 2**53 don't collapse onto the same float. String items are
    coerced, so a JSON payload whose numbers arrived as strings still matches.
    ``bool`` is excluded on both sides: ``True == 1`` is a Python accident, not
    an assertion the user meant.
    """
    if not isinstance(left, list):
        return None
    # A quoted number ("1") is the shape authoring emits, and V3 keeps operand
    # types verbatim, so without this the element-wise path below never fires
    # and CONTAINS falls back to a substring test on the list's repr. V2 got
    # here by coercing every operand in _resolve; that is too broad for V3
    # (scalar "007" must stay unequal to "7"), so coerce only opposite a list.
    if isinstance(right, str):
        text = right.strip()
        try:
            right = int(text)
        except ValueError:
            try:
                right = float(text)
            except ValueError:
                return None
    if isinstance(right, bool) or not isinstance(right, (int, float)):
        return None

    r_int = right if isinstance(right, int) else (
        int(right) if isinstance(right, float) and right.is_integer() else None
    )
    r_float = None if r_int is not None else float(right)

    def _item_matches(item) -> bool:
        if isinstance(item, bool):
            return False
        i_int = i_float = None
        if isinstance(item, int):
            i_int = item
        elif isinstance(item, float):
            if item.is_integer():
                i_int = int(item)
            else:
                i_float = item
        elif isinstance(item, str):
            text = item.strip()
            try:
                i_int = int(text)
            except ValueError:
                try:
                    parsed = float(text)
                except ValueError:
                    return False
                if parsed.is_integer():
                    i_int = int(parsed)
                else:
                    i_float = parsed
        else:
            return False

        if i_int is not None and r_int is not None:
            return i_int == r_int
        left_value = float(i_int) if i_int is not None else i_float
        right_value = float(r_int) if r_int is not None else r_float
        return left_value == right_value

    return any(_item_matches(item) for item in left)

class NonNumericOperandError(ValueError):
    """V2 parity (auteur-utils #956). Auteur classifies data-vs-system errors
    by the message prefix — keep it stable."""

    def __init__(self, value):
        self.value = value
        super().__init__(f"Non-numeric operand encountered: {value!r}")


class TypeMismatchError(ValueError):
    """V2 parity (auteur-utils #956). Auteur matches the message prefix — keep
    it stable."""

    def __init__(self, name, actual, expected):
        self.name, self.actual, self.expected = str(name), str(actual), str(expected)
        super().__init__(f"Type mismatch: {self.name!r} holds {self.actual}, needs {self.expected}")


def _safe_float(value: str) -> float:
    """V2 CommonParser.safe_float: tolerate thousands-separator commas
    ("3,000" -> 3000.0); raise (like ``float()``) on non-numeric input."""
    return float(value.strip().replace(",", ""))


def _ordered_compare(py_op, left, right):
    """V2 _ordered_compare: plain-Python semantics — whatever Python can
    compare natively, we compare; only its TypeErrors error out. Mixed
    str/number coerces the string STRICTLY; a non-numeric string raises the
    typed error instead of silently becoming 0."""
    try:
        return py_op(left, right)
    except TypeError:
        pass
    for operand in (left, right):
        if isinstance(operand, (list, tuple, set, dict)):
            raise TypeMismatchError(str(operand)[:60], type(operand).__name__, "a number")
    _l, _r = left, right
    try:
        if isinstance(_l, str):
            _l = _safe_float(_l)
        if isinstance(_r, str):
            _r = _safe_float(_r)
        return py_op(_l, _r)
    except (TypeError, ValueError):
        bad = left if not isinstance(left, (int, float)) else right
        raise NonNumericOperandError(bad)


def _as_int_operand(value):
    """V2 _as_int_operand: int coercion whose failure is the typed error."""
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            raise NonNumericOperandError(value)


def _step_into(value, key, path, expected):
    try:
        return value[key]
    except TypeError:
        raise TypeMismatchError(path, type(value).__name__, expected)


def _walk_path(variable_dump, name):
    """V2 _walk_path: dotted/indexed access whose failures are typed errors."""
    value = variable_dump
    for key in name.split('.'):
        while '[' in key and ']' in key:
            base_key, index = key.split('[', 1)
            index = int(index.split(']')[0])
            value = _step_into(value, base_key, name, "an object") if base_key else value
            value = _step_into(value, index, name, "a list")
            key = key[key.index(']') + 1:]
        if key:
            value = _step_into(value, key, name, "an object")
    return value


# -- Null-operand policy (TE-24465 / TE-25086, auteur-utils #927 + #944) ----
_NULL_SATISFIES_OPS = {"not_contain", "not_contains", "not_in"}
_MEMBERSHIP_IN_OPS = {"in", "not_in"}
_MEMBERSHIP_CONTAINS_OPS = {"contain", "contains", "not_contain", "not_contains",
                            "json_array_contains"}
# A typed null operand arrives as text, so it must match a resolved real None.
_NULL_LITERALS = {"null", "none"}


def _is_null_operand(value) -> bool:
    """A real None, or one of the literal tokens in any case.
    isinstance is load-bearing — list and numeric operands reach here too."""
    if value is None:
        return True
    return isinstance(value, str) and value.strip().lower() in _NULL_LITERALS


def null_operand_verdict(op_value: str, left, right, parse_array=None, type_equals=None) -> bool:
    """Null equals only null; other positive operators are False, negated ones True.
    Membership is the exception — defer to the collection when there really is one.

    Verbatim V2 policy (auteur-utils #927/#944), identical to the
    selenium-python port so both bindings agree."""
    if op_value in _MEMBERSHIP_IN_OPS and isinstance(right, (list, tuple)):
        return (left in right) if op_value == "in" else (left not in right)
    if op_value in _MEMBERSHIP_CONTAINS_OPS:
        seq = left
        if parse_array is not None and op_value == "json_array_contains":
            seq = parse_array(left)
        if isinstance(seq, (list, tuple)):
            present = right in seq
            return not present if op_value in {"not_contain", "not_contains"} else present

    both_null = _is_null_operand(left) and _is_null_operand(right)
    if op_value in {"==", "equals", "equal"}:
        return both_null
    if op_value in {"!=", "not_equals", "not_equal"}:
        return not both_null
    if op_value == "type_equals":
        return type_equals(left, right) if type_equals else type(left).__name__ == str(right)
    return op_value in _NULL_SATISFIES_OPS


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
        json_path: str = "",
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
        self.json_path: str = json_path or ""

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
        return _walk_path(variable_dump, name)

    def _eval_leaf_condition(self, cond: AssertionCondition, left, right) -> bool:
        # TE-24465 (auteur-utils #927): settle null before _normalize_text
        # (which str()s it to "None") or any coercion ever sees it.
        if left is None or right is None:
            return null_operand_verdict(
                cond.value, left, right,
                parse_array=_json_coerce,
                type_equals=lambda x, y: _are_types_equal(str(x), str(y)),
            )
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
        # TE-22956 (auteur-utils #956): ordering skips the lenient mixed
        # coercion ("sam" -> 0 made 5 > "sam" PASS); _ordered_compare coerces
        # strictly and raises the typed error on a non-numeric operand.
        if cond == AssertionCondition.GREATER_THAN:
            l, r = _normalize_bool_str(left, right)
            return _ordered_compare(_op.gt, l, r)
        if cond == AssertionCondition.LESS_THAN:
            l, r = _normalize_bool_str(left, right)
            return _ordered_compare(_op.lt, l, r)
        if cond == AssertionCondition.GREATER_THAN_OR_EQUALS:
            l, r = _normalize_bool_str(left, right)
            return _ordered_compare(_op.ge, l, r)
        if cond == AssertionCondition.LESS_THAN_OR_EQUALS:
            l, r = _normalize_bool_str(left, right)
            return _ordered_compare(_op.le, l, r)
        if cond in (AssertionCondition.CONTAINS, AssertionCondition.NOT_CONTAINS):
            # A list of numbers compared against a number is membership,
            # not a substring test on the list's repr.
            numeric_hit = _numeric_list_contains(left, right)
            if numeric_hit is not None:
                return numeric_hit if cond == AssertionCondition.CONTAINS else not numeric_hit
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
            return isinstance(coerced, dict) and len(coerced.keys()) == _as_int_operand(right)
        if cond == AssertionCondition.JSON_ARRAY_LENGTH_EQUALS:
            coerced = _json_coerce(left)  # V2 parity: accept stringified list
            return isinstance(coerced, list) and len(coerced) == _as_int_operand(right)
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
        # Materialized-condition contract (auteur #6461/#6161): an analyzer-
        # backed ASSERTION carries its replay contract as a sub_check LIST;
        # the legacy leaf beneath it is hollow. When sub_checks are present
        # they ARE the verdict — identical to the selenium-python port.
        if self.sub_checks:
            return self._evaluate_sub_checks(variables, get_variable_value, *args, **kwargs)
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

        if self.json_path:
            from testmu_helper.evaluation._evaluate import _apply_rfc_json_path
            matches = _apply_rfc_json_path(left, self.json_path)
            if not matches:
                return False, used_variables
            for cond in self.assertion_operator:
                for match_value in matches:
                    if not self._eval_leaf_condition(cond, match_value, right):
                        return False, used_variables
            return True, used_variables

        for cond in self.assertion_operator:
            if not self._eval_leaf_condition(cond, left, right):
                return False, used_variables
        return True, used_variables

    def _evaluate_sub_checks(self, variables, get_variable_value, *args, **kwargs):
        from testmu_helper.evaluation import evaluate_sub_checks

        used_variables = {}
        resolved = []
        for sc in self.sub_checks:
            raw_expected = sc.get("expected_value") or sc.get("expected") or ""
            raw_extracted = sc.get("extracted_value") or ""
            expected, used_r = self._resolve(raw_expected, variables, get_variable_value, *args, **kwargs)
            extracted, used_l = self._resolve(raw_extracted, variables, get_variable_value, *args, **kwargs)
            used_variables.update(used_l)
            used_variables.update(used_r)
            resolved.append({
                "description": sc.get("description") or "",
                "expected_value": expected,
                "extracted_value": extracted,
                "operator": sc.get("operator") or "equals",
                "transforms": sc.get("transforms") or [],
                # json_path must be carried — the transform is a no-op without
                # its path argument (auteur #6161).
                "json_path": sc.get("json_path"),
            })
        outcome = evaluate_sub_checks(self.claim, self.composite_operator or "and", resolved)
        self.sub_results = outcome["sub_results"]
        return outcome["status"] == "passed", used_variables

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
            json_path=json_data.get("json_path", ""),
            **v16_kwargs,
        )
