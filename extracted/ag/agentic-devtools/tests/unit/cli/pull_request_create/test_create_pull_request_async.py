import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli import pull_request_create


def test_create_pull_request_async_starts_background_task(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info") as print_info,
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="Title")

    run_task.assert_called_once()
    func_kwargs = run_task.call_args.kwargs["func_kwargs"]
    assert set(func_kwargs) == {"request_file", "state_dir"}
    snapshot_path = func_kwargs["request_file"]
    assert snapshot_path.startswith(str(tmp_path))
    assert snapshot_path.endswith(".json")
    assert func_kwargs["state_dir"] == str(tmp_path)
    print_info.assert_called_once_with("task", "Creating pull request")


def test_create_pull_request_async_does_not_call_build_create_request_before_backgrounding(tmp_path) -> None:
    """The foreground path snapshots resolved inputs without invoking the full request builder."""
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task"),
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
        patch.object(pull_request_create, "build_create_request") as build_request,
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="Title")

    build_request.assert_not_called()


def test_create_pull_request_async_writes_raw_overrides_to_snapshot_file(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(
            provider="github",
            source_branch="feature",
            title="Title",
            body="A" * 5000,
            reviewers=["alice", "bob"],
        )

    snapshot_path = run_task.call_args.kwargs["func_kwargs"]["request_file"]
    saved = json.loads(pull_request_create.Path(snapshot_path).read_text(encoding="utf-8"))
    assert saved["provider"] == "github"
    assert saved["source_branch"] == "feature"
    assert saved["body"] == "A" * 5000
    assert saved["reviewers"] == ["alice", "bob"]


def test_create_pull_request_async_persists_explicit_provider_when_unconfigured(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create._resolve_configured_provider", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value") as save,
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task"),
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(
            provider="github",
            source_branch="feature",
            title="Title",
        )

    save.assert_any_call("platform.code_hosting", "github")


def test_create_pull_request_async_normalizes_list_reviewers_before_snapshotting(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(
            source_branch="feature",
            title="Title",
            reviewers=[" alice,bob ", "carol "],
        )

    snapshot_path = run_task.call_args.kwargs["func_kwargs"]["request_file"]
    saved = json.loads(pull_request_create.Path(snapshot_path).read_text(encoding="utf-8"))
    assert saved["reviewers"] == ["alice", "bob", "carol"]


def test_create_pull_request_async_restricts_snapshot_permissions(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="Title")

    snapshot_path = pull_request_create.Path(run_task.call_args.kwargs["func_kwargs"]["request_file"])
    assert snapshot_path.stat().st_mode & 0o777 == 0o600


def test_create_pull_request_async_removes_snapshot_when_task_launch_fails(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch(
            "agentic_devtools.cli.pull_request_create.run_function_in_background",
            side_effect=RuntimeError("spawn failed"),
        ),
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        with pytest.raises(RuntimeError, match="spawn failed"):
            pull_request_create.create_pull_request_async(source_branch="feature", title="Title")

    snapshot_dir = tmp_path / "pending-pr-requests"
    assert list(snapshot_dir.glob("*.json")) == []


def test_create_pull_request_async_ignores_snapshot_cleanup_failure_on_launch_error(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch(
            "agentic_devtools.cli.pull_request_create.run_function_in_background",
            side_effect=RuntimeError("spawn failed"),
        ),
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_create.Path.unlink", side_effect=OSError),
    ):
        with pytest.raises(RuntimeError, match="spawn failed"):
            pull_request_create.create_pull_request_async(source_branch="feature", title="Title")


def test_create_pull_request_async_ignores_snapshot_chmod_failure(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.os.chmod", side_effect=OSError),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="Title")

    run_task.assert_called_once()


def test_create_pull_request_async_snapshots_effective_state_backed_values(tmp_path) -> None:
    values = {
        "platform.code_hosting": "github",
        "source_branch": "feature",
        "title": "Title",
        "description": "Body",
        "target_branch": "develop",
        "draft": "false",
        "reviewers": "alice,bob",
    }
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", side_effect=values.get),
        patch("agentic_devtools.cli.pull_request_create.is_dry_run", return_value=True),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async()

    snapshot_path = run_task.call_args.kwargs["func_kwargs"]["request_file"]
    saved = json.loads(pull_request_create.Path(snapshot_path).read_text(encoding="utf-8"))
    assert saved == {
        "provider": "github",
        "source_branch": "feature",
        "title": "Title",
        "body": "Body",
        "body_is_explicit": True,
        "target_branch": "develop",
        "draft": False,
        "reviewers": ["alice", "bob"],
        "dry_run": True,
    }


def test_create_pull_request_async_snapshots_rendered_template_body(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
        patch("agentic_devtools.cli.pull_request_create.set_value"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="Title")

    snapshot_path = run_task.call_args.kwargs["func_kwargs"]["request_file"]
    saved = json.loads(pull_request_create.Path(snapshot_path).read_text(encoding="utf-8"))
    assert saved["body"] == "Template body"


def test_create_pull_request_async_preserves_formatted_title_override(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template body"),
        patch("agentic_devtools.cli.pull_request_create.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task") as run_task,
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="feat(#42): add new feature")

    snapshot_path = run_task.call_args.kwargs["func_kwargs"]["request_file"]
    saved = json.loads(pull_request_create.Path(snapshot_path).read_text(encoding="utf-8"))
    assert saved["title"] == "feat(#42): add new feature"
    assert ("title", "feat(#42): add new feature") in [call.args for call in set_value.call_args_list]


def test_create_pull_request_async_persists_explicit_overrides(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task"),
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_create.set_value") as set_value,
    ):
        pull_request_create.create_pull_request_async(source_branch="feature", title="Title", body="Body")

    assert set_value.call_args_list == [
        (("source_branch", "feature"),),
        (("title", "Title"),),
        (("description", "Body"),),
    ]


def test_create_pull_request_async_skips_persisting_unset_overrides(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.resolve_pr_body", return_value="Template"),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background", return_value="task"),
        patch("agentic_devtools.cli.pull_request_create.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_create.set_value") as set_value,
        patch(
            "agentic_devtools.cli.pull_request_create.get_value",
            side_effect=lambda key: {"source_branch": "feature", "title": "Title"}.get(key),
        ),
    ):
        pull_request_create.create_pull_request_async()

    set_value.assert_not_called()


def test_create_pull_request_async_raises_before_scheduling_task_on_invalid_request(tmp_path) -> None:
    """An invalid request must fail synchronously instead of only inside the background task."""
    with (
        patch("agentic_devtools.cli.pull_request_create.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_create.run_function_in_background") as run_task,
        patch("agentic_devtools.cli.pull_request_create.set_value") as set_value,
        patch(
            "agentic_devtools.cli.pull_request_create.get_value",
            return_value=None,
        ),
    ):
        with pytest.raises(ValueError, match="title is required"):
            pull_request_create.create_pull_request_async(source_branch="feature")

    run_task.assert_not_called()
    set_value.assert_not_called()
