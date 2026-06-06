"""Tests for ``aiwatch setup hooks`` — strict-ordering guardrail + MDM/user scope writes."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.config import Config
from runlayer_cli.enrollment import enrollment_marker_path
from runlayer_cli.install_window import InstallWindowState

runner = CliRunner()


def _config_no_secret(host: str = "https://t.example.com") -> Config:
    return Config(default_host=host)


def _config_with_secret(host: str = "https://t.example.com") -> Config:
    return Config(
        default_host=host,
        hosts={"t.example.com": {"url": host, "secret": "rl_user_existing"}},
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


# ── strict-ordering guardrail (mdm scope, default) ─────────────────────


class TestInstallGuardrailMDMScope:
    def test_mdm_install_exit_4_when_console_user_unenrolled(
        self, tmp_path, monkeypatch
    ):
        """No console user → exit 4 (can't vouch for a credential)."""
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
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=None,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install"])

        assert result.exit_code == 4, result.output
        assert "no user credential" in result.output

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


# ── happy path (user scope) ────────────────────────────────────────────


class TestInstallHappyPathUserScope:
    def test_install_writes_for_installed_clients(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
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
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", "--user"])

        assert result.exit_code == 0, result.output
        assert "no client config dirs detected" in result.output


# ── check ──────────────────────────────────────────────────────────────


class TestCheck:
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
        ):
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "check", "--user"])

        assert result.exit_code == 2, result.output
        assert "no supported AI clients installed" in result.output

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
        (tmp_path / ".cursor").mkdir()
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
        (tmp_path / ".cursor").mkdir()
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

    Config-driven and scope-independent: absent ⇒ all events on; `false` ⇒
    enforcement only; `--all-events` always wins. User scope honors `Sessions`
    too so the bootstrap phase installs the full set by default everywhere.
    """

    def _invoke(self, tmp_path, monkeypatch, *, args, managed_config):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_with_secret()

        console_home = tmp_path / "ConsoleUser"
        _write_console_user_enrolled(console_home)

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
                return_value=managed_config,
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
            result = runner.invoke(aiwatch_app, ["setup", "hooks", "install", *args])

        assert result.exit_code == 0, result.output
        assert captured, "install_client never called"
        return captured

    def test_mdm_absent_sessions_includes_pipeline(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--mdm"], managed_config={}
        )
        assert all(kwargs.get("include_pipeline") is True for kwargs in captured)

    def test_mdm_sessions_false_excludes_pipeline(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--mdm"], managed_config={"sessions": False}
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
            tmp_path, monkeypatch, args=["--user"], managed_config={"sessions": False}
        )
        assert all(kwargs.get("include_pipeline") is False for kwargs in captured)

    def test_user_scope_absent_sessions_includes_pipeline(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--user"], managed_config={}
        )
        assert all(kwargs.get("include_pipeline") is True for kwargs in captured)
