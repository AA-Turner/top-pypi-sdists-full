import logging
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from connector_sdk_types.generated import RateLimitMode
from connector_sdk_types.oai.modules.rate_limiting_types import (
    RateLimitPolicySource,
)

from connector.utils.rate_limit_context import (
    RATE_LIMIT_CONTEXT,
    RateLimitExecutionContext,
)
from connector.utils.rate_limiting import RateLimitConfig

logger = logging.getLogger(__name__)


def _resolve_rate_limiting_mode(
    ctx: RateLimitExecutionContext | None, config: RateLimitConfig
) -> tuple[RateLimitMode, RateLimitPolicySource]:
    """Determine the effective RateLimitMode and its source for this execution.

    Priority (highest → lowest):
    1. Capability-level override
    2. Connector-wide override
    3. Caller requested mode
    4. SDK default: write = retry_only, read = enforce
    """

    # Capability-level override
    if ctx is not None and ctx.capability_override_mode is not None:
        return ctx.capability_override_mode, RateLimitPolicySource.CAPABILITY

    # Connector-wide override
    if config.mode is not None:
        return config.mode, RateLimitPolicySource.CONNECTOR

    # Caller requested mode
    if ctx is not None and ctx.caller_override_mode is not None:
        return ctx.caller_override_mode, RateLimitPolicySource.CALLER

    # SDK default: write capabilities don't block callers, reads enforce window
    if ctx is not None and ctx.capability_level == "write":
        return RateLimitMode.RETRY_ONLY, RateLimitPolicySource.SDK
    return RateLimitMode.ENFORCE, RateLimitPolicySource.SDK


@dataclass(frozen=True)
class ResolvedRateLimit:
    ctx: RateLimitExecutionContext | None
    config: RateLimitConfig
    mode: RateLimitMode
    policy_source: RateLimitPolicySource


def rate_limit_mode_guard() -> Callable[..., Any]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            rate_limit_config = kwargs["rate_limit_config"]

            ctx = RATE_LIMIT_CONTEXT.get()
            mode, src = _resolve_rate_limiting_mode(ctx, rate_limit_config)

            capability_name = ctx.capability_name if ctx else "unknown"
            logger.debug(f"[RateLimiting] mode={mode=} source={src=} capability={capability_name=}")

            if mode == RateLimitMode.BYPASS:
                return

            effective = (
                rate_limit_config.model_copy(update={"mode": mode})
                if mode != rate_limit_config.mode
                else rate_limit_config
            )

            resolved = ResolvedRateLimit(
                ctx=ctx,
                config=effective,
                mode=mode,
                policy_source=src,
            )

            return fn(*args, resolved=resolved, **kwargs)

        return wrapper

    return decorator
