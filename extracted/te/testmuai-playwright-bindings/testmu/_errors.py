"""Testmu exception classes."""


class TestmuConfigError(Exception):
    """Raised when a required configuration is missing (no LT creds, no env fallback)."""
    pass


class ConditionEvaluationError(Exception):
    """Raised by check_until_condition when an until-condition expression cannot
    be evaluated locally — natural language, a syntax error, or an unknown name.

    Parity with testmu_selenium._errors.ConditionEvaluationError. The generated
    test evaluates conditions as Python expressions; an unevaluable condition is a
    generation/authoring error, not a 'condition not met' result, so it surfaces
    loudly instead of silently returning False (which would let a retry loop
    exhaust its budget while masking the real problem)."""

    def __init__(self, condition: str, original: Exception):
        self.condition = condition
        self.original = original
        super().__init__(f"could not evaluate until-condition {condition!r}: {original}")


class AutohealExhausted(Exception):
    """Raised when the heal cascade cannot recover an action.

    Both direct heal entry and the Locator patch (_heal_patch) raise this
    class so callers can catch one exception type for exhaustion. Uses a
    plain message constructor; chaining is expressed via ``raise ... from``
    at the call site instead.
    """
    pass
