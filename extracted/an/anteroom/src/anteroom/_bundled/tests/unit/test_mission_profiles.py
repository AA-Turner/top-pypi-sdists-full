"""Tests for mission execution profiles — binding selection and plan transformation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import patch

import pytest

from anteroom.services.mission_compiler import CompiledItem, CompiledPlan
from anteroom.services.mission_profiles import (
    ExecutionProfile,
    apply_execution_profile,
    discover_workflows,
    list_profiles,
    resolve_profile,
    score_workflow,
    select_workflow,
)

# ---------------------------------------------------------------------------
# Helpers — lightweight workflow definition stubs
# ---------------------------------------------------------------------------


@dataclass
class _StubStep:
    id: str = "s1"
    type: str = "runner"
    runner: str | None = None


@dataclass
class _StubWorkflow:
    id: str = "test_workflow"
    version: str = "0.1.0"
    inputs: dict[str, Any] = field(default_factory=dict)
    steps: list[Any] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    description: str | None = None


def _make_plan(*items: CompiledItem) -> CompiledPlan:
    return CompiledPlan(items=list(items), title="Test Plan")


# ---------------------------------------------------------------------------
# resolve_profile
# ---------------------------------------------------------------------------


class TestResolveProfile:
    def test_builtin_profiles_exist(self) -> None:
        for name in ("default", "plan-then-execute", "parallel-review", "hands-off"):
            p = resolve_profile(name)
            assert p.name == name

    def test_unknown_profile_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown execution profile"):
            resolve_profile("nonexistent")

    def test_error_message_lists_available(self) -> None:
        with pytest.raises(ValueError, match="default"):
            resolve_profile("bad")

    def test_list_profiles(self) -> None:
        profiles = list_profiles()
        assert len(profiles) >= 4
        names = {p.name for p in profiles}
        assert "default" in names
        assert "hands-off" in names


# ---------------------------------------------------------------------------
# ExecutionProfile dataclass
# ---------------------------------------------------------------------------


class TestExecutionProfileDataclass:
    def test_frozen(self) -> None:
        p = resolve_profile("default")
        with pytest.raises(AttributeError):
            p.name = "modified"  # type: ignore[misc]

    def test_default_values(self) -> None:
        p = ExecutionProfile(name="test")
        assert p.plan_first is False
        assert p.parallel_lanes is False
        assert p.review_gate is False
        assert p.preferred_runners == []
        assert p.required_inputs == []
        assert p.default_adapter == "noop"
        assert p.escalation_on_failure == "hold"

    def test_custom_values(self) -> None:
        p = ExecutionProfile(
            name="custom",
            plan_first=True,
            preferred_runners=["cli_claude"],
            lane_limits={"default": 2},
        )
        assert p.plan_first is True
        assert p.preferred_runners == ["cli_claude"]
        assert p.lane_limits == {"default": 2}


# ---------------------------------------------------------------------------
# score_workflow
# ---------------------------------------------------------------------------


class TestScoreWorkflow:
    def test_runner_match_full(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(runner="cli_claude")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_claude"])
        score = score_workflow(wf, profile)
        assert score > 0.3

    def test_runner_match_none(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(runner="shell")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_codex"])
        score = score_workflow(wf, profile)
        # Runner doesn't match, so runner component is 0
        assert score < 0.5

    def test_input_match(self) -> None:
        wf = _StubWorkflow(inputs={"issue_number": {"type": "string"}})
        profile = ExecutionProfile(name="test", required_inputs=["issue_number"])
        score = score_workflow(wf, profile)
        assert score > 0.3

    def test_tag_match(self) -> None:
        wf = _StubWorkflow(tags=["test"])
        profile = ExecutionProfile(name="test")
        score = score_workflow(wf, profile)
        # Tag "test" matches profile name "test"
        assert score > 0.0

    def test_no_tags_scores_zero_for_tag_component(self) -> None:
        wf = _StubWorkflow(tags=[])
        profile = ExecutionProfile(name="test")
        score_no_tags = score_workflow(wf, profile)
        wf_with_tags = _StubWorkflow(tags=["test"])
        score_with_tags = score_workflow(wf_with_tags, profile)
        assert score_with_tags >= score_no_tags

    def test_structure_match_gate(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(type="gate")])
        profile = ExecutionProfile(name="test", review_gate=True)
        score = score_workflow(wf, profile)
        assert score > 0.0

    def test_structure_match_parallel(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(type="parallel")])
        profile = ExecutionProfile(name="test", parallel_lanes=True)
        score = score_workflow(wf, profile)
        assert score > 0.0

    def test_no_preferences_neutral(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(runner="cli_claude")])
        profile = ExecutionProfile(name="test")
        score = score_workflow(wf, profile)
        # Neutral scores for empty preferences
        assert 0.0 <= score <= 1.0

    def test_full_match_high_score(self) -> None:
        wf = _StubWorkflow(
            steps=[_StubStep(runner="cli_claude"), _StubStep(type="gate")],
            inputs={"issue_number": {"type": "string"}},
            tags=["parallel review"],
        )
        profile = ExecutionProfile(
            name="parallel-review",
            preferred_runners=["cli_claude"],
            required_inputs=["issue_number"],
            review_gate=True,
        )
        score = score_workflow(wf, profile)
        assert score > 0.6


# ---------------------------------------------------------------------------
# select_workflow
# ---------------------------------------------------------------------------


class TestSelectWorkflow:
    def test_empty_definitions(self) -> None:
        profile = ExecutionProfile(name="test")
        defn, reason = select_workflow([], profile)
        assert defn is None
        assert "no workflow definitions available" in reason

    def test_below_threshold(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(runner="shell")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_codex"])
        defn, reason = select_workflow([wf], profile, threshold=0.99)
        assert defn is None
        assert "no workflow matched" in reason

    def test_selects_best_match(self) -> None:
        wf_good = _StubWorkflow(
            id="good",
            steps=[_StubStep(runner="cli_claude")],
            inputs={"issue_number": {"type": "string"}},
        )
        wf_bad = _StubWorkflow(id="bad", steps=[_StubStep(runner="shell")])
        profile = ExecutionProfile(
            name="test",
            preferred_runners=["cli_claude"],
            required_inputs=["issue_number"],
        )
        defn, reason = select_workflow([wf_bad, wf_good], profile, threshold=0.3)
        assert defn is not None
        assert defn.id == "good"
        assert "matched workflow 'good'" in reason

    def test_reason_includes_score(self) -> None:
        wf = _StubWorkflow(steps=[_StubStep(runner="cli_claude")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_claude"])
        defn, reason = select_workflow([wf], profile, threshold=0.0)
        assert defn is not None
        assert "score" in reason


# ---------------------------------------------------------------------------
# discover_workflows
# ---------------------------------------------------------------------------


class TestDiscoverWorkflows:
    def test_returns_list(self) -> None:
        # May find 0+ workflows depending on installed package state
        result = discover_workflows()
        assert isinstance(result, list)

    def test_skips_unparseable(self, tmp_path: Any) -> None:
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text("not: a: valid: workflow")
        with patch(
            "anteroom.services.workflow_resolution.builtin_workflow_dirs",
            return_value=[tmp_path],
        ):
            result = discover_workflows()
            assert isinstance(result, list)
            # Should not crash, just skip

    def test_deduplicates_by_id(self, tmp_path: Any) -> None:
        valid = (
            "kind: workflow\nid: dupe\nversion: '0.1'\n"
            "steps:\n  - id: s1\n    type: runner\n    runner: shell\n    command: echo hi\n"
        )
        d1 = tmp_path / "d1"
        d2 = tmp_path / "d2"
        d1.mkdir()
        d2.mkdir()
        (d1 / "wf.yaml").write_text(valid)
        (d2 / "wf.yaml").write_text(valid)
        with patch(
            "anteroom.services.workflow_resolution.builtin_workflow_dirs",
            return_value=[d1, d2],
        ):
            result = discover_workflows()
            ids = [d.id for d in result]
            assert ids.count("dupe") == 1


# ---------------------------------------------------------------------------
# apply_execution_profile
# ---------------------------------------------------------------------------


class TestApplyExecutionProfile:
    def _item(self, temp_id: str = "t1", **kwargs: Any) -> CompiledItem:
        return CompiledItem(summary=f"Task {temp_id}", temp_id=temp_id, **kwargs)

    def test_default_profile_no_change(self) -> None:
        profile = resolve_profile("default")
        plan = _make_plan(self._item("t1"), self._item("t2"))
        new_plan, lane_limits = apply_execution_profile(plan, profile, workflows=[])
        assert len(new_plan.items) == 2
        assert lane_limits is None

    def test_plan_first_adds_planning_item(self) -> None:
        profile = ExecutionProfile(name="test", plan_first=True)
        plan = _make_plan(self._item("t1"), self._item("t2"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        ids = [i.temp_id for i in new_plan.items]
        assert "_planning" in ids
        # Execution items should depend on planning
        for item in new_plan.items:
            if item.temp_id != "_planning":
                assert "_planning" in item.depends_on

    def test_plan_first_single_item_no_planning(self) -> None:
        profile = ExecutionProfile(name="test", plan_first=True)
        plan = _make_plan(self._item("t1"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        ids = [i.temp_id for i in new_plan.items]
        assert "_planning" not in ids  # Degenerate: only 1 item

    def test_parallel_lanes_assigns_lanes(self) -> None:
        profile = ExecutionProfile(name="test", parallel_lanes=True, lane_limits={"default": 2})
        plan = _make_plan(self._item("t1"), self._item("t2"))
        new_plan, lane_limits = apply_execution_profile(plan, profile, workflows=[])
        lanes = [i.lane for i in new_plan.items if i.lane]
        assert len(lanes) == 2
        # All items use "default" lane to match lane_limits key
        assert all(lane == "default" for lane in lanes)
        assert lane_limits == {"default": 2}

    def test_review_gate_inserts_reviews(self) -> None:
        profile = ExecutionProfile(name="test", review_gate=True)
        plan = _make_plan(self._item("t1"), self._item("t2"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        review_items = [i for i in new_plan.items if i.item_type == "review"]
        assert len(review_items) == 2
        # Each review depends on its parent
        for ri in review_items:
            parent_id = ri.temp_id.replace("_review_", "")
            assert parent_id in ri.depends_on

    def test_workflow_binding_when_matched(self) -> None:
        from pathlib import Path

        wf = _StubWorkflow(id="matched", steps=[_StubStep(runner="cli_claude")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_claude"])
        plan = _make_plan(self._item("t1"))
        resolved = Path("/workflows/matched.yaml")
        with patch(
            "anteroom.services.workflow_resolution.resolve_workflow_path",
            return_value=resolved,
        ):
            new_plan, _ = apply_execution_profile(plan, profile, workflows=[wf])
        item = new_plan.items[0]
        assert item.adapter_type == "workflow"
        assert item.adapter_config["workflow_path"] == str(resolved)
        assert "matched workflow" in item.adapter_config["_binding_reason"]

    def test_fallback_when_no_workflow_matches(self) -> None:
        profile = ExecutionProfile(name="test", preferred_runners=["cli_codex"])
        plan = _make_plan(self._item("t1"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        item = new_plan.items[0]
        assert item.adapter_type == "noop"
        assert "fallback" in item.adapter_config["_binding_reason"]

    def test_does_not_override_explicit_adapter(self) -> None:
        wf = _StubWorkflow(id="matched", steps=[_StubStep(runner="cli_claude")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_claude"])
        item = self._item("t1", adapter_type="custom", adapter_config={"key": "val"})
        plan = _make_plan(item)
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[wf])
        assert new_plan.items[0].adapter_type == "custom"
        assert "explicitly set" in new_plan.items[0].adapter_config["_binding_reason"]

    def test_binding_reason_on_every_item(self) -> None:
        profile = resolve_profile("parallel-review")
        plan = _make_plan(self._item("t1"), self._item("t2"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        for item in new_plan.items:
            assert "_binding_reason" in item.adapter_config

    def test_execution_profile_name_on_plan(self) -> None:
        profile = resolve_profile("hands-off")
        plan = _make_plan(self._item("t1"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        assert new_plan.execution_profile == "hands-off"

    def test_combined_plan_first_and_review(self) -> None:
        profile = ExecutionProfile(name="test", plan_first=True, review_gate=True)
        plan = _make_plan(self._item("t1"), self._item("t2"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        ids = [i.temp_id for i in new_plan.items]
        # planning + 2 items + 2 reviews = 5
        assert len(new_plan.items) == 5
        assert "_planning" in ids
        review_items = [i for i in new_plan.items if i.item_type == "review"]
        assert len(review_items) == 2

    def test_lane_limits_none_when_no_profile_limits(self) -> None:
        profile = ExecutionProfile(name="test")
        plan = _make_plan(self._item("t1"))
        _, lane_limits = apply_execution_profile(plan, profile, workflows=[])
        assert lane_limits is None

    def test_preserves_existing_lane(self) -> None:
        profile = ExecutionProfile(name="test", parallel_lanes=True)
        item = self._item("t1", lane="custom_lane")
        plan = _make_plan(item)
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        assert new_plan.items[0].lane == "custom_lane"

    def test_review_gate_has_hold_on_create(self) -> None:
        """Review gates must block via hold_requested so they don't auto-complete."""
        profile = ExecutionProfile(name="test", review_gate=True)
        plan = _make_plan(self._item("t1"))
        new_plan, _ = apply_execution_profile(plan, profile, workflows=[])
        review_items = [i for i in new_plan.items if i.item_type == "review"]
        assert len(review_items) == 1
        assert review_items[0].adapter_config.get("_hold_on_create") is True

    def test_parallel_lanes_match_lane_limits_key(self) -> None:
        """Generated lane names must match lane_limits keys for scheduler enforcement."""
        profile = ExecutionProfile(name="test", parallel_lanes=True, lane_limits={"default": 2})
        plan = _make_plan(self._item("t1"), self._item("t2"), self._item("t3"))
        new_plan, lane_limits = apply_execution_profile(plan, profile, workflows=[])
        for item in new_plan.items:
            if item.lane:
                assert item.lane in (lane_limits or {}), f"Item lane '{item.lane}' not in lane_limits {lane_limits}"

    def test_workflow_path_resolved_not_bare_id(self) -> None:
        """Profile-selected workflows must store resolved paths, not bare IDs."""
        from pathlib import Path

        wf = _StubWorkflow(id="issue_delivery", steps=[_StubStep(runner="cli_claude")])
        profile = ExecutionProfile(name="test", preferred_runners=["cli_claude"])
        plan = _make_plan(self._item("t1"))
        resolved = Path("/pkg/workflows/examples/issue_delivery.yaml")
        with patch(
            "anteroom.services.workflow_resolution.resolve_workflow_path",
            return_value=resolved,
        ):
            new_plan, _ = apply_execution_profile(plan, profile, workflows=[wf])
        path = new_plan.items[0].adapter_config["workflow_path"]
        assert path == str(resolved)
        assert path.endswith(".yaml")


# ---------------------------------------------------------------------------
# preferred_workflow_tags
# ---------------------------------------------------------------------------


class TestPreferredWorkflowTags:
    """Tests for profile-driven workflow tag preferences (tie-breaking)."""

    def test_preferred_tag_field_default_empty(self) -> None:
        p = ExecutionProfile(name="test")
        assert p.preferred_workflow_tags == []

    def test_preferred_tag_field_set(self) -> None:
        p = ExecutionProfile(name="test", preferred_workflow_tags=["review_only"])
        assert p.preferred_workflow_tags == ["review_only"]

    def test_score_bonus_for_matching_tag(self) -> None:
        """Workflow whose tags match preferred_workflow_tags scores higher."""
        wf_match = _StubWorkflow(id="review_wf", tags=["review_only"])
        wf_no_match = _StubWorkflow(id="generic_wf", tags=["general"])
        profile = ExecutionProfile(name="test", preferred_workflow_tags=["review_only"])
        score_match = score_workflow(wf_match, profile)
        score_no = score_workflow(wf_no_match, profile)
        assert score_match > score_no

    def test_score_bonus_for_matching_id(self) -> None:
        """Workflow whose id matches a preferred tag gets a bonus."""
        wf = _StubWorkflow(id="issue_delivery", tags=[])
        profile = ExecutionProfile(name="test", preferred_workflow_tags=["issue_delivery"])
        score_with = score_workflow(wf, profile)
        profile_none = ExecutionProfile(name="test")
        score_without = score_workflow(wf, profile_none)
        assert score_with > score_without

    def test_no_preferred_tags_is_neutral(self) -> None:
        """Without preferred tags the component is neutral (0.5)."""
        wf = _StubWorkflow(id="any", tags=["something"])
        profile = ExecutionProfile(name="test")
        score = score_workflow(wf, profile)
        # Should still produce a valid score
        assert 0.0 <= score <= 1.0

    def test_select_workflow_prefers_tagged(self) -> None:
        """select_workflow picks the workflow matching preferred tags over others."""
        wf_preferred = _StubWorkflow(
            id="issue_delivery", steps=[_StubStep(runner="cli_claude")], tags=["issue_delivery"]
        )
        wf_other = _StubWorkflow(id="generic", steps=[_StubStep(runner="cli_claude")], tags=["generic"])
        profile = ExecutionProfile(
            name="test",
            preferred_runners=["cli_claude"],
            preferred_workflow_tags=["issue_delivery"],
        )
        defn, reason = select_workflow([wf_other, wf_preferred], profile, threshold=0.0)
        assert defn is not None
        assert defn.id == "issue_delivery"

    def test_select_workflow_reason_includes_preferred_tag(self) -> None:
        """Reason string mentions matched preferred tags."""
        wf = _StubWorkflow(id="issue_delivery", steps=[_StubStep(runner="cli_claude")], tags=["issue_delivery"])
        profile = ExecutionProfile(
            name="test",
            preferred_runners=["cli_claude"],
            preferred_workflow_tags=["issue_delivery"],
        )
        defn, reason = select_workflow([wf], profile, threshold=0.0)
        assert defn is not None
        assert "preferred tag" in reason
        assert "issue_delivery" in reason

    def test_builtin_parallel_review_has_tags(self) -> None:
        """parallel-review profile prefers router path."""
        p = resolve_profile("parallel-review")
        assert len(p.preferred_workflow_tags) > 0
        assert "router" in p.preferred_workflow_tags
        assert "work_item_router" in p.preferred_workflow_tags

    def test_builtin_hands_off_has_tags(self) -> None:
        """hands-off profile prefers router path."""
        p = resolve_profile("hands-off")
        assert len(p.preferred_workflow_tags) > 0
        assert "router" in p.preferred_workflow_tags
        assert "work_item_router" in p.preferred_workflow_tags

    def test_binding_reason_includes_profile_name(self) -> None:
        """When a workflow is matched, _binding_reason mentions the profile."""
        from pathlib import Path

        wf = _StubWorkflow(
            id="local_work_item_router",
            steps=[_StubStep(runner="cli_claude")],
            tags=["router", "work_item_router"],
        )
        profile = ExecutionProfile(
            name="hands-off",
            preferred_runners=["cli_claude"],
            preferred_workflow_tags=["router", "work_item_router"],
        )
        plan = CompiledPlan(
            items=[CompiledItem(summary="Task t1", temp_id="t1")],
            title="Test",
        )
        resolved = Path("/workflows/local_work_item_router.yaml")
        with patch(
            "anteroom.services.workflow_resolution.resolve_workflow_path",
            return_value=resolved,
        ):
            new_plan, _ = apply_execution_profile(plan, profile, workflows=[wf])
        reason = new_plan.items[0].adapter_config["_binding_reason"]
        assert "hands-off" in reason
        assert "local_work_item_router" in reason
