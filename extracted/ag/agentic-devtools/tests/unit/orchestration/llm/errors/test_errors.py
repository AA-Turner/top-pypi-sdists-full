"""Tests for custom exception classes."""

from agentic_devtools.orchestration.llm.errors import (
    AuthenticationError,
    ContextWindowOverflowError,
    DuplicateNodeMappingError,
    FixtureVersionMismatchError,
    LLMError,
    NoFixtureFoundError,
    ProviderNotConfiguredError,
    RateLimitExhaustedError,
    RetryExhaustedError,
    StreamInterruptedError,
    StructuredOutputValidationError,
)


class TestRetryExhaustedError:
    """Tests for RetryExhaustedError."""

    def test_default_message(self):
        err = RetryExhaustedError()
        assert "Retry attempts exhausted" in str(err)
        assert err.attempts == 0
        assert err.total_wait_seconds == 0.0
        assert err.last_status_code is None

    def test_custom_attributes(self):
        err = RetryExhaustedError("Custom msg", attempts=5, total_wait_seconds=30.0, last_status_code=503)
        assert err.attempts == 5
        assert err.total_wait_seconds == 30.0
        assert err.last_status_code == 503

    def test_is_llm_error(self):
        assert issubclass(RetryExhaustedError, LLMError)


class TestRateLimitExhaustedError:
    """Tests for RateLimitExhaustedError."""

    def test_default_message(self):
        err = RateLimitExhaustedError()
        assert "Rate limit exhausted" in str(err)
        assert err.attempts == 0
        assert err.total_wait_seconds == 0.0
        assert err.last_status_code is None

    def test_custom_attributes(self):
        err = RateLimitExhaustedError("Custom msg", attempts=5, total_wait_seconds=30.0, last_status_code=429)
        assert err.attempts == 5
        assert err.total_wait_seconds == 30.0
        assert err.last_status_code == 429

    def test_is_llm_error(self):
        assert issubclass(RateLimitExhaustedError, LLMError)

    def test_is_retry_exhausted_error(self):
        assert issubclass(RateLimitExhaustedError, RetryExhaustedError)


class TestContextWindowOverflowError:
    """Tests for ContextWindowOverflowError."""

    def test_attributes(self):
        err = ContextWindowOverflowError("Overflow", token_count=200000, max_tokens=128000, model="gpt-4o")
        assert err.token_count == 200000
        assert err.max_tokens == 128000
        assert err.model == "gpt-4o"


class TestStructuredOutputValidationError:
    """Tests for StructuredOutputValidationError."""

    def test_attributes(self):
        err = StructuredOutputValidationError(
            "Invalid",
            schema={"type": "object"},
            response_text='{"bad": true}',
            validation_errors=["Missing field 'name'"],
        )
        assert err.schema == {"type": "object"}
        assert err.response_text == '{"bad": true}'
        assert len(err.validation_errors) == 1


class TestNoFixtureFoundError:
    """Tests for NoFixtureFoundError."""

    def test_attributes(self):
        err = NoFixtureFoundError("Not found", fixture_key="abc123", fixture_dir="/fixtures")
        assert err.fixture_key == "abc123"
        assert err.fixture_dir == "/fixtures"


class TestFixtureVersionMismatchError:
    """Tests for FixtureVersionMismatchError."""

    def test_attributes(self):
        err = FixtureVersionMismatchError("Mismatch", expected_version=1, actual_version=2, fixture_path="/f/x.json")
        assert err.expected_version == 1
        assert err.actual_version == 2
        assert err.fixture_path == "/f/x.json"


class TestStreamInterruptedError:
    """Tests for StreamInterruptedError."""

    def test_attributes(self):
        err = StreamInterruptedError("Interrupted", partial_response="partial", chunks_received=5)
        assert err.partial_response == "partial"
        assert err.chunks_received == 5


class TestAuthenticationError:
    """Tests for AuthenticationError."""

    def test_attributes(self):
        err = AuthenticationError("Auth failed", provider_type="azure_openai", env_var="AZURE_KEY")
        assert err.provider_type == "azure_openai"
        assert err.env_var == "AZURE_KEY"


class TestDuplicateNodeMappingError:
    """Tests for DuplicateNodeMappingError."""

    def test_attributes(self):
        err = DuplicateNodeMappingError("Duplicate", workflow="pr_review", node_type="analysis")
        assert err.workflow == "pr_review"
        assert err.node_type == "analysis"


class TestProviderNotConfiguredError:
    """Tests for ProviderNotConfiguredError."""

    def test_attributes(self):
        err = ProviderNotConfiguredError("No provider", node_type="analysis", workflow="pr_review")
        assert err.node_type == "analysis"
        assert err.workflow == "pr_review"

    def test_default_message(self):
        err = ProviderNotConfiguredError()
        assert "No provider configured" in str(err)
        assert err.node_type == ""
        assert err.workflow == ""

    def test_is_llm_error(self):
        assert issubclass(ProviderNotConfiguredError, LLMError)
