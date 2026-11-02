import pytest

from agentic_devtools.ai_providers.availability import infer_validation_surface
from agentic_devtools.ai_providers.errors import ProviderError


def test_infer_validation_surface_prefers_validating_surface() -> None:
    assert (
        infer_validation_surface(
            "custom_agent is not valid",
            ("model", "custom_agent", "base_ref"),
        )
        == "custom_agent"
    )
    assert (
        infer_validation_surface(
            "base_ref missing",
            ("model", "custom_agent", "base_ref"),
        )
        == "base_ref"
    )
    assert (
        infer_validation_surface(
            "model claude; base reference is missing",
            ("model", "custom_agent", "base_ref"),
        )
        == "base_ref"
    )
    assert (
        infer_validation_surface(
            "model rejected",
            ("model", "custom_agent", "base_ref"),
        )
        == "model"
    )
    assert infer_validation_surface(None, ("model", "custom_agent", "base_ref")) == "model"
    assert infer_validation_surface("totally unrelated", ("model", "custom_agent", "base_ref")) == "model"


def test_infer_validation_surface_prefers_failure_field_over_contextual_mention() -> None:
    # "custom_agent 'reviewer' is invalid for model claude-opus-5" — the model is only
    # a descriptor; custom_agent is the actual failing field.  The function must not
    # return "model" just because it appears first in the validation order.
    assert (
        infer_validation_surface(
            "custom_agent 'reviewer' is invalid for model claude-opus-5",
            ("model", "custom_agent", "base_ref"),
        )
        == "custom_agent"
    )
    # Tight failure-phrase wins over a bare field mention appearing earlier in the text.
    assert (
        infer_validation_surface(
            "model context: invalid custom_agent abc",
            ("model", "custom_agent", "base_ref"),
        )
        == "custom_agent"
    )


def test_infer_validation_surface_uses_textual_position_when_multiple_failure_phrases_match() -> None:
    # When two surfaces both have tight failure-phrase matches, the one whose phrase
    # appears earlier in the text wins — not the one earlier in validation order.
    assert (
        infer_validation_surface(
            "ref not found; also invalid model mentioned later",
            ("model", "custom_agent", "base_ref"),
        )
        == "base_ref"
    )
    # Converse: model failure phrase first means model wins even though base_ref
    # also has a tight failure phrase later.  Exercises the pos >= earliest_fp
    # branch in the multi-surface tiebreaker loop.
    assert (
        infer_validation_surface(
            "invalid model; ref not found at end",
            ("model", "custom_agent", "base_ref"),
        )
        == "model"
    )


def test_infer_validation_surface_custom_agent_ref_not_found_returns_custom_agent() -> None:
    # "custom_agent ref not found" must resolve to custom_agent, not base_ref,
    # even though "ref not found" is listed as a base_ref failure phrase.
    assert (
        infer_validation_surface(
            "custom_agent ref not found",
            ("model", "custom_agent", "base_ref"),
        )
        == "custom_agent"
    )
    assert (
        infer_validation_surface(
            "custom agent reference not found",
            ("model", "custom_agent", "base_ref"),
        )
        == "custom_agent"
    )


def test_infer_validation_surface_prefers_base_ref_when_model_is_context_only() -> None:
    assert (
        infer_validation_surface(
            "model claude-opus-5 accepted; base_ref 'refs/heads/does-not-exist' was not found",
            ("model", "custom_agent", "base_ref"),
        )
        == "base_ref"
    )
    assert (
        infer_validation_surface(
            "model claude-opus-5 accepted; base_ref 'refs/heads/feature;foo' was not found",
            ("model", "custom_agent", "base_ref"),
        )
        == "base_ref"
    )
    assert (
        infer_validation_surface(
            "model claude-opus-5 accepted; base_ref 'refs/heads/feature,but' was not found",
            ("model", "custom_agent", "base_ref"),
        )
        == "base_ref"
    )


def test_infer_validation_surface_rejects_non_canonical_validation_order() -> None:
    with pytest.raises(ProviderError, match="validation_order must be exactly"):
        infer_validation_surface(None, ("other",))


def test_infer_validation_surface_ignores_partial_identifier_matches() -> None:
    assert infer_validation_surface("database_ref is invalid", ("model", "custom_agent", "base_ref")) == "model"
    assert infer_validation_surface("custom_agent_config failed validation", ("model", "custom_agent", "base_ref")) == (
        "model"
    )
