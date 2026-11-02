from agentic_devtools.cli import pull_request_create


def test_adapter_for_github_returns_github_adapter() -> None:
    adapter = pull_request_create._adapter_for("github")

    assert isinstance(adapter, pull_request_create.GitHubPullRequestCreateAdapter)


def test_adapter_for_azure_devops_returns_azure_devops_adapter() -> None:
    adapter = pull_request_create._adapter_for("azure_devops")

    assert isinstance(adapter, pull_request_create.AzureDevOpsPullRequestCreateAdapter)
