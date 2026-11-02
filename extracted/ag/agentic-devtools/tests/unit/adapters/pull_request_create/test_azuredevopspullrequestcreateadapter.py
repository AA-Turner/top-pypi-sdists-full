from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.adapters.pull_request_create import (
    _AZURE_BRIDGE_LOCK_TIMEOUT_SECONDS,
    _AZURE_CLI_TIMEOUT_SECONDS,
    AzureDevOpsPullRequestCreateAdapter,
    PullRequestCreateRequest,
)
from agentic_devtools.cli.azure_devops.commands import PullRequestCreationPostSubmitError

_BRIDGED_KEYS = {"source_branch", "title", "description", "target_branch", "draft", "reviewers", "dry_run"}


def test_azure_adapter_delegates_to_existing_command(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", "Body", "main", False, ())

    with patch("agentic_devtools.adapters.pull_request_create.azure_create_pull_request") as create:
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.provider == "azure_devops"
    assert result.status == "created"
    create.assert_called_once()
    assert create.call_args.kwargs["timeout"] == _AZURE_CLI_TIMEOUT_SECONDS
    assert create.call_args.kwargs["title"] == "Title"
    assert create.call_args.kwargs["title_is_rendered"] is True
    assert callable(create.call_args.kwargs["on_pull_request_created"])
    # Bridged keys never existed before the call, so they are cleaned up afterwards.
    final_state = state.load_state()
    assert not (_BRIDGED_KEYS & final_state.keys())


def test_azure_adapter_rejects_github_request_before_dry_run() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title", dry_run=True)

    with patch("agentic_devtools.adapters.pull_request_create._bridge_lock_path") as lock_path:
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    lock_path.assert_not_called()
    assert result.success is False
    assert result.provider == "github"
    assert result.status == "failed"
    assert result.error == "provider mismatch"


def test_azure_adapter_returns_legacy_command_url(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")

    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        return_value="https://dev.azure.com/org/project/_git/repo/pullrequest/42",
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.url == "https://dev.azure.com/org/project/_git/repo/pullrequest/42"


def test_azure_adapter_translates_timeout(temp_state_dir, clear_state_before) -> None:
    import subprocess

    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=subprocess.TimeoutExpired("az", 60),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.status == "indeterminate"
    assert result.error == "Azure DevOps pull-request creation outcome is indeterminate: the subprocess timed out"


def test_azure_adapter_passes_request_fields_directly_to_legacy_command(temp_state_dir, clear_state_before) -> None:
    """Concurrent state changes cannot replace the request passed to Azure."""
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", "Body", "main", False, ("carol",))

    seen: dict[str, object] = {}

    def _capture(**kwargs: object) -> None:
        seen.update(kwargs)
        for key in _BRIDGED_KEYS:
            state.set_value(key, f"concurrent {key} update")

    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=_capture,
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert {key: seen[key] for key in _BRIDGED_KEYS} == {
        "source_branch": "feature",
        "title": "Title",
        "description": "Body",
        "target_branch": "main",
        "draft": False,
        "reviewers": "carol",
        "dry_run": False,
    }
    assert all(state.get_value(key) == f"concurrent {key} update" for key in _BRIDGED_KEYS)


def test_azure_adapter_passes_generated_body_directly(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest(
        "azure_devops",
        "feature",
        "Title",
        "Generated body",
        body_is_explicit=False,
    )

    seen: dict[str, object] = {}

    def _capture(**kwargs: object) -> None:
        seen.update(kwargs)

    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=_capture,
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert seen["description"] == "Generated body"


def test_azure_adapter_leaves_preexisting_state_unchanged(temp_state_dir, clear_state_before) -> None:
    """Azure request arguments do not overwrite existing state values."""
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", "Generated body", "main", False, ())
    previous_values = {
        "source_branch": "old-branch",
        "title": "Old title",
        "description": "Explicit override",
        "target_branch": "develop",
        "draft": True,
        "reviewers": "carol",
        "dry_run": False,
    }
    for key, value in previous_values.items():
        state.set_value(key, value)

    with patch("agentic_devtools.adapters.pull_request_create.azure_create_pull_request"):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    final_state = state.load_state()
    for key, value in previous_values.items():
        assert final_state[key] == value


def test_azure_adapter_does_not_clobber_concurrent_state_change(temp_state_dir, clear_state_before) -> None:
    """A key changed by another task while the legacy command runs is left alone."""
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", dry_run=False)

    def _concurrent_update(**kwargs: object) -> None:
        # Simulate another background task changing "title" while this
        # adapter's legacy command is still running.
        state.set_value("title", "Changed by another task")

    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=_concurrent_update,
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert state.get_value("title") == "Changed by another task"


def test_azure_adapter_returns_dry_run_status(temp_state_dir, clear_state_before, capsys) -> None:
    request = PullRequestCreateRequest(
        "azure_devops", "feature", "Title", "Body", "main", False, ("carol",), dry_run=True
    )
    state.set_value("title", "Existing title")
    state.set_value("dry_run", False)
    result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.status == "dry_run"
    assert state.load_state()["title"] == "Existing title"
    assert state.load_state()["dry_run"] is False
    output = capsys.readouterr().out
    assert "Description: Body" in output
    assert "Reviewers: carol" in output


def test_azure_adapter_dry_run_omits_empty_optional_fields(temp_state_dir, clear_state_before, capsys) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", dry_run=True)

    result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.status == "dry_run"
    output = capsys.readouterr().out
    assert "Description:" not in output
    assert "Reviewers:" not in output


def test_azure_adapter_handles_command_failure(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=RuntimeError("failure"),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is False
    assert result.error == "failure"
    final_state = state.load_state()
    assert not (_BRIDGED_KEYS & final_state.keys())


def test_azure_adapter_handles_system_exit(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with patch("agentic_devtools.adapters.pull_request_create.azure_create_pull_request", side_effect=SystemExit(1)):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.status == "failed"
    assert result.error == "exit status 1"
    final_state = state.load_state()
    assert not (_BRIDGED_KEYS & final_state.keys())


def test_azure_adapter_leaves_state_unchanged_when_command_is_interrupted(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    state.set_value("title", "Original title")

    with (
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            side_effect=KeyboardInterrupt,
        ),
        pytest.raises(KeyboardInterrupt),
    ):
        AzureDevOpsPullRequestCreateAdapter().create(request)

    final_state = state.load_state()
    assert final_state["title"] == "Original title"
    assert not ((_BRIDGED_KEYS - {"title"}) & final_state.keys())


def test_azure_adapter_marks_post_submit_failure_indeterminate(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=PullRequestCreationPostSubmitError("response could not be parsed"),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.status == "indeterminate"
    assert result.error == "response could not be parsed"
    final_state = state.load_state()
    assert not (_BRIDGED_KEYS & final_state.keys())


def test_azure_adapter_persists_pr_id_after_post_submit_failure(temp_state_dir, clear_state_before) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")

    def _create_then_fail(**kwargs: object) -> None:
        callback = kwargs["on_pull_request_created"]
        assert callable(callback)
        callback(42)
        raise PullRequestCreationPostSubmitError("workflow advancement failed")

    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=_create_then_fail,
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.status == "indeterminate"
    assert result.error == "workflow advancement failed"
    final_state = state.load_state()
    assert final_state["pull_request_id"] == 42
    assert not (_BRIDGED_KEYS & final_state.keys())


def test_azure_bridge_lock_timeout_covers_all_subprocess_budgets() -> None:
    assert _AZURE_BRIDGE_LOCK_TIMEOUT_SECONDS >= 3 * _AZURE_CLI_TIMEOUT_SECONDS + 30


def test_azure_adapter_serializes_concurrent_legacy_invocations(temp_state_dir, clear_state_before) -> None:
    """Two concurrent Azure creations remain serialized through state persistence."""
    import threading
    import time

    active = 0
    max_active = 0
    guard = threading.Lock()

    def _slow_legacy_call(**kwargs: object) -> None:
        nonlocal active, max_active
        with guard:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.05)
        with guard:
            active -= 1

    def _run(title: str) -> None:
        request = PullRequestCreateRequest("azure_devops", "feature", title, dry_run=False)
        AzureDevOpsPullRequestCreateAdapter().create(request)

    with patch(
        "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
        side_effect=_slow_legacy_call,
    ):
        threads = [threading.Thread(target=_run, args=(f"Title {i}",), daemon=True) for i in range(3)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)

    assert all(not thread.is_alive() for thread in threads)
    assert max_active == 1


def test_azure_adapter_treats_state_persistence_failure_as_non_fatal_when_creation_succeeded(
    temp_state_dir, clear_state_before, capsys
) -> None:
    """A persistence failure must not turn remote creation into a retryable failure."""
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", "Body", "main", False, (), dry_run=False)

    def _create(**kwargs: object) -> str:
        callback = kwargs["on_pull_request_created"]
        assert callable(callback)
        callback(42)
        return "https://dev.azure.com/org/project/_git/repo/pullrequest/42"

    with (
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            side_effect=_create,
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state",
            side_effect=RuntimeError("disk full"),
        ),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.status == "created"
    assert "state persistence/migration failed" in capsys.readouterr().err


def test_azure_adapter_preserves_original_failure_when_state_persistence_also_fails(
    temp_state_dir, clear_state_before, capsys
) -> None:
    """When creation fails, a state persistence failure must not mask the real error."""
    request = PullRequestCreateRequest("azure_devops", "feature", "Title", dry_run=False)

    def _create_then_fail(**kwargs: object) -> None:
        callback = kwargs["on_pull_request_created"]
        assert callable(callback)
        callback(42)
        raise RuntimeError("create failed")

    with (
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            side_effect=_create_then_fail,
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.read_modify_write_state",
            side_effect=RuntimeError("disk full"),
        ),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is False
    assert result.error == "create failed"
    assert "state persistence/migration failed" in capsys.readouterr().err


def test_azure_adapter_migrates_stranded_state_after_worktree_key_switch(tmp_path) -> None:
    """A mid-flight worktree-key switch must not strand state in the old directory."""
    import json

    old_dir = tmp_path / "ISSUE-1"
    new_dir = tmp_path / "PR42"
    old_dir.mkdir()
    new_dir.mkdir()
    (old_dir / "state.json").write_text("{}", encoding="utf-8")
    (new_dir / "state.json").write_text("{}", encoding="utf-8")

    def _switch_worktree(**kwargs: object) -> str:
        # Simulate state left behind in the old directory as the created PR
        # becomes the active worktree context.
        (old_dir / "state.json").write_text(
            json.dumps({"pull_request_id": 42, "workflow_marker": "left-behind"}),
            encoding="utf-8",
        )
        callback = kwargs["on_pull_request_created"]
        assert callable(callback)
        callback(42)
        return "https://dev.azure.com/org/project/_git/repo/pullrequest/42"

    get_state_dir_calls = 0

    def _get_state_dir() -> Path:
        nonlocal get_state_dir_calls
        get_state_dir_calls += 1
        return old_dir if get_state_dir_calls == 1 else new_dir

    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with (
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.get_state_dir",
            side_effect=_get_state_dir,
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            side_effect=_switch_worktree,
        ),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    new_data = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert new_data.get("workflow_marker") == "left-behind"


def test_azure_adapter_migrates_state_without_bridged_request_values(tmp_path, monkeypatch) -> None:
    """The new PR worktree must receive the cleaned state, not bridge-only values."""
    import json

    agdt_dir = tmp_path / ".agdt"
    agdt_dir.mkdir()
    (agdt_dir / "identity.json").write_text('{"identity": "test", "email": ""}', encoding="utf-8")
    (agdt_dir / "runtime-bootstrap.json").write_text("{}", encoding="utf-8")
    old_dir = agdt_dir / "workflows" / "_unscoped"
    old_dir.mkdir(parents=True)
    (old_dir / "state.json").write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    def _capture_pr_id(**kwargs: object) -> str:
        callback = kwargs["on_pull_request_created"]
        assert callable(callback)
        callback(42)
        return "https://dev.azure.com/org/project/_git/repo/pullrequest/42"

    request = PullRequestCreateRequest("azure_devops", "feature", "Title", "Body", "main", False, ("alice",))
    with (
        patch("agentic_devtools.state._get_git_repo_root", return_value=tmp_path),
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            side_effect=_capture_pr_id,
        ),
        patch("agentic_devtools.adapters.pull_request_create.try_advance_workflow_after_pr_creation"),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    migrated = json.loads((agdt_dir / "workflows" / "test" / "PR42" / "state.json").read_text(encoding="utf-8"))
    assert migrated["pull_request_id"] == 42
    assert not (_BRIDGED_KEYS & migrated.keys())


def test_azure_adapter_does_not_migrate_state_to_an_unrelated_context(tmp_path) -> None:
    """A concurrent context switch unrelated to the created PR must not copy old state."""
    import json

    old_dir = tmp_path / "ISSUE-1"
    other_dir = tmp_path / "ISSUE-2"
    old_dir.mkdir()
    other_dir.mkdir()
    (old_dir / "state.json").write_text(
        json.dumps({"pull_request_id": 42, "workflow_marker": "left-behind"}),
        encoding="utf-8",
    )
    (other_dir / "state.json").write_text("{}", encoding="utf-8")

    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with (
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.get_state_dir",
            side_effect=[old_dir, other_dir],
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            return_value="https://dev.azure.com/org/project/_git/repo/pullrequest/42",
        ),
    ):
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert json.loads((other_dir / "state.json").read_text(encoding="utf-8")) == {}


def test_azure_adapter_survives_post_creation_cleanup_failure(temp_state_dir, clear_state_before, capsys) -> None:
    """A state migration failure must not destroy a successful creation.

    By the time the `finally` block runs, `azure_create_pull_request()` has
    already created the remote PR, so a filesystem error in migration must be
    surfaced as a non-fatal warning instead of replacing the successful result.
    """
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    state.save_state({"pull_request_id": 42})
    created_pr_dir = temp_state_dir.with_name("PR42")

    def _create(**kwargs: object) -> str:
        callback = kwargs["on_pull_request_created"]
        assert callable(callback)
        callback(42)
        return "https://dev.azure.com/org/project/_git/repo/pullrequest/42"

    get_state_dir_calls = 0

    def _get_state_dir() -> Path:
        nonlocal get_state_dir_calls
        get_state_dir_calls += 1
        return temp_state_dir if get_state_dir_calls == 1 else created_pr_dir

    with (
        patch(
            "agentic_devtools.adapters.pull_request_create.azure_create_pull_request",
            side_effect=_create,
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create._migrate_state_dir",
            side_effect=OSError("disk full"),
        ),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.get_state_dir",
            side_effect=_get_state_dir,
        ),
    ):
        created_pr_dir.mkdir()
        result = AzureDevOpsPullRequestCreateAdapter().create(request)

    assert result.success is True
    assert result.url == "https://dev.azure.com/org/project/_git/repo/pullrequest/42"
    assert "state persistence/migration failed" in capsys.readouterr().err
