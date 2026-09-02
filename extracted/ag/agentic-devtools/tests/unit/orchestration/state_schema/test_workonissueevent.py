"""Tests for WorkOnIssueEvent TypedDict schema."""

from typing import get_type_hints

from agentic_devtools.orchestration.state_schema import WorkOnIssueEvent


class TestWorkOnIssueEvent:
    """Tests for WorkOnIssueEvent TypedDict."""

    def test_can_instantiate_with_required_fields(self):
        event: WorkOnIssueEvent = {"event": "test_event", "timestamp": "2024-01-01T00:00:00Z"}
        assert event["event"] == "test_event"
        assert event["timestamp"] == "2024-01-01T00:00:00Z"

    def test_schema_fields_include_event_timestamp_and_signals(self):
        hints = get_type_hints(WorkOnIssueEvent, include_extras=True)
        assert set(hints.keys()) == {"event", "timestamp", "signals"}

    def test_event_field_is_str(self):
        hints = get_type_hints(WorkOnIssueEvent, include_extras=True)
        assert hints["event"] is str

    def test_timestamp_field_is_str(self):
        hints = get_type_hints(WorkOnIssueEvent, include_extras=True)
        assert hints["timestamp"] is str

    def test_signals_field_is_optional(self):
        """Signals field is NotRequired — events can omit it."""
        event: WorkOnIssueEvent = {"event": "test", "timestamp": "2024-01-01T00:00:00Z"}
        assert "signals" not in event

    def test_signals_field_accepts_dict(self):
        """Signals field can be populated with a dict."""
        event: WorkOnIssueEvent = {
            "event": "planning_completed",
            "timestamp": "2024-01-01T00:00:00Z",
            "signals": {"plan_posted": True},
        }
        assert event["signals"] == {"plan_posted": True}
