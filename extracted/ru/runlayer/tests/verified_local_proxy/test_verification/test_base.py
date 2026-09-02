"""Tests for verification base module and platform detection."""

import sys
from unittest.mock import patch

import pytest

from runlayer_cli.verified_local_proxy.verification import get_verifier
from runlayer_cli.verified_local_proxy.verification.base import ProcessInfo


class TestProcessInfo:
    """Tests for ProcessInfo dataclass."""

    def test_basic_creation(self):
        """Test basic ProcessInfo creation."""
        info = ProcessInfo(pid=12345, binary_path="/path/to/binary")
        assert info.pid == 12345
        assert info.binary_path == "/path/to/binary"
        assert info.name is None

    def test_with_name(self):
        """Test ProcessInfo with name."""
        info = ProcessInfo(pid=12345, binary_path="/path/to/binary", name="myprocess")
        assert info.name == "myprocess"


class TestGetVerifier:
    """Tests for get_verifier platform detection."""

    def test_macos_verifier(self):
        """Test that MacOSVerifier is returned on macOS."""
        with patch.object(sys, "platform", "darwin"):
            from runlayer_cli.verified_local_proxy.verification.macos import MacOSVerifier

            verifier = get_verifier()
            assert isinstance(verifier, MacOSVerifier)

    def test_windows_verifier(self):
        """Test that WindowsVerifier is returned on Windows."""
        with patch.object(sys, "platform", "win32"):
            from runlayer_cli.verified_local_proxy.verification.windows import WindowsVerifier

            verifier = get_verifier()
            assert isinstance(verifier, WindowsVerifier)

    def test_unsupported_platform(self):
        """Test that unsupported platforms raise RuntimeError."""
        with patch.object(sys, "platform", "linux"):
            with pytest.raises(RuntimeError) as exc_info:
                get_verifier()

            assert "Unsupported platform" in str(exc_info.value)
            assert "linux" in str(exc_info.value)
