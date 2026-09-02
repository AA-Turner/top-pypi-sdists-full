"""Tests for ``validate_model_metadata``."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.config.project_config import validate_model_metadata

_FRESH_TIMESTAMP = (datetime.now(UTC) - timedelta(days=1)).replace(microsecond=0).isoformat()

_VALID_ENTRY = {
    "modelId": "claude-opus-4.8",
    "pricingStatus": "priceable",
    "surfaces": {
        "copilot": {"modelId": "claude-opus-4.8"},
        "vscode": {"displayName": "claude-opus-4.8"},
        "docs": {"displayName": "claude-opus-4.8"},
    },
    "inputRatePerM": 3,
    "outputRatePerM": 15,
    "currency": "USD",
    "rateUnit": "USD per 1M tokens",
    "assumedInputTokens": 100_000,
    "assumedOutputTokens": 10_000,
    "modelledSessionCost": "0.45",
    "priceCategory": "standard",
    "provenance": "curated",
    "costDataAsOf": _FRESH_TIMESTAMP,
}


class TestValidateModelMetadata:
    """Tests for model metadata schema validation."""

    def test_valid_entry_passes(self):
        validate_model_metadata(_VALID_ENTRY)

    def test_unavailable_entry_without_monetary_fields_passes(self):
        entry = {
            "modelId": "claude-sonnet-5",
            "pricingStatus": "unavailable",
            "surfaces": {
                "copilot": {"modelId": "claude-sonnet-5"},
                "vscode": {"displayName": "Claude Sonnet 5"},
                "docs": {"displayName": "Claude Sonnet 5"},
            },
            "priceCategory": "low",
            "unavailableReason": "missing",
            "provenance": "acp-live",
        }
        validate_model_metadata(entry)

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("pricingStatus", None),
            ("priceCategory", 1),
            ("provenance", ""),
            ("observedAt", ""),
            ("observedAt", "not-a-timestamp"),
            ("sourceMetadata", "bad"),
            ("unavailableReason", "other"),
        ],
    )
    def test_unavailable_entry_rejects_invalid_status_metadata(self, field, value):
        entry = {
            "modelId": "claude-sonnet-5",
            "pricingStatus": "unavailable",
            "surfaces": {
                "copilot": {"modelId": "claude-sonnet-5"},
                "vscode": {"displayName": "Claude Sonnet 5"},
                "docs": {"displayName": "Claude Sonnet 5"},
            },
        }
        if value is None:
            entry.pop(field)
        else:
            entry[field] = value
        with pytest.raises(ValueError):
            validate_model_metadata(entry)

    def test_priceable_entry_rejects_unavailable_reason(self):
        with pytest.raises(ValueError, match="only supported"):
            validate_model_metadata({**_VALID_ENTRY, "unavailableReason": "missing"})

    def test_non_priceable_status_is_reserved_for_auto(self):
        entry = {
            "modelId": "claude-sonnet-5",
            "pricingStatus": "non_priceable",
            "surfaces": {
                "copilot": {"modelId": "claude-sonnet-5"},
                "vscode": {"displayName": "Claude Sonnet 5"},
                "docs": {"displayName": "Claude Sonnet 5"},
            },
        }
        with pytest.raises(ValueError, match="reserved for routing"):
            validate_model_metadata(entry)

    def test_non_priceable_entry_rejects_unavailable_reason(self):
        entry = {
            "modelId": "auto",
            "pricingStatus": "non_priceable",
            "surfaces": {
                "copilot": {"modelId": "auto"},
                "vscode": {"displayName": "Auto"},
                "docs": {"displayName": "Auto"},
            },
            "priceCategory": "non_priceable",
            "unavailableReason": "missing",
        }
        with pytest.raises(ValueError, match="only supported"):
            validate_model_metadata(entry)

    def test_non_priceable_entry_rejects_monetary_fields(self):
        surfaces = {
            "copilot": {"modelId": "auto"},
            "vscode": {"displayName": "Auto"},
            "docs": {"displayName": "Auto"},
        }
        with pytest.raises(ValueError, match="cannot carry monetary fields"):
            validate_model_metadata(
                {**_VALID_ENTRY, "modelId": "auto", "surfaces": surfaces, "pricingStatus": "non_priceable"}
            )

    def test_auto_model_rejects_priceable_status(self):
        surfaces = {
            "copilot": {"modelId": "auto"},
            "vscode": {"displayName": "Auto"},
            "docs": {"displayName": "Auto"},
        }
        with pytest.raises(ValueError, match="routing options must use non_priceable status"):
            validate_model_metadata({**_VALID_ENTRY, "modelId": "auto", "surfaces": surfaces})

    def test_invalid_status_is_rejected(self):
        with pytest.raises(ValueError, match="pricingStatus must be one of"):
            validate_model_metadata({**_VALID_ENTRY, "pricingStatus": "unknown"})

    def test_non_dict_raises(self):
        with pytest.raises(ValueError, match="must be a dict"):
            validate_model_metadata("bad")

    def test_missing_non_cost_required_field_raises(self):
        with pytest.raises(ValueError, match="missing required field 'modelId'"):
            validate_model_metadata({"surfaces": {"copilot": {"modelId": "m"}}})

    def test_missing_cost_required_field_raises_with_missing_warning_tag(self):
        entry = dict(_VALID_ENTRY)
        entry.pop("costDataAsOf")
        with pytest.raises(ValueError, match="WARN_COST_DATA_MISSING"):
            validate_model_metadata(entry)

    def test_blank_model_id_raises(self):
        with pytest.raises(ValueError, match="modelId must be a non-empty string"):
            validate_model_metadata({**_VALID_ENTRY, "modelId": ""})

    def test_surfaces_not_dict_raises(self):
        with pytest.raises(ValueError, match="surfaces must be a mapping"):
            validate_model_metadata({**_VALID_ENTRY, "surfaces": "bad"})

    def test_unknown_surface_key_raises(self):
        with pytest.raises(ValueError, match="unsupported keys"):
            validate_model_metadata({**_VALID_ENTRY, "surfaces": {"other": {"modelId": "m"}}})

    def test_surface_value_not_dict_raises(self):
        with pytest.raises(ValueError, match="must map to a dict"):
            validate_model_metadata(
                {
                    **_VALID_ENTRY,
                    "surfaces": {
                        "copilot": "bad",
                        "vscode": {"displayName": "x"},
                        "docs": {"displayName": "x"},
                    },
                }
            )

    def test_empty_surface_value_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_model_metadata(
                {
                    **_VALID_ENTRY,
                    "surfaces": {
                        "copilot": {},
                        "vscode": {"displayName": "x"},
                        "docs": {"displayName": "x"},
                    },
                }
            )

    def test_missing_surface_keys_raises(self):
        with pytest.raises(ValueError, match="missing required keys"):
            validate_model_metadata({**_VALID_ENTRY, "surfaces": {"copilot": {"modelId": "x"}}})

    def test_surface_missing_identity_field_raises(self):
        with pytest.raises(ValueError, match="must contain a non-empty"):
            validate_model_metadata(
                {
                    **_VALID_ENTRY,
                    "surfaces": {
                        "copilot": {"displayName": "x"},
                        "vscode": {"displayName": "x"},
                        "docs": {"displayName": "x"},
                    },
                }
            )

    def test_surface_blank_identity_field_raises(self):
        with pytest.raises(ValueError, match="must contain a non-empty"):
            validate_model_metadata(
                {
                    **_VALID_ENTRY,
                    "surfaces": {
                        "copilot": {"modelId": "  "},
                        "vscode": {"displayName": "x"},
                        "docs": {"displayName": "x"},
                    },
                }
            )

    def test_copilot_surface_model_id_must_match_model_id(self):
        with pytest.raises(ValueError, match=r"surfaces\['copilot'\]\['modelId'\] must match modelId"):
            validate_model_metadata(
                {
                    **_VALID_ENTRY,
                    "surfaces": {
                        "copilot": {"modelId": "gpt-5-mini"},
                        "vscode": {"displayName": "x"},
                        "docs": {"displayName": "x"},
                    },
                }
            )

    def test_blank_currency_raises(self):
        with pytest.raises(ValueError, match="currency must be a non-empty string"):
            validate_model_metadata({**_VALID_ENTRY, "currency": "   "})

    def test_none_currency_raises(self):
        with pytest.raises(ValueError, match="currency must be a non-empty string"):
            validate_model_metadata({**_VALID_ENTRY, "currency": None})

    def test_blank_provenance_raises(self):
        with pytest.raises(ValueError, match="provenance must be a non-empty string"):
            validate_model_metadata({**_VALID_ENTRY, "provenance": ""})

    def test_blank_rate_unit_raises(self):
        with pytest.raises(ValueError, match="rateUnit must be a non-empty string"):
            validate_model_metadata({**_VALID_ENTRY, "rateUnit": "   "})

    def test_blank_price_category_raises(self):
        with pytest.raises(ValueError, match="priceCategory must be a non-empty string"):
            validate_model_metadata({**_VALID_ENTRY, "priceCategory": ""})

    def test_negative_input_rate_raises(self):
        with pytest.raises(ValueError, match="inputRatePerM must be non-negative"):
            validate_model_metadata({**_VALID_ENTRY, "inputRatePerM": -1, "modelledSessionCost": "-0.1"})

    def test_negative_output_rate_raises(self):
        with pytest.raises(ValueError, match="outputRatePerM must be non-negative"):
            validate_model_metadata({**_VALID_ENTRY, "outputRatePerM": -1, "modelledSessionCost": "-0.1"})

    def test_fractional_input_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedInputTokens must be a non-negative integer"):
            validate_model_metadata({**_VALID_ENTRY, "assumedInputTokens": 1.5, "modelledSessionCost": "0.00015015"})

    def test_negative_input_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedInputTokens must be a non-negative integer"):
            validate_model_metadata({**_VALID_ENTRY, "assumedInputTokens": -1})

    def test_negative_output_tokens_raises(self):
        with pytest.raises(ValueError, match="assumedOutputTokens must be a non-negative integer"):
            validate_model_metadata({**_VALID_ENTRY, "assumedOutputTokens": -1})

    def test_cost_mismatch_raises(self):
        with pytest.raises(ValueError, match="modelledSessionCost mismatch"):
            validate_model_metadata({**_VALID_ENTRY, "modelledSessionCost": "0.46"})

    def test_non_string_cost_raises(self):
        with pytest.raises(ValueError, match="modelledSessionCost must be a string"):
            validate_model_metadata({**_VALID_ENTRY, "modelledSessionCost": 0.45})

    def test_invalid_decimal_cost_raises(self):
        with pytest.raises(ValueError, match="not a valid decimal"):
            validate_model_metadata({**_VALID_ENTRY, "modelledSessionCost": "not-a-number"})

    def test_nan_cost_raises(self):
        with pytest.raises(ValueError, match="modelledSessionCost must be finite"):
            validate_model_metadata({**_VALID_ENTRY, "modelledSessionCost": "NaN"})

    def test_infinity_cost_raises(self):
        with pytest.raises(ValueError, match="modelledSessionCost must be finite"):
            validate_model_metadata({**_VALID_ENTRY, "modelledSessionCost": "Infinity"})

    def test_equivalent_decimal_representation_passes(self):
        validate_model_metadata({**_VALID_ENTRY, "modelledSessionCost": "0.450"})

    def test_priceable_entry_rejects_invalid_source_metadata(self):
        with pytest.raises(ValueError, match="sourceMetadata"):
            validate_model_metadata({**_VALID_ENTRY, "sourceMetadata": "bad"})

    def test_priceable_entry_rejects_invalid_observation_timestamp(self):
        with pytest.raises(ValueError):
            validate_model_metadata({**_VALID_ENTRY, "observedAt": "not-a-timestamp"})
