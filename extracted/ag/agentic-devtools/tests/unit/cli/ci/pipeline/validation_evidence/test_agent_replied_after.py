import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.validation_evidence import agent_replied_after


def comment(author: str, created_at: str) -> IssueCommentInfo:
    return IssueCommentInfo(id=1, author=author, created_at=created_at)


def test_counts_a_timezone_aware_later_evidence_reply() -> None:
    anchor = comment("human", "2026-10-26T10:00:00+02:00")
    reply = comment("Copilot", "2026-10-26T08:00:01Z")

    assert agent_replied_after([reply], anchor)


@pytest.mark.parametrize(
    ("reply_time", "anchor_time"),
    [
        ("2026-10-26T08:00:00Z", "2026-10-26T08:00:00+00:00"),
        ("2026-10-26T07:59:59Z", "2026-10-26T08:00:00Z"),
        ("not-a-timestamp", "2026-10-26T08:00:00Z"),
        ("2026-13-26T08:00:00Z", "2026-10-26T08:00:00Z"),
        ("2026-10-26T09:00:00", "2026-10-26T08:00:00Z"),
        ("2026-10-26T09:00:00Z", "2026-10-26T08:00:00"),
        ("2026-10-26T09:00:00Z", "2026-13-26T08:00:00Z"),
        ("2026-10-26+09:00", "2026-10-26T08:00:00Z"),
        ("2026-10-26T09:00:00Z", "2026-10-26+08:00"),
    ],
)
def test_rejects_equal_earlier_malformed_or_naive_timestamps(reply_time: str, anchor_time: str) -> None:
    assert not agent_replied_after([comment("Copilot", reply_time)], comment("human", anchor_time))


def test_does_not_count_a_later_comment_from_a_non_evidence_author() -> None:
    anchor = comment("human", "2026-10-26T08:00:00Z")

    assert not agent_replied_after([comment("human-two", "2026-10-26T09:00:00Z")], anchor)
