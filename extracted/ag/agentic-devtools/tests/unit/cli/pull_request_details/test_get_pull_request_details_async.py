from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_details import get_pull_request_details_async


def test_get_pull_request_details_async_queues_task(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info") as print_info,
    ):
        transaction.return_value.__enter__.return_value = {}
        get_pull_request_details_async()
    run.assert_called_once()
    func_kwargs = run.call_args.kwargs["func_kwargs"]
    request_id = func_kwargs.pop("request_id")
    assert request_id
    assert func_kwargs == {
        "state": {"_pull_request_details_request_id": request_id},
        "state_snapshot": True,
    }
    assert run.call_args.kwargs["state_dir"] == str(tmp_path)
    print_info.assert_called_once_with("task", "Getting pull request details")


def test_get_pull_request_details_async_forwards_overrides_as_func_kwargs(tmp_path) -> None:
    """Explicit overrides must be forwarded so they outrank a stale persisted ``provider``."""
    state = {"organization": "org", "project": "project", "dry_run": True, "content": "x" * 100_000}
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details_async(provider="github", pull_request_id=7, repository="o/r")
    assert run.call_args.kwargs["func_kwargs"] == {
        "provider": "github",
        "pull_request_id": 7,
        "repository": "o/r",
        "state": {
            "organization": "org",
            "project": "project",
            "dry_run": True,
            "provider": "github",
            "platform": {"code_hosting": "github"},
            "pull_request_id": 7,
            "sourceCodeHostingPlatform": {"pullRequest": {"repository": "o/r"}},
            "_pull_request_details_request_id": run.call_args.kwargs["func_kwargs"]["request_id"],
        },
        "state_snapshot": True,
        "request_id": run.call_args.kwargs["func_kwargs"]["request_id"],
    }
    assert run.call_args.kwargs["state_dir"] == str(tmp_path)


def test_get_pull_request_details_async_forwards_only_resolution_state() -> None:
    state = {
        "provider": "github",
        "platform": {"other": "retained"},
        "sourceCodeHostingPlatform": {
            "other": "retained",
            "pullRequest": {"other": "retained"},
        },
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details_async(provider="github", repository="o/r")

    worker_state = run.call_args.kwargs["func_kwargs"]["state"]
    assert worker_state["platform"] == {"code_hosting": "github"}
    assert worker_state["sourceCodeHostingPlatform"] == {"pullRequest": {"repository": "o/r"}}
    assert set(worker_state) == {
        "provider",
        "platform",
        "sourceCodeHostingPlatform",
        "_pull_request_details_request_id",
    }


def test_get_pull_request_details_async_sanitizes_repository_aliases_on_provider_switch() -> None:
    state = {
        "provider": "azure_devops",
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "old/canonical"}},
        "azure_devops": {"repository": "old/legacy"},
        "repository": "old/generic",
        "github": {"repo": "target/saved"},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details_async(provider="github")

    worker_state = run.call_args.kwargs["func_kwargs"]["state"]
    assert "repository" not in worker_state
    assert "sourceCodeHostingPlatform" not in worker_state
    assert "azure_devops" not in worker_state
    assert worker_state["github"]["repo"] == "target/saved"
    assert worker_state["provider"] == "github"
    assert worker_state["platform"]["code_hosting"] == "github"
    assert run.call_args.kwargs["func_kwargs"]["state_snapshot"] is True


def test_get_pull_request_details_async_preserves_nested_azure_configuration() -> None:
    state = {
        "provider": "azure_devops",
        "azure_devops": {
            "organization": "https://dev.azure.com/example",
            "project": "Example Project",
        },
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details_async()

    worker_state = run.call_args.kwargs["func_kwargs"]["state"]
    assert worker_state["azure_devops"] == {
        "organization": "https://dev.azure.com/example",
        "project": "Example Project",
    }
    assert worker_state["organization"] == "https://dev.azure.com/example"
    assert worker_state["project"] == "Example Project"


def test_get_pull_request_details_async_prefers_top_level_azure_configuration() -> None:
    state = {
        "provider": "azure_devops",
        "organization": "https://dev.azure.com/top-level",
        "project": "Top-level Project",
        "azure_devops": {
            "organization": "https://dev.azure.com/nested",
            "project": "Nested Project",
        },
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details_async()

    worker_state = run.call_args.kwargs["func_kwargs"]["state"]
    assert worker_state["organization"] == "https://dev.azure.com/top-level"
    assert worker_state["project"] == "Top-level Project"
    assert worker_state["azure_devops"] == {
        "organization": "https://dev.azure.com/nested",
        "project": "Nested Project",
    }


def test_get_pull_request_details_async_promotes_nested_config_over_blank_top_level_values() -> None:
    state = {
        "provider": "azure_devops",
        "organization": None,
        "project": "  ",
        "azure_devops": {
            "organization": "https://dev.azure.com/example",
            "project": "Example Project",
        },
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details_async()

    worker_state = run.call_args.kwargs["func_kwargs"]["state"]
    assert worker_state["organization"] == "https://dev.azure.com/example"
    assert worker_state["project"] == "Example Project"


def test_get_pull_request_details_async_handles_missing_or_malformed_repository_aliases() -> None:
    states = [
        {"provider": "azure_devops"},
        {
            "provider": "azure_devops",
            "sourceCodeHostingPlatform": {"pullRequest": "malformed"},
            "azure_devops": "malformed",
        },
    ]
    for state in states:
        with (
            patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
            patch("agentic_devtools.cli.pull_request_details.run_function_in_background", return_value="task") as run,
            patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
        ):
            transaction.return_value.__enter__.return_value = state
            get_pull_request_details_async(provider="github")
        worker_state = run.call_args.kwargs["func_kwargs"]["state"]
        assert worker_state["provider"] == "github"
        assert worker_state["platform"]["code_hosting"] == "github"


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"pull_request_id": 0}, "pull_request_id"),
        ({"pull_request_id": True}, "pull_request_id"),
        ({"repository": "invalid"}, "owner/repo"),
        ({"repository": ""}, "non-empty string"),
        ({"repository": 42}, "non-empty string"),
    ],
)
def test_get_pull_request_details_async_rejects_invalid_overrides_before_persisting(overrides, error) -> None:
    state = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.run_function_in_background") as run,
        patch("agentic_devtools.cli.pull_request_details.print_task_tracking_info"),
    ):
        transaction.return_value.__enter__.return_value = state
        with pytest.raises(ValueError, match=error):
            get_pull_request_details_async(**overrides)

    assert state == {"provider": "github"}
    run.assert_not_called()
