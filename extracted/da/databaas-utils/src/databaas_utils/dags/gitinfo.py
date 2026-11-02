"""Where a deploy came from: the repo, ref and commit, from CI variables or git."""

from __future__ import annotations

import os
import re
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

_GIT_TIMEOUT = 10


@dataclass(frozen=True)
class GitInfo:
    """Repo, ref, commit and CI run URL of a deploy."""

    repo: str = ""
    ref: str = ""
    commit: str = ""
    run_url: str = ""


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _repo_from_remote(url: str) -> str:
    match = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?/?$", url)
    return match.group(1) if match else url


def collect(root: Path, env: Mapping[str, str] | None = None) -> GitInfo:
    """Gather provenance for `root`. CI variables win over local git state."""
    source = env if env is not None else os.environ
    # GITHUB_HEAD_REF is the PR's branch; GITHUB_REF_NAME on a PR is "<n>/merge".
    ref = (
        source.get("GITHUB_HEAD_REF")
        or source.get("GITHUB_REF_NAME")
        or source.get("BITBUCKET_BRANCH")
        or _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    )
    if ref == "HEAD":
        ref = ""
    commit = (
        source.get("GITHUB_SHA")
        or source.get("BITBUCKET_COMMIT")
        or _git(root, "rev-parse", "HEAD")
    )
    if source.get("GITHUB_REPOSITORY"):
        repo = source["GITHUB_REPOSITORY"]
    elif source.get("BITBUCKET_WORKSPACE") and source.get("BITBUCKET_REPO_SLUG"):
        repo = f"{source['BITBUCKET_WORKSPACE']}/{source['BITBUCKET_REPO_SLUG']}"
    else:
        repo = _repo_from_remote(_git(root, "remote", "get-url", "origin"))
    return GitInfo(
        repo=repo,
        ref=ref,
        commit=commit,
        run_url=_run_url(source),
    )


def _run_url(source: Mapping[str, str]) -> str:
    if source.get("GITHUB_RUN_ID") and source.get("GITHUB_REPOSITORY"):
        server = source.get("GITHUB_SERVER_URL", "https://github.com")
        repo, run = source["GITHUB_REPOSITORY"], source["GITHUB_RUN_ID"]
        return f"{server}/{repo}/actions/runs/{run}"
    if source.get("BITBUCKET_BUILD_NUMBER") and source.get("BITBUCKET_WORKSPACE"):
        return (
            f"https://bitbucket.org/{source['BITBUCKET_WORKSPACE']}/"
            f"{source.get('BITBUCKET_REPO_SLUG', '')}/pipelines/results/"
            f"{source['BITBUCKET_BUILD_NUMBER']}"
        )
    return ""
