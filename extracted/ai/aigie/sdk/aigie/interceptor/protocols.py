"""
Protocol definitions for the Aigie Interception Layer.

This module defines the core types and protocols used for real-time
interception of LLM calls, enabling pre-call and post-call hooks
with a hybrid local/backend decision approach.
"""

import hashlib
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol


class InterceptionDecision(Enum):
    """Decision made by interception hooks."""

    ALLOW = "allow"
    """Allow request to proceed normally."""

    BLOCK = "block"
    """Block request entirely."""

    MODIFY = "modify"
    """Allow request with modifications applied."""

    RETRY = "retry"
    """Retry the request with corrections applied."""

    CONSULT = "consult"
    """Need backend consultation for complex decision."""

    DEFER = "defer"
    """Defer decision to the next hook in chain."""


class FixActionType(Enum):
    """Types of fix actions that can be applied."""

    MODIFY_REQUEST = "modify_request"
    """Modify the LLM request before sending."""

    MODIFY_RESPONSE = "modify_response"
    """Modify the LLM response before returning."""

    RETRY = "retry"
    """Retry the request with modifications."""

    FALLBACK = "fallback"
    """Use a fallback response or model."""

    TRUNCATE_CONTEXT = "truncate_context"
    """Truncate context to reduce token count."""

    INJECT_INSTRUCTION = "inject_instruction"
    """Inject corrective instruction into messages."""

    OVERRIDE_RESPONSE = "override_response"
    """Completely override the response."""

    ESCALATE = "escalate"
    """Escalate to human review."""

    LOG_ONLY = "log_only"
    """Log the issue but take no action."""


@dataclass
class FixAction:
    """Action to apply as a fix for detected issues."""

    action_type: FixActionType
    """Type of fix action to apply."""

    parameters: dict[str, Any] = field(default_factory=dict)
    """Parameters for the fix action."""

    confidence: float = 0.0
    """Confidence score for this fix (0.0-1.0)."""

    source: str = "local"
    """Source of the fix: 'local', 'backend', 'user'."""

    reason: str | None = None
    """Human-readable reason for this fix."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata about the fix."""


@dataclass
class InterceptionContext:
    """
    Context passed through the interception chain.

    Contains all information about the LLM request and response,
    enabling hooks to make informed decisions about interception.
    """

    # Request information
    provider: str
    """LLM provider (e.g., 'openai', 'anthropic', 'google')."""

    model: str
    """Model identifier (e.g., 'gpt-4', 'claude-3-opus')."""

    messages: list[dict[str, Any]] = field(default_factory=list)
    """Input messages for the LLM call."""

    request_kwargs: dict[str, Any] = field(default_factory=dict)
    """Additional request parameters (temperature, max_tokens, etc.)."""

    # Trace context
    trace_id: str | None = None
    """Parent trace ID for this call."""

    span_id: str | None = None
    """Span ID for this call."""

    parent_span_id: str | None = None
    """Parent span ID if nested."""

    # Cost and usage estimation (pre-call)
    estimated_input_tokens: int = 0
    """Estimated input token count."""

    estimated_output_tokens: int = 0
    """Estimated output token count (based on max_tokens or heuristics)."""

    estimated_cost: float = 0.0
    """Estimated cost for this call."""

    accumulated_cost: float = 0.0
    """Total cost accumulated in this trace so far."""

    # Timing
    timestamp: datetime = field(default_factory=datetime.utcnow)
    """Timestamp when interception started."""

    # Response information (set after LLM call)
    response: Any | None = None
    """Raw LLM response object."""

    response_content: str | None = None
    """Extracted response content/text."""

    actual_input_tokens: int = 0
    """Actual input tokens used."""

    actual_output_tokens: int = 0
    """Actual output tokens generated."""

    actual_cost: float = 0.0
    """Actual cost of the call."""

    response_time_ms: float = 0.0
    """Response time in milliseconds."""

    # Context drift tracking
    context_hash: str | None = None
    """Hash of current context for drift detection."""

    previous_context_hash: str | None = None
    """Hash of previous context in the chain."""

    drift_score: float | None = None
    """Detected drift score (0.0 = no drift, 1.0 = complete drift)."""

    drift_details: dict[str, Any] = field(default_factory=dict)
    """Details about detected drift."""

    # Error tracking
    error: Exception | None = None
    """Exception if the LLM call failed."""

    error_type: str | None = None
    """Type of error (e.g., 'rate_limit', 'context_length', 'api_error')."""

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata from the application."""

    tags: list[str] = field(default_factory=list)
    """Tags associated with this call."""

    user_id: str | None = None
    """User ID if available."""

    session_id: str | None = None
    """Session ID if available."""

    # Auto-fix and retry
    fixes_applied: list["FixAction"] = field(default_factory=list)
    """List of fix actions applied or to apply."""

    retry_count: int = 0
    """Number of retries attempted."""

    def compute_context_hash(self) -> str:
        """Compute a hash of the current context for drift detection."""
        context_data = {
            "messages": self.messages[-5:] if self.messages else [],  # Last 5 messages
            "model": self.model,
            "provider": self.provider,
        }
        context_str = json.dumps(context_data, sort_keys=True, default=str)
        return hashlib.sha256(context_str.encode()).hexdigest()[:16]

    def with_response(
        self,
        response: Any,
        content: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0,
        response_time_ms: float = 0.0,
    ) -> "InterceptionContext":
        """Create a new context with response data filled in."""
        return InterceptionContext(
            # Copy request info
            provider=self.provider,
            model=self.model,
            messages=self.messages,
            request_kwargs=self.request_kwargs,
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            estimated_input_tokens=self.estimated_input_tokens,
            estimated_output_tokens=self.estimated_output_tokens,
            estimated_cost=self.estimated_cost,
            accumulated_cost=self.accumulated_cost,
            timestamp=self.timestamp,
            context_hash=self.context_hash,
            previous_context_hash=self.previous_context_hash,
            drift_score=self.drift_score,
            drift_details=self.drift_details,
            metadata=self.metadata,
            tags=self.tags,
            user_id=self.user_id,
            session_id=self.session_id,
            # Add response info
            response=response,
            response_content=content,
            actual_input_tokens=input_tokens,
            actual_output_tokens=output_tokens,
            actual_cost=cost,
            response_time_ms=response_time_ms,
        )

    def with_error(
        self,
        error: Exception,
        error_type: str | None = None,
    ) -> "InterceptionContext":
        """Create a new context with error information."""
        return InterceptionContext(
            # Copy all existing fields
            provider=self.provider,
            model=self.model,
            messages=self.messages,
            request_kwargs=self.request_kwargs,
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            estimated_input_tokens=self.estimated_input_tokens,
            estimated_output_tokens=self.estimated_output_tokens,
            estimated_cost=self.estimated_cost,
            accumulated_cost=self.accumulated_cost,
            timestamp=self.timestamp,
            context_hash=self.context_hash,
            previous_context_hash=self.previous_context_hash,
            drift_score=self.drift_score,
            drift_details=self.drift_details,
            metadata=self.metadata,
            tags=self.tags,
            user_id=self.user_id,
            session_id=self.session_id,
            response=self.response,
            response_content=self.response_content,
            actual_input_tokens=self.actual_input_tokens,
            actual_output_tokens=self.actual_output_tokens,
            actual_cost=self.actual_cost,
            response_time_ms=self.response_time_ms,
            # Add error info
            error=error,
            error_type=error_type or type(error).__name__,
        )


@dataclass
class PreCallResult:
    """Result from pre-call interception."""

    decision: InterceptionDecision
    """Decision about whether to proceed with the call."""

    reason: str | None = None
    """Human-readable reason for the decision."""

    modified_messages: list[dict[str, Any]] | None = None
    """Modified messages if decision is MODIFY."""

    modified_kwargs: dict[str, Any] | None = None
    """Modified request kwargs if decision is MODIFY."""

    fixes_applied: list[FixAction] = field(default_factory=list)
    """List of fixes that were applied."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata from the hook."""

    latency_ms: float = 0.0
    """Time taken by this hook in milliseconds."""

    hook_name: str | None = None
    """Name of the hook that produced this result."""

    @classmethod
    def allow(cls, hook_name: str = None, latency_ms: float = 0.0) -> "PreCallResult":
        """Create an ALLOW result."""
        return cls(
            decision=InterceptionDecision.ALLOW,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def block(
        cls,
        reason: str,
        hook_name: str = None,
        latency_ms: float = 0.0,
    ) -> "PreCallResult":
        """Create a BLOCK result."""
        return cls(
            decision=InterceptionDecision.BLOCK,
            reason=reason,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def modify(
        cls,
        messages: list[dict[str, Any]] = None,
        kwargs: dict[str, Any] = None,
        reason: str = None,
        hook_name: str = None,
        latency_ms: float = 0.0,
    ) -> "PreCallResult":
        """Create a MODIFY result."""
        return cls(
            decision=InterceptionDecision.MODIFY,
            reason=reason,
            modified_messages=messages,
            modified_kwargs=kwargs,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def consult(
        cls,
        reason: str = None,
        hook_name: str = None,
        latency_ms: float = 0.0,
    ) -> "PreCallResult":
        """Create a CONSULT result (need backend decision)."""
        return cls(
            decision=InterceptionDecision.CONSULT,
            reason=reason,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def defer(cls, hook_name: str = None, latency_ms: float = 0.0) -> "PreCallResult":
        """Create a DEFER result (let next hook decide)."""
        return cls(
            decision=InterceptionDecision.DEFER,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )


@dataclass
class PostCallResult:
    """Result from post-call interception."""

    decision: InterceptionDecision
    """Decision about the response."""

    reason: str | None = None
    """Human-readable reason for the decision."""

    modified_response: Any | None = None
    """Modified response if decision is MODIFY."""

    modified_content: str | None = None
    """Modified response content if decision is MODIFY."""

    fixes_applied: list[FixAction] = field(default_factory=list)
    """List of fixes that were applied."""

    should_retry: bool = False
    """Whether to retry the request."""

    retry_kwargs: dict[str, Any] | None = None
    """Modified kwargs for retry if should_retry is True."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata from the hook."""

    latency_ms: float = 0.0
    """Time taken by this hook in milliseconds."""

    hook_name: str | None = None
    """Name of the hook that produced this result."""

    @classmethod
    def allow(cls, hook_name: str = None, latency_ms: float = 0.0) -> "PostCallResult":
        """Create an ALLOW result."""
        return cls(
            decision=InterceptionDecision.ALLOW,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def modify(
        cls,
        response: Any = None,
        content: str = None,
        reason: str = None,
        fixes: list[FixAction] = None,
        hook_name: str = None,
        latency_ms: float = 0.0,
    ) -> "PostCallResult":
        """Create a MODIFY result."""
        return cls(
            decision=InterceptionDecision.MODIFY,
            reason=reason,
            modified_response=response,
            modified_content=content,
            fixes_applied=fixes or [],
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def retry(
        cls,
        reason: str,
        instruction: str = None,
        retry_kwargs: dict[str, Any] = None,
        hook_name: str = None,
        latency_ms: float = 0.0,
    ) -> "PostCallResult":
        """Create a result indicating retry is needed with corrective instruction.

        Args:
            reason: Human-readable reason for retry
            instruction: Corrective instruction to inject into the prompt
            retry_kwargs: Modified kwargs for the retry call
            hook_name: Name of the hook
            latency_ms: Time taken by hook
        """
        fixes = []
        if instruction:
            fixes.append(
                FixAction(
                    action_type=FixActionType.INJECT_INSTRUCTION,
                    confidence=0.9,
                    reason=reason,
                    parameters={"instruction": instruction},
                )
            )
        return cls(
            decision=InterceptionDecision.RETRY,
            reason=reason,
            should_retry=True,
            retry_kwargs=retry_kwargs,
            fixes_applied=fixes,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def consult(
        cls,
        reason: str = None,
        hook_name: str = None,
        latency_ms: float = 0.0,
    ) -> "PostCallResult":
        """Create a CONSULT result (need backend decision)."""
        return cls(
            decision=InterceptionDecision.CONSULT,
            reason=reason,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )

    @classmethod
    def defer(cls, hook_name: str = None, latency_ms: float = 0.0) -> "PostCallResult":
        """Create a DEFER result (let next hook decide)."""
        return cls(
            decision=InterceptionDecision.DEFER,
            hook_name=hook_name,
            latency_ms=latency_ms,
        )


class PreCallHook(Protocol):
    """
    Protocol for pre-call interception hooks.

    Pre-call hooks are executed before the LLM call is made.
    They can inspect and modify the request, or block it entirely.
    """

    @property
    def name(self) -> str:
        """Hook name for identification and logging."""
        ...

    @property
    def priority(self) -> int:
        """
        Hook priority (lower = earlier execution).

        Priority ranges:
        - 0-19: Critical (security, rate limiting)
        - 20-39: High (cost control, validation)
        - 40-59: Normal (default)
        - 60-79: Low (logging, metrics)
        - 80-99: Deferred (cleanup)
        """
        ...

    async def __call__(self, ctx: InterceptionContext) -> PreCallResult:
        """
        Evaluate context before LLM call.

        Args:
            ctx: Interception context with request information

        Returns:
            PreCallResult with decision and optional modifications
        """
        ...


class PostCallHook(Protocol):
    """
    Protocol for post-call interception hooks.

    Post-call hooks are executed after the LLM call completes.
    They can inspect and modify the response, trigger retries,
    or apply fixes for detected issues.
    """

    @property
    def name(self) -> str:
        """Hook name for identification and logging."""
        ...

    @property
    def priority(self) -> int:
        """
        Hook priority (lower = earlier execution).

        Priority ranges:
        - 0-19: Critical (error recovery, safety)
        - 20-39: High (quality validation, drift detection)
        - 40-59: Normal (default)
        - 60-79: Low (logging, metrics)
        - 80-99: Deferred (cleanup, caching)
        """
        ...

    async def __call__(self, ctx: InterceptionContext) -> PostCallResult:
        """
        Evaluate context after LLM call.

        Args:
            ctx: Interception context with response information

        Returns:
            PostCallResult with decision and optional fixes
        """
        ...


# Type aliases for convenience
PreCallHookFn = Callable[[InterceptionContext], Awaitable[PreCallResult]]
PostCallHookFn = Callable[[InterceptionContext], Awaitable[PostCallResult]]


class InterceptionBlockedError(Exception):
    """Exception raised when a request is blocked by interception."""

    def __init__(
        self,
        reason: str,
        hook_name: str | None = None,
        context: InterceptionContext | None = None,
    ):
        self.reason = reason
        self.hook_name = hook_name
        self.context = context
        super().__init__(f"Request blocked by {hook_name or 'interception'}: {reason}")


class InterceptionRetryError(Exception):
    """Exception raised when a retry is requested by interception."""

    def __init__(
        self,
        reason: str,
        retry_kwargs: dict[str, Any] | None = None,
        hook_name: str | None = None,
    ):
        self.reason = reason
        self.retry_kwargs = retry_kwargs or {}
        self.hook_name = hook_name
        super().__init__(f"Retry requested by {hook_name or 'interception'}: {reason}")
