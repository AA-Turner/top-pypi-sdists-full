from agentic_devtools.adapters.pull_request_threads import ThreadResolutionResult


def test_as_dict_serializes_tuple_diagnostics_and_github_ids() -> None:
    result = ThreadResolutionResult(
        success=False,
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        verification_status="failed",
        github_thread_node_id="PRRT_node",
        github_comment_id=44,
        diagnostics=("verification_failed", "rate_limited"),
    )

    assert result.as_dict() == {
        "success": False,
        "provider": "github",
        "repository": "owner/repo",
        "pull_request_id": 12,
        "discussion_kind": "review_thread",
        "requested_operation": "resolve",
        "status": "failed",
        "prior_state": "unknown",
        "resulting_state": "unknown",
        "verification_status": "failed",
        "azure_devops_thread_id": None,
        "github_thread_node_id": "PRRT_node",
        "github_comment_id": 44,
        "diagnostics": ["verification_failed", "rate_limited"],
    }


def test_as_dict_serializes_azure_devops_thread_id() -> None:
    result = ThreadResolutionResult(
        success=True,
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        status="resolved",
        prior_state="active",
        resulting_state="fixed",
        verification_status="verified",
        azure_devops_thread_id=34,
    )

    assert result.as_dict()["azure_devops_thread_id"] == 34
