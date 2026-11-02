"""Tests for create_pull_request function."""

import json
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli import azure_devops
from agentic_devtools.cli.azure_devops import commands
from agentic_devtools.cli.azure_devops.commands import PullRequestCreationPostSubmitError


@pytest.fixture(autouse=True)
def _mock_resolve_pr_body():
    """Mock resolve_pr_body for create_pull_request tests.

    The function is called internally by create_pull_request; these tests
    focus on the Azure DevOps CLI interaction, not template resolution.
    Returns the state ``description`` value to preserve existing test semantics.
    """
    with patch(
        "agentic_devtools.cli.pr_template.resolve_pr_body",
    ) as mock:

        def _from_state():
            return state.get_value("description") or ""

        mock.side_effect = _from_state
        yield mock


@pytest.fixture(autouse=True)
def _mock_resolve_pr_title():
    """Mock resolve_pr_title for create_pull_request tests.

    The function is called internally by create_pull_request; these tests
    focus on the Azure DevOps CLI interaction, not title template resolution.
    Returns None so that the fallback (convert_to_pull_request_title) is used.
    """
    with patch(
        "agentic_devtools.cli.pr_template.resolve_pr_title",
        return_value=None,
    ):
        yield


class TestCreatePullRequest:
    """Tests for create_pull_request command."""

    def test_negative_timeout_is_rejected_during_dry_run(self, temp_state_dir, clear_state_before):
        """Reject an invalid subprocess timeout before returning from dry-run mode."""
        with pytest.raises(ValueError, match="timeout must be non-negative"):
            azure_devops.create_pull_request(timeout=-1, dry_run=True)

    def test_dry_run_basic(self, temp_state_dir, clear_state_before, capsys):
        """Test basic dry run output."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "feature/test" in captured.out
        assert "Test PR" in captured.out

    def test_dry_run_with_target_branch(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run shows target branch."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("target_branch", "develop")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "develop" in captured.out

    def test_dry_run_defaults_empty_target_branch_to_main(self, temp_state_dir, clear_state_before, capsys):
        """An empty target-branch value retains the legacy main-branch fallback."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("target_branch", "")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        assert "Target Branch: main" in capsys.readouterr().out

    def test_dry_run_draft_mode_default(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run shows draft mode is True by default."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Draft Mode: True" in captured.out

    def test_dry_run_draft_mode_false(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run shows draft mode is False when set."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("draft", False)
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Draft Mode: False" in captured.out

    def test_dry_run_draft_mode_bool_true(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run with draft=True boolean."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("draft", True)
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Draft Mode: True" in captured.out

    def test_dry_run_draft_mode_string_true(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run with draft='true' string."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("draft", "true")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Draft Mode: True" in captured.out

    def test_dry_run_draft_mode_string_no(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run with draft='no' string."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("draft", "no")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Draft Mode: False" in captured.out

    def test_dry_run_draft_mode_string_0(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run with draft='0' string."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("draft", "0")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Draft Mode: False" in captured.out

    def test_dry_run_converts_title(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run converts Markdown title."""
        state.set_value("source_branch", "feature/test")
        state.set_value(
            "title",
            "feature([PROJECT-1234](https://jira.swica.ch/browse/PROJECT-1234)): test",
        )
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        # Title should have Markdown links stripped
        assert "Title: feature(PROJECT-1234): test" in captured.out

    @patch("agentic_devtools.cli.pr_template.resolve_pr_title", return_value="feat(PROJ-99): rendered title")
    def test_dry_run_uses_rendered_title_from_template(self, _mock_title, temp_state_dir, clear_state_before, capsys):
        """Uses rendered title from template when available."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "feat(PROJ-99): Original Title With Links")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        _mock_title.assert_called_once_with()
        assert "Title: feat(PROJ-99): rendered title" in captured.out

    def test_dry_run_accepts_already_rendered_title(self, temp_state_dir, clear_state_before, capsys):
        """Skips title template resolution when the caller supplies a rendered title."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Original title")
        state.set_dry_run(True)

        azure_devops.create_pull_request(title="Rendered title", title_is_rendered=True)

        assert "Title: Rendered title" in capsys.readouterr().out

    def test_empty_explicit_title_is_rejected_instead_of_using_state(self, temp_state_dir, clear_state_before, capsys):
        """Rejects an explicitly empty title even when state contains a title."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "State-backed title")

        with pytest.raises(SystemExit):
            azure_devops.create_pull_request(title="", dry_run=True)

        assert "Error: No title found." in capsys.readouterr().err

    @patch("agentic_devtools.cli.pr_template.resolve_pr_title", return_value="feat(PROJ-99): explicit title")
    def test_dry_run_uses_explicit_title_as_template_input(
        self, mock_resolve_title, temp_state_dir, clear_state_before, capsys
    ):
        """Uses an explicit title override as the PR title template input."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "State-backed title")
        state.set_dry_run(True)

        azure_devops.create_pull_request(title="Explicit title")

        mock_resolve_title.assert_called_once_with("Explicit title")
        assert "Title: feat(PROJ-99): explicit title" in capsys.readouterr().out

    def test_dry_run_with_description(self, temp_state_dir, clear_state_before, capsys):
        """Test dry run shows description when provided."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("description", "This is a test PR description")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Description: This is a test PR description" in captured.out

    def test_explicit_request_fields_override_state(self, temp_state_dir, clear_state_before, capsys):
        """The provider-neutral request takes precedence over mutable state."""
        state.set_value("source_branch", "state-branch")
        state.set_value("title", "State title")
        state.set_value("description", "State description")
        state.set_value("target_branch", "state-target")
        state.set_value("draft", True)
        state.set_value("reviewers", "state-reviewer")
        state.set_dry_run(False)

        azure_devops.create_pull_request(
            source_branch="request-branch",
            title="Request title",
            title_is_rendered=True,
            description="Request description",
            target_branch="request-target",
            draft=False,
            reviewers="request-reviewer",
            dry_run=True,
        )

        output = capsys.readouterr().out
        assert "Source Branch: request-branch" in output
        assert "Title: Request title" in output
        assert "Description: Request description" in output
        assert "Target Branch: request-target" in output
        assert "Draft Mode: False" in output
        assert "Reviewers: request-reviewer" in output

    def test_description_must_be_string(self, temp_state_dir, clear_state_before, capsys):
        """Reject non-string description overrides from state."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("description", {"body": "bad"})

        with pytest.raises(SystemExit):
            azure_devops.create_pull_request()

        assert "Error: description must be a string" in capsys.readouterr().err

    def test_target_branch_must_be_string(self, temp_state_dir, clear_state_before, capsys):
        """Reject non-string target-branch overrides from state."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("target_branch", 7)

        with pytest.raises(SystemExit):
            azure_devops.create_pull_request()

        assert "Error: target_branch must be a string" in capsys.readouterr().err

    @pytest.mark.parametrize("invalid_target_branch", [False, 0])
    def test_falsey_non_string_target_branch_is_rejected(
        self, invalid_target_branch, temp_state_dir, clear_state_before, capsys
    ):
        """Reject falsey non-string target-branch values rather than defaulting to main."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("target_branch", invalid_target_branch)
        state.set_dry_run(True)

        with pytest.raises(SystemExit):
            azure_devops.create_pull_request()

        assert "Error: target_branch must be a string" in capsys.readouterr().err

    def test_missing_source_branch(self, temp_state_dir, clear_state_before):
        """Test exits when source branch is missing."""
        state.set_value("title", "Test PR")
        with pytest.raises(SystemExit):
            azure_devops.create_pull_request()

    def test_missing_title(self, temp_state_dir, clear_state_before):
        """Test exits when title is missing."""
        state.set_value("source_branch", "feature/test")
        with pytest.raises(SystemExit):
            azure_devops.create_pull_request()

    def test_missing_description_ok(self, temp_state_dir, clear_state_before, capsys):
        """Test missing description is OK."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Description:" not in captured.out  # No description line when empty


class TestCreatePullRequestActualCall:
    """Tests for create_pull_request with mocked subprocess calls."""

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_successful_pr_creation(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test successful PR creation."""
        # Mock az --version check
        mock_version = MagicMock()
        mock_version.returncode = 0

        # Mock extension check
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"

        # Mock pr create
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {"webUrl": "https://test"}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "999" in captured.out

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_invalid_success_response_is_post_submit_failure(self, mock_run, temp_state_dir, clear_state_before):
        """Expose invalid JSON after a successful Azure CLI submission as indeterminate."""
        mock_version = MagicMock(returncode=0)
        mock_ext = MagicMock(returncode=0, stdout="azure-devops")
        mock_create = MagicMock(returncode=0, stdout="not-json")
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with pytest.raises(PullRequestCreationPostSubmitError, match="outcome is indeterminate"):
            azure_devops.create_pull_request()

    def test_az_cli_verification_timeout_is_pre_submit_failure(self, temp_state_dir, clear_state_before):
        """A timeout before the create command must not be reported as indeterminate success."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.verify_az_cli",
                side_effect=subprocess.TimeoutExpired("az --version", timeout=10),
            ),
            pytest.raises(RuntimeError, match="Azure CLI verification timed out before pull-request creation"),
        ):
            azure_devops.create_pull_request()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_state_persistence_failure_is_post_submit_failure(self, mock_run, temp_state_dir, clear_state_before):
        """A state-write failure after PR submission must be reported as indeterminate."""
        mock_run.side_effect = [
            MagicMock(returncode=0),
            MagicMock(returncode=0, stdout="azure-devops"),
            MagicMock(returncode=0, stdout='{"pullRequestId": 999, "repository": {}}'),
        ]
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.set_value",
                side_effect=OSError("disk full"),
            ),
            pytest.raises(PullRequestCreationPostSubmitError, match="state persistence failed"),
        ):
            azure_devops.create_pull_request()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_pull_request_id_persistence_can_be_deferred(self, mock_run, temp_state_dir, clear_state_before):
        """A caller can capture the created ID without triggering immediate state migration."""
        mock_run.side_effect = [
            MagicMock(returncode=0),
            MagicMock(returncode=0, stdout="azure-devops"),
            MagicMock(returncode=0, stdout='{"pullRequestId": 999, "repository": {}}'),
        ]
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        on_created = MagicMock()

        with (
            patch("agentic_devtools.cli.azure_devops.commands.set_value") as set_value,
            patch("agentic_devtools.cli.workflows.advancement.try_advance_workflow_after_pr_creation"),
        ):
            azure_devops.create_pull_request(on_pull_request_created=on_created)

        on_created.assert_called_once_with(999)
        set_value.assert_not_called()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_workflow_advancement_failure_is_post_submit_failure(self, mock_run, temp_state_dir, clear_state_before):
        """A workflow-advance failure after PR submission must not invite a duplicate retry."""
        mock_run.side_effect = [
            MagicMock(returncode=0),
            MagicMock(returncode=0, stdout="azure-devops"),
            MagicMock(returncode=0, stdout='{"pullRequestId": 999, "repository": {}}'),
        ]
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with (
            patch(
                "agentic_devtools.cli.workflows.advancement.try_advance_workflow_after_pr_creation",
                side_effect=RuntimeError("workflow unavailable"),
            ),
            pytest.raises(PullRequestCreationPostSubmitError, match="workflow advancement failed"),
        ):
            azure_devops.create_pull_request()

        assert state.get_value("pull_request_id") == 999

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_non_object_success_response_is_post_submit_failure(self, mock_run, temp_state_dir, clear_state_before):
        """Treat a valid JSON value with no PR object as an indeterminate outcome."""
        mock_version = MagicMock(returncode=0)
        mock_ext = MagicMock(returncode=0, stdout="azure-devops")
        mock_create = MagicMock(returncode=0, stdout="[]")
        mock_run.side_effect = [mock_version, mock_ext, mock_create]
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with pytest.raises(PullRequestCreationPostSubmitError, match="valid pullRequestId"):
            azure_devops.create_pull_request()

    @pytest.mark.parametrize("repository", [[], {"webUrl": 42}])
    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_malformed_repository_success_response_is_post_submit_failure(
        self, mock_run, repository, temp_state_dir, clear_state_before
    ):
        """Treat malformed repository metadata as an indeterminate outcome."""
        mock_version = MagicMock(returncode=0)
        mock_ext = MagicMock(returncode=0, stdout="azure-devops")
        mock_create = MagicMock(
            returncode=0,
            stdout=json.dumps({"pullRequestId": 9, "repository": repository}),
        )
        mock_run.side_effect = [mock_version, mock_ext, mock_create]
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with pytest.raises(PullRequestCreationPostSubmitError, match="malformed"):
            azure_devops.create_pull_request()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_pr_creation_failure(self, mock_run, temp_state_dir, clear_state_before, capsys):
        """Test PR creation fails when az command fails."""
        # Mock az --version check
        mock_version = MagicMock()
        mock_version.returncode = 0

        # Mock extension check
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"

        # Mock pr create failure
        mock_create = MagicMock()
        mock_create.returncode = 1
        mock_create.stderr = "PR creation failed: branch not found"

        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/nonexistent")
        state.set_value("title", "Test PR")

        with pytest.raises(SystemExit) as exc_info:
            azure_devops.create_pull_request()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error creating PR" in captured.err

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(
        "agentic_devtools.cli.azure_devops.commands.sys",
        SimpleNamespace(platform="linux", stderr=sys.stderr, exit=sys.exit),
    )
    @patch("subprocess.run")
    def test_pr_creation_with_description(self, mock_run, temp_state_dir, clear_state_before):
        """Test PR creation with description."""
        assert commands.sys is not sys
        mock_version = MagicMock(returncode=0)
        mock_ext = MagicMock(returncode=0, stdout="azure-devops")
        mock_create = MagicMock(returncode=0, stdout='{"pullRequestId": 999, "repository": {}}')

        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("description", "PR description")

        azure_devops.create_pull_request()

        # On non-Windows platforms, description is passed directly.
        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        assert "--description" in cmd
        desc_index = cmd.index("--description")
        assert cmd[desc_index + 1] == "PR description"

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_pr_creation_with_draft_false_omits_draft_flag(self, mock_run, temp_state_dir, clear_state_before):
        """A non-draft PR should omit the --draft flag."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("draft", False)

        azure_devops.create_pull_request()

        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        assert "--draft" not in cmd

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_pr_creation_without_pr_id_is_indeterminate(self, mock_run, temp_state_dir, clear_state_before):
        """Responses without a PR ID are treated as indeterminate post-submit outcomes."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"repository": {"webUrl": "https://test"}}'

        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with pytest.raises(PullRequestCreationPostSubmitError, match="valid pullRequestId"):
            azure_devops.create_pull_request()

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch(
        "agentic_devtools.cli.azure_devops.commands.sys",
        SimpleNamespace(platform="linux", stderr=sys.stderr, exit=sys.exit),
    )
    @patch("subprocess.run")
    @patch("agentic_devtools.cli.pr_template.resolve_pr_body", return_value="Body from template")
    def test_resolve_pr_body_called_and_passed_to_az(self, mock_resolve, mock_run, temp_state_dir, clear_state_before):
        """resolve_pr_body() is invoked and its return value is passed as --description to az."""
        assert commands.sys is not sys
        mock_version = MagicMock(returncode=0)
        mock_ext = MagicMock(returncode=0, stdout="azure-devops")
        mock_create = MagicMock(returncode=0, stdout='{"pullRequestId": 999, "repository": {}}')

        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        azure_devops.create_pull_request()

        mock_resolve.assert_called_once()
        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        assert "--description" in cmd
        desc_index = cmd.index("--description")
        assert cmd[desc_index + 1] == "Body from template"

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("tempfile.NamedTemporaryFile")
    @patch("os.unlink")
    @patch("subprocess.run")
    def test_pr_creation_with_description_uses_tempfile_on_windows(
        self,
        mock_run,
        mock_unlink,
        mock_named_temporary_file,
        temp_state_dir,
        clear_state_before,
    ):
        """Windows uses @filepath workaround for multiline-safe PR descriptions."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {}}'
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        mock_temp_file = MagicMock()
        mock_temp_file.name = r"C:\temp\agdt-pr-desc.md"
        mock_named_temporary_file.return_value.__enter__.return_value = mock_temp_file

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("description", "line one\nline two")

        with patch(
            "agentic_devtools.cli.azure_devops.commands.sys",
            SimpleNamespace(platform="win32", stderr=sys.stderr, exit=sys.exit),
        ):
            azure_devops.create_pull_request()

        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        desc_index = cmd.index("--description")
        assert cmd[desc_index + 1] == r"@C:\temp\agdt-pr-desc.md"
        mock_temp_file.write.assert_called_once_with("line one\nline two")
        mock_unlink.assert_called_once_with(r"C:\temp\agdt-pr-desc.md")

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("tempfile.NamedTemporaryFile")
    @patch("os.unlink")
    @patch("subprocess.run")
    def test_pr_creation_escapes_cmd_visible_values_on_windows(
        self,
        mock_run,
        mock_unlink,
        mock_named_temporary_file,
        temp_state_dir,
        clear_state_before,
    ):
        """Windows escapes percent signs in all cmd.exe-visible az arguments."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {}}'
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        mock_temp_file = MagicMock()
        mock_temp_file.name = r"C:\temp\%USERNAME%\agdt-pr-desc.md"
        mock_named_temporary_file.return_value.__enter__.return_value = mock_temp_file

        state.set_value("source_branch", "feature/%USERPROFILE%/test")
        state.set_value("target_branch", "release/%APPDATA%")
        state.set_value("title", "Test %AZURE_DEVOPS_EXT_PAT%")
        state.set_value("description", "line one\nline two")
        state.set_value("organization", "https://dev.azure.com/%ORG%")
        state.set_value("project", "%PROJECT%")
        state.set_value("repository", "%REPO%")

        with patch(
            "agentic_devtools.cli.azure_devops.commands.sys",
            SimpleNamespace(platform="win32", stderr=sys.stderr, exit=sys.exit),
        ):
            azure_devops.create_pull_request()

        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]

        source_index = cmd.index("--source-branch")
        target_index = cmd.index("--target-branch")
        title_index = cmd.index("--title")
        org_index = cmd.index("--organization")
        project_index = cmd.index("--project")
        repo_index = cmd.index("--repository")
        desc_index = cmd.index("--description")

        assert cmd[source_index + 1] == "feature/%%USERPROFILE%%/test"
        assert cmd[target_index + 1] == "release/%%APPDATA%%"
        assert cmd[title_index + 1] == "Test %%AZURE_DEVOPS_EXT_PAT%%"
        assert cmd[org_index + 1] == "https://dev.azure.com/%%ORG%%"
        assert cmd[project_index + 1] == "%%PROJECT%%"
        assert cmd[repo_index + 1] == "%%REPO%%"
        assert cmd[desc_index + 1] == r"@C:\temp\%%USERNAME%%\agdt-pr-desc.md"
        mock_unlink.assert_called_once_with(r"C:\temp\%USERNAME%\agdt-pr-desc.md")

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("tempfile.NamedTemporaryFile")
    @patch("os.unlink")
    @patch("subprocess.run")
    def test_pr_creation_failure_cleans_up_tempfile_on_windows(
        self,
        mock_run,
        mock_unlink,
        mock_named_temporary_file,
        temp_state_dir,
        clear_state_before,
    ):
        """Windows temp description files are removed even when PR creation fails."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 1
        mock_create.stderr = "creation failed"
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        mock_temp_file = MagicMock()
        mock_temp_file.name = r"C:\temp\agdt-pr-desc.md"
        mock_named_temporary_file.return_value.__enter__.return_value = mock_temp_file

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("description", "line one\nline two")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.commands.sys",
                SimpleNamespace(platform="win32", stderr=sys.stderr, exit=sys.exit),
            ),
            pytest.raises(SystemExit),
        ):
            azure_devops.create_pull_request()

        mock_unlink.assert_called_once_with(r"C:\temp\agdt-pr-desc.md")

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("tempfile.NamedTemporaryFile")
    @patch("subprocess.run")
    def test_pr_creation_without_description_does_not_use_tempfile_on_windows(
        self,
        mock_run,
        mock_named_temporary_file,
        temp_state_dir,
        clear_state_before,
    ):
        """Windows should not create a temp file when description is empty."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {}}'
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        with patch(
            "agentic_devtools.cli.azure_devops.commands.sys",
            SimpleNamespace(platform="win32", stderr=sys.stderr, exit=sys.exit),
        ):
            azure_devops.create_pull_request()

        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        assert "--description" not in cmd
        mock_named_temporary_file.assert_not_called()

    def test_dry_run_with_reviewers(self, temp_state_dir, clear_state_before, capsys):
        """Dry run should list the reviewers that would be assigned."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("reviewers", "alice@example.com,bob@example.com")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Reviewers: alice@example.com, bob@example.com" in captured.out

    def test_dry_run_without_reviewers_omits_reviewers_line(self, temp_state_dir, clear_state_before, capsys):
        """Dry run should not print a reviewers line when none are supplied."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_dry_run(True)

        azure_devops.create_pull_request()

        captured = capsys.readouterr()
        assert "Reviewers:" not in captured.out

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_pr_creation_with_reviewers(self, mock_run, temp_state_dir, clear_state_before):
        """Reviewers should be passed to az repos pr create as separate args."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {}}'
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("reviewers", "alice@example.com,bob@example.com")

        azure_devops.create_pull_request()

        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        assert "--reviewers" in cmd
        reviewers_index = cmd.index("--reviewers")
        assert cmd[reviewers_index + 1 : reviewers_index + 3] == [
            "alice@example.com",
            "bob@example.com",
        ]

    @patch.dict("os.environ", {"AZURE_DEV_OPS_COPILOT_PAT": "test-pat"})
    @patch("subprocess.run")
    def test_pr_creation_without_reviewers_omits_reviewers_flag(self, mock_run, temp_state_dir, clear_state_before):
        """No --reviewers flag should be passed when reviewers is unset."""
        mock_version = MagicMock()
        mock_version.returncode = 0
        mock_ext = MagicMock()
        mock_ext.returncode = 0
        mock_ext.stdout = "azure-devops"
        mock_create = MagicMock()
        mock_create.returncode = 0
        mock_create.stdout = '{"pullRequestId": 999, "repository": {}}'
        mock_run.side_effect = [mock_version, mock_ext, mock_create]

        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")

        azure_devops.create_pull_request()

        create_call = mock_run.call_args_list[2]
        cmd = create_call[0][0]
        assert "--reviewers" not in cmd

    def test_reviewers_non_string_errors(self, temp_state_dir, clear_state_before, capsys):
        """A non-string reviewers value should error before invoking az."""
        state.set_value("source_branch", "feature/test")
        state.set_value("title", "Test PR")
        state.set_value("reviewers", 123)

        with pytest.raises(SystemExit) as exc_info:
            azure_devops.create_pull_request()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "reviewers must be a comma-separated string" in captured.err
