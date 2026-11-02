"""Custom exception hierarchy for the LLM provider abstraction."""

from __future__ import annotations

from typing import Any


class LLMError(Exception):
    """Base exception for all LLM provider errors."""


class RetryExhaustedError(LLMError):
    """Raised when all retry attempts are exhausted for a retryable provider failure."""

    def __init__(
        self,
        message: str = "Retry attempts exhausted after transient provider failures",
        *,
        attempts: int = 0,
        total_wait_seconds: float = 0.0,
        last_status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.attempts = attempts
        self.total_wait_seconds = total_wait_seconds
        self.last_status_code = last_status_code


class RateLimitExhaustedError(RetryExhaustedError):
    """Raised when all retry attempts are exhausted due to rate limiting (HTTP 429)."""

    def __init__(
        self,
        message: str = "Rate limit exhausted after all retry attempts",
        *,
        attempts: int = 0,
        total_wait_seconds: float = 0.0,
        last_status_code: int | None = None,
    ) -> None:
        super().__init__(
            message,
            attempts=attempts,
            total_wait_seconds=total_wait_seconds,
            last_status_code=last_status_code,
        )


class ContextWindowOverflowError(LLMError):
    """Raised when input exceeds the model's context window."""

    def __init__(
        self,
        message: str = "Input exceeds context window",
        *,
        token_count: int = 0,
        max_tokens: int = 0,
        model: str = "",
    ) -> None:
        super().__init__(message)
        self.token_count = token_count
        self.max_tokens = max_tokens
        self.model = model


class StructuredOutputValidationError(LLMError):
    """Raised when LLM response does not conform to the expected JSON schema."""

    def __init__(
        self,
        message: str = "Response does not conform to expected schema",
        *,
        schema: dict[str, Any] | None = None,
        response_text: str = "",
        validation_errors: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.schema = schema
        self.response_text = response_text
        self.validation_errors = validation_errors or []


class NoFixtureFoundError(LLMError):
    """Raised when no fixture matches the request in deterministic test mode."""

    def __init__(
        self,
        message: str = "No fixture found for request",
        *,
        fixture_key: str = "",
        fixture_dir: str = "",
    ) -> None:
        super().__init__(message)
        self.fixture_key = fixture_key
        self.fixture_dir = fixture_dir


class FixtureVersionMismatchError(LLMError):
    """Raised when a fixture's version doesn't match the expected version."""

    def __init__(
        self,
        message: str = "Fixture version mismatch",
        *,
        expected_version: int = 0,
        actual_version: int = 0,
        fixture_path: str = "",
    ) -> None:
        super().__init__(message)
        self.expected_version = expected_version
        self.actual_version = actual_version
        self.fixture_path = fixture_path


class StreamInterruptedError(LLMError):
    """Raised when a streaming response is interrupted mid-stream."""

    def __init__(
        self,
        message: str = "Stream interrupted",
        *,
        partial_response: str = "",
        chunks_received: int = 0,
    ) -> None:
        super().__init__(message)
        self.partial_response = partial_response
        self.chunks_received = chunks_received


class AuthenticationError(LLMError):
    """Raised when provider authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        *,
        provider_type: str = "",
        env_var: str = "",
    ) -> None:
        super().__init__(message)
        self.provider_type = provider_type
        self.env_var = env_var


class DuplicateNodeMappingError(LLMError):
    """Raised when multiple providers are mapped to the same (workflow, node_type)."""

    def __init__(
        self,
        message: str = "Duplicate node mapping",
        *,
        workflow: str = "",
        node_type: str = "",
    ) -> None:
        super().__init__(message)
        self.workflow = workflow
        self.node_type = node_type


class ProviderNotConfiguredError(LLMError):
    """Raised when no provider is configured for the requested node type or workflow."""

    def __init__(
        self,
        message: str = "No provider configured",
        *,
        node_type: str = "",
        workflow: str = "",
    ) -> None:
        super().__init__(message)
        self.node_type = node_type
        self.workflow = workflow


class ModelNotAvailableError(LLMError):
    """Raised when a provider cannot serve the requested model."""

    def __init__(
        self,
        message: str = "Requested model is not available",
        *,
        provider_type: str = "",
        model: str = "",
    ) -> None:
        super().__init__(message)
        self.provider_type = provider_type
        self.model = model
