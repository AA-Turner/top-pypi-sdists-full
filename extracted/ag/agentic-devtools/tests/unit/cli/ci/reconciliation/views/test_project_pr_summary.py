from agentic_devtools.cli.ci.reconciliation.views import project_pr_summary


def test_project_pr_summary_is_consistent(foundation):
    state = foundation().state
    before = dict(state.obligations)
    view = project_pr_summary(state, 42)
    assert view.obligation_ids == ("problem",)
    assert view.finding_ids == ("finding",)
    assert view.attempt_count == 1
    assert view.rounds_used == 1
    assert state.obligations == before


def test_project_pr_summary_unknown_pr(foundation):
    view = project_pr_summary(foundation().state, 999)
    assert view.stage == "unknown"
    assert view.round_limit == 50
