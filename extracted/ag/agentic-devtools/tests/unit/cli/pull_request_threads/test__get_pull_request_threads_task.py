from unittest.mock import patch

from agentic_devtools.cli.pull_request_threads import _get_pull_request_threads_task


def test_returns_success_when_thread_listing_completes() -> None:
    with patch("agentic_devtools.cli.pull_request_threads.get_pull_request_threads"):
        assert _get_pull_request_threads_task(4, "github", "owner/repo") == 0
