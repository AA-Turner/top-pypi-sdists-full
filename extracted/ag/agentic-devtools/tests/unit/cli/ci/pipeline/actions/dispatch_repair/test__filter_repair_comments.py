"""Tests for _filter_repair_comments()."""

from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import _filter_repair_comments


def _comment(
    comment_id: int,
    *,
    author_login: str = "reviewer",
    body: str = "Fix this",
    in_reply_to_id: int | None = None,
) -> ReviewCommentInfo:
    return ReviewCommentInfo(
        id=comment_id,
        path="src/example.py",
        body=body,
        html_url="https://example.test/comment",
        author_login=author_login,
        in_reply_to_id=in_reply_to_id,
    )


class TestFilterRepairComments:
    """Tests for repair-comment classification."""

    def test_removes_answered_root_and_cloud_agent_reply(self) -> None:
        root = _comment(101)
        reply = _comment(
            202,
            author_login="copilot-swe-agent[bot]",
            body="Implemented.",
            in_reply_to_id=101,
        )

        assert _filter_repair_comments([root, reply]) == []

    def test_removes_cloud_agent_reply_even_when_body_is_empty(self) -> None:
        root = _comment(101)
        reply = _comment(
            202,
            author_login="copilot-swe-agent[bot]",
            body=" ",
            in_reply_to_id=101,
        )

        assert _filter_repair_comments([root, reply]) == [root]

    def test_keeps_reply_with_missing_parent(self) -> None:
        reply = _comment(
            202,
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )

        assert _filter_repair_comments([reply]) == [reply]

    def test_removes_resolved_comments(self) -> None:
        unresolved = _comment(101)
        resolved = _comment(202)

        assert _filter_repair_comments([unresolved, resolved], {202}) == [unresolved]

    def test_cca_reply_to_non_root_does_not_suppress_parent(self) -> None:
        """A CCA reply whose parent is itself a reply (not a root) must not suppress it.

        Only root comments (those with no parent) can be suppressed as
        "answered". When the CCA reply's parent is not a root, the parent
        check fails and the filter fails open — all three comments remain
        eligible rather than silently suppressing a human reply.
        """
        root = _comment(101)
        human_reply = _comment(202, author_login="octocat", in_reply_to_id=101)
        cca_nested = _comment(
            303,
            author_login="copilot-swe-agent[bot]",
            body="Done.",
            in_reply_to_id=202,  # points to human_reply, which is not a root
        )

        result = _filter_repair_comments([root, human_reply, cca_nested])

        # Parent 202 is not a root, so the response contract is unverifiable.
        # Filter fails open: all three comments remain eligible.
        assert result == [root, human_reply, cca_nested]
