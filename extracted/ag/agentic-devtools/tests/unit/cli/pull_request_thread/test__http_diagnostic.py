"""Tests for _http_diagnostic."""

import pytest

from agentic_devtools.cli.pull_request_thread import (
    _http_diagnostic,
)


class TestHelper:
    @pytest.mark.parametrize("status", [401, 403, 404, 409, 422, 429, 500])
    def test_http_diagnostic_is_actionable(self, status: int) -> None:
        assert _http_diagnostic(status)
