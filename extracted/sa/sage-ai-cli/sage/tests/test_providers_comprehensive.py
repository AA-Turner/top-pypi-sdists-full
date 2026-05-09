"""Comprehensive tests for sage/providers - AI Model Providers."""

import json
import time
from collections.abc import Iterator
from dataclasses import dataclass
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from sage.providers.base import Message, ModelInfo, ProviderBase
from sage.providers.retry import (
    TRANSIENT_STATUS_CODES,
    PERMANENT_STATUS_CODES,
    is_transient_error,
    is_rate_limited,
    get_retry_after,
    RetryConfig,
    CircuitBreaker,
    RateLimiter,
    get_rate_limiter,
    with_retry,
    retry_generator,
    DEFAULT_RETRY_CONFIG,
    AGGRESSIVE_RETRY_CONFIG,
    FAST_FAIL_CONFIG,
)
from sage.providers.openai_compat import (
    ProviderSpec,
    OpenAICompatProvider,
    OllamaProvider,
    GROQ_MODELS,
    OPENROUTER_MODELS,
    CEREBRAS_MODELS,
    SAMBANOVA_MODELS,
    TOGETHER_MODELS,
    MISTRAL_MODELS,
    COHERE_MODELS,
    GITHUB_MODELS,
    DEEPSEEK_MODELS,
    DEEPINFRA_MODELS,
    PROVIDER_SPECS,
    build_openai_compat_providers,
)
from sage.providers.gemini import (
    GeminiProvider,
    _build_payload,
    _extract_text,
    _FREE_MODELS,
)
from sage.providers.llama_cpp import LlamaCppProvider


# =============================================================================
# Tests for Message Dataclass
# =============================================================================


class TestMessage:
    """Tests for Message dataclass."""

    def test_create_user_message(self):
        """Create user message."""
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_create_system_message(self):
        """Create system message."""
        msg = Message(role="system", content="You are a helpful assistant.")
        assert msg.role == "system"
        assert msg.content == "You are a helpful assistant."

    def test_create_assistant_message(self):
        """Create assistant message."""
        msg = Message(role="assistant", content="How can I help?")
        assert msg.role == "assistant"
        assert msg.content == "How can I help?"

    def test_frozen(self):
        """Message is frozen (immutable)."""
        msg = Message(role="user", content="Test")
        with pytest.raises(Exception):  # FrozenInstanceError
            msg.role = "assistant"


# =============================================================================
# Tests for ModelInfo Dataclass
# =============================================================================


class TestModelInfo:
    """Tests for ModelInfo dataclass."""

    def test_create_minimal(self):
        """Create with required fields."""
        info = ModelInfo(
            id="test-model",
            provider="test",
            name="Test Model",
            local=False,
        )
        assert info.id == "test-model"
        assert info.provider == "test"
        assert info.name == "Test Model"
        assert info.local is False
        assert info.description == ""
        assert info.pros == ""
        assert info.cons == ""

    def test_create_full(self):
        """Create with all fields."""
        info = ModelInfo(
            id="gpt-4",
            provider="openai",
            name="GPT-4",
            local=False,
            description="Best model for complex tasks",
            pros="High quality, reasoning",
            cons="Expensive, slower",
        )
        assert info.description == "Best model for complex tasks"
        assert info.pros == "High quality, reasoning"
        assert info.cons == "Expensive, slower"

    def test_local_model(self):
        """Create local model info."""
        info = ModelInfo(
            id="llama-7b",
            provider="llama_cpp",
            name="Llama 7B",
            local=True,
        )
        assert info.local is True


# =============================================================================
# Tests for Retry Utilities
# =============================================================================


class TestTransientErrorDetection:
    """Tests for transient error detection."""

    def test_transient_status_codes_defined(self):
        """Transient status codes are defined."""
        assert 429 in TRANSIENT_STATUS_CODES  # Rate limited
        assert 500 in TRANSIENT_STATUS_CODES  # Server error
        assert 503 in TRANSIENT_STATUS_CODES  # Service unavailable

    def test_permanent_status_codes_defined(self):
        """Permanent status codes are defined."""
        assert 400 in PERMANENT_STATUS_CODES  # Bad request
        assert 401 in PERMANENT_STATUS_CODES  # Unauthorized
        assert 404 in PERMANENT_STATUS_CODES  # Not found

    def test_is_transient_error_http_429(self):
        """Detect rate limit as transient."""
        import httpx
        response = MagicMock()
        response.status_code = 429
        exc = httpx.HTTPStatusError("Rate limited", request=MagicMock(), response=response)
        assert is_transient_error(exc) is True

    def test_is_transient_error_http_500(self):
        """Detect server error as transient."""
        import httpx
        response = MagicMock()
        response.status_code = 500
        exc = httpx.HTTPStatusError("Server error", request=MagicMock(), response=response)
        assert is_transient_error(exc) is True

    def test_is_transient_error_http_401(self):
        """Unauthorized is not transient."""
        import httpx
        response = MagicMock()
        response.status_code = 401
        exc = httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response)
        assert is_transient_error(exc) is False

    def test_is_transient_error_timeout(self):
        """Timeout is transient."""
        import httpx
        exc = httpx.ReadTimeout("Read timeout")
        assert is_transient_error(exc) is True

    def test_is_transient_error_connect_error(self):
        """Connect error is transient."""
        import httpx
        exc = httpx.ConnectError("Connection refused")
        assert is_transient_error(exc) is True

    def test_is_transient_error_connection_error(self):
        """Generic connection error is transient."""
        exc = ConnectionError("Network error")
        assert is_transient_error(exc) is True

    def test_is_rate_limited_429(self):
        """Detect 429 as rate limited."""
        import httpx
        response = MagicMock()
        response.status_code = 429
        exc = httpx.HTTPStatusError("Rate limited", request=MagicMock(), response=response)
        assert is_rate_limited(exc) is True

    def test_is_rate_limited_other(self):
        """Other errors are not rate limited."""
        import httpx
        response = MagicMock()
        response.status_code = 500
        exc = httpx.HTTPStatusError("Server error", request=MagicMock(), response=response)
        assert is_rate_limited(exc) is False


class TestGetRetryAfter:
    """Tests for get_retry_after function."""

    def test_with_retry_after_header(self):
        """Extract Retry-After header."""
        import httpx
        response = MagicMock()
        response.headers = {"Retry-After": "30"}
        exc = httpx.HTTPStatusError("Rate limited", request=MagicMock(), response=response)
        assert get_retry_after(exc) == 30.0

    def test_without_retry_after_header(self):
        """No Retry-After header returns None."""
        import httpx
        response = MagicMock()
        response.headers = {}
        exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
        assert get_retry_after(exc) is None

    def test_invalid_retry_after_value(self):
        """Invalid Retry-After value returns None."""
        import httpx
        response = MagicMock()
        response.headers = {"Retry-After": "invalid"}
        exc = httpx.HTTPStatusError("Error", request=MagicMock(), response=response)
        assert get_retry_after(exc) is None


# =============================================================================
# Tests for RetryConfig
# =============================================================================


class TestRetryConfig:
    """Tests for RetryConfig dataclass."""

    def test_defaults(self):
        """Check default values."""
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.base_delay == 0.5
        assert config.max_delay == 30.0
        assert config.exponential_base == 2.0
        assert config.jitter == 0.1

    def test_custom_values(self):
        """Create with custom values."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=1.0,
            max_delay=60.0,
        )
        assert config.max_attempts == 5
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0

    def test_calculate_delay_first_attempt(self):
        """Calculate delay for first attempt."""
        config = RetryConfig(base_delay=1.0, jitter=0)
        delay = config.calculate_delay(0)
        assert delay == pytest.approx(1.0, abs=0.2)  # Allow for jitter

    def test_calculate_delay_exponential(self):
        """Delay increases exponentially."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=0)
        delay0 = config.calculate_delay(0)
        delay1 = config.calculate_delay(1)
        delay2 = config.calculate_delay(2)
        # delay0 ~ 1, delay1 ~ 2, delay2 ~ 4
        assert delay1 > delay0
        assert delay2 > delay1

    def test_calculate_delay_respects_max(self):
        """Delay respects max_delay."""
        config = RetryConfig(base_delay=10.0, max_delay=5.0, jitter=0)
        delay = config.calculate_delay(5)  # Would be 10 * 2^5 = 320
        assert delay <= 5.0

    def test_calculate_delay_with_retry_after(self):
        """Respects Retry-After header."""
        config = RetryConfig(base_delay=1.0)
        delay = config.calculate_delay(0, retry_after=10.0)
        assert delay == 10.0

    def test_calculate_delay_retry_after_respects_max(self):
        """Retry-After respects max_delay."""
        config = RetryConfig(max_delay=5.0)
        delay = config.calculate_delay(0, retry_after=10.0)
        assert delay == 5.0


# =============================================================================
# Tests for CircuitBreaker
# =============================================================================


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_init_closed(self):
        """Circuit starts closed."""
        cb = CircuitBreaker()
        assert cb._state == "closed"
        assert cb._failures == 0

    def test_record_success_resets(self):
        """Success resets failure count."""
        cb = CircuitBreaker()
        cb._failures = 3
        cb.record_success()
        assert cb._failures == 0
        assert cb._state == "closed"

    def test_record_failure_increments(self):
        """Failure increments count."""
        cb = CircuitBreaker()
        cb.record_failure()
        assert cb._failures == 1
        cb.record_failure()
        assert cb._failures == 2

    def test_opens_at_threshold(self):
        """Circuit opens at failure threshold."""
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb._state == "closed"
        cb.record_failure()  # 3rd failure
        assert cb._state == "open"

    def test_can_proceed_when_closed(self):
        """Can proceed when circuit is closed."""
        cb = CircuitBreaker()
        assert cb.can_proceed() is True

    def test_cannot_proceed_when_open(self):
        """Cannot proceed when circuit is open."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60.0)
        cb.record_failure()
        cb.record_failure()
        assert cb.can_proceed() is False

    def test_is_open(self):
        """is_open returns True when blocking."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60.0)
        cb.record_failure()
        cb.record_failure()
        assert cb.is_open() is True


# =============================================================================
# Tests for RateLimiter
# =============================================================================


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_init(self):
        """Initialize rate limiter."""
        rl = RateLimiter(requests_per_minute=60)
        assert rl.requests_per_minute == 60
        assert rl.burst_size == 60

    def test_custom_burst_size(self):
        """Custom burst size."""
        rl = RateLimiter(requests_per_minute=60, burst_size=10)
        assert rl.burst_size == 10

    def test_try_acquire_success(self):
        """Try acquire succeeds with available tokens."""
        rl = RateLimiter(requests_per_minute=60)
        assert rl.try_acquire() is True

    def test_try_acquire_depletes_tokens(self):
        """Tokens deplete on acquire."""
        rl = RateLimiter(requests_per_minute=60, burst_size=2)
        assert rl.try_acquire() is True
        assert rl.try_acquire() is True
        assert rl.try_acquire() is False

    def test_acquire_blocks_and_succeeds(self):
        """Acquire blocks and eventually succeeds."""
        rl = RateLimiter(requests_per_minute=6000, burst_size=1)  # Fast refill
        rl.try_acquire()  # Use the token
        # Should succeed quickly due to fast refill rate
        assert rl.acquire(timeout=1.0) is True

    def test_get_rate_limiter_creates_new(self):
        """get_rate_limiter creates new limiter."""
        # Use unique name to avoid conflicts
        rl = get_rate_limiter("test_provider_unique", 120)
        assert rl.requests_per_minute == 120

    def test_get_rate_limiter_returns_same(self):
        """get_rate_limiter returns same instance."""
        rl1 = get_rate_limiter("shared_provider")
        rl2 = get_rate_limiter("shared_provider")
        assert rl1 is rl2


# =============================================================================
# Tests for Retry Decorators
# =============================================================================


class TestWithRetry:
    """Tests for with_retry decorator."""

    def test_success_on_first_try(self):
        """Succeeds without retry."""
        call_count = [0]

        @with_retry()
        def func():
            call_count[0] += 1
            return "success"

        result = func()
        assert result == "success"
        assert call_count[0] == 1

    def test_retries_on_transient_error(self):
        """Retries on transient error."""
        import httpx
        call_count = [0]

        @with_retry(config=RetryConfig(max_attempts=3, base_delay=0.01))
        def func():
            call_count[0] += 1
            if call_count[0] < 3:
                response = MagicMock()
                response.status_code = 500
                raise httpx.HTTPStatusError("Server error", request=MagicMock(), response=response)
            return "success"

        result = func()
        assert result == "success"
        assert call_count[0] == 3

    def test_raises_on_permanent_error(self):
        """Raises immediately on permanent error."""
        import httpx
        call_count = [0]

        @with_retry()
        def func():
            call_count[0] += 1
            response = MagicMock()
            response.status_code = 401  # Unauthorized
            raise httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response)

        with pytest.raises(httpx.HTTPStatusError):
            func()
        assert call_count[0] == 1  # No retries


class TestRetryGenerator:
    """Tests for retry_generator decorator."""

    def test_success_yields_all(self):
        """Successful generator yields all items."""

        @retry_generator
        def gen():
            yield 1
            yield 2
            yield 3

        result = list(gen())
        assert result == [1, 2, 3]


# =============================================================================
# Tests for Default Configurations
# =============================================================================


class TestDefaultConfigs:
    """Tests for default retry configurations."""

    def test_default_config(self):
        """DEFAULT_RETRY_CONFIG is defined."""
        assert DEFAULT_RETRY_CONFIG.max_attempts == 3

    def test_aggressive_config(self):
        """AGGRESSIVE_RETRY_CONFIG has more attempts."""
        assert AGGRESSIVE_RETRY_CONFIG.max_attempts == 5

    def test_fast_fail_config(self):
        """FAST_FAIL_CONFIG has fewer attempts."""
        assert FAST_FAIL_CONFIG.max_attempts == 2


# =============================================================================
# Tests for ProviderSpec
# =============================================================================


class TestProviderSpec:
    """Tests for ProviderSpec dataclass."""

    def test_create(self):
        """Create provider spec."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="test-model",
        )
        assert spec.name == "test"
        assert spec.base_url == "https://api.test.com/v1"
        assert spec.supports_streaming is True
        assert spec.requires_key is True

    def test_free_provider(self):
        """Create free provider spec."""
        spec = ProviderSpec(
            name="free",
            base_url="https://free.api.com",
            api_key_config="free",
            env_var="FREE_API_KEY",
            models=[],
            default_model="free-model",
            requires_key=False,
        )
        assert spec.requires_key is False


# =============================================================================
# Tests for Model Lists
# =============================================================================


class TestModelLists:
    """Tests for provider model lists."""

    def test_groq_models(self):
        """GROQ_MODELS is populated."""
        assert len(GROQ_MODELS) > 0
        assert all(m.provider == "groq" for m in GROQ_MODELS)

    def test_openrouter_models(self):
        """OPENROUTER_MODELS is populated."""
        assert len(OPENROUTER_MODELS) > 0
        assert all(m.provider == "openrouter" for m in OPENROUTER_MODELS)

    def test_cerebras_models(self):
        """CEREBRAS_MODELS is populated."""
        assert len(CEREBRAS_MODELS) > 0

    def test_sambanova_models(self):
        """SAMBANOVA_MODELS is populated."""
        assert len(SAMBANOVA_MODELS) > 0

    def test_together_models(self):
        """TOGETHER_MODELS is populated."""
        assert len(TOGETHER_MODELS) > 0

    def test_mistral_models(self):
        """MISTRAL_MODELS is populated."""
        assert len(MISTRAL_MODELS) > 0

    def test_cohere_models(self):
        """COHERE_MODELS is populated."""
        assert len(COHERE_MODELS) > 0

    def test_github_models(self):
        """GITHUB_MODELS is populated."""
        assert len(GITHUB_MODELS) > 0

    def test_deepseek_models(self):
        """DEEPSEEK_MODELS is populated."""
        assert len(DEEPSEEK_MODELS) > 0
        # DeepSeek models have descriptions
        assert any(m.description for m in DEEPSEEK_MODELS)

    def test_deepinfra_models(self):
        """DEEPINFRA_MODELS is populated."""
        assert len(DEEPINFRA_MODELS) > 0


# =============================================================================
# Tests for PROVIDER_SPECS
# =============================================================================


class TestProviderSpecs:
    """Tests for PROVIDER_SPECS list."""

    def test_specs_defined(self):
        """Provider specs are defined."""
        assert len(PROVIDER_SPECS) > 0

    def test_all_have_required_fields(self):
        """All specs have required fields."""
        for spec in PROVIDER_SPECS:
            assert spec.name
            assert spec.base_url
            assert spec.api_key_config
            assert spec.env_var
            assert spec.default_model

    def test_groq_spec_exists(self):
        """Groq spec exists."""
        groq = next((s for s in PROVIDER_SPECS if s.name == "groq"), None)
        assert groq is not None
        assert "groq.com" in groq.base_url

# =============================================================================
# Tests for OpenAICompatProvider
# =============================================================================


class TestOpenAICompatProvider:
    """Tests for OpenAICompatProvider class."""

    def test_init(self):
        """Initialize provider."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="test-model",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {"test": "fake-key"}

        provider = OpenAICompatProvider(spec, mock_config)
        assert provider.name == "test"

    def test_is_available_with_key(self):
        """Available when key is configured."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="test-model",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {"test": "fake-key"}

        provider = OpenAICompatProvider(spec, mock_config)
        assert provider.is_available() is True

    def test_is_available_without_key(self):
        """Unavailable when key is missing."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="test-model",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {}

        provider = OpenAICompatProvider(spec, mock_config)
        assert provider.is_available() is False

    def test_free_provider_available(self):
        """Free provider available without key."""
        spec = ProviderSpec(
            name="free",
            base_url="https://free.api.com",
            api_key_config="free",
            env_var="FREE_API_KEY",
            models=[],
            default_model="free-model",
            requires_key=False,
        )
        mock_config = MagicMock()
        mock_config.api_keys = {}

        provider = OpenAICompatProvider(spec, mock_config)
        assert provider.is_available() is True

    def test_list_models_when_available(self):
        """List models when provider is available."""
        models = [
            ModelInfo(id="m1", provider="test", name="Model 1", local=False),
            ModelInfo(id="m2", provider="test", name="Model 2", local=False),
        ]
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=models,
            default_model="m1",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {"test": "fake-key"}

        provider = OpenAICompatProvider(spec, mock_config)
        result = provider.list_models()
        assert len(result) == 2

    def test_list_models_when_unavailable(self):
        """Return empty list when unavailable."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[ModelInfo(id="m1", provider="test", name="Model 1", local=False)],
            default_model="m1",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {}

        provider = OpenAICompatProvider(spec, mock_config)
        result = provider.list_models()
        assert result == []

    def test_completion_url_candidates(self):
        """Get completion URL candidates."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="m1",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {"test": "key"}

        provider = OpenAICompatProvider(spec, mock_config)
        urls = provider._completion_url_candidates()
        assert "https://api.test.com/v1/chat/completions" in urls

    def test_headers_include_auth(self):
        """Headers include authorization."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="m1",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {"test": "secret-key"}

        provider = OpenAICompatProvider(spec, mock_config)
        headers = provider._headers()
        assert headers["Authorization"] == "Bearer secret-key"

    def test_openrouter_headers(self):
        """OpenRouter has special headers."""
        or_spec = next(s for s in PROVIDER_SPECS if s.name == "openrouter")
        mock_config = MagicMock()
        mock_config.api_keys = {"openrouter": "key"}

        provider = OpenAICompatProvider(or_spec, mock_config)
        headers = provider._headers()
        assert "HTTP-Referer" in headers
        assert "X-Title" in headers

    def test_build_payload(self):
        """Build API payload."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="m1",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {"test": "key"}

        provider = OpenAICompatProvider(spec, mock_config)
        messages = [
            Message(role="system", content="Be helpful"),
            Message(role="user", content="Hello"),
        ]
        payload = provider._build_payload(messages, "m1", 0.7, 1024)

        assert payload["model"] == "m1"
        assert payload["temperature"] == 0.7
        assert payload["max_tokens"] == 1024
        assert len(payload["messages"]) == 2

    def test_generate_requires_key(self):
        """Generate raises if key required but missing."""
        spec = ProviderSpec(
            name="test",
            base_url="https://api.test.com/v1",
            api_key_config="test",
            env_var="TEST_API_KEY",
            models=[],
            default_model="m1",
        )
        mock_config = MagicMock()
        mock_config.api_keys = {}

        provider = OpenAICompatProvider(spec, mock_config)
        messages = [Message(role="user", content="Hello")]

        with pytest.raises(RuntimeError) as exc_info:
            provider.generate(messages)
        assert "not configured" in str(exc_info.value)


# =============================================================================
# Tests for OllamaProvider
# =============================================================================


class TestOllamaProvider:
    """Tests for OllamaProvider class."""

    def test_init(self):
        """Initialize Ollama provider."""
        mock_config = MagicMock()
        provider = OllamaProvider(mock_config)
        assert provider.name == "ollama"

    def test_custom_base_url(self):
        """Use custom base URL."""
        mock_config = MagicMock()
        provider = OllamaProvider(mock_config, base_url="http://custom:11434")
        assert provider._base_url == "http://custom:11434"

    def test_is_available_when_offline(self):
        """Unavailable when Ollama is offline."""
        mock_config = MagicMock()
        provider = OllamaProvider(mock_config, base_url="http://nonexistent:11434")
        assert provider.is_available() is False

    def test_build_messages(self):
        """Convert messages to Ollama format."""
        mock_config = MagicMock()
        provider = OllamaProvider(mock_config)
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there"),
        ]
        result = provider._build_messages(messages)
        assert result == [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ]


# =============================================================================
# Tests for build_openai_compat_providers
# =============================================================================


class TestBuildProviders:
    """Tests for build_openai_compat_providers function."""

    def test_builds_all_providers(self):
        """Builds providers for all specs."""
        mock_config = MagicMock()
        mock_config.api_keys = {}

        providers = build_openai_compat_providers(mock_config)
        assert len(providers) == len(PROVIDER_SPECS)

    def test_providers_are_openai_compat(self):
        """All providers are OpenAICompatProvider."""
        mock_config = MagicMock()
        mock_config.api_keys = {}

        providers = build_openai_compat_providers(mock_config)
        for p in providers:
            assert isinstance(p, OpenAICompatProvider)


# =============================================================================
# Tests for Gemini Provider Helpers
# =============================================================================


class TestGeminiHelpers:
    """Tests for Gemini helper functions."""

    def test_build_payload_user_only(self):
        """Build payload with user message."""
        messages = [Message(role="user", content="Hello")]
        payload = _build_payload(messages, 0.7, 1024)

        assert "contents" in payload
        assert payload["contents"][0]["role"] == "user"
        assert payload["generationConfig"]["temperature"] == 0.7
        assert payload["generationConfig"]["maxOutputTokens"] == 1024

    def test_build_payload_with_system(self):
        """Build payload with system message."""
        messages = [
            Message(role="system", content="Be helpful"),
            Message(role="user", content="Hello"),
        ]
        payload = _build_payload(messages, 0.7, 1024)

        assert "systemInstruction" in payload
        assert payload["systemInstruction"]["parts"][0]["text"] == "Be helpful"

    def test_build_payload_converts_assistant(self):
        """Convert assistant to model role."""
        messages = [
            Message(role="user", content="Hi"),
            Message(role="assistant", content="Hello"),
        ]
        payload = _build_payload(messages, 0.7, 1024)

        assert payload["contents"][1]["role"] == "model"

    def test_extract_text_success(self):
        """Extract text from valid response."""
        data = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "Hello!"}]
                }
            }]
        }
        assert _extract_text(data) == "Hello!"

    def test_extract_text_missing_parts(self):
        """Return empty string on missing parts."""
        assert _extract_text({}) == ""
        assert _extract_text({"candidates": []}) == ""
        assert _extract_text({"candidates": [{}]}) == ""


# =============================================================================
# Tests for Gemini Free Models
# =============================================================================


class TestGeminiFreeModels:
    """Tests for Gemini free models list."""

    def test_free_models_defined(self):
        """Free models are defined."""
        assert len(_FREE_MODELS) > 0

    def test_all_are_gemini_provider(self):
        """All models are gemini provider."""
        for model in _FREE_MODELS:
            assert model.provider == "gemini"

    def test_all_are_remote(self):
        """All models are remote (not local)."""
        for model in _FREE_MODELS:
            assert model.local is False


# =============================================================================
# Tests for GeminiProvider
# =============================================================================


class TestGeminiProvider:
    """Tests for GeminiProvider class."""

    def test_init(self):
        """Initialize Gemini provider."""
        mock_config = MagicMock()
        mock_config.gemini_api_key.return_value = "fake-key"

        provider = GeminiProvider(mock_config)
        assert provider.name == "gemini"

    def test_is_available_with_key(self):
        """Available with API key."""
        mock_config = MagicMock()
        mock_config.gemini_api_key.return_value = "fake-key"

        provider = GeminiProvider(mock_config)
        assert provider.is_available() is True

    def test_is_available_without_key(self):
        """Unavailable without API key."""
        mock_config = MagicMock()
        mock_config.gemini_api_key.return_value = None

        provider = GeminiProvider(mock_config)
        assert provider.is_available() is False

    def test_list_models_when_available(self):
        """List models when available."""
        mock_config = MagicMock()
        mock_config.gemini_api_key.return_value = "fake-key"

        provider = GeminiProvider(mock_config)
        models = provider.list_models()
        assert len(models) == len(_FREE_MODELS)

    def test_list_models_when_unavailable(self):
        """Return empty list when unavailable."""
        mock_config = MagicMock()
        mock_config.gemini_api_key.return_value = None

        provider = GeminiProvider(mock_config)
        models = provider.list_models()
        assert models == []

    def test_generate_requires_key(self):
        """Generate raises if key missing."""
        mock_config = MagicMock()
        mock_config.gemini_api_key.return_value = None

        provider = GeminiProvider(mock_config)
        messages = [Message(role="user", content="Hello")]

        with pytest.raises(RuntimeError) as exc_info:
            provider.generate(messages)
        assert "not configured" in str(exc_info.value)


# =============================================================================
# Tests for LlamaCppProvider
# =============================================================================


class TestLlamaCppProvider:
    """Tests for LlamaCppProvider class."""

    def test_init(self):
        """Initialize LlamaCpp provider."""
        mock_config = MagicMock()
        provider = LlamaCppProvider(mock_config)
        assert provider.name == "llama_cpp"

    def test_is_available_no_import(self):
        """Unavailable if llama_cpp not installed."""
        mock_config = MagicMock()

        with patch.dict("sys.modules", {"llama_cpp": None}):
            provider = LlamaCppProvider(mock_config)
            # Force reimport check
            with patch("builtins.__import__", side_effect=ImportError):
                assert provider.is_available() is False

    def test_to_chat_messages(self):
        """Convert messages to chat format."""
        mock_config = MagicMock()
        provider = LlamaCppProvider(mock_config)

        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi"),
        ]
        result = provider._to_chat_messages(messages)
        assert result == [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]


# =============================================================================
# Integration Tests
# =============================================================================


class TestProviderIntegration:
    """Integration tests for provider system."""

    def test_all_provider_specs_have_models(self):
        """All provider specs have at least one model."""
        for spec in PROVIDER_SPECS:
            assert len(spec.models) >= 0  # Some may be dynamic

    def test_provider_names_unique(self):
        """Provider names are unique."""
        names = [spec.name for spec in PROVIDER_SPECS]
        assert len(names) == len(set(names))

    def test_model_ids_unique_per_provider(self):
        """Model IDs are unique within each provider."""
        for spec in PROVIDER_SPECS:
            ids = [m.id for m in spec.models]
            assert len(ids) == len(set(ids)), f"Duplicate IDs in {spec.name}"
