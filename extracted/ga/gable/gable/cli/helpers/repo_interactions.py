import datetime
import os
import re
from typing import Optional, TypedDict, Union
from urllib.parse import unquote, urljoin

import click
import giturlparse
import requests
from loguru import logger


def get_ci_git_origins() -> list[str]:
    """Returns a list of known CI git origins. Wrap in a function to make testing easier"""
    # TODO: Fill in additional know fallbacks for Github/BitBucket, etc.
    ci_origins_from_env = [
        # Gitlab, in priority order
        os.environ.get("CI_PROJECT_URL"),
        os.environ.get("CI_REPOSITORY_URL"),
        (
            f"{os.environ.get('CI_SERVER_HOST')}/{os.environ.get('CI_PROJECT_PATH')}"
            if os.environ.get("CI_SERVER_HOST") and os.environ.get("CI_PROJECT_PATH")
            else None
        ),
        # Github, in priority order
        (
            f"{os.environ.get('GITHUB_SERVER_URL')}/{os.environ.get('GITHUB_REPOSITORY')}"
            if os.environ.get("GITHUB_SERVER_URL")
            and os.environ.get("GITHUB_REPOSITORY")
            else None
        ),
    ]

    return list(filter(None, ci_origins_from_env))


class GitInfo(TypedDict):
    gitHash: str
    gitBranch: str
    gitRemoteOriginHTTPS: str
    gitSSHRepo: str
    gitUser: str
    localRepoRootDir: str
    mergedAt: datetime.datetime


# Remove the git@ prefix from a git URL if it exists
def strip_ssh_user(s: str) -> str:
    # user@...
    return re.sub(r"^(.+)@", "", s)


def strip_git_ssh_password(s: str) -> str:
    """Changes user:password@... to user@...
    Also handles bug in giturlparse's url2ssh where it returns git@user:password@...
    """
    # giturlparse bug
    # git@user:password@...
    result = re.sub(r"^[^@]+@(.+):.+@", r"\1@", s)
    # Normal ssh user password
    # user:password@...
    result = re.sub(r"^(.+):.+@", r"\1@", result)
    return result


def strip_git_suffix(s: str) -> str:
    return s[:-4] if s.endswith(".git") else s


def join_repo_and_path(repo: str, path: str) -> str:
    # Remove trailing and preceding slashes
    repo_clean = repo.strip("/")
    clean_path = path.strip("/")

    # Join the two
    return urljoin(f"{repo_clean}/", clean_path)


def normalize_git_ssh_url(s: str) -> str:
    """Normalizes a git SSH URL to the form 'user@host:owner/repo'."""
    return strip_git_suffix(strip_git_ssh_password(s))


def get_pr_link() -> Union[str, None]:
    """Returns the PR link for the current CI environment.
    If the environment is not recognized, returns None.
    """
    return get_github_pr_link() or get_gitlab_pr_link()


def get_gitlab_pr_link() -> Union[str, None]:
    """Uses the default gitlab environment variables to get the PR link.
    see https://docs.gitlab.com/ee/ci/variables/predefined_variables.html#predefined-variables-for-merge-request-pipelines
    """
    gitlab_event_type = os.environ.get("CI_PIPELINE_SOURCE")
    gitlab_server_url = os.environ.get("CI_SERVER_URL")
    gitlab_project_path = os.environ.get("CI_PROJECT_PATH")

    if not gitlab_event_type or not gitlab_server_url or not gitlab_project_path:
        return None

    if gitlab_event_type == "merge_request_event":
        gitlab_merge_request_id = os.environ.get("CI_MERGE_REQUEST_IID")
        if gitlab_merge_request_id:
            return f"{gitlab_server_url}/{gitlab_project_path}/-/merge_requests/{gitlab_merge_request_id}"
    elif gitlab_event_type == "push":
        # Since there is no merge request ID on a push to the main branch,
        # we fall back to the commit SHA to generate the link to the commit.
        gitlab_commit_sha = os.environ.get("CI_COMMIT_SHA")
        if gitlab_commit_sha:
            return f"{gitlab_server_url}/{gitlab_project_path}/-/commit/{gitlab_commit_sha}"

    return None


def get_github_pr_link() -> Union[str, None]:
    """Uses the default github environment variables to get the PR link.
    see https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
    """
    github_event_name = os.environ.get("GITHUB_EVENT_NAME")
    if github_event_name == "pull_request":
        return get_github_pr_link_from_env_vars()
    elif github_event_name == "push":
        return get_github_pr_link_from_api()
    return None


def get_github_pr_link_from_env_vars() -> Optional[str]:
    github_ref_name = os.environ.get("GITHUB_REF_NAME")  # e.g. 123/merge
    github_server_url = os.environ.get("GITHUB_SERVER_URL")
    github_repository = os.environ.get("GITHUB_REPOSITORY")  # e.g. owner/repo
    if github_ref_name and github_server_url and github_repository:
        return f"{github_server_url}/{github_repository}/pull/{github_ref_name.split('/')[0]}"


def get_github_pr_link_from_api() -> Optional[str]:
    github_token = os.environ.get("GITHUB_TOKEN")
    git_hash = os.environ.get("GITHUB_SHA")
    github_api_url = os.environ.get("GITHUB_API_URL")  # e.g. https://api.github.com
    github_repository = os.environ.get("GITHUB_REPOSITORY")  # e.g. owner/repo
    if github_token and git_hash and github_api_url and github_repository:
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response = requests.get(
            f"{github_api_url}/repos/{github_repository}/commits/{git_hash}",
            headers=headers,
        ).json()
        if isinstance(response, dict):
            if response.get("status") == 403:
                logger.warning(
                    f"GITHUB_TOKEN provided does not have pull_request:read permissions to get pull request URLS: {response.get('documentation_url')}"
                )
                return None
        if len(response) != 1:
            return None
        return response[0].get("html_url")


def get_git_repo_info(path: Union[os.PathLike, str]) -> GitInfo:
    """Returns a dictionary with information about the git repo at the given path.
    If the given path is not in a git repo, or the repo doesn't have an origin remote,
    an exception is raised."""
    # Conditionally import git to avoid a hard dependency on git being installed if it's
    # not needed.
    from git import InvalidGitRepositoryError
    from git.repo import Repo

    try:
        repo = Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise click.ClickException(
            f"The directory '{path}' must be within a git repository."
        )

    if "origin" not in [r.name for r in repo.remotes]:
        raise click.ClickException(
            f"The git repository containing '{path}' must have an 'origin' remote."
        )

    # In a detached HEAD state, the active branch is not available
    # and we cannot get the branch name.
    # This can happen in CI environments or when checking out a specific commit.
    if not repo.head.is_detached:
        git_branch = repo.active_branch.name
    else:
        # Fallback to Github or GitLab environment variables if available
        git_branch = (
            os.environ.get("GITHUB_HEAD_REF")
            or os.environ.get("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME")
            or ""
        )

    # Decode the git URL, no-op if it's already done by the git library
    parsed_repo = giturlparse.parse(unquote(get_origin_url(repo.remotes.origin.url)))
    return {
        "gitHash": repo.head.commit.hexsha,
        "gitBranch": git_branch,
        "gitRemoteOriginHTTPS": parsed_repo.url2https,
        "gitSSHRepo": normalize_git_ssh_url(parsed_repo.url2ssh),
        "gitUser": repo.head.commit.author.name or "unknown-git-user",
        "localRepoRootDir": os.path.dirname(repo.git_dir),
        "mergedAt": repo.head.commit.committed_datetime,
    }


def get_relative_file_path(git_info: GitInfo, local_file_path: str) -> str:
    absolute_file_path = os.path.abspath(local_file_path)
    relative_path = os.path.relpath(absolute_file_path, git_info["localRepoRootDir"])
    return relative_path


def get_git_ssh_file_path(git_info: GitInfo, local_file_path: str) -> str:
    relative_path = get_relative_file_path(git_info, local_file_path)
    return join_repo_and_path(git_info["gitSSHRepo"], relative_path)


def get_origin_url(local_repo_origin: str) -> str:
    """Decide which git origin to used based on the origin of the local git repository, and
    CI environment variables."""
    ci_origins = get_ci_git_origins()
    logger.trace("Determining remote origin URL")
    logger.trace(f"\tremote.origin.url: {local_repo_origin}")
    logger.trace(f"\tCI environment variable URLs: {ci_origins}")
    if len(ci_origins) == 0 and not local_repo_origin:
        raise ValueError("Unable to detect git remote url - is this within a git repo?")
    # CI Environment variables take precedence, and come in priority order
    chosen_origin = ci_origins[0] if len(ci_origins) > 0 else local_repo_origin
    logger.trace(f"Using remote origin {chosen_origin}")
    return chosen_origin
