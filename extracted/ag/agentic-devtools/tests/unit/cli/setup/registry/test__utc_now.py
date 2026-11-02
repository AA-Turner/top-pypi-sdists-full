"""Tests for _utc_now."""

import re

from agentic_devtools.cli.setup.registry import _utc_now


class TestUtcNow:
    """Tests for _utc_now."""

    def test_returns_iso8601_utc_zulu_string(self) -> None:
        """Returns an ISO-8601 UTC timestamp with a trailing ``Z``."""
        value = _utc_now()
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value)
