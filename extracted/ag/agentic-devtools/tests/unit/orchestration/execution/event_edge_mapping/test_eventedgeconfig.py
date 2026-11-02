"""Tests for EventEdgeConfig and event-edge mapping infrastructure."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.execution.event_edge_mapping import (
    EventEdgeConfig,
    EventEdgeMappingError,
    EventEdgeRule,
    build_routing_function,
    load_event_edge_mapping,
)


class TestEventEdgeConfig:
    """Tests for EventEdgeConfig dataclass."""

    def test_construction(self) -> None:
        """Valid construction with rules."""
        rule = EventEdgeRule(
            event_name="JIRA_COMMENT_ADDED",
            source_node="planning_node",
            target_node="checklist_node",
            agdt_step_name="checklist-creation",
        )
        config = EventEdgeConfig(rules=(rule,))
        assert len(config.rules) == 1
        assert config.rules[0].event_name == "JIRA_COMMENT_ADDED"


class TestEventEdgeRule:
    """Tests for EventEdgeRule validation."""

    def test_valid_rule(self) -> None:
        """Valid rule passes validation."""
        rule = EventEdgeRule(
            event_name="TASK_DONE",
            source_node="impl_node",
            target_node="verify_node",
            agdt_step_name="verification",
        )
        assert rule.source_node == "impl_node"

    def test_invalid_source_node_raises(self) -> None:
        """Source node with hyphens raises."""
        with pytest.raises(EventEdgeMappingError, match="source_node must use underscores"):
            EventEdgeRule(
                event_name="X",
                source_node="bad-name",
                target_node="ok_name",
                agdt_step_name="ok-step",
            )

    def test_invalid_target_node_raises(self) -> None:
        """Target node with uppercase raises."""
        with pytest.raises(EventEdgeMappingError, match="target_node must use underscores"):
            EventEdgeRule(
                event_name="X",
                source_node="ok_name",
                target_node="BadName",
                agdt_step_name="ok-step",
            )

    def test_invalid_step_name_raises(self) -> None:
        """Step name with underscores raises."""
        with pytest.raises(EventEdgeMappingError, match="agdt_step_name must use hyphens"):
            EventEdgeRule(
                event_name="X",
                source_node="ok_name",
                target_node="ok_target",
                agdt_step_name="bad_step",
            )


class TestLoadEventEdgeMapping:
    """Tests for loading event edge config from YAML."""

    def test_load_valid_yaml(self, tmp_path: Path) -> None:
        """Loads a valid YAML config."""
        yaml_content = """
rules:
  - event_name: TASK_COMPLETE
    source_node: implementation_node
    target_node: verification_node
    agdt_step_name: verification
  - event_name: TESTS_PASS
    source_node: verification_node
    target_node: commit_node
    agdt_step_name: commit
"""
        path = tmp_path / "mapping.yml"
        path.write_text(yaml_content)

        config = load_event_edge_mapping(path)
        assert len(config.rules) == 2
        assert config.rules[0].target_node == "verification_node"

    def test_load_missing_file_raises(self, tmp_path: Path) -> None:
        """Missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_event_edge_mapping(tmp_path / "nonexistent.yml")

    def test_load_malformed_yaml_raises(self, tmp_path: Path) -> None:
        """Malformed YAML raises EventEdgeMappingError."""
        path = tmp_path / "bad.yml"
        path.write_text(": bad: yaml: {{")

        with pytest.raises(EventEdgeMappingError, match="Failed to parse"):
            load_event_edge_mapping(path)

    def test_load_non_dict_raises(self, tmp_path: Path) -> None:
        """Non-dict content raises EventEdgeMappingError."""
        path = tmp_path / "list.yml"
        path.write_text("[1, 2, 3]")

        with pytest.raises(EventEdgeMappingError, match="must be a dict"):
            load_event_edge_mapping(path)


class TestBuildRoutingFunction:
    """Tests for build_routing_function()."""

    def test_matches_rule(self) -> None:
        """Returns target node when rule matches event."""
        rules = (
            EventEdgeRule(
                event_name="DONE",
                source_node="working_node",
                target_node="complete_node",
                agdt_step_name="complete",
            ),
        )
        config = EventEdgeConfig(rules=rules)
        router = build_routing_function(config, "working_node")

        with patch("agentic_devtools.orchestration.execution.event_edge_mapping._sync_workflow_state"):
            target = router({"events": ["DONE"]})
        assert target == "complete_node"

    def test_no_match_returns_default(self) -> None:
        """Returns default_target when no rule matches."""
        rules = (
            EventEdgeRule(
                event_name="DONE",
                source_node="working_node",
                target_node="complete_node",
                agdt_step_name="complete",
            ),
        )
        config = EventEdgeConfig(rules=rules)
        router = build_routing_function(config, "working_node", default_target="end")

        target = router({"events": ["OTHER"]})
        assert target == "end"

    def test_empty_events_returns_default(self) -> None:
        """Returns default_target when no events in state."""
        config = EventEdgeConfig(rules=())
        router = build_routing_function(config, "node_a")

        target = router({"events": []})
        assert target == "end"

    def test_source_node_filter(self) -> None:
        """Only rules for the specified source_node are considered."""
        rules = (
            EventEdgeRule(
                event_name="DONE",
                source_node="other_node",
                target_node="target_a",
                agdt_step_name="step-a",
            ),
            EventEdgeRule(
                event_name="DONE",
                source_node="my_node",
                target_node="target_b",
                agdt_step_name="step-b",
            ),
        )
        config = EventEdgeConfig(rules=rules)
        router = build_routing_function(config, "my_node")

        with patch("agentic_devtools.orchestration.execution.event_edge_mapping._sync_workflow_state"):
            target = router({"events": ["DONE"]})
        assert target == "target_b"
