"""Policy validation exceptions."""

from __future__ import annotations


class PolicyValidationError(Exception):
    """Raised when a policy configuration value is invalid.

    Attributes:
        field_path: Dot-separated path to the invalid field (e.g., 'pr_review.confidence_minimum').
        invalid_value: The value that failed validation.
        constraint: Description of the constraint that was violated.
    """

    def __init__(
        self,
        field_path: str,
        invalid_value: object,
        constraint: str,
    ) -> None:
        self.field_path = field_path
        self.invalid_value = invalid_value
        self.constraint = constraint
        super().__init__(
            f"Policy validation error at '{field_path}': value {invalid_value!r} violates constraint: {constraint}"
        )
