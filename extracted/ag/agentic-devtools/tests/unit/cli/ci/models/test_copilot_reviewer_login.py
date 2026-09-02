"""Tests for Copilot reviewer login constants."""

from agentic_devtools.cli.ci.models import (
    COPILOT_COMMENT_LOGINS,
    COPILOT_LOGINS,
    COPILOT_REVIEWER_LOGIN,
    TAKEOVER_HEAD_AUTHOR_LOGINS,
)


class TestCopilotReviewerLogin:
    """Tests for Copilot reviewer login constants in CI models."""

    def test_canonical_login_value(self) -> None:
        assert COPILOT_REVIEWER_LOGIN == "copilot-pull-request-reviewer[bot]"

    def test_canonical_login_in_copilot_login_sets(self) -> None:
        assert COPILOT_REVIEWER_LOGIN in COPILOT_LOGINS
        assert COPILOT_REVIEWER_LOGIN in COPILOT_COMMENT_LOGINS

    def test_bot_identities_are_recognized_in_all_copilot_login_sets(self) -> None:
        for login in ("copilot[bot]", "copilot-swe-agent[bot]"):
            assert login in COPILOT_LOGINS
            assert login in COPILOT_COMMENT_LOGINS

    def test_github_actions_bot_not_in_copilot_logins(self) -> None:
        """github-actions[bot] must not pollute Copilot review-detection sets."""
        assert "github-actions[bot]" not in COPILOT_LOGINS
        assert "github-actions[bot]" not in COPILOT_COMMENT_LOGINS

    def test_takeover_head_author_logins_is_superset_of_copilot_logins(self) -> None:
        """TAKEOVER_HEAD_AUTHOR_LOGINS extends COPILOT_LOGINS with github-actions[bot]."""
        assert COPILOT_LOGINS < TAKEOVER_HEAD_AUTHOR_LOGINS
        assert "github-actions[bot]" in TAKEOVER_HEAD_AUTHOR_LOGINS
