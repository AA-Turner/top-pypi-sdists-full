from __future__ import annotations

from pathlib import Path

from git import Actor, Repo

from plato.git_ops.dispatch import run_request
from plato.git_ops.models import GitOpRequest
from plato.git_ops.repo import trust_git_directory

_ACTOR = Actor("Test", "test@example.com")


def _commit_file(repo: Repo, path: str, content: str, message: str) -> str:
    target = Path(repo.working_tree_dir or ".") / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    repo.git.add(A=True)
    return repo.index.commit(message, author=_ACTOR, committer=_ACTOR).hexsha


def test_head_diff_uses_tree_equivalence_for_noop(tmp_path):
    repo = Repo.init(tmp_path, initial_branch="main")
    trust_git_directory(tmp_path)

    base_sha = _commit_file(repo, "shared.txt", "base\n", "base")
    _commit_file(repo, "shared.txt", "changed\n", "change")
    _commit_file(repo, "shared.txt", "base\n", "revert")

    result = run_request(GitOpRequest.head_diff(str(tmp_path), base_sha))

    assert result.ok is True
    assert result.noop is True


def test_push_returns_error_result_on_non_fast_forward(tmp_path):
    bare = tmp_path / "origin.git"
    Repo.init(bare, bare=True, initial_branch="main")
    trust_git_directory(bare)

    first = Repo.clone_from(str(bare), tmp_path / "first")
    second = Repo.clone_from(str(bare), tmp_path / "second")
    trust_git_directory(tmp_path / "first")
    trust_git_directory(tmp_path / "second")

    _commit_file(first, "shared.txt", "base\n", "base")
    first.git.push("--porcelain", "origin", "HEAD:main")

    second.remote("origin").fetch()
    second.git.reset("--hard", "origin/main")
    _commit_file(second, "shared.txt", "second\n", "second")
    second.git.push("--porcelain", "origin", "HEAD:main")

    first.remote("origin").fetch()
    _commit_file(first, "shared.txt", "first\n", "first")

    result = run_request(GitOpRequest.push(str(tmp_path / "first"), "HEAD:main", force=False))

    assert result.ok is False
    assert result.stderr or result.stdout
