"""Structured requests and responses for git operations."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator

# Cap on free-form text fields shipped over the SSH stdio channel.
# A single GitOpResult is serialized as one JSON line; asyncio's StreamReader
# default line buffer is 64KB, so any individual string field above this risks
# pushing the encoded line past that limit and breaking readline(). Git output
# (verbose push progress, status on a workspace with thousands of untracked
# files, GitCommandError stderr dumps) can balloon past 64KB. Truncate to keep
# both head + tail visible for debugging.
_TEXT_FIELD_CAP = 16 * 1024


def _truncate_text(value: str) -> str:
    if len(value) <= _TEXT_FIELD_CAP:
        return value
    half = _TEXT_FIELD_CAP // 2
    return f"{value[:half]}\n... [truncated {len(value) - _TEXT_FIELD_CAP} bytes] ...\n{value[-half:]}"


GitOperation = Literal[
    "ping",
    "rev_parse",
    "status_short",
    "auto_commit",
    "clone_setup",
    "head_diff",
    "push",
    "fetch_origin",
    "publish_state",
    "rebase_ours",
    "abort_rebase_reset_main",
    "force_push_main",
    "merge_origin_main",
    "unmerged_files",
    "accept_theirs",
    "current_head_info",
    "commit_and_push_branch",
]


class GitOpRequest(BaseModel):
    """Serializable git operation request."""

    operation: GitOperation
    repo_path: str
    ref: str | None = None
    refspec: str | None = None
    force: bool = False
    commit_message: str | None = None
    bare_repo_path: str | None = None
    checkout_ref: str | None = None
    branch_name: str | None = None
    compare_ref: str | None = None
    message: str | None = None

    @classmethod
    def ping(cls) -> GitOpRequest:
        return cls(operation="ping", repo_path="")

    @classmethod
    def rev_parse(cls, repo_path: str, ref: str) -> GitOpRequest:
        return cls(operation="rev_parse", repo_path=repo_path, ref=ref)

    @classmethod
    def status_short(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="status_short", repo_path=repo_path)

    @classmethod
    def auto_commit(cls, repo_path: str, commit_message: str) -> GitOpRequest:
        return cls(operation="auto_commit", repo_path=repo_path, commit_message=commit_message)

    @classmethod
    def clone_setup(
        cls,
        repo_path: str,
        *,
        bare_repo_path: str,
        checkout_ref: str | None,
        branch_name: str | None,
    ) -> GitOpRequest:
        return cls(
            operation="clone_setup",
            repo_path=repo_path,
            bare_repo_path=bare_repo_path,
            checkout_ref=checkout_ref,
            branch_name=branch_name,
        )

    @classmethod
    def head_diff(cls, repo_path: str, compare_ref: str) -> GitOpRequest:
        return cls(operation="head_diff", repo_path=repo_path, compare_ref=compare_ref)

    @classmethod
    def push(cls, repo_path: str, refspec: str, *, force: bool = False) -> GitOpRequest:
        return cls(operation="push", repo_path=repo_path, refspec=refspec, force=force)

    @classmethod
    def fetch_origin(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="fetch_origin", repo_path=repo_path)

    @classmethod
    def publish_state(cls, repo_path: str, compare_ref: str) -> GitOpRequest:
        return cls(operation="publish_state", repo_path=repo_path, compare_ref=compare_ref)

    @classmethod
    def rebase_ours(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="rebase_ours", repo_path=repo_path)

    @classmethod
    def abort_rebase_reset_main(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="abort_rebase_reset_main", repo_path=repo_path)

    @classmethod
    def force_push_main(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="force_push_main", repo_path=repo_path)

    @classmethod
    def merge_origin_main(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="merge_origin_main", repo_path=repo_path)

    @classmethod
    def unmerged_files(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="unmerged_files", repo_path=repo_path)

    @classmethod
    def accept_theirs(cls, repo_path: str, message: str) -> GitOpRequest:
        return cls(operation="accept_theirs", repo_path=repo_path, message=message)

    @classmethod
    def current_head_info(cls, repo_path: str) -> GitOpRequest:
        return cls(operation="current_head_info", repo_path=repo_path)

    @classmethod
    def commit_and_push_branch(
        cls,
        repo_path: str,
        *,
        branch_name: str,
        commit_message: str,
    ) -> GitOpRequest:
        return cls(
            operation="commit_and_push_branch",
            repo_path=repo_path,
            branch_name=branch_name,
            commit_message=commit_message,
        )


class GitOpResult(BaseModel):
    """Serializable git operation result."""

    ok: bool
    exit_status: int | None = None
    stdout: str = ""
    stderr: str = ""
    branch: str | None = None
    head: str | None = None
    noop: bool | None = None
    head_sha: str | None = None
    compare_sha: str | None = None
    git_status: str | None = None
    ahead_behind: str | None = None
    files: list[str] | None = None

    @field_validator("stdout", "stderr", "git_status", mode="before")
    @classmethod
    def _cap_text(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return _truncate_text(v)
