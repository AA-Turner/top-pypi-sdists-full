"""Tests for get_pull_request_details function."""

import io
import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.azure_devops import get_pull_request_details


class TestGetPullRequestDetails:
    """Tests for get_pull_request_details command."""

    def test_dry_run_output(self, temp_state_dir, clear_state_before, capsys):
        """Should show dry run output when dry_run is set."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "23046")
        set_value("dry_run", "true")

        get_pull_request_details()

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "23046" in captured.out
        assert "Organization" in captured.out
        assert "Project" in captured.out
        assert "Repository" in captured.out

    def test_dry_run_shows_output_path(self, temp_state_dir, clear_state_before, capsys):
        """Should show output file path in dry run."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "true")

        get_pull_request_details()

        captured = capsys.readouterr()
        assert "Output" in captured.out
        assert "temp-get-pull-request-details-response.json" in captured.out

    def test_request_snapshot_uses_captured_dry_run_and_output_path(self, tmp_path, capsys):
        """A queued request uses its captured dry-run value and scoped output path."""
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

        output_file = tmp_path / "request-specific.json"
        state = {
            "organization": "https://dev.azure.com/test-org",
            "project": "TestProject",
            "repository": "test-repo",
            "pull_request_id": 7,
            "dry_run": False,
        }
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.AzureDevOpsConfig.from_state",
                return_value=AzureDevOpsConfig(
                    organization="https://dev.azure.com/test-org",
                    project="TestProject",
                    repository="test-repo",
                ),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.load_state_locked",
                side_effect=AssertionError("snapshot requests must not reload state"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.is_dry_run",
                side_effect=AssertionError("snapshot dry-run value must take precedence"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
        ):
            get_pull_request_details(
                pull_request_id=7,
                repository="test-repo",
                state=state,
                output_file=output_file,
                dry_run=True,
                state_snapshot=True,
            )

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert str(output_file) in captured.out

    def test_missing_pull_request_id(self, temp_state_dir, clear_state_before, capsys):
        """Should raise KeyError if pull_request_id is not set."""
        from agentic_devtools.state import set_value

        set_value("dry_run", "true")  # Don't set pull_request_id

        with pytest.raises(KeyError, match="pull_request_id"):
            get_pull_request_details()

    def test_explicit_overrides_bypass_state_lookup(self, tmp_path):
        """Explicit PR and repository overrides should drive the Azure REST request."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 7, "title": "PR", "repository": {}},
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details(
                pull_request_id=7,
                repository="override-repo",
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "dry_run": False,
                },
            )
        assert fetch.call_args.args[0] == 7
        assert fetch.call_args.args[1].repository == "override-repo"

    @pytest.mark.parametrize(
        ("state", "expected_organization", "expected_project"),
        [
            (
                {
                    "azure_devops": {
                        "organization": "https://dev.azure.com/nested-org",
                        "project": "Nested Project",
                    }
                },
                "https://dev.azure.com/nested-org",
                "Nested Project",
            ),
            (
                {
                    "organization": "https://dev.azure.com/top-level",
                    "project": "Top-level Project",
                    "azure_devops": {
                        "organization": "https://dev.azure.com/nested-org",
                        "project": "Nested Project",
                    },
                },
                "https://dev.azure.com/top-level",
                "Top-level Project",
            ),
        ],
    )
    def test_state_azure_configuration_is_used_for_neutral_fetch(
        self, tmp_path, state, expected_organization, expected_project
    ):
        """Nested configuration is used unless top-level Azure values are present."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.load_state_locked",
                return_value={},
            ),
            patch("agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote") as remote,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 7, "title": "PR", "repository": {}},
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            remote.return_value = ("https://dev.azure.com/remote-org", "Remote Project", "remote-repo")
            get_pull_request_details(
                pull_request_id=7,
                repository="selected-repo",
                state=state,
            )

        config = fetch.call_args.args[1]
        assert config.organization == expected_organization
        assert config.project == expected_project
        assert config.repository == "selected-repo"

    def test_creates_parent_for_caller_supplied_output_file(self, tmp_path):
        """A caller-supplied nested response path has its parent created before writing."""
        output_file = tmp_path / "nested" / "response.json"
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 7, "title": "PR", "repository": {}},
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
        ):
            get_pull_request_details(
                pull_request_id=7,
                repository="test-repo",
                output_file=output_file,
                state={"organization": "https://dev.azure.com/test-org", "project": "TestProject"},
            )

        assert json.loads(output_file.read_text(encoding="utf-8"))["pullRequest"]["pullRequestId"] == 7

    @pytest.mark.parametrize("repository", [42, "", "  ", [], {}])
    def test_invalid_explicit_repository_override_exits(self, repository):
        """Explicit repository overrides must be non-blank strings."""
        with pytest.raises(SystemExit, match="repository must be a non-blank string"):
            get_pull_request_details(
                pull_request_id=7,
                repository=repository,  # type: ignore[arg-type]
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "dry_run": False,
                },
            )

    def test_injected_complete_state_defaults_to_non_dry_run(self, tmp_path):
        """A complete injected Azure state without a dry-run flag executes normally."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 7, "title": "PR", "repository": {}},
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details(
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "pull_request_id": 7,
                }
            )

    @pytest.mark.parametrize(
        ("repository_state", "expected_repository"),
        [
            ({"azure_devops": {"repository": "legacy-repo"}}, "legacy-repo"),
            (
                {"sourceCodeHostingPlatform": {"pullRequest": {"repository": "canonical-repo"}}},
                "canonical-repo",
            ),
        ],
    )
    def test_complete_provider_repository_state_does_not_import_persisted_dry_run(
        self, tmp_path, repository_state, expected_repository
    ):
        """A provider or canonical repository state key avoids ambient state fallback."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.load_state_locked",
                return_value={"dry_run": True},
            ) as load_state,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.is_dry_run", return_value=False),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 7, "title": "PR", "repository": {}},
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details(
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "pull_request_id": 7,
                    **repository_state,
                }
            )

        load_state.assert_not_called()
        assert fetch.call_args.args[1].repository == expected_repository

    def test_injected_state_without_dry_run_falls_back_to_global_dry_run(self, tmp_path, capsys):
        """Injected state should not disable the legacy/global dry-run fallback."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat") as get_pat,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.is_dry_run", return_value=True),
        ):
            get_pull_request_details(
                pull_request_id=7,
                repository="override-repo",
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                },
            )
        assert "DRY-RUN" in capsys.readouterr().out
        get_pat.assert_not_called()

    @pytest.mark.parametrize("raw_pr_id", [True, None])
    def test_invalid_state_pull_request_id_type_exits(self, temp_state_dir, clear_state_before, raw_pr_id):
        """Non-numeric state PR values must fail fast with a clear exit."""
        target = "agentic_devtools.cli.azure_devops.pull_request_details_commands"
        state = dict(organization="https://dev.azure.com/test-org", project="TestProject", repository="test-repo")
        state.update(dry_run=False, pull_request_id=raw_pr_id)
        with patch(f"{target}.get_pat") as get_pat, patch(f"{target}.fetch_pull_request_via_rest") as fetch:
            with pytest.raises(SystemExit, match="positive integer"):
                get_pull_request_details(state=state)
        get_pat.assert_not_called()
        fetch.assert_not_called()

    def test_non_numeric_state_pull_request_id_exits(self):
        """A non-integer PR string from injected state must fail validation."""
        with pytest.raises(SystemExit, match="positive integer"):
            get_pull_request_details(
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "dry_run": False,
                    "pull_request_id": "not-a-number",
                }
            )

    def test_non_positive_explicit_pull_request_id_exits(self):
        """Explicit non-positive PR overrides must fail validation."""
        with pytest.raises(SystemExit, match="positive integer"):
            get_pull_request_details(
                pull_request_id=0,
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "dry_run": False,
                },
            )

    def test_explicit_boolean_pull_request_id_exits(self):
        """An explicit ``True`` override must not be silently accepted as PR 1."""
        with pytest.raises(SystemExit, match="positive integer"):
            get_pull_request_details(
                pull_request_id=True,
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "dry_run": False,
                },
            )

    def test_explicit_non_int_pull_request_id_exits(self):
        """An explicit non-``int`` override must fail with the same controlled message."""
        with pytest.raises(SystemExit, match="positive integer"):
            get_pull_request_details(
                pull_request_id="7",  # type: ignore[arg-type]
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "dry_run": False,
                },
            )

    def test_injected_state_falls_back_to_github_pull_request_number(self, tmp_path):
        """Injected state should honor the legacy GitHub PR-number fallback when needed."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 8, "title": "PR", "repository": {}},
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details(
                state={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "dry_run": False,
                    "github": {"pull_request_number": "8"},
                }
            )
        assert fetch.call_args.args[0] == 8

    def test_partial_injected_state_falls_back_to_loaded_pull_request_id(self, tmp_path):
        """Partial injected state should inherit the persisted PR id."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.load_state_locked",
                return_value={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "pull_request_id": "11",
                    "dry_run": False,
                },
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 11, "title": "PR", "repository": {}},
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details(state={"repository": "override-repo"})
        assert fetch.call_args.args[0] == 11
        assert fetch.call_args.args[1].repository == "override-repo"

    def test_partial_nested_github_override_preserves_persisted_sibling_keys(self, tmp_path):
        """A nested partial override under `github` must not drop sibling persisted keys."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.load_state_locked",
                return_value={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "github": {"repo": "persisted/repo", "pull_request_number": 11},
                    "dry_run": False,
                },
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat", return_value="test-pat"),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value={"pullRequestId": 11, "title": "PR", "repository": {}},
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries", return_value=[]),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details(state={"github": {"provider": "azure_devops"}})
        assert fetch.call_args.args[0] == 11

    def test_partial_injected_state_uses_persisted_dry_run_when_merge_occurs(self, tmp_path, capsys):
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.load_state_locked",
                return_value={
                    "organization": "https://dev.azure.com/test-org",
                    "project": "TestProject",
                    "repository": "test-repo",
                    "pull_request_id": "11",
                    "dry_run": True,
                },
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest"
            ) as fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.is_dry_run", return_value=False),
        ):
            get_pull_request_details(state={"repository": "override-repo"})
        assert "DRY-RUN" in capsys.readouterr().out
        fetch.assert_not_called()


class TestGetPullRequestDetailsExecution:
    """Tests for get_pull_request_details when not in dry-run mode."""

    @pytest.mark.parametrize("encoding", ["cp1252", "utf-8"])
    def test_unicode_metadata_output_preserves_saved_payload(self, tmp_path, monkeypatch, encoding):
        """Console fallbacks must not alter the Unicode PR data saved for review."""
        from agentic_devtools.cli.azure_devops import pull_request_details_commands as details_commands
        from agentic_devtools.state import set_value

        monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(tmp_path))
        set_value("pull_request_id", "123")
        set_value("dry_run", False)
        output_dir = tmp_path / "review-漢"
        pr_data = {
            "pullRequestId": 123,
            "title": "Review 漢",
            "autoCompleteSetBy": {"displayName": "Reviewer 漢"},
            "repository": {
                "id": "repo-id",
                "name": "repo-name",
                "url": "https://dev.azure.com/org/project/_git/repo-name",
                "project": {"id": "project-id", "name": "project-name"},
            },
        }
        with (
            io.TextIOWrapper(io.BytesIO(), encoding=encoding) as stdout,
            patch("sys.stdout", stdout),
            patch.object(details_commands, "get_state_dir", return_value=output_dir),
            patch.object(details_commands, "get_pat", return_value="test-pat"),
            patch.object(details_commands, "get_auth_headers", return_value={}),
            patch.object(details_commands, "fetch_pull_request_via_rest", return_value=pr_data),
            patch.object(details_commands, "get_diff_entries", return_value=[]),
            patch.object(details_commands, "_get_pull_request_threads", return_value=[]),
            patch.object(details_commands, "_get_pull_request_iterations", return_value=[]),
            patch.object(
                details_commands,
                "_get_reviewer_payload",
                return_value={"id": None, "vote": None, "reviewedFiles": []},
            ),
        ):
            get_pull_request_details()
            stdout.flush()
            output = stdout.buffer.getvalue().decode(encoding)

        detail = "?" if encoding == "cp1252" else "漢"
        assert f"Title: Review {detail}" in output
        assert f"Auto-Complete: Set by Reviewer {detail}" in output
        assert f"review-{detail}" in output
        payload = json.loads((output_dir / "temp-get-pull-request-details-response.json").read_text(encoding="utf-8"))
        assert payload["schemaVersion"] == 1
        assert payload["provider"] == "azure_devops"
        assert payload["pullRequest"] == pr_data
        assert payload["repository"] == {
            "id": "repo-id",
            "name": "repo-name",
            "url": "https://dev.azure.com/org/project/_git/repo-name",
            "project": {"id": "project-id", "name": "project-name"},
        }
        assert payload["providerData"] == {"repository": pr_data["repository"]}
        assert payload["capabilities"] == {
            "iterations": "available",
            "reviewedFiles": "available",
            "reviews": "unsupported",
            "reviewThreads": "available",
        }
        assert {warning["capability"]: warning["message"] for warning in payload["warnings"]} == {
            "reviews": "Azure DevOps pull-request details do not include normalized review records.",
        }

    def test_optional_provider_data_failures_are_reported_as_warnings(self, temp_state_dir, clear_state_before):
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")
        pr_data = {
            "pullRequestId": 12345,
            "lastMergeSourceCommit": {"commitId": "head"},
            "repository": {"id": "repo-id", "project": {"id": "project-id", "name": "project"}},
        }
        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_state_dir",
                return_value=temp_state_dir,
            ),
        ):
            get_pull_request_details()

        payload = json.loads((temp_state_dir / "temp-get-pull-request-details-response.json").read_text())
        assert payload["capabilities"] == {
            "iterations": "available",
            "reviewedFiles": "unavailable",
            "reviews": "unsupported",
            "reviewThreads": "unavailable",
        }
        assert {warning["capability"] for warning in payload["warnings"]} == {
            "reviewedFiles",
            "reviews",
            "reviewThreads",
        }

    def test_exits_when_rest_returns_none(self, temp_state_dir, clear_state_before, capsys):
        """Should exit with error when the project-scoped REST PR fetch returns None.

        The REST helper returns None on any failure (non-200 status, network error,
        unparseable body), so this single path replaces the previous az-CLI failure
        and invalid-JSON cases.
        """
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=None,
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                get_pull_request_details()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error" in captured.err
        assert "Failed to get pull request details" in captured.err

    def test_successful_execution(self, temp_state_dir, clear_state_before, tmp_path, capsys):
        """Should successfully retrieve and save PR details."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        # Mock PR data
        pr_data = {
            "pullRequestId": 12345,
            "title": "Test PR",
            "isDraft": False,
            "status": "active",
            "autoCompleteSetBy": None,
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature",
            "lastMergeTargetCommit": {"commitId": "abc123"},
            "lastMergeSourceCommit": {"commitId": "def456"},
            "repository": {
                "id": "repo-id-123",
                "project": {"id": "project-id-123"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
                return_value={"reviewedFiles": []},
            ),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        captured = capsys.readouterr()
        assert "12345" in captured.out
        assert "Test PR" in captured.out
        assert "Pull request details retrieved successfully" in captured.out

    def test_handles_auto_complete_set_by(self, temp_state_dir, clear_state_before, capsys):
        """Should display auto-complete info when set."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        pr_data = {
            "pullRequestId": 12345,
            "title": "Test PR",
            "isDraft": False,
            "status": "active",
            "autoCompleteSetBy": {"displayName": "John Doe"},
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature",
            "repository": {"id": "repo-id", "project": {"id": "project-id"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
                return_value=None,
            ),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        captured = capsys.readouterr()
        assert "Auto-Complete" in captured.out
        assert "John Doe" in captured.out

    def test_skips_sync_and_reviewer_when_no_branches_or_repo_id(self, temp_state_dir, clear_state_before, capsys):
        """Should skip sync_git_ref and reviewer fetch when branches/repo_id missing."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        # PR data with no branch refs, no repo id
        pr_data = {
            "pullRequestId": 12345,
            "title": "Minimal PR",
            "isDraft": False,
            "status": "active",
            "autoCompleteSetBy": None,
            "repository": {},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref") as mock_sync,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
            ) as mock_threads,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
            ) as mock_iterations,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
            ) as mock_reviewer,
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        # sync_git_ref not called because no branches
        mock_sync.assert_not_called()
        # threads/iterations/reviewer not called because no repo_id
        mock_threads.assert_not_called()
        mock_iterations.assert_not_called()
        mock_reviewer.assert_not_called()

    def test_rest_fetch_receives_pr_id_and_config(self, temp_state_dir, clear_state_before):
        """The REST fetch must receive the PR id and the resolved config (project scope).

        This is the essence of the fix: unlike the previous org-scoped
        ``az repos pr show``, the REST path passes the full ``AzureDevOpsConfig``
        (org + project + repository) so the request is project-scoped and
        authenticated with the PAT-derived headers.
        """
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")
        set_value("organization", "my-org")
        set_value("project", "my-project")
        set_value("repository", "my-repo")

        pr_data = {"pullRequestId": 12345, "title": "Test PR", "repository": {}}

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ) as mock_fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        mock_fetch.assert_called_once()
        call_args = mock_fetch.call_args.args
        assert call_args[0] == 12345
        assert isinstance(call_args[1], AzureDevOpsConfig)
        assert call_args[1].organization == "https://dev.azure.com/my-org"
        assert call_args[1].project == "my-project"
        assert call_args[1].repository == "my-repo"
        assert call_args[2] == {"Authorization": "Basic xxx"}
