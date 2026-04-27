"""Tests for config explanation and write guidance."""

from __future__ import annotations

from dataclasses import dataclass

from anteroom.services.config_explanation import (
    ConfigExplanationContext,
    explain_setting,
    format_explanation,
    format_write_plan,
    list_sources,
    plan_set,
)
from anteroom.services.config_overlays import (
    PackOverlayArtifact,
    merge_pack_overlays_with_provenance,
)


@dataclass
class _AI:
    model: str = "project-model"
    api_key: str = "sk-secret"
    temperature: float = 0.2


@dataclass
class _Safety:
    approval_mode: str = "ask_for_writes"


@dataclass
class _Config:
    ai: _AI
    safety: _Safety


def _context() -> ConfigExplanationContext:
    pack_merge = merge_pack_overlays_with_provenance(
        [
            PackOverlayArtifact("team/security", {"ai": {"model": "secure-model"}}, pack_id="p1"),
            PackOverlayArtifact("team/dev", {"ai": {"model": "dev-model"}}, pack_id="p2"),
        ],
        {"team/security": 10, "team/dev": 50},
    )
    layer_raws = {
        "team": {"ai": {"model": "team-model"}},
        "pack": pack_merge.merged,
        "personal": {"ai": {"model": "personal-model"}},
        "space": {},
        "project": {"ai": {"model": "project-model"}},
        "env var": {},
    }
    return ConfigExplanationContext(
        config=_Config(ai=_AI(), safety=_Safety()),
        source_map={"ai.model": "project", "ai.api_key": "personal"},
        enforced_fields=[],
        layer_raws=layer_raws,
        pack_merge=pack_merge,
        working_dir="/tmp/project",
    )


def test_explain_setting_shows_effective_layer_and_lower_values() -> None:
    explanation = explain_setting("ai.model", _context())

    assert explanation.effective_value == "project-model"
    assert explanation.source_layer == "project"
    assert [v.layer for v in explanation.layer_values] == ["team", "pack", "personal", "project"]
    assert "overridden by project" in " ".join(explanation.notes)


def test_explain_setting_includes_pack_winner_and_overridden_values() -> None:
    explanation = explain_setting("ai.model", _context())

    by_pack = {c.pack_label: c for c in explanation.pack_contributions}
    assert by_pack["team/security"].wins_pack_layer is True
    assert by_pack["team/dev"].wins_pack_layer is False
    assert by_pack["team/dev"].overridden_by == "team/security"


def test_sensitive_values_are_redacted_in_dict_and_text() -> None:
    explanation = explain_setting("ai.api_key", _context())

    assert explanation.display_value == "***"
    rendered = format_explanation(explanation)
    assert "sk-secret" not in rendered
    assert explanation.to_dict()["effective_value"] == "***"


def test_plan_set_recommends_project_when_project_value_would_override_personal() -> None:
    plan = plan_set("ai.model", "new-model", _context(), scope="personal")

    assert plan.can_write is True
    assert plan.would_be_effective is False
    assert plan.recommended_scope == "project"
    assert plan.blocking_layers == ["project"]


def test_plan_set_blocks_enforced_field() -> None:
    context = _context()
    enforced_context = ConfigExplanationContext(
        config=context.config,
        source_map=context.source_map,
        enforced_fields=["ai.model"],
        layer_raws=context.layer_raws,
    )

    plan = plan_set("ai.model", "new-model", enforced_context)

    assert plan.can_write is False
    assert plan.would_be_effective is False
    assert "enforced" in (plan.reason or "")


def test_explain_setting_rejects_invalid_dot_path() -> None:
    try:
        explain_setting("../ai.model", _context())
    except ValueError as exc:
        assert "Invalid config path" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_explain_setting_notes_default_source() -> None:
    context = ConfigExplanationContext(
        config=_Config(ai=_AI(), safety=_Safety()),
        source_map={},
        enforced_fields=[],
        layer_raws={"team": {}, "pack": {}, "personal": {}, "space": {}, "project": {}, "env var": {}},
    )

    explanation = explain_setting("ai.temperature", context)

    assert explanation.source_layer == "default"
    assert "defaults" in " ".join(explanation.notes)


def test_list_sources_sorts_enforced_fields_and_redacts_sensitive_pack_values() -> None:
    pack_merge = merge_pack_overlays_with_provenance(
        [PackOverlayArtifact("team/secrets", {"ai": {"api_key": "sk-pack"}}, pack_id="p1")],
        {"team/secrets": 50},
    )
    context = ConfigExplanationContext(
        config=_Config(ai=_AI(), safety=_Safety()),
        source_map={"ai.api_key": "pack"},
        enforced_fields=["safety.approval_mode", "ai.model"],
        layer_raws={"pack": pack_merge.merged, "personal": {"ai": {"model": "mine"}}},
        pack_merge=pack_merge,
    )

    payload = list_sources(context)

    assert payload["enforced_fields"] == ["ai.model", "safety.approval_mode"]
    assert payload["pack_contributions"][0]["value"] == "***"


def test_plan_set_blocks_unknown_field() -> None:
    plan = plan_set("ai.not_known", "value", _context())

    assert plan.can_write is False
    assert "not a known" in (plan.reason or "")


def test_plan_set_blocks_invalid_scope() -> None:
    plan = plan_set("ai.model", "value", _context(), scope="galaxy")

    assert plan.can_write is False
    assert "scope must" in (plan.reason or "")


def test_plan_set_blocks_env_var_override() -> None:
    context = _context()
    env_context = ConfigExplanationContext(
        config=context.config,
        source_map={"ai.model": "env var"},
        enforced_fields=[],
        layer_raws={**context.layer_raws, "env var": {"ai": {"model": "env-model"}}},
    )

    plan = plan_set("ai.model", "new-model", env_context, scope="project")

    assert plan.can_write is False
    assert plan.recommended_scope == "env var"
    assert plan.blocking_layers == ["env var"]


def test_plan_set_recommends_space_when_space_is_smallest_effective_scope() -> None:
    context = _context()
    space_context = ConfigExplanationContext(
        config=context.config,
        source_map=context.source_map,
        enforced_fields=[],
        layer_raws={**context.layer_raws, "space": {"ai": {"model": "space-model"}}, "project": {}},
        active_space={"id": "sp1", "source_file": "/tmp/space.yaml"},
    )

    plan = plan_set("ai.model", "new-model", space_context)

    assert plan.can_write is True
    assert plan.would_be_effective is True
    assert plan.recommended_scope == "space"


def test_format_write_plan_renders_blocked_effective_and_ineffective() -> None:
    blocked = plan_set("ai.model", "new-model", ConfigExplanationContext(_Config(_AI(), _Safety()), {}, ["ai.model"]))
    effective = plan_set(
        "ai.temperature",
        0.4,
        ConfigExplanationContext(
            _Config(_AI(), _Safety()),
            {},
            [],
            {"team": {}, "pack": {}, "personal": {}, "space": {}, "project": {}, "env var": {}},
        ),
    )
    ineffective = plan_set("ai.model", "new-model", _context(), scope="personal")

    assert format_write_plan(blocked).startswith("Cannot change")
    assert "take effect" in format_write_plan(effective)
    assert "would not take effect" in format_write_plan(ineffective)
