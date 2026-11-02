"""Tests for reject_trigger comment generation."""

from agentic_devtools.hierarchy.enforcement import reject_trigger


class TestRejectTrigger:
    """Tests for rejection comment generation."""

    def test_generates_comment_with_owner_repo(self) -> None:
        comment = reject_trigger(101, 100, owner="org", repo="my-repo")
        assert "#100" in comment
        assert "org/my-repo#100" in comment
        assert "SpecKit trigger rejected" in comment
        assert "parent" in comment.lower()

    def test_generates_comment_without_owner_repo(self) -> None:
        comment = reject_trigger(101, 100)
        assert "#100" in comment
        assert "SpecKit trigger rejected" in comment

    def test_includes_guidance(self) -> None:
        comment = reject_trigger(101, 100)
        assert "re-apply" in comment.lower() or "speckit" in comment.lower()

    def test_incorporates_issue_number(self) -> None:
        comment = reject_trigger(101, 100)
        assert "#101" in comment
