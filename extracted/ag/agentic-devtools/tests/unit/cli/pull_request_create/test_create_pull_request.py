from unittest.mock import patch

from agentic_devtools.adapters.pull_request_create import PullRequestCreateRequest, PullRequestCreateResult
from agentic_devtools.cli import pull_request_create


def test_create_pull_request_dispatches_provider_neutral_request() -> None:
    expected = PullRequestCreateResult(True, "github", "created", url="url")
    with (
        patch.object(pull_request_create, "build_create_request") as build,
        patch.object(pull_request_create, "dispatch_create_pull_request", return_value=expected) as dispatch,
    ):
        build.return_value = object()
        result = pull_request_create.create_pull_request()

    assert result == expected
    dispatch.assert_called_once_with(build.return_value)


def test_create_pull_request_persists_explicit_provider_when_unconfigured() -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with (
        patch.object(pull_request_create, "build_create_request", return_value=request),
        patch.object(pull_request_create, "_resolve_configured_provider", return_value=None),
        patch.object(pull_request_create, "set_value") as save,
        patch.object(
            pull_request_create,
            "dispatch_create_pull_request",
            return_value=PullRequestCreateResult(True, "github", "created"),
        ),
    ):
        pull_request_create.create_pull_request(provider="github")

    save.assert_called_once_with("platform.code_hosting", "github")


def test_create_pull_request_returns_invalid_result(capsys) -> None:
    with patch.object(pull_request_create, "build_create_request", side_effect=ValueError("bad")):
        result = pull_request_create.create_pull_request(provider="github")

    assert result.status == "invalid"
    assert '"error": "bad"' in capsys.readouterr().out


def test_create_pull_request_returns_failed_result_for_adapter_exception(capsys) -> None:
    request = PullRequestCreateRequest("azure_devops", "feature", "Title")
    with (
        patch.object(pull_request_create, "build_create_request", return_value=request),
        patch.object(pull_request_create, "dispatch_create_pull_request", side_effect=RuntimeError("lock busy")),
    ):
        result = pull_request_create.create_pull_request()

    assert result.provider == "azure_devops"
    assert result.status == "failed"
    assert result.error == "lock busy"
    assert '"status": "failed"' in capsys.readouterr().out


def test_create_pull_request_reports_timeout_as_indeterminate(capsys) -> None:
    request = PullRequestCreateRequest("github", "feature", "Title")
    with (
        patch.object(pull_request_create, "build_create_request", return_value=request),
        patch.object(
            pull_request_create,
            "dispatch_create_pull_request",
            side_effect=pull_request_create.subprocess.TimeoutExpired("create", 1),
        ),
    ):
        result = pull_request_create.create_pull_request()

    assert result.provider == "github"
    assert result.success is True
    assert result.status == "indeterminate"
    assert '"status": "indeterminate"' in capsys.readouterr().out


def test_create_pull_request_uses_unknown_provider_when_resolution_fails(capsys) -> None:
    with (
        patch.object(pull_request_create, "build_create_request", side_effect=ValueError("bad")),
        patch.object(pull_request_create, "resolve_create_provider", side_effect=ValueError("provider error")),
    ):
        result = pull_request_create.create_pull_request()

    assert result.provider == "unknown"
    assert result.status == "invalid"
    assert '"error": "bad"' in capsys.readouterr().out
