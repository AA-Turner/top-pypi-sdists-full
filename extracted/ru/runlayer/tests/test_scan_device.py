"""Tests for device identification."""

import os
import uuid
from pathlib import Path
from unittest import mock


from runlayer_cli.scan.device import (
    DEVICE_ID_NAMESPACE,
    _get_hardware_machine_id,
    _get_linux_hardware_id,
    _get_macos_console_user,
    _get_macos_hardware_id,
    _get_windows_hardware_id,
    detect_wsl,
    get_device_metadata,
    get_or_create_device_id,
    get_wsl_user_homes,
    list_wsl_distros,
)


class TestGetOrCreateDeviceId:
    @mock.patch.dict(os.environ, {"RUNLAYER_DEVICE_ID": "env-device-id"})
    def test_uses_env_var_if_set(self):
        """Uses environment variable when set."""
        result = get_or_create_device_id()
        assert result == "env-device-id"

    def test_creates_new_id_if_not_exists(self, tmp_path):
        """Creates new UUID if no existing ID and no hardware id."""
        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value=None,
            ),
            mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=tmp_path / "device_id",
            ),
            mock.patch.dict(os.environ, {}, clear=True),
        ):
            # Clear RUNLAYER_DEVICE_ID if it exists
            os.environ.pop("RUNLAYER_DEVICE_ID", None)
            result = get_or_create_device_id()
            # Should be valid UUID format
            assert len(result) == 36
            assert result.count("-") == 4

    def test_reuses_stored_id(self, tmp_path):
        """Reuses stored device ID when no hardware id is available."""
        device_id_file = tmp_path / "device_id"
        device_id_file.write_text("stored-device-id")

        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value=None,
            ),
            mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=device_id_file,
            ),
            mock.patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("RUNLAYER_DEVICE_ID", None)
            result = get_or_create_device_id()
            assert result == "stored-device-id"

    def test_stores_new_id_to_file(self, tmp_path):
        """Stores newly generated ID to file when no hardware id is available."""
        device_id_file = tmp_path / "runlayer" / "device_id"

        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value=None,
            ),
            mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=device_id_file,
            ),
            mock.patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("RUNLAYER_DEVICE_ID", None)
            result = get_or_create_device_id()

            # File should now exist with the ID
            assert device_id_file.exists()
            assert device_id_file.read_text() == result


class TestGetOrCreateDeviceIdStability:
    """device_id must be stable per physical machine, not per user/home.

    These reproduce the over-counting bug: under MDM the scan runs per console
    user, so a per-home random/stored UUID mints a new device_id per user and
    inflates COUNT(DISTINCT device_id) on the MDM card.
    """

    def test_prefers_hardware_id_over_stored_file(self, tmp_path):
        """A stable hardware id wins over a previously stored per-user UUID."""
        stored = tmp_path / "device_id"
        stored.write_text("stored-per-user-uuid")

        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value="hardware-uuid",
            ),
            mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=stored,
            ),
            mock.patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("RUNLAYER_DEVICE_ID", None)
            result = get_or_create_device_id()

        assert result == "hardware-uuid"

    def test_hardware_id_independent_of_home(self):
        """Same machine, different user homes -> same device id, no file write."""
        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value="hardware-uuid",
            ),
            mock.patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("RUNLAYER_DEVICE_ID", None)
            with mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=Path("/home/alice/.runlayer/device_id"),
            ):
                result_alice = get_or_create_device_id()
            with mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=Path("/home/bob/.runlayer/device_id"),
            ):
                result_bob = get_or_create_device_id()

        assert result_alice == result_bob == "hardware-uuid"

    def test_env_var_takes_precedence_over_hardware(self):
        """Explicit override still wins over the hardware id."""
        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value="hardware-uuid",
            ),
            mock.patch.dict(os.environ, {"RUNLAYER_DEVICE_ID": "env-id"}),
        ):
            result = get_or_create_device_id()

        assert result == "env-id"

    def test_falls_back_to_stored_file_when_no_hardware(self, tmp_path):
        """Hosts without a readable hardware id keep the stored-file behavior."""
        stored = tmp_path / "device_id"
        stored.write_text("stored-device-id")

        with (
            mock.patch(
                "runlayer_cli.scan.device._get_hardware_machine_id",
                return_value=None,
            ),
            mock.patch(
                "runlayer_cli.scan.device._get_device_id_path",
                return_value=stored,
            ),
            mock.patch.dict(os.environ, {}, clear=True),
        ):
            os.environ.pop("RUNLAYER_DEVICE_ID", None)
            result = get_or_create_device_id()

        assert result == "stored-device-id"


class TestHardwareMachineId:
    """Dispatch + uuid5 wrapping for _get_hardware_machine_id."""

    @mock.patch("platform.system", return_value="Darwin")
    @mock.patch(
        "runlayer_cli.scan.device._get_macos_hardware_id", return_value="RAW-MAC"
    )
    def test_macos_dispatch_wrapped_in_uuid5(self, _mac, _system):
        result = _get_hardware_machine_id()
        assert result == str(uuid.uuid5(DEVICE_ID_NAMESPACE, "RAW-MAC"))

    @mock.patch("platform.system", return_value="Windows")
    @mock.patch(
        "runlayer_cli.scan.device._get_windows_hardware_id", return_value="RAW-WIN"
    )
    def test_windows_dispatch_wrapped_in_uuid5(self, _win, _system):
        result = _get_hardware_machine_id()
        assert result == str(uuid.uuid5(DEVICE_ID_NAMESPACE, "RAW-WIN"))

    @mock.patch("platform.system", return_value="Linux")
    @mock.patch(
        "runlayer_cli.scan.device._get_linux_hardware_id", return_value="RAW-LINUX"
    )
    def test_linux_dispatch_wrapped_in_uuid5(self, _lin, _system):
        result = _get_hardware_machine_id()
        assert result == str(uuid.uuid5(DEVICE_ID_NAMESPACE, "RAW-LINUX"))

    def test_uuid5_is_deterministic_and_uuid_shaped(self):
        first = str(uuid.uuid5(DEVICE_ID_NAMESPACE, "RAW-MAC"))
        second = str(uuid.uuid5(DEVICE_ID_NAMESPACE, "RAW-MAC"))
        assert first == second
        assert len(first) == 36
        assert first.count("-") == 4

    @mock.patch("platform.system", return_value="Darwin")
    @mock.patch("runlayer_cli.scan.device._get_macos_hardware_id", return_value=None)
    def test_returns_none_when_no_hardware_id(self, _mac, _system):
        assert _get_hardware_machine_id() is None

    @mock.patch("platform.system", return_value="SunOS")
    def test_returns_none_on_unknown_platform(self, _system):
        assert _get_hardware_machine_id() is None


class TestMacosHardwareId:
    @mock.patch("subprocess.run")
    def test_parses_ioplatform_uuid(self, mock_run):
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout=(
                "  +-o IOPlatformExpertDevice  <class IOPlatformExpertDevice>\n"
                '      "IOPlatformUUID" = "ABCDEF12-3456-7890-ABCD-EF1234567890"\n'
            ),
        )
        result = _get_macos_hardware_id()
        assert result == "ABCDEF12-3456-7890-ABCD-EF1234567890"

    @mock.patch("subprocess.run")
    def test_returns_none_when_uuid_absent(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=0, stdout="no uuid here\n")
        assert _get_macos_hardware_id() is None

    @mock.patch("subprocess.run")
    def test_returns_none_on_nonzero_exit(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=1, stdout="")
        assert _get_macos_hardware_id() is None

    @mock.patch("subprocess.run", side_effect=Exception("ioreg missing"))
    def test_returns_none_on_error(self, _run):
        assert _get_macos_hardware_id() is None


class TestWindowsHardwareId:
    def test_reads_machine_guid(self):
        fake_winreg = mock.MagicMock()
        fake_key = mock.MagicMock()
        fake_winreg.OpenKey.return_value.__enter__.return_value = fake_key
        fake_winreg.QueryValueEx.return_value = ("machine-guid-1234", 1)

        with mock.patch("runlayer_cli.scan.device.winreg", fake_winreg):
            result = _get_windows_hardware_id()

        assert result == "machine-guid-1234"

    def test_returns_none_on_registry_error(self):
        fake_winreg = mock.MagicMock()
        fake_winreg.OpenKey.side_effect = OSError("no such key")

        with mock.patch("runlayer_cli.scan.device.winreg", fake_winreg):
            result = _get_windows_hardware_id()

        assert result is None

    def test_returns_none_when_winreg_unavailable(self):
        with mock.patch("runlayer_cli.scan.device.winreg", None):
            assert _get_windows_hardware_id() is None


class TestLinuxHardwareId:
    @mock.patch("pathlib.Path.read_text", return_value="linux-machine-id-123\n")
    def test_reads_machine_id(self, _read):
        assert _get_linux_hardware_id() == "linux-machine-id-123"

    @mock.patch("pathlib.Path.read_text", side_effect=OSError("not found"))
    def test_returns_none_when_unreadable(self, _read):
        assert _get_linux_hardware_id() is None


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


class TestDetectWSL:
    @mock.patch.dict(os.environ, {"WSL_DISTRO_NAME": "Ubuntu"})
    def test_detects_wsl_via_env_var(self):
        assert detect_wsl() is True

    @mock.patch.dict(os.environ, {}, clear=True)
    @mock.patch(
        "pathlib.Path.read_text",
        return_value="Linux version 5.15.0-1-microsoft-standard-WSL2",
    )
    def test_detects_wsl_via_proc_version(self, _read):
        os.environ.pop("WSL_DISTRO_NAME", None)
        assert detect_wsl() is True

    @mock.patch.dict(os.environ, {}, clear=True)
    @mock.patch(
        "pathlib.Path.read_text",
        return_value="Linux version 6.1.0-generic #1 SMP Debian",
    )
    def test_returns_false_on_native_linux(self, _read):
        os.environ.pop("WSL_DISTRO_NAME", None)
        assert detect_wsl() is False

    @mock.patch.dict(os.environ, {}, clear=True)
    @mock.patch("pathlib.Path.read_text", side_effect=OSError("not found"))
    def test_returns_false_when_proc_version_missing(self, _read):
        os.environ.pop("WSL_DISTRO_NAME", None)
        assert detect_wsl() is False


class TestListWSLDistros:
    @mock.patch("subprocess.run")
    def test_parses_utf16_distro_list(self, mock_run):
        # wsl.exe --list --quiet emits UTF-16LE, often with a BOM.
        raw = "\ufeffUbuntu\r\nDebian\r\n".encode("utf-16-le")
        mock_run.return_value = mock.Mock(stdout=raw, returncode=0)
        assert list_wsl_distros() == ["Ubuntu", "Debian"]

    @mock.patch("subprocess.run")
    def test_drops_docker_desktop_data(self, mock_run):
        raw = "Ubuntu\r\ndocker-desktop-data\r\n".encode("utf-16-le")
        mock_run.return_value = mock.Mock(stdout=raw, returncode=0)
        assert list_wsl_distros() == ["Ubuntu"]

    @mock.patch("subprocess.run")
    def test_returns_empty_on_nonzero_exit(self, mock_run):
        mock_run.return_value = mock.Mock(stdout=b"", returncode=1)
        assert list_wsl_distros() == []

    @mock.patch("subprocess.run", side_effect=FileNotFoundError("wsl.exe"))
    def test_returns_empty_when_wsl_missing(self, _run):
        assert list_wsl_distros() == []


class TestGetWSLUserHomes:
    def test_lists_home_dirs_via_unc(self, tmp_path):
        home_base = tmp_path / "home"
        home_base.mkdir()
        (home_base / "alex").mkdir()
        (home_base / "sam").mkdir()
        (home_base / "afile").write_text("x")

        def fake_path(p):
            text = str(p)
            text = text.replace(R"\\wsl.localhost\Ubuntu", str(tmp_path))
            return Path(text)

        with mock.patch("runlayer_cli.scan.device.Path", side_effect=fake_path):
            homes = get_wsl_user_homes("Ubuntu")

        names = sorted(h.name for h in homes)
        assert names == ["alex", "sam"]

    def test_returns_empty_when_unreachable(self, tmp_path):
        def fake_path(p):
            return Path(str(p).replace(R"\\wsl.localhost\Ubuntu", str(tmp_path)))

        with mock.patch("runlayer_cli.scan.device.Path", side_effect=fake_path):
            assert get_wsl_user_homes("Ubuntu") == []


class TestDeviceMetadataWSL:
    @mock.patch("platform.system", return_value="Linux")
    @mock.patch("runlayer_cli.scan.device.detect_wsl", return_value=True)
    def test_includes_is_wsl_flag(self, _wsl, _system):
        result = get_device_metadata()
        assert result["is_wsl"] is True
        assert result["os"] == "linux"

    @mock.patch("platform.system", return_value="Linux")
    @mock.patch("runlayer_cli.scan.device.detect_wsl", return_value=False)
    def test_no_wsl_flag_on_native_linux(self, _wsl, _system):
        result = get_device_metadata()
        assert "is_wsl" not in result
        assert result["os"] == "linux"

    @mock.patch("platform.system", return_value="Darwin")
    def test_no_wsl_flag_on_macos(self, _system):
        result = get_device_metadata()
        assert "is_wsl" not in result


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
