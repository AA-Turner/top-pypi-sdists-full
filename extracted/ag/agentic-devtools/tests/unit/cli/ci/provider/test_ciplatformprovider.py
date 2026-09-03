"""Tests for CIPlatformProvider ABC."""

import pytest

from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    EventPayload,
    FinalizationResult,
    IssueCommentInfo,
    IssueEvent,
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
    SquashResult,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider


class _ConcreteProvider(CIPlatformProvider):
    """Minimal concrete implementation for testing the ABC contract."""

    def parse_event(self, raw_payload: dict, event_name: str) -> EventPayload:
        return EventPayload(pr_number=raw_payload.get("number", 0), action=event_name)

    def get_pr_metadata(self, pr_number: int) -> PRMetadata:
        return PRMetadata(number=pr_number, title="test", head_branch="b", head_sha="s", base_branch="main")

    def list_check_runs(self, head_sha: str) -> list[CheckRunStatus]:
        return [CheckRunStatus(id=1, name="ci", status="completed", conclusion="success")]

    def list_reviews(self, pr_number: int) -> list[ReviewInfo]:
        return [ReviewInfo(id=1, user="reviewer", state="APPROVED")]

    def post_comment(self, pr_number: int, body: str) -> int:
        return 100

    def update_comment(self, comment_id: int, body: str) -> None:
        pass

    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        return None

    def approve_pr(self, pr_number: int, head_sha: str, body: str) -> bool:
        return True

    def merge_pr(self, pr_number: int, head_sha: str, method: str, *, commit_title: str | None = None) -> None:
        pass

    def delete_branch(self, branch: str) -> None:
        pass

    def request_reviewer(self, pr_number: int, reviewer: str) -> None:
        pass

    def count_unresolved_review_threads(self, pr_number: int) -> int:
        return 0

    def list_pr_files(self, pr_number: int) -> list[str]:
        return ["file.py"]

    def get_check_annotations(self, check_run_id: int, limit: int) -> list[str]:
        return ["annotation"]

    def dispatch_repair(
        self,
        pr_number: int,
        head_sha: str,
        repair_type: str,
        failed_checks: list[CheckRunStatus],
        review_comments: list[ReviewCommentInfo],
        review_id: int = 0,
        declared_author_comment_count: int = 0,
        declared_author_comment_counts_by_review: dict[int, int] | None = None,
    ) -> int:
        return 200

    def list_review_comments(self, pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
        return [ReviewCommentInfo(id=1, path="file.py", body="review comment", html_url="")]

    def list_issue_comments(self, pr_number: int) -> list[IssueCommentInfo]:
        return []

    def finalize_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
        review_id: int,
    ) -> FinalizationResult:
        return FinalizationResult()

    def squash_post_repair(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> SquashResult:
        return SquashResult()

    def list_pr_issue_events(self, pr_number: int) -> list[IssueEvent]:
        return []

    def publish_pr(self, pr_number: int) -> None:
        pass

    def squash_before_publish(
        self,
        *,
        pr_number: int,
        base_branch: str,
        head_branch: str,
        head_sha: str,
    ) -> None:
        pass


class TestCIPlatformProvider:
    """Tests for the CIPlatformProvider abstract base class."""

    def test_cannot_instantiate_abc(self) -> None:
        with pytest.raises(TypeError, match="abstract method"):
            CIPlatformProvider()  # type: ignore[abstract]

    def test_concrete_provider_instantiates(self) -> None:
        provider = _ConcreteProvider()
        assert isinstance(provider, CIPlatformProvider)

    def test_parse_event_signature(self) -> None:
        provider = _ConcreteProvider()
        result = provider.parse_event({"number": 42}, "pull_request")
        assert isinstance(result, EventPayload)
        assert result.pr_number == 42

    def test_get_pr_metadata_returns_correct_type(self) -> None:
        provider = _ConcreteProvider()
        result = provider.get_pr_metadata(10)
        assert isinstance(result, PRMetadata)
        assert result.number == 10

    def test_list_check_runs_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.list_check_runs("abc123")
        assert isinstance(result, list)
        assert all(isinstance(r, CheckRunStatus) for r in result)

    def test_list_reviews_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.list_reviews(1)
        assert isinstance(result, list)
        assert all(isinstance(r, ReviewInfo) for r in result)

    def test_post_comment_returns_int(self) -> None:
        provider = _ConcreteProvider()
        result = provider.post_comment(1, "hello")
        assert isinstance(result, int)

    def test_post_comment_as_pr_token_defaults_to_post_comment(self) -> None:
        """Base helper falls back to post_comment for providers without override."""
        provider = _ConcreteProvider()
        result = provider.post_comment_as_pr_token(1, "hello")
        assert result == 100

    def test_update_comment_returns_none(self) -> None:
        provider = _ConcreteProvider()
        assert provider.update_comment(1, "updated") is None  # type: ignore[func-returns-value]

    def test_find_comment_returns_none_or_tuple(self) -> None:
        provider = _ConcreteProvider()
        result = provider.find_comment(1, "marker")
        assert result is None

    def test_approve_pr_returns_bool(self) -> None:
        provider = _ConcreteProvider()
        result = provider.approve_pr(1, "sha", "LGTM")
        assert result is True

    def test_merge_pr_returns_none(self) -> None:
        provider = _ConcreteProvider()
        assert provider.merge_pr(1, "sha", "squash") is None  # type: ignore[func-returns-value]

    def test_request_reviewer_returns_none(self) -> None:
        provider = _ConcreteProvider()
        assert provider.request_reviewer(1, "user") is None  # type: ignore[func-returns-value]

    def test_list_pr_files_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.list_pr_files(1)
        assert isinstance(result, list)
        assert all(isinstance(f, str) for f in result)

    def test_get_check_annotations_returns_list(self) -> None:
        provider = _ConcreteProvider()
        result = provider.get_check_annotations(1, 10)
        assert isinstance(result, list)
        assert all(isinstance(a, str) for a in result)

    def test_publish_pr_returns_none(self) -> None:
        provider = _ConcreteProvider()
        assert provider.publish_pr(1) is None  # type: ignore[func-returns-value]

    def test_list_no_change_candidate_prs_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_no_change_candidate_prs"):
            provider.list_no_change_candidate_prs()

    def test_get_pr_tree_state_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_pr_tree_state"):
            provider.get_pr_tree_state(1)

    def test_get_issue_facts_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_issue_facts"):
            provider.get_issue_facts(1)

    def test_get_file_line_count_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_file_line_count"):
            provider.get_file_line_count("abc123", "src/module.py")

    def test_post_issue_comment_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement post_issue_comment"):
            provider.post_issue_comment(1, "body")

    def test_close_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement close_issue"):
            provider.close_issue(1)

    def test_close_pr_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement close_pr"):
            provider.close_pr(1)

    def test_dispatch_conflict_repair_default_raises_not_implemented(self) -> None:
        """Base class dispatch_conflict_repair raises NotImplementedError."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_conflict_repair"):
            provider.dispatch_conflict_repair(
                pr_number=1,
                head_sha="abc",
                base_sha="def",
                base_branch="main",
                head_branch="feat",
            )

    def test_get_pr_diff_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_pr_diff"):
            provider.get_pr_diff(1)

    def test_get_ref_sha_default_returns_empty(self) -> None:
        """Base class get_ref_sha degrades to an empty string."""
        provider = _ConcreteProvider()
        assert provider.get_ref_sha("main") == ""

    def test_get_commit_range_diff_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_commit_range_diff"):
            provider.get_commit_range_diff("abc", "def")

    def test_graphql_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement graphql"):
            provider.graphql(query="{ viewer { login } }")

    def test_count_commits_behind_default_returns_zero(self) -> None:
        provider = _ConcreteProvider()
        result = provider.count_commits_behind(pr_number=1, base_branch="main", head_branch="feature")
        assert result == 0

    def test_rebase_onto_base_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement rebase_onto_base"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

    def test_get_commit_author_login_default_returns_empty(self) -> None:
        provider = _ConcreteProvider()
        assert provider.get_commit_author_login("abc123") == ""

    def test_list_relevant_pull_requests_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_relevant_pull_requests"):
            provider.list_relevant_pull_requests()

    def test_get_pr_copilot_attribution_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_pr_copilot_attribution"):
            provider.get_pr_copilot_attribution(1)

    def test_get_approver_login_default_returns_empty(self) -> None:
        """Base class get_approver_login returns empty string (best-effort default)."""
        provider = _ConcreteProvider()
        assert provider.get_approver_login() == ""

    def test_get_pr_token_login_default_returns_empty(self) -> None:
        """Base class get_pr_token_login returns empty string (best-effort default)."""
        provider = _ConcreteProvider()
        assert provider.get_pr_token_login() == ""

    def test_reclaim_copilot_commit_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement reclaim_copilot_commit"):
            provider.reclaim_copilot_commit(pr_number=1, head_branch="feature", head_sha="abc123")

    def test_list_workflow_runs_default_raises_not_implemented(self) -> None:
        """Default list_workflow_runs raises NotImplementedError."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_workflow_runs"):
            provider.list_workflow_runs(workflow_id="ci.yml")

    def test_rerun_workflow_default_raises_not_implemented(self) -> None:
        """Default rerun_workflow raises NotImplementedError."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement rerun_workflow"):
            provider.rerun_workflow(run_id=12345)

    def test_list_closed_prs_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_closed_prs"):
            provider.list_closed_prs(exclude_labels=["audited"], limit=10)

    def test_claim_pr_for_audit_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement claim_pr_for_audit"):
            provider.claim_pr_for_audit(pr_number=1, label="in-progress")

    def test_add_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement add_label"):
            provider.add_label(pr_number=1, label="audited")

    def test_remove_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement remove_label"):
            provider.remove_label(pr_number=1, label="in-progress")

    def test_count_prs_without_labels_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement count_prs_without_labels"):
            provider.count_prs_without_labels(exclude_labels=["audited"])

    def test_list_all_review_comments_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_all_review_comments"):
            provider.list_all_review_comments(pr_number=1)

    def test_create_pull_request_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement create_pull_request"):
            provider.create_pull_request(title="My PR", body="Body")

    def test_delete_review_comments_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement delete_review_comments"):
            provider.delete_review_comments(1)

    def test_create_audit_tracking_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement create_audit_tracking_issue"):
            provider.create_audit_tracking_issue(batch_id="abc123", pr_numbers=[1, 2])

    def test_dispatch_audit_evaluation_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_audit_evaluation"):
            provider.dispatch_audit_evaluation(
                tracking_issue=2042,
                batch_id="abc123",
                batch_branch="audit/batch-abc123",
                batch_dir="audit-batches/abc123",
                pr_numbers=[1, 2],
            )

    def test_find_deferral_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement find_deferral_issue"):
            provider.find_deferral_issue(pr_number=11, review_id=42)

    def test_create_deferral_issue_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement create_deferral_issue"):
            provider.create_deferral_issue(
                pr_number=11,
                review_id=42,
                base_sha="abc1234",
                findings=[("specs/spec.md", "finding")],
                labels=["suppressed-comment-follow-up"],
            )

    def test_dispatch_suppressed_triage_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_suppressed_triage"):
            provider.dispatch_suppressed_triage(issue_number=4242, pr_number=11, review_id=42)

    def test_count_open_issues_with_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement count_open_issues_with_label"):
            provider.count_open_issues_with_label("suppressed-comment-follow-up")

    def test_list_linked_issue_labels_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_linked_issue_labels"):
            provider.list_linked_issue_labels(pr_number=11)

    def test_list_prs_with_label_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_prs_with_label"):
            provider.list_prs_with_label("in-progress")

    def test_get_label_applied_at_default_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_label_applied_at"):
            provider.get_label_applied_at(pr_number=1, label="in-progress")

    def test_list_review_thread_states_default_raises_not_implemented(self) -> None:
        """Providers must opt into review-thread state; the default fails closed."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_review_thread_states"):
            provider.list_review_thread_states(1)

    def test_abstract_methods_list(self) -> None:
        """Verify all expected abstract methods are defined."""
        expected_methods = {
            "parse_event",
            "get_pr_metadata",
            "list_check_runs",
            "list_reviews",
            "post_comment",
            "update_comment",
            "find_comment",
            "approve_pr",
            "merge_pr",
            "delete_branch",
            "publish_pr",
            "squash_before_publish",
            "request_reviewer",
            "count_unresolved_review_threads",
            "list_pr_files",
            "get_check_annotations",
            "dispatch_repair",
            "list_review_comments",
            "list_issue_comments",
            "finalize_post_repair",
            "squash_post_repair",
            "list_pr_issue_events",
        }
        actual_abstracts = CIPlatformProvider.__abstractmethods__
        assert actual_abstracts == expected_methods
