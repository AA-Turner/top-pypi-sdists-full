from typing import Any, cast

import pytest

from agentic_devtools.ai_providers.copilot_discovery import (
    DEFAULT_CONTEXT_WINDOW,
    normalize_acp_model,
)

_META = {
    "copilotUsage": "0.33x",
    "copilotPriceCategory": "low",
    "copilotEnablement": "enabled",
}


def test_normalizes_a_live_acp_entry() -> None:
    record = normalize_acp_model(
        {
            "modelId": " claude-haiku-4.5 ",
            "name": " Claude Haiku 4.5 ",
            "description": "Claude Haiku 4.5",
            "_meta": dict(_META),
        }
    )

    assert record is not None
    assert record.model_id == "claude-haiku-4.5"
    assert record.name == "Claude Haiku 4.5"
    assert record.provider == "copilot"
    assert record.context_window == DEFAULT_CONTEXT_WINDOW
    assert record.max_output_tokens is None
    assert record.supports_tools is True


def test_preserves_the_full_meta_object_unchanged() -> None:
    record = normalize_acp_model({"modelId": "gpt-5-mini", "_meta": dict(_META)})

    assert record is not None
    assert cast("dict[str, Any]", record.raw_metadata["_meta"]) == _META


def test_preserves_credential_like_keys_verbatim() -> None:
    """Credential-like keys inside the ACP entry must not be redacted."""
    entry = {"modelId": "gpt-5-mini", "token": "secret-value", "api_key": "also-secret"}
    record = normalize_acp_model(entry)

    assert record is not None
    assert record.raw_metadata["token"] == "secret-value"
    assert record.raw_metadata["api_key"] == "also-secret"


def test_falls_back_to_the_model_id_when_the_name_is_unusable() -> None:
    record = normalize_acp_model({"modelId": "auto", "name": "   "})

    assert record is not None
    assert record.name == "auto"


def test_uses_advertised_limits_and_tool_support_when_present() -> None:
    record = normalize_acp_model(
        {
            "modelId": "gpt-5-mini",
            "contextWindow": 200000,
            "maxOutputTokens": 64000,
            "supportsTools": False,
        }
    )

    assert record is not None
    assert record.context_window == 200000
    assert record.max_output_tokens == 64000
    assert record.supports_tools is False


@pytest.mark.parametrize(
    "entry",
    [
        None,
        "gpt-5-mini",
        {},
        {"modelId": ""},
        {"modelId": "   "},
        {"modelId": 42},
    ],
)
def test_returns_none_for_unusable_entries(entry: object) -> None:
    assert normalize_acp_model(entry) is None


@pytest.mark.parametrize("context_window", [0, -1, True, "200000", None])
def test_ignores_invalid_context_windows(context_window: object) -> None:
    record = normalize_acp_model({"modelId": "gpt-5-mini", "contextWindow": context_window})

    assert record is not None
    assert record.context_window == DEFAULT_CONTEXT_WINDOW
