"""Deterministic tier and marginal-cost model selection policy."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

from ..cli.config.project_config import validate_model_metadata
from .priors import DEFAULT_PRIOR_SET, PriorSet, PriorValidationError, resolve_prior

TIER_LADDER = {
    "tier-1": ("mai-code-1.1-flash", "gpt-5.6-luna"),
    "tier-2": ("claude-sonnet-5", "gemini-3.1-pro-preview"),
    "tier-3": ("claude-opus-5", "claude-opus-4.8", "claude-opus-4.6"),
}
EXCLUDED_MODELS = frozenset({"claude-sonnet-4.6", "gemini-3.6-flash", "gpt-5.4-mini"})
_TIERS = tuple(TIER_LADDER)


class ModelCostError(ValueError):
    """Raised when normalized model cost metadata is invalid."""


@dataclass(frozen=True)
class NoSelection:
    """Typed explanation for why a dispatch model was not selected."""

    reason: Literal["no_eligible_model", "budget_exhausted", "invalid_prior", "invalid_budget"]
    status: str = ""

    def __post_init__(self) -> None:
        if not self.status:
            object.__setattr__(self, "status", self.reason)


@dataclass(frozen=True)
class ModelSelection:
    """A model choice together with auditable marginal decision evidence."""

    model_id: str
    tier: str
    cost: Decimal
    currency: str
    prior_version: str
    prior: Decimal
    branch_value: Decimal
    expected_cost: Decimal
    ordinal: int
    remaining_attempts: int

    @property
    def modelId(self) -> str:  # noqa: N802
        return self.model_id

    @property
    def resolve_model_cost(self) -> Decimal:
        return self.cost


def _decimal(value: Any, field_name: str) -> Decimal:
    if isinstance(value, bool):
        raise ModelCostError(f"{field_name} must be numeric, not boolean")
    if not isinstance(value, (Decimal, int, float, str)):
        raise ModelCostError(f"{field_name} must be numeric")
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ModelCostError(f"{field_name} must be a valid decimal") from exc
    if not result.is_finite():
        raise ModelCostError(f"{field_name} must be finite")
    return result


def _metadata_entry(model: str | Mapping[str, Any], models: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if isinstance(model, Mapping):
        return model
    if models is None or not isinstance(models, Mapping):
        raise ModelCostError(f"no metadata supplied for {model!r}")
    entry = models.get(model)
    if not isinstance(entry, Mapping):
        raise ModelCostError(f"no metadata supplied for {model!r}")
    return entry


def resolve_model_cost(
    model: str | Mapping[str, Any],
    models: Mapping[str, Any] | None = None,
) -> Decimal:
    """Return a finite, non-negative exact decimal from normalized metadata."""
    entry = dict(_metadata_entry(model, models))
    if isinstance(model, str) and entry.get("modelId") != model:
        raise ModelCostError(f"metadata modelId {entry.get('modelId')!r} does not match requested model {model!r}")
    pricing_status = entry.get("pricingStatus")
    if pricing_status in {"unavailable", "non_priceable"}:
        raise ModelCostError(f"model {entry.get('modelId', model)!r} has no usable monetary pricing")
    if pricing_status is None and all(
        field in entry
        for field in (
            "inputRatePerM",
            "outputRatePerM",
            "currency",
            "rateUnit",
            "assumedInputTokens",
            "assumedOutputTokens",
            "modelledSessionCost",
            "priceCategory",
            "provenance",
            "costDataAsOf",
        )
    ):
        entry["pricingStatus"] = "priceable"
    elif pricing_status != "priceable":
        raise ModelCostError(f"model {entry.get('modelId', model)!r} has invalid pricing status")
    try:
        validate_model_metadata(entry)
    except (ValueError, TypeError) as exc:
        raise ModelCostError(str(exc)) from exc
    cost = _decimal(entry.get("modelledSessionCost"), "modelledSessionCost")
    if cost < 0:
        raise ModelCostError("modelledSessionCost must be non-negative")
    return cost


@dataclass(frozen=True)
class _Candidate:
    model_id: str
    tier: str
    cost: Decimal
    currency: str
    prior: Decimal


def _first_step_candidates(
    candidates: list[_Candidate],
    current_index: int,
) -> tuple[int | None, list[_Candidate], list[_Candidate]]:
    present_tiers = {candidate.tier for candidate in candidates}
    current = [c for c in candidates if _TIERS.index(c.tier) == current_index]
    if not current:
        next_indexes = [i for i in range(current_index + 1, len(_TIERS)) if _TIERS[i] in present_tiers]
        if not next_indexes:
            return None, [], []
        current_index = next_indexes[0]
        current = [c for c in candidates if _TIERS.index(c.tier) == current_index]

    next_candidates: list[_Candidate] = []
    next_indexes = [i for i in range(current_index + 1, len(_TIERS)) if _TIERS[i] in present_tiers]
    if next_indexes:
        next_candidates = [c for c in candidates if _TIERS.index(c.tier) == next_indexes[0]]
    return current_index, current, next_candidates


def _candidate_values(
    candidates: list[_Candidate],
    current_index: int,
    attempts_left: int,
) -> tuple[Decimal, list[_Candidate]]:
    if attempts_left <= 0 or not candidates:
        return Decimal("0"), []
    effective_index, current, next_candidates = _first_step_candidates(candidates, current_index)
    if effective_index is None:
        return Decimal("0"), []

    def branch(candidate: _Candidate) -> tuple[Decimal, Decimal, list[_Candidate]]:
        remaining = [c for c in candidates if c.model_id != candidate.model_id]
        rest, sequence = _candidate_values(remaining, _TIERS.index(candidate.tier), attempts_left - 1)
        value = candidate.cost + (Decimal("1") - candidate.prior) * rest
        return value, rest, [candidate, *sequence]

    current_results = [branch(c) for c in current]
    current_results.sort(key=lambda item: (item[0], item[2][0].cost, item[2][0].model_id))
    next_results = [branch(c) for c in next_candidates]
    next_results.sort(key=lambda item: (item[0], item[2][0].cost, item[2][0].model_id))
    if not next_results or current_results[0][0] <= next_results[0][0]:
        return current_results[0][0], current_results[0][2]
    return next_results[0][0], next_results[0][2]


def _coerce_attempted(value: Iterable[str] | None) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, (str, bytes)):
        raise ValueError("attempted_models must be an iterable of model IDs")
    result: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item:
            raise ValueError(f"each attempted model ID must be a non-empty string, got {item!r}")
        result.add(item)
    return result


def _rank_first_step_candidates(
    candidates: list[_Candidate],
    start_index: int,
    attempts_left: int,
) -> list[tuple[Decimal, _Candidate]]:
    if attempts_left <= 0 or not candidates:
        return []
    _, current, next_candidates = _first_step_candidates(candidates, start_index)
    ranked: list[tuple[Decimal, _Candidate]] = []
    for candidate in [*current, *next_candidates]:
        remaining = [c for c in candidates if c.model_id != candidate.model_id]
        rest, _ = _candidate_values(remaining, _TIERS.index(candidate.tier), attempts_left - 1)
        expected_cost = candidate.cost + (Decimal("1") - candidate.prior) * rest
        ranked.append((expected_cost, candidate))
    ranked.sort(key=lambda item: (item[0], item[1].cost, item[1].model_id))
    return ranked


def select_model_for_dispatch(
    models: Mapping[str, Any],
    availability: Mapping[str, Any],
    attempted_models: Iterable[str] | None = None,
    ordinal: int = 1,
    *,
    prior_set: PriorSet | None = None,
    model_overrides: Mapping[str, Any] | None = None,
    tier_overrides: Mapping[str, Any] | None = None,
    budget_ceiling: Any = None,
    committed_cost: Any = Decimal("0"),
    budget_currency: str | None = None,
    next_dispatch_ordinal: int | None = None,
    attempted_model_ids: Iterable[str] | None = None,
) -> ModelSelection | NoSelection:
    """Select an unattempted available model using recursive marginal values."""
    if not isinstance(models, Mapping) or not isinstance(availability, Mapping):
        raise ValueError("models and availability must be mappings")
    if next_dispatch_ordinal is not None:
        ordinal = next_dispatch_ordinal
    if attempted_model_ids is not None:
        if attempted_models is not None:
            raise ValueError("provide only one of attempted_models and attempted_model_ids")
        attempted_models = attempted_model_ids
    if isinstance(ordinal, bool) or not isinstance(ordinal, int) or not 1 <= ordinal <= 3:
        raise ValueError("ordinal must be an integer from 1 through 3")
    if attempted_models is not None and isinstance(attempted_models, (str, bytes)):
        raise ValueError("attempted_models must be an iterable of model IDs")
    attempted_sequence = tuple(attempted_models or ())
    attempted = _coerce_attempted(attempted_sequence)
    candidates: list[_Candidate] = []
    try:
        for tier, model_ids in TIER_LADDER.items():
            for model_id in model_ids:
                if model_id in attempted:
                    continue
                status = availability.get(model_id)
                if isinstance(status, Mapping):
                    status = status.get("status")
                if status != "available":
                    continue
                entry = models.get(model_id)
                if not isinstance(entry, Mapping):
                    continue
                try:
                    cost = resolve_model_cost(model_id, models)
                    prior = resolve_prior(
                        model_id,
                        tier,
                        prior_set if prior_set is not None else DEFAULT_PRIOR_SET,
                        model_overrides=model_overrides,
                        tier_overrides=tier_overrides,
                    )
                except ModelCostError:
                    continue
                except PriorValidationError:
                    return NoSelection("invalid_prior")
                currency = entry.get("currency")
                if not isinstance(currency, str) or not currency.strip():
                    continue
                candidates.append(_Candidate(model_id, tier, cost, currency, prior))
    except (TypeError, AttributeError):
        return NoSelection("no_eligible_model")

    if not candidates:
        return NoSelection("no_eligible_model")

    last_attempted_tier = None
    for tier in _TIERS:
        # _TIERS is ordered ascending (tier-1 < tier-2 < tier-3); each match
        # overwrites, so the final value is the highest tier containing any
        # attempted model.
        if any(model_id in TIER_LADDER[tier] for model_id in attempted):
            last_attempted_tier = tier
    start_index = _TIERS.index(last_attempted_tier) if last_attempted_tier else 0
    expected_cost, sequence = _candidate_values(candidates, start_index, 4 - ordinal)
    if not sequence:
        return NoSelection("no_eligible_model")
    selected = sequence[0]

    try:
        committed = _decimal(committed_cost, "committed_cost")
        if committed < 0:
            raise ModelCostError("committed_cost must be non-negative")
        ceiling = None if budget_ceiling is None else _decimal(budget_ceiling, "budget_ceiling")
        if ceiling is not None and ceiling < 0:
            raise ModelCostError("budget_ceiling must be non-negative")
    except ModelCostError:
        return NoSelection("invalid_budget")
    if budget_currency is not None and (not isinstance(budget_currency, str) or not budget_currency.strip()):
        return NoSelection("invalid_budget")
    currencies = {candidate.currency for candidate in candidates}
    if len(currencies) > 1:
        return NoSelection("invalid_budget")
    if ceiling is not None and budget_currency is not None and selected.currency != budget_currency:
        return NoSelection("invalid_budget")
    if ceiling is not None and committed + selected.cost > ceiling:
        fitting_ranking = next(
            (
                (value, candidate)
                for value, candidate in _rank_first_step_candidates(candidates, start_index, 4 - ordinal)
                if budget_currency in (None, candidate.currency) and committed + candidate.cost <= ceiling
            ),
            None,
        )
        if fitting_ranking is None:
            return NoSelection("budget_exhausted")
        expected_cost, selected = fitting_ranking

    branch_value = expected_cost
    return ModelSelection(
        model_id=selected.model_id,
        tier=selected.tier,
        cost=selected.cost,
        currency=selected.currency,
        prior_version=(prior_set if prior_set is not None else DEFAULT_PRIOR_SET).version,
        prior=selected.prior,
        branch_value=branch_value,
        expected_cost=expected_cost,
        ordinal=ordinal,
        remaining_attempts=3 - ordinal,
    )


__all__ = [
    "EXCLUDED_MODELS",
    "ModelCostError",
    "ModelSelection",
    "NoSelection",
    "TIER_LADDER",
    "resolve_model_cost",
    "select_model_for_dispatch",
]
