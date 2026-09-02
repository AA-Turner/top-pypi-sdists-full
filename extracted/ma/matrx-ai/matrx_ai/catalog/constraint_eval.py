"""Python port of the frontend model-constraint evaluator (matrx-frontend features/agents/.../validation/constraints.ts) — the TS evaluator is the spec; semantics mirror JS strict equality, Array.includes, and relational ToNumber coercion exactly."""

from __future__ import annotations

import json
import math
from typing import Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

ValidationSeverity = Literal["error", "warning", "info"]

ValidationCategory = Literal[
    "unrecognized_key",
    "invalid_value",
    "range_violation",
    "cross_field",
    "type_mismatch",
    "deprecated_key",
    "missing_required",
    "schema",
    "unsupported_by_model",
]

ConditionOp = Literal[
    "eq", "neq", "gt", "gte", "lt", "lte", "in", "not_in", "exists", "not_exists"
]

UnconditionalRule = Literal["required", "fixed", "min", "max", "one_of", "forbidden"]


class _Undefined:
    _instance: "_Undefined | None" = None

    def __new__(cls) -> "_Undefined":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "undefined"

    def __bool__(self) -> bool:
        return False


UNDEFINED: _Undefined = _Undefined()


class FieldCondition(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    field: str
    op: ConditionOp
    value: Any = UNDEFINED


class UnconditionalConstraint(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    id: str
    rule: UnconditionalRule
    field: str
    value: Any = UNDEFINED
    severity: ValidationSeverity
    message: str


class ConditionalConstraint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    when: FieldCondition
    require: FieldCondition
    severity: ValidationSeverity
    message: str


ModelConstraint = Union[UnconditionalConstraint, ConditionalConstraint]


class ValidationIssue(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, arbitrary_types_allowed=True)

    rule_id: str = Field(alias="ruleId")
    key: str
    severity: ValidationSeverity
    category: ValidationCategory
    message: str
    value: Any = UNDEFINED
    suggestion: str | None = None


def parse_constraint(raw: dict[str, Any]) -> ModelConstraint:
    if "when" in raw and "require" in raw:
        return ConditionalConstraint.model_validate(raw)
    return UnconditionalConstraint.model_validate(raw)


def _get(settings: dict[str, Any], field: str) -> Any:
    return settings.get(field, UNDEFINED)


def _is_js_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _js_to_number(v: Any) -> float:
    if v is UNDEFINED:
        return math.nan
    if v is None:
        return 0.0
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if _is_js_number(v):
        return float(v)
    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return 0.0
        try:
            return float(s)
        except ValueError:
            return math.nan
    return math.nan


def _js_strict_eq(a: Any, b: Any) -> bool:
    if a is UNDEFINED or b is UNDEFINED:
        return a is b
    if a is None or b is None:
        return a is b
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if _is_js_number(a) and _is_js_number(b):
        return float(a) == float(b)
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    return a is b


def _js_includes(arr: list[Any], needle: Any) -> bool:
    return any(_js_strict_eq(item, needle) for item in arr)


def _js_stringify(v: Any) -> str:
    if v is UNDEFINED:
        return "undefined"
    if _is_js_number(v) and isinstance(v, float) and v.is_integer():
        return str(int(v))
    return json.dumps(v, separators=(",", ":"))


def _js_join(arr: list[Any]) -> str:
    parts: list[str] = []
    for item in arr:
        if item is None or item is UNDEFINED:
            parts.append("")
        elif isinstance(item, bool):
            parts.append("true" if item else "false")
        elif _is_js_number(item) and isinstance(item, float) and item.is_integer():
            parts.append(str(int(item)))
        else:
            parts.append(str(item))
    return ", ".join(parts)


def evaluate_condition(cond: FieldCondition, settings: dict[str, Any]) -> bool:
    actual = _get(settings, cond.field)

    if cond.op == "eq":
        return _js_strict_eq(actual, cond.value)
    if cond.op == "neq":
        return not _js_strict_eq(actual, cond.value)
    if cond.op in ("gt", "gte", "lt", "lte"):
        if not _is_js_number(actual):
            return False
        rhs = _js_to_number(cond.value)
        if math.isnan(rhs):
            return False
        lhs = float(actual)
        if cond.op == "gt":
            return lhs > rhs
        if cond.op == "gte":
            return lhs >= rhs
        if cond.op == "lt":
            return lhs < rhs
        return lhs <= rhs
    if cond.op == "in":
        return isinstance(cond.value, list) and _js_includes(cond.value, actual)
    if cond.op == "not_in":
        return isinstance(cond.value, list) and not _js_includes(cond.value, actual)
    if cond.op == "exists":
        return actual is not UNDEFINED and actual is not None
    if cond.op == "not_exists":
        return actual is UNDEFINED or actual is None
    return False


def evaluate_unconditional(
    constraint: UnconditionalConstraint, settings: dict[str, Any]
) -> ValidationIssue | None:
    field = constraint.field
    value = constraint.value
    actual = _get(settings, field)

    def issue(category: ValidationCategory, suggestion: str) -> ValidationIssue:
        return ValidationIssue(
            rule_id="model-constraints",
            key=field,
            severity=constraint.severity,
            category=category,
            message=constraint.message,
            value=actual,
            suggestion=suggestion,
        )

    if constraint.rule == "required":
        if actual is UNDEFINED or actual is None:
            return issue("missing_required", f'Provide a value for "{field}"')
        return None

    if constraint.rule == "fixed":
        if actual is UNDEFINED or actual is None:
            return issue("invalid_value", f'Set "{field}" to {_js_stringify(value)}')
        if not _js_strict_eq(actual, value):
            return issue("invalid_value", f'Set "{field}" to {_js_stringify(value)}')
        return None

    if constraint.rule == "min":
        if actual is UNDEFINED or actual is None:
            return None
        if not _is_js_number(actual) or not _is_js_number(value):
            return None
        if float(actual) < float(value):
            return issue("range_violation", f'Set "{field}" to at least {_js_stringify(value)}')
        return None

    if constraint.rule == "max":
        if actual is UNDEFINED or actual is None:
            return None
        if not _is_js_number(actual) or not _is_js_number(value):
            return None
        if float(actual) > float(value):
            return issue("range_violation", f'Set "{field}" to at most {_js_stringify(value)}')
        return None

    if constraint.rule == "one_of":
        if actual is UNDEFINED or actual is None:
            return None
        if not isinstance(value, list):
            return None
        if not _js_includes(value, actual):
            return issue("invalid_value", f'Set "{field}" to one of: {_js_join(value)}')
        return None

    if constraint.rule == "forbidden":
        if actual is not UNDEFINED and actual is not None:
            return issue("invalid_value", f'Remove "{field}"')
        return None

    return None


def evaluate_conditional(
    constraint: ConditionalConstraint, settings: dict[str, Any]
) -> ValidationIssue | None:
    if not evaluate_condition(constraint.when, settings):
        return None
    if evaluate_condition(constraint.require, settings):
        return None

    return ValidationIssue(
        rule_id="model-constraints",
        key=constraint.require.field,
        severity=constraint.severity,
        category="cross_field",
        message=constraint.message,
        value=_get(settings, constraint.require.field),
        suggestion=(
            f"When {constraint.when.field} {constraint.when.op} "
            f"{_js_stringify(constraint.when.value)}, set {constraint.require.field} "
            f"to satisfy: {constraint.require.op} {_js_stringify(constraint.require.value)}"
        ),
    )


def evaluate_constraint(
    constraint: ModelConstraint, settings: dict[str, Any]
) -> ValidationIssue | None:
    if isinstance(constraint, ConditionalConstraint):
        return evaluate_conditional(constraint, settings)
    return evaluate_unconditional(constraint, settings)


def evaluate_all_constraints(
    constraints: list[ModelConstraint], settings: dict[str, Any]
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for constraint in constraints:
        result = evaluate_constraint(constraint, settings)
        if result is not None:
            issues.append(result)
    return issues
