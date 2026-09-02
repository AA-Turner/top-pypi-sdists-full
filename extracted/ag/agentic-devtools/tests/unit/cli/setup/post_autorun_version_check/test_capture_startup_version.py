"""Tests for capture_startup_version."""

from __future__ import annotations

from unittest.mock import patch

import agentic_devtools
from agentic_devtools.cli.setup.post_autorun_version_check import capture_startup_version


class TestCaptureStartupVersion:
    """Tests for the capture_startup_version function."""

    def test_returns_current_package_version(self) -> None:
        """Returns the value of agentic_devtools.__version__."""
        result = capture_startup_version()
        assert result == agentic_devtools.__version__

    def test_returns_patched_version(self) -> None:
        """Returns the patched version when __version__ is overridden."""
        with patch.object(agentic_devtools, "__version__", "99.99.99"):
            result = capture_startup_version()
        assert result == "99.99.99"

    def test_is_a_string(self) -> None:
        """Return type is always a string."""
        result = capture_startup_version()
        assert isinstance(result, str)
