"""Tests for _find_matching_deferral_comment."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.deferral import _find_matching_deferral_comment


def test_reraises_identity_lookup_failure_in_github_actions(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    provider = MagicMock()
    provider.list_issue_comments.return_value = []
    provider.get_trusted_loop_comment_logins.side_effect = RuntimeError("identity lookup failed")

    with pytest.raises(RuntimeError, match="identity lookup failed"):
        _find_matching_deferral_comment(provider, 42, 7)


def test_skips_malformed_label_without_deferral_marker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"loop-bot"}
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=1, author="loop-bot", body="ordinary text\n🤖 AI PR Loop ·")
    ]

    assert _find_matching_deferral_comment(provider, 42, 7) is None
