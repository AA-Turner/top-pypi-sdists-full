"""Tests for ``TrioConfig``."""

import pytest

from agentic_devtools.orchestration.trio_config import ReviewCap, RoleAssignment, TrioConfig, validate_trio_config
from tests.unit.orchestration.trio_config._samples import document


def test_valid_config_round_trip_and_immutable_models() -> None:
    config = validate_trio_config(document())
    assert isinstance(config, TrioConfig)
    assert config.review_cap == ReviewCap()
    assert config.adjudicator_applier == config.roles["adjudicator"]
    assert config.to_document() == document()
    with pytest.raises(TypeError):
        config.roles["doer"] = config.roles["duckA"]  # type: ignore[index]


def test_trioconfig_constructor_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        TrioConfig("2.0", "example-trio", {})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "Bad Ref", {})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", {})  # type: ignore[arg-type]
    valid_roles = {
        "doer": RoleAssignment("tier-1", "mai-code-1.1-flash"),
        "duckA": RoleAssignment("tier-2", "claude-sonnet-5"),
        "duckB": RoleAssignment("tier-1", "gpt-5.6-luna"),
        "adjudicator": RoleAssignment("tier-3", "claude-opus-5"),
    }
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", {**valid_roles, "other": object()})  # type: ignore[dict-item]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", {**valid_roles, "doer": object()})  # type: ignore[dict-item]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", valid_roles, review_cap=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", valid_roles, rotation_policy=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", valid_roles, adjudication_policy=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        TrioConfig("1.0", "example-trio", None)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="heavyweightDuckA must use tier-3"):
        TrioConfig(
            "1.0",
            "example-trio",
            {
                **valid_roles,
                "heavyweightDuckA": RoleAssignment("tier-2", "heavy-a"),
                "heavyweightDuckB": RoleAssignment("tier-3", "heavy-b"),
                "heavyweightAdjudicator": RoleAssignment("tier-3", "heavy-judge"),
            },
        )


def test_trioconfig_from_document_rejects_non_tier3_heavyweight_roles() -> None:
    doc = document()
    doc["roles"]["heavyweightDuckA"]["tier"] = "tier-2"
    with pytest.raises(ValueError, match="heavyweightDuckA must use tier-3"):
        TrioConfig.from_document(doc)
