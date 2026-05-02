"""Tests for GUI main entry point."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestInstanceLocking:
    """Test single-instance locking functions."""

    def test_acquire_lock_success(self):
        """Test acquiring lock when no other instance."""
        from g13_linux.gui import main as main_module

        mock_file = MagicMock()
        mock_file.fileno.return_value = 42

        with patch("builtins.open", return_value=mock_file):
            with patch("fcntl.flock") as mock_flock:
                result = main_module.acquire_instance_lock()

                assert result is True
                mock_flock.assert_called_once()
                mock_file.write.assert_called_once()

        # Cleanup
        main_module._lock_file_handle = None

    def test_acquire_lock_failure_already_locked(self):
        """Test acquiring lock when another instance holds it."""

        from g13_linux.gui import main as main_module

        mock_file = MagicMock()
        mock_file.fileno.return_value = 42

        with patch("builtins.open", return_value=mock_file):
            with patch("fcntl.flock", side_effect=OSError("Resource busy")):
                result = main_module.acquire_instance_lock()

                assert result is False
                mock_file.close.assert_called_once()

        # Cleanup
        main_module._lock_file_handle = None

    def test_acquire_lock_failure_open_error(self):
        """Test acquiring lock when file cannot be opened."""
        from g13_linux.gui import main as main_module

        with patch("builtins.open", side_effect=OSError("Permission denied")):
            result = main_module.acquire_instance_lock()

            assert result is False

    def test_release_lock(self):
        """Test releasing the lock."""
        from g13_linux.gui import main as main_module

        mock_file = MagicMock()
        mock_file.fileno.return_value = 42
        main_module._lock_file_handle = mock_file

        with patch("fcntl.flock") as mock_flock:
            with patch.object(Path, "unlink"):
                main_module.release_instance_lock()

                mock_flock.assert_called_once()
                mock_file.close.assert_called_once()
                assert main_module._lock_file_handle is None

    def test_release_lock_when_no_handle(self):
        """Test releasing lock when none was acquired."""
        from g13_linux.gui import main as main_module

        main_module._lock_file_handle = None

        with patch.object(Path, "unlink"):
            # Should not raise
            main_module.release_instance_lock()

            assert main_module._lock_file_handle is None

    def test_release_lock_handles_errors(self):
        """Test release handles errors gracefully."""
        from g13_linux.gui import main as main_module

        mock_file = MagicMock()
        mock_file.fileno.return_value = 42
        mock_file.close.side_effect = OSError("Error closing")
        main_module._lock_file_handle = mock_file

        with patch("fcntl.flock", side_effect=OSError("Error unlocking")):
            with patch.object(Path, "unlink", side_effect=OSError("Error unlinking")):
                # Should not raise
                main_module.release_instance_lock()

                assert main_module._lock_file_handle is None


class TestMainFunction:
    """Test the main() entry point function."""

    def test_main_already_running(self, qapp):
        """Test main() exits when another instance is running."""
        from g13_linux.gui.main import main

        with patch.object(sys, "argv", ["g13-linux-gui"]):
            with patch("g13_linux.gui.main.acquire_instance_lock", return_value=False):
                with patch("g13_linux.gui.main.QApplication") as mock_app_cls:
                    mock_app = MagicMock()
                    mock_app_cls.return_value = mock_app

                    with patch("g13_linux.gui.main.QMessageBox") as mock_msgbox:
                        result = main()

                        mock_msgbox.warning.assert_called_once()
                        assert result == 1

    def test_main_normal_mode(self, qapp):
        """Test main() runs in normal hidraw mode."""
        from g13_linux.gui.main import main

        # Mock sys.argv without --libusb
        with patch.object(sys, "argv", ["g13-linux-gui"]):
            with patch("g13_linux.gui.main.acquire_instance_lock", return_value=True):
                with patch("g13_linux.gui.main.QApplication") as mock_app_cls:
                    mock_app = MagicMock()
                    mock_app.exec.return_value = 0
                    mock_app_cls.return_value = mock_app

                    with patch("g13_linux.gui.views.main_window.MainWindow") as mock_window_cls:
                        mock_window = MagicMock()
                        mock_window_cls.return_value = mock_window

                        with patch(
                            "g13_linux.gui.controllers.app_controller.ApplicationController"
                        ) as mock_ctrl_cls:
                            mock_ctrl = MagicMock()
                            mock_ctrl_cls.return_value = mock_ctrl

                            result = main()

                            # Should have created controller without libusb
                            mock_ctrl_cls.assert_called_once()
                            call_kwargs = mock_ctrl_cls.call_args[1]
                            assert call_kwargs.get("use_libusb") is False

                            assert result == 0

    def test_main_libusb_mode(self, qapp):
        """Test main() runs in libusb mode with --libusb flag."""
        from g13_linux.gui.main import main

        # Need to copy argv because main() modifies it
        test_argv = ["g13-linux-gui", "--libusb"]

        with patch.object(sys, "argv", test_argv):
            with patch("g13_linux.gui.main.acquire_instance_lock", return_value=True):
                with patch("g13_linux.gui.main.QApplication") as mock_app_cls:
                    mock_app = MagicMock()
                    mock_app.exec.return_value = 0
                    mock_app_cls.return_value = mock_app

                    with patch("g13_linux.gui.views.main_window.MainWindow") as mock_window_cls:
                        mock_window = MagicMock()
                        mock_window_cls.return_value = mock_window

                        with patch(
                            "g13_linux.gui.controllers.app_controller.ApplicationController"
                        ) as mock_ctrl_cls:
                            mock_ctrl = MagicMock()
                            mock_ctrl_cls.return_value = mock_ctrl

                            result = main()

                            # Should have created controller with libusb=True
                            mock_ctrl_cls.assert_called_once()
                            call_kwargs = mock_ctrl_cls.call_args[1]
                            assert call_kwargs.get("use_libusb") is True

                            assert result == 0

    def test_main_controller_start_error(self, qapp):
        """Test main() handles controller.start() error."""
        from g13_linux.gui.main import main

        with patch.object(sys, "argv", ["g13-linux-gui"]):
            with patch("g13_linux.gui.main.acquire_instance_lock", return_value=True):
                with patch("g13_linux.gui.main.QApplication") as mock_app_cls:
                    mock_app = MagicMock()
                    mock_app.exec.return_value = 0
                    mock_app_cls.return_value = mock_app

                    with patch("g13_linux.gui.views.main_window.MainWindow") as mock_window_cls:
                        mock_window = MagicMock()
                        mock_window_cls.return_value = mock_window

                        with patch(
                            "g13_linux.gui.controllers.app_controller.ApplicationController"
                        ) as mock_ctrl_cls:
                            mock_ctrl = MagicMock()
                            mock_ctrl.start.side_effect = Exception("No device")
                            mock_ctrl_cls.return_value = mock_ctrl

                            with patch("g13_linux.gui.main.QMessageBox") as mock_msgbox:
                                result = main()

                                # Should show warning but continue
                                mock_msgbox.warning.assert_called_once()
                                mock_app.exec.assert_called_once()
                                assert result == 0

    def test_main_startup_error(self, qapp):
        """Test main() handles MainWindow exception."""
        from g13_linux.gui.main import main

        with patch.object(sys, "argv", ["g13-linux-gui"]):
            with patch("g13_linux.gui.main.acquire_instance_lock", return_value=True):
                with patch("g13_linux.gui.main.QApplication") as mock_app_cls:
                    mock_app = MagicMock()
                    mock_app_cls.return_value = mock_app

                    with patch("g13_linux.gui.views.main_window.MainWindow") as mock_window_cls:
                        mock_window_cls.side_effect = Exception("Startup failed")

                        with patch("g13_linux.gui.main.QMessageBox") as mock_msgbox:
                            result = main()

                            mock_msgbox.critical.assert_called_once()
                            assert result == 1


class TestMainImportErrors:
    """Test import error handling in main().

    Note: Lines 29-31 in main.py handle PyQt6 not being installed.
    This can only be tested via subprocess since PyQt6 is installed
    in our test environment. The subprocess test verifies the code path
    but cannot contribute to coverage.py metrics.
    """

    def test_main_gui_import_error(self, qapp):
        """Test main() handles GUI component import error."""
        import importlib

        from g13_linux.gui.main import main

        with patch.object(sys, "argv", ["g13-linux-gui"]):
            with patch("g13_linux.gui.main.acquire_instance_lock", return_value=True):
                with patch("g13_linux.gui.main.QApplication") as mock_app_cls:
                    mock_app = MagicMock()
                    mock_app_cls.return_value = mock_app

                    with patch("g13_linux.gui.main.QMessageBox") as mock_msgbox:
                        # Reload module to trigger fresh import attempt
                        # Mock the relative import to fail
                        original_import = importlib.import_module

                        def mock_import(name, *args, **kwargs):
                            if "main_window" in name:
                                raise ImportError("Missing MainWindow")
                            return original_import(name, *args, **kwargs)

                        # We need to make the relative import in main() fail
                        # The import happens inside the function, so we patch where it's looked up
                        with patch.object(importlib, "import_module", side_effect=mock_import):
                            # The import in main() uses relative import syntax
                            # We need to patch the __import__ builtin
                            import builtins

                            original_builtin_import = builtins.__import__

                            def blocking_import(
                                name, globals=None, locals=None, fromlist=(), level=0
                            ):
                                if level > 0 and fromlist:
                                    # Relative import
                                    if "main_window" in fromlist or "MainWindow" in fromlist:
                                        raise ImportError("Missing main_window")
                                return original_builtin_import(
                                    name, globals, locals, fromlist, level
                                )

                            with patch.object(builtins, "__import__", blocking_import):
                                result = main()

                                mock_msgbox.critical.assert_called_once()
                                assert result == 1
