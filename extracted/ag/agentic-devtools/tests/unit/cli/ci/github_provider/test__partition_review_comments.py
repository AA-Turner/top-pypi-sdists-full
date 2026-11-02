"""Tests for _partition_review_comments()."""

from agentic_devtools.cli.ci.github_provider import _partition_review_comments
from agentic_devtools.cli.ci.models import ReviewCommentInfo

_ANCHORED = ReviewCommentInfo(
    id=101,
    path="src/foo.py",
    body="Fix the null check here",
    html_url="https://github.com/owner/repo/pull/42#discussion_r101",
)
_ANCHORED_OTHER = ReviewCommentInfo(
    id=102,
    path="src/bar.py",
    body="Use a helper function",
    html_url="https://github.com/owner/repo/pull/42#discussion_r102",
)
_ANCHORED_SUPPRESSED = ReviewCommentInfo(
    id=103,
    path="src/baz.py",
    body="Subjective style preference",
    html_url="https://github.com/owner/repo/pull/42#discussion_r103",
    is_suppressed=True,
)
_BODY_ONLY = ReviewCommentInfo(
    id=0,
    path="docs/state-keys.md",
    body="This key is documented but never written",
    html_url="",
    is_suppressed=True,
)
_BODY_ONLY_OTHER = ReviewCommentInfo(
    id=0,
    path="docs/README.md",
    body="This paragraph contradicts the one above",
    html_url="",
    is_suppressed=True,
)
_UNANCHORED_NOT_SUPPRESSED = ReviewCommentInfo(
    id=104,
    path="src/qux.py",
    body="No anchor and not suppressed",
    html_url="",
)


class TestPartitionReviewComments:
    """Tests for splitting review comments into the two dispatch sections."""

    def test_body_only_suppressed_comment_is_an_author_comment(self) -> None:
        """The author section is exactly the comments with no anchor of their own."""
        author, agent = _partition_review_comments([_BODY_ONLY])
        assert author == [_BODY_ONLY]
        assert agent == []

    def test_anchored_comment_is_a_code_review_agent_comment(self) -> None:
        author, agent = _partition_review_comments([_ANCHORED])
        assert author == []
        assert agent == [_ANCHORED]

    def test_anchored_but_suppressed_comment_stays_with_the_code_review_agent(self) -> None:
        """Keying on ``is_suppressed`` alone would strip a real ``#discussion_r`` anchor."""
        author, agent = _partition_review_comments([_ANCHORED_SUPPRESSED])
        assert author == []
        assert agent == [_ANCHORED_SUPPRESSED]

    def test_unanchored_but_unsuppressed_comment_stays_with_the_code_review_agent(self) -> None:
        author, agent = _partition_review_comments([_UNANCHORED_NOT_SUPPRESSED])
        assert author == []
        assert agent == [_UNANCHORED_NOT_SUPPRESSED]

    def test_each_list_preserves_the_input_relative_order(self) -> None:
        author, agent = _partition_review_comments(
            [_ANCHORED, _BODY_ONLY, _ANCHORED_OTHER, _BODY_ONLY_OTHER, _ANCHORED_SUPPRESSED]
        )
        assert author == [_BODY_ONLY, _BODY_ONLY_OTHER]
        assert agent == [_ANCHORED, _ANCHORED_OTHER, _ANCHORED_SUPPRESSED]

    def test_empty_input_yields_two_empty_lists(self) -> None:
        assert _partition_review_comments([]) == ([], [])
