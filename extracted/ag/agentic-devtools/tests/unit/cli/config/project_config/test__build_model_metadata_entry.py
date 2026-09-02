"""Tests for ``_build_model_metadata_entry``."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from agentic_devtools.ai_providers.models import ModelRecord
from agentic_devtools.cli.config.project_config import (
    _build_model_metadata_entry,
    calculate_modelled_session_cost,
)


class TestBuildModelMetadataEntry:
    """Tests for canonical model-row normalization."""

    def test_builds_valid_entry_with_defaults(self):
        entry = _build_model_metadata_entry("claude-opus-4.8")
        assert entry["modelId"] == "claude-opus-4.8"
        assert set(entry["surfaces"]) == {"copilot", "vscode", "docs"}
        assert entry["currency"] == "USD"
        assert entry["provenance"] == "curated-catalog"
        assert "modelledSessionCost" in entry

    def test_preserves_existing_surfaces(self):
        existing = {
            "surfaces": {
                "copilot": {"modelId": "claude-opus-4.8"},
                "vscode": {"displayName": "Claude Opus 4.8"},
                "docs": {"displayName": "Claude Opus 4.8"},
            }
        }
        entry = _build_model_metadata_entry("claude-opus-4.8", existing_entry=existing)
        assert entry["surfaces"]["copilot"] == {"modelId": "claude-opus-4.8"}

    def test_non_string_model_id_raises(self):
        with pytest.raises(ValueError, match="model_id must be a string"):
            _build_model_metadata_entry(123)  # type: ignore[arg-type]

    def test_blank_model_id_raises(self):
        with pytest.raises(ValueError, match="model_id must not be blank"):
            _build_model_metadata_entry("   ")

    def test_invalid_surface_value_type_raises(self):
        with pytest.raises(ValueError, match=r"surfaces\[.*\] must map to a dict"):
            _build_model_metadata_entry("claude-opus-4.8", existing_entry={"surfaces": {"copilot": "bad"}})

    def test_empty_surface_dict_raises(self):
        with pytest.raises(ValueError, match=r"surfaces\[.*\] must not be empty"):
            _build_model_metadata_entry("claude-opus-4.8", existing_entry={"surfaces": {"copilot": {}}})

    def test_existing_entry_none_uses_defaults(self):
        entry = _build_model_metadata_entry("gpt-5-mini", existing_entry=None)
        assert entry["modelId"] == "gpt-5-mini"

    def test_existing_entry_non_dict_uses_defaults(self):
        entry = _build_model_metadata_entry("gpt-5-mini", existing_entry="bad")  # type: ignore[arg-type]
        assert entry["modelId"] == "gpt-5-mini"

    def test_uses_curated_surface_names(self):
        entry = _build_model_metadata_entry("claude-opus-4.8")
        assert entry["surfaces"]["copilot"] == {"modelId": "claude-opus-4.8"}
        assert entry["surfaces"]["vscode"]["displayName"] == "Claude Opus 4.8"
        assert entry["surfaces"]["docs"]["displayName"] == "Claude Opus 4.8"

    def test_auto_is_a_known_non_priceable_routing_option(self):
        entry = _build_model_metadata_entry("auto")
        assert entry["pricingStatus"] == "non_priceable"
        assert "inputRatePerM" not in entry

    def test_auto_normalization_discards_existing_priceable_fields(self):
        existing = _build_model_metadata_entry("claude-opus-4.8")
        existing["modelId"] = "auto"
        existing["surfaces"]["copilot"]["modelId"] = "auto"
        entry = _build_model_metadata_entry("auto", existing_entry=existing)
        assert entry["pricingStatus"] == "non_priceable"
        assert entry["priceCategory"] == "non_priceable"
        assert entry["provenance"] == "static-catalog"
        assert "inputRatePerM" not in entry
        assert "modelledSessionCost" not in entry

    def test_auto_normalization_ignores_malformed_live_pricing_without_warning(self, capsys):
        record = ModelRecord(
            name="Auto",
            model_id="auto",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "auto",
                "inputRatePerM": 1,
                "_meta": {"copilotPriceCategory": "low"},
            },
            source="acp-live",
        )
        entry = _build_model_metadata_entry("auto", acp_record=record)
        assert entry["pricingStatus"] == "non_priceable"
        assert entry["priceCategory"] == "non_priceable"
        assert entry["provenance"] == "static-catalog"
        assert "inputRatePerM" not in entry
        assert "WARN_COST_DATA_INVALID" not in capsys.readouterr().err

    def test_fractional_token_count_raises(self):
        with pytest.raises(ValueError, match="assumedInputTokens must be a non-negative integer"):
            _build_model_metadata_entry("claude-opus-4.8", existing_entry={"assumedInputTokens": 1.5})

    def test_boolean_token_count_raises(self):
        with pytest.raises(ValueError, match="not boolean"):
            _build_model_metadata_entry("claude-opus-4.8", existing_entry={"assumedInputTokens": True})

    def test_ad_hoc_key_in_existing_entry_is_stripped(self):
        """Unknown fields in existing_entry are excluded from the canonical output."""
        fresh = (datetime.now(UTC) - timedelta(days=1)).replace(microsecond=0).isoformat()
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            existing_entry={"someUnknownKey": "should-not-survive", "costDataAsOf": fresh},
        )
        assert "someUnknownKey" not in entry

    def test_existing_entry_model_id_mismatch_raises(self):
        with pytest.raises(ValueError, match="existing modelId .* does not match normalized model id"):
            _build_model_metadata_entry(
                "claude-opus-4.8",
                existing_entry={"modelId": "gpt-5-mini"},
            )

    def test_existing_entry_copilot_surface_model_id_mismatch_raises(self):
        with pytest.raises(ValueError, match=r"surfaces\['copilot'\]\['modelId'\].*does not match normalized model id"):
            _build_model_metadata_entry(
                "claude-opus-4.8",
                existing_entry={"surfaces": {"copilot": {"modelId": "gpt-5-mini"}}},
            )

    def test_non_catalog_model_with_complete_curated_data_is_preserved(self):
        """A model not in MODEL_CATALOG is accepted when its existing entry supplies all catalog fields."""
        fresh_timestamp = (datetime.now(UTC) - timedelta(days=1)).replace(microsecond=0).isoformat()
        entry = _build_model_metadata_entry(
            "custom-model-x",
            existing_entry={
                "surfaces": {
                    "copilot": {"modelId": "custom-model-x"},
                    "vscode": {"displayName": "Custom Model X"},
                    "docs": {"displayName": "Custom Model X"},
                },
                "inputRatePerM": 5.0,
                "outputRatePerM": 20.0,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100_000,
                "assumedOutputTokens": 10_000,
                "priceCategory": "standard",
                "provenance": "curated",
                "costDataAsOf": fresh_timestamp,
            },
        )
        assert entry["modelId"] == "custom-model-x"
        assert entry["inputRatePerM"] == 5.0
        assert "modelledSessionCost" in entry

    def test_live_record_pricing_and_metadata_take_precedence(self):
        record = ModelRecord(
            name="Live Name",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "future-model",
                "name": "Live Name",
                "inputRatePerM": 1,
                "outputRatePerM": 2,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100,
                "assumedOutputTokens": 10,
                "costDataAsOf": "2026-08-27T00:00:00+00:00",
                "_meta": {"copilotPriceCategory": "low", "copilotUsage": "0.33x"},
            },
            source="acp-live",
            observed_at="2026-08-28T00:00:00+00:00",
        )
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "acp-live"
        assert entry["priceCategory"] == "low"
        assert entry["sourceMetadata"]["acp"]["copilotUsage"] == "0.33x"
        assert entry["observedAt"] == "2026-08-28T00:00:00+00:00"

    def test_live_pricing_recomputes_stale_derived_cost_from_existing_entry(self):
        existing = _build_model_metadata_entry("claude-opus-4.8")
        existing["modelId"] = "future-model"
        existing["surfaces"]["copilot"]["modelId"] = "future-model"
        existing["modelledSessionCost"] = "999.00"
        record = ModelRecord(
            name="Live Name",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "future-model",
                "name": "Live Name",
                "inputRatePerM": 1,
                "outputRatePerM": 2,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100,
                "assumedOutputTokens": 10,
                "costDataAsOf": "2026-08-27T00:00:00+00:00",
                "_meta": {"copilotPriceCategory": "low", "copilotUsage": "0.33x"},
            },
            source="acp-live",
            observed_at="2026-08-28T00:00:00+00:00",
        )
        entry = _build_model_metadata_entry("future-model", existing_entry=existing, acp_record=record)
        assert entry["modelledSessionCost"] == calculate_modelled_session_cost("1", "2", 100, 10)
        assert entry["modelledSessionCost"] != "999.00"

    def test_live_name_repairs_non_mapping_surface_values_and_merges_source_metadata(self):
        record = ModelRecord(
            name="Live Name",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "future-model",
                "name": "Live Name",
                "_meta": {"copilotEnablement": "enabled"},
            },
        )
        entry = _build_model_metadata_entry(
            "future-model",
            existing_entry={
                "surfaces": {"vscode": "bad", "docs": []},
                "sourceMetadata": {"existing": True},
            },
            acp_record=record,
        )
        assert entry["surfaces"]["vscode"]["displayName"] == "Live Name"
        assert entry["sourceMetadata"]["existing"] is True
        assert entry["sourceMetadata"]["acp"]["copilotEnablement"] == "enabled"

    def test_category_only_live_record_falls_back_to_existing_price(self):
        record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "future-model", "_meta": {"copilotPriceCategory": "low"}},
        )
        existing = _build_model_metadata_entry("claude-opus-4.8")
        existing["modelId"] = "future-model"
        existing["surfaces"]["copilot"]["modelId"] = "future-model"
        entry = _build_model_metadata_entry("future-model", existing_entry=existing, acp_record=record)
        assert entry["pricingStatus"] == "priceable"
        assert entry["priceCategory"] == "low"

    def test_category_only_live_record_falls_back_to_cached_acp_pricing_before_catalog(self):
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
        entry = _build_model_metadata_entry(
            "future-model",
            acp_record=live_record,
            acp_cache_record=cached_record,
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "acp-cache"
        assert entry["priceCategory"] == "low"

    def test_cached_acp_price_category_used_when_live_meta_is_absent(self):
        """Cached _meta copilotPriceCategory flows through when live record has no _meta."""
        live_record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "future-model"},
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
                "_meta": {"copilotPriceCategory": "standard"},
            },
            source="acp-cache",
        )
        entry = _build_model_metadata_entry(
            "future-model",
            acp_record=live_record,
            acp_cache_record=cached_record,
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "acp-cache"
        assert entry["priceCategory"] == "standard"
        assert entry["sourceMetadata"]["acp"].get("copilotPriceCategory") == "standard"

    def test_cached_acp_pricing_uses_cached_price_category_when_live_record_is_absent(self):
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
                "_meta": {"copilotPriceCategory": "low"},
            },
            source="acp-cache",
        )
        entry = _build_model_metadata_entry("future-model", acp_cache_record=cached_record)
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "acp-cache"
        assert entry["priceCategory"] == "low"

    def test_cached_acp_pricing_without_cache_meta_defaults_price_category_to_unknown(self):
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
        entry = _build_model_metadata_entry("future-model", acp_cache_record=cached_record)
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "acp-cache"
        assert entry["priceCategory"] == "unknown"

    def test_catalog_fallback_preserves_acp_unavailable_status_metadata(self):
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            existing_entry={
                "pricingStatus": "unavailable",
                "priceCategory": "low",
                "unavailableReason": "invalid",
                "provenance": "acp-live",
                "sourceMetadata": {"acp": {"copilotPriceCategory": "low"}},
            },
        )
        assert entry["pricingStatus"] == "unavailable"
        assert entry["priceCategory"] == "low"
        assert entry["unavailableReason"] == "invalid"
        assert entry["provenance"] == "acp-live"

    def test_catalog_fallback_does_not_preserve_stale_invalid_when_new_acp_record_is_present(self):
        """A fresh ACP observation with no monetary pricing must not keep a stale invalid marker."""
        record = SimpleNamespace(
            name="Claude Opus 4.8",
            model_id="claude-opus-4.8",
            raw_metadata={"modelId": "claude-opus-4.8"},
            source="acp-live",
        )
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            existing_entry={
                "pricingStatus": "unavailable",
                "priceCategory": "low",
                "unavailableReason": "invalid",
                "provenance": "acp-cache",
            },
            acp_record=record,
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "curated-catalog"
        assert "unavailableReason" not in entry

    def test_catalog_fallback_upgrades_project_config_unavailable_status_metadata(self):
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            existing_entry={
                "pricingStatus": "unavailable",
                "priceCategory": None,
                "provenance": "project-config",
            },
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["priceCategory"] == "standard"
        assert entry["provenance"] == "curated-catalog"

    def test_catalog_fallback_upgrades_unavailable_when_only_source_metadata_marks_acp(self):
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            existing_entry={
                "pricingStatus": "unavailable",
                "priceCategory": None,
                "provenance": "project-config",
                "sourceMetadata": {"source": "acp-cache"},
            },
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "curated-catalog"

    def test_invalid_live_pricing_becomes_unavailable(self, capsys):
        record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "future-model", "inputRatePerM": -1},
            source="acp-cache",
        )
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "invalid"
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_acp_model_id_mismatch_raises(self):
        record = ModelRecord(
            name="Future",
            model_id="other-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "other-model"},
        )
        with pytest.raises(ValueError, match="ACP model_id"):
            _build_model_metadata_entry("future-model", acp_record=record)

    def test_acp_cache_model_id_mismatch_raises(self):
        record = ModelRecord(
            name="Future",
            model_id="other-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "other-model"},
            source="acp-cache",
        )
        with pytest.raises(ValueError, match="ACP cache model_id"):
            _build_model_metadata_entry("future-model", acp_cache_record=record)

    def test_cached_acp_pricing_fallback_ignores_non_mapping_raw_metadata(self):
        live_record = ModelRecord(
            name="Claude Opus 4.8",
            model_id="claude-opus-4.8",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "claude-opus-4.8", "_meta": {"copilotPriceCategory": "standard"}},
            source="acp-live",
        )
        cached_record = SimpleNamespace(model_id="claude-opus-4.8", raw_metadata=None, source="acp-cache")
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            acp_record=live_record,
            acp_cache_record=cached_record,
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "curated-catalog"

    def test_malformed_cache_pricing_fails_closed_with_warning(self, capsys):
        """A cache record with malformed monetary fields fails closed to unavailable, not priceable."""
        live_record = ModelRecord(
            name="Claude Opus 4.8",
            model_id="claude-opus-4.8",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "claude-opus-4.8", "_meta": {"copilotPriceCategory": "standard"}},
            source="acp-live",
        )
        invalid_cached_record = ModelRecord(
            name="Claude Opus 4.8",
            model_id="claude-opus-4.8",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "claude-opus-4.8", "inputRatePerM": -1},
            source="acp-cache",
        )
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            acp_record=live_record,
            acp_cache_record=invalid_cached_record,
        )
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "invalid"
        assert entry["provenance"] == "acp-cache"
        err = capsys.readouterr().err
        assert "WARN_COST_DATA_INVALID" in err
        assert "source=acp-cache" in err

    def test_category_only_cache_pricing_falls_through_to_catalog(self):
        """A cache record with only category metadata (no monetary fields) falls through to catalog."""
        live_record = ModelRecord(
            name="Claude Opus 4.8",
            model_id="claude-opus-4.8",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "claude-opus-4.8", "_meta": {"copilotPriceCategory": "standard"}},
            source="acp-live",
        )
        incomplete_cached_record = ModelRecord(
            name="Claude Opus 4.8",
            model_id="claude-opus-4.8",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "claude-opus-4.8", "_meta": {"copilotPriceCategory": "low"}},
            source="acp-cache",
        )
        entry = _build_model_metadata_entry(
            "claude-opus-4.8",
            acp_record=live_record,
            acp_cache_record=incomplete_cached_record,
        )
        assert entry["pricingStatus"] == "priceable"
        assert entry["provenance"] == "curated-catalog"

    def test_blank_copilot_price_category_in_live_record_falls_back_to_unknown(self):
        record = ModelRecord(
            name="Live Name",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "future-model",
                "name": "Live Name",
                "inputRatePerM": 1,
                "outputRatePerM": 2,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100,
                "assumedOutputTokens": 10,
                "costDataAsOf": "2026-08-27T00:00:00+00:00",
                "_meta": {"copilotPriceCategory": "   "},
            },
            source="acp-live",
            observed_at=None,
        )
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "priceable"
        assert entry["priceCategory"] == "unknown"

    def test_non_string_copilot_price_category_in_live_record_falls_back_to_unknown(self):
        record = ModelRecord(
            name="Live Name",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={
                "modelId": "future-model",
                "name": "Live Name",
                "inputRatePerM": 1,
                "outputRatePerM": 2,
                "currency": "USD",
                "rateUnit": "USD per 1M tokens",
                "assumedInputTokens": 100,
                "assumedOutputTokens": 10,
                "costDataAsOf": "2026-08-27T00:00:00+00:00",
                "_meta": {"copilotPriceCategory": 42},
            },
            source="acp-live",
            observed_at=None,
        )
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "priceable"
        assert entry["priceCategory"] == "unknown"

    def test_record_without_mapping_metadata_is_unavailable(self):
        record = SimpleNamespace(name="Future", model_id="future-model", raw_metadata=None, source="acp-live")
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "missing"

    def test_blank_copilot_price_category_in_invalid_pricing_normalizes_to_none(self):
        """A blank copilotPriceCategory on an acp_invalid unavailable row must not propagate raw."""
        record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "future-model", "inputRatePerM": -1, "_meta": {"copilotPriceCategory": "   "}},
            source="acp-live",
        )
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["priceCategory"] is None
        assert entry["unavailableReason"] == "invalid"

    def test_non_string_copilot_price_category_in_invalid_pricing_normalizes_to_none(self):
        """A non-string copilotPriceCategory on an acp_invalid unavailable row must not propagate raw."""
        record = ModelRecord(
            name="Future",
            model_id="future-model",
            provider="copilot",
            context_window=128000,
            max_output_tokens=None,
            supports_tools=True,
            raw_metadata={"modelId": "future-model", "inputRatePerM": -1, "_meta": {"copilotPriceCategory": 42}},
            source="acp-live",
        )
        entry = _build_model_metadata_entry("future-model", acp_record=record)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["priceCategory"] is None
        assert entry["unavailableReason"] == "invalid"

    def test_live_acp_record_replaces_stale_cache_provenance_on_unavailable_row(self):
        """When a live ACP record is present but has no pricing, provenance must reflect the
        live source even if a previously cached unavailable row had a different provenance."""
        existing = {
            "modelId": "future-model",
            "pricingStatus": "unavailable",
            "priceCategory": None,
            "provenance": "acp-cache",
        }
        record = SimpleNamespace(name="Future", model_id="future-model", raw_metadata=None, source="acp-live")
        entry = _build_model_metadata_entry("future-model", existing_entry=existing, acp_record=record)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["provenance"] == "acp-live"
        assert entry["unavailableReason"] == "missing"

    def test_no_catalog_acp_invalid_reason_preserved_without_acp_record(self):
        """An ACP-invalid row not in the catalog must retain unavailableReason 'invalid' when
        no live ACP record is supplied so the fail-closed marker survives subsequent loads."""
        existing = {
            "modelId": "future-model",
            "pricingStatus": "unavailable",
            "priceCategory": None,
            "unavailableReason": "invalid",
            "provenance": "acp-live",
        }
        entry = _build_model_metadata_entry("future-model", existing_entry=existing)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "invalid"
        assert entry["provenance"] == "acp-live"

    def test_no_catalog_acp_cache_invalid_reason_preserved_without_acp_record(self):
        """Same preservation applies when the persisted row has 'acp-cache' provenance."""
        existing = {
            "modelId": "future-model",
            "pricingStatus": "unavailable",
            "priceCategory": "low",
            "unavailableReason": "invalid",
            "provenance": "acp-cache",
        }
        entry = _build_model_metadata_entry("future-model", existing_entry=existing)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "invalid"
        assert entry["provenance"] == "acp-cache"

    def test_no_catalog_non_acp_invalid_reason_normalised_to_missing(self):
        """A project-config row with unavailableReason 'invalid' must be normalised to 'missing'
        by the no-catalog path, confirming the preservation guard is scoped to ACP sources only."""
        existing = {
            "modelId": "future-model",
            "pricingStatus": "unavailable",
            "priceCategory": None,
            "unavailableReason": "invalid",
            "provenance": "project-config",
        }
        entry = _build_model_metadata_entry("future-model", existing_entry=existing)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "missing"

    def test_no_catalog_fresh_acp_record_replaces_stale_invalid_reason_with_missing(self):
        """A new ACP record without monetary pricing must replace stale invalid with missing."""
        existing = {
            "modelId": "future-model",
            "pricingStatus": "unavailable",
            "priceCategory": None,
            "unavailableReason": "invalid",
            "provenance": "acp-cache",
        }
        record = SimpleNamespace(
            name="Future",
            model_id="future-model",
            raw_metadata={"modelId": "future-model"},
            source="acp-live",
        )
        entry = _build_model_metadata_entry("future-model", existing_entry=existing, acp_record=record)
        assert entry["pricingStatus"] == "unavailable"
        assert entry["unavailableReason"] == "missing"
        assert entry["provenance"] == "acp-live"
