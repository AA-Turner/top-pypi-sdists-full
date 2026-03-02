"""Repository management for local Git repositories."""

from pathlib import Path
from typing import Optional

from git import Repo

from ..core.exceptions import RepositoryError
from ..core.models import RepositoryEntity
from ..utils.logger import log


class RepositoryManager:
    """Manages local Git repository operations."""

    def __init__(self):
        """Initialize repository manager."""
        pass

    def get_or_clone(
        self,
        repo_path: str,
        skip_commit_count: bool = False
    ) -> tuple[Repo, RepositoryEntity]:
        """Get a local repository.

        Args:
            repo_path: Local path to repository
            skip_commit_count: Whether to skip counting commits (unused, kept for API compatibility)

        Returns:
            Tuple of (git.Repo, RepositoryEntity)

        Raises:
            RepositoryError: If repository cannot be accessed or path doesn't exist
        """
        # Only support local paths
        if not Path(repo_path).exists():
            raise RepositoryError(
                f"Repository path does not exist: {repo_path}. "
                "Remote repository URLs are not supported - please provide a local path."
            )

        return self._open_local_repo(repo_path)

    def _open_local_repo(self, path: str) -> tuple[Repo, RepositoryEntity]:
        """Open a local repository.

        Args:
            path: Local path to repository

        Returns:
            Tuple of (git.Repo, RepositoryEntity)
        """
        log.info(f"Opening local repository: {path}")

        try:
            repo = Repo(path)

            # Get repository info
            origin_url = self._get_origin_url(repo)
            repo_name = Path(path).name

            entity = RepositoryEntity(
                url=origin_url or f"file://{path}",
                name=repo_name,
                owner=None,
                default_branch=repo.active_branch.name,
                last_ingested=None,
                ingestion_status="pending",
            )

            return repo, entity

        except Exception as e:
            raise RepositoryError(f"Failed to open local repository {path}: {e}")

    def _get_origin_url(self, repo: Repo) -> Optional[str]:
        """Get the origin URL of a repository.

        Args:
            repo: Git repository

        Returns:
            Origin URL or None
        """
        try:
            if hasattr(repo.remotes, "origin"):
                return repo.remotes.origin.url
        except Exception:
            pass
        return None

    def get_source_files(
        self,
        repo: Repo,
        extensions: list[str],
        ignore_patterns: list[str] = None
    ) -> list[Path]:
        """Get all source files matching given extensions.

        Args:
            repo: Git repository
            extensions: List of file extensions (e.g., ['.py', '.ts', '.js'])
            ignore_patterns: Patterns to ignore (e.g., "__pycache__", "venv")

        Returns:
            List of source file paths
        """
        if ignore_patterns is None:
            ignore_patterns = [
                "__pycache__",
                "*.pyc",
                "*.pyo",
                ".git",
                ".venv",
                "venv",
                "env",
                "node_modules",
                ".tox",
                ".pytest_cache",
                "*.egg-info",
                "dist",
                "build",
            ]

        repo_path = Path(repo.working_dir)
        source_files = []

        # Normalize extensions to lowercase
        extensions = [ext.lower() for ext in extensions]

        for source_file in repo_path.rglob("*"):
            # Check if file (not directory)
            if not source_file.is_file():
                continue

            # Check extension
            if source_file.suffix.lower() not in extensions:
                continue

            # Check ignore patterns
            relative_path = source_file.relative_to(repo_path)
            if any(pattern in str(relative_path) for pattern in ignore_patterns):
                continue

            source_files.append(source_file)

        log.info(f"Found {len(source_files)} source files with extensions {extensions}")
        return source_files

    def get_python_files(self, repo: Repo, ignore_patterns: list[str] = None) -> list[Path]:
        """Get all Python files in a repository.

        Args:
            repo: Git repository
            ignore_patterns: Patterns to ignore (e.g., "__pycache__", "venv")

        Returns:
            List of Python file paths

        Note:
            This is a convenience wrapper around get_source_files() for backward compatibility.
        """
        return self.get_source_files(repo, ['.py'], ignore_patterns)
