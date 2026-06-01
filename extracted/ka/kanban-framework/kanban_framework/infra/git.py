from __future__ import annotations
import subprocess
from pathlib import Path


class GitError(Exception):
    pass


class Git:
    def __init__(self, repo_root: Path):
        self._root = Path(repo_root)
        self._git = ["git", "-C", str(self._root)]

    def is_repo(self) -> bool:
        return (self._root / ".git").exists()

    def current_branch(self) -> str:
        return self._run(["rev-parse", "--abbrev-ref", "HEAD"]).strip()

    def has_uncommitted_changes(self) -> bool:
        result = self._run(["status", "--porcelain"], check=False)
        return len(result.strip()) > 0

    def add(self, paths: list[str]) -> None:
        self._run(["add"] + paths)

    def commit(self, message: str) -> bool:
        if not self._has_staged():
            return False
        self._run(["commit", "-m", message])
        return True

    def push(self) -> None:
        branch = self.current_branch()
        self._run(["push", "origin", branch])

    def list_worktrees(self) -> list[dict]:
        output = self._run(["worktree", "list", "--porcelain"], check=False)
        return self._parse_worktree_list(output)

    def diff_stat(self) -> dict:
        """Return {files_changed, added, deleted, file_list} from git diff."""
        stat = self._run(["diff", "--shortstat"], check=False).strip()
        name_output = self._run(["diff", "--name-only"], check=False).strip()
        added, deleted = 0, 0
        files_changed = 0
        if stat:
            import re
            m = re.search(r"(\d+) files? changed", stat)
            if m:
                files_changed = int(m.group(1))
            m = re.search(r"(\d+) insertion", stat)
            if m:
                added = int(m.group(1))
            m = re.search(r"(\d+) deletion", stat)
            if m:
                deleted = int(m.group(1))
        file_list = name_output.split("\n") if name_output else []
        return {
            "files_changed": files_changed,
            "added": added,
            "deleted": deleted,
            "file_list": file_list,
        }

    def _has_staged(self) -> bool:
        result = self._run(["diff", "--cached", "--name-only"], check=False)
        return len(result.strip()) > 0

    @staticmethod
    def _sanitize_arg(arg: str) -> str:
        """Reject obviously dangerous git arguments. (#295)"""
        dangerous = (";", "|", "&", "$", "`", "(", ")", "{", "}", "<", ">", "\n", "\r")
        for ch in dangerous:
            if ch in arg:
                raise GitError(f"Dangerous character in git argument: {ch!r}")
        return arg

    def _run(self, args: list[str], check: bool = True) -> str:
        try:
            from kanban_framework.infra.filesystem import Filesystem
            safe_args = [self._sanitize_arg(a) if isinstance(a, str) else str(a) for a in args]
            result = Filesystem.run_no_window(self._git + safe_args, check=check)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise GitError(
                f"git {' '.join(args)}: {e.stderr.strip()}"
            ) from e

    @staticmethod
    def _parse_worktree_list(output: str) -> list[dict]:
        worktrees = []
        current = {}
        for line in output.strip().split("\n"):
            if line.startswith("worktree "):
                if current:
                    worktrees.append(current)
                current = {"path": line.split(" ", 1)[1]}
            elif line.startswith("HEAD "):
                current["head"] = line.split(" ", 1)[1]
            elif line.startswith("branch "):
                parts = line.split(" ", 2)
                current["branch"] = parts[2] if len(parts) > 2 else ""
        if current:
            worktrees.append(current)
        return worktrees
