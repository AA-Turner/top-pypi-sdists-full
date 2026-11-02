from decimal import Decimal

import pytest

from agentic_devtools.ai_providers.priors import (
    PRIORS_VERSION,
    PriorSet,
    PriorValidationError,
    resolve_prior,
)


def test_resolve_prior_uses_versioned_defaults_and_precedence() -> None:
    priors = PriorSet(
        model_overrides={"model-a": Decimal("1")},
        tier_overrides={"tier-1": Decimal("0.8")},
    )
    assert PRIORS_VERSION == "2026-08-01"
    assert resolve_prior("model-a", "tier-1", priors) == Decimal("1")
    assert resolve_prior("model-b", "tier-1", priors) == Decimal("0.8")
    assert resolve_prior("model-b", "tier-2", priors) == Decimal("0.70")


@pytest.mark.parametrize("value", [True, False, Decimal("-0.1"), Decimal("1.1"), "NaN", "Infinity"])
def test_resolve_prior_rejects_invalid_values(value: object) -> None:
    priors = PriorSet(model_overrides={"model-a": value})
    with pytest.raises(PriorValidationError):
        resolve_prior("model-a", "tier-1", priors)


@pytest.mark.parametrize("value", ["0.5", 0.5, 0.7])
def test_resolve_prior_rejects_string_and_float_inputs(value: object) -> None:
    priors = PriorSet(model_overrides={"model-a": value})
    with pytest.raises(PriorValidationError):
        resolve_prior("model-a", "tier-1", priors)


def test_resolve_prior_accepts_probability_endpoints() -> None:
    assert resolve_prior("model-a", "tier-1", PriorSet(model_overrides={"model-a": 0})) == Decimal("0")
    assert resolve_prior("model-b", "tier-1", PriorSet(tier_overrides={"tier-1": 1})) == Decimal("1")


@pytest.mark.parametrize(
    ("model_id", "tier", "prior_set"),
    [
        ("", "tier-1", PriorSet()),
        ("model-a", "", PriorSet()),
        ("model-a", "tier-1", object()),
        ("model-a", "tier-1", {}),
        ("model-a", "tier-1", False),
        ("model-a", "tier-9", PriorSet(tier_defaults={})),
    ],
)
def test_resolve_prior_rejects_invalid_configuration(model_id: str, tier: str, prior_set: object) -> None:
    with pytest.raises(PriorValidationError):
        resolve_prior(model_id, tier, prior_set)  # type: ignore[arg-type]


@pytest.mark.parametrize("kwargs", [{"model_overrides": []}, {"tier_overrides": []}])
def test_resolve_prior_rejects_non_mapping_overrides(kwargs: dict[str, object]) -> None:
    with pytest.raises(PriorValidationError):
        resolve_prior("model-a", "tier-1", **kwargs)  # type: ignore[arg-type]


def test_resolve_prior_applies_explicit_override_mappings() -> None:
    assert resolve_prior(
        "model-a",
        "tier-1",
        model_overrides={"model-a": Decimal("0.2")},
        tier_overrides={"tier-1": Decimal("0.3")},
    ) == Decimal("0.2")


def test_resolve_prior_rejects_non_numeric_and_malformed_values() -> None:
    with pytest.raises(PriorValidationError):
        resolve_prior("model-a", "tier-1", PriorSet(model_overrides={"model-a": object()}))
    with pytest.raises(PriorValidationError):
        resolve_prior("model-a", "tier-1", PriorSet(model_overrides={"model-a": "invalid"}))
