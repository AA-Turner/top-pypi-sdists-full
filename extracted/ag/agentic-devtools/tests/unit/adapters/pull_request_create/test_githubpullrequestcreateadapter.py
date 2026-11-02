import json
import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.pull_request_create import GitHubPullRequestCreateAdapter, PullRequestCreateRequest


@pytest.fixture(autouse=True)
def _no_repo_resolution_by_default():
    """Prevent real git-remote/state lookups from leaking into unrelated tests.

    Without this, ``resolve_github_repo_safe()`` (called by the adapter while
    building the ``gh pr create`` command) would hit the real environment's
    git remote and state, making unrelated command-shape assertions depend on
    whatever repository happens to be checked out. Defaulting to a stable
    repository also keeps URL-validation tests independent from the runner's
    checkout. Tests that specifically exercise repository resolution override
    this patch.
    """
    with (
        patch("agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe", return_value="o/r"),
        patch(
            "agentic_devtools.adapters.pull_request_create.require_default_repo_workflow_token",
            return_value="workflow-token",
        ),
    ):
        yield


class _RecordingState:
    """Stand-in for ``read_modify_write_state()`` that records the mutated dict."""

    def __init__(self) -> None:
        self.data: dict = {}

    def __enter__(self) -> dict:
        return self.data

    def __exit__(self, *exc: object) -> None:
        return None


def test_github_adapter_passes_resolved_repo_to_gh_create() -> None:
    """`--repo` is resolved explicitly instead of relying on `gh`'s cwd-based detection."""
    request = PullRequestCreateRequest("github", "feature", "Title", "Body", "main", False)
    result = MagicMock(returncode=0, stdout="https://github.com/owner/repo/pull/9\n", stderr="")

    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result) as run_safe,
        patch(
            "agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe",
            return_value="owner/repo",
        ) as resolve_repo,
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state",
            return_value=state,
        ) as read_modify_write_state,
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation"),
    ):
        GitHubPullRequestCreateAdapter().create(request)

    command = run_safe.call_args.args[0]
    assert "--repo" in command and command[command.index("--repo") + 1] == "owner/repo"
    resolve_repo.assert_called_once_with()
    read_modify_write_state.assert_called_once_with(
        _bootstrap_update=("pull_request_id", 9),
        _override_migrated_keys=("pull_request_id", "github.pull_request_number"),
    )


def test_github_adapter_fails_when_repo_is_unresolvable() -> None:
    """Repository resolution must fail closed instead of relying on gh's cwd heuristics."""
    request = PullRequestCreateRequest("github", "feature", "Title", "Body", "main", False)

    with (
        patch(
            "agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe",
            return_value=None,
        ),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is False
    assert created.status == "failed"
    assert created.error == "Could not determine GitHub repository for pull-request creation"


def test_github_adapter_creates_draft_and_assigns_reviewers() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title", "Body", "main", True, ("alice", "bob"))
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/7\n", stderr="")

    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result) as run_safe,
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    command = run_safe.call_args.args[0]
    assert command[:6] == ["gh", "pr", "create", "--title", "Title", "--body-file"]
    assert command[6].endswith(".md")
    assert command[7:9] == ["--base", "main"]
    assert "--head" in command and command[command.index("--head") + 1] == "feature"
    assert "--draft" in command
    assert command[-4:] == ["--reviewer", "alice", "--reviewer", "bob"]
    assert run_safe.call_args.kwargs["timeout"] == 60
    assert created.url == "https://github.com/o/r/pull/7"
    assert state.data["pull_request_id"] == 7
    assert state.data["github"]["pull_request_number"] == 7
    advance.assert_called_once_with(7, "https://github.com/o/r/pull/7")


def test_github_adapter_dry_run_does_not_execute_command(capsys) -> None:
    request = PullRequestCreateRequest("github", "feature", "Title", "", "main", False, (), dry_run=True)

    with patch("agentic_devtools.adapters.pull_request_create.run_safe") as run_safe:
        result = GitHubPullRequestCreateAdapter().create(request)

    run_safe.assert_not_called()
    assert result.status == "dry_run"
    assert "[DRY RUN]" in capsys.readouterr().out


def test_github_adapter_rejects_azure_request_before_dry_run() -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", dry_run=True)

    with patch("agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe") as resolve_repo:
        result = GitHubPullRequestCreateAdapter().create(request)

    resolve_repo.assert_not_called()
    assert result.success is False
    assert result.provider == "azure_devops"
    assert result.status == "failed"
    assert result.error == "provider mismatch"


def test_github_adapter_dry_run_prints_reviewers_when_present(capsys) -> None:
    request = PullRequestCreateRequest("github", "feature", "Title", "", "main", False, ("alice", "bob"), dry_run=True)

    with patch("agentic_devtools.adapters.pull_request_create.run_safe") as run_safe:
        GitHubPullRequestCreateAdapter().create(request)

    run_safe.assert_not_called()
    assert "Reviewers: alice, bob" in capsys.readouterr().out


def test_github_adapter_dry_run_omits_reviewers_line_when_empty(capsys) -> None:
    request = PullRequestCreateRequest("github", "feature", "Title", "", "main", False, (), dry_run=True)

    with patch("agentic_devtools.adapters.pull_request_create.run_safe") as run_safe:
        GitHubPullRequestCreateAdapter().create(request)

    run_safe.assert_not_called()
    assert "Reviewers:" not in capsys.readouterr().out


def test_github_adapter_creates_non_draft_without_reviewers() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title", "Body", "main", False)
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/8\n", stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result) as run_safe,
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    command = run_safe.call_args.args[0]
    assert "--draft" not in command
    assert "--reviewer" not in command
    assert created.success is True
    assert state.data["pull_request_id"] == 8
    assert state.data["github"]["pull_request_number"] == 8
    advance.assert_called_once_with(8, "https://github.com/o/r/pull/8")


def test_github_adapter_returns_cli_error() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with patch(
        "agentic_devtools.adapters.pull_request_create.run_safe",
        return_value=MagicMock(returncode=1, stdout="", stderr=""),
    ):
        result = GitHubPullRequestCreateAdapter().create(request)

    assert result.success is False
    assert result.error == "gh pr create failed"


def test_github_adapter_ignores_unrelated_diagnostic_urls() -> None:
    """A non-PR diagnostic URL must not be mistaken for an existing pull request."""
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(
        returncode=1,
        stdout="",
        stderr="permission denied: https://example.com/docs/pull/request",
    )

    with patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is False
    assert created.status == "failed"


def test_github_adapter_tracks_existing_pr_reported_on_cli_error() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    url = "https://github.com/o/r/pull/11"
    result = MagicMock(returncode=1, stdout="", stderr=f"an open pull request already exists: {url}")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created"
    assert created.url == url
    assert state.data["pull_request_id"] == 11
    advance.assert_called_once_with(11, url)


def test_github_adapter_tracks_created_pr_url_from_nonzero_cli_result(capsys) -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    url = "https://github.com/o/r/pull/12"
    warning = "failed to add reviewer"
    result = MagicMock(returncode=1, stdout=f"{url}\n", stderr=warning)
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created"
    assert created.url == url
    assert warning in created.error
    assert state.data["pull_request_id"] == 12
    assert state.data["github"]["pull_request_number"] == 12
    advance.assert_called_once_with(12, url)
    assert warning in capsys.readouterr().err


def test_github_adapter_rejects_existing_pr_diagnostic_for_other_repository() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(
        returncode=1,
        stdout="",
        stderr='a pull request for branch "feature" into branch "main" already exists:\nhttps://github.com/other/repo/pull/11',
    )

    with patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is False
    assert created.status == "failed"


def test_github_adapter_returns_indeterminate_on_timeout() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with patch(
        "agentic_devtools.adapters.pull_request_create.run_safe",
        side_effect=subprocess.TimeoutExpired("gh", 60),
    ):
        result = GitHubPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.status == "indeterminate"
    assert result.error == "GitHub pull-request creation outcome is indeterminate: the subprocess timed out"


def test_github_adapter_fails_before_submission_when_repo_is_unresolvable() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with (
        patch.object(GitHubPullRequestCreateAdapter, "_run_gh_create") as run_gh_create,
        patch("agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe", return_value=None),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is False
    assert created.status == "failed"
    assert created.error == "Could not determine GitHub repository for pull-request creation"
    run_gh_create.assert_not_called()


def test_github_adapter_returns_failed_result_when_gh_execution_raises() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with patch("agentic_devtools.adapters.pull_request_create.run_safe", side_effect=FileNotFoundError("gh")):
        result = GitHubPullRequestCreateAdapter().create(request)

    assert result.success is False
    assert result.status == "failed"
    assert result.error == "gh"


def test_github_adapter_returns_failed_result_when_temp_file_creation_raises() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with patch(
        "agentic_devtools.adapters.pull_request_create.tempfile.NamedTemporaryFile",
        side_effect=OSError("no temp file"),
    ):
        result = GitHubPullRequestCreateAdapter().create(request)

    assert result.success is False
    assert result.status == "failed"
    assert result.error == "no temp file"


def test_github_adapter_cleans_up_temp_file_when_write_fails() -> None:
    """The temp file path must be recorded before write(), so a write failure is still cleaned up."""

    class _TempFile:
        name = "/tmp/pr-body.md"

        def __enter__(self) -> _TempFile:
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def write(self, _: str) -> None:
            raise OSError("disk full")

    request = PullRequestCreateRequest("github", "feature", "Title")
    with (
        patch("agentic_devtools.adapters.pull_request_create.tempfile.NamedTemporaryFile", return_value=_TempFile()),
        patch("agentic_devtools.adapters.pull_request_create.Path.unlink") as unlink,
    ):
        result = GitHubPullRequestCreateAdapter().create(request)

    assert result.success is False
    assert result.status == "failed"
    assert "disk full" in result.error
    unlink.assert_called_once_with(missing_ok=True)


def test_github_adapter_skips_cleanup_when_temp_file_path_is_empty() -> None:
    class _TempFile:
        name = ""

        def __enter__(self) -> _TempFile:
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def write(self, _: str) -> None:
            return None

    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/9\n", stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.tempfile.NamedTemporaryFile", return_value=_TempFile()),
        patch("agentic_devtools.adapters.pull_request_create.os.chmod"),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 9
    assert state.data["github"]["pull_request_number"] == 9
    advance.assert_called_once_with(9, "https://github.com/o/r/pull/9")


def test_github_adapter_treats_unparseable_success_output_as_created_untracked(capsys) -> None:
    """A zero exit from `gh pr create` means the remote PR was already created.

    An output URL that fails the parser must not be reported as a failed
    creation -- that would let a caller retry the (background) task and
    create a duplicate PR.
    """
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="created\n", stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created_untracked"
    assert created.url == ""
    assert created.error == "created"
    assert state.data == {}
    advance.assert_not_called()
    assert "did not match the expected repository" in capsys.readouterr().err


def test_github_adapter_unlinks_temp_body_file_after_success() -> None:
    class _TempFile:
        name = "/tmp/pr-body.md"

        def __enter__(self) -> _TempFile:
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def write(self, _: str) -> None:
            return None

    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/10\n", stderr="")
    with (
        patch("agentic_devtools.adapters.pull_request_create.tempfile.NamedTemporaryFile", return_value=_TempFile()),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch("agentic_devtools.adapters.pull_request_create.os.chmod") as chmod,
        patch("agentic_devtools.adapters.pull_request_create.Path.unlink") as unlink,
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state",
            return_value=_RecordingState(),
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation"),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    chmod.assert_called_once_with("/tmp/pr-body.md", 0o600)
    unlink.assert_called_once_with(missing_ok=True)


def test_github_adapter_treats_temp_file_cleanup_failure_as_best_effort() -> None:
    """A cleanup OSError (e.g. Windows sharing violation) must not fail an already-created PR."""

    class _TempFile:
        name = "/tmp/pr-body.md"

        def __enter__(self) -> _TempFile:
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def write(self, _: str) -> None:
            return None

    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/15\n", stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.tempfile.NamedTemporaryFile", return_value=_TempFile()),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch("agentic_devtools.adapters.pull_request_create.os.chmod"),
        patch("agentic_devtools.adapters.pull_request_create.Path.unlink", side_effect=OSError("locked")),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.url == "https://github.com/o/r/pull/15"
    assert state.data["pull_request_id"] == 15
    advance.assert_called_once_with(15, "https://github.com/o/r/pull/15")


def test_github_adapter_accepts_repository_names_with_edge_hyphens() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/octo/-repo-/pull/11\n", stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch("agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe", return_value="octo/-repo-"),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 11
    assert state.data["github"]["pull_request_number"] == 11
    advance.assert_called_once_with(11, "https://github.com/octo/-repo-/pull/11")


def test_github_adapter_ignores_workflow_advancement_failure_after_creation(capsys) -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/12\n", stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation",
            side_effect=RuntimeError("workflow"),
        ),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.url == "https://github.com/o/r/pull/12"
    assert state.data["pull_request_id"] == 12
    assert state.data["github"]["pull_request_number"] == 12
    assert "workflow advancement failed: workflow" in capsys.readouterr().err


def test_github_adapter_reports_success_when_state_persistence_fails(capsys) -> None:
    """A post-creation state-write failure must not be reported as a failed PR creation.

    The remote PR already exists at that point; converting the persistence
    failure into a ``failed``/``invalid`` result would let a caller retry the
    task and create a duplicate PR.
    """
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/14\n", stderr="")
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state",
            side_effect=RuntimeError("lock timeout"),
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created"
    assert created.url == "https://github.com/o/r/pull/14"
    assert "state persistence failed: lock timeout" in capsys.readouterr().err
    advance.assert_called_once_with(14, "https://github.com/o/r/pull/14")


def test_github_adapter_accepts_server_urls_with_path_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    request, state = PullRequestCreateRequest("github", "feature", "Title"), _RecordingState()
    result = MagicMock(returncode=0, stdout="https://example.com/github/o/r/pull/13\n", stderr="")
    monkeypatch.delenv("GH_HOST", raising=False)
    with (
        patch.dict("os.environ", {"GITHUB_SERVER_URL": "https://example.com/github"}),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 13
    assert state.data["github"]["pull_request_number"] == 13
    advance.assert_called_once_with(13, "https://example.com/github/o/r/pull/13")


def test_github_adapter_does_not_track_mismatched_server_url_prefix() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://example.com/other/o/r/pull/13\n", stderr="")
    state = _RecordingState()
    with (
        patch.dict("os.environ", {"GITHUB_SERVER_URL": "https://example.com/github"}),
        patch(
            "agentic_devtools.adapters.pull_request_create.run_safe",
            return_value=result,
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created_untracked"
    assert created.url == ""
    assert created.error == "https://example.com/other/o/r/pull/13"
    assert state.data == {}
    advance.assert_not_called()


def test_github_adapter_does_not_track_extra_path_components() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(stdout="https://github.com/unexpected/o/r/pull/18\n", returncode=0, stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created_untracked"
    assert created.url == ""
    assert created.error == "https://github.com/unexpected/o/r/pull/18"
    assert state.data == {}
    advance.assert_not_called()


def test_github_adapter_does_not_persist_id_from_mismatched_repository_url() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(stdout="https://github.com/other/repo/pull/13\n", returncode=0, stderr="")
    state = _RecordingState()
    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created_untracked"
    assert created.url == ""
    assert created.error == "https://github.com/other/repo/pull/13"
    assert state.data == {}
    advance.assert_not_called()


def test_github_adapter_falls_back_to_gh_host_when_server_url_unset() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://ghe.example.com/o/r/pull/16\n", stderr="")
    state = _RecordingState()
    with (
        patch.dict("os.environ", {"GH_HOST": "ghe.example.com"}, clear=False),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        os.environ.pop("GITHUB_SERVER_URL", None)
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 16
    advance.assert_called_once_with(16, "https://ghe.example.com/o/r/pull/16")


def test_github_adapter_tracks_canonical_url_with_mixed_case_host_and_repository() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://ghe.example.com/O/R/pull/17\n", stderr="")
    state = _RecordingState()
    with (
        patch.dict("os.environ", {"GH_HOST": "GHE.EXAMPLE.COM"}, clear=False),
        patch("agentic_devtools.adapters.pull_request_create.resolve_github_repo_safe", return_value="o/r"),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        os.environ.pop("GITHUB_SERVER_URL", None)
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert created.status == "created"
    assert state.data["pull_request_id"] == 17
    assert state.data["github"]["pull_request_number"] == 17
    advance.assert_called_once_with(17, "https://ghe.example.com/O/R/pull/17")


def test_github_adapter_defaults_to_github_com_without_server_url_or_gh_host() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/17\n", stderr="")
    state = _RecordingState()
    with (
        patch.dict("os.environ", {}, clear=False),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        os.environ.pop("GITHUB_SERVER_URL", None)
        os.environ.pop("GH_HOST", None)
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 17
    advance.assert_called_once_with(17, "https://github.com/o/r/pull/17")


def test_github_adapter_accepts_custom_server_url_without_path_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    request, state = PullRequestCreateRequest("github", "feature", "Title"), _RecordingState()
    result = MagicMock(returncode=0, stdout="https://example.com/o/r/pull/14\n", stderr="")
    monkeypatch.delenv("GH_HOST", raising=False)
    with (
        patch.dict("os.environ", {"GITHUB_SERVER_URL": "https://example.com"}),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 14
    assert state.data["github"]["pull_request_number"] == 14
    advance.assert_called_once_with(14, "https://example.com/o/r/pull/14")


def test_github_adapter_uses_gh_host_when_set() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.enterprise.example/o/r/pull/15\n", stderr="")
    state = _RecordingState()
    with (
        patch.dict("os.environ", {"GH_HOST": "github.enterprise.example"}, clear=False),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation") as advance,
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 15
    advance.assert_called_once_with(15, "https://github.enterprise.example/o/r/pull/15")


def test_github_adapter_gh_host_takes_precedence_over_github_server_url() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    result = MagicMock(returncode=0, stdout="https://github.enterprise.example/o/r/pull/16\n", stderr="")
    state = _RecordingState()
    with (
        patch.dict(
            "os.environ",
            {"GH_HOST": "github.enterprise.example", "GITHUB_SERVER_URL": "https://github.com"},
            clear=False,
        ),
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state", return_value=state
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation"),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    assert state.data["pull_request_id"] == 16


def test_github_adapter_persists_identifiers_atomically_and_preserves_github_section(
    temp_state_dir, clear_state_before
) -> None:
    """Both identifiers are written under one lock, and other `github.*` keys survive."""
    from agentic_devtools import state

    state.set_value("github.repo_full_name", "octo/repo")

    request = PullRequestCreateRequest("github", "feature", "Title", "Body", "main", True, ())
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/42\n", stderr="")

    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation"),
        patch(
            "agentic_devtools.state._sync_bootstrap_for_context_key",
            wraps=state._sync_bootstrap_for_context_key,
        ) as sync_bootstrap,
        patch("agentic_devtools.state._update_bootstrap_worktree_key"),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    final_state = state.load_state()
    assert final_state["pull_request_id"] == 42
    assert final_state["github"]["pull_request_number"] == 42
    assert final_state["github"]["repo_full_name"] == "octo/repo"
    sync_bootstrap.assert_called_once_with("pull_request_id", 42, final_state, apply_update=False)


def test_github_adapter_migrates_state_before_publishing_worktree_key(tmp_path, monkeypatch) -> None:
    """When `_sync_bootstrap_for_context_key` moves the active worktree key mid-flight.

    (as it does for a direct invocation with no issue key set), the just-persisted
    identifiers must not be stranded in the directory resolved before the switch.
    """
    agdt_dir = tmp_path / ".agdt"
    agdt_dir.mkdir()
    (agdt_dir / "identity.json").write_text('{"identity": "test", "email": ""}', encoding="utf-8")
    (agdt_dir / "runtime-bootstrap.json").write_text("{}", encoding="utf-8")
    old_dir = agdt_dir / "workflows" / "_unscoped"
    old_dir.mkdir(parents=True)
    (old_dir / "state.json").write_text('{"workflow": {"step": "pull-request"}}', encoding="utf-8")
    destination_dir = agdt_dir / "workflows" / "test" / "PR42"
    destination_dir.mkdir(parents=True)
    (destination_dir / "state.json").write_text('{"github": {"pull_request_number": 7}}', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    request = PullRequestCreateRequest("github", "feature", "Title", "Body", "main", True, ())
    result = MagicMock(returncode=0, stdout="https://github.com/o/r/pull/42\n", stderr="")

    with (
        patch("agentic_devtools.adapters.pull_request_create.run_safe", return_value=result),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation"),
        patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path),
    ):
        created = GitHubPullRequestCreateAdapter().create(request)

    assert created.success is True
    bootstrap = json.loads((agdt_dir / "runtime-bootstrap.json").read_text(encoding="utf-8"))
    migrated = json.loads((agdt_dir / "workflows" / "test" / "PR42" / "state.json").read_text(encoding="utf-8"))
    assert bootstrap["worktree_key"] == "PR42"
    assert migrated["workflow"] == {"step": "pull-request"}
    assert migrated["pull_request_id"] == 42
    assert migrated["github"]["pull_request_number"] == 42
