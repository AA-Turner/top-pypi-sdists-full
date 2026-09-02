"""Tests for _populate_available_models."""

from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.ai_providers.models import ModelRecord
from agentic_devtools.cli.setup.commands import _populate_available_models

_QUERY = "agentic_devtools.cli.setup.commands._query_copilot_model_records"
_LOAD = "agentic_devtools.cli.config.project_config.load_project_config"
_SAVE = "agentic_devtools.cli.config.project_config.save_project_config"


def _records(*model_ids: str) -> list[ModelRecord]:
    return [
        ModelRecord(
            name=model_id,
            model_id=model_id,
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": model_id},
        )
        for model_id in model_ids
    ]


class TestPopulateAvailableModels:
    """Tests for _populate_available_models."""

    def test_populates_when_absent(self, capsys):
        """Queries and writes availableModels when the key is absent."""
        with patch(_QUERY, return_value=_records("m1", "m2")):
            with patch(_LOAD, return_value={}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        saved = mock_save.call_args[0][0]
        assert saved["availableModels"] == ["m1", "m2"]

    def test_preserves_existing_keys_when_populating(self, capsys):
        """Existing config keys are preserved when caching the inventory."""
        with patch(_QUERY, return_value=_records("m1")):
            with patch(_LOAD, return_value={"default_copilot_model": "m1"}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "m1"
        assert saved["availableModels"] == ["m1"]

    def test_refreshes_by_default_even_when_cached(self, capsys):
        """Discovery runs on every setup run and overwrites the cached inventory."""
        with patch(_QUERY, return_value=_records("fresh")) as mock_query:
            with patch(_LOAD, return_value={"availableModels": ["cached"]}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        mock_query.assert_called_once_with(refresh=True, allow_stale=False)
        assert mock_save.call_args[0][0]["availableModels"] == ["fresh"]

    def test_skips_discovery_when_refresh_is_disabled_and_cached(self, capsys):
        """--no-refresh-models keeps a valid cached inventory without discovery."""
        with patch(_QUERY) as mock_query:
            with patch(_LOAD, return_value={"availableModels": ["cached"]}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models(refresh_models=False)
        mock_query.assert_not_called()
        mock_save.assert_not_called()
        assert "--no-refresh-models" in capsys.readouterr().out

    def test_reads_the_cache_when_refresh_is_disabled_and_inventory_missing(self, capsys):
        """--no-refresh-models still fills a missing inventory from the discovery cache."""
        with patch(_QUERY, return_value=_records("cached-model")) as mock_query:
            with patch(_LOAD, return_value={}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models(refresh_models=False)
        mock_query.assert_called_once_with(refresh=False, allow_stale=True)
        assert mock_save.call_args[0][0]["availableModels"] == ["cached-model"]

    def test_keeps_the_cached_inventory_when_discovery_returns_nothing(self, capsys):
        """An offline discovery failure never clears or fails the cached inventory."""
        with patch(_QUERY, return_value=[]):
            with patch(_LOAD, return_value={"availableModels": ["cached"]}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        mock_save.assert_not_called()
        assert "keeping the cached availableModels inventory" in capsys.readouterr().out

    def test_continues_without_inventory_when_nothing_is_available(self, capsys):
        """An empty inventory is reported as a warning and never fails setup."""
        with patch(_QUERY, return_value=[]):
            with patch(_LOAD, return_value={}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        mock_save.assert_not_called()
        assert "availableModels remains empty" in capsys.readouterr().out

    def test_refreshes_even_when_cached(self, capsys):
        """Re-queries and overwrites the cached inventory when it already exists."""
        with patch(_QUERY, return_value=_records("new1", "new2")):
            with patch(_LOAD, return_value={"availableModels": ["old"]}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        saved = mock_save.call_args[0][0]
        assert saved["availableModels"] == ["new1", "new2"]

    def test_no_refresh_keeps_valid_inventory_when_cached(self, capsys):
        """--no-refresh-models keeps a valid inventory without discovery."""
        with patch(_QUERY) as mock_query:
            with patch(_LOAD, return_value={"availableModels": ["cached"]}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models(refresh_models=False)
        mock_query.assert_not_called()
        mock_save.assert_not_called()
        assert "--no-refresh-models" in capsys.readouterr().out

    def test_one_record_query_populates_inventory_and_metadata(self):
        """The same ACP records populate ordered IDs and normalized pricing metadata."""
        record = ModelRecord(
            name="Live Model",
            model_id="live-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "live-model",
                "name": "Live Model",
                "inputRatePerM": 1,
                "outputRatePerM": 2,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100,
                "assumedOutputTokens": 10,
                "costDataAsOf": "2026-08-27T00:00:00+00:00",
                "_meta": {"copilotPriceCategory": "standard"},
            },
            raw_metadata_verbatim=True,
            source="acp-live",
        )
        with patch(_QUERY, return_value=[record]) as mock_query:
            with patch(_LOAD, return_value={}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()
        saved = mock_save.call_args[0][0]
        assert saved["availableModels"] == ["live-model"]
        assert saved["models"]["live-model"]["pricingStatus"] == "priceable"
        assert saved["models"]["live-model"]["provenance"] == "acp-live"
        mock_query.assert_called_once_with(refresh=True, allow_stale=False)

    def test_refresh_preserves_prerefresh_cache_for_pricing_fallback(self):
        live_record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "future-model", "_meta": {"copilotPriceCategory": "low"}},
            source="acp-live",
        )
        cached_record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "future-model",
                "inputRatePerM": 1,
                "outputRatePerM": 2,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100,
                "assumedOutputTokens": 10,
                "costDataAsOf": "2026-08-27T00:00:00+00:00",
            },
            source="acp-cache",
        )
        with patch(
            "agentic_devtools.ai_providers.copilot_discovery.read_model_cache", return_value=[cached_record]
        ) as mock_cache:
            with patch(_QUERY, return_value=[live_record]):
                with patch(_LOAD, return_value={}):
                    with patch(_SAVE) as mock_save:
                        _populate_available_models()
        saved = mock_save.call_args[0][0]
        assert saved["models"]["future-model"]["pricingStatus"] == "priceable"
        assert saved["models"]["future-model"]["provenance"] == "acp-cache"
        assert saved["models"]["future-model"]["priceCategory"] == "low"
        mock_cache.assert_called_once_with(allow_stale=False)

    def test_refresh_ignores_prerefresh_cache_records_without_usable_model_ids(self):
        live_record = ModelRecord(
            name="Model A",
            model_id="model-a",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "model-a"},
            source="acp-live",
        )
        with patch(
            "agentic_devtools.ai_providers.copilot_discovery.read_model_cache",
            return_value=[SimpleNamespace(model_id="   ")],
        ):
            with patch(_QUERY, return_value=[live_record]):
                with patch(_LOAD, return_value={}):
                    with patch(_SAVE):
                        with patch(
                            "agentic_devtools.cli.config.project_config._build_model_metadata_entry"
                        ) as mock_build:
                            mock_build.return_value = {
                                "modelId": "model-a",
                                "pricingStatus": "unavailable",
                                "surfaces": {
                                    "copilot": {"modelId": "model-a"},
                                    "vscode": {"displayName": "Model A"},
                                    "docs": {"displayName": "Model A"},
                                },
                                "priceCategory": None,
                                "provenance": "acp-live",
                            }
                            _populate_available_models()
        assert mock_build.call_args.kwargs["acp_cache_record"] is None

    def test_filters_unusable_records_without_creating_models_tree(self):
        with patch(_QUERY, return_value=[SimpleNamespace(model_id="  ")]):
            with patch(_LOAD, return_value={}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()

        saved = mock_save.call_args[0][0]
        assert saved["availableModels"] == []
        assert "models" not in saved

    def test_deduplicates_record_ids_after_normalizing_whitespace(self):
        with patch(_QUERY, return_value=_records(" model-a ", "model-a")):
            with patch(_LOAD, return_value={}):
                with patch(_SAVE) as mock_save:
                    _populate_available_models()

        assert mock_save.call_args[0][0]["availableModels"] == ["model-a"]

    def test_suppresses_pre_save_cost_warnings_during_setup_normalization(self):
        record = ModelRecord(
            name="Catalog Model",
            model_id="claude-opus-4.8",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "claude-opus-4.8"},
        )
        with patch(_QUERY, return_value=[record]):
            with patch(_LOAD, return_value={"models": {}}):
                with patch(_SAVE):
                    with patch(
                        "agentic_devtools.cli.config.project_config._build_model_metadata_entry"
                    ) as mock_build_entry:
                        mock_build_entry.return_value = {
                            "modelId": "claude-opus-4.8",
                            "pricingStatus": "priceable",
                            "surfaces": {
                                "copilot": {"modelId": "claude-opus-4.8"},
                                "vscode": {"displayName": "Claude Opus 4.8"},
                                "docs": {"displayName": "Claude Opus 4.8"},
                            },
                            "inputRatePerM": "3",
                            "outputRatePerM": "15",
                            "currency": "USD",
                            "rateUnit": "USD per 1M tokens",
                            "assumedInputTokens": 100000,
                            "assumedOutputTokens": 10000,
                            "modelledSessionCost": "0.45",
                            "priceCategory": "standard",
                            "provenance": "curated-catalog",
                            "costDataAsOf": "2026-08-01T00:00:00+00:00",
                        }
                        _populate_available_models()
        assert mock_build_entry.call_args.kwargs["emit_warnings"] is False
