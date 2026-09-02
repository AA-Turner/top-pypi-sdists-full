"""Tests for _select_repairable_thread_owner_reviews."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import (
    _select_repairable_thread_owner_reviews,
)
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot


class TestSelectRepairableThreadOwnerReviews:
    """Tests for _select_repairable_thread_owner_reviews."""

    def test_returns_input_when_lookup_not_callable(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id = None
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_when_lookup_raises(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("boom")
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_when_no_unresolved_comments(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_when_comment_fetch_fails(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_review_comments.side_effect = RuntimeError("comments boom")
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_when_no_owners_match(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=202, path="a.py", body="not in unresolved thread", html_url="")
        ]
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert list(comments_cache) == [10]

    def test_returns_input_when_thread_states_not_dict(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = "not-a-dict"
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_on_malformed_entry_non_tuple_state(self) -> None:
        """Fall back when any entry is not a (bool, tuple) pair."""
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": "malformed",
        }
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_on_malformed_entry_non_int_comment_id(self) -> None:
        """Fall back when any entry has a non-integer comment ID."""
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (False, ("bad-id",)),
        }
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_returns_input_on_malformed_entry_negative_comment_id(self) -> None:
        """Fall back when any entry has a negative comment ID."""
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (False, (-5,)),
        }
        snapshot = PRStateSnapshot(pr_number=42)
        reviews = [ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")]

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, reviews)

        assert owners == reviews
        assert comments_cache == {}

    def test_selects_owning_review_when_valid_mapping(self) -> None:
        """Narrow to the review that owns an unresolved comment."""
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        review_10 = ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="sha")
        review_20 = ReviewInfo(id=20, user="Copilot", state="COMMENTED", commit_sha="sha")

        def comments_for(pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
            if review_id == 10:
                return [ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url="")]
            return [ReviewCommentInfo(id=202, path="b.py", body="unrelated", html_url="")]

        provider.list_review_comments.side_effect = comments_for
        snapshot = PRStateSnapshot(pr_number=42)

        owners, _ = _select_repairable_thread_owner_reviews(provider, snapshot, [review_10, review_20])

        assert owners == [review_10]

    def test_does_not_select_review_containing_only_answered_cloud_reply(self) -> None:
        """A Cloud Coding Agent reply and its answered root cannot own a repair."""
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 202))}
        review = ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="sha")
        root = ReviewCommentInfo(
            id=101,
            path="a.py",
            body="fix this",
            html_url="",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="a.py",
            body="Implemented.",
            html_url="",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        provider.list_review_comments.return_value = [root, reply]
        snapshot = PRStateSnapshot(pr_number=42)

        owners, comments_cache = _select_repairable_thread_owner_reviews(provider, snapshot, [review])

        assert owners == []
        assert comments_cache == {10: []}
