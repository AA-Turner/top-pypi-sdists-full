"""Versioned success priors for provider-neutral model selection."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal
from types import MappingProxyType
from typing import Any

PRIORS_VERSION = "2026-08-01"

_DEFAULT_TIER_PRIORS = {
    "tier-1": Decimal("0.55"),
    "tier-2": Decimal("0.70"),
    "tier-3": Decimal("0.85"),
}


class PriorValidationError(ValueError):
    """Raised when a success prior is not a valid probability."""


def _validate_probability(value: Any, *, name: str) -> Decimal:
    if isinstance(value, bool):
        raise PriorValidationError(f"{name} must be a numeric probability, not a boolean")
    if isinstance(value, (str, float)):
        raise PriorValidationError(f"{name} must be a Decimal or integer, not {type(value).__name__}")
    if not isinstance(value, (Decimal, int)):
        raise PriorValidationError(f"{name} must be numeric")
    probability = value if isinstance(value, Decimal) else Decimal(value)
    if not probability.is_finite() or not Decimal("0") <= probability <= Decimal("1"):
        raise PriorValidationError(f"{name} must be finite and between 0 and 1")
    return probability


def _freeze(values: Mapping[str, Any]) -> MappingProxyType:
    if not isinstance(values, Mapping):
        raise PriorValidationError("prior overrides must be mappings")
    return MappingProxyType(dict(values))


@dataclass(frozen=True)
class PriorSet:
    """An immutable, versioned collection of model, tier, and default priors."""

    version: str = PRIORS_VERSION
    model_overrides: Mapping[str, Any] = field(default_factory=dict)
    tier_overrides: Mapping[str, Any] = field(default_factory=dict)
    tier_defaults: Mapping[str, Any] = field(default_factory=lambda: dict(_DEFAULT_TIER_PRIORS))

    def __post_init__(self) -> None:
        if not isinstance(self.version, str) or not self.version:
            raise PriorValidationError("prior version must be a non-empty string")
        object.__setattr__(self, "model_overrides", _freeze(self.model_overrides))
        object.__setattr__(self, "tier_overrides", _freeze(self.tier_overrides))
        object.__setattr__(self, "tier_defaults", _freeze(self.tier_defaults))


DEFAULT_PRIOR_SET = PriorSet()
DEFAULT_PRIORS = MappingProxyType(dict(_DEFAULT_TIER_PRIORS))


def resolve_prior(
    model_id: str,
    tier: str,
    prior_set: PriorSet | None = None,
    *,
    model_overrides: Mapping[str, Any] | None = None,
    tier_overrides: Mapping[str, Any] | None = None,
) -> Decimal:
    """Resolve and validate a model prior using specificity-first precedence."""
    if not isinstance(model_id, str) or not model_id:
        raise PriorValidationError("model_id must be a non-empty string")
    if not isinstance(tier, str) or not tier:
        raise PriorValidationError("tier must be a non-empty string")
    selected = DEFAULT_PRIOR_SET if prior_set is None else prior_set
    if not isinstance(selected, PriorSet):
        raise PriorValidationError("prior_set must be a PriorSet")
    if model_overrides is not None and not isinstance(model_overrides, Mapping):
        raise PriorValidationError("model_overrides must be a mapping")
    if tier_overrides is not None and not isinstance(tier_overrides, Mapping):
        raise PriorValidationError("tier_overrides must be a mapping")

    model_values = dict(selected.model_overrides)
    tier_values = dict(selected.tier_overrides)
    if model_overrides is not None:
        model_values.update(model_overrides)
    if tier_overrides is not None:
        tier_values.update(tier_overrides)

    if model_id in model_values:
        return _validate_probability(model_values[model_id], name=f"prior for {model_id!r}")
    if tier in tier_values:
        return _validate_probability(tier_values[tier], name=f"prior for {tier!r}")
    if tier not in selected.tier_defaults:
        raise PriorValidationError(f"no prior configured for {tier!r}")
    return _validate_probability(selected.tier_defaults[tier], name=f"default prior for {tier!r}")


__all__ = [
    "DEFAULT_PRIOR_SET",
    "DEFAULT_PRIORS",
    "PRIORS_VERSION",
    "PriorSet",
    "PriorValidationError",
    "resolve_prior",
]
