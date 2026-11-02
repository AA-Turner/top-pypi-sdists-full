import pytest

from agentic_devtools.adapters.exceptions import AdapterValidationError
from agentic_devtools.adapters.suggestion_confirm import SuggestionConfirmationRequest


def test_validates_github_request() -> None:
    request = SuggestionConfirmationRequest("github", "owner/repo", 1, 2, "abcdef", "PRRT_abc")
    assert request.review_thread_id == "PRRT_abc"


@pytest.mark.parametrize("thread_id", [None, "", 1, "123", "abc", "PRRT_"])
def test_rejects_missing_github_thread_id(thread_id: object) -> None:
    with pytest.raises(AdapterValidationError):
        SuggestionConfirmationRequest("github", "owner/repo", 1, 2, "abcdef", thread_id)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"provider": "jira"},
        {"provider": []},
        {"provider": {}},
        {"repository": ""},
        {"pull_request_id": 0},
        {"commit_hash": 1},
        {"provider": "github", "repository": "bad"},
        {"provider": "github", "review_thread_id": None},
        {"provider": "github", "review_thread_id": ""},
        {"provider": "github", "review_thread_id": 1},
        {"provider": "azure_devops", "discussion_id": 0},
        {"dry_run": "yes"},
        {"commit_hash": ""},
        {"organization": ""},
        {"project": " "},
        {"provider": "azure_devops", "organization": "https://dev.azure.com/org"},
        {"provider": "azure_devops", "project": "project"},
    ],
)
def test_rejects_invalid_request(kwargs: dict[str, object]) -> None:
    values: dict[str, object] = {
        "provider": "azure_devops",
        "repository": "repo",
        "pull_request_id": 1,
        "discussion_id": 1,
        "commit_hash": "abc",
    }
    values.update(kwargs)
    with pytest.raises(AdapterValidationError):
        SuggestionConfirmationRequest(**values)  # type: ignore[arg-type]
