from unittest.mock import patch

from agentic_devtools.adapters.suggestion_confirm import SuggestionConfirmationRequest, SuggestionConfirmationResult
from agentic_devtools.cli.suggestion_confirm import confirm_suggestion_addressed


def test_reports_invalid_request_as_json(capsys) -> None:
    with patch(
        "agentic_devtools.cli.suggestion_confirm.build_confirmation_request",
        side_effect=ValueError("invalid"),
    ):
        result = confirm_suggestion_addressed()
    assert result["status"] == "invalid"
    assert "invalid" in capsys.readouterr().out


def test_confirms_supplied_request(capsys) -> None:
    request = SuggestionConfirmationRequest("azure_devops", "repo", 1, 2, "abc")
    with patch(
        "agentic_devtools.cli.suggestion_confirm.SuggestionConfirmationAdapter.confirm",
        return_value=SuggestionConfirmationResult(True, "azure_devops", "replied_and_resolved"),
    ) as confirm:
        result = confirm_suggestion_addressed(request)
    confirm.assert_called_once_with(request)
    assert result["success"] is True
    assert "replied_and_resolved" in capsys.readouterr().out


def test_accepts_request_mapping(capsys) -> None:
    request = {
        "provider": "azure_devops",
        "repository": "repo",
        "pull_request_id": 1,
        "discussion_id": 2,
        "commit_hash": "abc",
        "dry_run": True,
    }
    result = confirm_suggestion_addressed(request)
    assert result["status"] == "dry_run"
    assert "dry_run" in capsys.readouterr().out
