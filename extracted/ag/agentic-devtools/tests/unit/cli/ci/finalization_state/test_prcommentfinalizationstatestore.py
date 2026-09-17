"""Tests for PRCommentFinalizationStateStore."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.finalization_state import (
    FinalizedReviewKey,
    PRCommentFinalizationStateStore,
)
from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_is_terminal_returns_true_for_matching_review_key() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=1,
            author="copilot",
            body='<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":7} -->',
        )
    ]
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is True


def test_is_terminal_trusts_only_pr_token_author_when_available() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "trusted-bot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=1,
            author="another-user",
            body='<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":7} -->',
        )
    ]
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is False


def test_is_terminal_returns_false_when_pr_token_author_lookup_fails() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.side_effect = RuntimeError("boom")
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is False
    provider.list_issue_comments.assert_not_called()


def test_is_terminal_returns_false_when_pr_token_author_is_empty() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = ""
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is False
    provider.list_issue_comments.assert_not_called()


def test_is_terminal_returns_false_for_non_matching_review_key() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=2, author="copilot", body="non marker"),
        IssueCommentInfo(
            id=1,
            author="copilot",
            body='<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":8} -->',
        ),
    ]
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is False


def test_is_terminal_fails_open_when_state_is_unavailable() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.side_effect = RuntimeError("boom")
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is False


def test_is_terminal_uses_provider_cache_for_repeat_lookups() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=1,
            author="copilot",
            body='<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":7} -->',
        )
    ]
    store = PRCommentFinalizationStateStore(provider)

    first = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))
    second = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert first is True
    assert second is True
    provider.list_issue_comments.assert_called_once_with(42)


def test_is_terminal_ignores_non_set_cached_value_and_refetches() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider._finalized_review_keys_cache = {42: ("invalid",)}
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=1,
            author="copilot",
            body='<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":7} -->',
        )
    ]
    store = PRCommentFinalizationStateStore(provider)

    result = store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7))

    assert result is True
    provider.list_issue_comments.assert_called_once_with(42)


def test_mark_terminal_posts_review_marker() -> None:
    provider = MagicMock()
    store = PRCommentFinalizationStateStore(provider)

    store.mark_terminal(
        key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7),
        reason="verified",
    )

    provider.post_comment_as_pr_token.assert_called_once()
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert '"repo": "owner/repo"' in body
    assert '"pr": 42' in body
    assert '"review_id": 7' in body
    assert '"reason": "verified"' in body


def test_mark_terminal_updates_provider_cache() -> None:
    provider = MagicMock()
    store = PRCommentFinalizationStateStore(provider)
    key = FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7)

    store.mark_terminal(key=key, reason="verified")

    assert getattr(provider, "_finalized_review_keys_cache")[42] == {key}


def test_mark_terminal_updates_existing_provider_cache() -> None:
    provider = MagicMock()
    existing_key = FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7)
    provider._finalized_review_keys_cache = {42: {existing_key}}
    store = PRCommentFinalizationStateStore(provider)
    new_key = FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=8)

    store.mark_terminal(key=new_key, reason="verified")

    assert getattr(provider, "_finalized_review_keys_cache")[42] == {existing_key, new_key}


def test_mark_terminal_swallows_provider_errors() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.return_value = []
    provider.post_comment_as_pr_token.side_effect = RuntimeError("boom")
    store = PRCommentFinalizationStateStore(provider)

    store.mark_terminal(
        key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=7),
        reason="verified",
    )


def test_mark_terminal_handles_comment_search_error() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.side_effect = RuntimeError("list failed")
    store = PRCommentFinalizationStateStore(provider)

    store.mark_terminal(
        key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=102),
        reason="verified",
    )

    provider.post_comment_as_pr_token.assert_called_once()


def test_mark_terminal_appends_to_legacy_blank_comment_and_adds_header() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    legacy_body = '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":101} -->'
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=997, author="copilot", body=legacy_body),
        IssueCommentInfo(id=998, author="copilot", body="regular text without marker"),
        IssueCommentInfo(id=999, author="other-user", body="some other comment"),
    ]
    store = PRCommentFinalizationStateStore(provider)

    store.mark_terminal(
        key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=102),
        reason="verified",
    )

    provider.update_comment.assert_called_once()
    updated = provider.update_comment.call_args.args[1]
    assert "### 🤖 AI PR Loop State & Finalized Reviews" in updated
    assert "101" in updated
    assert "102" in updated


def test_is_terminal_parses_multiple_markers_in_single_comment() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    multi_body = (
        "### 🤖 AI PR Loop State & Finalized Reviews\n"
        "<!-- ai-pr-loop:finalized-review not-json -->\n"
        '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":101} -->\n'
        '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":102} -->\n'
        '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":103} -->'
    )
    provider.list_issue_comments.return_value = [IssueCommentInfo(id=1, author="copilot", body=multi_body)]
    store = PRCommentFinalizationStateStore(provider)

    assert store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=101)) is True
    assert store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=102)) is True
    assert store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=103)) is True
    assert store.is_terminal(key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=104)) is False


def test_mark_terminal_appends_to_existing_tracking_comment() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    existing_body = (
        "### 🤖 AI PR Loop State & Finalized Reviews\n"
        "<!-- agdt:ai-pr-loop-tracking -->\n\n"
        '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":101} -->'
    )
    provider.list_issue_comments.return_value = [IssueCommentInfo(id=999, author="copilot", body=existing_body)]
    store = PRCommentFinalizationStateStore(provider)

    store.mark_terminal(
        key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=102),
        reason="verified",
    )

    provider.update_comment.assert_called_once()
    assert provider.update_comment.call_args.args[0] == 999
    updated = provider.update_comment.call_args.args[1]
    assert "101" in updated
    assert "102" in updated
    provider.post_comment_as_pr_token.assert_not_called()


def test_mark_terminal_creates_comment_with_visible_header_when_none_exists() -> None:
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "copilot"
    provider.list_issue_comments.return_value = []
    store = PRCommentFinalizationStateStore(provider)

    store.mark_terminal(
        key=FinalizedReviewKey(repository="owner/repo", pr_number=42, review_id=201),
        reason="verified",
    )

    provider.post_comment_as_pr_token.assert_called_once()
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert "### 🤖 AI PR Loop State & Finalized Reviews" in body
    assert "<!-- agdt:ai-pr-loop-tracking -->" in body
    assert '"review_id": 201' in body
