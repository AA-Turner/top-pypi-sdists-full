"""Tests for fetch_pr_details_node()."""

from __future__ import annotations

import json
import os
import subprocess
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.orchestration.review.nodes.fetch_pr_details import fetch_pr_details_node


class TestFetchPrDetailsNode:
    """Tests for the fetch_pr_details node."""

    def test_missing_pr_id_returns_error(self) -> None:
        """Returns an error when pr_id is missing."""
        result = fetch_pr_details_node({})
        assert any("pr_id is required" in error for error in result["errors"])

    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_config_load_failure_returns_error(self, mock_from_state) -> None:
        """Returns error when ADO config cannot be loaded."""
        mock_from_state.side_effect = RuntimeError("no config")
        result = fetch_pr_details_node({"pr_id": 123})
        assert any("failed to load ADO config" in error for error in result["errors"])

    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_auth_failure_returns_error(self, mock_from_state, mock_get_pat) -> None:
        """Authentication failures are surfaced as node errors."""
        mock_from_state.return_value = MagicMock(project="MyProject", organization="https://dev.azure.com/org")
        mock_get_pat.side_effect = RuntimeError("bad pat")

        result = fetch_pr_details_node({"pr_id": 123})

        assert any("authentication failed" in error for error in result["errors"])

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_returns_error_when_pr_lookup_fails(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """A falsey PR payload is treated as a fetch failure."""
        mock_from_state.return_value = MagicMock(project="MyProject", organization="https://dev.azure.com/org")
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = None

        result = fetch_pr_details_node({"pr_id": 123})

        assert any("failed to fetch PR #123" in error for error in result["errors"])

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_warns_when_commit_hash_is_missing(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """A warning is emitted when lastMergeSourceCommit.commitId is absent."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
            # lastMergeSourceCommit absent — commit hash will be blank
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["commit_hash"] == ""
        assert "commitId is missing or blank" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_non_dict_last_merge_target_commit_yields_empty_base_hash(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """When lastMergeTargetCommit is not a dict, base_commit_hash is empty."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "lastMergeTargetCommit": "not-a-dict",
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["base_commit_hash"] == ""

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_non_dict_last_merge_target_commit_does_not_raise_in_diff_path(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Non-dict lastMergeTargetCommit must not raise AttributeError in diff enrichment."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 456,
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/x",
            "lastMergeSourceCommit": {"commitId": "src111"},
            # Non-dict value — the diff-enrichment path must reuse the
            # pre-validated base_commit_hash string rather than calling
            # .get() on this value again.
            "lastMergeTargetCommit": "not-a-dict",
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {"item": {"path": "/src/app.py", "isFolder": False}, "changeType": "edit"},
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", side_effect=RuntimeError("no git")),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            # Must complete without AttributeError
            result = fetch_pr_details_node({"pr_id": 456})

        assert result["base_commit_hash"] == ""

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_successful_fetch(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Successfully fetches PR details and populates state."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config

        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}

        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "MyProject"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[{"id": 1, "status": "active"}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {
                        "item": {"path": "/src/main.py", "isFolder": False},
                        "changeType": "edit",
                    },
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                return_value=SimpleNamespace(
                    added=SimpleNamespace(
                        is_binary=False,
                        lines=[SimpleNamespace(line_number=2, content="new")],
                    ),
                    removed=SimpleNamespace(lines=[SimpleNamespace(line_number=1, content="old")]),
                ),
            ),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_patch",
                return_value="@@ -1 +1 @@\n-old\n+new",
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["commit_hash"] == "abc123def456"
        assert result["latest_iteration_id"] == 1
        assert result["repo_id"] == "repo-guid"
        assert result["project"] == "MyProject"
        assert result["files"] == [
            {
                "path": "/src/main.py",
                "changeType": "edit",
                "item": {"path": "/src/main.py", "isFolder": False},
                "isBinary": False,
                "addedLines": [{"line": 2, "content": "new"}],
                "removedLines": [{"line": 1, "content": "old"}],
                "patch": "@@ -1 +1 @@\n-old\n+new",
            }
        ]
        assert result["threads"] == [{"id": 1, "status": "active"}]

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_preserves_original_path_for_renames(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Rename changes preserve originalPath for downstream base-side retrieval."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "MyProject"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {
                        "item": {"path": "/src/new_name.py", "isFolder": False},
                        "changeType": "rename",
                        "originalPath": "/src/old_name.py",
                    },
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                return_value=SimpleNamespace(
                    added=SimpleNamespace(is_binary=False, lines=[]),
                    removed=SimpleNamespace(lines=[]),
                ),
            ),
            patch("agentic_devtools.cli.git.diff.get_diff_patch", return_value=""),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["files"][0]["originalPath"] == "/src/old_name.py"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_diff_enrichment_setup_failures_fall_back_to_basic_file_entry(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Setup-time diff enrichment failures keep the basic file entry intact."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {
                        "item": {"path": "/src/main.py", "isFolder": False},
                        "changeType": "edit",
                    },
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", side_effect=RuntimeError("git boom")),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["files"] == [
            {
                "path": "/src/main.py",
                "changeType": "edit",
                "item": {"path": "/src/main.py", "isFolder": False},
            }
        ]

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_writes_temp_file_and_handles_empty_threads_and_iterations(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        tmp_path,
    ) -> None:
        """Empty thread/iteration lists are accepted and PR details are persisted."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        pr_data = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }
        mock_fetch_pr.return_value = pr_data

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", side_effect=RuntimeError("bad config")),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        output_path = tmp_path / "temp-langchain-pr-details-123.json"
        assert output_path.exists()
        persisted = json.loads(output_path.read_text(encoding="utf-8"))
        assert persisted["pr_data"]["pullRequestId"] == 123
        assert "files" in persisted
        assert "threads" in persisted
        assert "iterations" in persisted
        assert "jira_issue_key" in persisted
        assert "jira_issue" in persisted
        assert result["threads"] == []
        assert result["files"] == []
        assert result["config"] == {}
        assert result["latest_iteration_id"] == 0

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_uses_encoded_project_for_ado_rest_helpers(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Project names are percent-encoded before calling naive REST helpers."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="My Project/#1",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "My Project/#1"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ) as mock_threads,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ) as mock_iterations,
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            fetch_pr_details_node({"pr_id": 123})

        assert mock_fetch_pr.call_args.args[1].project == "My%20Project%2F%231"
        assert mock_threads.call_args.args[1] == "My%20Project%2F%231"
        assert mock_iterations.call_args.args[1] == "My%20Project%2F%231"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_encodes_project_on_non_dataclass_config_objects(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Non-dataclass config objects still get an encoded project for helper calls."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "My Project/#1"
        mock_config.repository = "repo"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "My Project/#1"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            fetch_pr_details_node({"pr_id": 123})

        assert mock_fetch_pr.call_args.args[1] is not mock_config
        assert mock_fetch_pr.call_args.args[1].project == "My%20Project%2F%231"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_decodes_fallback_project_when_pr_payload_omits_project_name(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Fallback config project is decoded before storing it in graph state."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="My%20Project",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {"id": "repo-guid"},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["project"] == "My Project"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_reports_repo_id_and_empty_iterations_errors_when_pr_payload_omits_repository_id(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        tmp_path,
    ) -> None:
        """Reports both missing repository.id and empty-iterations errors."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="MyProject",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {"project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["errors"] == [
            "fetch_pr_details: repository id is missing from PR payload",
            "fetch_pr_details: no changed files were retrieved from the iterations API",
        ]

    @patch("agentic_devtools.cli.azure_devops.helpers.find_jira_issue_from_pr")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_prefers_jira_issue_key_from_graph_state(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        mock_find_jira,
    ) -> None:
        """Graph-provided Jira issue keys are propagated without extra lookup."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="MyProject",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "MyProject"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "jira_issue_key": "PROJECT-1234"})

        assert result["jira_issue_key"] == "PROJECT-1234"
        mock_find_jira.assert_not_called()

    @patch("agentic_devtools.state.get_value", return_value=" PROJECT-5678 ")
    @patch("agentic_devtools.cli.azure_devops.helpers.find_jira_issue_from_pr")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_uses_state_jira_issue_key_when_graph_key_is_blank(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        mock_find_jira,
        mock_get_value,
    ) -> None:
        """Blank graph Jira keys fall back to jira.issue_key from state."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="MyProject",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "MyProject"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "jira_issue_key": "   "})

        assert result["jira_issue_key"] == "PROJECT-5678"
        mock_find_jira.assert_not_called()
        assert ("jira.issue_key",) in [c.args for c in mock_get_value.call_args_list]

    @patch("agentic_devtools.state.get_value", return_value="   ")
    @patch("agentic_devtools.cli.azure_devops.helpers.find_jira_issue_from_pr", return_value="PROJECT-9999")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_uses_pr_lookup_when_graph_and_state_issue_keys_are_blank(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        mock_find_jira,
        mock_get_value,
    ) -> None:
        """Falls back to PR-based issue lookup when no usable key is already present."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="MyProject",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "MyProject"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "jira_issue_key": "   "})

        assert result["jira_issue_key"] == "PROJECT-9999"
        mock_find_jira.assert_called_once()
        assert ("jira.issue_key",) in [c.args for c in mock_get_value.call_args_list]

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_loads_repo_config_from_repo_root_when_env_missing(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Repo config resolution falls back to the git repo root, not cwd."""
        mock_from_state.return_value = MagicMock(project="MyProject", organization="https://dev.azure.com/org")
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value="/resolved/repo-root",
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}) as mock_load_config,
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            fetch_pr_details_node({"pr_id": 123})

        mock_load_config.assert_called_once_with("/resolved/repo-root")

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_per_file_diff_enrichment_failures_are_non_fatal(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Per-file diff failures do not prevent the file from being reviewed."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {
                        "item": {"path": "/src/main.py", "isFolder": False},
                        "changeType": "edit",
                    },
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                side_effect=RuntimeError("diff boom"),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["files"] == [
            {
                "path": "/src/main.py",
                "changeType": "edit",
                "item": {"path": "/src/main.py", "isFolder": False},
                "patch": None,
                "isBinary": False,
                "addedLines": [],
                "removedLines": [],
            }
        ]

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_per_file_diff_enrichment_failure_logs_warning(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Unexpected diff errors emit a prefixed warning containing the file path."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {
                        "item": {"path": "/src/main.py", "isFolder": False},
                        "changeType": "edit",
                    },
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                side_effect=RuntimeError("diff boom"),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        # File must still be present (non-fatal)
        assert len(result["files"]) == 1
        err = capsys.readouterr().err
        assert "Warning: fetch_pr_details: diff enrichment failed for /src/main.py" in err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_thread_lookup_warning_is_non_fatal(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Thread lookup failures are logged but do not abort the node."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                side_effect=RuntimeError("thread boom"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["threads"] == []
        assert "Warning: fetch_pr_details: failed to fetch threads" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_ignores_folder_and_missing_path_changes(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Folder entries and changes without paths are excluded from file reviews."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 2}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {"item": {"path": "/src/folder", "isFolder": True}, "changeType": "edit"},
                    {"item": {}, "changeType": "edit"},
                ],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["files"] == []

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_empty_iteration_changes_are_accepted(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """An empty iteration change list yields no files without error."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 2}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["files"] == []

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_iteration_change_warning_is_non_fatal(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Iteration change lookup failures are logged and skipped."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 2}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                side_effect=RuntimeError("changes boom"),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["files"] == []
        assert "Warning: fetch_pr_details: failed to fetch iteration changes" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_strips_leading_slash_from_path_when_calling_git_diff(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """git diff helpers receive repo-root-relative paths (no leading slash)."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "lastMergeTargetCommit": {"commitId": "base000"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        mock_diff_lines = MagicMock(
            return_value=SimpleNamespace(
                added=SimpleNamespace(is_binary=False, lines=[]),
                removed=SimpleNamespace(lines=[]),
            )
        )
        mock_diff_patch = MagicMock(return_value="@@ -1 +1 @@\n-old\n+new")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {
                        "item": {"path": "/src/main.py", "isFolder": False},
                        "changeType": "edit",
                    },
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch("agentic_devtools.cli.git.diff.get_diff_lines_info", mock_diff_lines),
            patch("agentic_devtools.cli.git.diff.get_diff_patch", mock_diff_patch),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            fetch_pr_details_node({"pr_id": 123})

        # git diff must receive the path WITHOUT the leading slash
        diff_lines_path = mock_diff_lines.call_args.args[2]
        diff_patch_path = mock_diff_patch.call_args.args[2]
        assert diff_lines_path == "src/main.py", f"Expected 'src/main.py', got {diff_lines_path!r}"
        assert diff_patch_path == "src/main.py", f"Expected 'src/main.py', got {diff_patch_path!r}"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_iterations_metadata_populated_from_api_response(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Full iteration history is extracted as lightweight metadata."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        iterations_data = [
            {
                "id": 1,
                "description": "Initial push",
                "sourceRefCommit": {"commitId": "aaa"},
                "targetRefCommit": {"commitId": "bbb"},
                "createdDate": "2024-01-01T00:00:00Z",
                "reason": "push",
                "extraField": "should-be-ignored",
            },
            {
                "id": 2,
                "description": "Fix review feedback",
                "sourceRefCommit": {"commitId": "ccc"},
                "targetRefCommit": {"commitId": "ddd"},
                "createdDate": "2024-01-02T00:00:00Z",
                "reason": "push",
            },
        ]

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=iterations_data,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert len(result["iterations"]) == 2
        first = result["iterations"][0]
        assert set(first.keys()) == {"id", "description", "sourceRefCommit", "targetRefCommit", "createdDate", "reason"}
        assert first["id"] == 1
        assert first["description"] == "Initial push"
        assert first["reason"] == "push"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_iterations_empty_when_api_returns_none(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Iterations is empty list when API returns None."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=None,
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["iterations"] == []

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_iterations_empty_when_fetch_fails(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Iteration fetch failure yields empty list and warning."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                side_effect=RuntimeError("iteration boom"),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["iterations"] == []
        assert "Warning: fetch_pr_details:" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_iterations_metadata_skips_non_dict_entries(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Non-dict entries (e.g. None placeholders) in iterations list are ignored."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                # Mix of valid dict and malformed None/string entries
                return_value=[
                    {"id": 1, "description": "Initial push", "reason": "push"},
                    None,
                    "unexpected-string",
                    {"id": 2, "description": "Fix feedback", "reason": "push"},
                ],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        # Only the two dict entries should appear in iteration_metadata
        assert len(result["iterations"]) == 2
        assert result["iterations"][0]["id"] == 1
        assert result["iterations"][1]["id"] == 2

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_non_dict_latest_iteration_still_uses_latest_dict_iteration(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """A non-dict last iteration does not break latest iteration resolution."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 7}, None],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[{"item": {"path": "/src/main.py", "isFolder": False}, "changeType": "edit"}],
            ) as mock_get_iteration_changes,
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["latest_iteration_id"] == 7
        assert len(result["files"]) == 1
        assert mock_get_iteration_changes.call_args.args[4] == 7

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_per_file_diff_timeout_logs_warning_and_sets_null_patch(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Diff timeout produces patch=None and a warning."""

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {"item": {"path": "/src/slow.py", "isFolder": False}, "changeType": "edit"},
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                side_effect=subprocess.TimeoutExpired(cmd="git diff", timeout=10),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert len(result["files"]) == 1
        file_entry = result["files"][0]
        assert file_entry["patch"] is None
        assert file_entry["isBinary"] is False
        assert file_entry["addedLines"] == []
        assert file_entry["removedLines"] == []
        err = capsys.readouterr().err
        assert "Warning: fetch_pr_details: diff computation timed out" in err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_patch_timeout_keeps_precomputed_diff_info(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Timeout in patch fetch keeps line-level diff metadata on the file entry."""

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[{"item": {"path": "/src/main.py", "isFolder": False}, "changeType": "edit"}],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                return_value=SimpleNamespace(
                    added=SimpleNamespace(
                        is_binary=False,
                        lines=[SimpleNamespace(line_number=10, content="+new line")],
                    ),
                    removed=SimpleNamespace(lines=[SimpleNamespace(line_number=4, content="-old line")]),
                ),
            ),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_patch",
                side_effect=subprocess.TimeoutExpired(cmd="git diff", timeout=10),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert len(result["files"]) == 1
        file_entry = result["files"][0]
        assert file_entry["isBinary"] is False
        assert file_entry["patch"] is None
        assert file_entry["addedLines"] == [{"line": 10, "content": "+new line"}]
        assert file_entry["removedLines"] == [{"line": 4, "content": "-old line"}]
        assert "Warning: fetch_pr_details: diff computation timed out" in capsys.readouterr().err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_patch_failure_logs_warning_and_keeps_precomputed_diff_info(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Unexpected patch errors keep line metadata and emit a prefixed warning."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[{"item": {"path": "/src/main.py", "isFolder": False}, "changeType": "edit"}],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                return_value=SimpleNamespace(
                    added=SimpleNamespace(
                        is_binary=False,
                        lines=[SimpleNamespace(line_number=10, content="+new line")],
                    ),
                    removed=SimpleNamespace(lines=[SimpleNamespace(line_number=4, content="-old line")]),
                ),
            ),
            patch("agentic_devtools.cli.git.diff.get_diff_patch", side_effect=RuntimeError("patch boom")),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert len(result["files"]) == 1
        file_entry = result["files"][0]
        assert file_entry["isBinary"] is False
        assert file_entry["patch"] is None
        assert file_entry["addedLines"] == [{"line": 10, "content": "+new line"}]
        assert file_entry["removedLines"] == [{"line": 4, "content": "-old line"}]
        assert (
            "Warning: fetch_pr_details: diff enrichment failed for /src/main.py: patch boom" in capsys.readouterr().err
        )

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_diff_timeout_does_not_block_remaining_files(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """A timeout on the first file does not prevent the second from succeeding."""

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        def diff_lines_side_effect(base, compare, path, **kwargs):
            if "slow" in path:
                raise subprocess.TimeoutExpired(cmd="git diff", timeout=10)
            return SimpleNamespace(
                added=SimpleNamespace(is_binary=False, lines=[]),
                removed=SimpleNamespace(lines=[]),
            )

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {"item": {"path": "/src/slow.py", "isFolder": False}, "changeType": "edit"},
                    {"item": {"path": "/src/fast.py", "isFolder": False}, "changeType": "edit"},
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch("agentic_devtools.cli.git.diff.get_diff_lines_info", side_effect=diff_lines_side_effect),
            patch("agentic_devtools.cli.git.diff.get_diff_patch", return_value="@@ patch @@"),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert len(result["files"]) == 2
        slow_file = next(f for f in result["files"] if "slow" in f["path"])
        fast_file = next(f for f in result["files"] if "fast" in f["path"])
        assert slow_file["patch"] is None
        assert fast_file["patch"] == "@@ patch @@"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_jira_issue_fetched_and_normalized_on_success(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Jira issue is fetched and normalized when key is available."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        jira_response = {
            "issue": {
                "key": "PROJ-42",
                "fields": {
                    "summary": "Add feature",
                    "description": "Details",
                    "status": {"name": "In Progress"},
                    "issuetype": {"name": "Story"},
                    "priority": {"name": "Medium"},
                    "labels": ["backend"],
                    "customfield_10014": "User can do X",
                },
            }
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira.example.com"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={"Authorization": "Basic x"}),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value=jira_response),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "jira_issue_key": "PROJ-42"})

        assert result["jira_issue"] is not None
        assert result["jira_issue"]["key"] == "PROJ-42"
        assert result["jira_issue"]["summary"] == "Add feature"
        assert result["jira_issue"]["acceptance_criteria"] == "User can do X"
        assert set(result["jira_issue"].keys()) == {
            "key",
            "summary",
            "description",
            "status",
            "issue_type",
            "labels",
            "acceptance_criteria",
            "priority",
        }

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_jira_issue_none_when_no_key_resolved(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """jira_issue is None when no Jira key is found."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
            patch("agentic_devtools.state.get_value", return_value=None),
            patch("agentic_devtools.cli.azure_devops.helpers.find_jira_issue_from_pr", return_value=None),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["jira_issue"] is None

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_jira_issue_none_when_fetch_fails(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """jira_issue is None when Jira API fails, and warning is logged."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira.example.com"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={"Authorization": "Basic x"}),
            patch("agentic_devtools.tools.jira.fetch_issue_context", side_effect=RuntimeError("Jira down")),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "jira_issue_key": "PROJ-42"})

        assert result["jira_issue"] is None
        err = capsys.readouterr().err
        assert "Warning: fetch_pr_details: failed to fetch Jira issue" in err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_threads_include_all_statuses(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """All thread statuses (active, resolved, closed) are preserved."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        all_threads = [
            {"id": 1, "status": "active"},
            {"id": 2, "status": "closed"},
            {"id": 3, "status": "fixed"},
        ]

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=all_threads,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["threads"] == all_threads

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_persisted_artifact_contains_all_sections(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        tmp_path,
    ) -> None:
        """Persisted JSON artifact contains all required sections."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 456,
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[{"id": 1, "status": "active"}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1, "reason": "push"}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            fetch_pr_details_node({"pr_id": 456, "jira_issue_key": "PROJ-99"})

        output_path = tmp_path / "temp-langchain-pr-details-456.json"
        assert output_path.exists()
        persisted = json.loads(output_path.read_text(encoding="utf-8"))
        assert "pr_data" in persisted
        assert "files" in persisted
        assert "threads" in persisted
        assert "iterations" in persisted
        assert "jira_issue_key" in persisted
        assert "jira_issue" in persisted
        assert persisted["pr_data"]["pullRequestId"] == 456
        assert persisted["jira_issue_key"] == "PROJ-99"

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_persistence_failure_logs_warning_and_continues(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Artifact persistence failure is non-fatal and logs a warning."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=OSError("disk full")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        # Node still returns a valid result
        assert "files" in result
        assert "threads" in result
        err = capsys.readouterr().err
        assert "Warning: fetch_pr_details: failed to persist artifact" in err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_git_refs_unavailable_sets_patch_null_and_logs_warning(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        capsys,
    ) -> None:
        """Files are retained with no diff data when git ref sync fails."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {"item": {"path": "/src/a.py", "isFolder": False}, "changeType": "edit"},
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", side_effect=RuntimeError("no git")),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        # File is still in the list but without diff enrichment
        assert len(result["files"]) == 1
        assert "patch" not in result["files"][0]
        err = capsys.readouterr().err
        assert "Warning: fetch_pr_details: git ref sync failed" in err

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_binary_file_has_is_binary_true_and_null_patch(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """Binary files get isBinary=True and patch=None."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature/test",
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_iteration_changes",
                return_value=[
                    {"item": {"path": "/assets/logo.png", "isFolder": False}, "changeType": "add"},
                ],
            ),
            patch("agentic_devtools.cli.git.diff.sync_git_ref", return_value=True),
            patch(
                "agentic_devtools.cli.git.diff.get_diff_lines_info",
                return_value=SimpleNamespace(
                    added=SimpleNamespace(is_binary=True, lines=[]),
                    removed=SimpleNamespace(lines=[]),
                ),
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert len(result["files"]) == 1
        assert result["files"][0]["isBinary"] is True
        assert result["files"][0]["patch"] is None

    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_jira_issue_none_when_context_result_issue_is_not_dict(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
    ) -> None:
        """jira_issue stays None when context_result['issue'] is not a dict."""
        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_from_state.return_value = mock_config
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "lastMergeSourceCommit": {"commitId": "abc123"},
            "repository": {"id": "repo-guid", "project": {"name": "MyProject"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira.example.com"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={"Authorization": "Basic x"}),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": None}),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "jira_issue_key": "PROJ-42"})

        assert result["jira_issue"] is None

    @patch("agentic_devtools.state.get_value", return_value="   ")
    @patch("agentic_devtools.cli.azure_devops.helpers.find_jira_issue_from_pr")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_pull_request_details")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_emits_warning_when_jira_auto_detect_raises(
        self,
        mock_from_state,
        mock_get_pat,
        mock_get_auth,
        mock_fetch_pr,
        mock_find_jira,
        mock_get_value,
        capsys,
    ) -> None:
        """A warning is printed to stderr when find_jira_issue_from_pr raises."""
        mock_from_state.return_value = AzureDevOpsConfig(
            organization="https://dev.azure.com/org",
            project="MyProject",
            repository="repo",
        )
        mock_get_pat.return_value = "fake-pat"
        mock_get_auth.return_value = {"Authorization": "Basic fake"}
        mock_fetch_pr.return_value = {
            "pullRequestId": 123,
            "lastMergeSourceCommit": {"commitId": "abc123def456"},
            "repository": {
                "id": "repo-guid",
                "project": {"name": "MyProject"},
            },
        }
        mock_find_jira.side_effect = RuntimeError("network error")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", side_effect=Exception("no state dir")),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["jira_issue_key"] == ""
        captured = capsys.readouterr()
        assert "Warning: fetch_pr_details: Jira key auto-detection failed: network error" in captured.err
