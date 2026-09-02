"""Tests for ``aiwatch setup hooks`` — strict-ordering guardrail + MDM/user scope writes."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.config import Config, url_to_host_key
from runlayer_cli.enrollment import enrollment_marker_path
from runlayer_cli.hook_install.browser_extension import BrowserExtensionResult
from runlayer_cli.install_window import InstallWindowState

runner = CliRunner()
UPDATE_URL = "https://downloads.runlayer.com/extension/update_manifest.xml"


@pytest.fixture(autouse=True)
def _stub_lifecycle_steps(monkeypatch):
    """Keep existing hook-config tests away from host launchd/SCM state."""
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.read_managed_config",
        lambda: {"sessions": True},
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._install_daemon_lifecycle_step",
        lambda _managed, **_kwargs: (False, False),
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._check_daemon_lifecycle_step",
        lambda _managed: False,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._install_scan_lifecycle_step",
        lambda: (False, False),
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._check_scan_lifecycle_step",
        lambda: False,
    )


def _browser_managed_config() -> dict[str, object]:
    return {
        "host": "https://t.example.com",
        "org_api_key": "rl_org_secret",
        "sessions": True,
        "browser_extension_id": "a" * 32,
        "browser_extension_update_url": UPDATE_URL,
    }


def _config_no_secret(host: str = "https://t.example.com") -> Config:
    return Config(default_host=host)


def _config_with_secret(host: str = "https://t.example.com") -> Config:
    return Config(
        default_host=host,
        hosts={url_to_host_key(host): {"url": host, "secret": "rl_user_existing"}},
    )


def _write_console_user_enrolled(
    home: Path, host: str = "https://t.example.com"
) -> None:
    """Drop the per-host enrollment marker into *home* (gate witness).

    Mirrors what ``aiwatch enroll`` persists — the user's keychain holds the
    secret, and ``~/.runlayer/.enrolled-<host_key>`` is the marker file the
    root/SYSTEM gate ``stat()``s.
    """
    marker = enrollment_marker_path(host, home=home)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()


def _mark_cursor_installed(home: Path, monkeypatch) -> None:
    """Seed cursor's config plus the executable the presence gate requires.

    Config files survive uninstall, so they alone no longer prove a client is
    installed. Stubbing the binary probe (rather than dropping a real file in
    *home*) also keeps a host-installed CLI from leaking in as a second client.
    """
    from runlayer_cli.scan import client_presence

    cursor_dir = home / ".cursor"
    cursor_dir.mkdir(exist_ok=True)
    (cursor_dir / "mcp.json").write_text("{}")
    monkeypatch.setattr(
        client_presence,
        "locate_cli_binary",
        lambda binary, **_kwargs: Path("/test/cursor") if binary == "cursor" else None,
    )


def test_setup_config_reports_incomplete_when_preferences_have_not_flushed(
    monkeypatch,
) -> None:
    write = MagicMock(
        return_value={
            "host": "https://tenant.runlayer.com",
            "flushed": False,
        }
    )
    reconcile = MagicMock(return_value=0)
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.configure_aiwatch_test_device",
        write,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._reconcile_hooks",
        reconcile,
    )

    result = runner.invoke(
        aiwatch_app,
        [
            "setup",
            "config",
            "--host",
            "https://tenant.runlayer.com",
            "--org-api-key",
            "rl_org_secret",
        ],
    )

    assert result.exit_code == 1, result.output
    reconcile.assert_called_once_with(
        client=None,
        host="https://tenant.runlayer.com",
        mdm=True,
        all_events=False,
    )
    assert "hook reconciliation is incomplete" in result.output
    assert "hourly bootstrap daemon will retry" in result.output
    assert "rl_org_secret" not in result.output


# ── strict-ordering guardrail (user scope) ─────────────────────────────


class TestInstallGuardrailUserScope:
    def test_install_user_exit_4_when_no_credential(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=InstallWindowState.NO_STAMP,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

        assert result.exit_code == 4, result.output
        assert "no user credential" in result.output
        assert "aiwatch enroll" in result.output

    def test_install_exit_2_when_no_host(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.delenv("RUNLAYER_HOST", raising=False)
        config = Config()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            # OrgApiKey present → passes the MDM-scope self-gate so host
            # resolution (which still fails) is what surfaces exit 2.
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x", "sessions": True},
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        assert result.exit_code == 2, result.output
        assert "no host configured" in result.output


# ── bounded install-window fast-retry (drives bootstrap LaunchDaemon's KeepAlive) ─


class TestInstallWindowExitCode:
    """`aiwatch setup hooks install` exit code on credential-gate failure
    must depend on the install-window stamp:

    * ``NO_STAMP`` (dev / non-pkg host) ⇒ exit 4 (today's strict behavior)
    * ``INSIDE`` (within 10 min of pkg install) ⇒ exit 4 (KeepAlive fast-retries)
    * ``OUTSIDE`` (stamp older than 10 min) ⇒ exit 0 (KeepAlive idles, hourly StartInterval takes over)
    """

    def _failure_count_path(self, tmp_path, monkeypatch, initial=None):
        path = tmp_path / "bootstrap-failures"
        if initial is not None:
            path.write_text(initial)
        monkeypatch.setattr(
            "runlayer_cli.commands.aiwatch_setup._BOOTSTRAP_FAILURE_COUNT_PATH",
            path,
        )
        return path

    def _invoke_regular_installs(
        self,
        *,
        attempts=1,
        install_effect=None,
        mdm=True,
        window_state=InstallWindowState.OUTSIDE,
    ):
        if install_effect is None:
            install_effect = OSError("read-only filesystem")
        window = MagicMock()
        if isinstance(window_state, list):
            window.side_effect = window_state
        else:
            window.return_value = window_state
        args = [
            "setup",
            "hooks",
            "install",
            "--mdm" if mdm else "--user",
            "--host",
            "https://t.example.com",
            "--client",
            "cursor",
        ]

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                # Sessions fails closed; enable it explicitly so these tests
                # exercise the install path rather than scan-only removal.
                return_value={"org_api_key": "rl_org_x", "sessions": True},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=install_effect,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                window,
            ),
        ):
            return [runner.invoke(aiwatch_app, args) for _ in range(attempts)]

    def _invoke_scan_only(self, *, failed):
        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={
                    "org_api_key": "rl_org_x",
                    "mode": "monitor",
                    "sessions": False,
                },
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._uninstall_targets",
                return_value=failed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=InstallWindowState.OUTSIDE,
            ),
        ):
            return runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--host",
                    "https://t.example.com",
                    "--client",
                    "cursor",
                ],
            )

    def _invoke_no_host(self, *, attempts=1):
        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x"},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_host",
                return_value=None,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=InstallWindowState.OUTSIDE,
            ),
        ):
            return [
                runner.invoke(aiwatch_app, ["setup", "hooks", "install"])
                for _ in range(attempts)
            ]

    def _invoke_no_credential(self, tmp_path, monkeypatch, *, window_state):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=window_state,
            ),
        ):
            return runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

    def test_no_stamp_exits_4(self, tmp_path, monkeypatch):
        result = self._invoke_no_credential(
            tmp_path, monkeypatch, window_state=InstallWindowState.NO_STAMP
        )
        assert result.exit_code == 4, result.output

    def test_inside_window_exits_4(self, tmp_path, monkeypatch):
        result = self._invoke_no_credential(
            tmp_path, monkeypatch, window_state=InstallWindowState.INSIDE
        )
        assert result.exit_code == 4, result.output
        assert "no user credential" in result.output

    def test_outside_window_exits_0_with_loud_stderr(self, tmp_path, monkeypatch):
        result = self._invoke_no_credential(
            tmp_path, monkeypatch, window_state=InstallWindowState.OUTSIDE
        )
        assert result.exit_code == 0, result.output
        # Stderr stays loud — only the exit code is softened so launchd's
        # KeepAlive idles. Operator UX still surfaces the missing credential.
        assert "no user credential" in result.output

    def test_outside_window_bounds_consecutive_misconfig_retries(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.delenv("RUNLAYER_HOST", raising=False)
        monkeypatch.setattr(
            "runlayer_cli.commands.aiwatch_setup._BOOTSTRAP_FAILURE_COUNT_PATH",
            tmp_path / "bootstrap-failures",
            raising=False,
        )
        config = Config()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x"},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=InstallWindowState.OUTSIDE,
            ),
        ):
            results = [
                runner.invoke(aiwatch_app, ["setup", "hooks", "install"])
                for _ in range(5)
            ]

        assert [result.exit_code for result in results] == [2, 2, 2, 2, 0]
        assert all("no host configured" in result.output for result in results)

    def test_outside_window_bounds_consecutive_partial_failure_retries(
        self, tmp_path, monkeypatch
    ):
        count_path = self._failure_count_path(tmp_path, monkeypatch)
        results = self._invoke_regular_installs(attempts=6)

        assert [result.exit_code for result in results] == [1, 1, 1, 1, 0, 0]
        assert all("write failed" in result.output for result in results)
        assert count_path.read_text() == "5\n"

    def test_success_resets_consecutive_failure_count(self, tmp_path, monkeypatch):
        from runlayer_cli.hook_install.clients import InstallResult

        self._failure_count_path(tmp_path, monkeypatch)
        attempt = 0

        def _install(client, **_kwargs):
            nonlocal attempt
            attempt += 1
            if attempt != 5:
                raise OSError("read-only filesystem")
            return InstallResult(
                client=client,
                config_path=tmp_path / "hooks.json",
                written=True,
            )

        results = self._invoke_regular_installs(
            attempts=6,
            install_effect=_install,
        )

        assert [result.exit_code for result in results] == [1, 1, 1, 1, 0, 1]

    def test_no_org_key_noop_resets_consecutive_failure_count(
        self, tmp_path, monkeypatch
    ):
        self._failure_count_path(tmp_path, monkeypatch, "4\n")

        with patch(
            "runlayer_cli.commands.aiwatch_setup.read_managed_config",
            return_value={},
        ):
            noop = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        failure = self._invoke_regular_installs()[0]

        assert noop.exit_code == 0, noop.output
        assert failure.exit_code == 1, failure.output

    def test_outside_window_bounds_scan_only_partial_failure(
        self, tmp_path, monkeypatch
    ):
        self._failure_count_path(tmp_path, monkeypatch, "4\n")
        result = self._invoke_scan_only(failed=True)

        assert result.exit_code == 0, result.output

    def test_scan_only_success_resets_consecutive_failure_count(
        self, tmp_path, monkeypatch
    ):
        self._failure_count_path(tmp_path, monkeypatch, "4\n")
        success = self._invoke_scan_only(failed=False)
        failure = self._invoke_regular_installs()[0]

        assert success.exit_code == 0, success.output
        assert failure.exit_code == 1, failure.output

    def test_outside_window_bounds_missing_binary_retries(self, tmp_path, monkeypatch):
        self._failure_count_path(tmp_path, monkeypatch, "4\n")

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x", "sessions": True},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                side_effect=FileNotFoundError("aiwatch-hook"),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=InstallWindowState.OUTSIDE,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 0, result.output
        assert "cannot find aiwatch binary" in result.output

    def test_inside_window_is_strict_and_resets_failure_count(
        self, tmp_path, monkeypatch
    ):
        self._failure_count_path(tmp_path, monkeypatch, "4\n")
        results = self._invoke_regular_installs(
            attempts=2,
            window_state=[
                InstallWindowState.INSIDE,
                InstallWindowState.OUTSIDE,
            ],
        )

        assert [result.exit_code for result in results] == [1, 1]

    def test_user_scope_failure_does_not_touch_failure_count(
        self, tmp_path, monkeypatch
    ):
        count_path = self._failure_count_path(tmp_path, monkeypatch, "4\n")
        result = self._invoke_regular_installs(mdm=False)[0]

        assert result.exit_code == 1, result.output
        assert count_path.read_text() == "4\n"

    def test_no_stamp_failure_is_strict_and_does_not_touch_failure_count(
        self, tmp_path, monkeypatch
    ):
        count_path = self._failure_count_path(tmp_path, monkeypatch, "4\n")
        result = self._invoke_regular_installs(
            window_state=InstallWindowState.NO_STAMP
        )[0]

        assert result.exit_code == 1, result.output
        assert count_path.read_text() == "4\n"

    def test_outside_window_missing_credential_softens_without_counting(
        self, tmp_path, monkeypatch
    ):
        self._failure_count_path(tmp_path, monkeypatch, "4\n")

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x", "sessions": True},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(False, "missing"),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_window_state",
                return_value=InstallWindowState.OUTSIDE,
            ),
        ):
            credential_failure = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--host",
                    "https://t.example.com",
                ],
            )

        partial_failure = self._invoke_regular_installs()[0]

        assert credential_failure.exit_code == 0, credential_failure.output
        assert partial_failure.exit_code == 1, partial_failure.output

    def test_corrupt_failure_count_recovers_and_bounds_retries(
        self, tmp_path, monkeypatch
    ):
        self._failure_count_path(tmp_path, monkeypatch, "corrupt\n")
        results = self._invoke_no_host(attempts=5)

        assert [result.exit_code for result in results] == [2, 2, 2, 2, 0]

    def test_unwritable_failure_count_preserves_original_outcomes(
        self, tmp_path, monkeypatch
    ):
        blocker = tmp_path / "not-a-directory"
        blocker.write_text("")
        monkeypatch.setattr(
            "runlayer_cli.commands.aiwatch_setup._BOOTSTRAP_FAILURE_COUNT_PATH",
            blocker / "bootstrap-failures",
        )
        result = self._invoke_no_host()[0]

        with patch(
            "runlayer_cli.commands.aiwatch_setup.read_managed_config",
            return_value={},
        ):
            success = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        assert result.exit_code == 2, result.output
        assert "no host configured" in result.output
        assert success.exit_code == 0, success.output


# ── strict-ordering guardrail (mdm scope, default) ─────────────────────


class TestInstallGuardrailMDMScope:
    def test_mdm_install_exit_0_when_no_org_api_key(self, tmp_path, monkeypatch):
        """Self-gate: MDM scope with no managed OrgApiKey exits 0 silently and
        writes nothing.

        The packaged bootstrap LaunchDaemon runs ``aiwatch setup hooks install
        --mdm`` directly with ``KeepAlive(SuccessfulExit=false)``; a non-zero
        exit on an unconfigured fleet would relaunch forever. This replaces the
        plist's old ``defaults read OrgApiKey || exit 0`` shell wrapper.
        """
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={},
            ),
            patch("runlayer_cli.commands.aiwatch_setup.install_client") as mock_install,
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        assert result.exit_code == 0, result.output
        mock_install.assert_not_called()

    def test_mdm_install_proceeds_when_console_user_enrolled(
        self, tmp_path, monkeypatch
    ):
        """Console user has enrolled → install runs (writes guarded by hook_command stub)."""
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        console_home = tmp_path / "ConsoleUser"
        _write_console_user_enrolled(console_home)

        # Capture the install_client calls so we can verify scope without
        # writing to the real /Library/Application Support/Cursor.
        captured = []

        def _fake_install(client, **kwargs):
            captured.append((client, kwargs))
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            # OrgApiKey present → passes the MDM-scope self-gate; the credential
            # itself is still proven via the console user's enrollment marker
            # (credential_gate.read_managed_config stays unpatched / empty).
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x", "sessions": True},
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        assert result.exit_code == 0, result.output
        assert captured, "install_client never called"

        from runlayer_cli.hook_install.paths import InstallScope

        for _client, kwargs in captured:
            assert kwargs.get("scope") == InstallScope.MDM, (
                f"expected MDM scope by default, got {kwargs.get('scope')}"
            )


class TestBackendConfigSync:
    def test_mdm_config_change_immediately_reports_updated_mode(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        initial = {
            "host": "https://managed.runlayer.com/",
            "org_api_key": "rl_org_secret",
            "mode": "monitor",
            "sessions": False,
            "detect_processes": False,
            "detect_containers": False,
            "project_depth": 7,
            "project_timeout": 60,
        }
        synced = {
            **initial,
            "mode": "enforce",
            "sessions": True,
            "detect_processes": True,
        }

        def _fake_install(client, **_kwargs):
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                side_effect=[initial, synced],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=True,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.aiwatch_checkin.read_managed_config",
                return_value=synced,
            ),
            patch("runlayer_cli.aiwatch_checkin.check_all", return_value=[]),
            patch(
                "runlayer_cli.aiwatch_checkin._make_device_context",
                return_value={
                    "device_id": "device-1",
                    "hostname": "DESKTOP-1",
                    "os": "windows",
                    "os_version": "11",
                    "username": "alex",
                    "org_device_id": None,
                    "serial_number": "SERIAL-1",
                },
            ),
            patch(
                "runlayer_cli.scan.device.get_installed_tools",
                return_value=[],
            ),
            patch(
                "runlayer_cli.api.RunlayerClient.submit_aiwatch_checkin"
            ) as submit_checkin,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://managed.runlayer.com",
                    "--client",
                    "cursor",
                ],
            )

        assert result.exit_code == 0, result.output
        payloads = [call.args[0] for call in submit_checkin.call_args_list]
        assert any(
            payload["feature"] == "enforce" and payload["status"] == "ok"
            for payload in payloads
        )

    def test_mdm_unchanged_config_does_not_report(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        managed = {
            "host": "https://managed.runlayer.com/",
            "org_api_key": "rl_org_secret",
            "mode": "enforce",
            "sessions": True,
            "detect_processes": True,
            "detect_containers": False,
            "project_depth": 7,
            "project_timeout": 60,
        }

        def _fake_install(client, **_kwargs):
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                side_effect=[managed, managed],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=True,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._submit_config_change_checkins"
            ) as submit_checkins,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://managed.runlayer.com",
                    "--client",
                    "cursor",
                ],
            )

        assert result.exit_code == 0, result.output
        submit_checkins.assert_not_called()

    def test_mdm_install_syncs_then_reloads_settings_before_reconcile(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        initial = {
            "host": "https://managed.runlayer.com/",
            "org_api_key": "rl_org_secret",
            "mode": "monitor",
            "sessions": False,
            "detect_processes": False,
            "detect_containers": False,
            "project_depth": 7,
            "project_timeout": 60,
        }
        synced = {
            **initial,
            "mode": "protect",
            "sessions": True,
            "detect_processes": True,
            "project_depth": 12,
            "project_timeout": 90,
        }
        captured = []

        def _fake_install(client, **kwargs):
            captured.append((client, kwargs))
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                side_effect=[initial, synced],
            ) as read_managed,
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=True,
            ) as sync_config,
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://override.invalid",
                    "--client",
                    "cursor",
                ],
            )

        assert result.exit_code == 0, result.output
        sync_config.assert_called_once_with(
            host="https://managed.runlayer.com",
            org_api_key="rl_org_secret",
        )
        assert read_managed.call_count == 2
        assert [client.value for client, _kwargs in captured] == ["cursor"]

    def test_scan_only_partial_removal_still_reports_changed_config(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        initial = {
            "host": "https://managed.runlayer.com/",
            "org_api_key": "rl_org_secret",
            "mode": "enforce",
            "sessions": True,
            "detect_processes": False,
            "detect_containers": False,
            "project_depth": 7,
            "project_timeout": 60,
        }
        synced = {
            **initial,
            "mode": "monitor",
            "sessions": False,
        }

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                side_effect=[initial, synced],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=True,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.uninstall_client",
                side_effect=OSError("access denied"),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._submit_config_change_checkins"
            ) as submit_checkins,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://managed.runlayer.com",
                    "--client",
                    "cursor",
                ],
            )

        assert result.exit_code == 1, result.output
        submit_checkins.assert_called_once_with(
            host="https://managed.runlayer.com",
            key="rl_org_secret",
        )

    def test_config_change_checkin_skips_without_console_user(self):
        from runlayer_cli.commands.aiwatch_setup import (
            _submit_config_change_checkins,
        )

        with (
            patch(
                "runlayer_cli.aiwatch_checkin._make_device_context",
                return_value={
                    "device_id": "device-1",
                    "hostname": "DESKTOP-1",
                    "os": "windows",
                    "os_version": "11",
                    "username": None,
                    "org_device_id": None,
                    "serial_number": "SERIAL-1",
                },
            ),
            patch("runlayer_cli.api.RunlayerClient") as client,
            patch(
                "runlayer_cli.aiwatch_checkin.submit_validation_checkins"
            ) as submit_checkins,
        ):
            _submit_config_change_checkins(
                host="https://managed.runlayer.com",
                key="rl_org_secret",
            )

        client.assert_not_called()
        submit_checkins.assert_not_called()

    def test_user_install_does_not_sync_backend_config(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_with_secret("https://tenant.runlayer.com")
        sync_config = MagicMock()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                sync_config,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--user",
                    "--host",
                    "https://tenant.runlayer.com",
                ],
            )

        assert result.exit_code == 0, result.output
        sync_config.assert_not_called()


# ── happy path (user scope) ────────────────────────────────────────────


class TestInstallHappyPathUserScope:
    def test_install_writes_for_installed_clients(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

        assert result.exit_code == 0, result.output
        hooks_json = tmp_path / ".cursor" / "hooks.json"
        assert hooks_json.exists()
        hooks = json.loads(hooks_json.read_text())["hooks"]
        assert hooks["beforeMCPExecution"][0]["command"].endswith(
            "aiwatch-hook --client cursor"
        )

    def test_install_user_proceeds_on_enrollment_marker_without_secret(
        self, tmp_path, monkeypatch
    ):
        """USER scope: the current user's enrollment marker satisfies the gate.

        The aiwatch binary ignores ``~/.runlayer/config.yaml`` so a seeded YAML
        secret is unreachable; the credential proof is the marker ``aiwatch
        enroll`` drops (mirrors the rootless frozen ``--user`` install). No
        keychain secret, no managed org key.
        """
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        _write_console_user_enrolled(tmp_path)
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

        assert result.exit_code == 0, result.output
        assert (tmp_path / ".cursor" / "hooks.json").exists()

    def test_install_user_skips_missing_clients_without_failing(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        # No client dirs created — every supported client is "not installed".
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.scan.client_presence.detect_client_presence",
                return_value=[],
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

        assert result.exit_code == 0, result.output
        assert "no client config dirs detected" in result.output


class TestBrowserExtensionInstall:
    def test_install_mdm_client_still_reconciles_browser_extension(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_with_secret()
        managed = _browser_managed_config()
        captured = []

        def _fake_install(client, **kwargs):
            captured.append((client, kwargs))
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_browser_extension",
                return_value=BrowserExtensionResult(
                    written=True,
                    policy_path=tmp_path / "policy.plist",
                    install_path=tmp_path / "extension.json",
                ),
            ) as mock_install_extension,
        ):
            result = runner.invoke(
                aiwatch_app,
                ["setup", "hooks", "install", "--mdm", "--client", "cursor"],
            )

        assert result.exit_code == 0, result.output
        assert [client.value for client, _kwargs in captured] == ["cursor"]
        mock_install_extension.assert_called_once_with(managed)
        assert "browser_extension: browser policies reconciled" in result.output

    def test_invalid_managed_grok_home_does_not_abort_other_reconciliation(
        self, tmp_path
    ):
        from runlayer_cli.hook_install.clients import Client, InstallResult
        from runlayer_cli.hook_install.paths import enterprise_grok_cli_dir

        console_home = tmp_path / "ConsoleUser"
        managed = {
            **_browser_managed_config(),
            "grok_home": str(tmp_path / "OutsideConsoleHome"),
        }
        attempted: list[Client] = []

        def _fake_install(client, **_kwargs):
            attempted.append(client)
            if client == Client.GROK_CLI:
                enterprise_grok_cli_dir()
            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, True),
            ) as install_browser,
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.mdm_config.read_managed_config",
                return_value=managed,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        assert "grok-cli: configuration invalid" in result.output
        assert (
            "managed GrokHome must stay within the console user's home" in result.output
        )
        assert Client.CLINE_CLI in attempted
        install_browser.assert_called_once_with(managed)

    def test_install_does_not_hide_unexpected_value_error(self):
        from runlayer_cli.commands import aiwatch_setup
        from runlayer_cli.hook_install import Client

        with (
            patch.object(
                aiwatch_setup,
                "read_managed_config",
                return_value={"sessions": True},
            ),
            patch.object(
                aiwatch_setup,
                "resolve_host",
                return_value="https://t.example.com",
            ),
            patch.object(
                aiwatch_setup, "credential_present", return_value=(True, None)
            ),
            patch.object(
                aiwatch_setup,
                "resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch.object(
                aiwatch_setup, "_targets_from_client", return_value=(Client.CURSOR,)
            ),
            patch.object(
                aiwatch_setup,
                "install_client",
                side_effect=ValueError("unknown client programming error"),
            ),
        ):
            with pytest.raises(ValueError, match="unknown client programming error"):
                aiwatch_setup._reconcile_hooks(
                    client=None,
                    host="https://t.example.com",
                    mdm=False,
                    all_events=False,
                )

    def test_uninstall_does_not_hide_unexpected_value_error(self):
        from runlayer_cli.commands import aiwatch_setup
        from runlayer_cli.hook_install import Client, InstallScope

        with patch.object(
            aiwatch_setup,
            "uninstall_client",
            side_effect=ValueError("unknown client programming error"),
        ):
            with pytest.raises(ValueError, match="unknown client programming error"):
                aiwatch_setup._uninstall_targets(
                    (Client.CURSOR,), scope=InstallScope.MDM
                )


class TestDaemonLifecycleReconcile:
    def test_mdm_gate_flip_restarts_windows_service(self):
        initial = {
            "host": "https://t.example.com",
            "org_api_key": "rl_org_secret",
            "mode": "monitor",
            "sessions": False,
            "daemon_enabled": False,
        }
        synced = {**initial, "daemon_enabled": True}
        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                side_effect=[initial, synced],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=True,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._uninstall_targets",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_daemon_lifecycle_step",
                return_value=(False, True),
            ) as reconcile_daemon,
            patch("runlayer_cli.commands.aiwatch_setup._submit_config_change_checkins"),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 0, result.output
        reconcile_daemon.assert_called_once_with(
            synced,
            restart_windows_service=True,
        )

    def test_mdm_install_reconciles_closed_daemon_gate_for_scan_only(self):
        """Remove gate-off service state without requiring package repair."""
        managed = {
            "host": "https://t.example.com",
            "org_api_key": "rl_org_secret",
            "mode": "monitor",
            "sessions": False,
            "daemon_enabled": False,
        }
        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                side_effect=[managed, managed],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._uninstall_targets",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, False),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_daemon_lifecycle_step",
                return_value=(False, True),
            ) as reconcile_daemon,
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_scan_lifecycle_step",
                return_value=(False, True),
            ) as reconcile_scan,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 0, result.output
        reconcile_daemon.assert_called_once_with(
            managed,
            restart_windows_service=False,
        )
        reconcile_scan.assert_called_once_with()

    def test_mdm_check_includes_daemon_lifecycle_drift(self):
        managed = {
            "host": "https://t.example.com",
            "org_api_key": "rl_org_secret",
            "mode": "monitor",
            "sessions": False,
        }
        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_absent",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_browser_extension_step",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_daemon_lifecycle_step",
                return_value=True,
            ) as check_daemon,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "check",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        check_daemon.assert_called_once_with(managed)

    def test_mdm_scan_only_check_includes_scan_lifecycle_drift(self):
        managed = {
            "host": "https://t.example.com",
            "org_api_key": "rl_org_secret",
            "mode": "monitor",
            "sessions": False,
        }
        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_absent",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_browser_extension_step",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_daemon_lifecycle_step",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_scan_lifecycle_step",
                return_value=True,
            ) as check_scan,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "check",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        check_scan.assert_called_once_with()


# ── check ──────────────────────────────────────────────────────────────


class TestCheck:
    def test_invalid_managed_grok_home_is_drift_and_check_continues(self, tmp_path):
        from runlayer_cli.hook_install.clients import Client
        from runlayer_cli.hook_install.paths import enterprise_grok_cli_dir

        console_home = tmp_path / "ConsoleUser"
        managed = {
            **_browser_managed_config(),
            "grok_home": str(tmp_path / "OutsideConsoleHome"),
        }
        checked: list[Client] = []

        def _fake_client_is_installed(client, **_kwargs):
            checked.append(client)
            if client == Client.GROK_CLI:
                enterprise_grok_cli_dir()
            return False

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=_config_with_secret(),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.hook_install.check.iter_supported_clients",
                return_value=(Client.GROK_CLI, Client.CLINE_CLI),
            ),
            patch(
                "runlayer_cli.hook_install.check.client_is_installed",
                side_effect=_fake_client_is_installed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_browser_extension_step",
                return_value=False,
            ) as check_browser,
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.mdm_config.read_managed_config",
                return_value=managed,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "check",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        assert (
            "grok-cli: drifted (configuration invalid: managed GrokHome must stay "
            "within the console user's home)"
        ) in result.output
        assert checked == [Client.GROK_CLI, Client.CLINE_CLI]
        check_browser.assert_called_once_with(managed)

    def test_check_user_exits_2_when_no_clients_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.scan.client_presence.detect_client_presence",
                return_value=[],
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "check", "--user"])

        assert result.exit_code == 2, result.output
        assert "no supported AI clients installed" in result.output

    def test_check_mdm_exits_1_on_daemon_drift_without_clients(self):
        managed = {
            "host": "https://t.example.com",
            "org_api_key": "rl_org_secret",
            "sessions": True,
        }

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.check_all",
                return_value=[],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_daemon_lifecycle_step",
                return_value=True,
            ) as check_daemon,
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_browser_extension_step",
                return_value=False,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "check",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        assert "no supported AI clients installed" in result.output
        check_daemon.assert_called_once_with(managed)

    def test_check_mdm_exits_1_on_scan_drift_without_clients(self):
        managed = {
            "host": "https://t.example.com",
            "org_api_key": "rl_org_secret",
            "sessions": True,
        }

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
                return_value=(True, None),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.check_all",
                return_value=[],
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_daemon_lifecycle_step",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_browser_extension_step",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_scan_lifecycle_step",
                return_value=True,
            ) as check_scan,
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "check",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        assert "no supported AI clients installed" in result.output
        check_scan.assert_called_once_with()

    def test_check_user_exits_4_without_credential(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "check", "--user"])

        assert result.exit_code == 4, result.output

    def test_check_user_exits_1_on_drift(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        (tmp_path / ".cursor" / "hooks.json").write_text("{}")
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "check", "--user"])

        assert result.exit_code == 1, result.output

    def test_check_user_ok_after_install(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.hook_install.check.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            install_result = runner.invoke(
                aiwatch_app, ["setup", "hooks", "install", "--user"]
            )
            assert install_result.exit_code == 0, install_result.output

            check_result = runner.invoke(
                aiwatch_app, ["setup", "hooks", "check", "--user"]
            )

        assert check_result.exit_code == 0, check_result.output


# ── Sessions MDM key → include_pipeline resolution ─────────────────────


class TestSessionsIncludePipeline:
    """`Sessions` MDM key drives whether event/session hooks install.

    Config-driven and scope-independent: absent ⇒ scan-only; `false` ⇒
    enforcement only when enforcement is enabled; `--all-events` always wins.
    User scope honors `Sessions` too.
    """

    def _invoke(self, tmp_path, monkeypatch, *, args, managed_config):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_with_secret()

        console_home = tmp_path / "ConsoleUser"
        _write_console_user_enrolled(console_home)

        # A managed OrgApiKey satisfies the MDM-scope install self-gate; the
        # Sessions/Enforcement keys under test drive include_pipeline
        # independently of it.
        managed = {"org_api_key": "rl_org_x", **managed_config}

        captured: list[dict] = []

        def _fake_install(client, **kwargs):
            captured.append(kwargs)
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._uninstall_targets",
                return_value=False,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", *args])

        assert result.exit_code == 0, result.output
        return captured

    def test_mdm_absent_sessions_installs_no_hooks(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--mdm"], managed_config={}
        )
        assert captured == []

    def test_mdm_sessions_false_excludes_pipeline(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path,
            monkeypatch,
            args=["--mdm"],
            managed_config={"enforcement": True, "sessions": False},
        )
        assert all(kwargs.get("include_pipeline") is False for kwargs in captured)

    def test_mdm_sessions_false_with_all_events_includes_pipeline(
        self, tmp_path, monkeypatch
    ):
        captured = self._invoke(
            tmp_path,
            monkeypatch,
            args=["--mdm", "--all-events"],
            managed_config={"sessions": False},
        )
        assert all(kwargs.get("include_pipeline") is True for kwargs in captured)

    def test_user_scope_honors_mdm_sessions(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--user"], managed_config={"sessions": True}
        )
        assert all(kwargs.get("include_pipeline") is True for kwargs in captured)

    def test_user_scope_sessions_false_excludes_pipeline(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path,
            monkeypatch,
            args=["--user"],
            managed_config={"enforcement": True, "sessions": False},
        )
        assert all(kwargs.get("include_pipeline") is False for kwargs in captured)

    def test_user_scope_absent_sessions_installs_no_hooks(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--user"], managed_config={}
        )
        assert captured == []


# ── org-key mode satisfies the credential gate (ENG-3180) ──────────────


class TestOrgKeyModeInstall:
    """A managed ``OrgApiKey`` satisfies the install credential gate directly —
    no per-user enroll marker needed (hooks authenticate with the org key)."""

    def test_mdm_install_proceeds_on_org_api_key_without_enroll_marker(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        captured: list = []

        def _fake_install(client, **kwargs):
            captured.append((client, kwargs))
            from runlayer_cli.hook_install.clients import InstallResult

            return InstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                written=True,
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            # No console-user enroll marker exists anywhere.
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=None,
            ),
            # Managed org key present → satisfies both the command-level
            # self-gate and the credential gate (no enroll marker needed).
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"org_api_key": "rl_org_x", "sessions": True},
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.read_managed_config",
                return_value={"org_api_key": "rl_org_x"},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.install_client",
                side_effect=_fake_install,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        assert result.exit_code == 0, result.output
        assert captured, "install_client never called"


# ── scan-only hook removal (Enforcement + Sessions both off) ──────────────────


class TestScanOnlyRemoval:
    def test_install_user_metadata_only_writes_one_mcp_hook(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        config = _config_with_secret()
        managed = {
            "mode": "monitor",
            "sessions": False,
            "mcp_usage_metadata": True,
        }

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                ["setup", "hooks", "install", "--user", "--client", "cursor"],
            )

        assert result.exit_code == 0, result.output
        hooks = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())["hooks"]
        assert set(hooks) == {"beforeMCPExecution"}

    def test_install_user_scan_only_uninstalls_stale_hooks_without_credential(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        (cursor_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/usr/local/bin/aiwatch hook --client cursor"},
                            {"command": "/opt/other/hook"},
                        ],
                        "beforeReadFile": [{"command": "/usr/local/bin/aiwatch-hook"}],
                    },
                }
            )
        )
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"enforcement": False, "sessions": False},
            ),
            patch("runlayer_cli.commands.aiwatch_setup.install_client") as mock_install,
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

        assert result.exit_code == 0, result.output
        assert "scan-only" in result.output
        mock_install.assert_not_called()
        data = json.loads((cursor_dir / "hooks.json").read_text())
        assert data["hooks"] == {"beforeMCPExecution": [{"command": "/opt/other/hook"}]}

    def test_invalid_managed_grok_home_does_not_abort_scan_only_reconciliation(
        self, tmp_path
    ):
        from runlayer_cli.hook_install.clients import Client, UninstallResult
        from runlayer_cli.hook_install.paths import enterprise_grok_cli_dir

        console_home = tmp_path / "ConsoleUser"
        managed = {
            **_browser_managed_config(),
            "enforcement": False,
            "sessions": False,
            "grok_home": str(tmp_path / "OutsideConsoleHome"),
        }
        attempted: list[Client] = []

        def _fake_uninstall(client, **_kwargs):
            attempted.append(client)
            if client == Client.GROK_CLI:
                enterprise_grok_cli_dir()
            return UninstallResult(
                client=client,
                config_path=tmp_path / f"fake-{client.value}.json",
                changed=False,
                skipped_reason="no Runlayer hooks",
            )

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
                return_value=False,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.uninstall_client",
                side_effect=_fake_uninstall,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
                return_value=(False, True),
            ) as install_browser,
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.mdm_config.read_managed_config",
                return_value=managed,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "install",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        assert "grok-cli: configuration invalid" in result.output
        assert (
            "managed GrokHome must stay within the console user's home" in result.output
        )
        assert Client.CLINE_CLI in attempted
        install_browser.assert_called_once_with(managed)

    def test_install_all_events_overrides_scan_only(self, tmp_path, monkeypatch):
        """``--all-events`` forces install even when Enforcement+Sessions are off."""
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        _mark_cursor_installed(tmp_path, monkeypatch)
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"enforcement": False, "sessions": False},
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(
                aiwatch_app, ["setup", "hooks", "install", "--user", "--all-events"]
            )

        assert result.exit_code == 0, result.output
        assert (tmp_path / ".cursor" / "hooks.json").exists()

    def test_check_user_scan_only_drifts_until_reconciled(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        (tmp_path / ".cursor" / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "beforeMCPExecution": [
                            {"command": "/usr/local/bin/aiwatch hook --client cursor"}
                        ]
                    },
                }
            )
        )
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value={"enforcement": False, "sessions": False},
            ),
        ):
            drift_result = runner.invoke(
                aiwatch_app, ["setup", "hooks", "check", "--user"]
            )
            install_result = runner.invoke(
                aiwatch_app, ["setup", "hooks", "install", "--user"]
            )
            ok_result = runner.invoke(
                aiwatch_app, ["setup", "hooks", "check", "--user"]
            )

        assert drift_result.exit_code == 1, drift_result.output
        assert "Runlayer hook entries present" in drift_result.output
        assert install_result.exit_code == 0, install_result.output
        assert ok_result.exit_code == 0, ok_result.output
        assert "scan-only" in ok_result.output

    def test_invalid_managed_grok_home_is_scan_only_drift_and_check_continues(
        self, tmp_path
    ):
        from runlayer_cli.hook_install.clients import Client

        console_home = tmp_path / "ConsoleUser"
        cline_hooks = console_home / ".cline" / "hooks"
        cline_hooks.mkdir(parents=True)
        (cline_hooks / "PreToolUse").write_text(
            "# runlayer-owned Cline hook — safe to delete\n"
        )
        managed = {
            **_browser_managed_config(),
            "enforcement": False,
            "sessions": False,
            "grok_home": str(tmp_path / "OutsideConsoleHome"),
        }

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.hook_install.check.iter_supported_clients",
                return_value=(Client.GROK_CLI, Client.CLINE_CLI),
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_browser_extension_step",
                return_value=False,
            ) as check_browser,
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.mdm_config.read_managed_config",
                return_value=managed,
            ),
        ):
            result = runner.invoke(
                aiwatch_app,
                [
                    "setup",
                    "hooks",
                    "check",
                    "--mdm",
                    "--host",
                    "https://t.example.com",
                ],
            )

        assert result.exit_code == 1, result.output
        assert (
            "grok-cli: drifted (configuration invalid: managed GrokHome must stay "
            "within the console user's home)"
        ) in result.output
        assert "cline-cli: drifted (Runlayer hook scripts present)" in result.output
        check_browser.assert_called_once_with(managed)

    def test_check_mdm_scan_only_reports_browser_extension_drift(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        managed = {
            **_browser_managed_config(),
            "enforcement": False,
            "sessions": False,
        }

        with (
            patch(
                "runlayer_cli.commands.aiwatch_setup.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value=managed,
            ),
            patch(
                "runlayer_cli.commands.aiwatch_setup._check_absent",
                return_value=False,
            ) as mock_check_absent,
            patch(
                "runlayer_cli.commands.aiwatch_setup.check_browser_extension",
                return_value=(False, "force-install policy missing"),
            ) as mock_check_extension,
            patch(
                "runlayer_cli.commands.aiwatch_setup.credential_present",
            ) as mock_credential,
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "check", "--mdm"])

        assert result.exit_code == 1, result.output
        assert (
            "browser_extension: drifted (force-install policy missing)" in result.output
        )
        mock_check_absent.assert_called_once()
        mock_check_extension.assert_called_once_with(managed)
        mock_credential.assert_not_called()
