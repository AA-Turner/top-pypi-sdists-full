"""GitHub repository resolution utilities.

Resolves ``owner/repo`` from CLI arguments, state, or git remote URL.
Shared by all ``agdt-gh-*`` commands.
"""

import os
import re
import subprocess
import sys
from collections.abc import Mapping
from typing import Any

from ...config import load_platform_config
from ...state import get_repo_root, get_value
from ..subprocess_utils import run_safe

# GitHub remote URL patterns
_GITHUB_HTTPS_RE = re.compile(r"https?://(?:[^/@]+@)?github\.com(?::\d+)?/([\w.-]+)/([\w.-]+?)(?:\.git)?$")
_GITHUB_SSH_URL_RE = re.compile(r"ssh://git@github\.com(?::\d+)?/([\w.-]+)/([\w.-]+?)(?:\.git)?$")
_GITHUB_SSH_RE = re.compile(r"git@github\.com:([\w.-]+)/([\w.-]+?)(?:\.git)?$")
_GIT_REMOTE_TIMEOUT_SECONDS = 30


def _resolve_repo_from_git_remote() -> str | None:
    """Attempt to derive ``owner/repo`` from the git origin remote URL."""
    try:
        result = run_safe(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=_GIT_REMOTE_TIMEOUT_SECONDS,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        url = result.stdout.strip()
    except OSError, subprocess.TimeoutExpired:
        return None

    for pattern in (_GITHUB_HTTPS_RE, _GITHUB_SSH_URL_RE, _GITHUB_SSH_RE):
        m = pattern.search(url)
        if m:
            return f"{m.group(1)}/{m.group(2)}"

    return None


def _validate_repo_format(repo: str) -> str | None:
    """Return normalized ``owner/repo`` if valid, else ``None``."""
    repo = repo.strip()
    if repo.endswith(".git"):
        repo = repo[:-4]
    parts = repo.split("/")
    if len(parts) == 2 and all(parts):
        return repo
    return None


def _resolve_repo_from_platform_config() -> str | None:
    """Resolve ``platform.github.repo`` from ``.github/agdt-config.json``."""
    root = get_repo_root()
    if root is None:
        return None
    try:
        github_config = load_platform_config(str(root)).get("github")
    except Exception:
        return None
    if not isinstance(github_config, Mapping):
        return None
    config_repo = github_config.get("repo")
    if not isinstance(config_repo, str):
        return None
    return _validate_repo_format(config_repo)


def resolve_github_repo_safe(state: Mapping[str, Any] | None = None) -> str | None:
    """Resolve GitHub ``owner/repo`` without exiting on failure.

    Same resolution logic as :func:`resolve_github_repo` but returns
    ``None`` instead of calling ``sys.exit(1)`` when resolution fails.
    When ``state`` is provided, it is used instead of reading global state.

    Resolution order:
    1. ``github.repo`` state key.
    2. ``platform.github.repo`` state key.
    3. ``platform.github.repo`` from ``.github/agdt-config.json``.
    4. ``GITHUB_REPOSITORY`` environment variable.
    5. Git ``origin`` remote URL.
    """
    state_repo = state.get("github.repo") if state is not None else get_value("github.repo")
    if state is not None and isinstance(state.get("github"), Mapping):
        state_repo = state["github"].get("repo")
    if state_repo and isinstance(state_repo, str):
        validated = _validate_repo_format(state_repo)
        if validated:
            return validated

    platform_repo = state.get("platform.github.repo") if state is not None else None
    if state is not None and isinstance(state.get("platform"), Mapping):
        platform = state["platform"]
        if isinstance(platform.get("github"), Mapping):
            platform_repo = platform["github"].get("repo")
    elif state is None:
        platform_repo = get_value("platform.github.repo")
    if isinstance(platform_repo, str):
        validated = _validate_repo_format(platform_repo)
        if validated:
            return validated

    config_repo = _resolve_repo_from_platform_config()
    if config_repo:
        return config_repo

    environment_repo = os.environ.get("GITHUB_REPOSITORY")
    if environment_repo:
        validated = _validate_repo_format(environment_repo)
        if validated:
            return validated

    remote_repo = _resolve_repo_from_git_remote()
    if remote_repo:
        return remote_repo

    return None


def resolve_github_repo(cli_repo: str | None = None) -> str:
    """Resolve GitHub ``owner/repo`` from CLI arg, state, or git remote.

    Resolution order:
    1. Explicit *cli_repo* argument (``--repo`` flag).
    2. ``github.repo`` state key.
    3. ``platform.github.repo`` state key.
    4. ``platform.github.repo`` from ``.github/agdt-config.json``.
    5. ``GITHUB_REPOSITORY`` environment variable.
    6. Git ``origin`` remote URL.

    Calls ``sys.exit(1)`` when resolution fails.
    """
    if cli_repo:
        validated = _validate_repo_format(cli_repo)
        if validated:
            return validated
        print(
            f"Error: Invalid --repo format: {cli_repo!r}. Expected 'owner/repo'.",
            file=sys.stderr,
        )
        sys.exit(1)

    state_repo = get_value("github.repo")
    if state_repo and isinstance(state_repo, str):
        validated = _validate_repo_format(state_repo)
        if validated:
            return validated
        # State has a value but it's malformed — fall through to git remote

    platform_repo = get_value("platform.github.repo")
    if isinstance(platform_repo, str):
        validated = _validate_repo_format(platform_repo)
        if validated:
            return validated

    config_repo = _resolve_repo_from_platform_config()
    if config_repo:
        return config_repo

    environment_repo = os.environ.get("GITHUB_REPOSITORY")
    if environment_repo:
        validated = _validate_repo_format(environment_repo)
        if validated:
            return validated

    remote_repo = _resolve_repo_from_git_remote()
    if remote_repo:
        return remote_repo

    print(
        "Error: Could not determine GitHub repository. "
        "Provide --repo owner/repo, set github.repo in state, "
        "configure platform.github.repo in .github/agdt-config.json, "
        "set GITHUB_REPOSITORY to owner/repo, "
        "or ensure a GitHub origin remote is configured.",
        file=sys.stderr,
    )
    sys.exit(1)
