"""Tests for proxy module."""

import time
from unittest.mock import MagicMock, patch

import pytest

from runlayer_cli.verified_local_proxy.config import VerificationConfig
from runlayer_cli.verified_local_proxy.exceptions import (
    TargetNotRunningError,
    VerificationError,
)
from runlayer_cli.verified_local_proxy.proxy import (
    _get_transport,
    _get_heartbeat,
    _update_heartbeat,
    verify_target,
)
from runlayer_cli.verified_local_proxy.verification.base import ProcessInfo


@pytest.fixture
def sample_config():
    """Create a sample verification config."""
    return VerificationConfig(
        server_id="com.example/test",
        display_name="Example Test",
        target_port=8000,
        target_path="/mcp",
        macos_authority="Developer ID Application: Example Inc (ABC123DEF)",
    )


@pytest.fixture
def sample_sse_config():
    """Create a sample SSE verification config."""
    return VerificationConfig(
        server_id="com.figma/desktop-mcp",
        display_name="Figma Desktop MCP",
        target_port=3845,
        target_path="/sse",
    )


class TestGetTransport:
    """Tests for _get_transport function."""

    def test_sse_transport_for_sse_path(self, sample_sse_config):
        """Test that SSETransport is used for /sse paths."""
        from fastmcp.client.transports import SSETransport

        transport = _get_transport(sample_sse_config)
        assert isinstance(transport, SSETransport)

    def test_streamable_http_for_mcp_path(self, sample_config):
        """Test that StreamableHttpTransport is used for non-SSE paths."""
        from fastmcp.client.transports import StreamableHttpTransport

        transport = _get_transport(sample_config)
        assert isinstance(transport, StreamableHttpTransport)

    def test_sse_path_case_insensitive(self):
        """Test that SSE detection is case-insensitive."""
        from fastmcp.client.transports import SSETransport

        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            target_path="/SSE",
        )
        transport = _get_transport(config)
        assert isinstance(transport, SSETransport)


class TestVerifyTarget:
    """Tests for verify_target function."""

    def test_verify_target_success(self, sample_config):
        """Test successful target verification."""
        mock_verifier = MagicMock()
        mock_verifier.find_process_on_port.return_value = ProcessInfo(
            pid=12345,
            binary_path="/Applications/Example.app/Contents/MacOS/example",
            name="example",
        )

        with patch("runlayer_cli.verified_local_proxy.proxy.get_verifier", return_value=mock_verifier):
            # Should not raise
            verify_target(sample_config)

        mock_verifier.find_process_on_port.assert_called_once_with(8000)
        mock_verifier.verify_signature.assert_called_once()

    def test_verify_target_not_running(self, sample_config):
        """Test error when target is not running."""
        mock_verifier = MagicMock()
        mock_verifier.find_process_on_port.return_value = None

        with patch("runlayer_cli.verified_local_proxy.proxy.get_verifier", return_value=mock_verifier):
            with patch("time.sleep"):  # Don't actually sleep in tests
                with pytest.raises(TargetNotRunningError) as exc_info:
                    verify_target(sample_config, max_retries=2, retry_delay=0)

        assert "No process found listening on port 8000" in str(exc_info.value)
        assert mock_verifier.find_process_on_port.call_count == 2

    def test_verify_target_retries(self, sample_config):
        """Test that retries happen when process not immediately found."""
        mock_verifier = MagicMock()
        # Fail first two times, succeed third time
        mock_verifier.find_process_on_port.side_effect = [
            None,
            None,
            ProcessInfo(pid=12345, binary_path="/path/to/binary"),
        ]

        with patch("runlayer_cli.verified_local_proxy.proxy.get_verifier", return_value=mock_verifier):
            with patch("time.sleep"):  # Don't actually sleep in tests
                verify_target(sample_config, max_retries=3)

        assert mock_verifier.find_process_on_port.call_count == 3

    def test_verify_target_signature_failure(self, sample_config):
        """Test error propagation when signature verification fails."""
        mock_verifier = MagicMock()
        mock_verifier.find_process_on_port.return_value = ProcessInfo(
            pid=12345,
            binary_path="/path/to/binary",
        )
        mock_verifier.verify_signature.side_effect = VerificationError("Signature invalid")

        with patch("runlayer_cli.verified_local_proxy.proxy.get_verifier", return_value=mock_verifier):
            with pytest.raises(VerificationError) as exc_info:
                verify_target(sample_config)

        assert "Signature invalid" in str(exc_info.value)


class TestHeartbeat:
    """Tests for heartbeat functions used by watchdog."""

    def test_update_and_get_heartbeat(self):
        """Test heartbeat update and retrieval."""
        # Update heartbeat
        _update_heartbeat()
        heartbeat = _get_heartbeat()

        # Should be very recent (within last second)
        assert time.monotonic() - heartbeat < 1.0

    def test_heartbeat_increases(self):
        """Test that heartbeat timestamp increases on update."""
        _update_heartbeat()
        first = _get_heartbeat()

        time.sleep(0.01)  # Small delay

        _update_heartbeat()
        second = _get_heartbeat()

        assert second > first


class TestReverificationLoop:
    """Tests for the reverification loop behavior."""

    def test_reverification_updates_heartbeat(self):
        """Test that successful reverification updates heartbeat."""
        from runlayer_cli.verified_local_proxy.proxy import (
            _reverification_loop,
            _stop_reverification,
        )

        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            reverify_interval_seconds=1,
        )

        mock_verifier = MagicMock()
        mock_verifier.find_process_on_port.return_value = ProcessInfo(
            pid=12345,
            binary_path="/path/to/binary",
        )

        # Clear stop flag and record initial heartbeat
        _stop_reverification.clear()
        initial_heartbeat = _get_heartbeat()

        def stop_after_one_iteration(*args, **kwargs):
            """Stop the loop after verification runs once."""
            _stop_reverification.set()

        mock_verifier.verify_signature.side_effect = stop_after_one_iteration

        with patch("runlayer_cli.verified_local_proxy.proxy.get_verifier", return_value=mock_verifier):
            with patch("runlayer_cli.verified_local_proxy.proxy._stop_reverification") as mock_stop:
                # Simulate: first wait returns False (loop runs), then returns True (loop exits)
                mock_stop.wait.side_effect = [False, True]
                mock_stop.set = MagicMock()

                _reverification_loop(config)

        # Heartbeat should have been updated
        assert _get_heartbeat() >= initial_heartbeat

    def test_reverification_disabled_when_interval_none(self):
        """Test that reverification loop exits immediately when interval is None."""
        from runlayer_cli.verified_local_proxy.proxy import _reverification_loop

        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            reverify_interval_seconds=None,  # Disabled
        )

        # Should return immediately without doing anything
        _reverification_loop(config)  # Should not hang or error


class TestWatchdogLoop:
    """Tests for the watchdog loop behavior."""

    def test_watchdog_allows_fresh_heartbeat(self):
        """Test that watchdog doesn't trigger when heartbeat is fresh."""
        from runlayer_cli.verified_local_proxy.proxy import (
            _watchdog_loop,
            _stop_reverification,
        )

        # Update heartbeat to make it fresh
        _update_heartbeat()

        # Set up to run one iteration then stop
        _stop_reverification.clear()

        with patch("runlayer_cli.verified_local_proxy.proxy._stop_reverification") as mock_stop:
            mock_stop.wait.side_effect = [False, True]  # Run once, then exit

            with patch("runlayer_cli.verified_local_proxy.proxy.os._exit") as mock_exit:
                _watchdog_loop(interval=60)

                # Should NOT have called os._exit
                mock_exit.assert_not_called()

    def test_watchdog_triggers_on_stale_heartbeat(self):
        """Test that watchdog triggers os._exit when heartbeat is stale."""
        from runlayer_cli.verified_local_proxy.proxy import _watchdog_loop

        # Set heartbeat to a very old time
        import runlayer_cli.verified_local_proxy.proxy as proxy_module

        with patch.object(proxy_module, "_heartbeat_time", time.monotonic() - 1000):
            with patch("runlayer_cli.verified_local_proxy.proxy._stop_reverification") as mock_stop:
                mock_stop.wait.return_value = False  # Keep looping

                with patch("runlayer_cli.verified_local_proxy.proxy.os._exit") as mock_exit:
                    # Make os._exit raise to break out of the loop
                    mock_exit.side_effect = SystemExit(1)

                    with pytest.raises(SystemExit):
                        _watchdog_loop(interval=10)

                    # Should have called os._exit(1)
                    mock_exit.assert_called_once_with(1)


class TestConfigOptions:
    """Tests for new config options."""

    def test_reverify_interval_default_none(self):
        """Test that reverify_interval_seconds defaults to None."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
        )
        assert config.reverify_interval_seconds is None

    def test_reverify_interval_can_be_set(self):
        """Test that reverify_interval_seconds can be configured."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            reverify_interval_seconds=60,
        )
        assert config.reverify_interval_seconds == 60

    def test_strict_resource_check_default_false(self):
        """Test that macos_strict_resource_check defaults to False."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
        )
        assert config.macos_strict_resource_check is False

    def test_strict_resource_check_can_be_enabled(self):
        """Test that macos_strict_resource_check can be enabled."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test",
            target_port=8000,
            macos_strict_resource_check=True,
        )
        assert config.macos_strict_resource_check is True
