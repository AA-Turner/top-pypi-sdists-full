"""Tests for _shared_decision_block()."""

from agentic_devtools.cli.ci.github_provider import _shared_decision_block

_INTRO = (
    "I don't want you to blindly implement the suggestions. Instead, please evaluate each comment against the "
    "codebase and address it with code changes only if you believe that doing so would increase the overall "
    "quality of the code changes in this PR. It is also possible that a comment points out a valid problem "
    "with the code, but either does not suggest the optimal solution, or the suggested solution is out of "
    "scope for the current PR and the related issue (if there is one). Therefore, for each comment you have "
    "4 options:"
)


class TestSharedDecisionBlock:
    """Tests for the four-option decision framework shared by both comment sections."""

    def test_emits_its_own_heading_after_a_leading_blank(self) -> None:
        entries = _shared_decision_block()
        assert entries[0] == ""
        assert entries[1] == "## How to decide on each comment"
        assert entries[2] == ""

    def test_carries_the_full_framework_intro(self) -> None:
        assert _shared_decision_block()[3] == _INTRO

    def test_carries_all_four_options_in_order(self) -> None:
        entries = _shared_decision_block()
        assert entries[4] == ""
        assert entries[5] == (
            "1. Accept the comment and implement it as suggested. Where the comment identifies a problem "
            "without proposing a specific fix, implement the fix you judge best."
        )
        assert entries[6] == (
            "2. Accept the problem pointed out by the comment, but reject the solution as suboptimal, and "
            "instead implement the optimal solution."
        )
        assert entries[7] == (
            "3. Reject that a real problem has been identified by the comment, and assert that the related "
            "code is better left as is."
        )
        assert entries[8] == (
            "4. Accept the problem pointed out by the comment, but classify it as out of scope for the current "
            "PR and the related issue (if there is one). In this case a follow-up issue should be created."
        )
        assert len(entries) == 9

    def test_option_one_accommodates_a_comment_that_proposes_no_fix(self) -> None:
        """Author comments are recovered from review prose and often propose no concrete fix."""
        assert "implement the fix you judge best" in _shared_decision_block()[5]

    def test_carries_no_section_specific_reply_contract(self) -> None:
        """Reply/resolve mechanics are the only thing that differs between the two sections."""
        joined = "\n".join(_shared_decision_block())
        assert "reply to each one" not in joined
        assert "summary comment you post on the PR" not in joined
