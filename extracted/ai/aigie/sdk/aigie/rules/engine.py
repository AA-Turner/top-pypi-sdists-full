"""
LocalRulesEngine - Fast local rule evaluation for interception decisions.

This engine evaluates rules synchronously to achieve sub-5ms decision latency.
Rules are evaluated in priority order and can short-circuit on blocking decisions.
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Protocol

if TYPE_CHECKING:
    from ..config import Config
    from ..interceptor.protocols import InterceptionContext, PreCallResult

logger = logging.getLogger("aigie.rules")


class RuleDecision(Enum):
    """Decision from rule evaluation."""

    ALLOW = "allow"
    """Allow the request to proceed."""

    BLOCK = "block"
    """Block the request."""

    WARN = "warn"
    """Allow but log a warning."""

    CONSULT_BACKEND = "consult_backend"
    """Need backend consultation for this case."""

    SKIP = "skip"
    """Rule not applicable, skip to next rule."""


@dataclass
class RuleResult:
    """Result from rule evaluation."""

    decision: RuleDecision
    """The decision made by this rule."""

    reason: str | None = None
    """Human-readable reason for the decision."""

    confidence: float = 1.0
    """Confidence in this decision (0.0-1.0)."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata about the decision."""

    latency_ms: float = 0.0
    """Time taken to evaluate this rule in milliseconds."""

    rule_name: str | None = None
    """Name of the rule that produced this result."""

    @classmethod
    def allow(cls, rule_name: str = None, latency_ms: float = 0.0) -> "RuleResult":
        """Create an ALLOW result."""
        return cls(
            decision=RuleDecision.ALLOW,
            rule_name=rule_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def block(
        cls,
        reason: str,
        rule_name: str = None,
        latency_ms: float = 0.0,
        metadata: dict[str, Any] = None,
    ) -> "RuleResult":
        """Create a BLOCK result."""
        return cls(
            decision=RuleDecision.BLOCK,
            reason=reason,
            rule_name=rule_name,
            latency_ms=latency_ms,
            metadata=metadata or {},
        )

    @classmethod
    def warn(
        cls,
        reason: str,
        rule_name: str = None,
        latency_ms: float = 0.0,
    ) -> "RuleResult":
        """Create a WARN result."""
        return cls(
            decision=RuleDecision.WARN,
            reason=reason,
            rule_name=rule_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def consult(
        cls,
        reason: str = None,
        rule_name: str = None,
        latency_ms: float = 0.0,
    ) -> "RuleResult":
        """Create a CONSULT_BACKEND result."""
        return cls(
            decision=RuleDecision.CONSULT_BACKEND,
            reason=reason,
            rule_name=rule_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def skip(cls, rule_name: str = None, latency_ms: float = 0.0) -> "RuleResult":
        """Create a SKIP result (rule not applicable)."""
        return cls(
            decision=RuleDecision.SKIP,
            rule_name=rule_name,
            latency_ms=latency_ms,
        )


class Rule(Protocol):
    """
    Protocol for local rules.

    Rules must implement fast, synchronous evaluation (target: <1ms per rule).
    """

    @property
    def name(self) -> str:
        """Rule name for identification and logging."""
        ...

    @property
    def priority(self) -> int:
        """
        Rule priority (lower = earlier evaluation).

        Priority ranges:
        - 0-9: Critical (security, hard limits)
        - 10-19: High (cost limits, rate limits)
        - 20-29: Normal (content validation)
        - 30-39: Low (logging, metrics)
        - 40-49: Deferred (cleanup)
        """
        ...

    @property
    def enabled(self) -> bool:
        """Whether this rule is currently enabled."""
        ...

    def evaluate(self, ctx: "InterceptionContext") -> RuleResult:
        """
        Evaluate the rule synchronously.

        This method MUST be fast (<1ms target) as it runs synchronously
        in the request path.

        Args:
            ctx: The interception context to evaluate

        Returns:
            RuleResult with the decision
        """
        ...


@dataclass
class RuleEntry:
    """Entry in the rules engine with priority."""

    rule: Rule
    priority: int
    name: str
    enabled: bool = True


class LocalRulesEngine:
    """
    Fast local rules engine for interception decisions.

    Evaluates rules in priority order with short-circuit logic.
    Target latency: <5ms total for all rules.

    Features:
    - Priority-based rule ordering
    - Short-circuit on BLOCK decisions
    - Warning aggregation
    - Performance tracking
    - Rule enable/disable at runtime
    """

    def __init__(self, config: Optional["Config"] = None):
        """
        Initialize the rules engine.

        Args:
            config: Configuration for default rules and thresholds
        """
        self._config = config
        self._rules: list[RuleEntry] = []

        # Statistics
        self._stats = {
            "evaluations": 0,
            "blocks": 0,
            "warnings": 0,
            "consults": 0,
            "total_latency_ms": 0.0,
        }

        # Initialize built-in rules from config
        if config:
            self._init_builtin_rules(config)

    def _init_builtin_rules(self, config: "Config") -> None:
        """Initialize built-in rules from configuration."""
        from .builtin import (
            BlockedPatternsRule,
            ContextDriftRule,
            CostLimitRule,
            RateLimitRule,
            TokenLimitRule,
        )

        # Cost limit rules
        if config.cost_limit_per_request:
            self.add_rule(
                CostLimitRule(
                    max_cost=config.cost_limit_per_request,
                    limit_type="request",
                ),
                priority=10,
            )

        if config.cost_limit_per_trace:
            self.add_rule(
                CostLimitRule(
                    max_cost=config.cost_limit_per_trace,
                    limit_type="trace",
                ),
                priority=11,
            )

        # Token limit rule
        if config.token_limit_per_request:
            self.add_rule(
                TokenLimitRule(max_tokens=config.token_limit_per_request),
                priority=12,
            )

        # Blocked patterns rule
        if config.blocked_patterns:
            self.add_rule(
                BlockedPatternsRule(patterns=config.blocked_patterns),
                priority=5,  # High priority for security
            )

        # Rate limit rule
        if config.rate_limit_per_minute:
            self.add_rule(
                RateLimitRule(max_requests_per_minute=config.rate_limit_per_minute),
                priority=8,
            )

        # Drift detection rule
        if config.enable_drift_detection:
            self.add_rule(
                ContextDriftRule(threshold=config.drift_threshold),
                priority=25,
            )

    def add_rule(
        self,
        rule: Rule,
        priority: int | None = None,
        name: str | None = None,
    ) -> None:
        """
        Add a rule to the engine.

        Args:
            rule: The rule to add
            priority: Override priority (default: use rule.priority)
            name: Override name (default: use rule.name)
        """
        entry = RuleEntry(
            rule=rule,
            priority=priority if priority is not None else getattr(rule, "priority", 50),
            name=name or getattr(rule, "name", rule.__class__.__name__),
            enabled=getattr(rule, "enabled", True),
        )
        self._rules.append(entry)
        self._rules.sort(key=lambda e: e.priority)
        logger.debug(f"Added rule: {entry.name} (priority: {entry.priority})")

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name. Returns True if found and removed."""
        for i, entry in enumerate(self._rules):
            if entry.name == name:
                del self._rules[i]
                logger.debug(f"Removed rule: {name}")
                return True
        return False

    def enable_rule(self, name: str, enabled: bool = True) -> bool:
        """Enable or disable a rule by name. Returns True if found."""
        for entry in self._rules:
            if entry.name == name:
                entry.enabled = enabled
                logger.debug(f"{'Enabled' if enabled else 'Disabled'} rule: {name}")
                return True
        return False

    async def evaluate(self, ctx: "InterceptionContext") -> "PreCallResult":
        """
        Evaluate all rules on the context.

        Rules are evaluated in priority order. Short-circuits on BLOCK.
        WARN results are aggregated but don't stop evaluation.
        CONSULT_BACKEND triggers backend consultation.

        Args:
            ctx: The interception context

        Returns:
            PreCallResult with the aggregated decision
        """
        from ..interceptor.protocols import PreCallResult

        start_time = time.perf_counter()
        self._stats["evaluations"] += 1

        warnings: list[str] = []
        should_consult = False
        consult_reasons: list[str] = []

        for entry in self._rules:
            if not entry.enabled:
                continue

            try:
                rule_start = time.perf_counter()
                result = entry.rule.evaluate(ctx)
                rule_latency = (time.perf_counter() - rule_start) * 1000
                result.latency_ms = rule_latency
                result.rule_name = entry.name

                if result.decision == RuleDecision.BLOCK:
                    self._stats["blocks"] += 1
                    total_latency = (time.perf_counter() - start_time) * 1000
                    self._stats["total_latency_ms"] += total_latency

                    return PreCallResult.block(
                        reason=result.reason or f"Blocked by rule: {entry.name}",
                        hook_name=f"rule:{entry.name}",
                        latency_ms=total_latency,
                    )

                if result.decision == RuleDecision.WARN:
                    self._stats["warnings"] += 1
                    warnings.append(result.reason or f"Warning from rule: {entry.name}")
                    logger.warning(f"Rule {entry.name}: {result.reason}")

                if result.decision == RuleDecision.CONSULT_BACKEND:
                    self._stats["consults"] += 1
                    should_consult = True
                    if result.reason:
                        consult_reasons.append(result.reason)

            except Exception as e:
                logger.error(f"Rule {entry.name} evaluation error: {e}")
                # Continue to next rule on error

        total_latency = (time.perf_counter() - start_time) * 1000
        self._stats["total_latency_ms"] += total_latency

        # Check if we need backend consultation
        if should_consult:
            return PreCallResult.consult(
                reason="; ".join(consult_reasons)
                if consult_reasons
                else "Backend consultation requested",
                hook_name="rules_engine",
                latency_ms=total_latency,
            )

        # All rules passed
        return PreCallResult.allow(
            hook_name="rules_engine",
            latency_ms=total_latency,
        )

    def get_stats(self) -> dict[str, Any]:
        """Get engine statistics."""
        return {
            **self._stats,
            "rules_count": len(self._rules),
            "enabled_rules": sum(1 for r in self._rules if r.enabled),
            "avg_latency_ms": (
                self._stats["total_latency_ms"] / max(self._stats["evaluations"], 1)
            ),
        }

    def reset_stats(self) -> None:
        """Reset engine statistics."""
        self._stats = {
            "evaluations": 0,
            "blocks": 0,
            "warnings": 0,
            "consults": 0,
            "total_latency_ms": 0.0,
        }

    def list_rules(self) -> list[dict[str, Any]]:
        """List all registered rules."""
        return [
            {
                "name": entry.name,
                "priority": entry.priority,
                "enabled": entry.enabled,
                "type": entry.rule.__class__.__name__,
            }
            for entry in self._rules
        ]
