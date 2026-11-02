"""Tests for _get_requests."""

from agentic_devtools.cli.pull_request_thread import (
    _get_requests,
)


class TestHelper:
    def test_loads_http_client(self) -> None:
        assert _get_requests() is not None
