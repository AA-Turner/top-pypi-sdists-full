from unittest.mock import patch

from agentic_devtools.cli.pull_request_threads import get_pull_request_threads_async


def test_starts_background_task() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=4),
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch(
            "agentic_devtools.cli.pull_request_threads._thread_listing_repository",
            return_value="owner/repo",
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value="task"
        ) as task_runner,
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        get_pull_request_threads_async()
    assert task_runner.call_args.kwargs["func_kwargs"] == {
        "pull_request_id": 4,
        "provider": "github",
        "repository": "owner/repo",
    }


def test_missing_pull_request_id_exits() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        try:
            get_pull_request_threads_async()
        except SystemExit as exc:
            assert exc.code == 1
        else:
            raise AssertionError("expected SystemExit")


def test_parses_pull_request_id_from_argv() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads", "-p", "4"]),
        patch("agentic_devtools.cli.pull_request_threads.set_value") as set_value,
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value="task"
        ) as task_runner,
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch(
            "agentic_devtools.cli.pull_request_threads._thread_listing_repository",
            return_value="owner/repo",
        ),
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
    ):
        get_pull_request_threads_async()
    assert task_runner.call_args.kwargs["func_kwargs"] == {
        "pull_request_id": 4,
        "provider": "github",
        "repository": "owner/repo",
    }
    set_value.assert_called_once_with("pull_request_id", 4)


def test_falls_back_to_legacy_azure_context_before_queuing() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.get_value", side_effect=[4, None]),
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            return_value="azure_devops",
        ) as resolve_provider,
        patch(
            "agentic_devtools.cli.pull_request_threads._azure_devops_context",
            return_value=("https://dev.azure.com/org", "MyProject", "repo"),
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value="task"
        ) as task_runner,
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        get_pull_request_threads_async()
    assert task_runner.call_args.kwargs["func_kwargs"] == {
        "pull_request_id": 4,
        "provider": "azure_devops",
        "repository": "repo",
        "organization": "https://dev.azure.com/org",
        "project": "MyProject",
    }
    resolve_provider.assert_called_once_with(None, allow_legacy_azure_fallback=True)


def test_queues_root_azure_devops_coordinates() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.get_value",
            side_effect=lambda key: 4 if key == "pull_request_id" else None,
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_workflow_state", return_value={}),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={
                "code_hosting": "other",
                "azure_devops": {
                    "organization": "https://dev.azure.com/configured-org",
                    "project": "ConfiguredProject",
                    "repository": "configured-repo",
                },
            },
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_repo_config",
            return_value={
                "platform": {
                    "azure_devops": {
                        "organization": "https://dev.azure.com/configured-org",
                        "project": "ConfiguredProject",
                        "repository": "configured-repo",
                    }
                }
            },
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value="task"
        ) as task_runner,
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        get_pull_request_threads_async()

    assert task_runner.call_args.kwargs["func_kwargs"] == {
        "pull_request_id": 4,
        "provider": "azure_devops",
        "repository": "configured-repo",
        "organization": "https://dev.azure.com/configured-org",
        "project": "ConfiguredProject",
    }


def test_resolves_explicit_azure_repository_before_queuing() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads._azure_devops_context",
            return_value=("https://dev.azure.com/org", "project", "repo"),
        ) as resolve_context,
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value="task"
        ) as task_runner,
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        get_pull_request_threads_async("4", provider="azure_devops", repository="repo")

    resolve_context.assert_called_once_with("repo")
    assert task_runner.call_args.kwargs["func_kwargs"] == {
        "pull_request_id": 4,
        "provider": "azure_devops",
        "repository": "repo",
        "organization": "https://dev.azure.com/org",
        "project": "project",
    }


def test_resolves_explicit_repository_before_queuing() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            return_value="github",
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads._repository",
            return_value="owner/repo",
        ) as resolve_repository,
        patch(
            "agentic_devtools.cli.pull_request_threads.run_function_in_background", return_value="task"
        ) as task_runner,
        patch("agentic_devtools.cli.pull_request_threads.print_task_tracking_info"),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        get_pull_request_threads_async("4", repository="owner/repo")
    resolve_repository.assert_called_once_with("github", "owner/repo")
    assert task_runner.call_args.kwargs["func_kwargs"] == {
        "pull_request_id": 4,
        "provider": "github",
        "repository": "owner/repo",
    }


def test_rejects_invalid_explicit_provider_before_queuing() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            side_effect=ValueError("bad provider"),
        ),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        try:
            get_pull_request_threads_async("4", provider="bitbucket")
        except SystemExit as exc:
            assert exc.code == 1
        else:
            raise AssertionError("expected SystemExit")


def test_rejects_malformed_configured_provider_before_queuing() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.get_value",
            side_effect=[4, 123],
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            side_effect=ValueError("bad provider"),
        ),
        patch("agentic_devtools.cli.pull_request_threads.sys.argv", ["agdt-get-pull-request-threads"]),
    ):
        try:
            get_pull_request_threads_async()
        except SystemExit as exc:
            assert exc.code == 1
        else:
            raise AssertionError("expected SystemExit")
