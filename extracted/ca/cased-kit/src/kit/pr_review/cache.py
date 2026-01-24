"""Repository caching functionality for PR review."""

import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

from .config import ReviewConfig


class RepoCache:
    """Manages cached repositories for efficient PR analysis."""

    def __init__(self, config: ReviewConfig, quiet: bool = False):
        self.config = config
        self.quiet = quiet
        self.cache_dir = Path(config.cache_directory).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_repo_path(self, owner: str, repo: str, sha: str) -> str:
        """Get repository path, using cache if available and valid."""
        if not self.config.cache_repos:
            # Caching disabled, use temporary directory
            return self._clone_to_temp(owner, repo, sha)

        repo_cache_dir = self.cache_dir / owner / repo

        # Check if we have a valid cached version
        if self._is_cache_valid(repo_cache_dir, sha):
            if not self.quiet:
                print(f"Using cached repository: {repo_cache_dir}")
            self._checkout_sha(repo_cache_dir, sha)
            return str(repo_cache_dir)

        # Need to clone or update cache
        return self._update_cache(owner, repo, sha, repo_cache_dir)

    def _is_cache_valid(self, repo_path: Path, target_sha: str) -> bool:
        """Check if cached repository is valid and recent enough."""
        if not repo_path.exists():
            return False

        if not (repo_path / ".git").exists():
            return False

        # Check if cache is too old
        try:
            cache_time = repo_path.stat().st_mtime
            age_hours = (time.time() - cache_time) / 3600
            if age_hours > self.config.cache_ttl_hours:
                if not self.quiet:
                    print(f"Cache expired ({age_hours:.1f}h old), refreshing...")
                return False
        except OSError:
            return False

        # Check if we have the target SHA
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "cat-file", "-e", target_sha], capture_output=True, check=False
            )
            return result.returncode == 0
        except subprocess.SubprocessError:
            return False

    def _update_cache(self, owner: str, repo: str, sha: str, repo_path: Path) -> str:
        """Clone or update the cached repository."""
        repo_url = f"https://github.com/{owner}/{repo}.git"

        if repo_path.exists():
            if not self.quiet:
                print(f"Updating cached repository: {repo_path}")
            try:
                # Fetch latest changes
                subprocess.run(["git", "-C", str(repo_path), "fetch", "origin"], check=True, capture_output=True)

                # Try to checkout the target SHA
                self._checkout_sha(repo_path, sha)

                # Update cache timestamp
                repo_path.touch()

                return str(repo_path)

            except subprocess.CalledProcessError as e:
                if not self.quiet:
                    print(f"Failed to update cache, re-cloning: {e}")
                # Remove corrupted cache and re-clone
                shutil.rmtree(repo_path)

        # Fresh clone
        if not self.quiet:
            print(f"Cloning repository to cache: {repo_path}")
        repo_path.parent.mkdir(parents=True, exist_ok=True)

        subprocess.run(["git", "clone", "--depth", "50", repo_url, str(repo_path)], check=True, capture_output=True)

        self._checkout_sha(repo_path, sha)
        return str(repo_path)

    def _checkout_sha(self, repo_path: Path, sha: str) -> None:
        """Checkout specific SHA in the repository."""
        try:
            # First try to checkout directly
            subprocess.run(["git", "-C", str(repo_path), "checkout", sha], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # If that fails, fetch and try again
            subprocess.run(["git", "-C", str(repo_path), "fetch", "origin", sha], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo_path), "checkout", sha], check=True, capture_output=True)

    def _clone_to_temp(self, owner: str, repo: str, sha: str) -> str:
        """Clone repository to temporary directory (no caching)."""
        import tempfile

        repo_url = f"https://github.com/{owner}/{repo}.git"
        temp_dir = Path(tempfile.mkdtemp())
        repo_path = temp_dir / f"{owner}-{repo}"

        subprocess.run(["git", "clone", "--depth", "50", repo_url, str(repo_path)], check=True, capture_output=True)

        self._checkout_sha(repo_path, sha)
        return str(repo_path)

    def cleanup_cache(self, max_size_gb: Optional[float] = None) -> None:
        """Clean up old cache entries."""
        if not self.cache_dir.exists():
            return

        # Get cache size
        total_size = sum(f.stat().st_size for f in self.cache_dir.rglob("*") if f.is_file()) / (
            1024**3
        )  # Convert to GB

        print(f"Cache size: {total_size:.2f} GB")

        if max_size_gb and total_size > max_size_gb:
            print(f"Cache exceeds {max_size_gb} GB, cleaning up...")

            # Get all repo directories with their last modified times
            repos = []
            for owner_dir in self.cache_dir.iterdir():
                if owner_dir.is_dir():
                    for repo_dir in owner_dir.iterdir():
                        if repo_dir.is_dir():
                            repos.append((repo_dir.stat().st_mtime, repo_dir))

            # Sort by last modified (oldest first)
            repos.sort()

            # Remove oldest repos until we're under the limit
            for _, repo_dir in repos:
                if total_size <= max_size_gb:
                    break

                print(f"Removing old cache: {repo_dir}")
                repo_size = sum(f.stat().st_size for f in repo_dir.rglob("*") if f.is_file()) / (1024**3)

                shutil.rmtree(repo_dir)
                total_size -= repo_size

    def clear_cache(self) -> None:
        """Clear all cached repositories."""
        if self.cache_dir.exists():
            print(f"Clearing cache: {self.cache_dir}")
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
