"""
Built-in rules for common interception use cases.

These rules are designed for fast evaluation (<1ms each) and cover
common scenarios like cost limits, rate limits, and content filtering.
"""

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .engine import RuleResult

if TYPE_CHECKING:
    from ..interceptor.protocols import InterceptionContext

logger = logging.getLogger("aigie.rules")


@dataclass
class CostLimitRule:
    """
    Rule to enforce cost limits per request or trace.

    Blocks requests that would exceed the configured cost threshold.
    """

    max_cost: float
    """Maximum allowed cost in dollars."""

    limit_type: str = "request"
    """Type of limit: 'request' or 'trace'."""

    @property
    def name(self) -> str:
        return f"cost_limit_{self.limit_type}"

    @property
    def priority(self) -> int:
        return 10

    @property
    def enabled(self) -> bool:
        return True

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if estimated cost exceeds the limit."""
        if self.limit_type == "request":
            cost = ctx.estimated_cost
            if cost > self.max_cost:
                return RuleResult.block(
                    reason=f"Estimated cost ${cost:.4f} exceeds limit ${self.max_cost:.4f}",
                    rule_name=self.name,
                    metadata={"estimated_cost": cost, "limit": self.max_cost},
                )
        elif self.limit_type == "trace":
            total_cost = ctx.accumulated_cost + ctx.estimated_cost
            if total_cost > self.max_cost:
                return RuleResult.block(
                    reason=f"Trace cost ${total_cost:.4f} would exceed limit ${self.max_cost:.4f}",
                    rule_name=self.name,
                    metadata={
                        "accumulated_cost": ctx.accumulated_cost,
                        "estimated_cost": ctx.estimated_cost,
                        "limit": self.max_cost,
                    },
                )

        return RuleResult.allow(rule_name=self.name)


@dataclass
class TokenLimitRule:
    """
    Rule to enforce token limits per request.

    Blocks requests that would exceed the configured token threshold.
    """

    max_tokens: int
    """Maximum allowed tokens (input + estimated output)."""

    @property
    def name(self) -> str:
        return "token_limit"

    @property
    def priority(self) -> int:
        return 12

    @property
    def enabled(self) -> bool:
        return True

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if estimated tokens exceed the limit."""
        total_tokens = ctx.estimated_input_tokens + ctx.estimated_output_tokens

        if total_tokens > self.max_tokens:
            return RuleResult.block(
                reason=f"Estimated tokens {total_tokens} exceeds limit {self.max_tokens}",
                rule_name=self.name,
                metadata={
                    "estimated_input_tokens": ctx.estimated_input_tokens,
                    "estimated_output_tokens": ctx.estimated_output_tokens,
                    "total": total_tokens,
                    "limit": self.max_tokens,
                },
            )

        return RuleResult.allow(rule_name=self.name)


@dataclass
class BlockedPatternsRule:
    """
    Rule to block requests containing specific patterns.

    Uses regex matching for flexible pattern detection.
    Commonly used for security (prompt injection) or policy enforcement.
    """

    patterns: list[str] = field(default_factory=list)
    """List of regex patterns to block."""

    case_sensitive: bool = False
    """Whether pattern matching is case-sensitive."""

    _compiled_patterns: list[re.Pattern] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        """Compile regex patterns for efficient matching."""
        flags = 0 if self.case_sensitive else re.IGNORECASE
        self._compiled_patterns = [re.compile(pattern, flags) for pattern in self.patterns]

    @property
    def name(self) -> str:
        return "blocked_patterns"

    @property
    def priority(self) -> int:
        return 5  # High priority for security

    @property
    def enabled(self) -> bool:
        return bool(self.patterns)

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if any message contains blocked patterns."""
        if not self._compiled_patterns:
            return RuleResult.skip(rule_name=self.name)

        # Check all messages
        for msg in ctx.messages:
            content = str(msg.get("content", ""))
            for i, pattern in enumerate(self._compiled_patterns):
                if pattern.search(content):
                    return RuleResult.block(
                        reason=f"Message contains blocked pattern: {self.patterns[i]}",
                        rule_name=self.name,
                        metadata={
                            "pattern": self.patterns[i],
                            "message_role": msg.get("role"),
                        },
                    )

        return RuleResult.allow(rule_name=self.name)


@dataclass
class RateLimitRule:
    """
    Rule to enforce rate limits per minute.

    Uses a sliding window counter for rate limiting.
    """

    max_requests_per_minute: int
    """Maximum requests allowed per minute."""

    # Internal state
    _request_times: dict[str, list[datetime]] = field(
        default_factory=lambda: defaultdict(list),
        init=False,
        repr=False,
    )

    @property
    def name(self) -> str:
        return "rate_limit"

    @property
    def priority(self) -> int:
        return 8

    @property
    def enabled(self) -> bool:
        return self.max_requests_per_minute > 0

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if rate limit is exceeded."""
        # Use user_id or trace_id as the rate limit key
        key = ctx.user_id or ctx.trace_id or "global"
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=1)

        # Clean old entries and count recent requests
        self._request_times[key] = [t for t in self._request_times[key] if t > window_start]
        recent_count = len(self._request_times[key])

        if recent_count >= self.max_requests_per_minute:
            return RuleResult.block(
                reason=f"Rate limit exceeded: {recent_count}/{self.max_requests_per_minute} requests per minute",
                rule_name=self.name,
                metadata={
                    "current_rate": recent_count,
                    "limit": self.max_requests_per_minute,
                    "key": key,
                },
            )

        # Record this request
        self._request_times[key].append(now)

        # Warn if approaching limit
        if recent_count >= self.max_requests_per_minute * 0.8:
            return RuleResult.warn(
                reason=f"Approaching rate limit: {recent_count}/{self.max_requests_per_minute}",
                rule_name=self.name,
            )

        return RuleResult.allow(rule_name=self.name)


@dataclass
class ContextDriftRule:
    """
    Rule to detect context drift using local heuristics.

    For high-confidence drift detection, suggests backend consultation.
    """

    threshold: float = 0.7
    """Drift score threshold (0.0-1.0) for flagging issues."""

    consult_threshold: float = 0.5
    """Drift score threshold for requesting backend consultation."""

    @property
    def name(self) -> str:
        return "context_drift"

    @property
    def priority(self) -> int:
        return 25

    @property
    def enabled(self) -> bool:
        return True

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check for context drift."""
        # If drift score is already computed
        if ctx.drift_score is not None:
            if ctx.drift_score >= self.threshold:
                return RuleResult.consult(
                    reason=f"High context drift detected: {ctx.drift_score:.2f}",
                    rule_name=self.name,
                )
            if ctx.drift_score >= self.consult_threshold:
                return RuleResult.warn(
                    reason=f"Moderate context drift: {ctx.drift_score:.2f}",
                    rule_name=self.name,
                )
            return RuleResult.allow(rule_name=self.name)

        # Quick heuristic check if no drift score
        if ctx.previous_context_hash and ctx.context_hash:
            if ctx.previous_context_hash != ctx.context_hash:
                # Context changed - suggest backend check for complex analysis
                return RuleResult.consult(
                    reason="Context changed, backend analysis recommended",
                    rule_name=self.name,
                )

        return RuleResult.allow(rule_name=self.name)


@dataclass
class ModelAllowlistRule:
    """
    Rule to restrict which models can be used.

    Blocks requests to models not in the allowlist.
    """

    allowed_models: list[str] = field(default_factory=list)
    """List of allowed model names (supports wildcards with *)."""

    @property
    def name(self) -> str:
        return "model_allowlist"

    @property
    def priority(self) -> int:
        return 3  # Very high priority

    @property
    def enabled(self) -> bool:
        return bool(self.allowed_models)

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if the model is in the allowlist."""
        if not self.allowed_models:
            return RuleResult.skip(rule_name=self.name)

        model = ctx.model.lower()

        for allowed in self.allowed_models:
            allowed_lower = allowed.lower()
            if allowed_lower.endswith("*"):
                # Prefix match
                if model.startswith(allowed_lower[:-1]):
                    return RuleResult.allow(rule_name=self.name)
            elif model == allowed_lower:
                return RuleResult.allow(rule_name=self.name)

        return RuleResult.block(
            reason=f"Model '{ctx.model}' not in allowlist",
            rule_name=self.name,
            metadata={"model": ctx.model, "allowed": self.allowed_models},
        )


@dataclass
class ProviderAllowlistRule:
    """
    Rule to restrict which providers can be used.

    Blocks requests to providers not in the allowlist.
    """

    allowed_providers: list[str] = field(default_factory=list)
    """List of allowed provider names."""

    @property
    def name(self) -> str:
        return "provider_allowlist"

    @property
    def priority(self) -> int:
        return 2  # Very high priority

    @property
    def enabled(self) -> bool:
        return bool(self.allowed_providers)

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if the provider is in the allowlist."""
        if not self.allowed_providers:
            return RuleResult.skip(rule_name=self.name)

        provider = ctx.provider.lower()

        if provider in [p.lower() for p in self.allowed_providers]:
            return RuleResult.allow(rule_name=self.name)

        return RuleResult.block(
            reason=f"Provider '{ctx.provider}' not in allowlist",
            rule_name=self.name,
            metadata={"provider": ctx.provider, "allowed": self.allowed_providers},
        )


@dataclass
class MaxMessagesRule:
    """
    Rule to limit the number of messages in a conversation.

    Prevents context window overflow and excessive API costs.
    """

    max_messages: int = 100
    """Maximum number of messages allowed."""

    @property
    def name(self) -> str:
        return "max_messages"

    @property
    def priority(self) -> int:
        return 15

    @property
    def enabled(self) -> bool:
        return self.max_messages > 0

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """Check if message count exceeds limit."""
        message_count = len(ctx.messages)

        if message_count > self.max_messages:
            return RuleResult.block(
                reason=f"Message count {message_count} exceeds limit {self.max_messages}",
                rule_name=self.name,
                metadata={"count": message_count, "limit": self.max_messages},
            )

        # Warn if approaching limit
        if message_count > self.max_messages * 0.8:
            return RuleResult.warn(
                reason=f"Approaching message limit: {message_count}/{self.max_messages}",
                rule_name=self.name,
            )

        return RuleResult.allow(rule_name=self.name)
