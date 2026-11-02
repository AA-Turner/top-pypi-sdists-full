"""Tests for ``_resolve_model_id()``."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.review.nodes.scaffold_comments import _resolve_model_id

_PATCH_LOAD_CONFIG = "agentic_devtools.orchestration.llm.config.load_config"
_PATCH_RESOLVE_NODE_CONFIG = "agentic_devtools.orchestration.llm.config.resolve_node_config"


class TestResolveModelId:
    """FR-007: model_id resolution precedence."""

    def test_model_config_raw_default_model_takes_priority(self) -> None:
        """model_config_raw.get('default-model') is the primary source."""
        state = {"model_config_raw": {"default-model": "claude-opus-4.6"}}
        assert _resolve_model_id(state, lambda _: "gpt-4o") == "claude-opus-4.6"

    def test_prefers_effective_model_from_file_results(self) -> None:
        state = {"model_config_raw": {"default-model": "requested"}, "file_results": [{"model_id": "canonical"}]}

        assert _resolve_model_id(state, lambda _: "fallback") == "canonical"

    def test_reads_effective_model_from_result_object(self) -> None:
        state = {"file_results": [SimpleNamespace(model_id="canonical")]}

        assert _resolve_model_id(state, lambda _: "fallback") == "canonical"

    def test_skips_invalid_file_result_models(self) -> None:
        state = {"file_results": [{"model_id": 1}, {"model_id": "canonical"}], "requested_model": "requested"}

        assert _resolve_model_id(state, lambda _: "fallback") == "requested"

    def test_does_not_promote_mixed_file_result_models(self) -> None:
        state = {
            "file_results": [{"model_id": "first"}, {"model_id": "second"}],
            "requested_model": "requested",
        }

        assert _resolve_model_id(state, lambda _: "fallback") == "requested"

    def test_empty_file_results_fall_back_to_requested_model(self) -> None:
        state: dict[str, Any] = {"file_results": [], "requested_model": "gemini-3.7-flash"}

        assert _resolve_model_id(state, lambda _: "fallback") == "gemini-3.7-flash"

    def test_requested_model_takes_priority_over_model_config_raw_default(self) -> None:
        state = {
            "requested_model": "gemini-3.7-flash",
            "model_config_raw": {"default-model": "claude-opus-4.6"},
        }

        assert _resolve_model_id(state, lambda _: "fallback") == "gemini-3.7-flash"

    def test_falls_back_to_get_value_when_model_config_raw_missing(self) -> None:
        """Falls back to get_value('copilot.model_id') when model_config_raw absent."""
        state: dict[str, Any] = {}
        assert _resolve_model_id(state, lambda _: "gpt-4o") == "gpt-4o"

    def test_falls_back_to_get_value_when_default_model_empty(self) -> None:
        """Blank default-model is treated as absent."""
        state = {"model_config_raw": {"default-model": "  "}}
        assert _resolve_model_id(state, lambda _: "gpt-4o") == "gpt-4o"

    def test_falls_back_to_get_value_when_default_model_non_string(self) -> None:
        """Non-string default-model is treated as absent."""
        state = {"model_config_raw": {"default-model": 42}}
        assert _resolve_model_id(state, lambda _: "gpt-4o") == "gpt-4o"

    def test_falls_back_to_unknown_when_both_sources_empty(self) -> None:
        """Returns 'unknown' when both sources yield nothing."""
        state: dict[str, Any] = {}
        assert _resolve_model_id(state, lambda _: None) == "unknown"

    def test_falls_back_to_unknown_when_get_value_returns_empty_string(self) -> None:
        """Empty string from get_value is treated as absent."""
        state: dict[str, Any] = {}
        assert _resolve_model_id(state, lambda _: "") == "unknown"

    def test_strips_whitespace_from_model_config_raw(self) -> None:
        """Whitespace around the model name is stripped."""
        state = {"model_config_raw": {"default-model": "  claude-opus-4.6  "}}
        assert _resolve_model_id(state, lambda _: "gpt-4o") == "claude-opus-4.6"

    def test_strips_whitespace_from_get_value_fallback(self) -> None:
        """Whitespace around the fallback model name is stripped."""
        state: dict[str, Any] = {}
        assert _resolve_model_id(state, lambda _: "  gpt-4o  ") == "gpt-4o"

    def test_model_config_raw_not_dict_falls_through(self) -> None:
        """Non-dict model_config_raw is treated as absent."""
        state = {"model_config_raw": "not-a-dict"}
        assert _resolve_model_id(state, lambda _: "gpt-4o") == "gpt-4o"

    def test_get_value_returns_non_string_falls_to_unknown(self) -> None:
        """Non-string from get_value falls to unknown."""
        state: dict[str, Any] = {}
        assert _resolve_model_id(state, lambda _: 42) == "unknown"

    def test_langchain_engine_uses_resolved_provider_model(self) -> None:
        """For LangChain engine, uses effective_model from resolve_node_config."""

        def get_value_fn(key: str) -> str | None:
            if key == "review.engine":
                return "langchain"
            if key == "copilot.model_id":
                return "gemini-3.7-flash"
            return None

        mock_node_config = MagicMock()
        mock_node_config.effective_model = "gpt-4o"

        state: dict[str, Any] = {}
        with (
            patch(_PATCH_LOAD_CONFIG, return_value=MagicMock()),
            patch(_PATCH_RESOLVE_NODE_CONFIG, return_value=mock_node_config),
        ):
            result = _resolve_model_id(state, get_value_fn)

        assert result == "gpt-4o"

    def test_langchain_engine_provider_resolution_failure_falls_back_to_get_value(self) -> None:
        """If provider resolution raises, falls back to copilot.model_id."""

        def get_value_fn(key: str) -> str | None:
            if key == "review.engine":
                return "langchain"
            if key == "copilot.model_id":
                return "gemini-3.7-flash"
            return None

        state: dict[str, Any] = {}
        with patch(_PATCH_LOAD_CONFIG, side_effect=FileNotFoundError("no config")):
            result = _resolve_model_id(state, get_value_fn)

        assert result == "gemini-3.7-flash"

    def test_langchain_engine_empty_provider_model_falls_back_to_get_value(self) -> None:
        """If provider effective_model is blank, falls back to copilot.model_id."""

        def get_value_fn(key: str) -> str | None:
            if key == "review.engine":
                return "langchain"
            if key == "copilot.model_id":
                return "gemini-3.7-flash"
            return None

        mock_node_config = MagicMock()
        mock_node_config.effective_model = "  "

        state: dict[str, Any] = {}
        with (
            patch(_PATCH_LOAD_CONFIG, return_value=MagicMock()),
            patch(_PATCH_RESOLVE_NODE_CONFIG, return_value=mock_node_config),
        ):
            result = _resolve_model_id(state, get_value_fn)

        assert result == "gemini-3.7-flash"

    def test_non_langchain_engine_skips_provider_resolution(self) -> None:
        """For non-LangChain engine, provider resolution is not attempted."""

        def get_value_fn(key: str) -> str | None:
            if key == "review.engine":
                return "copilot"
            if key == "copilot.model_id":
                return "gpt-4o"
            return None

        state: dict[str, Any] = {}
        with patch(_PATCH_LOAD_CONFIG) as mock_load:
            result = _resolve_model_id(state, get_value_fn)

        mock_load.assert_not_called()
        assert result == "gpt-4o"

    def test_langchain_engine_forwards_llm_config_path_from_state(self) -> None:
        """llm_config_path from state is forwarded to load_config."""

        def get_value_fn(key: str) -> str | None:
            if key == "review.engine":
                return "langchain"
            return None

        mock_node_config = MagicMock()
        mock_node_config.effective_model = "gemini-3.7-flash"

        state: dict[str, Any] = {"llm_config_path": "/repo/.agdt/config/llm-providers.yml"}
        with (
            patch(_PATCH_LOAD_CONFIG, return_value=MagicMock()) as mock_load,
            patch(_PATCH_RESOLVE_NODE_CONFIG, return_value=mock_node_config),
        ):
            result = _resolve_model_id(state, get_value_fn)

        mock_load.assert_called_once_with("/repo/.agdt/config/llm-providers.yml")
        assert result == "gemini-3.7-flash"
