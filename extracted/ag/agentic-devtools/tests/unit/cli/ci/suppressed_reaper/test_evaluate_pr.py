"""Tests for suppressed_reaper.evaluate_pr().

Every documented no-close case from the reaper's acceptance criteria is asserted
here: the string filters are never sufficient on their own, and the empty diff is
never sufficient on its own either.
"""

from __future__ import annotations

from agentic_devtools.cli.ci.models import IssueCommentInfo, IssueFacts, PRTreeState
from agentic_devtools.cli.ci.suppressed_reaper import build_deferral_issue_comment, evaluate_pr
from tests.unit.cli.ci.suppressed_reaper._fixtures import (
    ISSUE,
    MARKER,
    REVIEW_ID,
    SENTINEL,
    TABLE,
    brief,
    issue_body,
    pr_body,
    provider,
)


class TestEvaluatePrCloses:
    """The eligible path — all five conditions hold."""

    def test_eligible_pr_is_closable(self) -> None:
        """A contract-conforming empty-diff PR is eligible and carries its table."""
        decision = evaluate_pr(provider(), brief())
        assert decision.should_close is True
        assert decision.reason == "eligible"
        assert decision.deferred_issue == ISSUE
        assert decision.verdict_table is not None
        assert decision.evaluated_head_sha == "h" * 40
        assert "`valid-no-action`" in decision.verdict_table

    def test_citations_are_resolved_at_the_merge_base(self) -> None:
        """Non-stale rows are resolved against the merge base, stale rows are not."""
        mock = provider()
        evaluate_pr(mock, brief())
        mock.get_file_line_count.assert_called_once_with("b" * 40, "specs/spec.md")


class TestEvaluatePrRefusesToClose:
    """Each acceptance case that must leave the PR open."""

    def test_empty_diff_without_marker(self) -> None:
        """An empty diff alone never closes a PR."""
        decision = evaluate_pr(provider(), brief(body=pr_body(marker=False)))
        assert (decision.should_close, decision.reason) == (False, "no-marker")

    def test_marker_with_non_empty_diff(self) -> None:
        """The marker beside a real diff is a contract violation, not a close."""
        decision = evaluate_pr(provider(), brief(changed_files=1, additions=3, deletions=1))
        assert (decision.should_close, decision.reason) == (False, "non-empty-diff")

    def test_additions_only_diff_is_rejected(self) -> None:
        """Zero changed files but non-zero lines still counts as a diff."""
        decision = evaluate_pr(provider(), brief(additions=1))
        assert (decision.should_close, decision.reason) == (False, "non-empty-diff")

    def test_deletions_only_diff_is_rejected(self) -> None:
        """Zero changed files but non-zero deletions still counts as a diff."""
        decision = evaluate_pr(provider(), brief(deletions=1))
        assert (decision.should_close, decision.reason) == (False, "non-empty-diff")

    def test_marker_only_in_a_review_comment(self) -> None:
        """Only the raw body is read, so a marker posted as a comment is invisible."""
        mock = provider()
        decision = evaluate_pr(mock, brief(body=pr_body(marker=False)))
        assert decision.should_close is False
        # The reaper never asks the provider for comments in the first place.
        mock.list_review_comments.assert_not_called()
        mock.list_issue_comments.assert_not_called()

    def test_marker_appearing_only_inside_the_diff_text(self) -> None:
        """A marker inside diff text is not in the body, so nothing closes."""
        diff_text = f"+{MARKER}\n+{SENTINEL}\n"
        decision = evaluate_pr(provider(), brief(body=pr_body(marker=False), changed_files=1, additions=2))
        assert (decision.should_close, decision.reason) == (False, "non-empty-diff")
        assert MARKER in diff_text  # the marker lives in the diff, never in the body

    def test_indented_marker_inside_a_quote_is_not_anchored(self) -> None:
        """A quoted marker line does not satisfy the anchored-marker condition."""
        decision = evaluate_pr(provider(), brief(body=f"{TABLE}\n\n{SENTINEL}\n\n> {MARKER}\n"))
        assert (decision.should_close, decision.reason) == (False, "no-marker")

    def test_duplicate_markers_are_ambiguous(self) -> None:
        """Two anchored markers name two issues; the body is never acted upon."""
        decision = evaluate_pr(provider(), brief(body=f"{pr_body()}\n\n{MARKER}\n"))
        assert (decision.should_close, decision.reason) == (False, "no-marker")

    def test_non_agent_author(self) -> None:
        """Only the Copilot coding agent's follow-up PRs are reaped."""
        decision = evaluate_pr(provider(), brief(author_login="a-human"))
        assert (decision.should_close, decision.reason) == (False, "not-agent-author")

    def test_missing_sentinel(self) -> None:
        """The marker without the sentinel fails condition 4."""
        decision = evaluate_pr(provider(), brief(body=pr_body(sentinel=False)))
        assert (decision.should_close, decision.reason) == (False, "no-sentinel")

    def test_sentinel_not_on_its_own_line(self) -> None:
        """An inline mention of the sentinel does not satisfy condition 4."""
        body = pr_body(sentinel=False).replace("Closes", f"Not {SENTINEL} here. Closes")
        decision = evaluate_pr(provider(), brief(body=body))
        assert (decision.should_close, decision.reason) == (False, "no-sentinel")

    def test_deferred_issue_already_closed(self) -> None:
        """A closed issue without the prior reaper comment is not resumed."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="CLOSED", body=issue_body())
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "deferral-issue-not-open")

    def test_deferred_issue_with_unknown_state_is_not_acted_upon(self) -> None:
        """Only open issues and resumable closed issues may drive a close."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="locked", body=issue_body())
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "deferral-issue-not-open")

    def test_deferred_issue_already_closed_with_matching_reaper_comment_is_resumed(self) -> None:
        """A prior issue-close success can be resumed by closing the still-open PR."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="CLOSED", body=issue_body())
        mock.list_issue_comments.return_value = [
            IssueCommentInfo(id=1, author="github-actions[bot]", body=build_deferral_issue_comment(99, TABLE))
        ]
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (True, "eligible")
        assert decision.resume_after_issue_close is True

    def test_deferred_issue_already_closed_untrusted_author_is_not_resumed(self) -> None:
        """A matching comment body from an untrusted author does not qualify for resume."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="CLOSED", body=issue_body())
        # Same body, but posted by a user who could copy the deterministic body to bypass the check.
        mock.list_issue_comments.return_value = [
            IssueCommentInfo(id=1, author="some-user", body=build_deferral_issue_comment(99, TABLE))
        ]
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "deferral-issue-not-open")

    def test_deferred_issue_is_not_a_deferral_issue(self) -> None:
        """An open issue without the issue-side marker fails condition 3."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="open", body="just an issue")
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "deferral-marker-missing")

    def test_deferred_target_that_is_a_pull_request(self) -> None:
        """The deferred target must be an actual issue, not a pull request."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(
            number=ISSUE,
            state="open",
            body=issue_body(),
            resource_kind="pull_request",
        )
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "deferred-target-not-issue")

    def test_review_id_mismatch(self) -> None:
        """The marker's review-id must match the deferral issue's payload."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(
            number=ISSUE, state="open", body=issue_body(review_id=REVIEW_ID + 1)
        )
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "review-id-mismatch")

    def test_tree_mismatch_on_a_reported_empty_diff(self) -> None:
        """A revert can report zero changed files; the tree check catches it."""
        mock = provider()
        mock.get_pr_tree_state.return_value = PRTreeState("b" * 40, "t" * 40, "u" * 40)
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "tree-mismatch")

    def test_unresolvable_tree_is_not_treated_as_identical(self) -> None:
        """Empty tree SHAs mean the comparison failed, so nothing is closed."""
        mock = provider()
        mock.get_pr_tree_state.return_value = PRTreeState("b" * 40, "", "")
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "tree-mismatch")

    def test_table_shorter_than_the_finding_count(self) -> None:
        """A table with fewer rows than findings is the lazy-agent signal."""
        mock = provider()
        mock.get_issue_facts.return_value = IssueFacts(number=ISSUE, state="open", body=issue_body(finding_count=3))
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "row-count-mismatch")

    def test_table_rows_are_misnumbered(self) -> None:
        """Row indices must be contiguous and ascending from one."""
        table = TABLE.replace("| 2 |", "| 3 |")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "row-numbering-mismatch")

    def test_unknown_verdict_token(self) -> None:
        """A verdict outside the closed vocabulary fails the check."""
        table = TABLE.replace("`valid-no-action`", "`looks-fine`")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "unknown-verdict")

    def test_valid_fix_verdict_contradicts_the_empty_diff(self) -> None:
        """A ``valid-fix`` row beside an empty diff is never closed."""
        table = TABLE.replace("`valid-no-action`", "`valid-fix`")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "blocking-verdict")

    def test_unparseable_verdict_needs_a_human(self) -> None:
        """An ``unparseable`` row leaves the PR open for human review."""
        table = TABLE.replace("`valid-no-action`", "`unparseable`")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "blocking-verdict")

    def test_citation_that_does_not_resolve(self) -> None:
        """A cited file missing at the merge base fails condition 5."""
        mock = provider()
        mock.get_file_line_count.return_value = None
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")

    def test_citation_line_beyond_end_of_file(self) -> None:
        """A line number past the end of the cited file does not resolve."""
        mock = provider()
        mock.get_file_line_count.return_value = 10
        decision = evaluate_pr(mock, brief())
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")

    def test_citation_path_with_spaces_resolves(self) -> None:
        """Valid repo-relative paths may contain spaces before the final line suffix."""
        mock = provider()
        table = TABLE.replace("`specs/spec.md:42`", "`docs/my file.md:42`")
        decision = evaluate_pr(mock, brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (True, "eligible")
        mock.get_file_line_count.assert_called_once_with("b" * 40, "docs/my file.md")

    def test_citation_without_a_line_anchor(self) -> None:
        """An unanchored citation is not resolvable and is refused."""
        table = TABLE.replace("`specs/spec.md:42`", "`specs/spec.md`")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")

    def test_citation_line_zero_is_rejected(self) -> None:
        """Line numbers are one-based; ``:0`` never resolves."""
        table = TABLE.replace("`specs/spec.md:42`", "`specs/spec.md:0`")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")

    def test_citation_with_parent_directory_traversal(self) -> None:
        """A traversing path is refused before it reaches the provider."""
        mock = provider()
        table = TABLE.replace("`specs/spec.md:42`", "`../etc/passwd:1`")
        decision = evaluate_pr(mock, brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")
        mock.get_file_line_count.assert_not_called()

    def test_absolute_citation_path(self) -> None:
        """An absolute path is refused before it reaches the provider."""
        mock = provider()
        table = TABLE.replace("`specs/spec.md:42`", "`/etc/passwd:1`")
        decision = evaluate_pr(mock, brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")
        mock.get_file_line_count.assert_not_called()

    def test_option_like_citation_path(self) -> None:
        """A path that could be read as a CLI flag is refused."""
        mock = provider()
        table = TABLE.replace("`specs/spec.md:42`", "`--repo:1`")
        decision = evaluate_pr(mock, brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "unresolved-citation")
        mock.get_file_line_count.assert_not_called()

    def test_stale_verdict_requires_the_literal_stale_location(self) -> None:
        """A stale row whose location is not exactly ``stale`` violates the table contract."""
        table = TABLE.replace("`stale` | `stale`", "`specs/research.md:9` | `stale`")
        decision = evaluate_pr(provider(), brief(body=pr_body(table=table)))
        assert (decision.should_close, decision.reason) == (False, "stale-location-mismatch")
