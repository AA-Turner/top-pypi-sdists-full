"""Tests for the NoChangePRBrief dataclass."""

import dataclasses

import pytest

from agentic_devtools.cli.ci.models import NoChangePRBrief


class TestNoChangePRBrief:
    """Tests for the NoChangePRBrief dataclass."""

    def test_required_fields(self) -> None:
        brief = NoChangePRBrief(
            number=42,
            author_login="copilot-swe-agent[bot]",
            body="body",
            changed_files=0,
            additions=0,
            deletions=0,
        )
        assert brief.number == 42
        assert brief.author_login == "copilot-swe-agent[bot]"
        assert brief.body == "body"
        assert brief.changed_files == 0
        assert brief.additions == 0
        assert brief.deletions == 0

    def test_default_values(self) -> None:
        brief = NoChangePRBrief(
            number=1,
            author_login="a",
            body="",
            changed_files=1,
            additions=2,
            deletions=3,
        )
        assert brief.head_branch == ""
        assert brief.is_cross_repository is False

    def test_with_all_fields(self) -> None:
        brief = NoChangePRBrief(
            number=7,
            author_login="a",
            body="b",
            changed_files=0,
            additions=0,
            deletions=0,
            head_branch="copilot/triage-1240",
            is_cross_repository=True,
        )
        assert brief.head_branch == "copilot/triage-1240"
        assert brief.is_cross_repository is True

    def test_is_frozen(self) -> None:
        brief = NoChangePRBrief(
            number=1,
            author_login="a",
            body="",
            changed_files=0,
            additions=0,
            deletions=0,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            brief.number = 2  # type: ignore[misc]
