"""Deterministic test provider using recorded fixtures."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import jsonschema

from agentic_devtools.orchestration.llm.base_provider import LLMProvider, omit_none_values
from agentic_devtools.orchestration.llm.errors import StructuredOutputValidationError
from agentic_devtools.orchestration.llm.testing.canonical_hash import compute_fixture_key
from agentic_devtools.orchestration.llm.testing.fixture_store import FixtureStore, save_fixture
from agentic_devtools.orchestration.llm.types import (
    LLMMessage,
    LLMResponse,
    ProviderType,
    StreamChunk,
    TokenUsage,
)


class DeterministicTestProvider(LLMProvider):
    """Provider that replays recorded fixtures without network calls.

    Supports:
    - Fixture lookup by SHA-256 hash of canonical request
    - Explicit fixture name override
    - Record mode for capturing new fixtures
    - Byte-identical responses for reproducible tests
    """

    def __init__(
        self,
        fixture_dir: str | Path,
        *,
        record_mode: bool = False,
        real_provider: LLMProvider | None = None,
        node_type: str = "",
        model: str = "test-model",
    ) -> None:
        """Initialize deterministic test provider.

        Args:
            fixture_dir: Directory containing fixture files.
            record_mode: If True, calls real_provider and saves responses.
            real_provider: Provider to use in record mode.
            node_type: Default node type for fixture key computation.
            model: Default model name for fixture key computation.
        """
        self._store = FixtureStore(fixture_dir)
        if record_mode and real_provider is None:
            raise ValueError("record_mode=True requires a real_provider to be specified")
        self._record_mode = record_mode
        self._real_provider = real_provider
        self._node_type = node_type
        self._model = model

    @property
    def fixture_store(self) -> FixtureStore:
        """Return the fixture store."""
        return self._store

    def _build_request_payload(
        self,
        messages: list[LLMMessage],
        provider_kwargs: dict[str, Any],
        key_additional_params: dict[str, Any],
    ) -> dict[str, Any]:
        """Build the persisted request payload for a recorded fixture."""
        request_payload: dict[str, Any] = {
            "node_type": self._node_type,
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content, "name": m.name} for m in messages],
        }
        if "temperature" in provider_kwargs:
            request_payload["temperature"] = provider_kwargs["temperature"]
        if "max_tokens" in provider_kwargs:
            request_payload["max_tokens"] = provider_kwargs["max_tokens"]
        if "response_format" in provider_kwargs:
            request_payload["response_format"] = provider_kwargs["response_format"]
        if key_additional_params:
            request_payload["additional_params"] = key_additional_params
        return request_payload

    def _save_recorded_fixture(
        self,
        key: str,
        messages: list[LLMMessage],
        provider_kwargs: dict[str, Any],
        key_additional_params: dict[str, Any],
        response: LLMResponse,
    ) -> None:
        """Persist a recorded fixture."""
        request_payload = self._build_request_payload(messages, provider_kwargs, key_additional_params)
        response_payload = {
            "text": response.text,
            "model": response.model,
            "provider_type": response.provider_type.value,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens,
                "estimated_cost_usd": response.usage.estimated_cost_usd,
            }
            if response.usage
            else None,
        }
        save_fixture(key, request=request_payload, response=response_payload, fixture_dir=self._store.fixture_dir)

    async def complete(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> LLMResponse:
        """Replay or record a completion call."""
        fixture_name = kwargs.pop("fixture_name", None)
        provider_kwargs = omit_none_values(kwargs)
        key_additional_params = {
            key: value
            for key, value in provider_kwargs.items()
            if key not in {"temperature", "max_tokens", "response_format"}
        }
        key = fixture_name or compute_fixture_key(
            node_type=self._node_type,
            model=self._model,
            messages=messages,
            temperature=provider_kwargs.get("temperature"),
            max_tokens=provider_kwargs.get("max_tokens"),
            response_format=provider_kwargs.get("response_format"),
            additional_params=key_additional_params,
        )

        if self._record_mode and self._real_provider:
            # Record mode: call real provider and save
            response = await self._real_provider.complete(messages, **provider_kwargs)
            self._save_recorded_fixture(key, messages, provider_kwargs, key_additional_params, response)
            return response

        # Replay mode: load from fixture
        record = self._store.load(key)
        resp_data = record["response"]

        usage = None
        if resp_data.get("usage"):
            u = resp_data["usage"]
            usage = TokenUsage(
                input_tokens=u["input_tokens"],
                output_tokens=u["output_tokens"],
                total_tokens=u["total_tokens"],
                estimated_cost_usd=u.get("estimated_cost_usd"),
            )

        return LLMResponse(
            text=resp_data["text"],
            model=resp_data.get("model", self._model),
            provider_type=ProviderType(resp_data.get("provider_type", "azure_openai")),
            usage=usage,
            served_from_fixture=True,
        )

    async def complete_structured(
        self,
        messages: list[LLMMessage],
        schema: dict[str, Any],
        **kwargs: Any,
    ) -> LLMResponse:
        """Replay or record a structured completion call."""
        kwargs.setdefault("response_format", {"type": "json_schema", "json_schema": schema})
        if self._record_mode and self._real_provider:
            fixture_name = kwargs.pop("fixture_name", None)
            provider_kwargs = omit_none_values(kwargs)
            key_additional_params = {
                key: value
                for key, value in provider_kwargs.items()
                if key not in {"temperature", "max_tokens", "response_format"}
            }
            key = fixture_name or compute_fixture_key(
                node_type=self._node_type,
                model=self._model,
                messages=messages,
                temperature=provider_kwargs.get("temperature"),
                max_tokens=provider_kwargs.get("max_tokens"),
                response_format=provider_kwargs.get("response_format"),
                additional_params=key_additional_params,
            )
            real_provider_kwargs = dict(provider_kwargs)
            real_provider_kwargs.pop("response_format", None)
            response = await self._real_provider.complete_structured(
                messages,
                schema=schema,
                **real_provider_kwargs,
            )
            self._save_recorded_fixture(key, messages, provider_kwargs, key_additional_params, response)
            return response
        response = await self.complete(messages, **kwargs)
        try:
            parsed = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise StructuredOutputValidationError(
                f"Fixture response is not valid JSON: {exc}",
                schema=schema,
                response_text=response.text,
            ) from exc
        try:
            jsonschema.validate(parsed, schema)
        except jsonschema.ValidationError as exc:
            raise StructuredOutputValidationError(
                f"Fixture response does not conform to schema: {exc.message}",
                schema=schema,
                response_text=response.text,
                validation_errors=[exc.message],
            ) from exc
        return response

    async def stream(
        self,
        messages: list[LLMMessage],
        **kwargs: Any,
    ) -> AsyncIterator[StreamChunk]:
        """Replay a fixture as a single-chunk stream."""
        response = await self.complete(messages, **kwargs)

        # Emit the full response as a single chunk with finish_reason
        yield StreamChunk(
            text_delta=response.text,
            chunk_index=0,
            finish_reason="stop",
            token_usage=response.usage,
        )
