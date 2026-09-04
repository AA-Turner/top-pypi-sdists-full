"""Tests for ``validate_round_assignments``."""

import pytest

from agentic_devtools.orchestration.trio_config import (
    RoleDiversityViolation,
    TrioConfig,
    validate_round_assignments,
    validate_trio_config,
)
from tests.unit.orchestration.trio_config._samples import availability, canonical_metadata, document, metadata


def test_validate_round_assignments_enforces_roles_tiers_models_families_and_status() -> None:
    config = validate_trio_config(document())
    assignments = {
        "doer": "mai-code-1.1-flash",
        "duckA": "claude-sonnet-5",
        "duckB": "gpt-5.6-luna",
        "adjudicator": "claude-opus-5",
    }
    model_metadata = metadata(*assignments.values())
    validate_round_assignments(config, assignments, phase="standard", model_metadata=model_metadata)

    for invalid in (
        {**assignments, "duckB": "claude-sonnet-5"},
        {**assignments, "duckB": "unknown"},
        {**assignments, "duckB": "mai-code-1.1-flash"},
    ):
        with pytest.raises(RoleDiversityViolation):
            validate_round_assignments(config, invalid, phase="standard", model_metadata=model_metadata)

    same_family = {name: dict(values) for name, values in model_metadata.items()}
    same_family["claude-sonnet-5"]["modelFamily"] = " Reviewer "
    same_family["gpt-5.6-luna"]["modelFamily"] = "reviewer"
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(config, assignments, phase="standard", model_metadata=same_family)
    blank_family = {name: dict(values) for name, values in model_metadata.items()}
    blank_family["claude-sonnet-5"]["modelFamily"] = "   "
    validate_round_assignments(config, assignments, phase="standard", model_metadata=blank_family)

    canonical = canonical_metadata(*assignments.values())
    no_status = availability(*assignments.values(), unavailable=("gpt-5.6-luna",))
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=canonical,
            availability=no_status,
        )

    with pytest.raises(ValueError):
        validate_round_assignments(object(), assignments, phase="standard", model_metadata=model_metadata)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_round_assignments(config, assignments, phase="invalid", model_metadata=model_metadata)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_round_assignments(config, assignments, phase="standard", model_metadata="invalid")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=model_metadata,
            availability="invalid",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=model_metadata,
            attempted_models="invalid",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=model_metadata,
            attempted_models={"doer": "mai-code-1.1-flash"},  # type: ignore[dict-item]
        )
    with pytest.raises(ValueError):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=model_metadata,
            attempted_models={"": []},  # type: ignore[dict-item]
        )
    with pytest.raises(ValueError):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=model_metadata,
            attempted_models={"doer": [None]},  # type: ignore[list-item]
        )
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(
            config, {"doer": "mai-code-1.1-flash"}, phase="standard", model_metadata=model_metadata
        )
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(config, {**assignments, "doer": ""}, phase="standard", model_metadata=model_metadata)
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(
            config,
            assignments,
            phase="standard",
            model_metadata=model_metadata,
            attempted_models={"doer": ["mai-code-1.1-flash"]},
        )
    unavailable = {name: dict(values) for name, values in model_metadata.items()}
    unavailable["mai-code-1.1-flash"]["status"] = "unavailable"
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(config, assignments, phase="standard", model_metadata=unavailable)
    wrong_tier = {name: dict(values) for name, values in model_metadata.items()}
    wrong_tier["mai-code-1.1-flash"]["tier"] = "tier-2"
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(config, assignments, phase="standard", model_metadata=wrong_tier)
    out_of_role_candidate = {**assignments, "adjudicator": "claude-opus-4.6"}
    with pytest.raises(RoleDiversityViolation, match="not configured for that role"):
        validate_round_assignments(
            config,
            out_of_role_candidate,
            phase="standard",
            model_metadata=metadata(*out_of_role_candidate.values()),
        )


def test_validate_round_assignments_heavyweight_phase_allows_non_tier3_doer() -> None:
    config = validate_trio_config(document())
    assignments = {
        "doer": "mai-code-1.1-flash",
        "heavyweightDuckA": "claude-opus-4.8",
        "heavyweightDuckB": "claude-opus-4.6",
        "heavyweightAdjudicator": "claude-opus-5",
    }
    model_metadata = metadata(*assignments.values())
    model_metadata["claude-opus-4.8"]["modelFamily"] = "heavy-a"
    model_metadata["claude-opus-4.6"]["modelFamily"] = "heavy-b"
    validate_round_assignments(
        config,
        assignments,
        phase="heavyweight_checkpoint",
        model_metadata=model_metadata,
    )

    bad_doer_tier = {name: dict(values) for name, values in model_metadata.items()}
    bad_doer_tier["mai-code-1.1-flash"]["tier"] = "tier-2"
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(config, assignments, phase="heavyweight_checkpoint", model_metadata=bad_doer_tier)

    bad_heavyweight_tier = {name: dict(values) for name, values in model_metadata.items()}
    bad_heavyweight_tier["claude-opus-4.8"]["tier"] = "tier-2"
    with pytest.raises(RoleDiversityViolation):
        validate_round_assignments(
            config,
            assignments,
            phase="heavyweight_checkpoint",
            model_metadata=bad_heavyweight_tier,
        )

    missing_heavy_roles_document = document()
    del missing_heavy_roles_document["roles"]["heavyweightDuckA"]
    del missing_heavy_roles_document["roles"]["heavyweightDuckB"]
    del missing_heavy_roles_document["roles"]["heavyweightAdjudicator"]
    with pytest.raises(RoleDiversityViolation, match="missing active role definitions"):
        validate_round_assignments(
            TrioConfig.from_document(missing_heavy_roles_document),
            assignments,
            phase="heavyweight_checkpoint",
            model_metadata=model_metadata,
        )


def test_validate_round_assignments_rejects_configured_candidate_with_mismatched_tier() -> None:
    roles = validate_trio_config(document()).roles
    config = TrioConfig(
        schema_version="1.0",
        trio_ref="tier-mismatch",
        roles={
            **roles,
            "doer": type(roles["doer"])(tier="tier-2", model_preference="mai-code-1.1-flash", fallback_models=()),
        },
    )
    with pytest.raises(RoleDiversityViolation, match="does not match declared tier"):
        validate_round_assignments(
            config,
            {
                "doer": "mai-code-1.1-flash",
                "duckA": "claude-sonnet-5",
                "duckB": "gpt-5.6-luna",
                "adjudicator": "claude-opus-5",
            },
            phase="standard",
            model_metadata=metadata("mai-code-1.1-flash", "claude-sonnet-5", "gpt-5.6-luna", "claude-opus-5"),
        )
