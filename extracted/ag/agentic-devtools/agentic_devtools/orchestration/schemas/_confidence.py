"""ConfidenceScore annotated type for structured LLM output schemas.

Provides a float type constrained to [0.0, 1.0] with int→float coercion.
"""

from __future__ import annotations

import math
from typing import Annotated, Any

from pydantic import AfterValidator, BeforeValidator


def _coerce_int_to_float(value: Any) -> Any:
    """Coerce integer values (0, 1) to float for confidence scores."""
    if isinstance(value, int) and not isinstance(value, bool):
        return float(value)
    return value


def _validate_confidence_range(value: float) -> float:
    """Validate that confidence score is within [0.0, 1.0].

    Non-finite values (NaN, ±Inf) are explicitly rejected because NaN comparisons
    always return False, allowing NaN to silently bypass the [0.0, 1.0] range check.
    """
    if not math.isfinite(value):
        msg = f"Confidence score must be a finite number, got {value}"
        raise ValueError(msg)
    if value < 0.0 or value > 1.0:
        msg = f"Confidence score must be between 0.0 and 1.0, got {value}"
        raise ValueError(msg)
    return value


ConfidenceScore = Annotated[
    float,
    BeforeValidator(_coerce_int_to_float),
    AfterValidator(_validate_confidence_range),
]
"""A float constrained to [0.0, 1.0] representing confidence in a decision.

Accepts integers 0 and 1 (coerced to 0.0 and 1.0 respectively).
"""
