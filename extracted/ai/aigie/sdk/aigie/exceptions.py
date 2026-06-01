"""
Aigie Exception Hierarchy

This module provides a comprehensive exception hierarchy for the Aigie SDK,
inspired by LiteLLM's approach of mapping all errors to a consistent set of types.

The hierarchy allows for:
- Specific error handling by type (e.g., catch only ContextDriftDetected)
- Generic error handling (e.g., catch all AigieError)
- Clear error messages with context for debugging
- Retry information included in error messages

Usage:
    from aigie.exceptions import (
        AigieError,
        ContextDriftDetected,
        RemediationFailed,
    )

    try:
        result = await agent.run()
    except ContextDriftDetected as e:
        print(f"Drift detected: {e.drift_score}")
        # Handle drift specifically
    except RemediationFailed as e:
        print(f"Auto-fix failed after {e.attempts} attempts")
    except AigieError as e:
        print(f"Aigie error: {e}")
"""

from datetime import datetime
from typing import Any


class AigieError(Exception):
    """
    Base exception for all Aigie errors.

    All Aigie-specific exceptions inherit from this class,
    allowing for catch-all error handling while preserving
    the ability to catch specific error types.

    Attributes:
        message: Human-readable error message
        trace_id: Associated trace ID (if available)
        span_id: Associated span ID (if available)
        model: LLM model involved (if applicable)
        provider: LLM provider involved (if applicable)
        metadata: Additional context about the error
    """

    def __init__(
        self,
        message: str,
        *,
        trace_id: str | None = None,
        span_id: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self.message = message
        self.trace_id = trace_id
        self.span_id = span_id
        self.model = model
        self.provider = provider
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()

        # Format message with context
        formatted = f"aigie.{self.__class__.__name__}: {message}"
        if trace_id:
            formatted += f" [trace_id={trace_id}]"
        if span_id:
            formatted += f" [span_id={span_id}]"

        super().__init__(formatted)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/reporting."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "model": self.model,
            "provider": self.provider,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


# ============================================================================
# Drift Detection Errors
# ============================================================================


class DriftError(AigieError):
    """Base class for drift-related errors."""

    pass


class ContextDriftDetected(DriftError):
    """
    Raised when context drift is detected during agent execution.

    Context drift occurs when the agent's behavior deviates from expected
    patterns, such as:
    - Topic drift (talking about unrelated subjects)
    - Behavior drift (acting inconsistently with previous interactions)
    - Quality drift (response quality degradation)
    - Coherence drift (losing track of conversation context)

    Attributes:
        drift_type: Type of drift detected ("topic", "behavior", "quality", "coherence")
        drift_score: Drift severity score (0.0 to 1.0)
        threshold: The threshold that was exceeded
        expected_context: What the context should have been
        actual_context: What the context actually was
    """

    def __init__(
        self,
        message: str,
        *,
        drift_type: str = "unknown",
        drift_score: float = 0.0,
        threshold: float = 0.7,
        expected_context: str | None = None,
        actual_context: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.drift_type = drift_type
        self.drift_score = drift_score
        self.threshold = threshold
        self.expected_context = expected_context
        self.actual_context = actual_context

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                "drift_type": self.drift_type,
                "drift_score": self.drift_score,
                "threshold": self.threshold,
            }
        )
        return d


class TopicDriftDetected(ContextDriftDetected):
    """Raised when topic drift is detected."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, drift_type="topic", **kwargs)


class BehaviorDriftDetected(ContextDriftDetected):
    """Raised when behavior drift is detected."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, drift_type="behavior", **kwargs)


class QualityDriftDetected(ContextDriftDetected):
    """Raised when quality drift is detected."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, drift_type="quality", **kwargs)


class LoopDetectedError(DriftError):
    """
    Raised when an agent loop is detected.

    This error indicates that the agent has entered a repetitive pattern,
    potentially stuck in an infinite loop. This is a key predictive prevention
    feature to detect problems BEFORE they impact users.

    Attributes:
        loop_count: Number of similar states detected
        similarity_score: How similar the repeated states are (0.0 to 1.0)
        similar_states: List of state hashes that were detected as similar
    """

    def __init__(
        self,
        message: str,
        *,
        loop_count: int = 0,
        similarity_score: float = 0.0,
        similar_states: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.loop_count = loop_count
        self.similarity_score = similarity_score
        self.similar_states = similar_states or []

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                "loop_count": self.loop_count,
                "similarity_score": self.similarity_score,
                "similar_states_count": len(self.similar_states),
            }
        )
        return d


# ============================================================================
# Remediation Errors
# ============================================================================


class RemediationError(AigieError):
    """Base class for remediation-related errors."""

    pass


class RemediationFailed(RemediationError):
    """
    Raised when automatic remediation fails.

    This error indicates that Aigie detected an issue and attempted
    to fix it, but the fix was unsuccessful.

    Attributes:
        attempts: Number of remediation attempts made
        max_attempts: Maximum attempts configured
        last_error: The last error encountered during remediation
        fixes_attempted: List of fix strategies that were tried
    """

    def __init__(
        self,
        message: str,
        *,
        attempts: int = 0,
        max_attempts: int = 3,
        last_error: str | None = None,
        fixes_attempted: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.attempts = attempts
        self.max_attempts = max_attempts
        self.last_error = last_error
        self.fixes_attempted = fixes_attempted or []

    def to_dict(self) -> dict[str, Any]:
        d = super().to_dict()
        d.update(
            {
                "attempts": self.attempts,
                "max_attempts": self.max_attempts,
                "last_error": self.last_error,
                "fixes_attempted": self.fixes_attempted,
            }
        )
        return d


class RemediationRejected(RemediationError):
    """
    Raised when a remediation is rejected by policy or user.

    This can happen when:
    - Auto-fix is disabled but would have fixed the issue
    - User rejected a recommended fix
    - Policy prevents automatic changes
    """

    def __init__(
        self,
        message: str,
        *,
        reason: str = "policy",
        recommended_fix: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.reason = reason
        self.recommended_fix = recommended_fix


class RetryExhausted(RemediationError):
    """
    Raised when all retry attempts are exhausted.

    Attributes:
        attempts: Number of retry attempts made
        errors: List of errors from each attempt
    """

    def __init__(
        self,
        message: str,
        *,
        attempts: int = 0,
        errors: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.attempts = attempts
        self.errors = errors or []


# ============================================================================
# Tracing Errors
# ============================================================================


class TracingError(AigieError):
    """Base class for tracing-related errors."""

    pass


class TraceBufferError(TracingError):
    """
    Raised when the event buffer encounters an error.

    This can happen when:
    - Buffer is full and cannot accept new events
    - Flush to backend fails
    - Serialization fails
    """

    def __init__(
        self,
        message: str,
        *,
        buffer_size: int = 0,
        pending_events: int = 0,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.buffer_size = buffer_size
        self.pending_events = pending_events


class TraceContextError(TracingError):
    """
    Raised when there's an issue with trace context.

    This can happen when:
    - No active trace context when one is expected
    - Trace context is corrupted
    - Parent span not found
    """

    pass


class SpanCreationError(TracingError):
    """Raised when span creation fails."""

    pass


class TraceSendError(TracingError):
    """
    Raised when sending trace data to backend fails.

    Attributes:
        status_code: HTTP status code if applicable
        retry_after: Suggested retry delay in seconds
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        retry_after: float | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.retry_after = retry_after


# ============================================================================
# Interception Errors
# ============================================================================


class InterceptionError(AigieError):
    """Base class for interception-related errors."""

    pass


class InterceptionBlocked(InterceptionError):
    """
    Raised when an LLM call is blocked by interception rules.

    This indicates that pre-call hooks or rules determined
    the request should not proceed.

    Attributes:
        rule_name: Name of the rule that blocked the request
        reason: Detailed reason for blocking
    """

    def __init__(
        self,
        message: str,
        *,
        rule_name: str | None = None,
        reason: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.rule_name = rule_name
        self.reason = reason


class InterceptionModified(InterceptionError):
    """
    Raised when an LLM call is modified by interception.

    This is informational - the call proceeded but was modified.

    Attributes:
        modifications: List of modifications made
    """

    def __init__(
        self,
        message: str,
        *,
        modifications: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.modifications = modifications or []


class InterceptionRetryRequested(InterceptionError):
    """
    Raised when post-call hooks request a retry.

    Attributes:
        retry_count: Current retry count
        max_retries: Maximum retries allowed
        reason: Reason for retry request
    """

    def __init__(
        self,
        message: str,
        *,
        retry_count: int = 0,
        max_retries: int = 3,
        reason: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.retry_count = retry_count
        self.max_retries = max_retries
        self.reason = reason


# ============================================================================
# Configuration Errors
# ============================================================================


class ConfigurationError(AigieError):
    """Base class for configuration-related errors."""

    pass


class InvalidConfigurationError(ConfigurationError):
    """
    Raised when configuration is invalid.

    Attributes:
        config_key: The configuration key that is invalid
        expected: Expected value or format
        actual: Actual value provided
    """

    def __init__(
        self,
        message: str,
        *,
        config_key: str | None = None,
        expected: str | None = None,
        actual: Any | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.config_key = config_key
        self.expected = expected
        self.actual = actual


class MissingConfigurationError(ConfigurationError):
    """
    Raised when required configuration is missing.

    Attributes:
        config_keys: List of missing configuration keys
    """

    def __init__(
        self,
        message: str,
        *,
        config_keys: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.config_keys = config_keys or []


# ============================================================================
# Integration Errors
# ============================================================================


class IntegrationError(AigieError):
    """Base class for integration-related errors."""

    pass


class IntegrationNotFoundError(IntegrationError):
    """
    Raised when an integration is not found.

    Attributes:
        integration_name: Name of the integration
        available_integrations: List of available integrations
    """

    def __init__(
        self,
        message: str,
        *,
        integration_name: str | None = None,
        available_integrations: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.integration_name = integration_name
        self.available_integrations = available_integrations or []


class IntegrationNotInstalledError(IntegrationError):
    """
    Raised when an integration's package is not installed.

    Attributes:
        integration_name: Name of the integration
        package_name: pip package that needs to be installed
    """

    def __init__(
        self,
        message: str,
        *,
        integration_name: str | None = None,
        package_name: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.integration_name = integration_name
        self.package_name = package_name


class IntegrationPatchError(IntegrationError):
    """Raised when patching an integration fails."""

    def __init__(
        self,
        message: str,
        *,
        integration_name: str | None = None,
        original_error: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.integration_name = integration_name
        self.original_error = original_error


# ============================================================================
# Backend/API Errors
# ============================================================================


class BackendError(AigieError):
    """Base class for backend communication errors."""

    pass


class BackendConnectionError(BackendError):
    """
    Raised when connection to Aigie backend fails.

    Attributes:
        api_url: The API URL that failed
        status_code: HTTP status code if applicable
    """

    def __init__(
        self,
        message: str,
        *,
        api_url: str | None = None,
        status_code: int | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.api_url = api_url
        self.status_code = status_code


class BackendTimeoutError(BackendError):
    """
    Raised when a backend request times out.

    Attributes:
        timeout_seconds: The timeout that was exceeded
    """

    def __init__(
        self,
        message: str,
        *,
        timeout_seconds: float = 30.0,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.timeout_seconds = timeout_seconds


class RateLimitError(BackendError):
    """
    Raised when rate limit is exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying
        limit: The rate limit that was hit
        remaining: Remaining requests (if known)
    """

    def __init__(
        self,
        message: str,
        *,
        retry_after: float | None = None,
        limit: int | None = None,
        remaining: int = 0,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining


class AuthenticationError(BackendError):
    """Raised when authentication fails."""

    pass


class AuthorizationError(BackendError):
    """Raised when authorization fails (valid auth but insufficient permissions)."""

    pass


# ============================================================================
# Evaluation Errors
# ============================================================================


class EvaluationError(AigieError):
    """Base class for evaluation-related errors."""

    pass


class JudgeError(EvaluationError):
    """
    Raised when the LLM judge encounters an error.

    Attributes:
        judge_model: The model used for judging
        evaluation_type: Type of evaluation being performed
    """

    def __init__(
        self,
        message: str,
        *,
        judge_model: str | None = None,
        evaluation_type: str | None = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.judge_model = judge_model
        self.evaluation_type = evaluation_type


class ScoreError(EvaluationError):
    """Raised when score submission fails."""

    pass


# ============================================================================
# Callback Errors
# ============================================================================


class CallbackError(AigieError):
    """Base class for callback-related errors."""

    pass


class WebhookError(CallbackError):
    """
    Raised when webhook delivery fails.

    Attributes:
        webhook_url: The webhook URL that failed
        status_code: HTTP status code returned
        attempts: Number of delivery attempts
    """

    def __init__(
        self,
        message: str,
        *,
        webhook_url: str | None = None,
        status_code: int | None = None,
        attempts: int = 1,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.webhook_url = webhook_url
        self.status_code = status_code
        self.attempts = attempts


class CallbackTimeoutError(CallbackError):
    """Raised when a callback times out."""

    pass


# ============================================================================
# Convenience exports
# ============================================================================

__all__ = [
    # Base
    "AigieError",
    # Drift
    "DriftError",
    "ContextDriftDetected",
    "TopicDriftDetected",
    "BehaviorDriftDetected",
    "QualityDriftDetected",
    "LoopDetectedError",
    # Remediation
    "RemediationError",
    "RemediationFailed",
    "RemediationRejected",
    "RetryExhausted",
    # Tracing
    "TracingError",
    "TraceBufferError",
    "TraceContextError",
    "SpanCreationError",
    "TraceSendError",
    # Interception
    "InterceptionError",
    "InterceptionBlocked",
    "InterceptionModified",
    "InterceptionRetryRequested",
    # Configuration
    "ConfigurationError",
    "InvalidConfigurationError",
    "MissingConfigurationError",
    # Integration
    "IntegrationError",
    "IntegrationNotFoundError",
    "IntegrationNotInstalledError",
    "IntegrationPatchError",
    # Backend
    "BackendError",
    "BackendConnectionError",
    "BackendTimeoutError",
    "RateLimitError",
    "AuthenticationError",
    "AuthorizationError",
    # Evaluation
    "EvaluationError",
    "JudgeError",
    "ScoreError",
    # Callbacks
    "CallbackError",
    "WebhookError",
    "CallbackTimeoutError",
]
