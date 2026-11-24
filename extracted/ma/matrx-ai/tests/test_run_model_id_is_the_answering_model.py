"""A stored run row names the model that ANSWERED, not the configured one (program-lead ruling 2026-11-19)."""

from types import SimpleNamespace

import pytest

from matrx_ai.agents.run_attribution import run_model_id

CFG = SimpleNamespace(model="claude-opus-5-5")
IDS = {"claude-opus-5-5": "opus-id", "claude-sonnet-5-5": "sonnet-id", "opus-id": "opus-id", "sonnet-id": "sonnet-id"}


@pytest.fixture(autouse=True)
def _catalog(monkeypatch) -> None:
    from matrx_ai.catalog.manager import ai_catalog_manager

    monkeypatch.setattr(ai_catalog_manager, "resolve_model_ref", lambda ref: IDS.get(ref, ref))


def test_usage_naming_one_model_wins_over_the_configured_model() -> None:
    usage = {"models": {"claude-sonnet-5-5": {"request_count": 1}}}
    assert run_model_id({}, CFG, usage) == "sonnet-id"
    assert run_model_id({"model": "claude-opus-5-5"}, CFG, usage) == "sonnet-id"


def test_no_single_model_in_usage_keeps_the_configured_reading_as_its_catalog_id() -> None:
    assert run_model_id({}, CFG, None) == "opus-id"
    assert run_model_id({}, CFG, {}) == "opus-id"
    two = {"models": {"a": {}, "b": {}}}
    assert run_model_id({"model": "m"}, CFG, two) == "m"


def test_the_aggregated_usage_shape_names_its_models_under_by_model() -> None:
    """The executor hands ``AggregatedUsage.to_dict()``: ``by_model``, not ``models`` (a first fix read only ``models``
    and the live pair a3d-chain still recorded the configured Opus)."""
    from matrx_ai.config.usage_config import AggregatedUsage, ModelUsageSummary

    usage = AggregatedUsage(by_model={"claude-sonnet-5-5": ModelUsageSummary()}).to_dict()
    assert "models" not in usage
    assert run_model_id({}, CFG, usage) == "sonnet-id"


def test_the_catalog_id_is_saved_whatever_form_the_config_holds() -> None:
    assert run_model_id({"model": "opus-id"}, SimpleNamespace(model="opus-id"), {"models": {"claude-opus-5-5": {}}}) == "opus-id"
    # a swap leaves the stand-in's NAME on the config (live run 68c8c791 saved the name)
    assert run_model_id({}, SimpleNamespace(model="claude-sonnet-5-5"), {"models": {"claude-sonnet-5-5": {}}}) == "sonnet-id"
