"""Tests for EpicRow in generate_epic_progress_report."""

from __future__ import annotations

from tests.scripts.generate_epic_progress_report import NOW, PREV_RUN_AT, _node, report


def _make_row(epic):
    return report.EpicRow(
        metrics=report.compute_metrics(epic),
        max_updated=None,
        prev=None,
        prev_run_at=None,
        open_failed=[],
        blocked=[],
        anomalies=[],
    )


def _make_row_with_prev(epic, *, closed_tasks: int = 0, truncated: bool = False):
    """Build a row with a baseline and optionally truncate the child list."""
    if truncated:
        epic = report.Node(
            number=epic.number,
            title=epic.title,
            state=epic.state,
            updated_at=epic.updated_at,
            labels=epic.labels,
            assignees=epic.assignees,
            children=epic.children,
            child_total=epic.child_total + 99,
        )
    return report.EpicRow(
        metrics=report.compute_metrics(epic),
        max_updated=PREV_RUN_AT,
        prev={"closed_tasks": closed_tasks, "closed_features": 0},
        prev_run_at=NOW,
        open_failed=[],
        blocked=[],
        anomalies=[],
    )


def test_truncated_is_false_when_child_totals_match():
    """Returns False when epic and all features have complete child lists."""
    task = _node(301)
    feature = _node(201, children=[task])
    epic = _node(101, children=[feature])
    row = _make_row(epic)
    assert row.truncated is False


def test_truncated_is_true_when_epic_child_total_exceeds_fetched_count():
    """Returns True when the epic has more features than were fetched."""
    feature = _node(201)
    epic = _node(101, children=[feature], child_total=5)
    row = _make_row(epic)
    assert row.truncated is True


def test_truncated_is_true_when_feature_child_total_exceeds_fetched_count():
    """Returns True when any feature has more tasks than were fetched."""
    task = _node(301)
    feature = _node(201, children=[task], child_total=10)
    epic = _node(101, children=[feature])
    row = _make_row(epic)
    assert row.truncated is True


def test_stalled_is_true_when_no_progress_and_complete_data():
    """Reports stalled=True when delta_tasks==0 and data is not truncated."""
    task = _node(301, state="CLOSED")
    feature = _node(201, children=[task])
    epic = _node(101, children=[feature])
    row = _make_row_with_prev(epic, closed_tasks=1)
    assert row.stalled is True


def test_stalled_is_false_when_truncated():
    """Reports stalled=False when the child list is truncated, even with delta==0."""
    task = _node(301, state="CLOSED")
    feature = _node(201, children=[task])
    epic = _node(101, children=[feature])
    row = _make_row_with_prev(epic, closed_tasks=1, truncated=True)
    assert row.stalled is False
