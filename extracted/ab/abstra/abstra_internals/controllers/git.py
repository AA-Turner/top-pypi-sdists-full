from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import requests

from abstra_internals.cloud_api import get_api_key_info
from abstra_internals.credentials import get_credentials, resolve_headers
from abstra_internals.environment import CLOUD_API_CLI_URL, REMOTE_GIT_URL, REMOTE_NAME
from abstra_internals.interface.cli.deploy_messages import DeployMessages
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.git import (
    AheadBehindInfo,
    GitCommit,
    GitStatusResponse,
    RemoteGitStatus,
    create_git_repository,
)
from abstra_internals.settings import Settings


class EmailProvider(ABC):
    """Interface that requires a get_email method."""

    @abstractmethod
    def get_email(self) -> str:
        pass


class DefaultEmailProvider(EmailProvider):
    """Concrete implementation with a default email."""

    def get_email(self) -> str:
        return "abstra@mail.com"


class GitController:
    def __init__(self, email_provider: EmailProvider = DefaultEmailProvider()):
        self.git_repository = create_git_repository(Settings.root_path)
        self.email_provider = email_provider
        self.git_email = email_provider.get_email()

        # Run git maintenance tasks (cleanup temp objects, gc if needed)
        self._run_maintenance()

    def _run_maintenance(self) -> None:
        """Run git maintenance tasks and log results."""
        result = self.git_repository.run_maintenance()
        if result.success and result.cleanup and result.cleanup.directories_cleaned > 0:
            mb_freed = result.cleanup.bytes_freed / (1024 * 1024)
            AbstraLogger.info(
                f"[Git] Maintenance: cleaned {result.cleanup.directories_cleaned} temp directories, freed {mb_freed:.1f} MB"
            )

    def _ensure_authentication(self) -> bool:
        try:
            if self.git_email is None:
                self.git_email = self.email_provider.get_email()

            if self.git_email is None:
                print("No email available for git configuration")
                return False

            self.git_repository.configure_git_user(
                fallback_email=self.git_email,
                fallback_name=self.git_email.split("@")[0],
            )

            credentials = get_credentials()
            if not credentials:
                return False

            if self.git_repository.has_remote(REMOTE_NAME):
                if not self.git_repository.set_remote_url(REMOTE_NAME, REMOTE_GIT_URL):
                    return False
            else:
                if not self.git_repository.add_remote(REMOTE_NAME, REMOTE_GIT_URL):
                    return False

            config_key = f"http.{REMOTE_GIT_URL}.extraHeader"
            config_value = f"Api-Authorization: Bearer {credentials}"

            if self.git_repository.get_git_config(config_key) == config_value:
                return True

            return self.git_repository.set_git_config(config_key, config_value)

        except Exception as e:
            print(f"Authentication setup failed: {e}")
            return False

    def _fetch_remote_status(self, branch: str = "main") -> RemoteGitStatus:
        try:
            credentials = get_credentials()
            if not credentials:
                return RemoteGitStatus(
                    success=False, message="No authentication credentials available"
                )

            api_url = f"{CLOUD_API_CLI_URL}/git/status"
            headers = {"Api-Authorization": f"Bearer {credentials}"}
            params = {"branch": branch}

            response = requests.get(api_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                try:
                    data = response.json()

                    if not isinstance(data, dict):
                        return RemoteGitStatus(
                            success=False,
                            message=f"Unexpected response format. Expected dict, got {type(data).__name__}",
                        )

                    return RemoteGitStatus(
                        success=data.get("success", True),
                        remote_commit=data.get("remote_commit"),
                        branch=data.get("branch", branch),
                        has_commits=data.get("has_commits", False),
                        available_branches=data.get("available_branches", [branch]),
                        message=data.get("message"),
                        ahead_behind=None,
                    )
                except ValueError as json_error:
                    return RemoteGitStatus(
                        success=False, message=f"Invalid JSON response: {json_error}"
                    )
            else:
                response_text = (
                    response.text[:200] if response.text else "No response body"
                )
                return RemoteGitStatus(
                    success=False,
                    message=f"API call failed with status {response.status_code}: {response_text}",
                )

        except Exception as e:
            return RemoteGitStatus(
                success=False, message=f"Error fetching remote status: {str(e)}"
            )

    def get_status(self) -> Dict[str, Any]:
        """
        Get the git status of the project, including current branch, last commit,
        whether the working tree has uncommitted changes, and a list of changed files.

        Returns:
            dict: ``{ available, branch, last_commit, has_changes, changed_files, ... }``.
            ``available`` is ``False`` when the project is not a git repository.
        """
        self._ensure_authentication()

        status = self.git_repository.get_repository_status()

        remote_status = None

        if status.available:
            remote_status = self._fetch_remote_status()

            if (
                remote_status.success
                and remote_status.remote_commit
                and status.last_commit
                and remote_status.remote_commit != status.last_commit.hash
            ):
                try:
                    ahead, behind = self.git_repository.get_ahead_behind_count(
                        status.last_commit.hash, remote_status.remote_commit
                    )
                    remote_status.ahead_behind = AheadBehindInfo(
                        ahead=ahead, behind=behind
                    )
                except Exception as e:
                    print(f"Failed to calculate ahead/behind: {e}")

                remote_status.has_conflicts = self.git_repository.check_merge_conflicts(
                    remote_status.remote_commit
                )

                if remote_status.ahead_behind:
                    remote_status.has_remote_changes = (
                        remote_status.ahead_behind.behind > 0
                    )
                else:
                    remote_status.has_remote_changes = (
                        remote_status.remote_commit != status.last_commit.hash
                    )

        status_response = GitStatusResponse(
            available=status.available,
            git_installed=status.git_installed,
            is_monorepo=status.is_monorepo,
            branch=status.branch,
            branches=status.branches,
            last_commit=status.last_commit,
            has_changes=status.has_changes,
            changed_files=status.changed_files,
            changed_files_with_status=status.changed_files_with_status,
            remote_status=remote_status,
        )

        return status_response.to_dict()

    def checkout_branch(self, branch_name: str) -> Dict[str, Any]:
        success, error_message = self.git_repository.checkout_branch(branch_name)

        message = f"Switched to branch '{branch_name}'" if success else error_message

        return {"success": success, "message": message}

    def checkout_commit(self, commit_hash: str) -> Dict[str, Any]:
        success, error_message = self.git_repository.checkout_commit(commit_hash)

        message = (
            f"Switched to commit '{commit_hash[:8]}'" if success else error_message
        )

        return {"success": success, "message": message}

    def pull_changes(
        self, strategy: str, allow_unrelated: bool, conflict_resolution: Optional[str]
    ) -> Dict[str, Any]:
        self._ensure_authentication()

        success, error_message = self.git_repository.pull_changes(
            strategy=strategy,
            allow_unrelated=allow_unrelated,
            conflict_resolution=conflict_resolution,
        )

        message = "Successfully pulled changes" if success else error_message

        return {"success": success, "message": message}

    def check_large_files(
        self, max_size_bytes: int = 5 * 1024 * 1024
    ) -> Dict[str, Any]:
        large_files = self.git_repository.get_large_files(max_size_bytes)
        return {
            "hasLargeFiles": len(large_files) > 0,
            "largeFiles": [
                {
                    "path": f.path,
                    "sizeBytes": f.size_bytes,
                    "sizeHuman": f.size_human,
                }
                for f in large_files
            ],
        }

    def commit_changes(
        self, message: str, author: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Stage and commit ALL current working-tree changes with the given message.

        Use this when the user asks to checkpoint progress or before deploying.
        Does NOT push. Fails if the project contains files larger than 5MB
        (returns ``errorType: "large_files"``).

        Args:
            message (str): Commit message. Required and non-empty.
            author (Optional[str]): Override the commit author (``Name <email>`` format).

        Returns:
            dict: ``{ success: bool, message: str, errorType?: str, largeFiles?: list }``.
        """
        commit_message = message.strip()
        if not commit_message:
            return {"success": False, "message": "Commit message cannot be empty"}

        large_files_info = self.check_large_files()
        if large_files_info["hasLargeFiles"]:
            return {
                "success": False,
                "message": "Cannot commit: some files are too large",
                "errorType": "large_files",
                "largeFiles": large_files_info["largeFiles"],
            }

        success, error_message = self.git_repository.commit_changes(
            commit_message, author
        )

        message = (
            f"Successfully committed changes: {commit_message}"
            if success
            else error_message or "Commit failed"
        )

        return {"success": success, "message": message}

    def add_to_gitignore(self, paths: List[str]) -> Dict[str, Any]:
        if not paths:
            return {"success": False, "message": "No paths provided"}

        success, error_message = self.git_repository.add_to_gitignore(paths)

        message = (
            f"Successfully added {len(paths)} file(s) to .gitignore"
            if success
            else error_message or "Failed to update .gitignore"
        )

        return {"success": success, "message": message}

    def stash_changes(self, message: str = "WIP") -> Dict[str, Any]:
        success, error_message = self.git_repository.stash_changes(message)

        message = (
            "Successfully stashed changes"
            if success
            else error_message or "Stash failed"
        )

        return {"success": success, "message": message}

    def get_commit_history(
        self, limit: int = 10, offset: int = 0, branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List recent commits on the current (or named) branch.

        Args:
            limit (int): Maximum number of commits to return.
            offset (int): Skip the most recent ``offset`` commits.
            branch (Optional[str]): Branch to read history from. Omit for current.

        Returns:
            dict: ``{ commits: [{ hash, message, author, date }], hasMore: bool }``.
        """
        commits = self.git_repository.get_commit_history(
            limit=limit, offset=offset, branch=branch
        )

        return {
            "commits": [self._format_commit(commit) for commit in commits],
            "hasMore": len(commits) == limit,
        }

    def _get_project_id(self) -> Optional[str]:
        try:
            headers = resolve_headers()
            if headers:
                api_key_info = get_api_key_info(headers)
                if api_key_info.get("logged"):
                    return api_key_info.get("info", {}).get("projectId")
        except Exception:
            pass
        return None

    def push_and_deploy(
        self, branch: str = "main", show_start_message: bool = True
    ) -> Dict[str, Any]:
        if show_start_message:
            DeployMessages.start(method="git")

        DeployMessages.authenticating()
        self._ensure_authentication()

        DeployMessages.pushing(branch)
        success, error_message = self.git_repository.push_and_deploy(branch)

        if not success and error_message:
            # These indicators signal that the push was rejected or interrupted
            # below the application layer (transport error, server-side body
            # rejection, mid-stream disconnect). They DO NOT prove the cause is
            # large files: a flaky network or a server 5xx unrelated to size
            # produces the same stderr.
            transport_error_indicators = [
                "curl 18",
                "curl 22",
                "HTTP 413",
                "HTTP 500",
                "transfer closed with outstanding read data remaining",
                "unexpected disconnect while reading sideband packet",
                "the remote end hung up unexpectedly",
                "RPC failed",
            ]

            is_transport_error = any(
                indicator.lower() in error_message.lower()
                for indicator in transport_error_indicators
            )

            if is_transport_error:
                large_files_info = self.check_large_files()
                if large_files_info["hasLargeFiles"]:
                    # Working tree has files over the per-file threshold; we
                    # can confidently point at them.
                    user_message = "Push failed: your project contains files that are too large to upload. Please add them to .gitignore and try again."
                    DeployMessages.error(user_message)
                    return {
                        "success": False,
                        "message": user_message,
                        "errorType": "large_files_push",
                        "largeFiles": large_files_info.get("largeFiles", []),
                        "details": error_message,
                    }
                # No large files found in the working tree. The cause could be
                # an oversized blob in history, cumulative pack size, or a
                # transport-level failure (proxy, VPN, server 5xx). Be honest
                # about the uncertainty and surface the raw git stderr.
                user_message = (
                    "Push failed: the server rejected or interrupted the upload. "
                    "This can happen when the project contains large files in its history, "
                    "or when the network drops the connection mid-upload. "
                    "See the raw error below for more detail. "
                    "If the problem persists, please contact us through the in-app Smart Chat."
                )
                DeployMessages.error(user_message)
                return {
                    "success": False,
                    "message": user_message,
                    "errorType": "push_transport_error",
                    "largeFiles": [],
                    "details": error_message,
                }

        if success:
            project_id = self._get_project_id()
            DeployMessages.success(project_id)
            message = f"Successfully deployed branch '{branch}' to Abstra"
        else:
            DeployMessages.error(error_message or "Unknown error")
            message = error_message

        return {"success": success, "message": message}

    def get_remotes(self) -> Dict[str, Any]:
        remotes = self.git_repository.get_remotes()

        return {"remotes": remotes, "hasAbstraRemote": REMOTE_NAME in remotes}

    def revert_commit(self, commit_hash: str) -> Dict[str, Any]:
        if not commit_hash.strip():
            return {"success": False, "message": "Commit hash is required"}

        commits = self.git_repository.get_commit_history(limit=200)
        commit_to_revert = next(
            (c for c in commits if c.hash.startswith(commit_hash)), None
        )

        if not commit_to_revert:
            return {"success": False, "message": f"Commit {commit_hash[:8]} not found"}

        try:
            success, error_message = self.git_repository.revert_commit(commit_hash)

            message = (
                f"Successfully restored content from commit: {commit_to_revert.message}. A new commit was created with the content from that version."
                if success
                else error_message
            )

            return {"success": success, "message": message}

        except Exception as e:
            return {
                "success": False,
                "message": f"Error restoring content from commit {commit_hash[:8]}: {str(e)}",
            }

    def _format_commit(self, commit: GitCommit) -> Dict[str, str]:
        return {
            "hash": commit.hash,
            "message": commit.message,
            "author": commit.author,
            "date": commit.date,
        }
