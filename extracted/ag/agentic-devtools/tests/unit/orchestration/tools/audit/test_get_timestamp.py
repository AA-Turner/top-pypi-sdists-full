"""Tests for audit.get_timestamp()."""

import time

from agentic_devtools.orchestration.tools.audit import get_timestamp


class TestGetTimestamp:
    """Tests for get_timestamp utility."""

    def test_returns_float(self):
        """get_timestamp returns a float."""
        ts = get_timestamp()
        assert isinstance(ts, float)

    def test_returns_current_time(self):
        """get_timestamp returns approximately current time."""
        before = time.time()
        ts = get_timestamp()
        after = time.time()
        assert before <= ts <= after
