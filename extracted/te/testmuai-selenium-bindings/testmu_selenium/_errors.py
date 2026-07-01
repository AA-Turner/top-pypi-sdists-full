"""Public exception classes for testmu_selenium.

These are the exception types that:
- Generated test.py code may catch (NoSuchElementException, StaleElementReferenceException
  etc. from selenium.common.exceptions are caught at the test level)
- Heal cascade may raise (AutohealExhausted, HealAuthError)
- Click strategy fallback may raise (ClickAllMethodsFailed)
- Configuration validation may raise (TestmuConfigError)
"""
from selenium.common.exceptions import ElementClickInterceptedException


class TestmuConfigError(Exception):
    """Raised when configure(**kwargs) receives invalid or missing required config."""


class HealTierMiss(Exception):
    """Internal: raised by individual heal tiers when their attempt produces no candidates.
    Caught by the cascade dispatcher to advance to the next tier.
    Should not propagate out of _heal_cascade()."""

    def __init__(self, tier: str, reason: str | Exception):
        self.tier = tier
        self.reason = reason
        super().__init__(f"[heal] tier {tier} miss: {reason}")


class HealAuthError(Exception):
    """Raised when AUTOMIND returns 401/403 — config / credential issue.
    Not retried; not caught by retry-loop; propagates as deploy/config error."""

    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        super().__init__(f"AUTOMIND auth error (status {status_code}): {message}")


class AutohealExhausted(Exception):
    """Raised by _heal_cascade when all configured tiers miss.
    Carries the original Selenium exception that triggered heal + the last tier-miss reason.
    NOT in the retry-loop's catch tuple — propagates uncaught → terminal test failure."""

    def __init__(self, original: Exception, last_miss: Exception | None = None):
        self.original = original
        self.last_miss = last_miss
        super().__init__(f"all heal tiers miss; original: {original}; last_miss: {last_miss}")


class ClickAllMethodsFailed(ElementClickInterceptedException):
    """Raised by clickElement when all configured fallback strategies (SE→JS→AC) exhaust.
    Subclasses ElementClickInterceptedException so the retry-loop's recoverable-exception
    tuple naturally catches it and triggers heal."""


class ConditionEvaluationError(Exception):
    """Raised by check_until_condition when an until-condition expression cannot
    be evaluated locally — natural language, a syntax error, or an unknown name.

    Selenium V3 export evaluates conditions as Python expressions; an unevaluable
    condition is a generation/authoring error, not a 'condition not met' result,
    so it surfaces loudly instead of silently returning False (which would let a
    retry loop exhaust its budget while masking the real problem)."""

    def __init__(self, condition: str, original: Exception):
        self.condition = condition
        self.original = original
        super().__init__(f"could not evaluate until-condition {condition!r}: {original}")
