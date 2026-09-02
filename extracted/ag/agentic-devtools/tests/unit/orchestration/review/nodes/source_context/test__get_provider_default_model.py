"""Tests for _get_provider_default_model helper."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.review.nodes.source_context import _get_provider_default_model


class TestGetProviderDefaultModel:
    """Tests for _get_provider_default_model."""

    def test_returns_provider_model_attribute(self) -> None:
        """Returns the provider's _model attribute when set."""
        mock_provider = MagicMock()
        mock_provider._model = "gpt-4o"
        with patch(
            "agentic_devtools.orchestration.llm.factory.get_provider",
            return_value=mock_provider,
        ):
            result = _get_provider_default_model()
        assert result == "gpt-4o"

    def test_returns_none_when_model_attribute_absent(self) -> None:
        """Returns None when the provider has no _model attribute."""
        mock_provider = MagicMock(spec=[])
        with patch(
            "agentic_devtools.orchestration.llm.factory.get_provider",
            return_value=mock_provider,
        ):
            result = _get_provider_default_model()
        assert result is None

    def test_returns_none_when_model_attribute_is_empty_string(self) -> None:
        """Returns None when _model is an empty or whitespace-only string."""
        mock_provider = MagicMock()
        mock_provider._model = "   "
        with patch(
            "agentic_devtools.orchestration.llm.factory.get_provider",
            return_value=mock_provider,
        ):
            result = _get_provider_default_model()
        assert result is None

    def test_returns_none_on_get_provider_exception(self) -> None:
        """Returns None when get_provider raises (e.g., not configured)."""
        with patch(
            "agentic_devtools.orchestration.llm.factory.get_provider",
            side_effect=RuntimeError("provider not configured"),
        ):
            result = _get_provider_default_model()
        assert result is None

    def test_returns_none_on_import_error(self) -> None:
        """Returns None when get_provider cannot be imported."""
        import sys

        with patch.dict(sys.modules, {"agentic_devtools.orchestration.llm.factory": None}):
            result = _get_provider_default_model()
        assert result is None

    def test_forwards_config_path_to_load_config(self) -> None:
        """config_path is forwarded to load_config so both preflight and node use the same snapshot."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        mock_snapshot = LLMConfigSnapshot()
        mock_provider = MagicMock()
        mock_provider._model = "gemini-3.7-flash"

        with (
            patch(
                "agentic_devtools.orchestration.llm.config.load_config",
                return_value=mock_snapshot,
            ) as mock_load_config,
            patch(
                "agentic_devtools.orchestration.llm.factory.get_provider",
                return_value=mock_provider,
            ) as mock_get_provider,
        ):
            result = _get_provider_default_model("/repo/.agdt/config/llm-providers.yml")

        assert result == "gemini-3.7-flash"
        mock_load_config.assert_called_once_with("/repo/.agdt/config/llm-providers.yml")
        mock_get_provider.assert_called_once_with("review_files", "pr_review", config=mock_snapshot)

    def test_uses_none_config_path_by_default(self) -> None:
        """Omitting config_path passes None to load_config (CWD-relative default)."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        mock_snapshot = LLMConfigSnapshot()
        mock_provider = MagicMock()
        mock_provider._model = "gpt-4o"

        with (
            patch(
                "agentic_devtools.orchestration.llm.config.load_config",
                return_value=mock_snapshot,
            ) as mock_load_config,
            patch(
                "agentic_devtools.orchestration.llm.factory.get_provider",
                return_value=mock_provider,
            ),
        ):
            result = _get_provider_default_model()

        assert result == "gpt-4o"
        mock_load_config.assert_called_once_with(None)
