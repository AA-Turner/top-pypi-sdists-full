"""Tests for the ``aiwatch bootstrap`` typer command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.config import Config
from runlayer_cli.enrollment import (
    EnrollmentError,
    EnrollmentResult,
    enrollment_marker_path,
)

runner = CliRunner()


def _config_no_secret(host: str = "https://t.example.com") -> Config:
    return Config(default_host=host)


def _config_with_secret(host: str = "https://t.example.com") -> Config:
    return Config(
        default_host=host,
        hosts={"t.example.com": {"url": host, "secret": "rl_user_existing"}},
    )


def _patch_user_scope_console_lookup(tmp_path: Path):
    """Force MDM-default gate paths to no-op so we can test user-scope explicitly."""
    return patch(
        "runlayer_cli.hook_install.credential_gate.find_console_user_home",
        return_value=tmp_path,
    )


# ── fresh install (user scope) ─────────────────────────────────────────


class TestFreshInstallUserScope:
    def test_enroll_then_install_hooks(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()

        seen_enroll = {"called": False}

        def _next_config():
            return (
                _config_with_secret() if seen_enroll["called"] else _config_no_secret()
            )

        def _fake_exchange(**_kwargs):
            seen_enroll["called"] = True
            return EnrollmentResult(
                api_key="rl_user_new",
                username="u@example.com",
                device_name="Mac-1",
            )

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                side_effect=_next_config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                side_effect=_next_config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={
                    "enrollment_key": "rl_enroll_abc",
                    "username": "u@example.com",
                    "device_name": "Mac-1",
                },
            ),
            patch(
                "runlayer_cli.commands.bootstrap.exchange_enrollment_key",
                side_effect=_fake_exchange,
            ) as mock_ex,
            patch("runlayer_cli.config.save_config"),
            patch.object(Config, "set_host_credentials", return_value=False),
            patch(
                "runlayer_cli.commands.bootstrap.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--user"])

        assert result.exit_code == 0, result.output
        mock_ex.assert_called_once()
        assert "enroll: credential stored" in result.output
        assert "hooks: cursor configured" in result.output
        assert (tmp_path / ".cursor" / "hooks.json").exists()
        # Successful enroll must drop the per-host gate witness.
        assert enrollment_marker_path("https://t.example.com", home=tmp_path).is_file()


# ── already-bootstrapped short-circuit ──────────────────────────────────


class TestAlreadyBootstrapped:
    def test_skips_enrollment_when_credential_exists(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=config,
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={"enrollment_key": "rl_enroll_abc"},
            ),
            patch("runlayer_cli.commands.bootstrap.exchange_enrollment_key") as mock_ex,
            patch(
                "runlayer_cli.commands.bootstrap.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--user"])

        assert result.exit_code == 0, result.output
        mock_ex.assert_not_called()
        assert "enroll: credential already present" in result.output
        # Self-migration: short-circuit still refreshes the marker so devices
        # enrolled before this change satisfy the gate on the next hourly tick.
        assert enrollment_marker_path("https://t.example.com", home=tmp_path).is_file()


# ── enroll failure stops install ───────────────────────────────────────


class TestEnrollFails:
    def test_enroll_failure_aborts_before_install(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={"enrollment_key": "rl_enroll_abc"},
            ),
            patch(
                "runlayer_cli.commands.bootstrap.exchange_enrollment_key",
                side_effect=EnrollmentError("server down", status_code=503),
            ),
            patch("runlayer_cli.commands.bootstrap.install_client") as mock_install,
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--user"])

        assert result.exit_code == 1, result.output
        assert "enroll: server down" in result.output
        mock_install.assert_not_called()

    def test_no_enrollment_key_when_credential_missing_exits_2(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        monkeypatch.delenv("RUNLAYER_ENROLLMENT_API_KEY", raising=False)

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--user"])

        assert result.exit_code == 2, result.output
        assert "no enrollment key" in result.output


# ── --check mode ───────────────────────────────────────────────────────


class TestCheckMode:
    def test_check_exit_4_when_no_credential(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            # User scope so the gate only checks the current process.
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=None,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--check", "--user"])

        assert result.exit_code == 4, result.output
        assert "missing credential" in result.output

    def test_check_exit_0_when_no_clients_installed(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_with_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_with_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--check", "--user"])

        assert result.exit_code == 0, result.output
        assert "no supported AI clients installed" in result.output

    def test_check_does_not_mutate(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_with_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_with_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch("runlayer_cli.commands.bootstrap.install_client") as mock_install,
            patch("runlayer_cli.commands.bootstrap.exchange_enrollment_key") as mock_ex,
        ):
            runner.invoke(aiwatch_app, ["bootstrap", "--check", "--user"])

        mock_install.assert_not_called()
        mock_ex.assert_not_called()
        assert not (tmp_path / ".cursor" / "hooks.json").exists()


# ── MDM scope (default) ────────────────────────────────────────────────


class TestMDMDefault:
    def test_check_consults_console_user_when_current_user_unset(
        self, tmp_path, monkeypatch
    ):
        """``--mdm`` (default) gate succeeds when console-user has enrolled."""
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        console_home = tmp_path / "ConsoleUser"
        # Marker file is the gate witness; aiwatch enroll drops it on success.
        marker = enrollment_marker_path("https://t.example.com", home=console_home)
        marker.parent.mkdir(parents=True)
        marker.touch()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.read_managed_config",
                return_value={},
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=console_home,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--check"])

        assert "credential present" in result.output, result.output

    def test_check_exit_4_when_no_console_user_enrolled(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=_config_no_secret(),
            ),
            patch(
                "runlayer_cli.enrollment.load_config",
                return_value=_config_no_secret(),
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
            result = runner.invoke(aiwatch_app, ["bootstrap", "--check"])

        assert result.exit_code == 4, result.output


# ── Sessions MDM key → include_pipeline resolution ─────────────────────


class TestSessionsIncludePipeline:
    """`Sessions` MDM key drives event/session hook install on bootstrap.

    Config-driven and scope-independent: absent ⇒ all events on; `false` ⇒
    enforcement only; `--all-events` always wins. User scope honors `Sessions`
    too so the bootstrap phase installs the full set by default everywhere.
    """

    def _invoke(self, tmp_path, monkeypatch, *, args, managed_config):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_with_secret()

        console_home = tmp_path / "ConsoleUser"
        marker = enrollment_marker_path("https://t.example.com", home=console_home)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()

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
                "runlayer_cli.commands.bootstrap.load_config",
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
                "runlayer_cli.commands.bootstrap.read_managed_config",
                return_value=managed_config,
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=console_home,
            ),
            patch(
                "runlayer_cli.commands.bootstrap.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
            patch(
                "runlayer_cli.commands.bootstrap.install_client",
                side_effect=_fake_install,
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", *args])

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

    def test_user_scope_absent_sessions_includes_pipeline(self, tmp_path, monkeypatch):
        captured = self._invoke(
            tmp_path, monkeypatch, args=["--user"], managed_config={}
        )
        assert all(kwargs.get("include_pipeline") is True for kwargs in captured)


# ── org-key mode: skip the legacy enroll step (ENG-3180) ───────────────


class TestOrgKeyModeSkipsEnroll:
    def test_bootstrap_skips_enroll_when_org_api_key_present(
        self, tmp_path, monkeypatch
    ):
        """A managed ``OrgApiKey`` ⇒ no enroll exchange; hooks still install."""
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.bootstrap.read_managed_config",
                return_value={"org_api_key": "rl_org_x"},
            ),
            patch(
                "runlayer_cli.hook_install.credential_gate.read_managed_config",
                return_value={"org_api_key": "rl_org_x"},
            ),
            patch("runlayer_cli.commands.bootstrap.exchange_enrollment_key") as mock_ex,
            patch(
                "runlayer_cli.commands.bootstrap.resolve_hook_command",
                return_value="/usr/local/bin/aiwatch-hook",
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--user"])

        assert result.exit_code == 0, result.output
        mock_ex.assert_not_called()
        assert "using managed org api key" in result.output
        assert (tmp_path / ".cursor" / "hooks.json").exists()


# ── scan-only no-op (Enforcement + Sessions both off) ──────────────────


class TestScanOnlyNoOp:
    def test_bootstrap_scan_only_no_op(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        (tmp_path / ".cursor").mkdir()
        config = _config_with_secret()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.bootstrap.read_managed_config",
                return_value={"enforcement": False, "sessions": False},
            ),
            patch("runlayer_cli.commands.bootstrap.exchange_enrollment_key") as mock_ex,
            patch("runlayer_cli.commands.bootstrap.install_client") as mock_install,
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--user"])

        assert result.exit_code == 0, result.output
        assert "scan-only" in result.output
        mock_ex.assert_not_called()
        mock_install.assert_not_called()
        assert not (tmp_path / ".cursor" / "hooks.json").exists()

    def test_bootstrap_check_scan_only_no_op(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
        config = _config_no_secret()

        with (
            patch(
                "runlayer_cli.commands.bootstrap.load_config",
                return_value=config,
            ),
            patch("runlayer_cli.enrollment.load_config", return_value=config),
            patch("runlayer_cli.enrollment.read_managed_config", return_value={}),
            patch(
                "runlayer_cli.commands.bootstrap.read_managed_config",
                return_value={"enforcement": False, "sessions": False},
            ),
        ):
            result = runner.invoke(aiwatch_app, ["bootstrap", "--check", "--user"])

        assert result.exit_code == 0, result.output
        assert "scan-only" in result.output
