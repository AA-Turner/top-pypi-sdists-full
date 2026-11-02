"""Tests for LLMResponse dataclass."""

from agentic_devtools.orchestration.llm.types import LLMResponse, NodeConfig, ProviderType, TokenUsage


class TestLLMResponse:
    """Tests for LLMResponse."""

    def test_basic_creation(self):
        response = LLMResponse(
            text="Hello",
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
        )
        assert response.text == "Hello"
        assert response.model == "gpt-4o"
        assert response.provider_type == ProviderType.AZURE_OPENAI
        assert response.usage is None
        assert response.served_from_fixture is False
        assert response.latency_ms is None
        assert response.finish_reason is None

    def test_with_usage(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        response = LLMResponse(
            text="Hello",
            model="gpt-4o",
            provider_type=ProviderType.OPENAI_DIRECT,
            usage=usage,
            latency_ms=250,
        )
        assert response.usage == usage
        assert response.latency_ms == 250

    def test_fixture_flag(self):
        response = LLMResponse(
            text="Fixture",
            model="test-model",
            provider_type=ProviderType.AZURE_OPENAI,
            served_from_fixture=True,
        )
        assert response.served_from_fixture is True

    def test_frozen(self):
        response = LLMResponse(text="Hi", model="gpt-4o", provider_type=ProviderType.AZURE_OPENAI)
        try:
            response.text = "Changed"  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass


class TestNodeConfigProperties:
    """Tests for NodeConfig computed properties."""

    def test_effective_model_returns_override_when_set(self):
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            model_override="gpt-4o-mini",
        )
        assert config.effective_model == "gpt-4o-mini"

    def test_effective_model_returns_base_when_no_override(self):
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
        )
        assert config.effective_model == "gpt-4o"

    def test_effective_temperature_from_override(self):
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            temperature=0.7,
            params_override={"temperature": 0.2},
        )
        assert config.effective_temperature == 0.2

    def test_effective_temperature_from_base(self):
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            temperature=0.7,
        )
        assert config.effective_temperature == 0.7

    def test_effective_max_tokens_from_override(self):
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            max_tokens=1000,
            params_override={"max_tokens": 2000},
        )
        assert config.effective_max_tokens == 2000

    def test_effective_max_tokens_from_base(self):
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            max_tokens=1000,
        )
        assert config.effective_max_tokens == 1000

    def test_params_override_is_copied_and_immutable(self):
        source = {"temperature": 0.2}
        config = NodeConfig(
            provider_id="p1",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            params_override=source,
        )

        source["temperature"] = 0.9

        assert config.effective_temperature == 0.2
        try:
            config.params_override["temperature"] = 0.5  # type: ignore[index]
            assert False, "Should have raised"
        except TypeError:
            pass
