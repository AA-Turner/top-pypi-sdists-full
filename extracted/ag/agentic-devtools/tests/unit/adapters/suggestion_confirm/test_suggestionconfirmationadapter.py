from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.suggestion_confirm import (
    SuggestionConfirmationAdapter,
    SuggestionConfirmationRequest,
)


def test_dry_run_does_not_mutate() -> None:
    request = SuggestionConfirmationRequest("azure_devops", "repo", 1, 2, "abcdef", dry_run=True)
    result = SuggestionConfirmationAdapter().confirm(request)
    assert result.as_dict()["status"] == "dry_run"


def test_sanitizes_environment_credentials(monkeypatch) -> None:
    monkeypatch.setenv("AZURE_DEV_OPS_COPILOT_PAT", "env-token")
    adapter = SuggestionConfirmationAdapter()
    assert adapter._sanitize_diagnostic("request failed: env-token") == "request failed: [redacted]"


def test_confirms_azure_suggestion() -> None:
    response = MagicMock()
    response.json.return_value = {"id": 7}
    requests_module = MagicMock()
    requests_module.post.return_value = response
    config = MagicMock()
    config.organization = "https://dev.azure.com/org"
    config.project = "project"
    config.repository = "state-repo"
    config.build_api_url.return_value = "https://example/comments"
    with (
        patch(
            "agentic_devtools.adapters.suggestion_confirm.get_repository_id",
            return_value="repo-id",
        ) as get_repo_id,
        patch("agentic_devtools.adapters.suggestion_confirm.resolve_thread_by_id"),
    ):
        result = SuggestionConfirmationAdapter(requests_module=requests_module, azure_config=config, pat="pat").confirm(
            SuggestionConfirmationRequest("azure_devops", "request-repo", 1, 2, "abcdef")
        )
    get_repo_id.assert_called_once_with(
        "https://dev.azure.com/org",
        "project",
        "request-repo",
        requests_module=requests_module,
        pat="pat",
    )
    assert result.success is True
    assert result.reply_id == 7


def test_normalizes_provider_failure(monkeypatch) -> None:
    monkeypatch.setenv("AZURE_DEV_OPS_COPILOT_PAT", "env-token")
    request = SuggestionConfirmationRequest("azure_devops", "repo", 1, 2, "abcdef")
    with patch("agentic_devtools.adapters.suggestion_confirm.get_repository_id", return_value="repo-id"):
        result = SuggestionConfirmationAdapter(
            requests_module=MagicMock(post=MagicMock(side_effect=RuntimeError("boom secret-token env-token"))),
            azure_config=MagicMock(),
            pat="secret-token",
        ).confirm(request)
    assert result.success is False
    assert result.status == "failed"
    assert result.diagnostics == ("boom [redacted] [redacted]",)


def test_reports_azure_partial_success_when_resolution_fails(monkeypatch) -> None:
    monkeypatch.setenv("AZURE_DEV_OPS_COPILOT_PAT", "secret-token")
    response = MagicMock()
    response.json.return_value = {"id": 7}
    requests_module = MagicMock()
    requests_module.post.return_value = response
    request = SuggestionConfirmationRequest(
        "azure_devops",
        "request-repo",
        1,
        2,
        "abcdef",
        organization="https://dev.azure.com/request-org",
        project="request-project",
    )
    with (
        patch("agentic_devtools.adapters.suggestion_confirm.AzureDevOpsConfig.from_state", side_effect=AssertionError),
        patch("agentic_devtools.adapters.suggestion_confirm.get_repository_id", return_value="repo-id"),
        patch(
            "agentic_devtools.adapters.suggestion_confirm.resolve_thread_by_id",
            side_effect=RuntimeError("close failed secret-token"),
        ),
    ):
        result = SuggestionConfirmationAdapter(requests_module=requests_module, pat="pat").confirm(request)
    assert result.success is False
    assert result.status == "partial_success"
    assert result.reply_id == 7
    assert result.diagnostics == ("Reply posted but resolution failed: close failed [redacted]",)


def test_uses_state_snapshot_for_azure_context_when_request_omits_it() -> None:
    response = MagicMock()
    response.json.return_value = {"id": 7}
    requests_module = MagicMock()
    requests_module.post.return_value = response
    state_config = type(
        "Config",
        (),
        {
            "organization": "https://dev.azure.com/state-org",
            "project": "state-project",
        },
    )()
    with (
        patch("agentic_devtools.adapters.suggestion_confirm.AzureDevOpsConfig.from_state", return_value=state_config),
        patch("agentic_devtools.adapters.suggestion_confirm.get_repository_id", return_value="repo-id") as get_repo_id,
        patch("agentic_devtools.adapters.suggestion_confirm.resolve_thread_by_id"),
    ):
        result = SuggestionConfirmationAdapter(requests_module=requests_module, pat="pat").confirm(
            SuggestionConfirmationRequest("azure_devops", "request-repo", 1, 2, "abcdef")
        )
    get_repo_id.assert_called_once_with(
        "https://dev.azure.com/state-org",
        "state-project",
        "request-repo",
        requests_module=requests_module,
        pat="pat",
    )
    assert result.success is True


def test_reports_partial_success_when_azure_response_is_not_json(monkeypatch) -> None:
    monkeypatch.setenv("AZURE_DEV_OPS_COPILOT_PAT", "secret-token")
    response = MagicMock()
    response.json.side_effect = ValueError("not json secret-token")
    requests_module = MagicMock()
    requests_module.post.return_value = response
    config = MagicMock()
    config.organization = "https://dev.azure.com/org"
    config.project = "project"
    config.repository = "state-repo"
    config.build_api_url.return_value = "https://example/comments"
    with (
        patch("agentic_devtools.adapters.suggestion_confirm.get_repository_id", return_value="repo-id"),
        patch("agentic_devtools.adapters.suggestion_confirm.resolve_thread_by_id") as resolve_thread,
    ):
        result = SuggestionConfirmationAdapter(requests_module=requests_module, azure_config=config, pat="pat").confirm(
            SuggestionConfirmationRequest("azure_devops", "request-repo", 1, 2, "abcdef")
        )
    resolve_thread.assert_not_called()
    assert result.success is False
    assert result.status == "partial_success"
    assert result.reply_id is None
    assert result.diagnostics == ("Reply posted but response payload was not valid JSON: not json [redacted]",)


@pytest.mark.parametrize("payload", [{"id": "not-an-int"}, {"id": -1}, {"id": True}, {}, ["not-a-dict"], None])
def test_reports_partial_success_when_azure_response_id_is_invalid(payload: object) -> None:
    response = MagicMock()
    response.json.return_value = payload
    requests_module = MagicMock()
    requests_module.post.return_value = response
    config = MagicMock()
    config.organization = "https://dev.azure.com/org"
    config.project = "project"
    config.repository = "state-repo"
    config.build_api_url.return_value = "https://example/comments"
    with (
        patch("agentic_devtools.adapters.suggestion_confirm.get_repository_id", return_value="repo-id"),
        patch("agentic_devtools.adapters.suggestion_confirm.resolve_thread_by_id") as resolve_thread,
    ):
        result = SuggestionConfirmationAdapter(requests_module=requests_module, azure_config=config, pat="pat").confirm(
            SuggestionConfirmationRequest("azure_devops", "request-repo", 1, 2, "abcdef")
        )
    resolve_thread.assert_not_called()
    assert result.success is False
    assert result.status == "partial_success"
    assert result.reply_id is None
    assert result.diagnostics == ("Reply posted but response did not include a valid positive integer id",)


def test_confirms_github_suggestion() -> None:
    request = SuggestionConfirmationRequest("github", "owner/repo", 1, 2, "abcdef", "PRRT_abc")
    reply_result = MagicMock(mutation_status="replied_and_resolved", reply_id=9, diagnostics=())
    with (
        patch(
            "agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread",
            return_value=reply_result,
        ) as reply_to_thread,
        patch(
            "agentic_devtools.state.load_state_locked",
            side_effect=AssertionError("GitHub confirmation must use the captured request"),
        ),
    ):
        result = SuggestionConfirmationAdapter().confirm(request)
    assert result.success is True
    assert result.reply_id == 9
    reply_request = reply_to_thread.call_args.args[0]
    assert reply_request.provider == "github"
    assert reply_request.repository == "owner/repo"
    assert reply_request.pull_request_number == 1
    assert reply_request.discussion_id == 2
    assert reply_request.body == "✅ Suggestion addressed in commit `abcdef`."
    assert reply_request.resolve is True
    assert reply_request.review_thread_id == "PRRT_abc"
    assert reply_request.dry_run is False


def test_reports_github_partial_result() -> None:
    request = SuggestionConfirmationRequest("github", "owner/repo", 1, 2, "abcdef", "PRRT_abc")
    reply_result = MagicMock(mutation_status="partial_success", reply_id=9, diagnostics=("failed",))
    with (
        patch("agentic_devtools.cli.pull_request_thread.build_reply_request"),
        patch(
            "agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread",
            return_value=reply_result,
        ),
    ):
        result = SuggestionConfirmationAdapter().confirm(request)
    assert result.success is False
    assert result.diagnostics == ("failed",)
