"""Tests for render_report in generate_epic_progress_report."""

from __future__ import annotations

from tests.scripts.generate_epic_progress_report import NOW, PREV_RUN_AT, _node, report

# A timestamp older than PREV_RUN_AT so that subtree_max_updated() returns a value
# that does NOT count as activity after the previous run.
_OLD_UPDATED = "2026-07-08T00:00:00Z"


def _old_node(number, *, state="OPEN", labels=None, children=None, child_total=None):
    """Like _node() but with updated_at set before PREV_RUN_AT to suppress activity."""
    nodes = [] if children is None else children
    return report.Node(
        number=number,
        title=f"Issue {number}",
        state=state,
        updated_at=_OLD_UPDATED,
        labels=[] if labels is None else labels,
        assignees=[],
        children=nodes,
        child_total=len(nodes) if child_total is None else child_total,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _rows(epics, prev_state=None):
    return report.build_rows(epics, NOW, prev_state or {})


def _render(rows, prev_state=None, *, show_details=False):
    return report.render_report("swai-factory", "agentic-devtools", rows, NOW, prev_state or {}, show_details)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_render_report_baseline_run_shows_title_and_no_delta_message():
    """First run (no prev_state) shows the correct title and a baseline notice."""
    task = _node(301, state="CLOSED")
    feature = _node(201, children=[task])
    epic = _node(101, children=[feature])
    rows = _rows([epic])
    output = _render(rows)

    assert "# 📊 AI PR Loop — Epic Progress Report" in output
    assert "baseline; deltas start next run" in output


def test_render_report_subsequent_run_shows_delta_counts():
    """Second run with a prior baseline shows per-epic (+N) deltas."""
    task_prev = _old_node(301, state="CLOSED")
    task_new = _old_node(302, state="CLOSED")
    feature = _old_node(201, children=[task_prev, task_new])
    epic = _old_node(101, children=[feature])

    prev_state = {
        "generated_at": PREV_RUN_AT.isoformat(),
        "epics": {"101": {"closed_tasks": 1, "closed_features": 0}},
    }
    rows = _rows([epic], prev_state)
    output = _render(rows, prev_state)

    # Overall delta line and per-epic delta should both appear.
    assert f"Since {PREV_RUN_AT.date().isoformat()}" in output
    assert "(+1)" in output


def test_render_report_stalled_epic_shows_stall_marker():
    """An epic with no new progress since the baseline is flagged with 🛑."""
    # One closed task, one open task — pct < 100 so stall detection applies.
    task_closed = _old_node(301, state="CLOSED")
    task_open = _old_node(302, state="OPEN")
    feature = _old_node(201, children=[task_closed, task_open])
    epic = _old_node(101, children=[feature])

    # Baseline records the same closed_tasks count as the current run.
    prev_state = {
        "generated_at": PREV_RUN_AT.isoformat(),
        "epics": {"101": {"closed_tasks": 1, "closed_features": 0}},
    }
    rows = _rows([epic], prev_state)
    assert rows[0].stalled, "precondition: row must be stalled for this test to be meaningful"

    output = _render(rows, prev_state)
    assert "🛑" in output


def test_render_report_truncation_warning_shown_when_child_list_incomplete():
    """When an epic or feature has more children than were fetched a warning is included."""
    # child_total=5 but only 0 children fetched → truncation detected.
    epic = _node(101, child_total=5)
    rows = _rows([epic])
    output = _render(rows)

    assert "counts may be underreported and percentages/deltas may be inaccurate for" in output
    assert "#101" in output
