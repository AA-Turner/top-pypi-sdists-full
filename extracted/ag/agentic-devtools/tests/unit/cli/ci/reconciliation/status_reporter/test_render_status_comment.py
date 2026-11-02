from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.status_reporter import render_status_comment


def test_render_status_comment_contains_marker_and_projection(foundation):
    fixture = foundation()
    fixture.state.findings["finding"] = replace(fixture.state.findings["finding"], disposition="implement_suggestion")
    body = render_status_comment(fixture.state, 42)
    assert "<!-- ai-pr-loop:status -->" in body
    assert "rounds: `1/50`" in body
    assert "suggestion=1" in body
