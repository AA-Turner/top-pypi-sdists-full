import pytest

from agentic_devtools.adapters.pull_request_publish import PullRequestPublishRequest


def test_validates_request() -> None:
    request = PullRequestPublishRequest("github", 12, "owner/repo")
    assert request.pull_request_id == 12


@pytest.mark.parametrize(
    ("provider", "number", "repository", "message"),
    [
        ("other", 1, "", "provider"),
        ("github", True, "owner/repo", "positive"),
        ("github", 0, "owner/repo", "positive"),
        ("github", 1, None, "repository"),
        ("github", 1, ["owner", "repo"], "repository"),
        ("azure_devops", 1, None, "repository"),
        ("azure_devops", 1, ["owner", "repo"], "repository"),
        ("github", 1, "", "repository"),
        ("github", 1, "invalid", "owner/repo"),
    ],
)
def test_rejects_invalid_request(provider: str, number: object, repository: object, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        PullRequestPublishRequest(provider, number, repository)  # type: ignore[arg-type]


def test_rejects_non_boolean_dry_run() -> None:
    with pytest.raises(ValueError, match="boolean"):
        PullRequestPublishRequest("github", 1, "owner/repo", dry_run="yes")  # type: ignore[arg-type]
