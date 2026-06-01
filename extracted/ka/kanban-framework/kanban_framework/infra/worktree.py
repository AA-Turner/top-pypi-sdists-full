from __future__ import annotations
from pathlib import Path
from kanban_framework.infra.git import Git, GitError


class WorktreeError(Exception):
    pass


class Worktree:
    def __init__(self, git: Git, repo_root: Path,
                 worktree_base: Path | None = None):
        self._git = git
        self._root = Path(repo_root)
        if worktree_base is not None:
            self._worktrees_dir = Path(worktree_base)
        else:
            self._worktrees_dir = self._root / ".kanban" / "worktrees"

    def create(self, task_id: str, branch: str) -> Path:
        path = self._worktree_path(task_id)
        if path.exists():
            raise WorktreeError(
                f"Worktree for {task_id} already exists at {path}"
            )
        try:
            self._git._run(
                ["worktree", "add", str(path), "-b", branch]
            )
        except GitError as e:
            raise WorktreeError(
                f"Failed to create worktree for {task_id}: {e}"
            ) from e
        # Verify .git exists after creation
        if not (path / ".git").exists():
            raise WorktreeError(
                f"Worktree created at {path} but .git directory missing. "
                f"Git operations (commit/push) will fail."
            )
        return path

    def remove(self, task_id: str, force: bool = False) -> None:
        path = self._worktree_path(task_id)
        if not path.exists():
            return
        args = ["worktree", "remove"]
        if force:
            args.append("--force")
        args.append(str(path))
        try:
            self._git._run(args)
        except GitError as e:
            raise WorktreeError(
                f"Failed to remove worktree {task_id}: {e}"
            ) from e

    def exists(self, task_id: str) -> bool:
        return self._worktree_path(task_id).exists()

    def list_all(self) -> list[dict]:
        return self._git.list_worktrees()

    def _worktree_path(self, task_id: str) -> Path:
        return self._worktrees_dir / task_id
