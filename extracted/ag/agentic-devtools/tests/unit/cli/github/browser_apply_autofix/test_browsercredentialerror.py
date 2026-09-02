"""Tests for BrowserCredentialError."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.browser_apply_autofix import BrowserCredentialError


class TestBrowserCredentialError:
    """Tests for the BrowserCredentialError exception."""

    def test_is_runtime_error_subclass(self) -> None:
        assert issubclass(BrowserCredentialError, RuntimeError)

    def test_can_be_raised_with_message(self) -> None:
        with pytest.raises(BrowserCredentialError, match="bad creds"):
            raise BrowserCredentialError("bad creds")
