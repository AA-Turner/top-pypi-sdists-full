from agentic_devtools.adapters.pull_request_threads import (
    GitHubThreadResolutionAdapter,
    ThreadResolutionCapability,
)


def test_defaults_to_supported_and_verified_without_comment_lookup() -> None:
    capability = ThreadResolutionCapability(provider="azure_devops")

    assert capability.provider == "azure_devops"
    assert capability.supported is True
    assert capability.verify is True
    assert capability.comment_lookup is False


def test_github_adapter_capability_enables_comment_lookup() -> None:
    capability = GitHubThreadResolutionAdapter.capability

    assert capability.provider == "github"
    assert capability.supported is True
    assert capability.verify is True
    assert capability.comment_lookup is True
