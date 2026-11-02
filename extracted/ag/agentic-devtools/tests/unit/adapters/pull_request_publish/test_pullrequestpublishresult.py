from agentic_devtools.adapters.pull_request_publish import PullRequestPublishResult


def test_stores_result() -> None:
    result = PullRequestPublishResult(True, "github", "published")
    assert result.success
    assert result.error == ""
