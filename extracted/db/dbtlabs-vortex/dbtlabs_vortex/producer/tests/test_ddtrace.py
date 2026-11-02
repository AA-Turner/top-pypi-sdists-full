"""
Tests for the ddtrace module to ensure it properly suppresses log messages.
"""

import io
import logging
import platform
import sys
from unittest.mock import patch

import pytest

# Skip Linux-specific tests on non-Linux platforms
is_linux = platform.system() == "Linux"


class TestDDTraceLogging:
    """
    Tests to ensure ddtrace logs are properly suppressed.
    """

    @pytest.mark.skipif(not is_linux, reason="Test requires Linux platform for _pslinux module")
    def test_suppress_vendor_traceback_at_load_time(self, caplog):
        """
        Test that the trace context manager suppresses logs from ddtrace vendor modules.
        """
        # ### replicate the behavior first

        # Setup capturing logs at DEBUG level
        caplog.set_level(logging.DEBUG)

        # Create an object to capture stdout
        stdout_capture = io.StringIO()
        sys.stdout = stdout_capture
        sys.stderr = stdout_capture

        # Mock FileNotFoundError for psutil functions
        # This simulates what happens in environments without /proc
        file_not_found_error = FileNotFoundError(2, "No such file or directory", "/proc/stat")

        with patch("dbtlabs_vortex.producer.ddtrace.has_ddtrace_dependency", return_value=True):
            # Mock the FileNotFoundError when psutil tries to access /proc/stat
            with patch("ddtrace.vendor.psutil._common.open_binary") as mock_open:
                mock_open.side_effect = file_not_found_error
                from importlib import reload

                import ddtrace.vendor.psutil._pslinux

                ddtrace.vendor.psutil._pslinux.set_scputimes_ntuple.cache_clear()
                reload(ddtrace.vendor.psutil._pslinux)

        # Restore stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        mock_open.assert_called_once_with("/proc/stat")

        # Check that no ddtrace logs appear in captured output
        captured_stdout = stdout_capture.getvalue()
        print(f"captured_stdout: {captured_stdout}")
        assert "FileNotFoundError" in captured_stdout
        assert "/proc/stat" in captured_stdout

        # ### fix the behavior
        print("### fix the behavior")
        # Setup capturing logs at DEBUG level
        caplog.set_level(logging.DEBUG)

        # Create an object to capture stdout
        stdout_capture = io.StringIO()
        sys.stdout = stdout_capture
        sys.stderr = stdout_capture

        with patch("dbtlabs_vortex.producer.ddtrace.has_ddtrace_dependency", return_value=True):
            # Mock the FileNotFoundError when psutil tries to access /proc/stat
            with patch("ddtrace.vendor.psutil._common.open_binary") as mock_open:
                mock_open.side_effect = file_not_found_error
                sys.modules.pop("ddtrace.vendor.psutil._pslinux")
                sys.modules.pop("dbtlabs_vortex.producer.ddtrace")
                from importlib import reload

                import dbtlabs_vortex.producer.ddtrace

                reload(dbtlabs_vortex.producer.ddtrace)
                ddtrace.vendor.psutil._pslinux.set_scputimes_ntuple.cache_clear()
                dbtlabs_vortex.producer.ddtrace._preload_psutil_muted_traceback()

                import ddtrace.vendor.psutil._pslinux  # type: ignore

        # Restore stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        captured_stdout = stdout_capture.getvalue()
        print(f"captured_stdout: {captured_stdout}")

        mock_open.assert_called_once_with("/proc/stat")

        # Check that no ddtrace logs appear in captured output
        assert "FileNotFoundError" not in captured_stdout
        assert "/proc/stat" not in captured_stdout
