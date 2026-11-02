from unittest.mock import patch

from agentic_devtools.cli import pull_request_create


def test_dispatch_create_pull_request_selects_github_adapter() -> None:
    request = pull_request_create.PullRequestCreateRequest("github", "feature", "Title")
    with patch.object(pull_request_create.GitHubPullRequestCreateAdapter, "create") as create:
        pull_request_create.dispatch_create_pull_request(request)
    create.assert_called_once_with(request)


def test_dispatch_create_pull_request_selects_azure_adapter() -> None:
    request = pull_request_create.PullRequestCreateRequest("azure_devops", "feature", "Title")
    with patch.object(pull_request_create.AzureDevOpsPullRequestCreateAdapter, "create") as create:
        pull_request_create.dispatch_create_pull_request(request)
    create.assert_called_once_with(request)
