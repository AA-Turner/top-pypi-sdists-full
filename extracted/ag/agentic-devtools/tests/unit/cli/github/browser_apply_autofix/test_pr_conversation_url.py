"""Tests for _pr_conversation_url."""

from __future__ import annotations

from agentic_devtools.cli.github.browser_apply_autofix import _pr_conversation_url


class TestPrConversationUrl:
    """Tests for _pr_conversation_url."""

    def test_builds_conversation_url(self) -> None:
        assert _pr_conversation_url("owner/repo", 42) == "https://github.com/owner/repo/pull/42"
