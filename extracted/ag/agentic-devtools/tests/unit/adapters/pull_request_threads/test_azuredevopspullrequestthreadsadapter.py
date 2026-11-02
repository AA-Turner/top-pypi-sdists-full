import pytest

from agentic_devtools.adapters.pull_request_threads import (
    AzureDevOpsPullRequestThreadsAdapter,
    PullRequestThreadsRequest,
)


def test_normalizes_fetched_threads() -> None:
    request = PullRequestThreadsRequest("azure_devops", "repo", 3)
    adapter = AzureDevOpsPullRequestThreadsAdapter(
        lambda _request: [
            {
                "id": 7,
                "status": "active",
                "threadContext": {"filePath": "/a.py", "rightFileStart": {"line": 9}},
                "comments": [{"id": 8, "author": {"displayName": "A"}, "content": "hi"}],
            }
        ]
    )
    result = adapter.list(request)
    assert result[0].line == 9


def test_rejects_provider_mismatch_and_bad_payload() -> None:
    with pytest.raises(ValueError, match="provider mismatch"):
        AzureDevOpsPullRequestThreadsAdapter(lambda _: []).list(PullRequestThreadsRequest("github", "owner/repo", 1))
    with pytest.raises(ValueError, match="must be a list"):
        AzureDevOpsPullRequestThreadsAdapter(lambda _: {}).list(PullRequestThreadsRequest("azure_devops", "repo", 1))
