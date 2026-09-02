"""Tests for Windows verification module."""

import pytest

from runlayer_cli.verified_local_proxy.config import VerificationConfig
from runlayer_cli.verified_local_proxy.exceptions import VerificationError
from runlayer_cli.verified_local_proxy.verification.base import ProcessInfo
from runlayer_cli.verified_local_proxy.verification.windows import WindowsVerifier


@pytest.fixture
def verifier():
    """Create a WindowsVerifier instance."""
    return WindowsVerifier()


@pytest.fixture
def sample_config():
    """Create a sample verification config."""
    return VerificationConfig(
        server_id="com.example/test",
        display_name="Example Test",
        target_port=8000,
    )


@pytest.fixture
def process_info():
    """Create sample process info."""
    return ProcessInfo(
        pid=12345,
        binary_path="C:\\Program Files\\Example\\example.exe",
        name="example",
    )


class TestWindowsNotImplemented:
    """Tests that Windows verification raises not implemented error."""

    def test_find_process_not_implemented(self, verifier):
        """Test that find_process_on_port raises not implemented error."""
        with pytest.raises(VerificationError) as exc_info:
            verifier.find_process_on_port(8000)

        assert "not yet implemented" in str(exc_info.value)
        assert "macOS" in str(exc_info.value)

    def test_verify_signature_not_implemented(self, verifier, process_info, sample_config):
        """Test that verify_signature raises not implemented error."""
        with pytest.raises(VerificationError) as exc_info:
            verifier.verify_signature(process_info, sample_config)

        assert "not yet implemented" in str(exc_info.value)
        assert "macOS" in str(exc_info.value)
