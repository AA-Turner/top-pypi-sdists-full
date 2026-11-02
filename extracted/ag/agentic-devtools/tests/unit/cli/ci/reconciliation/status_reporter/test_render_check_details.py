from agentic_devtools.cli.ci.reconciliation.status_reporter import render_check_details


def test_render_check_details_has_github_fields(foundation):
    details = render_check_details(foundation().state, 42)
    assert set(details) == {"title", "summary", "text"}
    assert "PR #42" in details["title"]
