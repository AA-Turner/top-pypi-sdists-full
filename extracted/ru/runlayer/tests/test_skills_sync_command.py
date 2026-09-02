"""Tests for ``runlayer skills sync`` (managed skill reconciler command)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
import typer

import runlayer_cli.aiwatch_checkin as aiwatch_checkin
import runlayer_cli.commands.skills as skills_cmd
import runlayer_cli.scan.windows_users as windows_users_mod
import runlayer_cli.skills.device_sync as ds

_EFFECTIVE_HOST = "https://tenant.runlayer.com"


def _run_sync(
    *,
    managed: dict | None = None,
    sync_key: str | None = None,
    report: ds.SyncReport | None = None,
    secret: str | None = None,
    euid: int = 501,
    windows_system: bool = False,
    quiet: bool = True,
    checkin_side_effect: Exception | None = None,
) -> SimpleNamespace:
    ctx = typer.Context(typer.main.get_command(skills_cmd.app))
    client = Mock(name="client")
    device_ctx = {
        "device_id": "device-1",
        "hostname": "host-1",
        "os": "darwin",
        "os_version": "15.0",
        "username": "alice",
        "org_device_id": None,
        "serial_number": "SERIAL123",
    }
    with (
        patch.object(skills_cmd, "setup_logging", return_value=Path("/tmp/log")),
        patch.object(skills_cmd.os, "geteuid", return_value=euid, create=True),
        patch.object(
            windows_users_mod, "is_windows_system_context", return_value=windows_system
        ),
        patch.object(
            skills_cmd, "read_managed_config", return_value=managed or {}
        ) as read_managed,
        patch.object(
            skills_cmd,
            "resolve_credentials",
            return_value={"host": _EFFECTIVE_HOST, "secret": "rl_org_scan"},
        ) as resolve_creds,
        patch.object(
            skills_cmd, "resolve_skill_sync_secret", return_value=sync_key
        ) as resolve_key,
        patch.object(skills_cmd, "RunlayerClient", return_value=client) as client_cls,
        patch(
            "runlayer_cli.scan.device.get_or_create_device_id",
            return_value="device-1",
        ),
        patch.object(ds, "sync_assigned_skills", return_value=report) as sync,
        patch.object(aiwatch_checkin, "_make_device_context", return_value=device_ctx),
        patch.object(
            aiwatch_checkin,
            "submit_skill_sync_checkin",
            side_effect=checkin_side_effect,
        ) as checkin,
        patch.object(aiwatch_checkin, "submit_skill_sync_disabled_checkin") as disabled,
    ):
        exit_code: int | None = None
        try:
            skills_cmd.sync(ctx, secret=secret, host=None, username=None, quiet=quiet)
        except typer.Exit as exc:
            exit_code = exc.exit_code
    return SimpleNamespace(
        client=client,
        client_cls=client_cls,
        read_managed=read_managed,
        resolve_creds=resolve_creds,
        resolve_key=resolve_key,
        sync=sync,
        checkin=checkin,
        disabled=disabled,
        exit_code=exit_code,
    )


class TestGating:
    def test_disabled_by_managed_config_exits_zero_without_disabled_checkin(self):
        # Manual verb: gate exits 0 quietly, no disabled check-in (that's the
        # scheduled job's contract, not the operator command's).
        run = _run_sync(managed={"sync_skills": False})

        assert run.exit_code == 0
        run.sync.assert_not_called()
        run.checkin.assert_not_called()
        run.disabled.assert_not_called()
        run.resolve_creds.assert_not_called()

    def test_disabled_gate_message(self, capsys: pytest.CaptureFixture[str]):
        _run_sync(managed={"sync_skills": False}, quiet=False)
        assert "disabled by managed configuration" in capsys.readouterr().out

    def test_root_skips_quietly(self):
        run = _run_sync(euid=0)

        assert run.exit_code == 0
        run.read_managed.assert_not_called()
        run.sync.assert_not_called()
        run.checkin.assert_not_called()

    def test_root_skip_message(self, capsys: pytest.CaptureFixture[str]):
        _run_sync(euid=0, quiet=False)
        assert "not root/SYSTEM" in capsys.readouterr().out

    def test_windows_system_skips_quietly(self):
        run = _run_sync(windows_system=True)

        assert run.exit_code == 0
        run.sync.assert_not_called()
        run.checkin.assert_not_called()


class TestCredentialOrder:
    def test_explicit_secret_beats_dedicated_sync_key(self):
        run = _run_sync(
            secret="rl_explicit", sync_key="rl_org_sync", report=ds.SyncReport()
        )

        run.client_cls.assert_called_once_with(
            hostname=_EFFECTIVE_HOST, secret="rl_explicit"
        )

    def test_dedicated_sync_key_used_for_sync_and_checkin(self):
        run = _run_sync(sync_key="rl_org_sync", report=ds.SyncReport(updated=["a"]))

        run.client_cls.assert_called_once_with(
            hostname=_EFFECTIVE_HOST, secret="rl_org_sync"
        )
        assert run.sync.call_args.args[0] is run.client
        run.checkin.assert_called_once()
        assert run.checkin.call_args.args[0] is run.client
        assert run.checkin.call_args.kwargs["tools"] == []
        assert run.checkin.call_args.kwargs["report"].updated == ["a"]

    def test_falls_back_to_resolved_credential_without_sync_key(self):
        run = _run_sync(sync_key=None, report=ds.SyncReport())

        run.client_cls.assert_called_once_with(
            hostname=_EFFECTIVE_HOST, secret="rl_org_scan"
        )
        run.checkin.assert_called_once()
        assert run.checkin.call_args.args[0] is run.client


class TestOutcomes:
    def test_keep_state_exits_zero_without_checkin(self):
        run = _run_sync(report=None)

        assert run.exit_code == 0
        run.checkin.assert_not_called()
        run.disabled.assert_not_called()

    def test_report_errors_exit_one_after_checkin(self):
        run = _run_sync(report=ds.SyncReport(errors=["a: boom"]))

        assert run.exit_code == 1
        run.checkin.assert_called_once()

    def test_report_includes_restored_bucket(self, capsys: pytest.CaptureFixture[str]):
        _run_sync(report=ds.SyncReport(restored=["my-skill"]), quiet=False)
        assert "1 restored" in capsys.readouterr().out

    def test_checkin_failure_swallowed(self):
        run = _run_sync(
            report=ds.SyncReport(), checkin_side_effect=RuntimeError("unexpected")
        )

        run.checkin.assert_called_once()
        assert run.exit_code in (None, 0)


class TestDedicatedKeyOnlyFleet:
    """A fleet pushing ONLY SkillSyncOrgApiKey (no OrgApiKey, no user login)
    must sync — exercised through the real resolve_credentials /
    resolve_skill_sync_secret seam, not wholesale mocks."""

    def test_syncs_with_only_skill_sync_org_api_key(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        import runlayer_cli.config as config_mod

        for var in ("RUNLAYER_API_KEY", "RUNLAYER_SKILL_SYNC_API_KEY", "RUNLAYER_HOST"):
            monkeypatch.delenv(var, raising=False)
        managed = {"host": _EFFECTIVE_HOST, "skill_sync_org_api_key": "rl_org_sync"}

        ctx = typer.Context(typer.main.get_command(skills_cmd.app))
        client = Mock(name="client")
        exit_code: int | None = None
        with (
            patch.object(skills_cmd, "setup_logging", return_value=Path("/tmp/log")),
            patch.object(skills_cmd.os, "geteuid", return_value=501, create=True),
            patch.object(
                windows_users_mod, "is_windows_system_context", return_value=False
            ),
            patch.object(skills_cmd, "read_managed_config", return_value=managed),
            patch.object(config_mod, "read_managed_config", return_value=managed),
            patch.object(config_mod, "load_config", return_value=config_mod.Config()),
            patch.object(
                skills_cmd, "RunlayerClient", return_value=client
            ) as client_cls,
            patch(
                "runlayer_cli.scan.device.get_or_create_device_id",
                return_value="device-1",
            ),
            patch.object(ds, "sync_assigned_skills", return_value=ds.SyncReport()),
            patch.object(aiwatch_checkin, "_make_device_context", return_value={}),
            patch.object(aiwatch_checkin, "submit_skill_sync_checkin"),
        ):
            try:
                skills_cmd.sync(ctx, secret=None, host=None, username=None, quiet=True)
            except typer.Exit as exc:
                exit_code = exc.exit_code

        assert exit_code in (None, 0)
        client_cls.assert_called_once_with(
            hostname=_EFFECTIVE_HOST, secret="rl_org_sync"
        )

    def test_no_secret_anywhere_errors(self, monkeypatch: pytest.MonkeyPatch):
        import runlayer_cli.config as config_mod

        for var in ("RUNLAYER_API_KEY", "RUNLAYER_SKILL_SYNC_API_KEY", "RUNLAYER_HOST"):
            monkeypatch.delenv(var, raising=False)
        managed = {"host": _EFFECTIVE_HOST}

        ctx = typer.Context(typer.main.get_command(skills_cmd.app))
        exit_code: int | None = None
        with (
            patch.object(skills_cmd, "setup_logging", return_value=Path("/tmp/log")),
            patch.object(skills_cmd.os, "geteuid", return_value=501, create=True),
            patch.object(
                windows_users_mod, "is_windows_system_context", return_value=False
            ),
            patch.object(skills_cmd, "read_managed_config", return_value=managed),
            patch.object(config_mod, "read_managed_config", return_value=managed),
            patch.object(config_mod, "load_config", return_value=config_mod.Config()),
            patch.object(ds, "sync_assigned_skills") as sync,
        ):
            try:
                skills_cmd.sync(ctx, secret=None, host=None, username=None, quiet=True)
            except typer.Exit as exc:
                exit_code = exc.exit_code

        assert exit_code == 1
        sync.assert_not_called()


class TestQuietErrors:
    def test_quiet_still_prints_report_errors(self, capsys: pytest.CaptureFixture[str]):
        run = _run_sync(report=ds.SyncReport(errors=["my-skill: boom"]), quiet=True)

        assert run.exit_code == 1
        captured = capsys.readouterr()
        assert "my-skill: boom" in captured.out + captured.err


class TestErrorSummaryLine:
    def test_errors_not_reported_as_green_success(
        self, capsys: pytest.CaptureFixture[str]
    ):
        run = _run_sync(
            report=ds.SyncReport(installed=["a"], errors=["b: boom"]), quiet=False
        )

        assert run.exit_code == 1
        out = capsys.readouterr().out
        assert "completed with errors" in out
        assert "Skill sync complete:" not in out
