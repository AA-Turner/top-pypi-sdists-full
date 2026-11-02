"""Tests for normalize_provider (issue #2117)."""

import pytest

from agentic_devtools.cli.jira.create_epic_router import normalize_provider


@pytest.mark.parametrize(
    "raw,expected",
    [
        (None, None),
        ("github", "github"),
        ("JIRA", "jira"),
        ("  GitHub  ", "github"),
        ("Markdown", "markdown"),
        ("", ""),
    ],
)
def test_normalize_provider(raw, expected):
    assert normalize_provider(raw) == expected
