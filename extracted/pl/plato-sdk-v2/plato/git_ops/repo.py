"""Reusable GitPython-backed repository operations."""

from __future__ import annotations

import shutil
import threading
from pathlib import Path

from git import Actor, Git, Repo
from git.exc import GitCommandError

from plato.git_ops.models import GitOpResult

PLATO_ACTOR = Actor("Plato", "plato@plato.dev")
AGENT_ACTOR = Actor("Plato Agent", "agent@plato.dev")
_TRUSTED_DIRECTORIES: set[str] = set()
_TRUSTED_DIRECTORIES_LOCK = threading.Lock()


def trust_git_directory(path: str | Path) -> None:
    """Mark a repository path as trusted for GitPython/git."""
    resolved_path = str(Path(path).resolve())
    if resolved_path in _TRUSTED_DIRECTORIES:
        return

    with _TRUSTED_DIRECTORIES_LOCK:
        if resolved_path in _TRUSTED_DIRECTORIES:
            return
        Git().config("--global", "--add", "safe.directory", resolved_path)
        _TRUSTED_DIRECTORIES.add(resolved_path)


def checkout_main_from_bare(*, bare_repo_path: str, worktree_path: str) -> None:
    """Refresh the repo/ working tree from the bare repo's main branch.

    If worktree_path is a git clone (has .git), fetches from the bare repo
    and resets to match main. Otherwise falls back to bare checkout.
    """
    from pathlib import Path

    trust_git_directory(bare_repo_path)
    trust_git_directory(worktree_path)

    git_dir = Path(worktree_path) / ".git"
    if git_dir.is_dir():
        repo = Repo(worktree_path)
        repo.git.config("core.logAllRefUpdates", "false")
        repo.git.fetch("origin", "main")
        repo.git.reset("--hard", "origin/main")
        repo.git.clean(
            "-fd", "-e", ".durable", "-e", ".code-review-output", "-e", ".webclone", "-e", ".pr-review-results"
        )
    else:
        repo = Repo(bare_repo_path)
        repo.git.update_environment(GIT_WORK_TREE=worktree_path)
        repo.git.checkout("-f", "main")


def _repo(path: str) -> Repo:
    trust_git_directory(path)
    return Repo(path)


def _error_result(exc: BaseException) -> GitOpResult:
    return GitOpResult(
        ok=False,
        exit_status=getattr(exc, "status", None),
        stderr=(getattr(exc, "stderr", "") or getattr(exc, "stdout", "") or str(exc)).strip(),
        stdout=(getattr(exc, "stdout", "") or "").strip(),
    )


def rev_parse(repo_path: str, ref: str) -> GitOpResult:
    repo = _repo(repo_path)
    return GitOpResult(ok=True, stdout=repo.commit(ref).hexsha)


def status_short(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    return GitOpResult(ok=True, stdout=repo.git.status("--short"))


def auto_commit(repo_path: str, commit_message: str) -> GitOpResult:
    repo = _repo(repo_path)
    # Evict already-tracked paths that match the current .gitignore.
    # ``git add -A`` respects .gitignore for *new* paths but does NOT
    # un-stage paths that were already committed in a prior session.
    # When a workspace is restored from a checkpoint that committed
    # build artifacts (e.g. ``web/.next-3000/``, ``.runtime/``) and the
    # gitignore is later broadened to exclude them, every auto-sync
    # keeps committing modifications to those tracked files. List the
    # offenders with ``ls-files -ci --exclude-standard`` (cached AND
    # ignored) and ``rm --cached`` them so subsequent ``add -A`` writes
    # a clean index.
    try:
        ignored_tracked = repo.git.ls_files("-ci", "--exclude-standard", "-z").split("\x00")
        ignored_tracked = [p for p in ignored_tracked if p]
        if ignored_tracked:
            # Pass with --ignore-unmatch in case any path raced and is
            # already gone, and cap the arg list to avoid blowing argv
            # on pathological workspaces (10k+ entries).
            for chunk_start in range(0, len(ignored_tracked), 200):
                chunk = ignored_tracked[chunk_start : chunk_start + 200]
                repo.git.rm("-r", "--cached", "--ignore-unmatch", "--", *chunk)
    except GitCommandError:
        # Don't block auto_commit on eviction failures — proceed with
        # add -A and let the worst case be a single sticky tracked path.
        pass
    repo.git.add(A=True)
    if repo.is_dirty(index=True, working_tree=False, untracked_files=True):
        # Build a descriptive commit message from the staged diff
        stat = repo.git.diff("--cached", "--stat")
        if stat:
            message = f"auto-sync: {stat.strip().splitlines()[-1].strip()}"
        else:
            message = commit_message
        repo.index.commit(message, author=AGENT_ACTOR, committer=AGENT_ACTOR)
    return GitOpResult(ok=True, git_status=repo.git.status("--short"))


def clone_setup(
    repo_path: str,
    *,
    bare_repo_path: str,
    checkout_ref: str | None,
    branch_name: str | None,
) -> GitOpResult:
    target = Path(repo_path)
    shutil.rmtree(target, ignore_errors=True)
    repo = Repo.clone_from(f"world-git:{bare_repo_path}", target)
    trust_git_directory(target)
    with repo.config_writer() as config:
        config.set_value("user", "email", AGENT_ACTOR.email)
        config.set_value("user", "name", AGENT_ACTOR.name)
    if checkout_ref is not None:
        effective_branch = branch_name or "plato-task"
        # Reuse existing branch if it was previously pushed (resume scenario).
        # Otherwise create a fresh branch from the checkout ref.
        remote_ref = f"origin/{effective_branch}"
        try:
            repo.git.rev_parse("--verify", remote_ref)
            # Branch exists on remote — check it out
            repo.git.checkout("-B", effective_branch, remote_ref)
        except GitCommandError:
            # Branch doesn't exist yet — create from base ref
            repo.git.checkout("-B", effective_branch, checkout_ref)
    branch = repo.active_branch.name if not repo.head.is_detached else ""
    return GitOpResult(ok=True, branch=branch, head=repo.head.commit.hexsha)


def head_diff(repo_path: str, compare_ref: str) -> GitOpResult:
    repo = _repo(repo_path)
    return GitOpResult(ok=True, noop=repo.head.commit.tree.hexsha == repo.commit(compare_ref).tree.hexsha)


def push(repo_path: str, refspec: str, *, force: bool) -> GitOpResult:
    repo = _repo(repo_path)
    args = ["--porcelain"]
    if force:
        args.append("--force")
    args.extend(["origin", refspec])
    stdout = repo.git.push(*args)
    return GitOpResult(ok=True, stdout=stdout)


def fetch_origin(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    repo.remote("origin").fetch()
    return GitOpResult(ok=True)


def publish_state(repo_path: str, compare_ref: str) -> GitOpResult:
    repo = _repo(repo_path)
    return GitOpResult(
        ok=True,
        head_sha=repo.head.commit.hexsha,
        compare_sha=repo.commit(compare_ref).hexsha,
        git_status=repo.git.status("--short"),
        ahead_behind=repo.git.rev_list("--left-right", "--count", f"{compare_ref}...HEAD"),
    )


def rebase_ours(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    repo.remote("origin").fetch()
    repo.git.rebase("-X", "ours", "origin/main")
    return GitOpResult(ok=True)


def abort_rebase_reset_main(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    try:
        repo.git.rebase("--abort")
    except GitCommandError:
        pass
    repo.remote("origin").fetch()
    repo.git.reset("--hard", "origin/main")
    return GitOpResult(ok=True)


def force_push_main(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    repo.remote("origin").fetch()
    stdout = repo.git.push("--porcelain", "--force", "origin", "HEAD:main")
    return GitOpResult(ok=True, stdout=stdout)


def merge_origin_main(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    repo.remote("origin").fetch()
    repo.git.merge("origin/main", "-m", "Merge remote changes")
    return GitOpResult(ok=True)


def unmerged_files(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    files = sorted(str(path) for path in repo.index.unmerged_blobs().keys())
    return GitOpResult(ok=True, files=files)


def accept_theirs(repo_path: str, message: str) -> GitOpResult:
    repo = _repo(repo_path)
    repo.git.checkout("--theirs", ".")
    repo.git.add(A=True)
    repo.index.commit(message, author=PLATO_ACTOR, committer=PLATO_ACTOR)
    return GitOpResult(ok=True)


def current_head_info(repo_path: str) -> GitOpResult:
    repo = _repo(repo_path)
    branch = repo.active_branch.name if not repo.head.is_detached else ""
    return GitOpResult(ok=True, branch=branch, head=repo.head.commit.hexsha)


def commit_and_push_branch(repo_path: str, *, branch_name: str, commit_message: str) -> GitOpResult:
    repo = _repo(repo_path)
    repo.git.add(A=True)
    if repo.is_dirty(index=True, working_tree=False, untracked_files=True):
        repo.index.commit(commit_message)
    stdout = repo.git.push("--porcelain", "--force", "origin", f"HEAD:refs/heads/{branch_name}")
    return GitOpResult(ok=True, stdout=stdout)
