"""Tests for the review_commands module and helper functions."""

import json
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestSetupPullRequestReviewFocusAreas:
    """Tests for focus-area loading in setup_pull_request_review."""

    def _make_pr_details(self, source_ref="refs/heads/feature/test"):
        return {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": source_ref,
                "targetRefName": "refs/heads/main",
            },
            "files": [],
            "threads": [],
        }

    def _default_get_value(self, key, default=None):
        mapping = {
            "pull_request_id": "123",
            "jira.issue_key": None,
            "include_reviewed": "false",
        }
        return mapping.get(key, default)

    def _patch_setup_dependencies(
        self,
        stack,
        pr_details,
        provider,
        focus_areas_return,
        canonical_repository,
        compatibility_pr_details,
        generated_prompts_dir,
        state_writes,
        capture_render,
        mock_git_result,
        mock_config,
    ):
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        fetch_details = stack.enter_context(patch("agentic_devtools.cli.pull_request_details.get_pull_request_details"))
        fetch_details.return_value = pr_details
        scaffold_threads = stack.enter_context(
            patch("agentic_devtools.cli.azure_devops.review_commands._scaffold_threads_for_review")
        )
        stack.enter_context(
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=lambda key, default=None: {
                    "pull_request_id": "123",
                    "jira.issue_key": None,
                    "include_reviewed": "false",
                    "platform.code_hosting": provider,
                    "github.repo": "owner/repo" if provider == "github" and canonical_repository is None else None,
                    "azure_devops.repository": "test-repo" if provider != "github" else None,
                    "repository": "owner/repo" if provider == "github" else None,
                    "sourceCodeHostingPlatform.pullRequest.repository": canonical_repository,
                }.get(key, default),
            )
        )
        stack.enter_context(patch("agentic_devtools.cli.azure_devops.review_commands.is_dry_run", return_value=False))
        stack.enter_context(
            patch("agentic_devtools.state.set_value", side_effect=lambda *args: state_writes.append(args))
        )
        mock_open = stack.enter_context(patch("builtins.open", create=True))
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
            compatibility_pr_details if compatibility_pr_details is not None else pr_details
        )
        stack.enter_context(patch("pathlib.Path.exists", return_value=True))
        stack.enter_context(
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                return_value=(True, None, set(), False, None),
            )
        )
        stack.enter_context(
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                return_value=(3, 0, 0, generated_prompts_dir, []),
            )
        )
        stack.enter_context(patch("agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"))
        stack.enter_context(patch("agentic_devtools.state.set_workflow_state"))
        stack.enter_context(patch("agentic_devtools.prompts.loader.load_and_render_prompt", side_effect=capture_render))
        stack.enter_context(patch("agentic_devtools.config.load_review_focus_areas", return_value=focus_areas_return))
        stack.enter_context(
            patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=mock_git_result)
        )
        stack.enter_context(
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            )
        )
        stack.enter_context(patch("agentic_devtools.state.set_bootstrap_state"))
        stack.enter_context(patch("agentic_devtools.state.delete_value"))
        return setup_pull_request_review, fetch_details, scaffold_threads

    def _run_setup(
        self,
        pr_details,
        focus_areas_return,
        prompts_dir=None,
        provider=None,
        expect_setup_error=False,
        canonical_repository=None,
        compatibility_pr_details=None,
    ):
        """Run setup_pull_request_review with mocked dependencies, return captured calls."""
        captured_variables = {}
        generated_prompts_dir = prompts_dir or MagicMock()

        def capture_render(workflow_name, step_name, variables, **kwargs):
            captured_variables.update(variables)

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        state_writes = []

        with ExitStack() as stack:
            setup_pull_request_review, fetch_details, scaffold_threads = self._patch_setup_dependencies(
                stack,
                pr_details,
                provider,
                focus_areas_return,
                canonical_repository,
                compatibility_pr_details,
                generated_prompts_dir,
                state_writes,
                capture_render,
                mock_git_result,
                mock_config,
            )
            if expect_setup_error:
                with pytest.raises(SystemExit) as exc_info:
                    setup_pull_request_review()
                assert exc_info.value.code == 1
            else:
                setup_pull_request_review()

        fetch_details.assert_called_once_with(provider=provider or "azure_devops")
        if provider == "github":
            assert ("provider", "github") in state_writes
            assert ("platform.code_hosting", "github") in state_writes
            if canonical_repository is None:
                assert ("github.repo", "owner/repo") in state_writes
            assert ("repository", "owner/repo") in state_writes
            if canonical_repository:
                assert ("sourceCodeHostingPlatform.pullRequest.repository", canonical_repository) in state_writes
            scaffold_threads.assert_not_called()
        else:
            scaffold_threads.assert_called_once()
        return captured_variables

    def test_focus_areas_passed_to_prompt_when_available(self):
        """Test that repo_review_focus_areas is passed when load_review_focus_areas returns content."""
        focus_content = "## .NET DI Patterns\n- Use constructor injection"
        variables = self._run_setup(self._make_pr_details(), focus_content)

        assert variables.get("repo_review_focus_areas") == focus_content

    def test_focus_areas_empty_string_when_none_returned(self):
        """Test that repo_review_focus_areas is empty string when load_review_focus_areas returns None."""
        variables = self._run_setup(self._make_pr_details(), None)

        assert variables.get("repo_review_focus_areas") == ""

    def test_pr_url_passed_to_prompt(self):
        """Test that pr_url is passed to the prompt variables containing the PR ID."""
        variables = self._run_setup(self._make_pr_details(), None)

        pr_url = variables.get("pr_url")
        assert pr_url is not None
        assert "/pullrequest/" in pr_url
        assert "123" in pr_url

    def test_source_code_platform_passed_to_prompt(self):
        """Test that source_code_platform is passed as AzureDevOps."""
        variables = self._run_setup(self._make_pr_details(), None)

        assert variables.get("source_code_platform") == "AzureDevOps"

    def test_github_setup_uses_github_url_and_platform(self):
        """GitHub setup preserves its provider and renders provider-specific review context."""
        pr_details = self._make_pr_details()
        pr_details.update(
            {
                "provider": "github",
                "repository": {"id": "owner/repo", "name": "repo", "project": {"name": "owner"}},
            }
        )

        variables = self._run_setup(pr_details, None, provider="github")

        assert variables["pr_url"] == "https://github.com/owner/repo/pull/123"
        assert variables["source_code_platform"] == "GitHub"

    def test_setup_uses_fetched_payload_instead_of_compatibility_file(self):
        """Setup initializes review context from its own fetch result, not shared state."""
        fetched_details = self._make_pr_details()
        fetched_details["pullRequest"]["title"] = "fresh title"
        compatibility_details = self._make_pr_details()
        compatibility_details["pullRequest"]["title"] = "stale title"

        variables = self._run_setup(
            fetched_details,
            None,
            compatibility_pr_details=compatibility_details,
        )

        assert variables["pr_title"] == "fresh title"

    def test_github_setup_preserves_canonical_repository_during_bootstrap(self):
        """Canonical provider-neutral repository state survives bootstrap scoping."""
        pr_details = self._make_pr_details()
        pr_details.update(
            {
                "provider": "github",
                "repository": {"id": "canonical/repo", "name": "repo", "project": {"name": "canonical"}},
            }
        )

        self._run_setup(pr_details, None, provider="github", canonical_repository="canonical/repo")

    def test_github_setup_rejects_invalid_repository_metadata(self):
        """GitHub setup rejects an invalid repository before rendering workflow context."""
        pr_details = self._make_pr_details()
        pr_details.update({"provider": "github", "repository": "invalid"})

        self._run_setup(pr_details, None, provider="github", expect_setup_error=True)

    def test_artifact_context_matches_commit_scoped_prompts_directory(self, tmp_path):
        """Setup passes the generated commit-scoped directory to later review prompts."""
        prompts_dir = tmp_path / "pull-request-review" / "e8f8350144db"

        variables = self._run_setup(self._make_pr_details(), None, prompts_dir=prompts_dir)

        assert variables["review_artifact_dir_name"] == "e8f8350144db"
        assert variables["review_artifact_dir"] == "pull-request-review/e8f8350144db"

    def test_artifact_context_preserves_pr_fallback_directory(self, tmp_path):
        """Setup passes the PR-scoped fallback when no commit directory is available."""
        prompts_dir = tmp_path / "pull-request-review" / "PR123"

        variables = self._run_setup(self._make_pr_details(), None, prompts_dir=prompts_dir)

        assert variables["review_artifact_dir_name"] == "PR123"
        assert variables["review_artifact_dir"] == "pull-request-review/PR123"

    def test_load_review_focus_areas_called_with_git_root(self):
        """Test that load_review_focus_areas is called with the git repo root when available."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        pr_details = self._make_pr_details()

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=self._default_get_value,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(pr_details)
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch(
                            "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                            return_value=(True, None, set(), False, None),
                        ):
                            with patch(
                                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                                return_value=(3, 0, 0, MagicMock(), []),
                            ):
                                with patch(
                                    "agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"
                                ):
                                    with patch("agentic_devtools.state.set_workflow_state"):
                                        with patch("agentic_devtools.prompts.loader.load_and_render_prompt"):
                                            with patch("agentic_devtools.config.load_review_focus_areas") as mock_load:
                                                mock_load.return_value = None
                                                with patch(
                                                    "agentic_devtools.cli.azure_devops.review_commands.run_safe",
                                                    return_value=mock_git_result,
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                                                        return_value=mock_config,
                                                    ):
                                                        with patch("agentic_devtools.state.set_bootstrap_state"):
                                                            with patch("agentic_devtools.state.set_value"):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()
                                                                mock_load.assert_called_once_with("/repo/root")

    def test_load_review_focus_areas_falls_back_to_cwd_when_git_fails(self):
        """Test that load_review_focus_areas falls back to cwd when git rev-parse fails."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        pr_details = self._make_pr_details()

        mock_git_result = MagicMock()
        mock_git_result.returncode = 128
        mock_git_result.stdout = ""

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=self._default_get_value,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(pr_details)
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch(
                            "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                            return_value=(True, None, set(), False, None),
                        ):
                            with patch(
                                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                                return_value=(3, 0, 0, MagicMock(), []),
                            ):
                                with patch(
                                    "agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"
                                ):
                                    with patch("agentic_devtools.state.set_workflow_state"):
                                        with patch("agentic_devtools.prompts.loader.load_and_render_prompt"):
                                            with patch("agentic_devtools.config.load_review_focus_areas") as mock_load:
                                                mock_load.return_value = None
                                                with patch(
                                                    "agentic_devtools.cli.azure_devops.review_commands.run_safe",
                                                    return_value=mock_git_result,
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                                                        return_value=mock_config,
                                                    ):
                                                        with patch("agentic_devtools.state.set_bootstrap_state"):
                                                            with patch("agentic_devtools.state.set_value"):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()
                                                                mock_load.assert_called_once_with(str(Path.cwd()))

    def test_load_review_focus_areas_falls_back_to_cwd_when_run_safe_raises(self):
        """Test that load_review_focus_areas falls back to cwd when run_safe raises an exception."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        pr_details = self._make_pr_details()

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=self._default_get_value,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(pr_details)
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch(
                            "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                            return_value=(True, None, set(), False, None),
                        ):
                            with patch(
                                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                                return_value=(3, 0, 0, MagicMock(), []),
                            ):
                                with patch(
                                    "agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"
                                ):
                                    with patch("agentic_devtools.state.set_workflow_state"):
                                        with patch("agentic_devtools.prompts.loader.load_and_render_prompt"):
                                            with patch("agentic_devtools.config.load_review_focus_areas") as mock_load:
                                                mock_load.return_value = None
                                                with patch(
                                                    "agentic_devtools.cli.azure_devops.review_commands.run_safe",
                                                    side_effect=OSError("git not found"),
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                                                        return_value=mock_config,
                                                    ):
                                                        with patch("agentic_devtools.state.set_bootstrap_state"):
                                                            with patch("agentic_devtools.state.set_value"):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()
                                                                mock_load.assert_called_once_with(str(Path.cwd()))
