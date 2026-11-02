from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_issuecommentinfo_preserves_html_url() -> None:
    comment = IssueCommentInfo(
        id=11,
        author="reviewer",
        body="comment",
        html_url="https://github.com/owner/repo/pull/42#issuecomment-11",
    )

    assert comment.html_url == "https://github.com/owner/repo/pull/42#issuecomment-11"
