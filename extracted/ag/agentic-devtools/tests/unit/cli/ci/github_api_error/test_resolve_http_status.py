"""Tests for resolving GitHub API status provenance."""

from agentic_devtools.cli.ci.agent_task_diagnostics import AgentTaskDiagnostics
from agentic_devtools.cli.ci.github_api_error import resolve_http_status


def test_preserves_response_header_status() -> None:
    diagnostics = AgentTaskDiagnostics("/repos/o/r", None, str)
    diagnostics.status = 404
    diagnostics.status_source = "response_headers"

    assert resolve_http_status(diagnostics, 404, "403 Request rejected") == 404
    assert diagnostics.status == 404
    assert diagnostics.status_source == "response_headers"


def test_records_leading_bare_status_from_stderr() -> None:
    diagnostics = AgentTaskDiagnostics("/repos/o/r", None, str)

    assert resolve_http_status(diagnostics, None, "404 Request rejected") == 404
    assert diagnostics.status == 404
    assert diagnostics.status_source == "stderr"


def test_ignores_incidental_status_digits() -> None:
    diagnostics = AgentTaskDiagnostics("/repos/o/r", None, str)

    assert (
        resolve_http_status(diagnostics, None, "GraphQL: failed lookup for https://github.com/o/r/issues/503") is None
    )
    assert diagnostics.status is None
    assert diagnostics.status_source is None
