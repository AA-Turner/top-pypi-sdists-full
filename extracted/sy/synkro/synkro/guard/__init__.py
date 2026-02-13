"""Real-time policy compliance guard for LLM gateways.

Example:
    >>> from synkro import PolicyGuard
    >>> guard = await PolicyGuard.from_policy("Max $50 Uber per week")
    >>> result = await guard.check_async(messages)
    >>> if not result.passed:
    ...     print(result.issues)
"""

from synkro.guard.guard import PolicyGuard
from synkro.guard.types import GuardResult

__all__ = ["PolicyGuard", "GuardResult"]
