"""Tests for _agent_retry_comment_header."""

from agentic_devtools.cli.ci.guards import _agent_retry_comment_header


def test_returns_current_and_legacy_retry_headers() -> None:
    current = "@copilot\n\n<!-- agdt:agent-retry:task-1:1 -->\n<!-- agdt:agent-retry-alias:42 -->\ncontent"
    legacy = "<!-- agdt:agent-retry:task-1:1 -->\n\n@copilot Please resume.\ncontent"

    assert _agent_retry_comment_header(current) == [
        "@copilot",
        "",
        "<!-- agdt:agent-retry:task-1:1 -->",
        "<!-- agdt:agent-retry-alias:42 -->",
    ]
    assert _agent_retry_comment_header(legacy) == [
        "<!-- agdt:agent-retry:task-1:1 -->",
        "",
        "@copilot Please resume.",
        "content",
    ]


def test_does_not_treat_quoted_finding_markers_as_headers() -> None:
    body = "@copilot Please repair this finding.\n\n## Finding\n\n<!-- agdt:agent-retry:task-1:1 -->"

    assert _agent_retry_comment_header(body) == []
    assert _agent_retry_comment_header("") == []


def test_handles_retry_headers_without_metadata() -> None:
    current = "@copilot\n\n<!-- agdt:agent-retry:task-1:1 -->"
    legacy = "<!-- agdt:agent-retry:task-1:1 -->\ncontent"

    assert _agent_retry_comment_header(current) == [
        "@copilot",
        "",
        "<!-- agdt:agent-retry:task-1:1 -->",
    ]
    assert _agent_retry_comment_header(legacy) == ["<!-- agdt:agent-retry:task-1:1 -->"]
