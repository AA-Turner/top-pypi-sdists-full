from unittest.mock import patch

from agentic_devtools.adapters.pull_request_publish import PullRequestPublishResult
from agentic_devtools.cli.pull_request_publish import _run_publish


@patch("agentic_devtools.cli.pull_request_publish.publish_pull_request")
def test_returns_zero_for_azure(mock_publish) -> None:
    mock_publish.return_value = None
    assert _run_publish(provider="azure_devops") == 0


@patch("agentic_devtools.cli.pull_request_publish.publish_pull_request")
def test_returns_zero_for_success(mock_publish) -> None:
    mock_publish.return_value = PullRequestPublishResult(True, "github", "published")
    assert _run_publish(provider="github") == 0


@patch("agentic_devtools.cli.pull_request_publish.publish_pull_request")
def test_returns_one_for_failure(mock_publish) -> None:
    mock_publish.return_value = PullRequestPublishResult(False, "github", "failed")
    assert _run_publish(provider="github") == 1
