"""CLI helpers for hierarchy commands.

Provides shared utility functions for hierarchy CLI commands.
"""

from __future__ import annotations

import subprocess


def resolve_owner_repo(
    *,
    owner: str | None = None,
    repo: str | None = None,
) -> tuple[str, str]:
    """Resolve GitHub owner and repo from arguments or git remote.

    Args:
        owner: Explicit owner. If None, detect from git remote.
        repo: Explicit repo. If None, detect from git remote.

    Returns:
        Tuple of (owner, repo).

    Raises:
        ValueError: If owner/repo cannot be resolved.
    """
    if owner and repo:
        return (owner, repo)

    # Try to detect from git remote
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            url = result.stdout.strip()
            # Handle HTTPS: https://github.com/owner/repo.git
            # Handle SSH (SCP): git@github.com:owner/repo.git
            # Handle SSH (URL): ssh://git@github.com/owner/repo.git
            for prefix in ["https://github.com/", "git@github.com:", "ssh://git@github.com/"]:
                if url.startswith(prefix):
                    remainder = url[len(prefix) :]
                    remainder = remainder.removesuffix(".git")
                    parts = remainder.split("/")
                    if len(parts) >= 2:
                        return (owner or parts[0], repo or parts[1])
    except FileNotFoundError:
        pass

    msg = (
        "Cannot resolve GitHub owner/repo. "
        "Provide --owner and --repo, or run from a git repository with an 'origin' remote."
    )
    raise ValueError(msg)
