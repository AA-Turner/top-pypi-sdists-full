import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.validation_evidence import (
    BLOCKER_MARKER,
    find_marker_comment,
)


def comment(author: str, body: str) -> IssueCommentInfo:
    return IssueCommentInfo(id=1, author=author, body=body)


def test_matches_only_an_unquoted_whole_marker_line() -> None:
    quoted = comment("human-one", f"> {BLOCKER_MARKER}")
    embedded = comment("human-two", f"Prefix {BLOCKER_MARKER} suffix")
    fenced = comment("human-four", f"```text\n{BLOCKER_MARKER}\n```")
    eligible = comment("human-three", f"Status\n{BLOCKER_MARKER}\nDone")

    assert find_marker_comment([quoted, embedded, fenced, eligible], BLOCKER_MARKER) is eligible


@pytest.mark.parametrize("invalid_closer", ["```", "````python"])
def test_ignores_marker_inside_fence_after_invalid_closer(invalid_closer: str) -> None:
    fenced = comment("human", f"````text\n{invalid_closer}\n{BLOCKER_MARKER}\n````")

    assert find_marker_comment([fenced], BLOCKER_MARKER) is None


def test_ignores_marker_after_four_space_indented_closer() -> None:
    fenced = comment("human", f"```\n    ```\n{BLOCKER_MARKER}")

    assert find_marker_comment([fenced], BLOCKER_MARKER) is None


def test_recognizes_marker_after_inline_code_span() -> None:
    fenced = comment("human", f"```example```\n{BLOCKER_MARKER}")

    assert find_marker_comment([fenced], BLOCKER_MARKER) is fenced


def test_recognizes_marker_after_closing_fence_with_trailing_whitespace() -> None:
    fenced = comment("human", f"````text\nexample\n````  \t\n{BLOCKER_MARKER}")

    assert find_marker_comment([fenced], BLOCKER_MARKER) is fenced


def test_excludes_copilot_and_evidence_authors_and_returns_first_human_marker() -> None:
    copilot = comment("Copilot", BLOCKER_MARKER)
    coding_agent = comment("copilot-swe-agent", BLOCKER_MARKER)
    first_human = comment("human-one", BLOCKER_MARKER)
    second_human = comment("human-two", BLOCKER_MARKER)

    assert find_marker_comment([copilot, coding_agent, first_human, second_human], BLOCKER_MARKER) is first_human


def test_returns_none_when_no_eligible_comment_has_the_marker() -> None:
    assert find_marker_comment([comment("human", "no marker")], BLOCKER_MARKER) is None
