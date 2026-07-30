"""GitHub write APIs for sync-back (commits and pull requests).

Uses the Git Data API to assemble a single aggregated commit per run (blobs ->
tree -> commit -> ref), so all changed documents land in one commit and, in PR
mode, one pull request. Authentication reuses the OSS ``GitHubTokenProvider``
(GitHub App installation token or PAT); the minted installation token carries
the App's write permissions.
"""

from __future__ import annotations

import base64
import logging
from dataclasses import dataclass
from typing import List, NoReturn, Optional, Tuple
from urllib.parse import quote

import requests

from datahub.ingestion.source.github_documents.github_api import (
    GITHUB_API_BASE,
    GitHubTokenProvider,
)

logger = logging.getLogger(__name__)


class GitHubWriteError(Exception):
    """A GitHub write operation failed."""


@dataclass(frozen=True)
class CommitFile:
    """A file to include in a sync-back commit."""

    path: str
    content: str


@dataclass(frozen=True)
class PullRequest:
    """A created or existing pull request."""

    number: int
    url: str


class GitHubWriteClient:
    def __init__(
        self,
        token_provider: GitHubTokenProvider,
        timeout_seconds: int = 30,
    ) -> None:
        self._token_provider = token_provider
        self._session = requests.Session()
        self._timeout = timeout_seconds

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._token_provider.get_token()}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def branch_exists(self, repo: str, branch: str) -> bool:
        """Return True if a branch ref exists in the repository."""
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/ref/heads/{quote(branch, safe='')}"
        response = self._session.get(
            url, headers=self._headers(), timeout=self._timeout
        )
        return response.status_code == 200

    def get_current_blob_sha(self, repo: str, path: str, branch: str) -> Optional[str]:
        """Return the blob sha of a file on a branch, or None if absent."""
        url = (
            f"{GITHUB_API_BASE}/repos/{repo}/contents/{quote(path, safe='')}"
            f"?ref={quote(branch, safe='')}"
        )
        response = self._session.get(
            url, headers=self._headers(), timeout=self._timeout
        )
        if response.status_code == 404:
            return None
        body = self._json_or_raise(response, f"get contents for {path}")
        sha = body.get("sha")
        return sha if isinstance(sha, str) else None

    def fetch_file_content(self, repo: str, path: str, branch: str) -> Optional[str]:
        """Return decoded UTF-8 file content on a branch, or None if absent."""
        url = (
            f"{GITHUB_API_BASE}/repos/{repo}/contents/{quote(path, safe='')}"
            f"?ref={quote(branch, safe='')}"
        )
        response = self._session.get(
            url, headers=self._headers(), timeout=self._timeout
        )
        if response.status_code == 404:
            return None
        body = self._json_or_raise(response, f"get contents for {path}")
        encoded = body.get("content")
        if not isinstance(encoded, str):
            return None
        return base64.b64decode(encoded).decode("utf-8")

    def fetch_blob_content(self, repo: str, blob_sha: str) -> str:
        """Return decoded UTF-8 content for a git blob SHA."""
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/blobs/{blob_sha}"
        body = self._json_or_raise(
            self._session.get(url, headers=self._headers(), timeout=self._timeout),
            f"get blob {blob_sha}",
        )
        encoded = body.get("content")
        if not isinstance(encoded, str):
            raise GitHubWriteError(f"Unexpected blob payload for {blob_sha}.")
        return base64.b64decode(encoded).decode("utf-8")

    def create_aggregated_commit(
        self,
        repo: str,
        base_branch: str,
        files: List[CommitFile],
        message: str,
        *,
        deletions: Optional[List[str]] = None,
    ) -> Tuple[str, str]:
        """Create one commit containing all file writes and deletes on base_branch head.

        Returns a (base_sha, commit_sha) tuple. Does not move any ref; the caller
        decides whether to fast-forward the target branch (direct commit) or push
        a PR branch.
        """
        base_sha = self._get_branch_head_sha(repo, base_branch)
        base_tree_sha = self._get_commit_tree_sha(repo, base_sha)

        # Deletion entries carry "sha": None (GitHub's Git Trees API deletes a path
        # when its sha is null), so the list holds mixed str/None values.
        tree_entries: List[dict] = []
        for file in files:
            blob_sha = self._create_blob(repo, file.content)
            tree_entries.append(
                {
                    "path": file.path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob_sha,
                }
            )
        for path in deletions or []:
            tree_entries.append(
                {
                    "path": path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": None,
                }
            )
        tree_sha = self._create_tree(repo, base_tree_sha, tree_entries)
        commit_sha = self._create_commit(repo, message, tree_sha, base_sha)
        return base_sha, commit_sha

    def update_branch_ref(self, repo: str, branch: str, commit_sha: str) -> None:
        """Fast-forward an existing branch to a commit (direct-commit mode)."""
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/refs/heads/{quote(branch, safe='')}"
        response = self._session.patch(
            url,
            headers=self._headers(),
            json={"sha": commit_sha, "force": False},
            timeout=self._timeout,
        )
        self._json_or_raise(response, f"update branch {branch}")

    def create_or_reset_branch(self, repo: str, branch: str, commit_sha: str) -> None:
        """Create the PR branch at commit_sha, or reset it there if it exists."""
        create_url = f"{GITHUB_API_BASE}/repos/{repo}/git/refs"
        response = self._session.post(
            create_url,
            headers=self._headers(),
            json={"ref": f"refs/heads/{branch}", "sha": commit_sha},
            timeout=self._timeout,
        )
        if response.status_code == 201:
            return
        # 422 means the ref already exists; force-update it to our new commit.
        if response.status_code == 422:
            update_url = (
                f"{GITHUB_API_BASE}/repos/{repo}/git/refs/heads/"
                f"{quote(branch, safe='')}"
            )
            update = self._session.patch(
                update_url,
                headers=self._headers(),
                json={"sha": commit_sha, "force": True},
                timeout=self._timeout,
            )
            self._json_or_raise(update, f"reset branch {branch}")
            return
        self._raise(response, f"create branch {branch}")

    def find_open_pull_request(
        self, repo: str, head_branch: str, base_branch: str
    ) -> Optional[PullRequest]:
        """Find an already-open PR for head_branch -> base_branch."""
        owner = repo.split("/")[0]
        url = (
            f"{GITHUB_API_BASE}/repos/{repo}/pulls"
            f"?state=open&head={quote(f'{owner}:{head_branch}', safe='')}"
            f"&base={quote(base_branch, safe='')}"
        )
        response = self._session.get(
            url, headers=self._headers(), timeout=self._timeout
        )
        body = self._json_list_or_raise(response, "list pull requests")
        if not body:
            return None
        pr = body[0]
        return PullRequest(number=pr["number"], url=pr["html_url"])

    def create_pull_request(
        self,
        repo: str,
        head_branch: str,
        base_branch: str,
        title: str,
        body: str,
    ) -> PullRequest:
        """Open a new PR from head_branch into base_branch."""
        url = f"{GITHUB_API_BASE}/repos/{repo}/pulls"
        response = self._session.post(
            url,
            headers=self._headers(),
            json={
                "title": title,
                "head": head_branch,
                "base": base_branch,
                "body": body,
            },
            timeout=self._timeout,
        )
        created = self._json_or_raise(response, "create pull request")
        return PullRequest(number=created["number"], url=created["html_url"])

    def update_pull_request_body(self, repo: str, pull_number: int, body: str) -> None:
        """Update the body of an existing pull request."""
        url = f"{GITHUB_API_BASE}/repos/{repo}/pulls/{pull_number}"
        response = self._session.patch(
            url,
            headers=self._headers(),
            json={"body": body},
            timeout=self._timeout,
        )
        self._json_or_raise(response, f"update pull request #{pull_number}")

    def _get_branch_head_sha(self, repo: str, branch: str) -> str:
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/ref/heads/{quote(branch, safe='')}"
        body = self._json_or_raise(
            self._session.get(url, headers=self._headers(), timeout=self._timeout),
            f"get ref for {branch}",
        )
        return body["object"]["sha"]

    def _get_commit_tree_sha(self, repo: str, commit_sha: str) -> str:
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/commits/{commit_sha}"
        body = self._json_or_raise(
            self._session.get(url, headers=self._headers(), timeout=self._timeout),
            f"get commit {commit_sha}",
        )
        return body["tree"]["sha"]

    def _create_blob(self, repo: str, content: str) -> str:
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/blobs"
        body = self._json_or_raise(
            self._session.post(
                url,
                headers=self._headers(),
                json={"content": content, "encoding": "utf-8"},
                timeout=self._timeout,
            ),
            "create blob",
        )
        return body["sha"]

    def _create_tree(self, repo: str, base_tree_sha: str, entries: List[dict]) -> str:
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/trees"
        body = self._json_or_raise(
            self._session.post(
                url,
                headers=self._headers(),
                json={"base_tree": base_tree_sha, "tree": entries},
                timeout=self._timeout,
            ),
            "create tree",
        )
        return body["sha"]

    def _create_commit(
        self, repo: str, message: str, tree_sha: str, parent_sha: str
    ) -> str:
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/commits"
        body = self._json_or_raise(
            self._session.post(
                url,
                headers=self._headers(),
                json={"message": message, "tree": tree_sha, "parents": [parent_sha]},
                timeout=self._timeout,
            ),
            "create commit",
        )
        return body["sha"]

    def _json_or_raise(self, response: requests.Response, action: str) -> dict:
        if response.status_code in (200, 201):
            payload = response.json()
            if isinstance(payload, dict):
                return payload
            raise GitHubWriteError(f"Unexpected GitHub response for {action}.")
        self._raise(response, action)

    def _json_list_or_raise(
        self, response: requests.Response, action: str
    ) -> List[dict]:
        if response.status_code == 200:
            payload = response.json()
            if isinstance(payload, list):
                return payload
            raise GitHubWriteError(f"Unexpected GitHub response for {action}.")
        self._raise(response, action)

    @staticmethod
    def _raise(response: requests.Response, action: str) -> NoReturn:
        detail = ""
        try:
            detail = response.json().get("message", "")
        except ValueError:
            detail = response.text[:200]
        raise GitHubWriteError(
            f"GitHub API failed to {action} (HTTP {response.status_code}): {detail}"
        )
