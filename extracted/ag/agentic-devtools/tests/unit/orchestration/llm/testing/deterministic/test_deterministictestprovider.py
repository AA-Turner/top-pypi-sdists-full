"""Tests for DeterministicTestProvider."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_devtools.orchestration.llm.errors import NoFixtureFoundError
from agentic_devtools.orchestration.llm.testing.deterministic import DeterministicTestProvider
from agentic_devtools.orchestration.llm.types import LLMMessage, LLMResponse, ProviderType, TokenUsage


class TestDeterministicTestProvider:
    """Tests for DeterministicTestProvider."""

    def _create_fixture(self, tmp_path, key, text="fixture response", usage=None):
        usage_data = usage or {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}
        fixture = {
            "fixture_version": 1,
            "request": {},
            "response": {
                "text": text,
                "model": "gpt-4o",
                "provider_type": "azure_openai",
                "usage": usage_data,
            },
        }
        (tmp_path / f"{key}.json").write_text(json.dumps(fixture))

    @pytest.mark.asyncio
    async def test_replay_fixture_by_name(self, tmp_path):
        self._create_fixture(tmp_path, "my-fixture", "Hello from fixture")
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        result = await provider.complete(
            [LLMMessage(role="user", content="Hi")],
            fixture_name="my-fixture",
        )

        assert result.text == "Hello from fixture"
        assert result.served_from_fixture is True
        assert result.provider_type == ProviderType.AZURE_OPENAI
        assert result.usage is not None
        assert result.usage.total_tokens == 15

    @pytest.mark.asyncio
    async def test_replay_produces_identical_response(self, tmp_path):
        self._create_fixture(tmp_path, "stable")
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        r1 = await provider.complete([LLMMessage(role="user", content="Hi")], fixture_name="stable")
        r2 = await provider.complete([LLMMessage(role="user", content="Hi")], fixture_name="stable")
        assert r1.text == r2.text
        assert r1.usage == r2.usage

    @pytest.mark.asyncio
    async def test_no_fixture_raises(self, tmp_path):
        provider = DeterministicTestProvider(fixture_dir=tmp_path)
        with pytest.raises(NoFixtureFoundError):
            await provider.complete(
                [LLMMessage(role="user", content="Hi")],
                fixture_name="nonexistent",
            )

    @pytest.mark.asyncio
    async def test_stream_returns_single_chunk(self, tmp_path):
        self._create_fixture(tmp_path, "stream-fixture", "streamed text")
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        chunks = []
        async for chunk in provider.stream([LLMMessage(role="user", content="Hi")], fixture_name="stream-fixture"):
            chunks.append(chunk)

        assert len(chunks) == 1
        assert chunks[0].text_delta == "streamed text"
        assert chunks[0].finish_reason == "stop"

    def test_fixture_store_property(self, tmp_path):
        provider = DeterministicTestProvider(fixture_dir=tmp_path)
        assert provider.fixture_store.fixture_dir == tmp_path

    def test_record_mode_without_real_provider_raises(self, tmp_path):
        """record_mode=True without real_provider must raise ValueError immediately."""
        with pytest.raises(ValueError, match="record_mode"):
            DeterministicTestProvider(fixture_dir=tmp_path, record_mode=True)

    @pytest.mark.asyncio
    async def test_record_mode_saves_fixture(self, tmp_path):
        """Record mode calls real provider and saves response."""
        real_provider = MagicMock()
        real_response = LLMResponse(
            text="recorded response",
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
            usage=TokenUsage(input_tokens=20, output_tokens=10, total_tokens=30),
        )
        real_provider.complete = AsyncMock(return_value=real_response)

        provider = DeterministicTestProvider(
            fixture_dir=tmp_path,
            record_mode=True,
            real_provider=real_provider,
            model="gpt-4o",
        )

        result = await provider.complete(
            [LLMMessage(role="user", content="Hi")],
            fixture_name="record-test",
        )
        assert result.text == "recorded response"
        # Verify fixture was saved
        assert (tmp_path / "record-test.json").exists()

    @pytest.mark.asyncio
    async def test_record_mode_includes_kwargs_in_request_payload(self, tmp_path):
        """Record mode must include temperature/max_tokens/response_format in request_payload."""
        real_provider = MagicMock()
        real_response = LLMResponse(
            text="r",
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
            usage=TokenUsage(input_tokens=5, output_tokens=5, total_tokens=10),
        )
        real_provider.complete = AsyncMock(return_value=real_response)

        provider = DeterministicTestProvider(
            fixture_dir=tmp_path,
            record_mode=True,
            real_provider=real_provider,
            model="gpt-4o",
            node_type="test-node",
        )
        schema = {"type": "object"}
        await provider.complete(
            [LLMMessage(role="user", content="Hi")],
            fixture_name="kwargs-test",
            temperature=0.5,
            max_tokens=512,
            response_format={"type": "json_schema", "json_schema": schema},
            top_p=0.8,
        )

        saved = json.loads((tmp_path / "kwargs-test.json").read_text())
        req = saved["request"]
        assert req["temperature"] == pytest.approx(0.5)
        assert req["max_tokens"] == 512
        assert req["response_format"] == {"type": "json_schema", "json_schema": schema}
        assert req["additional_params"] == {"top_p": 0.8}

    @pytest.mark.asyncio
    async def test_record_mode_omits_none_kwargs_from_request_payload(self, tmp_path):
        """None-valued kwargs must not appear in the saved request_payload."""
        real_provider = MagicMock()
        real_response = LLMResponse(
            text="r",
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
            usage=TokenUsage(input_tokens=5, output_tokens=5, total_tokens=10),
        )
        real_provider.complete = AsyncMock(return_value=real_response)

        provider = DeterministicTestProvider(
            fixture_dir=tmp_path,
            record_mode=True,
            real_provider=real_provider,
            model="gpt-4o",
        )
        await provider.complete(
            [LLMMessage(role="user", content="Hi")],
            fixture_name="no-kwargs-test",
            temperature=None,
            max_tokens=None,
            response_format=None,
        )

        saved = json.loads((tmp_path / "no-kwargs-test.json").read_text())
        req = saved["request"]
        assert "temperature" not in req
        assert "max_tokens" not in req
        assert "response_format" not in req
        real_provider.complete.assert_awaited_once_with([LLMMessage(role="user", content="Hi")])

    @pytest.mark.asyncio
    async def test_record_mode_preserves_estimated_cost_usd(self, tmp_path):
        """Record mode must persist estimated_cost_usd so replayed fixtures can reproduce cost tracking."""
        real_provider = MagicMock()
        real_response = LLMResponse(
            text="cost response",
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
            usage=TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150, estimated_cost_usd=0.0042),
        )
        real_provider.complete = AsyncMock(return_value=real_response)

        provider = DeterministicTestProvider(
            fixture_dir=tmp_path,
            record_mode=True,
            real_provider=real_provider,
            model="gpt-4o",
        )

        await provider.complete([LLMMessage(role="user", content="Price me")], fixture_name="cost-test")

        saved = json.loads((tmp_path / "cost-test.json").read_text())
        assert saved["response"]["usage"]["estimated_cost_usd"] == pytest.approx(0.0042)

    @pytest.mark.asyncio
    async def test_record_mode_preserves_null_estimated_cost_usd(self, tmp_path):
        """Record mode must persist null estimated_cost_usd when the provider did not populate it."""
        real_provider = MagicMock()
        real_response = LLMResponse(
            text="no cost response",
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
            usage=TokenUsage(input_tokens=10, output_tokens=5, total_tokens=15, estimated_cost_usd=None),
        )
        real_provider.complete = AsyncMock(return_value=real_response)

        provider = DeterministicTestProvider(
            fixture_dir=tmp_path,
            record_mode=True,
            real_provider=real_provider,
            model="gpt-4o",
        )

        await provider.complete([LLMMessage(role="user", content="No cost")], fixture_name="null-cost-test")

        saved = json.loads((tmp_path / "null-cost-test.json").read_text())
        assert saved["response"]["usage"]["estimated_cost_usd"] is None

    @pytest.mark.asyncio
    async def test_complete_structured_delegates_to_complete(self, tmp_path):
        """complete_structured should call complete with response_format set."""
        self._create_fixture(tmp_path, "structured-fixture", '{"key": "value"}')
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        result = await provider.complete_structured(
            [LLMMessage(role="user", content="Get data")],
            schema={"type": "object"},
            fixture_name="structured-fixture",
        )
        assert result.text == '{"key": "value"}'
        assert result.served_from_fixture is True

    @pytest.mark.asyncio
    async def test_record_mode_complete_structured_uses_real_structured_call(self, tmp_path):
        """Record mode should use the real provider's structured API."""
        real_provider = MagicMock()
        real_response = LLMResponse(
            text='{"answer": "ok"}',
            model="gpt-4o",
            provider_type=ProviderType.AZURE_OPENAI,
            usage=TokenUsage(input_tokens=12, output_tokens=6, total_tokens=18),
        )
        real_provider.complete = AsyncMock()
        real_provider.complete_structured = AsyncMock(return_value=real_response)

        provider = DeterministicTestProvider(
            fixture_dir=tmp_path,
            record_mode=True,
            real_provider=real_provider,
            model="gpt-4o",
            node_type="test-node",
        )
        messages = [LLMMessage(role="user", content="Return JSON")]
        schema = {"type": "object", "properties": {"answer": {"type": "string"}}}

        result = await provider.complete_structured(
            messages,
            schema=schema,
            fixture_name="structured-record",
            temperature=0.5,
            max_tokens=256,
            top_p=0.8,
        )

        assert result == real_response
        real_provider.complete.assert_not_called()
        real_provider.complete_structured.assert_awaited_once_with(
            messages,
            schema=schema,
            temperature=0.5,
            max_tokens=256,
            top_p=0.8,
        )
        saved = json.loads((tmp_path / "structured-record.json").read_text())
        assert saved["request"]["response_format"] == {
            "type": "json_schema",
            "json_schema": schema,
        }
        assert saved["request"]["additional_params"] == {"top_p": 0.8}

    @pytest.mark.asyncio
    async def test_replay_without_usage(self, tmp_path):
        """Fixture without usage data should still work."""
        fixture = {
            "fixture_version": 1,
            "request": {},
            "response": {
                "text": "no usage",
                "model": "gpt-4o",
                "provider_type": "azure_openai",
                "usage": None,
            },
        }
        (tmp_path / "no-usage.json").write_text(json.dumps(fixture))
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        result = await provider.complete(
            [LLMMessage(role="user", content="Hi")],
            fixture_name="no-usage",
        )
        assert result.text == "no usage"
        assert result.usage is None

    @pytest.mark.asyncio
    async def test_structured_and_plain_calls_use_different_fixture_keys(self, tmp_path):
        """complete_structured and complete with same messages must resolve to different fixture keys."""
        from agentic_devtools.orchestration.llm.testing.canonical_hash import compute_fixture_key
        from agentic_devtools.orchestration.llm.types import LLMMessage

        messages = [LLMMessage(role="user", content="Return JSON")]
        schema = {"type": "object", "properties": {"answer": {"type": "string"}}}

        plain_key = compute_fixture_key(node_type="t", model="m", messages=messages)
        structured_key = compute_fixture_key(
            node_type="t",
            model="m",
            messages=messages,
            response_format={"type": "json_schema", "json_schema": schema},
        )
        assert plain_key != structured_key

    @pytest.mark.asyncio
    async def test_complete_structured_includes_schema_in_fixture_key(self, tmp_path):
        """Structured requests should include the provided schema in the fixture-key response_format."""
        provider = DeterministicTestProvider(fixture_dir=tmp_path)
        schema = {"type": "object", "properties": {"answer": {"type": "string"}}}

        with patch(
            "agentic_devtools.orchestration.llm.testing.deterministic.compute_fixture_key",
            return_value="missing",
        ) as mocked_compute_fixture_key:
            with pytest.raises(NoFixtureFoundError):
                await provider.complete_structured([LLMMessage(role="user", content="Return JSON")], schema=schema)

        assert mocked_compute_fixture_key.call_count == 1
        assert mocked_compute_fixture_key.call_args.kwargs["response_format"] == {
            "type": "json_schema",
            "json_schema": schema,
        }

    @pytest.mark.asyncio
    async def test_complete_includes_extra_kwargs_in_fixture_key(self, tmp_path):
        """Extra generation kwargs must contribute to fixture-key computation."""
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        with patch(
            "agentic_devtools.orchestration.llm.testing.deterministic.compute_fixture_key",
            return_value="missing",
        ) as mocked_compute_fixture_key:
            with pytest.raises(NoFixtureFoundError):
                await provider.complete([LLMMessage(role="user", content="Return JSON")], top_p=0.9, seed=42)

        assert mocked_compute_fixture_key.call_count == 1
        assert mocked_compute_fixture_key.call_args.kwargs["additional_params"] == {"top_p": 0.9, "seed": 42}

    @pytest.mark.asyncio
    async def test_complete_structured_replay_raises_on_invalid_json_fixture(self, tmp_path):
        """complete_structured in replay mode must raise StructuredOutputValidationError
        when the fixture response text is not valid JSON."""
        from agentic_devtools.orchestration.llm.errors import StructuredOutputValidationError

        self._create_fixture(tmp_path, "bad-json", text="not valid json {{{")
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        with pytest.raises(StructuredOutputValidationError, match="not valid JSON"):
            await provider.complete_structured(
                [LLMMessage(role="user", content="Get data")],
                schema={"type": "object"},
                fixture_name="bad-json",
            )

    @pytest.mark.asyncio
    async def test_complete_structured_replay_returns_response_for_valid_json_fixture(self, tmp_path):
        """complete_structured in replay mode succeeds when fixture text is valid JSON."""
        self._create_fixture(tmp_path, "valid-json", text='{"key": "value"}')
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        result = await provider.complete_structured(
            [LLMMessage(role="user", content="Get data")],
            schema={"type": "object"},
            fixture_name="valid-json",
        )
        assert result.text == '{"key": "value"}'
        assert result.served_from_fixture is True

    @pytest.mark.asyncio
    async def test_complete_structured_replay_raises_on_schema_violation(self, tmp_path):
        """complete_structured in replay mode must raise StructuredOutputValidationError
        when the fixture response is valid JSON but violates the provided schema."""
        from agentic_devtools.orchestration.llm.errors import StructuredOutputValidationError

        # Valid JSON, but schema requires a 'name' property of type string
        self._create_fixture(tmp_path, "bad-schema", text='{"age": 42}')
        provider = DeterministicTestProvider(fixture_dir=tmp_path)

        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        with pytest.raises(StructuredOutputValidationError, match="does not conform to schema"):
            await provider.complete_structured(
                [LLMMessage(role="user", content="Get person")],
                schema=schema,
                fixture_name="bad-schema",
            )
