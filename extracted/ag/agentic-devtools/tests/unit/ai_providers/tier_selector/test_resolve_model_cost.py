from decimal import Decimal
from types import MappingProxyType
from typing import Any

import pytest

import agentic_devtools.ai_providers.tier_selector as tier_selector
from agentic_devtools.ai_providers.tier_selector import ModelCostError, resolve_model_cost


def _metadata(cost: str = "1.25") -> dict[str, object]:
    return {
        "modelId": "model-a",
        "surfaces": {
            "copilot": {"modelId": "model-a"},
            "vscode": {"displayName": "Model A"},
            "docs": {"displayName": "Model A"},
        },
        "inputRatePerM": 1,
        "outputRatePerM": 1,
        "currency": "USD",
        "rateUnit": "USD per 1M tokens",
        "assumedInputTokens": 0,
        "assumedOutputTokens": 1_250_000,
        "modelledSessionCost": cost,
        "priceCategory": "standard",
        "provenance": "fixture",
        "costDataAsOf": "2026-08-24T00:00:00+00:00",
    }


def test_resolve_model_cost_returns_exact_metadata_decimal() -> None:
    assert resolve_model_cost(_metadata()) == Decimal("1.25")
    assert resolve_model_cost(MappingProxyType(_metadata())) == Decimal("1.25")


@pytest.mark.parametrize("field_value", ["NaN", "-1.0", "not-a-number"])
def test_resolve_model_cost_rejects_invalid_cost(field_value: str) -> None:
    with pytest.raises(ModelCostError):
        resolve_model_cost(_metadata(field_value))


def test_resolve_model_cost_rejects_model_id_mismatch() -> None:
    metadata = _metadata()
    metadata["modelId"] = "other-model"
    with pytest.raises(ModelCostError, match="does not match"):
        resolve_model_cost("model-a", {"model-a": metadata})


def test_resolve_model_cost_rejects_unavailable_or_non_priceable_models() -> None:
    for model_id, status in (("model-a", "unavailable"), ("auto", "non_priceable")):
        with pytest.raises(ModelCostError, match="no usable monetary pricing"):
            resolve_model_cost(model_id, {model_id: {"modelId": model_id, "pricingStatus": status}})


def test_resolve_model_cost_rejects_invalid_pricing_status() -> None:
    with pytest.raises(ModelCostError, match="invalid pricing status"):
        resolve_model_cost("model-a", {"model-a": {"modelId": "model-a", "pricingStatus": "unknown"}})


def test_resolve_model_cost_rejects_legacy_rows_without_status_when_pricing_is_incomplete() -> None:
    with pytest.raises(ModelCostError, match="invalid pricing status"):
        resolve_model_cost(
            {
                "modelId": "model-a",
                "surfaces": {
                    "copilot": {"modelId": "model-a"},
                    "vscode": {"displayName": "Model A"},
                    "docs": {"displayName": "Model A"},
                },
                "modelledSessionCost": "1.25",
            }
        )


def test_resolve_model_cost_accepts_correct_model_id_and_mapping_entry() -> None:
    metadata = _metadata()
    explicit = _metadata()
    explicit["pricingStatus"] = "priceable"
    assert resolve_model_cost("model-a", {"model-a": metadata}) == Decimal("1.25")
    assert resolve_model_cost(metadata) == Decimal("1.25")
    assert resolve_model_cost(explicit) == Decimal("1.25")
    assert "pricingStatus" not in metadata


def test_resolve_model_cost_rejects_negative_cost_after_schema_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tier_selector, "validate_model_metadata", lambda entry: None)
    with pytest.raises(ModelCostError, match="invalid pricing status"):
        resolve_model_cost({"modelledSessionCost": Decimal("1.25")})
    with pytest.raises(ModelCostError):
        resolve_model_cost(_metadata("-1"))


def test_resolve_model_cost_wraps_schema_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def reject(entry: dict[str, Any]) -> None:
        raise ValueError("bad")

    monkeypatch.setattr(tier_selector, "validate_model_metadata", reject)
    with pytest.raises(ModelCostError, match="bad"):
        resolve_model_cost(_metadata())
