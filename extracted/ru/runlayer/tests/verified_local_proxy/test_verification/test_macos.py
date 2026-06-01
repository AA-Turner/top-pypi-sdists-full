"""Tests for macOS verification module."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from runlayer_cli.verified_local_proxy.config import VerificationConfig
from runlayer_cli.verified_local_proxy.exceptions import VerificationError
from runlayer_cli.verified_local_proxy.verification.base import ProcessInfo
from runlayer_cli.verified_local_proxy.verification.macos import MacOSVerifier


@pytest.fixture(autouse=True)
def mock_verify_system_binary():
    """Mock system binary verification for tests."""
    with patch(
        "runlayer_cli.verified_local_proxy.verification.macos._verify_system_binary"
    ) as mock:
        mock.return_value = None  # Pass verification
        yield mock


@pytest.fixture
def verifier():
    """Create a MacOSVerifier instance."""
    return MacOSVerifier()


@pytest.fixture
def sample_config():
    """Create a sample verification config."""
    return VerificationConfig(
        server_id="com.example/test",
        display_name="Example Test",
        target_port=8000,
        # Must match exact codesign output format (includes team ID in parens)
        macos_authority="Developer ID Application: Example Inc (ABC123DEF)",
        macos_root_ca="Apple Root CA",
        expected_binary_paths=["/Applications/Example.app"],
    )


@pytest.fixture
def process_info():
    """Create sample process info."""
    return ProcessInfo(
        pid=12345,
        binary_path="/Applications/Example.app/Contents/MacOS/example",
        name="example",
    )


class TestFindProcessOnPort:
    """Tests for find_process_on_port method."""

    def test_find_process_success(self, verifier):
        """Test successful process discovery."""
        lsof_output = "COMMAND  PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME\nexample  123 user   10u  IPv4 0x1234567890      0t0  TCP *:8000 (LISTEN)"
        ps_output = "/Applications/Example.app/Contents/MacOS/example"

        with patch("subprocess.run") as mock_run:
            # Mock lsof call
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout=lsof_output, stderr=""),
                MagicMock(returncode=0, stdout=ps_output, stderr=""),
            ]

            result = verifier.find_process_on_port(8000)

        assert result is not None
        assert result.pid == 123
        assert result.name == "example"

    def test_find_process_not_listening(self, verifier):
        """Test when no process is listening on port."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
            result = verifier.find_process_on_port(8000)

        assert result is None

    def test_find_process_timeout(self, verifier):
        """Test timeout handling."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="lsof", timeout=10)
            result = verifier.find_process_on_port(8000)

        assert result is None


class TestVerifySignature:
    """Tests for verify_signature method."""

    def test_verify_signature_success(self, verifier, process_info, sample_config):
        """Test successful signature verification."""
        codesign_verify_output = ""
        codesign_detail_output = """Executable=/Applications/Example.app/Contents/MacOS/example
Authority=Developer ID Application: Example Inc (ABC123DEF)
Authority=Developer ID Certification Authority
Authority=Apple Root CA
TeamIdentifier=ABC123DEF
"""

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=codesign_verify_output),
                MagicMock(returncode=0, stdout="", stderr=codesign_detail_output),
            ]

            # Should not raise
            verifier.verify_signature(process_info, sample_config)

    def test_verify_signature_invalid(self, verifier, process_info, sample_config):
        """Test invalid signature detection."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="invalid signature",
            )

            with pytest.raises(VerificationError) as exc_info:
                verifier.verify_signature(process_info, sample_config)

            assert "invalid" in str(exc_info.value).lower()

    def test_verify_signature_wrong_authority(
        self, verifier, process_info, sample_config
    ):
        """Test wrong authority detection."""
        codesign_detail_output = """Executable=/Applications/Example.app/Contents/MacOS/example
Authority=Developer ID Application: Wrong Inc (XYZ789)
TeamIdentifier=XYZ789
"""

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=codesign_detail_output),
            ]

            with pytest.raises(VerificationError) as exc_info:
                verifier.verify_signature(process_info, sample_config)

            assert "Authority mismatch" in str(exc_info.value)

    def test_verify_signature_unexpected_path(self, verifier, sample_config):
        """Test unexpected binary path detection."""
        process_info = ProcessInfo(
            pid=12345,
            binary_path="/tmp/risky/example",
            name="example",
        )

        with pytest.raises(VerificationError) as exc_info:
            verifier.verify_signature(process_info, sample_config)

        assert "not in expected paths" in str(exc_info.value)

    def test_verify_signature_rejects_path_prefix_attack(self, verifier, sample_config):
        """Test that path prefix attacks are rejected (e.g., /Applications/Example.app.evil)."""
        # Attacker creates /Applications/Example.app.evil which starts with /Applications/Example.app
        process_info = ProcessInfo(
            pid=12345,
            binary_path="/Applications/Example.app.evil/Contents/MacOS/example",
            name="example",
        )

        with pytest.raises(VerificationError) as exc_info:
            verifier.verify_signature(process_info, sample_config)

        assert "not in expected paths" in str(exc_info.value)


class TestCertificateChainValidation:
    """Tests for certificate chain validation (risky CA prevention)."""

    def test_reject_risky_ca(self, verifier, process_info):
        """Test rejection of certificate not from Apple Root CA."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            # Must match exact codesign output format
            macos_authority="Developer ID Application: Example Inc (ABC123DEF)",
            macos_root_ca="Apple Root CA",
            expected_binary_paths=["/Applications/Example.app"],
        )

        # Certificate chain with risky self-signed CA (not Apple Root CA)
        codesign_detail_output = """Executable=/Applications/Example.app/Contents/MacOS/example
Authority=Developer ID Application: Example Inc (ABC123DEF)
Authority=Risky CA
TeamIdentifier=ABC123DEF
"""

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=codesign_detail_output),
            ]

            with pytest.raises(VerificationError) as exc_info:
                verifier.verify_signature(process_info, config)

            assert "Root CA mismatch" in str(exc_info.value)
            assert "risky certificate" in str(exc_info.value).lower()

    def test_accept_valid_apple_chain(self, verifier, process_info):
        """Test acceptance of valid Apple certificate chain."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            # Must match exact codesign output format
            macos_authority="Developer ID Application: Example Inc (ABC123DEF)",
            macos_root_ca="Apple Root CA",
            expected_binary_paths=["/Applications/Example.app"],
        )

        # Valid Apple certificate chain
        codesign_detail_output = """Executable=/Applications/Example.app/Contents/MacOS/example
Authority=Developer ID Application: Example Inc (ABC123DEF)
Authority=Developer ID Certification Authority
Authority=Apple Root CA
TeamIdentifier=ABC123DEF
"""

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=codesign_detail_output),
            ]

            # Should not raise
            verifier.verify_signature(process_info, config)


class TestStrictResourceCheck:
    """Tests for macos_strict_resource_check config option."""

    def test_ignore_resources_included_by_default(self, verifier, process_info):
        """Test that --ignore-resources is included when strict check is disabled (default)."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            macos_strict_resource_check=False,  # Default
            expected_binary_paths=["/Applications/Example.app"],
        )

        codesign_detail_output = """Executable=/Applications/Example.app/Contents/MacOS/example
Authority=Developer ID Application: Example Inc (ABC123DEF)
Authority=Developer ID Certification Authority
Authority=Apple Root CA
TeamIdentifier=ABC123DEF
"""

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=codesign_detail_output),
            ]

            verifier.verify_signature(process_info, config)

            # Check first call (codesign --verify) includes --ignore-resources
            first_call_args = mock_run.call_args_list[0][0][0]
            assert "--ignore-resources" in first_call_args

    def test_ignore_resources_excluded_when_strict(self, verifier, process_info):
        """Test that --ignore-resources is excluded when strict check is enabled."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            macos_strict_resource_check=True,  # Strict mode
            expected_binary_paths=["/Applications/Example.app"],
        )

        codesign_detail_output = """Executable=/Applications/Example.app/Contents/MacOS/example
Authority=Developer ID Application: Example Inc (ABC123DEF)
Authority=Developer ID Certification Authority
Authority=Apple Root CA
TeamIdentifier=ABC123DEF
"""

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),
                MagicMock(returncode=0, stdout="", stderr=codesign_detail_output),
            ]

            verifier.verify_signature(process_info, config)

            # Check first call (codesign --verify) does NOT include --ignore-resources
            first_call_args = mock_run.call_args_list[0][0][0]
            assert "--ignore-resources" not in first_call_args


class TestExtractAppBundlePath:
    """Tests for _extract_app_bundle_path method."""

    def test_extract_from_macos_path(self, verifier):
        """Test extracting .app path from MacOS binary path."""
        path = "/Applications/Example.app/Contents/MacOS/example"
        result = verifier._extract_app_bundle_path(path)
        assert result == "/Applications/Example.app"

    def test_extract_from_nested_path(self, verifier):
        """Test extracting .app path from nested path."""
        path = "/Applications/Example.app/Contents/Frameworks/Helper.app/Contents/MacOS/helper"
        result = verifier._extract_app_bundle_path(path)
        # Should extract first .app match
        assert result == "/Applications/Example.app/Contents/Frameworks/Helper.app"

    def test_no_app_in_path(self, verifier):
        """Test path without .app bundle."""
        path = "/usr/local/bin/example"
        result = verifier._extract_app_bundle_path(path)
        assert result is None
