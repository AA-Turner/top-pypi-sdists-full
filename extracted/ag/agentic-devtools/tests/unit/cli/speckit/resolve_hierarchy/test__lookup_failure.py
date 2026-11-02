"""Tests for fail-closed lookup result classification."""

from agentic_devtools.cli.speckit.resolve_hierarchy import Resolution, _lookup_failure


def test_lookup_failure_exits_for_unknown_and_task_but_preserves_epic() -> None:
    assert _lookup_failure(None) == Resolution("unknown", "", "", "", "lookup-failed", 2)
    assert _lookup_failure({"labels": [], "type": {"name": "Feature"}}) == Resolution(
        "unknown", "", "", "", "lookup-failed", 0
    )
    assert _lookup_failure({"labels": [], "type": {"name": "Task"}}) == Resolution(
        "unknown", "", "", "", "lookup-failed", 2
    )
    assert _lookup_failure({"labels": [], "type": {"name": "Feature"}}, task_resolution=True) == Resolution(
        "unknown", "", "", "", "lookup-failed", 2
    )
    assert _lookup_failure({"labels": [{"name": "epic"}], "type": {"name": "Task"}}) == Resolution(
        "epic", "", "", "", "resolved"
    )
