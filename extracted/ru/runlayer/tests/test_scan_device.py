"""Tests for device identification."""

import os
import uuid
from pathlib import Path
from unittest import mock

import pytest


from runlayer_cli.scan.device import (
    DEVICE_ID_NAMESPACE,
    WSLRegistryMetadata,
    _get_hardware_machine_id,
    _get_linux_hardware_id,
    _get_linux_serial_number,
    _get_macos_console_user,
    _get_macos_hardware_id,
    _get_macos_serial_number,
    _get_serial_number,
    _get_windows_hardware_id,
    _get_windows_serial_number,
    _parse_wsl_verbose_output,
    _quiet_fallback_inventory,
    _read_macos_ioplatform_device,
    _read_wsl_registry_metadata,
    _reject_placeholder_serial,
    detect_wsl,
    get_device_metadata,
    get_or_create_device_id,
    get_wsl_distro_inventory,
    get_wsl_user_homes,
    list_wsl_distros,
)
from runlayer_cli.scan.wsl_limits import (
    MAX_WSL_DISTROS,
    MAX_WSL_HOMES,
    MAX_WSL_HOME_PROBES,
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

    def setup_method(self):
        _get_hardware_machine_id.cache_clear()

    def teardown_method(self):
        _get_hardware_machine_id.cache_clear()

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
    def setup_method(self):
        # _get_macos_hardware_id reads a single cached ioreg parse; clear it so
        # each test's mocked subprocess output is re-read.
        _read_macos_ioplatform_device.cache_clear()

    def teardown_method(self):
        _read_macos_ioplatform_device.cache_clear()

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

    def test_machine_id_path_override(self, tmp_path):
        """RUNLAYER_MACHINE_ID_PATH is read first (bind-mounted host id)."""
        mid = tmp_path / "host-machine-id"
        mid.write_text("host-mid-abc\n")
        with mock.patch.dict(
            os.environ, {"RUNLAYER_MACHINE_ID_PATH": str(mid)}, clear=False
        ):
            assert _get_linux_hardware_id() == "host-mid-abc"

    def test_machine_id_override_falls_back_when_missing(self, tmp_path):
        """A missing override path falls through to the default locations."""
        missing = tmp_path / "nope"

        def fake_read_text(self, *a, **k):
            if str(self) == str(missing):
                raise OSError("not found")
            return "default-mid\n"

        with (
            mock.patch.dict(
                os.environ, {"RUNLAYER_MACHINE_ID_PATH": str(missing)}, clear=False
            ),
            mock.patch.object(
                Path, "read_text", autospec=True, side_effect=fake_read_text
            ),
        ):
            assert _get_linux_hardware_id() == "default-mid"


class TestMacosSerialNumber:
    def setup_method(self):
        _read_macos_ioplatform_device.cache_clear()

    def teardown_method(self):
        _read_macos_ioplatform_device.cache_clear()

    @mock.patch("subprocess.run")
    def test_parses_ioplatform_serial(self, mock_run):
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout=(
                "  +-o IOPlatformExpertDevice  <class IOPlatformExpertDevice>\n"
                '      "IOPlatformUUID" = "ABCDEF12-3456-7890-ABCD-EF1234567890"\n'
                '      "IOPlatformSerialNumber" = "C02XYZ123ABC"\n'
            ),
        )
        assert _get_macos_serial_number() == "C02XYZ123ABC"

    @mock.patch("subprocess.run")
    def test_returns_none_when_serial_absent(self, mock_run):
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout='      "IOPlatformUUID" = "ABCDEF12-3456-7890-ABCD-EF1234567890"\n',
        )
        assert _get_macos_serial_number() is None

    @mock.patch("subprocess.run")
    def test_returns_none_on_nonzero_exit(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=1, stdout="")
        assert _get_macos_serial_number() is None

    @mock.patch("subprocess.run", side_effect=Exception("ioreg missing"))
    def test_returns_none_on_error(self, _run):
        assert _get_macos_serial_number() is None

    @mock.patch("subprocess.run")
    def test_single_ioreg_call_feeds_uuid_and_serial(self, mock_run):
        """UUID + serial come from one cached ioreg invocation (the raw serial
        rides the existing device-id probe)."""
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout=(
                '      "IOPlatformUUID" = "ABCDEF12-3456-7890-ABCD-EF1234567890"\n'
                '      "IOPlatformSerialNumber" = "C02XYZ123ABC"\n'
            ),
        )
        assert _get_macos_hardware_id() == "ABCDEF12-3456-7890-ABCD-EF1234567890"
        assert _get_macos_serial_number() == "C02XYZ123ABC"
        assert mock_run.call_count == 1


class TestWindowsSerialNumber:
    @mock.patch("subprocess.run")
    def test_reads_bios_serial(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=0, stdout="WINSERIAL123\r\n")
        assert _get_windows_serial_number() == "WINSERIAL123"

    @mock.patch("subprocess.run")
    def test_returns_none_on_empty_output(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=0, stdout="   \n")
        assert _get_windows_serial_number() is None

    @mock.patch("subprocess.run")
    def test_returns_none_on_nonzero_exit(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=1, stdout="whatever")
        assert _get_windows_serial_number() is None

    @mock.patch("subprocess.run", side_effect=Exception("powershell missing"))
    def test_returns_none_on_error(self, _run):
        assert _get_windows_serial_number() is None


class TestLinuxSerialNumber:
    @mock.patch("pathlib.Path.read_text", return_value="LINUXSERIAL123\n")
    def test_reads_dmi_serial(self, _read):
        assert _get_linux_serial_number() == "LINUXSERIAL123"

    @mock.patch("pathlib.Path.read_text", side_effect=OSError("permission denied"))
    def test_returns_none_when_unreadable(self, _read):
        assert _get_linux_serial_number() is None

    @mock.patch("pathlib.Path.read_text", return_value="  \n")
    def test_returns_none_on_blank(self, _read):
        assert _get_linux_serial_number() is None


class TestGetSerialNumber:
    """Per-OS dispatch for the cached _get_serial_number."""

    def setup_method(self):
        _get_serial_number.cache_clear()

    def teardown_method(self):
        _get_serial_number.cache_clear()

    @mock.patch("platform.system", return_value="Darwin")
    @mock.patch(
        "runlayer_cli.scan.device._get_macos_serial_number", return_value="MAC-SER"
    )
    def test_macos_dispatch(self, _mac, _system):
        assert _get_serial_number() == "MAC-SER"

    @mock.patch("platform.system", return_value="Windows")
    @mock.patch(
        "runlayer_cli.scan.device._get_windows_serial_number", return_value="WIN-SER"
    )
    def test_windows_dispatch(self, _win, _system):
        assert _get_serial_number() == "WIN-SER"

    @mock.patch("platform.system", return_value="Linux")
    @mock.patch(
        "runlayer_cli.scan.device._get_linux_serial_number", return_value="LNX-SER"
    )
    def test_linux_dispatch(self, _lin, _system):
        assert _get_serial_number() == "LNX-SER"

    @mock.patch("platform.system", return_value="SunOS")
    def test_returns_none_on_unknown_platform(self, _system):
        assert _get_serial_number() is None

    @mock.patch("platform.system", return_value="Windows")
    @mock.patch(
        "runlayer_cli.scan.device._get_windows_serial_number",
        return_value="To be filled by O.E.M.",
    )
    def test_placeholder_from_platform_probe_is_dropped(self, _win, _system):
        """A placeholder reported by the OS probe never leaves the device."""
        assert _get_serial_number() is None


class TestRejectPlaceholderSerial:
    """Known SMBIOS/DMI junk placeholders are filtered to None; real serials
    (and unusual-but-real ones) pass through untouched."""

    def test_none_passthrough(self):
        assert _reject_placeholder_serial(None) is None

    def test_real_serial_passes_through_unchanged(self):
        assert _reject_placeholder_serial("C02XYZ123ABC") == "C02XYZ123ABC"

    def test_blank_and_whitespace_only_become_none(self):
        assert _reject_placeholder_serial("") is None
        assert _reject_placeholder_serial("   ") is None

    @pytest.mark.parametrize(
        "value",
        [
            "None",
            "none",
            "Not Applicable",
            "Not Specified",
            "Not Available",
            "System Serial Number",
            "To be filled by O.E.M.",
            "To Be Filled By O.E.M.",
            "To be filled by O.E.M",
            "Default string",
            "  Default   String  ",  # surrounding + repeated whitespace collapsed
        ],
    )
    def test_known_placeholders_become_none(self, value):
        assert _reject_placeholder_serial(value) is None

    def test_serial_containing_placeholder_substring_is_kept(self):
        """Only whole-string matches are rejected — a real serial that merely
        contains a placeholder word is not discarded."""
        assert (
            _reject_placeholder_serial("DEFAULT-STRING-1234") == "DEFAULT-STRING-1234"
        )


class TestGetDeviceMetadata:
    def test_hostname_env_override(self):
        """RUNLAYER_HOSTNAME overrides the detected hostname (K8s node name)."""
        with mock.patch.dict(
            os.environ, {"RUNLAYER_HOSTNAME": "node-42.internal"}, clear=False
        ):
            assert get_device_metadata()["hostname"] == "node-42.internal"

    def test_hostname_falls_back_to_gethostname(self):
        """Absent the override, socket.gethostname() is used."""
        with (
            mock.patch.dict(os.environ, {}, clear=False),
            mock.patch("socket.gethostname", return_value="real-host"),
        ):
            os.environ.pop("RUNLAYER_HOSTNAME", None)
            assert get_device_metadata()["hostname"] == "real-host"

    def test_returns_dict(self):
        """Returns dictionary with expected keys."""
        result = get_device_metadata()
        assert isinstance(result, dict)
        assert "hostname" in result
        assert "os" in result
        assert "os_version" in result
        assert "username" in result
        assert "serial_number" in result

    @mock.patch("runlayer_cli.scan.device._get_serial_number", return_value="SER-123")
    def test_includes_serial_number(self, _serial):
        """The collected hardware serial is attached to device metadata."""
        result = get_device_metadata()
        assert result["serial_number"] == "SER-123"

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


def _wsl_list_side_effect(**outcomes):
    """Route mocked ``wsl.exe --list`` calls by variant.

    Keys: ``verbose``, ``quiet``, ``running``. Values are a mock result or an
    exception to raise. Unlisted variants fail the test if called.
    """

    def run(cmd, **_kwargs):
        assert cmd[:2] == ["wsl.exe", "--list"]
        variant = {
            ("--verbose",): "verbose",
            ("--quiet",): "quiet",
            ("--running", "--quiet"): "running",
        }[tuple(cmd[2:])]
        outcome = outcomes[variant]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return run


class TestListWSLDistros:
    def setup_method(self):
        get_wsl_distro_inventory.cache_clear()

    def teardown_method(self):
        get_wsl_distro_inventory.cache_clear()

    @mock.patch("subprocess.run")
    def test_parses_utf16_verbose_inventory(self, mock_run):
        raw = (
            "\ufeff  NAME                   STATE           VERSION\r\n"
            "* Ubuntu 24.04           Running         2\r\n"
            "  Debian                  Stopped         1\r\n"
            "  docker-desktop-data     Stopped         2\r\n"
        ).encode("utf-16-le")
        mock_run.return_value = mock.Mock(stdout=raw, returncode=0)

        inventory = get_wsl_distro_inventory()

        assert inventory.success is True
        assert mock_run.call_args.kwargs["env"]["WSL_UTF8"] == "1"
        assert [distro.to_api_payload() for distro in inventory.distros] == [
            {
                "distro_name": "Ubuntu 24.04",
                "wsl_version": 2,
                "is_running": True,
                "scanned": False,
                "container_runtimes": [],
            },
            {
                "distro_name": "Debian",
                "wsl_version": 1,
                "is_running": False,
                "scanned": False,
                "container_runtimes": [],
            },
        ]
        assert list_wsl_distros() == ["Ubuntu 24.04", "Debian"]
        mock_run.assert_called_once()
        assert mock_run.call_args.args[0] == ["wsl.exe", "--list", "--verbose"]
        assert mock_run.call_args.kwargs["capture_output"] is True
        assert mock_run.call_args.kwargs["timeout"] == 10

    def test_successful_empty_inventory(self):
        inventory = _parse_wsl_verbose_output("NAME STATE VERSION\r\n")

        assert inventory.success is True
        assert inventory.distros == ()

    def test_malformed_inventory_is_incomplete_but_keeps_valid_rows(self):
        inventory = _parse_wsl_verbose_output(
            "NAME STATE VERSION\r\nUbuntu Running 2\r\nthis row has no version\r\n"
        )

        assert inventory.success is False
        assert [distro.name for distro in inventory.distros] == ["Ubuntu"]

    def test_verbose_inventory_cap_retains_rows_but_is_incomplete(self):
        inventory = _parse_wsl_verbose_output(
            "NAME STATE VERSION\n"
            + "\n".join(
                f"Distro-{index} Running 2" for index in range(MAX_WSL_DISTROS + 1)
            )
        )

        assert len(inventory.distros) == MAX_WSL_DISTROS
        assert inventory.success is False

    def test_quiet_inventory_cap_retains_rows_but_is_incomplete(self, monkeypatch):
        from runlayer_cli.scan import device

        all_distros = "\n".join(
            f"Distro-{index}" for index in range(MAX_WSL_DISTROS + 1)
        )
        monkeypatch.setattr(
            device,
            "_run_wsl_list",
            lambda args: "" if args == ["--running", "--quiet"] else all_distros,
        )

        inventory = _quiet_fallback_inventory()

        assert len(inventory.distros) == MAX_WSL_DISTROS
        assert inventory.success is False

    @mock.patch("subprocess.run")
    def test_capped_quiet_fallback_remains_available_for_diagnostics(self, mock_run):
        quiet_rows = "\n".join(
            f"Distro-{index}" for index in range(MAX_WSL_DISTROS + 1)
        )
        mock_run.side_effect = _wsl_list_side_effect(
            verbose=mock.Mock(stdout="NOM ETAT VERSION\n", returncode=0),
            quiet=mock.Mock(stdout=quiet_rows, returncode=0),
            running=mock.Mock(stdout="", returncode=0),
        )

        inventory = get_wsl_distro_inventory()

        assert len(inventory.distros) == MAX_WSL_DISTROS
        assert inventory.success is False

    @mock.patch("subprocess.run")
    def test_incomplete_inventory_does_not_drive_discovery(self, mock_run):
        raw = (
            "\ufeff  NAME             STATE           VERSION\r\n"
            "* Ubuntu           Running         2\r\n"
            "  this row has no version\r\n"
        ).encode("utf-16-le")
        mock_run.side_effect = _wsl_list_side_effect(
            verbose=mock.Mock(stdout=raw, returncode=0),
            quiet=mock.Mock(stdout=b"", returncode=1),
        )

        inventory = get_wsl_distro_inventory()

        # Partial rows stay available for local diagnostics ...
        assert inventory.success is False
        assert [distro.name for distro in inventory.distros] == ["Ubuntu"]
        # ... but must not expand WSL homes or attribute WSL-scoped artifacts,
        # because the same scan omits the inventory the backend would need.
        assert list_wsl_distros() == []

    @mock.patch("subprocess.run")
    def test_localized_verbose_output_falls_back_to_quiet_listing(self, mock_run):
        # German console: localized header + multi-word Running state, which
        # the strict English verbose parse must not attempt to interpret.
        verbose_raw = (
            "\ufeff  NAME                   STATUS          VERSION\r\n"
            "* Ubuntu 24.04           Wird ausgeführt 2\r\n"
            "  Debian                  Beendet         1\r\n"
        ).encode("utf-16-le")
        quiet_raw = ("\ufeffUbuntu 24.04\r\nDebian\r\ndocker-desktop-data\r\n").encode(
            "utf-16-le"
        )
        running_raw = "\ufeffUbuntu 24.04\r\n".encode("utf-16-le")
        mock_run.side_effect = _wsl_list_side_effect(
            verbose=mock.Mock(stdout=verbose_raw, returncode=0),
            quiet=mock.Mock(stdout=quiet_raw, returncode=0),
            running=mock.Mock(stdout=running_raw, returncode=0),
        )

        inventory = get_wsl_distro_inventory()

        assert inventory.success is True
        assert [distro.to_api_payload() for distro in inventory.distros] == [
            {
                "distro_name": "Ubuntu 24.04",
                "wsl_version": None,
                "is_running": True,
                "scanned": False,
                "container_runtimes": [],
            },
            {
                "distro_name": "Debian",
                "wsl_version": None,
                "is_running": False,
                "scanned": False,
                "container_runtimes": [],
            },
        ]
        assert list_wsl_distros() == ["Ubuntu 24.04", "Debian"]

    @mock.patch("subprocess.run")
    def test_quiet_fallback_reports_repeated_running_query_failure(self, mock_run):
        mock_run.side_effect = _wsl_list_side_effect(
            verbose=mock.Mock(stdout=b"", returncode=1),
            quiet=mock.Mock(
                stdout="\ufeffUbuntu\r\n".encode("utf-16-le"), returncode=0
            ),
            running=mock.Mock(stdout=b"", returncode=1),
        )

        inventory = get_wsl_distro_inventory()

        assert inventory.success is False
        assert [distro.name for distro in inventory.distros] == ["Ubuntu"]
        running_calls = [
            call
            for call in mock_run.call_args_list
            if call.args[0] == ["wsl.exe", "--list", "--running", "--quiet"]
        ]
        assert len(running_calls) == 2

    @mock.patch("subprocess.run")
    def test_quiet_fallback_accepts_successful_empty_running_list(self, mock_run):
        mock_run.side_effect = _wsl_list_side_effect(
            verbose=mock.Mock(stdout=b"", returncode=1),
            quiet=mock.Mock(
                stdout="\ufeffUbuntu\r\n".encode("utf-16-le"), returncode=0
            ),
            running=mock.Mock(stdout=b"", returncode=0),
        )

        inventory = get_wsl_distro_inventory()

        assert inventory.success is True
        assert [distro.is_running for distro in inventory.distros] == [False]
        assert list_wsl_distros() == ["Ubuntu"]
        running_calls = [
            call
            for call in mock_run.call_args_list
            if call.args[0] == ["wsl.exe", "--list", "--running", "--quiet"]
        ]
        assert len(running_calls) == 1

    @mock.patch(
        "runlayer_cli.scan.device._read_wsl_registry_metadata",
        return_value={
            "ubuntu": WSLRegistryMetadata(version=2),
        },
    )
    @mock.patch("subprocess.run")
    def test_quiet_fallback_uses_registry_version(
        self,
        mock_run,
        _registry,
    ):
        mock_run.side_effect = _wsl_list_side_effect(
            verbose=mock.Mock(stdout=b"", returncode=1),
            quiet=mock.Mock(
                stdout="\ufeffUbuntu\r\n".encode("utf-16-le"),
                returncode=0,
            ),
            running=mock.Mock(
                stdout="\ufeffUbuntu\r\n".encode("utf-16-le"),
                returncode=0,
            ),
        )

        inventory = get_wsl_distro_inventory()

        assert inventory.success is True
        assert inventory.distros[0].wsl_version == 2

    def test_registry_metadata_reads_only_required_values(self):
        fake_winreg = mock.MagicMock()
        lxss_key = mock.MagicMock()
        distro_key = mock.MagicMock()
        lxss_context = mock.MagicMock()
        distro_context = mock.MagicMock()
        lxss_context.__enter__.return_value = lxss_key
        distro_context.__enter__.return_value = distro_key
        fake_winreg.OpenKey.side_effect = [lxss_context, distro_context]
        fake_winreg.QueryInfoKey.return_value = (1, 0, 0)
        fake_winreg.EnumKey.return_value = "{distro-id}"

        def query_value(key, name):
            assert key is distro_key
            if name == "DistributionName":
                return "Ubuntu", 1
            if name == "Version":
                return 2, 4
            raise AssertionError(f"unexpected registry value: {name}")

        fake_winreg.QueryValueEx.side_effect = query_value

        with mock.patch("runlayer_cli.scan.device.winreg", fake_winreg):
            metadata = _read_wsl_registry_metadata()

        assert metadata["ubuntu"].version == 2

    @pytest.mark.parametrize(
        "run_result,side_effect",
        [
            (mock.Mock(stdout=b"", returncode=1), None),
            (None, FileNotFoundError("wsl.exe")),
        ],
    )
    @mock.patch("subprocess.run")
    def test_command_failure_is_not_successful(
        self,
        mock_run,
        run_result,
        side_effect,
    ):
        mock_run.return_value = run_result
        mock_run.side_effect = side_effect

        inventory = get_wsl_distro_inventory()

        assert inventory.success is False
        assert inventory.distros == ()
        assert list_wsl_distros() == []


class TestGetWSLUserHomes:
    def test_lists_home_dirs_via_unc(self, tmp_path):
        home_base = tmp_path / "home"
        home_base.mkdir()
        (home_base / "alex").mkdir()
        (home_base / "sam").mkdir()
        (home_base / "afile").write_text("x")
        (tmp_path / "root").mkdir()

        def fake_path(p):
            text = str(p)
            text = text.replace(R"\\wsl.localhost\Ubuntu", str(tmp_path))
            return Path(text)

        with mock.patch("runlayer_cli.scan.device.Path", side_effect=fake_path):
            homes = get_wsl_user_homes("Ubuntu")

        names = sorted(h.name for h in homes)
        assert names == ["alex", "root", "sam"]

    def test_non_directories_do_not_consume_home_limit(self, tmp_path, monkeypatch):
        home_base = tmp_path / "home"
        home_base.mkdir()
        files = [home_base / f"file-{index}" for index in range(MAX_WSL_HOMES)]
        directories = [home_base / f"user-{index}" for index in range(MAX_WSL_HOMES)]
        for file_path in files:
            file_path.write_text("x")
        for directory in directories:
            directory.mkdir()

        def fake_path(path):
            return Path(str(path).replace(R"\\wsl.localhost\Ubuntu", str(tmp_path)))

        path_type = type(tmp_path)
        original_iterdir = path_type.iterdir

        def ordered_iterdir(path):
            if path == home_base:
                return iter([*files, *directories])
            return original_iterdir(path)

        monkeypatch.setattr("runlayer_cli.scan.device.Path", fake_path)
        monkeypatch.setattr(path_type, "iterdir", ordered_iterdir)

        homes = get_wsl_user_homes("Ubuntu")

        assert homes == directories

    def test_home_limit_uses_stable_sorted_subset(self, tmp_path, monkeypatch):
        home_base = tmp_path / "home"
        home_base.mkdir()
        directories = [
            home_base / name for name in ("zed", "charlie", "bob", "alice", "dave")
        ]
        for directory in directories:
            directory.mkdir()

        def fake_path(path):
            return Path(str(path).replace(R"\\wsl.localhost\Ubuntu", str(tmp_path)))

        path_type = type(tmp_path)
        original_iterdir = path_type.iterdir

        def reverse_iterdir(path):
            if path == home_base:
                return iter(reversed(directories))
            return original_iterdir(path)

        monkeypatch.setattr("runlayer_cli.scan.device.Path", fake_path)
        monkeypatch.setattr(path_type, "iterdir", reverse_iterdir)

        homes = get_wsl_user_homes("Ubuntu")

        assert homes == sorted(directories)[:MAX_WSL_HOMES]

    def test_caps_home_probes_during_iteration_with_root_first(
        self,
        tmp_path,
        monkeypatch,
    ):
        home_base = tmp_path / "home"
        home_base.mkdir()
        files = [
            home_base / f"file-{index}" for index in range(MAX_WSL_HOME_PROBES + 1)
        ]
        for file_path in files:
            file_path.write_text("x")
        (tmp_path / "root").mkdir()

        def fake_path(path):
            return Path(str(path).replace(R"\\wsl.localhost\Ubuntu", str(tmp_path)))

        path_type = type(tmp_path)
        original_iterdir = path_type.iterdir
        original_is_dir = path_type.is_dir
        entry_probes: list[str] = []

        def ordered_iterdir(path):
            if path == home_base:
                return iter(files)
            return original_iterdir(path)

        def tracked_is_dir(path):
            if path.parent == home_base:
                entry_probes.append(path.name)
            return original_is_dir(path)

        monkeypatch.setattr("runlayer_cli.scan.device.Path", fake_path)
        monkeypatch.setattr(path_type, "iterdir", ordered_iterdir)
        monkeypatch.setattr(path_type, "is_dir", tracked_is_dir)

        homes = get_wsl_user_homes("Ubuntu")

        assert [home.name for home in homes] == ["root"]
        assert len(entry_probes) == MAX_WSL_HOME_PROBES

    def test_bounds_home_enumeration_before_sorting(self, tmp_path, monkeypatch):
        home_base = tmp_path / "home"
        home_base.mkdir()
        directories = [
            home_base / f"user-{index:02d}"
            for index in reversed(range(MAX_WSL_HOME_PROBES))
        ]
        extra_directory = home_base / "user-extra"
        for directory in [*directories, extra_directory]:
            directory.mkdir()

        def fake_path(path):
            return Path(str(path).replace(R"\\wsl.localhost\Ubuntu", str(tmp_path)))

        path_type = type(tmp_path)
        original_iterdir = path_type.iterdir
        enumerated: list[Path] = []

        def bounded_iterdir(path):
            if path != home_base:
                return original_iterdir(path)

            def entries():
                for entry in [*directories, extra_directory]:
                    enumerated.append(entry)
                    yield entry

            return entries()

        monkeypatch.setattr("runlayer_cli.scan.device.Path", fake_path)
        monkeypatch.setattr(path_type, "iterdir", bounded_iterdir)

        homes = get_wsl_user_homes("Ubuntu")

        assert homes == sorted(directories)[:MAX_WSL_HOMES]
        assert len(enumerated) == MAX_WSL_HOME_PROBES

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


class TestStripReportedPathPrefix:
    """Container mount-prefix strip for scan-derived paths (RUNLAYER_STRIP_PATH_PREFIX)."""

    def _strip(self, value):
        from runlayer_cli.paths import strip_reported_path_prefix

        return strip_reported_path_prefix(value)

    def test_noop_when_env_unset(self, monkeypatch):
        monkeypatch.delenv("RUNLAYER_STRIP_PATH_PREFIX", raising=False)
        assert self._strip("/host/home/alice/.cursor") == "/host/home/alice/.cursor"

    def test_strips_prefix(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host")
        assert self._strip("/host/home/alice/.cursor") == "/home/alice/.cursor"

    def test_exact_prefix_becomes_root(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host")
        assert self._strip("/host") == "/"

    def test_non_prefixed_and_lookalike_paths_untouched(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host")
        assert self._strip("/home/alice") == "/home/alice"
        # Prefix must match a whole component: /hostile is NOT under /host.
        assert self._strip("/hostile/config") == "/hostile/config"

    def test_none_passthrough(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host")
        assert self._strip(None) is None

    def test_trailing_slash_prefix_normalized(self, monkeypatch):
        monkeypatch.setenv("RUNLAYER_STRIP_PATH_PREFIX", "/host/")
        assert self._strip("/host/root/projects/demo") == "/root/projects/demo"
