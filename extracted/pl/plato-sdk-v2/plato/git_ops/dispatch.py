"""Dispatch structured git requests onto repo operations."""

from __future__ import annotations

from plato.git_ops import repo as repo_ops
from plato.git_ops.models import GitOpRequest, GitOpResult


def run_request(request: GitOpRequest) -> GitOpResult:
    """Execute a structured git operation request."""
    try:
        if request.operation == "ping":
            return GitOpResult(ok=True, stdout="pong")
        if request.operation == "rev_parse":
            assert request.ref is not None
            return repo_ops.rev_parse(request.repo_path, request.ref)
        if request.operation == "status_short":
            return repo_ops.status_short(request.repo_path)
        if request.operation == "auto_commit":
            assert request.commit_message is not None
            return repo_ops.auto_commit(request.repo_path, request.commit_message)
        if request.operation == "clone_setup":
            assert request.bare_repo_path is not None
            return repo_ops.clone_setup(
                request.repo_path,
                bare_repo_path=request.bare_repo_path,
                checkout_ref=request.checkout_ref,
                branch_name=request.branch_name,
            )
        if request.operation == "head_diff":
            assert request.compare_ref is not None
            return repo_ops.head_diff(request.repo_path, request.compare_ref)
        if request.operation == "push":
            assert request.refspec is not None
            return repo_ops.push(request.repo_path, request.refspec, force=request.force)
        if request.operation == "fetch_origin":
            return repo_ops.fetch_origin(request.repo_path)
        if request.operation == "publish_state":
            assert request.compare_ref is not None
            return repo_ops.publish_state(request.repo_path, request.compare_ref)
        if request.operation == "rebase_ours":
            return repo_ops.rebase_ours(request.repo_path)
        if request.operation == "abort_rebase_reset_main":
            return repo_ops.abort_rebase_reset_main(request.repo_path)
        if request.operation == "force_push_main":
            return repo_ops.force_push_main(request.repo_path)
        if request.operation == "merge_origin_main":
            return repo_ops.merge_origin_main(request.repo_path)
        if request.operation == "unmerged_files":
            return repo_ops.unmerged_files(request.repo_path)
        if request.operation == "accept_theirs":
            assert request.message is not None
            return repo_ops.accept_theirs(request.repo_path, request.message)
        if request.operation == "current_head_info":
            return repo_ops.current_head_info(request.repo_path)
        if request.operation == "commit_and_push_branch":
            assert request.branch_name is not None
            assert request.commit_message is not None
            return repo_ops.commit_and_push_branch(
                request.repo_path,
                branch_name=request.branch_name,
                commit_message=request.commit_message,
            )
    except Exception as exc:  # noqa: BLE001
        return repo_ops._error_result(exc)
    raise ValueError(f"Unknown git operation: {request.operation}")
