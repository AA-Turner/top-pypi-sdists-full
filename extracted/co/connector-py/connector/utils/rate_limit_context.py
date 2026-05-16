from contextvars import ContextVar
from dataclasses import dataclass
from typing import Literal

from connector_sdk_types.generated import (
    RateLimitMode,
    RateLimitStateSnapshot,
    StandardCapabilityName,
)


@dataclass(frozen=True)
class RateLimitExecutionContext:
    capability_name: StandardCapabilityName | str
    capability_level: Literal["read", "write"]
    # Set from request.rate_limit.caller_override_mode
    caller_override_mode: RateLimitMode | None
    # Set from CapabilityMetadata.rate_limit_mode at capability registration time
    capability_override_mode: RateLimitMode | None = None
    # Carried from request.rate_limit.last_known_state to seed the RateLimiter.
    # Keyed by config_id so each tier's state seeds the correct limiter.
    last_known_state: dict[str, RateLimitStateSnapshot] | None = None
    # Absolute Unix timestamp deadline derived from request.rate_limit.max_execution_time.
    deadline: float | None = None


RATE_LIMIT_CONTEXT: ContextVar[RateLimitExecutionContext | None] = ContextVar(
    "rate_limit_context",
    default=None,
)

# Written by BaseIntegrationClient.__aexit__ so the executor can collect it for the response.
# Keyed by config_id so multi-tier connectors accumulate all states in one pass.
RATE_LIMIT_RESULT_CONTEXT: ContextVar[dict[str, RateLimitStateSnapshot] | None] = ContextVar(
    "rate_limit_result_context",
    default=None,
)


class RateLimitCtx:
    """Bundles the rate limit execution context and provides access to the result state."""

    __slots__ = ("execution_ctx",)

    def __init__(self, execution_ctx: RateLimitExecutionContext) -> None:
        self.execution_ctx = execution_ctx

    @property
    def result_state(self) -> dict[str, RateLimitStateSnapshot] | None:
        return RATE_LIMIT_RESULT_CONTEXT.get()
