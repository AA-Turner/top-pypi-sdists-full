"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._jira_probe_worker`."""

from __future__ import annotations

from unittest.mock import Mock, patch

import requests

from agentic_devtools.cli.setup.provider_connectivity import _jira_probe_worker


class _QueueRecorder:
    def __init__(self) -> None:
        self.items: list[tuple[object, ...]] = []

    def put(self, item: tuple[object, ...]) -> None:
        self.items.append(item)


class TestJiraProbeWorker:
    """Verify the child-process Jira probe reports each outcome shape correctly."""

    def test_returns_response_payload(self) -> None:
        """Successful responses are serialized as status/text tuples."""
        queue = _QueueRecorder()
        response = Mock(status_code=200, text="ok")

        with patch("requests.get", return_value=response) as mock_get:
            _jira_probe_worker(
                queue, "https://jira.example.com/rest/api/2/myself", {"Authorization": "******"}, 5.0, True
            )

        assert queue.items == [("response", 200, "ok")]
        mock_get.assert_called_once_with(
            "https://jira.example.com/rest/api/2/myself",
            headers={"Authorization": "******"},
            timeout=5.0,
            verify=True,
            allow_redirects=False,
        )

    def test_truncates_large_response_payload(self) -> None:
        """Probe responses are truncated before queueing to avoid large queue flush delays."""
        queue = _QueueRecorder()
        response = Mock(status_code=500, text="x" * 5000)

        with patch("requests.get", return_value=response):
            _jira_probe_worker(
                queue, "https://jira.example.com/rest/api/2/myself", {"Authorization": "******"}, 5.0, True
            )

        assert queue.items == [("response", 500, "x" * 200)]

    def test_returns_timeout_payload(self) -> None:
        """requests timeouts are reported distinctly for the hard-deadline wrapper."""
        queue = _QueueRecorder()

        with patch("requests.get", side_effect=requests.Timeout("timed out")):
            _jira_probe_worker(
                queue, "https://jira.example.com/rest/api/2/myself", {"Authorization": "******"}, 5.0, True
            )

        assert queue.items == [("timeout", "timed out")]

    def test_returns_request_exception_payload(self) -> None:
        """Non-timeout request failures are reported as generic probe errors."""
        queue = _QueueRecorder()

        with patch("requests.get", side_effect=requests.ConnectionError("offline")):
            _jira_probe_worker(
                queue, "https://jira.example.com/rest/api/2/myself", {"Authorization": "******"}, 5.0, True
            )

        assert queue.items == [("error", "offline")]

    def test_returns_unexpected_exception_payload(self) -> None:
        """Non-requests exceptions are converted to generic error payloads."""
        queue = _QueueRecorder()

        with patch("requests.get", side_effect=OSError("missing pem")):
            _jira_probe_worker(
                queue, "https://jira.example.com/rest/api/2/myself", {"Authorization": "******"}, 5.0, "/bad.pem"
            )

        assert queue.items == [("error", "missing pem")]
