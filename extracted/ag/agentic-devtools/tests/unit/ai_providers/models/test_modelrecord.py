from types import MappingProxyType
from typing import Any, cast

import pytest

from agentic_devtools.ai_providers.models import ModelRecord


def test_model_record_creation() -> None:
    raw_meta: dict[str, Any] = {
        "foo": "bar",
        "token": "secret-value",
        "nested": {"api_key": "hidden", "safe": [1]},
    }
    record = ModelRecord(
        name="Test Model",
        model_id="test-v1",
        provider="TestProvider",
        context_window=4096,
        max_output_tokens=1024,
        supports_tools=True,
        raw_metadata=raw_meta,
    )
    nested = cast("dict[str, Any]", record.raw_metadata["nested"])
    assert record.name == "Test Model"
    assert record.max_output_tokens == 1024
    assert record.raw_metadata["foo"] == "bar"
    assert record.raw_metadata["token"] == "<redacted>"
    assert nested["api_key"] == "<redacted>"
    assert isinstance(record.raw_metadata, MappingProxyType)
    assert nested["safe"] == (1,)

    raw_meta["nested"]["safe"].append(2)
    assert nested["safe"] == (1,)


def test_model_record_can_preserve_raw_metadata_verbatim() -> None:
    raw_meta: dict[str, Any] = {"token": "secret-value", "nested": {"api_key": "hidden"}}

    record = ModelRecord(
        name="Test Model",
        model_id="test-v1",
        provider="TestProvider",
        context_window=4096,
        max_output_tokens=1024,
        supports_tools=True,
        raw_metadata=raw_meta,
        raw_metadata_verbatim=True,
    )

    nested = cast("dict[str, Any]", record.raw_metadata["nested"])

    assert record.raw_metadata["token"] == "secret-value"
    assert nested["api_key"] == "hidden"


def test_model_record_allows_missing_max_output_tokens() -> None:
    record = ModelRecord(
        name="Test Model",
        model_id="test-v1",
        provider="TestProvider",
        context_window=4096,
        max_output_tokens=None,
        supports_tools=True,
        raw_metadata={},
    )

    assert record.max_output_tokens is None


def test_model_record_accepts_source_observation_metadata() -> None:
    record = ModelRecord(
        name="Test Model",
        model_id="test-v1",
        provider="TestProvider",
        context_window=4096,
        max_output_tokens=None,
        supports_tools=True,
        raw_metadata={},
        source="acp-cache",
        observed_at="2026-08-27T00:00:00+00:00",
    )

    assert record.source == "acp-cache"
    assert record.observed_at == "2026-08-27T00:00:00+00:00"


def test_model_record_rejects_invalid_observed_at_timestamp() -> None:
    with pytest.raises(ValueError, match="observed_at must be a valid ISO-8601 timestamp"):
        ModelRecord(
            name="Test Model",
            model_id="test-v1",
            provider="TestProvider",
            context_window=4096,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={},
            source="acp-cache",
            observed_at="yesterday",
        )


def test_model_record_rejects_naive_observed_at_timestamp() -> None:
    with pytest.raises(ValueError, match="observed_at must be a timezone-aware ISO-8601 timestamp"):
        ModelRecord(
            name="Test Model",
            model_id="test-v1",
            provider="TestProvider",
            context_window=4096,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={},
            source="acp-cache",
            observed_at="2026-08-27T00:00:00",
        )


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {
                "name": "",
                "model_id": "test-v1",
                "provider": "TestProvider",
                "context_window": 4096,
                "max_output_tokens": 1024,
                "supports_tools": True,
                "raw_metadata": {},
            },
            "name must be a non-empty string",
        ),
        (
            {
                "name": "Test Model",
                "model_id": "",
                "provider": "TestProvider",
                "context_window": 4096,
                "max_output_tokens": 1024,
                "supports_tools": True,
                "raw_metadata": {},
            },
            "model_id must be a non-empty string",
        ),
        (
            {
                "name": "Test Model",
                "model_id": "test-v1",
                "provider": "",
                "context_window": 4096,
                "max_output_tokens": 1024,
                "supports_tools": True,
                "raw_metadata": {},
            },
            "provider must be a non-empty string",
        ),
        (
            {
                "name": "Test Model",
                "model_id": "test-v1",
                "provider": "TestProvider",
                "context_window": 0,
                "max_output_tokens": 1024,
                "supports_tools": True,
                "raw_metadata": {},
            },
            "context_window must be a positive integer",
        ),
        (
            {
                "name": "Test Model",
                "model_id": "test-v1",
                "provider": "TestProvider",
                "context_window": 4096,
                "max_output_tokens": -1,
                "supports_tools": True,
                "raw_metadata": {},
            },
            "max_output_tokens must be a positive integer",
        ),
        (
            {
                "name": "Test Model",
                "model_id": "test-v1",
                "provider": "TestProvider",
                "context_window": 4096,
                "max_output_tokens": 1024,
                "supports_tools": "yes",
                "raw_metadata": {},
            },
            "supports_tools must be a boolean",
        ),
    ],
)
def test_model_record_rejects_invalid_schema(kwargs: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        ModelRecord(**kwargs)  # type: ignore[arg-type]
