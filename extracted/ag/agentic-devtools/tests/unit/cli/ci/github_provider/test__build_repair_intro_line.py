"""Tests for _build_repair_intro_line()."""

from agentic_devtools.cli.ci.github_provider import _build_repair_intro_line


class TestBuildRepairIntroLine:
    """Tests for the first line of a repair dispatch comment with no comment section."""

    def test_always_begins_with_at_copilot(self) -> None:
        """Every variant must begin with @copilot for reliable agent triggering."""
        variants = [
            _build_repair_intro_line(has_review_context=True),
            _build_repair_intro_line(has_review_context=False),
        ]
        assert all(line.startswith("@copilot") for line in variants)

    def test_review_without_fetched_comments_asks_about_the_review(self) -> None:
        assert _build_repair_intro_line(has_review_context=True) == (
            "@copilot - please evaluate the review that was just left by a Code Review Agent "
            "and address any feedback you find to be valid:"
        )

    def test_no_context_returns_bare_mention(self) -> None:
        assert _build_repair_intro_line(has_review_context=False) == "@copilot"
