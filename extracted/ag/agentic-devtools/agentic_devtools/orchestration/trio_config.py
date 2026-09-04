"""Typed validation and deterministic model rotation for subagent trios."""

from __future__ import annotations

import json
import re
from collections.abc import Collection, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Literal, cast

from jsonschema import Draft202012Validator

from agentic_devtools.ai_providers.tier_selector import TIER_LADDER
from agentic_devtools.cli.azure_devops.review_attribution import get_model_family

Phase = Literal["standard", "heavyweight_checkpoint"]
Tier = Literal["tier-1", "tier-2", "tier-3"]
ExhaustionMode = Literal["rotate_then_escalate", "fail_closed"]
Verdict = Literal["ACCEPT", "REJECT", "OVERTURN", "UPHOLD_REJECTION"]

_ROLES = ("doer", "duckA", "duckB", "adjudicator")
_HEAVYWEIGHT_ROLES = ("doer", "heavyweightDuckA", "heavyweightDuckB", "heavyweightAdjudicator")
_ROLE_NAMES = frozenset((*_ROLES, *_HEAVYWEIGHT_ROLES))
_TIERS = frozenset(TIER_LADDER)
_VERDICTS: frozenset[str] = frozenset({"ACCEPT", "REJECT", "OVERTURN", "UPHOLD_REJECTION"})
_POINT_PATTERN = re.compile(r"^POINT (.+?): (ACCEPT|REJECT|OVERTURN|UPHOLD_REJECTION) \| EVIDENCE: (.+)$")
_SUMMARY_PATTERN = re.compile(r"^RESPONSE_COMPLETE: accepted=(\d+) rejected=(\d+) total=(\d+)$")
_EVIDENCE_REFERENCE_PATTERN = re.compile(r"\b(?:clause|line):\s*\S", re.IGNORECASE)
_UNRESOLVED_DISPUTE_PATTERN = re.compile(
    r"\b(?:unresolved|still\s+disputed?|remains?\s+disputed?|dispute\s+remains?)\b",
    re.IGNORECASE,
)
_NEGATED_UNRESOLVED_DISPUTE_PATTERN = re.compile(
    r"\b(?:no|not|without)\s+unresolved(?:\s+dispute)?\b",
    re.IGNORECASE,
)


class TrioConfigValidationError(ValueError):
    """Raised when a trio document cannot be loaded or structurally validated."""

    def __init__(self, errors: Collection[str] | str, *, cause: BaseException | None = None) -> None:
        normalized: tuple[str, ...]
        if isinstance(errors, str):
            normalized = (errors,)
        else:
            normalized = tuple(errors)
        self.errors = normalized
        self.paths = tuple(error.split(":", 1)[0] for error in normalized if error.startswith("/"))
        self.messages = tuple(error.split(":", 1)[1].strip() if ":" in error else error for error in normalized)
        super().__init__("; ".join(normalized))
        if cause is not None:
            self.__cause__ = cause


class RoleDiversityViolation(ValueError):
    """Raised when a round cannot preserve model or reviewer-family diversity."""


class ReviewCapViolation(ValueError):
    """Raised when a review exceeds a configured cap."""


@dataclass(frozen=True)
class RoleAssignment:
    """A role's preferred model and ordered fallback models."""

    tier: Tier
    model_preference: str
    fallback_models: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.tier, str) or self.tier not in _TIERS:
            raise ValueError(f"tier must be one of {sorted(_TIERS)}")
        if not isinstance(self.model_preference, str) or not self.model_preference:
            raise ValueError("model_preference must be a non-empty string")
        if isinstance(self.fallback_models, (str, bytes)) or not isinstance(self.fallback_models, Sequence):
            raise ValueError("fallback_models must be an ordered sequence of model identifiers")
        fallbacks = tuple(self.fallback_models)
        if any(not isinstance(model, str) or not model for model in fallbacks):
            raise ValueError("fallback_models must contain only non-empty strings")
        if len(fallbacks) != len(set(fallbacks)):
            raise ValueError("fallback_models must not contain duplicate model identifiers")
        object.__setattr__(self, "fallback_models", fallbacks)

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> RoleAssignment:
        return cls(
            tier=document["tier"],
            model_preference=document["modelPreference"],
            fallback_models=tuple(document["fallbackModels"]),
        )

    def to_document(self) -> dict[str, Any]:
        return {
            "tier": self.tier,
            "modelPreference": self.model_preference,
            "fallbackModels": list(self.fallback_models),
        }


@dataclass(frozen=True)
class ReviewCap:
    """Bounds for a standard or heavyweight review phase."""

    mode: Phase = "standard"
    max_rounds: int = 5
    max_points_per_review: int = 20
    time_budget_minutes: int = 30

    def __post_init__(self) -> None:
        if self.mode not in ("standard", "heavyweight_checkpoint"):
            raise ValueError("mode must be standard or heavyweight_checkpoint")
        max_rounds_upper_bound = 2 if self.mode == "heavyweight_checkpoint" else 5
        _require_integer_range("max_rounds", self.max_rounds, 1, max_rounds_upper_bound)
        _require_integer_range("max_points_per_review", self.max_points_per_review, 1, 20)
        _require_integer_range("time_budget_minutes", self.time_budget_minutes, 5, 120)

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> ReviewCap:
        return cls(
            mode=document["mode"],
            max_rounds=document["maxRounds"],
            max_points_per_review=document["maxPointsPerReview"],
            time_budget_minutes=document["timeBudgetMinutes"],
        )

    def to_document(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "maxRounds": self.max_rounds,
            "maxPointsPerReview": self.max_points_per_review,
            "timeBudgetMinutes": self.time_budget_minutes,
        }


@dataclass(frozen=True)
class RotationPolicy:
    """Model diversity and exhaustion behavior for round assignment."""

    require_distinct_models: bool = True
    require_distinct_reviewer_families: bool = True
    on_exhaustion: ExhaustionMode = "rotate_then_escalate"

    def __post_init__(self) -> None:
        if not isinstance(self.require_distinct_models, bool):
            raise ValueError("require_distinct_models must be a boolean")
        if not isinstance(self.require_distinct_reviewer_families, bool):
            raise ValueError("require_distinct_reviewer_families must be a boolean")
        if not self.require_distinct_models or not self.require_distinct_reviewer_families:
            raise ValueError("schema version 1.0 requires both diversity policies to be true")
        if self.on_exhaustion not in ("rotate_then_escalate", "fail_closed"):
            raise ValueError("on_exhaustion must be rotate_then_escalate or fail_closed")

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> RotationPolicy:
        return cls(
            require_distinct_models=document["requireDistinctModels"],
            require_distinct_reviewer_families=document["requireDistinctReviewerFamilies"],
            on_exhaustion=document["onExhaustion"],
        )

    def to_document(self) -> dict[str, Any]:
        return {
            "requireDistinctModels": self.require_distinct_models,
            "requireDistinctReviewerFamilies": self.require_distinct_reviewer_families,
            "onExhaustion": self.on_exhaustion,
        }


@dataclass(frozen=True)
class AdjudicationPolicy:
    """Rules applied while parsing neutral adjudicator output."""

    allow_overturn: bool
    require_evidentiary_reasoning: bool
    fail_closed_on_dispute: bool

    def __post_init__(self) -> None:
        for name in ("allow_overturn", "require_evidentiary_reasoning", "fail_closed_on_dispute"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> AdjudicationPolicy:
        return cls(
            allow_overturn=document["allowOverturn"],
            require_evidentiary_reasoning=document["requireEvidentiaryReasoning"],
            fail_closed_on_dispute=document["failClosedOnDispute"],
        )

    def to_document(self) -> dict[str, Any]:
        return {
            "allowOverturn": self.allow_overturn,
            "requireEvidentiaryReasoning": self.require_evidentiary_reasoning,
            "failClosedOnDispute": self.fail_closed_on_dispute,
        }


@dataclass(frozen=True)
class TrioConfig:
    """Immutable, validated configuration for standard and heavyweight rounds."""

    schema_version: Literal["1.0"]
    trio_ref: str
    roles: Mapping[str, RoleAssignment]
    review_cap: ReviewCap = field(default_factory=ReviewCap)
    rotation_policy: RotationPolicy = field(default_factory=RotationPolicy)
    adjudication_policy: AdjudicationPolicy = field(
        default_factory=lambda: AdjudicationPolicy(
            allow_overturn=True,
            require_evidentiary_reasoning=True,
            fail_closed_on_dispute=True,
        )
    )

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise ValueError("schema_version must be '1.0'")
        if not isinstance(self.trio_ref, str) or not re.fullmatch(r"[a-z0-9-]+", self.trio_ref):
            raise ValueError("trio_ref must match ^[a-z0-9-]+$")
        if not isinstance(self.roles, Mapping):
            raise ValueError("roles must be a mapping")
        if not isinstance(self.review_cap, ReviewCap):
            raise ValueError("review_cap must be a ReviewCap")
        if not isinstance(self.rotation_policy, RotationPolicy):
            raise ValueError("rotation_policy must be a RotationPolicy")
        if not isinstance(self.adjudication_policy, AdjudicationPolicy):
            raise ValueError("adjudication_policy must be an AdjudicationPolicy")
        role_map = dict(self.roles)
        if not set(_ROLES).issubset(role_map):
            raise ValueError("roles must include doer, duckA, duckB, and adjudicator")
        if set(role_map) - _ROLE_NAMES:
            raise ValueError("roles contains an unknown role")
        if any(not isinstance(value, RoleAssignment) for value in role_map.values()):
            raise ValueError("roles must contain RoleAssignment values")
        for role_name in ("heavyweightDuckA", "heavyweightDuckB", "heavyweightAdjudicator"):
            assignment = role_map.get(role_name)
            if isinstance(assignment, RoleAssignment) and assignment.tier != "tier-3":
                raise ValueError(f"{role_name} must use tier-3")
        object.__setattr__(self, "roles", MappingProxyType(role_map))

    @property
    def adjudicator_applier(self) -> RoleAssignment:
        """Return the Python-named alias for the canonical adjudicator role."""
        return self.roles["adjudicator"]

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> TrioConfig:
        roles = {name: RoleAssignment.from_document(value) for name, value in document["roles"].items()}
        return cls(
            schema_version=document["schemaVersion"],
            trio_ref=document["trioRef"],
            roles=roles,
            review_cap=ReviewCap.from_document(document["reviewCap"]),
            rotation_policy=RotationPolicy.from_document(document["rotationPolicy"]),
            adjudication_policy=AdjudicationPolicy.from_document(document["adjudicationPolicy"]),
        )

    def to_document(self) -> dict[str, Any]:
        return {
            "schemaVersion": self.schema_version,
            "trioRef": self.trio_ref,
            "roles": {name: assignment.to_document() for name, assignment in self.roles.items()},
            "reviewCap": self.review_cap.to_document(),
            "rotationPolicy": self.rotation_policy.to_document(),
            "adjudicationPolicy": self.adjudication_policy.to_document(),
        }


@dataclass(frozen=True)
class PointVerdict:
    """One adjudicator decision and its evidentiary explanation."""

    point_id: str
    verdict: Verdict
    evidence: str

    def __post_init__(self) -> None:
        if not isinstance(self.point_id, str) or not self.point_id:
            raise ValueError("point_id must be a non-empty string")
        if not isinstance(self.verdict, str) or self.verdict not in _VERDICTS:
            raise ValueError(f"verdict must be one of {sorted(_VERDICTS)}")
        if not isinstance(self.evidence, str) or not self.evidence.strip():
            raise ValueError("evidence must be a non-empty string")

    @property
    def accepted(self) -> bool:
        return self.verdict in {"ACCEPT", "OVERTURN"}


@dataclass(frozen=True)
class AdjudicationResult:
    """Immutable adjudication decisions with mechanically derived counts."""

    point_verdicts: tuple[PointVerdict, ...]
    accepted: int = field(init=False)
    rejected: int = field(init=False)
    total: int = field(init=False)

    def __post_init__(self) -> None:
        decisions = tuple(self.point_verdicts)
        if any(not isinstance(decision, PointVerdict) for decision in decisions):
            raise ValueError("point_verdicts must contain PointVerdict values")
        accepted = sum(decision.accepted for decision in decisions)
        object.__setattr__(self, "point_verdicts", decisions)
        object.__setattr__(self, "accepted", accepted)
        object.__setattr__(self, "rejected", len(decisions) - accepted)
        object.__setattr__(self, "total", len(decisions))

    @property
    def decisions(self) -> tuple[PointVerdict, ...]:
        return self.point_verdicts


@dataclass(frozen=True)
class RoundAssignments(Mapping[str, str]):
    """Resolved role assignments plus the effective phase they require."""

    requested_phase: Phase
    effective_phase: Phase
    assignments: Mapping[str, str]

    def __post_init__(self) -> None:
        if self.requested_phase not in ("standard", "heavyweight_checkpoint"):
            raise ValueError("requested_phase must be standard or heavyweight_checkpoint")
        if self.effective_phase not in ("standard", "heavyweight_checkpoint"):
            raise ValueError("effective_phase must be standard or heavyweight_checkpoint")
        if not isinstance(self.assignments, Mapping):
            raise ValueError("assignments must be a mapping")
        frozen_assignments = dict(self.assignments)
        if not frozen_assignments:
            raise ValueError("assignments must not be empty")
        for role, model in frozen_assignments.items():
            if role not in _ROLE_NAMES:
                raise ValueError(f"assignments contains unknown role {role!r}")
            if not isinstance(model, str) or not model:
                raise ValueError("assignments must contain non-empty model identifiers")
        object.__setattr__(self, "assignments", MappingProxyType(frozen_assignments))

    @property
    def escalated(self) -> bool:
        return self.requested_phase != self.effective_phase

    def __getitem__(self, key: str) -> str:
        return self.assignments[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.assignments)

    def __len__(self) -> int:
        return len(self.assignments)


def _require_integer_range(name: str, value: object, minimum: int, maximum: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer from {minimum} through {maximum}")


def _json_pointer(parts: Collection[object]) -> str:
    return "".join(f"/{str(part).replace('~', '~0').replace('/', '~1')}" for part in parts)


def _schema_issue(error: Any) -> str:
    path = list(error.absolute_path)
    if error.validator == "required":
        match = re.search(r"'([^']+)' is a required property", error.message)
        if match:
            path.append(match.group(1))
    elif error.validator == "additionalProperties":
        match = re.search(r"\('([^']+)' was unexpected\)", error.message)
        if match:
            path.append(match.group(1))
    pointer = _json_pointer(path)
    return f"{pointer or '/'}: {error.message}"


def _validate_document(document: Mapping[str, Any]) -> None:
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "trio.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    issues = tuple(
        sorted(
            (_schema_issue(error) for error in validator.iter_errors(document)),
            key=lambda value: value.split(":", 1)[0],
        )
    )
    if issues:
        raise TrioConfigValidationError(issues)


def validate_trio_config(
    document: Mapping[str, Any],
    *,
    model_metadata: Mapping[str, Mapping[str, Any]] | None = None,
) -> TrioConfig:
    """Validate a trio document structurally, then materialize its typed model."""
    if not isinstance(document, Mapping):
        raise TrioConfigValidationError("/: trio configuration root must be an object")
    try:
        _validate_document(document)
    except TrioConfigValidationError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise TrioConfigValidationError("/: unable to load trio schema", cause=exc) from exc
    try:
        config = TrioConfig.from_document(document)
    except (KeyError, TypeError, ValueError) as exc:
        raise TrioConfigValidationError(f"/: invalid trio configuration: {exc}", cause=exc) from exc
    if model_metadata is not None:
        if not isinstance(model_metadata, Mapping):
            raise TrioConfigValidationError("/: model_metadata must be a mapping")
        _validate_model_metadata_compatibility(config, model_metadata)
    return config


def load_trio_config(path: Path) -> TrioConfig:
    """Read UTF-8 JSON from ``path`` and validate it as a trio configuration."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TrioConfigValidationError(f"/: unable to read trio configuration: {exc}", cause=exc) from exc
    if not isinstance(document, Mapping):
        raise TrioConfigValidationError("/: trio configuration root must be an object")
    return validate_trio_config(document)


def _active_roles(phase: Phase) -> tuple[str, ...]:
    if phase == "standard":
        return _ROLES
    if phase == "heavyweight_checkpoint":
        return _HEAVYWEIGHT_ROLES
    raise ValueError("phase must be standard or heavyweight_checkpoint")


def _metadata_for(model: str, model_metadata: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    metadata = model_metadata.get(model)
    if not isinstance(metadata, Mapping):
        raise RoleDiversityViolation(f"model {model!r} has no available metadata")
    if metadata.get("status") != "available":
        raise RoleDiversityViolation(f"model {model!r} is not available")
    return metadata


def _availability_status(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    if isinstance(value, Mapping):
        status = value.get("status")
        if isinstance(status, str) and status:
            return status
    return None


def _normalized_family(model: str, family: object) -> str:
    if isinstance(family, str):
        normalized = family.strip()
        if normalized:
            return get_model_family(normalized) or normalized.lower()
    return get_model_family(model) or model.lower()


def _tier_for_model(model: str) -> Tier | None:
    for tier, models in TIER_LADDER.items():
        if model in models:
            return cast(Tier, tier)
    return None


def _normalized_model_metadata(
    model_metadata: Mapping[str, Mapping[str, Any]],
    availability: Mapping[str, Any] | None = None,
) -> dict[str, dict[str, str]]:
    normalized: dict[str, dict[str, str]] = {}
    for model, entry in model_metadata.items():
        if not isinstance(model, str) or not model or not isinstance(entry, Mapping):
            continue
        authoritative_tier = _tier_for_model(model)
        declared_tier = entry.get("tier")
        if declared_tier is None:
            if authoritative_tier is None:
                continue
            tier = authoritative_tier
        else:
            if not isinstance(declared_tier, str) or declared_tier not in _TIERS:
                continue
            if authoritative_tier is None or declared_tier != authoritative_tier:
                continue
            tier = cast(Tier, declared_tier)
        status = _availability_status(availability.get(model)) if availability is not None else None
        if availability is None and status is None:
            status = _availability_status(entry.get("status"))
        if status is None:
            if availability is not None:
                continue
            status = "available"
        normalized[model] = {
            "tier": tier,
            "status": status,
            "modelFamily": _normalized_family(model, entry.get("modelFamily")),
        }
    return normalized


def _normalize_attempted_models(
    attempted_models: Mapping[str, Collection[str]] | None,
) -> dict[str, tuple[str, ...]]:
    if attempted_models is None:
        return {}
    if not isinstance(attempted_models, Mapping):
        raise ValueError("attempted_models must be a mapping when provided")
    normalized: dict[str, tuple[str, ...]] = {}
    for role, attempted in attempted_models.items():
        if not isinstance(role, str) or not role:
            raise ValueError("attempted_models keys must be non-empty role strings")
        if isinstance(attempted, (str, bytes)) or not isinstance(attempted, Collection):
            raise ValueError("attempted_models values must be collections of model identifiers")
        attempted_values = tuple(attempted)
        if any(not isinstance(model, str) or not model for model in attempted_values):
            raise ValueError("attempted_models values must contain only non-empty model identifiers")
        normalized[role] = attempted_values
    return normalized


def _validate_model_metadata_compatibility(config: TrioConfig, model_metadata: Mapping[str, Mapping[str, Any]]) -> None:
    normalized_metadata = _normalized_model_metadata(model_metadata)
    issues: list[str] = []
    for role, assignment in config.roles.items():
        expected_models = (assignment.model_preference, *assignment.fallback_models)
        for index, model in enumerate(expected_models):
            pointer = f"/roles/{role}/modelPreference" if index == 0 else f"/roles/{role}/fallbackModels/{index - 1}"
            if model not in normalized_metadata:
                issues.append(f"{pointer}: model {model!r} is missing or tier-incompatible in model_metadata")
                continue
            model_tier = normalized_metadata[model].get("tier")
            if model_tier != assignment.tier:
                issues.append(
                    f"{pointer}: model {model!r} is tier {model_tier!r} but role {role!r} requires {assignment.tier!r}"
                )
    if issues:
        raise TrioConfigValidationError(tuple(issues))


def validate_round_assignments(
    config: TrioConfig,
    assignments: Mapping[str, str],
    *,
    phase: Phase,
    model_metadata: Mapping[str, Mapping[str, Any]],
    attempted_models: Mapping[str, Collection[str]] | None = None,
    availability: Mapping[str, Any] | None = None,
) -> None:
    """Validate resolved models against active roles, tiers, and diversity rules."""
    if not isinstance(config, TrioConfig) or not isinstance(assignments, Mapping):
        raise ValueError("config must be TrioConfig and assignments must be a mapping")
    if not isinstance(model_metadata, Mapping) or (availability is not None and not isinstance(availability, Mapping)):
        raise ValueError("model_metadata must be a mapping and availability must be a mapping when provided")
    active = _active_roles(phase)
    missing_roles = [role for role in active if role not in config.roles]
    if missing_roles:
        raise RoleDiversityViolation(
            f"configuration is missing active role definitions for {phase}: {', '.join(missing_roles)}"
        )
    normalized_metadata = _normalized_model_metadata(model_metadata, availability)
    if set(assignments) != set(active):
        raise RoleDiversityViolation(f"assignments must contain exactly the active roles: {', '.join(active)}")
    attempted = _normalize_attempted_models(attempted_models)
    selected: dict[str, Mapping[str, Any]] = {}
    for role in active:
        model = assignments[role]
        if not isinstance(model, str) or not model:
            raise RoleDiversityViolation(f"{role} must resolve to a non-empty model identifier")
        configured_candidates = (config.roles[role].model_preference, *config.roles[role].fallback_models)
        if model not in configured_candidates:
            raise RoleDiversityViolation(f"{role} model {model!r} is not configured for that role")
        if model in set(attempted.get(role, ())):
            raise RoleDiversityViolation(f"{role} resolved to previously attempted model {model!r}")
        metadata = _metadata_for(model, normalized_metadata)
        declared_tier = metadata.get("tier")
        if declared_tier not in _TIERS or declared_tier != config.roles[role].tier:
            raise RoleDiversityViolation(
                f"{role} model {model!r} does not match declared tier {config.roles[role].tier}"
            )
        selected[role] = metadata
    models = [assignments[role] for role in active]
    if len(models) != len(set(models)):
        raise RoleDiversityViolation("active roles must use pairwise distinct models")
    family_a = selected["heavyweightDuckA" if phase == "heavyweight_checkpoint" else "duckA"].get("modelFamily")
    family_b = selected["heavyweightDuckB" if phase == "heavyweight_checkpoint" else "duckB"].get("modelFamily")
    if family_a == family_b:
        raise RoleDiversityViolation("reviewer roles must use distinct model families")


def _candidate_models(
    role: str,
    assignment: RoleAssignment,
    available_models: Mapping[str, Mapping[str, Any]],
    attempted: Collection[str],
    used: set[str],
) -> list[str]:
    candidates = [assignment.model_preference, *assignment.fallback_models]
    result: list[str] = []
    for model in candidates:
        if model in attempted or model in used or model in result:
            continue
        metadata = available_models.get(model)
        if not isinstance(metadata, Mapping) or metadata.get("status") != "available":
            continue
        if metadata.get("tier") != assignment.tier or metadata.get("tier") not in _TIERS:
            continue
        result.append(model)
    return result


def _find_assignment(
    config: TrioConfig,
    roles: tuple[str, ...],
    available_models: Mapping[str, Mapping[str, Any]],
    attempted_models: Mapping[str, Collection[str]],
) -> dict[str, str] | None:
    if any(role not in config.roles for role in roles):
        return None

    def search(index: int, result: dict[str, str], used: set[str]) -> dict[str, str] | None:
        if index == len(roles):
            reviewer_a = "heavyweightDuckA" if roles == _HEAVYWEIGHT_ROLES else "duckA"
            reviewer_b = "heavyweightDuckB" if roles == _HEAVYWEIGHT_ROLES else "duckB"
            family_a = available_models[result[reviewer_a]].get("modelFamily")
            family_b = available_models[result[reviewer_b]].get("modelFamily")
            return result if family_a != family_b else None
        role = roles[index]
        candidates = _candidate_models(role, config.roles[role], available_models, attempted_models.get(role, ()), used)
        for model in candidates:
            result[role] = model
            found = search(index + 1, result, used | {model})
            if found is not None:
                return found
            del result[role]
        return None

    return search(0, {}, set())


def resolve_round_assignments(
    config: TrioConfig,
    *,
    phase: Phase,
    available_models: Mapping[str, Mapping[str, Any]],
    attempted_models: Mapping[str, Collection[str]] | None = None,
    availability: Mapping[str, Any] | None = None,
) -> RoundAssignments:
    """Resolve preferred and fallback models without violating round diversity."""
    if not isinstance(config, TrioConfig) or not isinstance(available_models, Mapping):
        raise ValueError("config must be TrioConfig and available_models must be a mapping")
    if availability is not None and not isinstance(availability, Mapping):
        raise ValueError("availability must be a mapping when provided")
    attempted = _normalize_attempted_models(attempted_models)
    normalized_models = _normalized_model_metadata(available_models, availability)
    roles = _active_roles(phase)
    resolved = _find_assignment(config, roles, normalized_models, attempted)
    if resolved is not None:
        return RoundAssignments(phase, phase, resolved)
    if phase == "standard" and config.rotation_policy.on_exhaustion == "rotate_then_escalate":
        escalation_attempted = {role: models for role, models in attempted.items() if role in _HEAVYWEIGHT_ROLES}
        escalation_attempted["doer"] = ()
        resolved = _find_assignment(config, _HEAVYWEIGHT_ROLES, normalized_models, escalation_attempted)
        if resolved is not None:
            return RoundAssignments(phase, "heavyweight_checkpoint", resolved)
    raise RoleDiversityViolation("no legal diverse model assignment remains; failing closed")


def validate_review_budget(
    cap: ReviewCap,
    *,
    phase: Phase,
    round_number: int,
    point_count: int,
    elapsed_minutes: int,
) -> None:
    """Raise ``ReviewCapViolation`` when any review budget is exceeded."""
    if not isinstance(cap, ReviewCap):
        raise ValueError("cap must be a ReviewCap")
    if phase not in ("standard", "heavyweight_checkpoint"):
        raise ValueError("phase must be standard or heavyweight_checkpoint")
    if isinstance(round_number, bool) or not isinstance(round_number, int) or round_number < 1:
        raise ReviewCapViolation("round_number must be at least 1")
    if isinstance(point_count, bool) or not isinstance(point_count, int) or point_count < 0:
        raise ReviewCapViolation("point_count must be a non-negative integer")
    if isinstance(elapsed_minutes, bool) or not isinstance(elapsed_minutes, int) or elapsed_minutes < 0:
        raise ReviewCapViolation("elapsed_minutes must be a non-negative integer")
    max_rounds = min(cap.max_rounds, 2) if phase == "heavyweight_checkpoint" else cap.max_rounds
    if round_number > max_rounds:
        raise ReviewCapViolation(f"round_number {round_number} exceeds {phase} cap {max_rounds}")
    if point_count > cap.max_points_per_review:
        raise ReviewCapViolation(f"point_count {point_count} exceeds cap {cap.max_points_per_review}")
    if elapsed_minutes > cap.time_budget_minutes:
        raise ReviewCapViolation(f"elapsed_minutes {elapsed_minutes} exceeds cap {cap.time_budget_minutes}")


def parse_adjudication_response(
    text: str,
    expected_point_ids: Collection[str],
    *,
    policy: AdjudicationPolicy,
) -> AdjudicationResult:
    """Parse point decisions and verify the exact adjudication summary."""
    if not isinstance(text, str) or not isinstance(policy, AdjudicationPolicy):
        raise ValueError("text must be a string and policy must be AdjudicationPolicy")
    if isinstance(expected_point_ids, (str, bytes)) or not isinstance(expected_point_ids, Collection):
        raise ValueError("expected_point_ids must be a collection of point IDs")
    expected = tuple(expected_point_ids)
    if any(not isinstance(point_id, str) or not point_id for point_id in expected):
        raise ValueError("expected_point_ids must contain unique non-empty strings")
    if len(expected) != len(set(expected)):
        raise ValueError("expected_point_ids must contain unique non-empty strings")
    if not isinstance(expected_point_ids, Sequence):
        expected = tuple(sorted(expected))
    lines = text.splitlines()
    if not lines or _SUMMARY_PATTERN.fullmatch(lines[-1]) is None:
        raise ValueError("response must end with an exact RESPONSE_COMPLETE summary")
    summary = _SUMMARY_PATTERN.fullmatch(lines[-1])
    if summary is None:  # pragma: no cover - guarded by the preceding fullmatch
        raise ValueError("response must end with an exact RESPONSE_COMPLETE summary")
    decisions: dict[str, PointVerdict] = {}
    for line in lines[:-1]:
        match = _POINT_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError("each point must use the exact POINT <id>: <VERDICT> | EVIDENCE: <text> form")
        point_id, verdict, evidence = match.groups()
        if point_id not in expected:
            raise ValueError(f"unknown point ID {point_id!r}")
        if point_id in decisions:
            raise ValueError(f"duplicate point ID {point_id!r}")
        if policy.require_evidentiary_reasoning and _EVIDENCE_REFERENCE_PATTERN.search(evidence) is None:
            raise ValueError(f"point {point_id!r} evidence must reference clause: or line:")
        if verdict == "OVERTURN" and not policy.allow_overturn:
            raise ValueError("OVERTURN is disabled by adjudication policy")
        if policy.fail_closed_on_dispute and _contains_unresolved_dispute(evidence):
            raise ValueError(f"point {point_id!r} contains unresolved or disputed evidence")
        decisions[point_id] = PointVerdict(point_id, cast(Verdict, verdict), evidence)
    missing = [point_id for point_id in expected if point_id not in decisions]
    if missing:
        raise ValueError(f"missing point IDs: {', '.join(missing)}")
    result = AdjudicationResult(tuple(decisions[point_id] for point_id in expected))
    counts = tuple(int(value) for value in summary.groups())
    if counts != (result.accepted, result.rejected, result.total):
        raise ValueError(
            f"summary counts accepted={counts[0]} rejected={counts[1]} total={counts[2]} "
            f"do not match accepted={result.accepted} rejected={result.rejected} total={result.total}"
        )
    return result


def _contains_unresolved_dispute(evidence: str) -> bool:
    """Return whether evidence still describes an unresolved dispute."""
    if _UNRESOLVED_DISPUTE_PATTERN.search(evidence) is None:
        return False
    scrubbed = _NEGATED_UNRESOLVED_DISPUTE_PATTERN.sub("", evidence)
    return _UNRESOLVED_DISPUTE_PATTERN.search(scrubbed) is not None


__all__ = [
    "AdjudicationPolicy",
    "AdjudicationResult",
    "Phase",
    "PointVerdict",
    "RoundAssignments",
    "ReviewCap",
    "ReviewCapViolation",
    "RoleAssignment",
    "RoleDiversityViolation",
    "RotationPolicy",
    "TrioConfig",
    "TrioConfigValidationError",
    "load_trio_config",
    "parse_adjudication_response",
    "resolve_round_assignments",
    "validate_review_budget",
    "validate_round_assignments",
    "validate_trio_config",
]
