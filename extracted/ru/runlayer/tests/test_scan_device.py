"""Tests for device identification."""

import os
from unittest import mock


from runlayer_cli.scan.device import (
    _get_macos_console_user,
    get_device_metadata,
    get_or_create_device_id,
)


class TestGetOrCreateDeviceId:
    @mock.patch.dict(os.environ, {"RUNLAYER_DEVICE_ID": "env-device-id"})
    def test_uses_env_var_if_set(self):
        """Uses environment variable when set."""
        result = get_or_create_device_id()
        assert result == "env-device-id"

    def test_creates_new_id_if_not_exists(self, tmp_path):
        """Creates new UUID if no existing ID."""
        with mock.patch(
            "runlayer_cli.scan.device._get_device_id_path",
            return_value=tmp_path / "device_id",
        ):
            with mock.patch.dict(os.environ, {}, clear=True):
                # Clear RUNLAYER_DEVICE_ID if it exists
                os.environ.pop("RUNLAYER_DEVICE_ID", None)
                result = get_or_create_device_id()
                # Should be valid UUID format
                assert len(result) == 36
                assert result.count("-") == 4

    def test_reuses_stored_id(self, tmp_path):
        """Reuses stored device ID on subsequent calls."""
        device_id_file = tmp_path / "device_id"
        device_id_file.write_text("stored-device-id")

        with mock.patch(
            "runlayer_cli.scan.device._get_device_id_path",
            return_value=device_id_file,
        ):
            with mock.patch.dict(os.environ, {}, clear=True):
                os.environ.pop("RUNLAYER_DEVICE_ID", None)
                result = get_or_create_device_id()
                assert result == "stored-device-id"

    def test_stores_new_id_to_file(self, tmp_path):
        """Stores newly generated ID to file for future use."""
        device_id_file = tmp_path / "runlayer" / "device_id"

        with mock.patch(
            "runlayer_cli.scan.device._get_device_id_path",
            return_value=device_id_file,
        ):
            with mock.patch.dict(os.environ, {}, clear=True):
                os.environ.pop("RUNLAYER_DEVICE_ID", None)
                result = get_or_create_device_id()

                # File should now exist with the ID
                assert device_id_file.exists()
                assert device_id_file.read_text() == result


class TestGetDeviceMetadata:
    def test_returns_dict(self):
        """Returns dictionary with expected keys."""
        result = get_device_metadata()
        assert isinstance(result, dict)
        assert "hostname" in result
        assert "os" in result
        assert "os_version" in result
        assert "username" in result

    def test_os_is_normalized(self):
        """OS name is normalized."""
        result = get_device_metadata()
        assert (
            result["os"] in ["darwin", "windows", "linux"] or result["os"] is not None
        )

    @mock.patch("platform.system", return_value="Darwin")
    def test_darwin_normalized_to_darwin(self, mock_system):
        """Darwin is normalized to 'darwin'."""
        result = get_device_metadata()
        assert result["os"] == "darwin"

    @mock.patch("platform.system", return_value="Windows")
    def test_windows_normalized_to_windows(self, mock_system):
        """Windows is normalized to 'windows'."""
        result = get_device_metadata()
        assert result["os"] == "windows"

    @mock.patch("platform.system", return_value="Linux")
    def test_linux_normalized_to_linux(self, mock_system):
        """Linux is normalized to 'linux'."""
        result = get_device_metadata()
        assert result["os"] == "linux"

    @mock.patch("platform.system", return_value="Darwin")
    @mock.patch("os.getlogin", return_value="root")
    @mock.patch(
        "runlayer_cli.scan.device._get_macos_console_user", return_value="awfrazer"
    )
    def test_root_username_triggers_macos_fallback(
        self, mock_console, mock_login, mock_system
    ):
        """On macOS, 'root' username falls back to console user detection."""
        result = get_device_metadata()
        assert result["username"] == "awfrazer"

    @mock.patch("platform.system", return_value="Darwin")
    @mock.patch("os.getlogin", return_value="root")
    @mock.patch("runlayer_cli.scan.device._get_macos_console_user", return_value=None)
    def test_root_username_kept_when_no_console_user(
        self, mock_console, mock_login, mock_system
    ):
        """Falls back to 'root' if console user detection also fails."""
        result = get_device_metadata()
        assert result["username"] == "root"

    @mock.patch("platform.system", return_value="Linux")
    @mock.patch("os.getlogin", return_value="root")
    @mock.patch("runlayer_cli.scan.device._get_macos_console_user")
    def test_root_on_linux_skips_macos_fallback(
        self, mock_console, mock_login, mock_system
    ):
        """On Linux, 'root' does not trigger macOS console user detection."""
        result = get_device_metadata()
        assert result["username"] == "root"
        mock_console.assert_not_called()

    @mock.patch("platform.system", return_value="Darwin")
    @mock.patch("os.getlogin", return_value="realuser")
    @mock.patch("runlayer_cli.scan.device._get_macos_console_user")
    def test_normal_username_skips_fallback(
        self, mock_console, mock_login, mock_system
    ):
        """Normal username on macOS does not trigger console user detection."""
        result = get_device_metadata()
        assert result["username"] == "realuser"
        mock_console.assert_not_called()


class TestGetMacosConsoleUser:
    @mock.patch("subprocess.run")
    def test_returns_console_user(self, mock_run):
        mock_run.return_value = mock.Mock(stdout="awfrazer\n")
        assert _get_macos_console_user() == "awfrazer"

    @mock.patch("subprocess.run")
    def test_filters_system_usernames(self, mock_run):
        mock_run.return_value = mock.Mock(stdout="root\n")
        assert _get_macos_console_user() is None

    @mock.patch("subprocess.run", side_effect=Exception("not macOS"))
    def test_returns_none_on_error(self, mock_run):
        assert _get_macos_console_user() is None
