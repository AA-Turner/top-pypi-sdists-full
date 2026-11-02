"""Tests for the public CIPlatformProvider API contract."""

import inspect

from agentic_devtools.cli.ci import CIPlatformProvider as PublicCIPlatformProvider
from agentic_devtools.cli.ci.provider import CIPlatformProvider

_EXPECTED_SIGNATURES = {
    "add_label": "(self, pr_number: 'int', label: 'str') -> 'None'",
    "approve_pr": "(self, pr_number: 'int', head_sha: 'str', body: 'str') -> 'bool'",
    "claim_pr_for_audit": "(self, pr_number: 'int', label: 'str') -> 'ClaimResult'",
    "close_issue": "(self, issue_number: 'int', *, reason: 'str' = 'completed') -> 'None'",
    "close_pr": "(self, pr_number: 'int', *, comment: 'str | None' = None) -> 'None'",
    "compute_diff_files": "(self, *, base_branch: 'str', sha: 'str', base_sha: 'str' = '') -> 'list[str] | None'",
    "compute_diff_hash": "(self, *, base_branch: 'str', sha: 'str', base_sha: 'str' = '') -> 'str | None'",
    "count_commits_behind": "(self, *, pr_number: 'int', base_branch: 'str', head_branch: 'str') -> 'int'",
    "count_open_issues_with_label": "(self, label: 'str') -> 'int'",
    "count_prs_without_labels": "(self, *, exclude_labels: 'list[str]', state: 'str' = 'closed') -> 'int'",
    "count_unresolved_review_threads": "(self, pr_number: 'int') -> 'int'",
    "create_audit_tracking_issue": "(self, *, batch_id: 'str', pr_numbers: 'list[int]') -> 'int'",
    "create_deferral_issue": (
        "(self, *, pr_number: 'int', review_id: 'int', base_sha: 'str', "
        "findings: 'list[tuple[str, str]]', labels: 'list[str]') -> 'int'"
    ),
    "create_pull_request": "(self, title: 'str', body: 'str', *, draft: 'bool' = True) -> 'str'",
    "create_review_thread": (
        "(self, *, pr_number: 'int', commit_sha: 'str', path: 'str', line: 'int', "
        "side: 'str', body: 'str') -> 'ReviewCommentInfo'"
    ),
    "delete_branch": "(self, branch: 'str') -> 'None'",
    "delete_comment": "(self, comment_id: 'int') -> 'None'",
    "delete_review_comments": (
        "(self, pr_number: 'int', *, execute: 'bool' = False, "
        "author_substring: 'str | None' = None) -> 'ReviewCommentDeletionResult'"
    ),
    "dispatch_agent_retry": "(self, pr_number: 'int', prompt: 'str', failure_event_id: 'str') -> 'int'",
    "dispatch_audit_evaluation": (
        "(self, *, tracking_issue: 'int', batch_id: 'str', batch_branch: 'str', "
        "batch_dir: 'str', pr_numbers: 'list[int]') -> 'AgentAssignmentResult'"
    ),
    "dispatch_conflict_repair": "".join(
        (
            "(self, pr_number: 'int', head_sha: 'str', base_sha: 'str', ",
            "base_branch: 'str', head_branch: 'str') -> 'int'",
        )
    ),
    "dispatch_repair": (
        "(self, pr_number: 'int', head_sha: 'str', repair_type: 'str', "
        "failed_checks: 'list[CheckRunStatus]', review_comments: 'list[ReviewCommentInfo]', "
        "review_id: 'int' = 0, declared_author_comment_count: 'int' = 0, "
        "declared_author_comment_counts_by_review: 'dict[int, int] | None' = None, "
        "agent_task_prompt: 'str | None' = None) -> 'int | str'"
    ),
    "dispatch_suppressed_triage": "".join(
        (
            "(self, *, issue_number: 'int', pr_number: 'int', review_id: 'int') -> ",
            "'AgentAssignmentResult'",
        )
    ),
    "dispatch_workflow": "(self, workflow: 'str', inputs: 'dict[str, str]') -> 'None'",
    "finalize_post_repair": (
        "(self, *, pr_number: 'int', base_branch: 'str', head_branch: 'str', "
        "head_sha: 'str', review_id: 'int') -> 'FinalizationResult'"
    ),
    "find_comment": "(self, pr_number: 'int', marker: 'str') -> 'tuple[int, str] | None'",
    "find_deferral_issue": "(self, *, pr_number: 'int', review_id: 'int') -> 'int | None'",
    "get_agent_task_first_observed_at": (
        "(self, pr_number: 'int', *, task_id: 'str', session_id: 'str' = '', "
        "head_branch: 'str' = '', expected_head_sha: 'str' = '') -> 'str | None'"
    ),
    "get_agent_task_prompt": "(self, task_id: 'str') -> 'str'",
    "get_approver_login": "(self) -> 'str'",
    "get_bookkeeping_token_login": "(self) -> 'str'",
    "get_check_annotations": "(self, check_run_id: 'int', limit: 'int') -> 'list[str]'",
    "get_commit_author_login": "(self, sha: 'str') -> 'str'",
    "get_commit_range_diff": "(self, base_sha: 'str', head_sha: 'str') -> 'str'",
    "get_commit_range_diff_bytes": "(self, base_sha: 'str', head_sha: 'str') -> 'bytes'",
    "get_commit_range_diff_change_counts": "(self, base_sha: 'str', head_sha: 'str') -> 'dict[str, int]'",
    "get_dispatch_login": "(self) -> 'str'",
    "get_file_line_count": "(self, ref: 'str', path: 'str') -> 'int | None'",
    "get_issue_facts": "(self, issue_number: 'int') -> 'IssueFacts'",
    "get_label_applied_at": "(self, pr_number: 'int', label: 'str') -> 'datetime | None'",
    "get_or_record_agent_task_first_observed_at": (
        "(self, pr_number: 'int', *, task_id: 'str', session_id: 'str' = '', "
        "head_branch: 'str' = '', expected_head_sha: 'str' = '') -> 'str | None'"
    ),
    "get_pr_body": "(self, pr_number: 'int') -> 'str'",
    "get_pr_copilot_attribution": (
        "(self, pr_number: 'int', *, observation_watermark: 'str' = '') -> 'dict[str, bool | str]'"
    ),
    "get_pr_diff": "(self, pr_number: 'int') -> 'str'",
    "get_pr_metadata": "(self, pr_number: 'int') -> 'PRMetadata'",
    "get_pr_token_login": "(self) -> 'str'",
    "get_pr_tree_state": "(self, pr_number: 'int') -> 'PRTreeState'",
    "get_recent_dispatch_history": "(self, workflow: 'str') -> 'list[DispatchEvent]'",
    "get_ref_sha": "(self, ref: 'str') -> 'str'",
    "get_trusted_loop_comment_logins": "(self) -> 'set[str]'",
    "get_variable": "(self, name: 'str', *, use_writer_token: 'bool' = False) -> 'str | None'",
    "graphql": "(self, *, query: 'str', variables: 'dict | None' = None) -> 'dict'",
    "invalidate_agent_task_inventory": "(self, pr_number: 'int | None' = None) -> 'None'",
    "is_codeql_configured": "(self, repo: 'str | None' = None, *, base_branch: 'str' = '') -> 'bool'",
    "list_agent_tasks": "(self, repo: 'str') -> 'AgentTaskInventoryLoadResult'",
    "list_all_review_comments": "(self, pr_number: 'int') -> 'list[ReviewCommentInfo]'",
    "list_check_runs": "(self, head_sha: 'str') -> 'list[CheckRunStatus]'",
    "list_closed_prs": "".join(
        (
            "(self, *, exclude_labels: 'list[str]', limit: 'int', state: 'str' = 'closed') ",
            "-> 'list[ClosedPRInfo]'",
        )
    ),
    "list_closing_issues": "(self, pr_number: 'int') -> 'list[ClosingIssue]'",
    "list_eligible_prs": "(self, max_prs: 'int | None' = None) -> 'list[EligiblePR]'",
    "list_eligible_prs_with_retry_liveness": "(self, max_prs: 'int | None' = None) -> 'tuple[list[EligiblePR], bool]'",
    "list_issue_comments": "(self, issue_or_pr_number: 'int') -> 'list[IssueCommentInfo]'",
    "list_linked_issue_labels": "(self, pr_number: 'int') -> 'list[str]'",
    "list_no_change_candidate_prs": "(self) -> 'list[NoChangePRBrief]'",
    "list_open_copilot_pr_briefs": "(self) -> 'list[dict[str, Any]]'",
    "list_pr_agent_task_lifecycles": (
        "(self, pr_number: 'int', *, pr_id: 'int | None' = None, head_branch: 'str' = '', "
        "head_sha: 'str' = '') -> 'AgentTaskInventory'"
    ),
    "list_pr_commits": "(self, pr_number: 'int') -> 'list[dict[str, Any]]'",
    "list_pr_files": "(self, pr_number: 'int') -> 'list[str]'",
    "list_pr_issue_events": "(self, pr_number: 'int') -> 'list[IssueEvent]'",
    "list_pr_session_summaries": "(self, pr_number: 'int') -> 'list[CopilotSessionSummary]'",
    "list_prs_with_label": "(self, label: 'str') -> 'list[int]'",
    "list_relevant_pull_requests": "".join(
        (
            "(self, *, cursor: 'str | None' = None, limit: 'int' = 25) ",
            "-> 'tuple[list[PRMetadata], str | None]'",
        )
    ),
    "list_review_comments": "(self, pr_number: 'int', review_id: 'int') -> 'list[ReviewCommentInfo]'",
    "list_review_thread_states": "(self, pr_number: 'int') -> 'dict[int, tuple[bool, bool]]'",
    "list_reviews": "(self, pr_number: 'int') -> 'list[ReviewInfo]'",
    "list_supervisor_prs": "(self, max_prs: 'int | None' = None) -> 'list[EligiblePR]'",
    "list_workflow_runs": (
        "(self, workflow_id: 'str', *, window_hours: 'int' = 24, "
        "include_dispatch_inputs: 'bool' = False) -> 'list[WorkflowRun]'"
    ),
    "merge_pr": "".join(
        (
            "(self, pr_number: 'int', head_sha: 'str', method: 'str', *, ",
            "commit_title: 'str | None' = None) -> 'None'",
        )
    ),
    "parse_event": "(self, raw_payload: 'dict', event_name: 'str') -> 'EventPayload'",
    "post_comment": "(self, pr_number: 'int', body: 'str') -> 'int'",
    "post_comment_as_pr_token": "(self, pr_number: 'int', body: 'str') -> 'int'",
    "post_issue_comment": "(self, issue_number: 'int', body: 'str') -> 'int'",
    "post_issue_comment_as_bookkeeping_token": "(self, issue_number: 'int', body: 'str') -> 'int'",
    "publish_pr": "(self, pr_number: 'int') -> 'None'",
    "rebase_onto_base": "".join(
        (
            "(self, *, pr_number: 'int', base_branch: 'str', head_branch: 'str', ",
            "head_sha: 'str') -> 'str | None'",
        )
    ),
    "reclaim_copilot_commit": "(self, *, pr_number: 'int', head_branch: 'str', head_sha: 'str') -> 'None'",
    "remove_label": "(self, pr_number: 'int', label: 'str') -> 'None'",
    "request_reviewer": "(self, pr_number: 'int', reviewer: 'str') -> 'None'",
    "rerun_workflow": "(self, run_id: 'int') -> 'None'",
    "set_variable": "(self, name: 'str', value: 'str') -> 'None'",
    "squash_before_publish": "".join(
        (
            "(self, *, pr_number: 'int', base_branch: 'str', head_branch: 'str', ",
            "head_sha: 'str') -> 'None'",
        )
    ),
    "squash_post_repair": "".join(
        (
            "(self, *, pr_number: 'int', base_branch: 'str', head_branch: 'str', ",
            "head_sha: 'str') -> 'SquashResult'",
        )
    ),
    "update_comment": "(self, comment_id: 'int', body: 'str') -> 'int | None'",
    "update_comment_as_pr_token": "(self, comment_id: 'int', body: 'str') -> 'int | None'",
    "update_pr_title": "(self, pr_number: 'int', title: 'str') -> 'None'",
    "validate_variable_token": "(self) -> 'bool'",
}


class TestCIPlatformProviderContract:
    """Protect the provider's public import identity and method signatures."""

    def test_public_import_path_and_package_export_are_stable(self) -> None:
        assert CIPlatformProvider.__module__ == "agentic_devtools.cli.ci.provider"
        assert PublicCIPlatformProvider is CIPlatformProvider

    def test_public_method_signatures_match_the_pre_split_contract(self) -> None:
        actual = {
            name: str(inspect.signature(method))
            for name, method in inspect.getmembers(CIPlatformProvider, inspect.isfunction)
            if not name.startswith("_")
        }
        assert actual == _EXPECTED_SIGNATURES
