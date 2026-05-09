"""Comprehensive tests for sage/core/router.py - Provider router."""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from collections.abc import Iterator

from sage.core.router import ProviderRouter
from sage.providers.base import Message, ModelInfo, ProviderBase


# =============================================================================
# Mock Provider Helper
# =============================================================================


class MockProvider(ProviderBase):
    """Mock provider for testing."""

    def __init__(
        self,
        name: str,
        available: bool = True,
        models: list[ModelInfo] | None = None,
        generate_response: str = "Generated response",
        stream_response: list[str] | None = None,
        raise_on_generate: Exception | None = None,
        raise_on_stream: Exception | None = None,
    ):
        self._name = name
        self._available = available
        self._models = models if models is not None else [ModelInfo(id=f"{name}-model", provider=name, name=f"{name} Model", local=False)]
        self._generate_response = generate_response
        self._stream_response = stream_response or ["Streamed ", "response"]
        self._raise_on_generate = raise_on_generate
        self._raise_on_stream = raise_on_stream

    @property
    def name(self) -> str:
        return self._name

    def is_available(self) -> bool:
        return self._available

    def list_models(self) -> list[ModelInfo]:
        return self._models

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if self._raise_on_generate:
            raise self._raise_on_generate
        return self._generate_response

    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        if self._raise_on_stream:
            raise self._raise_on_stream
        yield from self._stream_response


# =============================================================================
# Tests for ProviderRouter initialization
# =============================================================================


class TestProviderRouterInit:
    """Tests for ProviderRouter initialization."""

    def test_empty_providers(self):
        """Initialize with empty providers."""
        router = ProviderRouter(providers=[])
        assert router._providers == {}
        assert router._fallback_order == []

    def test_single_provider(self):
        """Initialize with single provider."""
        provider = MockProvider("test")
        router = ProviderRouter(providers=[provider])

        assert "test" in router._providers
        assert router._fallback_order == ["test"]

    def test_multiple_providers(self):
        """Initialize with multiple providers."""
        providers = [
            MockProvider("gemini"),
            MockProvider("openai"),
            MockProvider("local"),
        ]
        router = ProviderRouter(providers=providers)

        assert len(router._providers) == 3
        assert router._fallback_order == ["gemini", "openai", "local"]

    def test_default_model(self):
        """Initialize with default model."""
        router = ProviderRouter(
            providers=[MockProvider("test")],
            default_model="gemini:gemini-2.0-flash",
        )
        assert router._default_model == "gemini:gemini-2.0-flash"


# =============================================================================
# Tests for resolve method
# =============================================================================


class TestResolve:
    """Tests for resolve method."""

    def test_resolve_with_prefix(self):
        """Resolve model with provider prefix."""
        provider = MockProvider("gemini")
        router = ProviderRouter(providers=[provider])

        result_provider, model_name = router.resolve("gemini:gemini-2.0-flash")

        assert result_provider is provider
        assert model_name == "gemini-2.0-flash"

    def test_resolve_without_prefix_known_model(self):
        """Resolve model without prefix when model is known."""
        provider = MockProvider(
            "gemini",
            models=[ModelInfo(id="gemini-2.0-flash", provider="gemini", name="Flash", local=False)],
        )
        router = ProviderRouter(providers=[provider])

        result_provider, model_name = router.resolve("gemini-2.0-flash")

        assert result_provider is provider
        assert model_name == "gemini-2.0-flash"

    def test_resolve_uses_default_model(self):
        """Resolve uses default model when empty string."""
        provider = MockProvider("gemini")
        router = ProviderRouter(
            providers=[provider],
            default_model="gemini:flash",
        )

        result_provider, model_name = router.resolve("")

        assert result_provider is provider
        assert model_name == "flash"

    def test_resolve_fallback_to_first_available(self):
        """Resolve falls back to first available provider."""
        provider = MockProvider(
            "gemini",
            models=[ModelInfo(id="default-model", provider="gemini", name="Default", local=False)],
        )
        router = ProviderRouter(providers=[provider])

        result_provider, model_name = router.resolve("unknown-model")

        assert result_provider is provider
        assert model_name == "default-model"

    def test_resolve_unavailable_provider(self):
        """Resolve raises for unavailable provider."""
        provider = MockProvider("gemini", available=False)
        router = ProviderRouter(providers=[provider])

        with pytest.raises(RuntimeError) as exc_info:
            router.resolve("gemini:model")

        assert "not available" in str(exc_info.value)

    def test_resolve_unregistered_provider(self):
        """Resolve raises for unregistered provider."""
        router = ProviderRouter(providers=[])

        with pytest.raises(RuntimeError) as exc_info:
            router.resolve("unknown:model")

        assert "not registered" in str(exc_info.value)

    def test_resolve_no_providers_available(self):
        """Resolve raises when no providers available."""
        provider = MockProvider("gemini", available=False)
        router = ProviderRouter(providers=[provider])

        with pytest.raises(RuntimeError) as exc_info:
            router.resolve("some-model")

        assert "No providers available" in str(exc_info.value)

    def test_resolve_skips_unavailable_providers(self):
        """Resolve skips unavailable providers during lookup."""
        unavailable = MockProvider("gemini", available=False)
        available = MockProvider(
            "openai",
            models=[ModelInfo(id="gpt-4", provider="openai", name="GPT-4", local=False)],
        )
        router = ProviderRouter(providers=[unavailable, available])

        result_provider, model_name = router.resolve("gpt-4")

        assert result_provider is available


# =============================================================================
# Tests for generate method
# =============================================================================


class TestGenerate:
    """Tests for generate method."""

    def test_generate_success(self):
        """Generate returns response on success."""
        provider = MockProvider("gemini", generate_response="Hello!")
        router = ProviderRouter(providers=[provider])
        messages = [Message(role="user", content="Hi")]

        result = router.generate(messages, "gemini:model")

        assert result == "Hello!"

    def test_generate_with_parameters(self):
        """Generate passes parameters correctly."""
        mock_provider = MagicMock(spec=ProviderBase)
        mock_provider.name = "test"
        mock_provider.is_available.return_value = True
        mock_provider.list_models.return_value = [
            ModelInfo(id="model", provider="test", name="Model", local=False)
        ]
        mock_provider.generate.return_value = "Response"

        router = ProviderRouter(providers=[mock_provider])
        messages = [Message(role="user", content="Hi")]

        router.generate(messages, "test:model", temperature=0.5, max_tokens=1000)

        mock_provider.generate.assert_called_once_with(
            messages, "model", 0.5, 1000
        )

    def test_generate_fallback_on_error(self):
        """Generate falls back to another provider on error."""
        failing = MockProvider(
            "primary",
            raise_on_generate=Exception("API Error"),
        )
        backup = MockProvider("backup", generate_response="Backup response")
        router = ProviderRouter(providers=[failing, backup])
        messages = [Message(role="user", content="Hi")]

        result = router.generate(messages, "primary:model")

        assert result == "Backup response"

    def test_generate_all_providers_fail(self):
        """Generate raises when all providers fail."""
        failing1 = MockProvider(
            "provider1",
            raise_on_generate=Exception("Error 1"),
        )
        failing2 = MockProvider(
            "provider2",
            raise_on_generate=Exception("Error 2"),
        )
        router = ProviderRouter(providers=[failing1, failing2])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(RuntimeError) as exc_info:
            router.generate(messages, "provider1:model")

        assert "All providers failed" in str(exc_info.value)

    def test_generate_keyboard_interrupt(self):
        """Generate doesn't swallow KeyboardInterrupt."""
        provider = MockProvider(
            "gemini",
            raise_on_generate=KeyboardInterrupt(),
        )
        router = ProviderRouter(providers=[provider])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(KeyboardInterrupt):
            router.generate(messages, "gemini:model")

    def test_generate_skips_unavailable_fallback(self):
        """Generate skips unavailable providers during fallback."""
        failing = MockProvider(
            "primary",
            raise_on_generate=Exception("Error"),
        )
        unavailable = MockProvider("unavailable", available=False)
        backup = MockProvider("backup", generate_response="Success")
        router = ProviderRouter(providers=[failing, unavailable, backup])
        messages = [Message(role="user", content="Hi")]

        result = router.generate(messages, "primary:model")

        assert result == "Success"

    def test_generate_skips_empty_model_list(self):
        """Generate skips providers with no models."""
        failing = MockProvider(
            "primary",
            raise_on_generate=Exception("Error"),
        )
        no_models = MockProvider("empty", models=[])
        backup = MockProvider("backup", generate_response="Success")
        router = ProviderRouter(providers=[failing, no_models, backup])
        messages = [Message(role="user", content="Hi")]

        result = router.generate(messages, "primary:model")

        assert result == "Success"

    def test_generate_explicit_provider_does_not_cross_fallback(self):
        """If the user explicitly requested a provider, router should not jump to another one."""
        failing = MockProvider(
            "primary",
            raise_on_generate=Exception("API Error"),
        )
        backup = MockProvider("backup", generate_response="Backup response")
        router = ProviderRouter(providers=[failing, backup])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(RuntimeError) as exc_info:
            router.generate(messages, "primary:model", lock_provider=True)

        assert "requested model" in str(exc_info.value).lower()
        assert "primary:model" in str(exc_info.value)


# =============================================================================
# Tests for stream method
# =============================================================================


class TestStream:
    """Tests for stream method."""

    def test_stream_success(self):
        """Stream yields tokens on success."""
        provider = MockProvider(
            "gemini",
            stream_response=["Hello", " ", "World"],
        )
        router = ProviderRouter(providers=[provider])
        messages = [Message(role="user", content="Hi")]

        result = list(router.stream(messages, "gemini:model"))

        assert result == ["Hello", " ", "World"]

    def test_stream_with_parameters(self):
        """Stream passes parameters correctly."""
        mock_provider = MagicMock(spec=ProviderBase)
        mock_provider.name = "test"
        mock_provider.is_available.return_value = True
        mock_provider.list_models.return_value = [
            ModelInfo(id="model", provider="test", name="Model", local=False)
        ]
        mock_provider.stream.return_value = iter(["Response"])

        router = ProviderRouter(providers=[mock_provider])
        messages = [Message(role="user", content="Hi")]

        list(router.stream(messages, "test:model", temperature=0.5, max_tokens=1000))

        mock_provider.stream.assert_called_once_with(
            messages, "model", 0.5, 1000
        )

    def test_stream_fallback_on_error(self):
        """Stream falls back to another provider on error."""
        failing = MockProvider(
            "primary",
            raise_on_stream=Exception("API Error"),
        )
        backup = MockProvider(
            "backup",
            stream_response=["Backup", " ", "response"],
        )
        router = ProviderRouter(providers=[failing, backup])
        messages = [Message(role="user", content="Hi")]

        result = list(router.stream(messages, "primary:model"))

        assert result == ["Backup", " ", "response"]

    def test_stream_all_providers_fail(self):
        """Stream raises when all providers fail."""
        failing1 = MockProvider(
            "provider1",
            raise_on_stream=Exception("Error 1"),
        )
        failing2 = MockProvider(
            "provider2",
            raise_on_stream=Exception("Error 2"),
        )
        router = ProviderRouter(providers=[failing1, failing2])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(RuntimeError) as exc_info:
            list(router.stream(messages, "provider1:model"))

        assert "All providers failed" in str(exc_info.value)

    def test_stream_keyboard_interrupt(self):
        """Stream doesn't swallow KeyboardInterrupt."""
        provider = MockProvider(
            "gemini",
            raise_on_stream=KeyboardInterrupt(),
        )
        router = ProviderRouter(providers=[provider])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(KeyboardInterrupt):
            list(router.stream(messages, "gemini:model"))

    def test_stream_skips_unavailable_fallback(self):
        """Stream skips unavailable providers during fallback."""
        failing = MockProvider(
            "primary",
            raise_on_stream=Exception("Error"),
        )
        unavailable = MockProvider("unavailable", available=False)
        backup = MockProvider("backup", stream_response=["Success"])
        router = ProviderRouter(providers=[failing, unavailable, backup])
        messages = [Message(role="user", content="Hi")]

        result = list(router.stream(messages, "primary:model"))

        assert result == ["Success"]

    def test_stream_explicit_provider_does_not_cross_fallback(self):
        """Streaming should also stay pinned to the explicitly requested provider."""
        failing = MockProvider(
            "primary",
            raise_on_stream=Exception("API Error"),
        )
        backup = MockProvider(
            "backup",
            stream_response=["Backup"],
        )
        router = ProviderRouter(providers=[failing, backup])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(RuntimeError) as exc_info:
            list(router.stream(messages, "primary:model", lock_provider=True))

        assert "requested model" in str(exc_info.value).lower()
        assert "primary:model" in str(exc_info.value)


# =============================================================================
# Tests for list_all_models method
# =============================================================================


class TestListAllModels:
    """Tests for list_all_models method."""

    def test_list_empty(self):
        """List models with no providers."""
        router = ProviderRouter(providers=[])
        result = router.list_all_models()
        assert result == []

    def test_list_single_provider(self):
        """List models from single provider."""
        provider = MockProvider(
            "gemini",
            models=[
                ModelInfo(id="model-1", provider="gemini", name="Model 1", local=False),
                ModelInfo(id="model-2", provider="gemini", name="Model 2", local=False),
            ],
        )
        router = ProviderRouter(providers=[provider])

        result = router.list_all_models()

        assert len(result) == 2
        assert any(m.id == "model-1" for m in result)
        assert any(m.id == "model-2" for m in result)

    def test_list_multiple_providers(self):
        """List models from multiple providers."""
        provider1 = MockProvider(
            "gemini",
            models=[ModelInfo(id="gemini-model", provider="gemini", name="Gemini", local=False)],
        )
        provider2 = MockProvider(
            "openai",
            models=[ModelInfo(id="gpt-4", provider="openai", name="GPT-4", local=False)],
        )
        router = ProviderRouter(providers=[provider1, provider2])

        result = router.list_all_models()

        assert len(result) == 2
        assert any(m.id == "gemini-model" for m in result)
        assert any(m.id == "gpt-4" for m in result)

    def test_list_skips_unavailable(self):
        """List models skips unavailable providers."""
        available = MockProvider(
            "gemini",
            models=[ModelInfo(id="model", provider="gemini", name="Model", local=False)],
        )
        unavailable = MockProvider(
            "openai",
            available=False,
            models=[ModelInfo(id="gpt-4", provider="openai", name="GPT-4", local=False)],
        )
        router = ProviderRouter(providers=[available, unavailable])

        result = router.list_all_models()

        assert len(result) == 1
        assert result[0].id == "model"


# =============================================================================
# Integration tests
# =============================================================================


class TestRouterIntegration:
    """Integration tests for ProviderRouter."""

    def test_full_workflow(self):
        """Full workflow with multiple providers."""
        gemini = MockProvider(
            "gemini",
            models=[ModelInfo(id="gemini-flash", provider="gemini", name="Gemini Flash", local=False)],
            generate_response="Gemini response",
            stream_response=["Gemini", " stream"],
        )
        openai = MockProvider(
            "openai",
            models=[ModelInfo(id="gpt-4", provider="openai", name="GPT-4", local=False)],
            generate_response="OpenAI response",
        )
        router = ProviderRouter(
            providers=[gemini, openai],
            default_model="gemini:gemini-flash",
        )

        # Test model listing
        models = router.list_all_models()
        assert len(models) == 2

        # Test resolution
        provider, model = router.resolve("gemini:gemini-flash")
        assert provider is gemini
        assert model == "gemini-flash"

        # Test generation
        messages = [Message(role="user", content="Hi")]
        response = router.generate(messages, "gemini:model")
        assert response == "Gemini response"

        # Test streaming
        stream = list(router.stream(messages, "gemini:model"))
        assert stream == ["Gemini", " stream"]

    def test_fallback_chain(self):
        """Fallback chain works correctly."""
        failing = MockProvider(
            "primary",
            raise_on_generate=Exception("Primary failed"),
        )
        also_failing = MockProvider(
            "secondary",
            raise_on_generate=Exception("Secondary failed"),
        )
        working = MockProvider(
            "tertiary",
            generate_response="Success!",
        )
        router = ProviderRouter(providers=[failing, also_failing, working])
        messages = [Message(role="user", content="Hi")]

        result = router.generate(messages, "primary:model")

        assert result == "Success!"

    def test_provider_order_preserved(self):
        """Provider order is preserved for fallback."""
        provider1 = MockProvider("first")
        provider2 = MockProvider("second")
        provider3 = MockProvider("third")

        router = ProviderRouter(providers=[provider1, provider2, provider3])

        assert router._fallback_order == ["first", "second", "third"]

    def test_error_message_includes_details(self):
        """Error message includes failure details."""
        failing1 = MockProvider(
            "provider1",
            raise_on_generate=Exception("Connection timeout"),
        )
        failing2 = MockProvider(
            "provider2",
            raise_on_generate=Exception("API rate limit"),
        )
        router = ProviderRouter(providers=[failing1, failing2])
        messages = [Message(role="user", content="Hi")]

        with pytest.raises(RuntimeError) as exc_info:
            router.generate(messages, "provider1:model")

        error_msg = str(exc_info.value)
        assert "provider1" in error_msg
        assert "provider2" in error_msg
        assert "Connection timeout" in error_msg or "API rate limit" in error_msg
