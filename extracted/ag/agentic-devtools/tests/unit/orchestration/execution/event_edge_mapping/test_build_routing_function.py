"""Tests for build_routing_function() — dict events and _sync_workflow_state."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.orchestration.execution.event_edge_mapping import (
    EventEdgeConfig,
    EventEdgeRule,
    _sync_workflow_state,
    build_routing_function,
)


class TestBuildRoutingFunctionDictEvents:
    """Tests for routing with dict-style events."""

    def test_dict_event_matches(self) -> None:
        """Dict events with 'name' field are matched."""
        rules = (
            EventEdgeRule(
                event_name="COMPLETE",
                source_node="working_node",
                target_node="done_node",
                agdt_step_name="done",
            ),
        )
        config = EventEdgeConfig(rules=rules)
        router = build_routing_function(config, "working_node")

        with patch("agentic_devtools.orchestration.execution.event_edge_mapping._sync_workflow_state"):
            target = router({"events": [{"name": "COMPLETE"}]})
        assert target == "done_node"

    def test_dict_event_no_name_returns_default(self) -> None:
        """Dict events without 'name' don't match any rule."""
        rules = (
            EventEdgeRule(
                event_name="COMPLETE",
                source_node="working_node",
                target_node="done_node",
                agdt_step_name="done",
            ),
        )
        config = EventEdgeConfig(rules=rules)
        router = build_routing_function(config, "working_node")

        target = router({"events": [{"type": "COMPLETE"}]})
        assert target == "end"

    def test_missing_events_key_returns_default(self) -> None:
        """State without 'events' key returns default target."""
        config = EventEdgeConfig(rules=())
        router = build_routing_function(config, "node_a")

        target = router({})
        assert target == "end"

    def test_non_list_events_returns_default(self) -> None:
        """Non-list truthy events value returns default target."""
        config = EventEdgeConfig(rules=())
        router = build_routing_function(config, "node_a")

        # events is a truthy non-list — latest_event becomes None
        target = router({"events": "not_a_list"})
        assert target == "end"

    def test_non_dict_non_str_event_returns_default(self) -> None:
        """Event that is neither str nor dict returns default_target without raising."""
        rules = (
            EventEdgeRule(
                event_name="COMPLETE",
                source_node="node_a",
                target_node="done_node",
                agdt_step_name="done",
            ),
        )
        config = EventEdgeConfig(rules=rules)
        router = build_routing_function(config, "node_a")

        # list, int, and Exception objects are all non-str/non-dict
        for bad_event in ([{"name": "COMPLETE"}], 42, RuntimeError("boom")):
            target = router({"events": [bad_event]})
            assert target == "end", f"Expected 'end' for event type {type(bad_event).__name__}"


class TestSyncWorkflowState:
    """Tests for _sync_workflow_state() error handling."""

    def test_exception_is_swallowed(self) -> None:
        """Exceptions in _sync_workflow_state don't propagate."""
        with patch(
            "agentic_devtools.state.update_workflow_step",
            side_effect=RuntimeError("state error"),
        ):
            # Should not raise
            _sync_workflow_state("some-step")

    def test_successful_sync(self) -> None:
        """Successful sync calls update_workflow_step."""
        with patch("agentic_devtools.state.update_workflow_step") as mock_update:
            _sync_workflow_state("my-step")
        mock_update.assert_called_once_with("my-step")
