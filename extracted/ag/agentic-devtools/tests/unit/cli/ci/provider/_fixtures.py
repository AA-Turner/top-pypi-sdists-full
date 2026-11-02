"""Shared provider fixtures for capability tests."""

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

    def update_comment(self, comment_id: int, body: str) -> int | None:
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
