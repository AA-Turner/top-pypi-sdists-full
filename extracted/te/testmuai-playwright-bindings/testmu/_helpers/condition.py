"""Condition classes for test evaluation.

Ported from the Selenium binding condition module. The public API is consumed by
exported Playwright test code via ``testmu.Condition``, etc.

Usage in emitted test.py:
    from testmu import Condition, ResolvedCondition, PossibleCondition, get_variable_value

    result = Condition(
        conditions=[ResolvedCondition(
            left_operand='{{x}}',
            operator=PossibleCondition('=='),
            right_operand='5',
        )],
        connectors=[],
    ).evaluate({}, get_variable_value)[0]
"""
from __future__ import annotations

import enum
from typing import Any, Callable

from testmu._helpers._assertion_v3_eval import _normalize_text


class ResolvedCondition:
    """A single comparison triple: left_operand op right_operand."""

    def __init__(self, left_operand: str, operator: PossibleCondition, right_operand: str):
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand

    def to_dict(self):
        """Serialize to a JSON-compatible dict."""
        return {
            "left_operand": self.left_operand,
            "operator": self.operator.value,
            "right_operand": self.right_operand,
        }

    @classmethod
    def from_string(cls, condition: str) -> ResolvedCondition:
        """Parse 'left op right' whitespace-delimited string."""
        left_operand, _operator, right_operand = condition.split()
        operator = PossibleCondition(_operator.strip())
        return cls(left_operand.strip(), operator, right_operand.strip())

    @classmethod
    def from_json(cls, json_data: dict) -> ResolvedCondition:
        """Deserialize from a dict (e.g. parsed from JSON blob)."""
        return cls(
            left_operand=json_data.get("left_operand", ""),
            operator=PossibleCondition(json_data.get("operator", "")),
            right_operand=json_data.get("right_operand", ""),
        )

    @classmethod
    def create_string_from_condition(
        cls,
        conditions: list[ResolvedCondition],
        connectors: list[ConcatenationOperator],
    ) -> str:
        """Render a list of conditions + connectors into a human-readable string."""
        condition_string = ""
        for idx, condition in enumerate(conditions):
            condition_string += str(condition)
            if idx < len(connectors):
                condition_string += connectors[idx].value
        return condition_string

    def __str__(self) -> str:
        return f"{self.left_operand} {self.operator.value} {self.right_operand}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResolvedCondition):
            return False
        return (
            self.left_operand == other.left_operand
            and self.operator == other.operator
            and self.right_operand == other.right_operand
        )


class Condition:
    """Composite condition: a list of ResolvedConditions joined by ConcatenationOperators.

    Evaluate with ``.evaluate(variables_dict, get_variable_value_fn)`` — returns
    ``(bool, used_variables_dict)``.
    """

    def __init__(
        self,
        conditions: list[ResolvedCondition],
        connectors: list[ConcatenationOperator],
        is_v3: bool | None = None,
    ):
        self.connectors = connectors
        self.conditions = conditions
        # V3 mode: text ops are case-insensitive + unicode-folded; AND binds
        # tighter than OR (A OR B AND C == A OR (B AND C)).
        # When is_v3 is not passed explicitly, resolve it from the runtime config
        # (kane_version == "v3"). Codegen emits inline conditionals as bare
        # Condition(...) with no is_v3 arg, so this is what makes those pick up V3
        # semantics. Lazy import avoids a circular import at module load (mirrors
        # wait.py). Default config is "v4", so non-V3 runs stay byte-identical.
        if is_v3 is None:
            from testmu import _configure
            is_v3 = _configure.get("kane_version", "v4") == "v3"
        self.is_v3 = is_v3

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_placeholder(
        self,
        s: str,
        variables: dict,
        get_variable_value: Callable,
        *args: Any,
        **kwargs: Any,
    ):
        if get_variable_value is not None and callable(get_variable_value):
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

    def _access_nested_value(self, variable_dump: Any, name: str) -> Any:
        """Access nested values using dot notation and bracket indexing.

        Handles keys like 'api_variablebe40.response_body.amount'.
        """
        keys = name.split(".")
        value = variable_dump

        for key in keys:
            while "[" in key and "]" in key:
                base_key, index = key.split("[", 1)
                index = int(index.split("]")[0])
                value = value[base_key] if base_key else value
                value = value[index]
                key = key[key.index("]") + 1:]

            if key:
                value = value[key]
        return value

    def _is_numeric(self, val: Any) -> bool:
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

    def _to_numeric(self, val: Any) -> Any:
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            val = val.strip()
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
        if (s.startswith('"') and s.endswith('"')) or (
            s.startswith("'") and s.endswith("'")
        ):
            return s[1:-1]
        return s

    def _is_typecast_required(
        self, left_operand: Any, right_operand: Any
    ) -> tuple[Any, Any]:
        """Coerce mixed string/number operands before comparing.

        Ported from the Selenium condition parser for parity. A genuinely
        non-numeric operand is left unchanged so an invalid ordering comparison
        still raises TypeError.
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

    def _eval_condition(
        self,
        operator: PossibleCondition,
        left_operand: Any,
        right_operand: Any,
    ) -> bool:
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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate(
        self,
        variables: dict,
        get_variable_value: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[bool, dict]:
        """Evaluate all conditions using variable resolution via get_variable_value.

        Args:
            variables:          A dict of already-resolved variables (may be empty).
            get_variable_value: Callable(template, variables, *args) -> resolved value.

        Returns:
            A ``(result_bool, used_variables_dict)`` tuple. Index [0] is the
            overall boolean result after applying connectors.
        """
        used_variables: dict = {}
        results: list[bool] = []
        for condition in self.conditions:
            _left_operand, left_operand_variables = self._resolve_placeholder(
                condition.left_operand, variables, get_variable_value, *args, **kwargs
            )
            _right_operand, right_operand_variables = self._resolve_placeholder(
                condition.right_operand, variables, get_variable_value, *args, **kwargs
            )
            result = self._eval_condition(condition.operator, _left_operand, _right_operand)
            used_variables.update(left_operand_variables)
            used_variables.update(right_operand_variables)
            results.append(result)

        # V3 precedence fold: AND binds tighter than OR so
        # A OR B AND C == A OR (B AND C).  Accumulate AND-groups left-to-right;
        # each OR flushes the running group into or_groups and starts a new one.
        # any(or_groups) short-circuits like Python's built-in `or`.
        if self.is_v3:
            if not results:
                return True, used_variables
            current = results[0]
            or_groups: list[bool] = []
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
        for idx, connector in enumerate(self.connectors):
            if connector == ConcatenationOperator.AND:
                final_result = final_result and results[idx + 1]
            elif connector == ConcatenationOperator.OR:
                final_result = final_result or results[idx + 1]
            else:
                raise ValueError(f"Unsupported connector: {connector}")
        return final_result, used_variables

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dict."""
        return {
            "connectors": [connector.value for connector in self.connectors],
            "conditions": [condition.to_dict() for condition in self.conditions],
        }


class PossibleCondition(enum.Enum):
    """Comparison operators supported in conditions."""

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

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PossibleCondition):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class ConcatenationOperator(enum.Enum):
    """Logical connectors between conditions."""

    AND = "AND"
    OR = "OR"
