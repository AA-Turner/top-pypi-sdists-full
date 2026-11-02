"""Tests for provider-neutral fetch_pr_details_node()."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.review.nodes.fetch_pr_details import fetch_pr_details_node


@pytest.fixture
def normalized_payload() -> dict:
    return {
        "pullRequest": {
            "lastMergeSourceCommit": {"commitId": "head-sha"},
            "lastMergeTargetCommit": {"commitId": "base-sha"},
        },
        "repository": {"id": "repo-id", "project": {"name": "project"}},
        "files": [{"path": "src/app.py", "changeType": "edit"}],
        "threads": [{"id": "thread-1", "comments": []}],
        "iterations": [{"id": 1}, {"id": True}, {"id": 3}, {"id": "4"}],
    }


class TestFetchPrDetailsNode:
    """Tests for the review-graph PR details node."""

    @pytest.fixture(autouse=True)
    def isolate_state(self, monkeypatch) -> None:
        monkeypatch.setattr("agentic_devtools.state.load_state_locked", lambda: {})

    @pytest.mark.parametrize("state", [{}, {"pr_id": ""}])
    def test_missing_pr_id_returns_error(self, state) -> None:
        result = fetch_pr_details_node(state)
        assert result["errors"][0].startswith("fetch_pr_details: pr_id is required")

    @pytest.mark.parametrize("pr_id", [True, 1.5, 0, -1, "1.5", "0", "-1", {}, []])
    def test_invalid_pr_id_returns_error_without_fetching_details(self, pr_id) -> None:
        with patch("agentic_devtools.cli.pull_request_details.get_pull_request_details") as get_details:
            result = fetch_pr_details_node({"pr_id": pr_id, "provider": "github"})

        assert result == {"errors": [f"fetch_pr_details: pr_id must be a positive integer but was {pr_id!r}"]}
        get_details.assert_not_called()

    def test_missing_provider_context_fails_without_using_checkout_origin(self) -> None:
        with patch("agentic_devtools.cli.pull_request_details.get_pull_request_details") as get_details:
            result = fetch_pr_details_node({"pr_id": 123})

        assert result == {
            "errors": [
                "fetch_pr_details: provider configuration is missing or unsupported; "
                "set platform.code_hosting or provider"
            ]
        }
        get_details.assert_not_called()

    def test_state_load_failure_does_not_infer_provider(self) -> None:
        with (
            patch("agentic_devtools.state.load_state_locked", side_effect=OSError("state unavailable")),
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details") as get_details,
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        assert result["errors"][0].startswith("fetch_pr_details: provider configuration is missing")
        get_details.assert_not_called()

    @pytest.mark.parametrize("provider", ["github", "azure_devops"])
    @pytest.mark.parametrize("pr_id", [123, "123"])
    def test_fetches_and_maps_normalized_details_for_each_provider(
        self, provider, pr_id, normalized_payload, tmp_path
    ) -> None:
        state = {
            "pr_id": pr_id,
            "provider": provider,
            "organization": "https://dev.azure.com/org",
            "jira_issue_key": "PROJECT-123",
        }
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=normalized_payload,
            ) as get_details,
            patch("agentic_devtools.config.load_repo_config", return_value={"review": {"enabled": True}}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": None}),
        ):
            result = fetch_pr_details_node(state)

        get_details.assert_called_once_with(
            provider=provider,
            pull_request_id=123,
            repository=None,
            state=state,
        )
        assert result["files"] == normalized_payload["files"]
        assert result["threads"] == normalized_payload["threads"]
        assert result["commit_hash"] == "head-sha"
        assert result["base_commit_hash"] == "base-sha"
        assert result["latest_iteration_id"] == 3
        assert result["iterations"] == normalized_payload["iterations"]
        assert result["repo_id"] == "repo-id"
        assert result["project"] == "project"
        assert result["organization"] == ("https://dev.azure.com/org" if provider == "azure_devops" else "")
        artifact = json.loads((tmp_path / "temp-langchain-pr-details-123.json").read_text(encoding="utf-8"))
        assert artifact["files"] == normalized_payload["files"]
        assert artifact["threads"] == normalized_payload["threads"]

    def test_uses_provider_from_persisted_state(self, normalized_payload, tmp_path) -> None:
        persisted_state = {"platform": {"code_hosting": "github"}, "github": {"repo": "owner/repo"}}
        merged_state = {**persisted_state, "pr_id": 123}
        with (
            patch("agentic_devtools.state.load_state_locked", return_value=persisted_state),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=normalized_payload,
            ) as get_details,
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123})

        get_details.assert_called_once_with(
            provider="github",
            pull_request_id=123,
            repository=None,
            state=merged_state,
        )
        assert result["repo_id"] == "repo-id"

    def test_uses_provider_from_platform_state(self, normalized_payload, tmp_path) -> None:
        state = {"pr_id": 123, "platform": {"code_hosting": "github"}}
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=normalized_payload,
            ) as get_details,
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node(state)

        get_details.assert_called_once_with(
            provider="github",
            pull_request_id=123,
            repository=None,
            state=state,
        )
        assert result["repo_id"] == "repo-id"

    def test_merges_persisted_azure_config_beneath_configured_graph_provider(
        self, normalized_payload, tmp_path
    ) -> None:
        persisted_state = {
            "platform": {"code_hosting": "github"},
            "azure_devops": {
                "organization": "https://dev.azure.com/persisted-org",
                "project": "Persisted Project",
            },
        }
        graph_state = {
            "pr_id": 123,
            "provider": "azure_devops",
            "platform": {"code_hosting": "azure_devops"},
        }
        with (
            patch("agentic_devtools.state.load_state_locked", return_value=persisted_state),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=normalized_payload,
            ) as get_details,
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node(graph_state)

        get_details.assert_called_once_with(
            provider="azure_devops",
            pull_request_id=123,
            repository=None,
            state={
                **graph_state,
                "platform": {"code_hosting": "azure_devops"},
                "azure_devops": persisted_state["azure_devops"],
            },
        )
        assert result["organization"] == "https://dev.azure.com/persisted-org"

    def test_state_load_failure_still_uses_graph_provider(self, normalized_payload, tmp_path) -> None:
        state = {"pr_id": 123, "provider": "azure_devops"}
        with (
            patch("agentic_devtools.state.load_state_locked", side_effect=OSError("unavailable")),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=normalized_payload,
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node(state)

        assert result["repo_id"] == "repo-id"

    @pytest.mark.parametrize(
        ("failure", "expected_category"),
        [
            (SystemExit("token missing: private-value"), "credentials"),
            (RuntimeError("HTTP 403 forbidden"), "authorization"),
            (RuntimeError("HTTP 404 not found"), "not found"),
            (RuntimeError("HTTP 429 rate limit"), "rate limited"),
            (subprocess.TimeoutExpired("gh", 1), "timed out"),
            (RuntimeError("malformed response"), "malformed pull-request details"),
        ],
    )
    def test_provider_failures_return_sanitized_categories(self, failure, expected_category) -> None:
        with patch(
            "agentic_devtools.cli.pull_request_details.get_pull_request_details",
            side_effect=failure,
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert expected_category in result["errors"][0]
        assert "private-value" not in result["errors"][0]

    @pytest.mark.parametrize("payload", [None, []])
    def test_rejects_non_mapping_normalized_payload(self, payload) -> None:
        with patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result == {"errors": ["fetch_pr_details: provider returned malformed pull-request details; retry"]}

    def test_normalizes_malformed_payload_sections_and_reports_missing_data(self, tmp_path) -> None:
        payload = {
            "pullRequest": None,
            "repository": None,
            "files": {},
            "threads": {},
            "iterations": {"status": "unsupported", "items": []},
        }
        with (
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result["files"] == []
        assert result["threads"] == []
        assert result["iterations"] == []
        assert result["errors"] == [
            "fetch_pr_details: repository id is missing from PR payload",
            "fetch_pr_details: no changed files were retrieved",
        ]

    def test_malformed_repository_and_commit_fields_are_ignored(self, tmp_path) -> None:
        payload = {
            "pullRequest": {"lastMergeSourceCommit": None, "lastMergeTargetCommit": []},
            "repository": {"id": 42, "project": []},
            "files": [{"path": "src/app.py"}],
            "threads": [],
            "iterations": [{"id": True}, {"id": "7"}],
        }
        with (
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result["commit_hash"] == ""
        assert result["base_commit_hash"] == ""
        assert result["latest_iteration_id"] == 0
        assert result["repo_id"] == ""
        assert result["project"] == ""

    def test_normalizes_whitespace_commit_ids_to_empty_strings(self, tmp_path) -> None:
        payload = {
            "pullRequest": {
                "lastMergeSourceCommit": {"commitId": "  \t"},
                "lastMergeTargetCommit": {"commitId": "\n "},
            },
            "repository": {"id": "repo-id"},
            "files": [{"path": "src/app.py"}],
        }
        with (
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result["commit_hash"] == ""
        assert result["base_commit_hash"] == ""

    def test_defaults_invalid_iterations_shape_to_empty(self, normalized_payload, tmp_path) -> None:
        payload = {**normalized_payload, "iterations": None}
        with (
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result["iterations"] == []
        assert result["latest_iteration_id"] == 0

    def test_reports_repo_config_and_artifact_failures_without_losing_details(self, normalized_payload, capsys) -> None:
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=normalized_payload
            ),
            patch("agentic_devtools.config.load_repo_config", side_effect=RuntimeError("config unavailable")),
            patch("agentic_devtools.state.get_state_dir", side_effect=OSError("state unavailable")),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result["repo_id"] == "repo-id"
        assert result["errors"] == [
            "fetch_pr_details: failed to persist PR details artifact: state unavailable",
        ]
        assert "Warning: fetch_pr_details: failed to load repo config" in capsys.readouterr().err

    def test_uses_jira_issue_key_from_graph_state_and_normalizes_issue(self, normalized_payload, tmp_path) -> None:
        issue = {"key": "PROJECT-123", "fields": {"summary": "Summary", "labels": ["bug"]}}
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=normalized_payload
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={}),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": issue}),
        ):
            result = fetch_pr_details_node(
                {"pr_id": 123, "provider": "azure_devops", "jira_issue_key": " PROJECT-123 "}
            )

        assert result["jira_issue_key"] == "PROJECT-123"
        assert result["jira_issue"] == {
            "key": "PROJECT-123",
            "summary": "Summary",
            "description": None,
            "status": None,
            "issue_type": None,
            "labels": ["bug"],
            "acceptance_criteria": None,
            "priority": None,
        }

    def test_reads_jira_key_from_state_and_ignores_invalid_issue_shape(self, normalized_payload, tmp_path) -> None:
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=normalized_payload
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_value", return_value=" PROJECT-456 "),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={}),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": None}),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github", "jira_issue_key": " "})

        assert result["jira_issue_key"] == "PROJECT-456"
        assert result["jira_issue"] is None

    @pytest.mark.parametrize(
        ("issue_key", "expected_key"),
        [(42, "PROJECT-456"), ("#42", "PROJECT-456"), ("PROJECT-123", "PROJECT-123")],
    )
    def test_validates_top_level_issue_key_before_using_it(
        self, issue_key, expected_key, normalized_payload, tmp_path
    ) -> None:
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=normalized_payload
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_value", return_value="PROJECT-456"),
            patch("agentic_devtools.cli.jira.config.get_jira_project_keys", return_value=["PROJECT"]),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={}),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": None}) as fetch_issue,
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github", "issue_key": issue_key})

        assert result["jira_issue_key"] == expected_key
        fetch_issue.assert_called_once()
        assert fetch_issue.call_args.args[1] == expected_key

    def test_uses_jira_state_key_when_top_level_key_cannot_be_validated(self, normalized_payload, tmp_path) -> None:
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=normalized_payload
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_value", return_value="PROJECT-456"),
            patch(
                "agentic_devtools.cli.jira.config.get_jira_project_keys",
                side_effect=RuntimeError("Jira configuration unavailable"),
            ),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={}),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": None}) as fetch_issue,
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github", "issue_key": "#42"})

        assert result["jira_issue_key"] == "PROJECT-456"
        fetch_issue.assert_called_once()
        assert fetch_issue.call_args.args[1] == "PROJECT-456"

    def test_auto_detects_jira_key_from_normalized_source_ref(self, normalized_payload, tmp_path) -> None:
        payload = {
            **normalized_payload,
            "pullRequest": {
                "sourceRefName": "refs/heads/PROJECT-123/feature",
                "title": "PROJECT-456 title",
                "description": "PROJECT-789 description",
            },
        }
        with (
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_value", return_value=None),
            patch("agentic_devtools.cli.jira.config.get_jira_project_keys", return_value=["PROJECT"]),
            patch("agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira"),
            patch("agentic_devtools.cli.jira.config.get_jira_headers", return_value={}),
            patch("agentic_devtools.cli.jira.helpers._get_ssl_verify", return_value=True),
            patch("agentic_devtools.tools.jira.fetch_issue_context", return_value={"issue": None}),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "azure_devops", "issue_key": "#42"})

        assert result["jira_issue_key"] == "PROJECT-123"

    def test_keeps_jira_key_empty_when_normalized_metadata_has_no_match(self, normalized_payload, tmp_path) -> None:
        payload = {
            **normalized_payload,
            "pullRequest": {
                "sourceRefName": "refs/heads/feature",
                "title": "A regular pull request",
                "description": "No tracker key here.",
            },
        }
        with (
            patch("agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=payload),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_value", return_value=None),
            patch("agentic_devtools.cli.jira.config.get_jira_project_keys", return_value=[]),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "azure_devops"})

        assert result["jira_issue_key"] == ""
        assert result["jira_issue"] is None

    def test_ignores_state_lookup_failure_when_no_jira_key(self, normalized_payload, tmp_path) -> None:
        with (
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details", return_value=normalized_payload
            ),
            patch("agentic_devtools.config.load_repo_config", return_value={}),
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.state.get_value", side_effect=RuntimeError("no state")),
        ):
            result = fetch_pr_details_node({"pr_id": 123, "provider": "github"})

        assert result["jira_issue_key"] == ""
        assert result["jira_issue"] is None
