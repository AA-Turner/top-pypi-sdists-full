"""Tests for _author_shortfall_notice()."""

from agentic_devtools.cli.ci.github_provider import _author_shortfall_notice


class TestAuthorShortfallNotice:
    """Tests for the notice naming undelivered author comments."""

    def test_names_the_declared_and_recovered_counts(self) -> None:
        entries = _author_shortfall_notice(
            declared=4,
            recovered=1,
            repository_full_name="owner/repo",
            pr_number=42,
            review_id=99,
        )
        assert entries[1].startswith("_4 findings were declared in the review but 1 could be recovered.")

    def test_leads_with_a_blank_entry_and_emits_one_content_line(self) -> None:
        """Blank-line ownership: the unit owns its leading blank and never a trailing one."""
        entries = _author_shortfall_notice(
            declared=2,
            recovered=0,
            repository_full_name="owner/repo",
            pr_number=42,
            review_id=99,
        )
        assert len(entries) == 2
        assert entries[0] == ""
        assert entries[1].endswith("_")

    def test_includes_the_review_body_fetch_command(self) -> None:
        entries = _author_shortfall_notice(
            declared=3,
            recovered=0,
            repository_full_name="owner/repo",
            pr_number=42,
            review_id=99,
        )
        assert "gh api \"repos/owner/repo/pulls/42/reviews/99\" --jq '.body'" in entries[1]

    def test_omits_the_command_when_the_repository_is_unknown(self) -> None:
        entries = _author_shortfall_notice(
            declared=3,
            recovered=0,
            repository_full_name="",
            pr_number=42,
            review_id=99,
        )
        assert "gh api" not in entries[1]
        assert entries[1] == "_3 findings were declared in the review but 0 could be recovered._"

    def test_omits_the_command_when_the_repository_has_no_slash(self) -> None:
        entries = _author_shortfall_notice(
            declared=3,
            recovered=0,
            repository_full_name="repo",
            pr_number=42,
            review_id=99,
        )
        assert "gh api" not in entries[1]

    def test_omits_the_command_when_the_pr_number_is_unknown(self) -> None:
        entries = _author_shortfall_notice(
            declared=3,
            recovered=0,
            repository_full_name="owner/repo",
            pr_number=0,
            review_id=99,
        )
        assert "gh api" not in entries[1]

    def test_omits_the_command_when_the_review_id_is_unknown(self) -> None:
        entries = _author_shortfall_notice(
            declared=3,
            recovered=0,
            repository_full_name="owner/repo",
            pr_number=42,
            review_id=0,
        )
        assert "gh api" not in entries[1]

    def test_uses_singular_noun_and_verb_when_declared_is_one(self) -> None:
        entries = _author_shortfall_notice(
            declared=1,
            recovered=0,
            repository_full_name="owner/repo",
            pr_number=42,
            review_id=99,
        )
        assert entries[1].startswith("_1 finding was declared in the review but 0 could be recovered.")
