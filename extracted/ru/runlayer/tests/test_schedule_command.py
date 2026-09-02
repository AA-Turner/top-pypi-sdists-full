"""Tests for ``runlayer schedule`` (per-user scheduler LaunchAgent job).

The scheduler's contract: every gated or failed state is a quiet exit 0
(launchd must never see noise on unconfigured devices), tasks run isolated
(one task's failure never blocks the next), and MDM-disabled skill sync is
reported as an explicit ``disabled`` check-in so the backend can tell
"intentionally off" from "never ran".
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
import typer

import runlayer_cli.aiwatch_checkin as aiwatch_checkin
import runlayer_cli.commands.schedule as schedule_mod
import runlayer_cli.skills.device_sync as ds
from runlayer_cli.commands.schedule import ScheduledTask, schedule
from runlayer_cli.scan import windows_users

_HOST = "https://tenant.runlayer.com"


def _run(
    *,
    managed: dict | None = None,
    sync_key: str | None = None,
    report: ds.SyncReport | None = None,
    privileged: bool = False,
    sync_side_effect: Exception | None = None,
    checkin_side_effect: Exception | None = None,
    disabled_side_effect: Exception | None = None,
) -> SimpleNamespace:
    if sync_key is not None:
        managed = {**(managed or {}), "skill_sync_org_api_key": sync_key}
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
        patch.object(schedule_mod, "_privileged_sync_context", return_value=privileged),
        patch.object(
            schedule_mod, "read_managed_config", return_value=managed or {}
        ) as read_managed,
        patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=True),
        patch.dict("os.environ", {"RUNLAYER_SKILL_SYNC_API_KEY": ""}),
        patch.object(schedule_mod, "RunlayerClient", return_value=client) as client_cls,
        patch(
            "runlayer_cli.scan.device.get_or_create_device_id",
            return_value="device-1",
        ),
        patch.object(
            ds,
            "sync_assigned_skills",
            return_value=report,
            side_effect=sync_side_effect,
        ) as sync,
        patch.object(aiwatch_checkin, "_make_device_context", return_value=device_ctx),
        patch.object(
            aiwatch_checkin,
            "submit_skill_sync_checkin",
            side_effect=checkin_side_effect,
        ) as checkin,
        patch.object(
            aiwatch_checkin,
            "submit_skill_sync_disabled_checkin",
            side_effect=disabled_side_effect,
        ) as disabled,
    ):
        schedule()  # must never raise, whatever the state
    return SimpleNamespace(
        client=client,
        client_cls=client_cls,
        read_managed=read_managed,
        sync=sync,
        checkin=checkin,
        disabled=disabled,
    )


_CONFIGURED = {"host": _HOST, "org_api_key": "rl_org_key"}


class TestAllUsersDispatch:
    def test_dispatches_before_reading_managed_config(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        orchestrator = Mock(return_value=0)
        read_managed = Mock()
        monkeypatch.setattr(windows_users, "run_all_users_schedule", orchestrator)
        monkeypatch.setattr(schedule_mod, "read_managed_config", read_managed)

        schedule(all_users=True)

        orchestrator.assert_called_once_with()
        read_managed.assert_not_called()

    def test_propagates_orchestrator_failure(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users, "run_all_users_schedule", lambda: 2)

        with pytest.raises(typer.Exit) as exc_info:
            schedule(all_users=True)

        assert exc_info.value.exit_code == 2


class TestAllUsersOrchestrator:
    @staticmethod
    def _profile(sid: str, username: str) -> windows_users.RealUserProfile:
        return windows_users.RealUserProfile(
            sid=sid,
            profile_path=Path(rf"C:\Users\{username}"),
            username=username,
        )

    def test_non_windows_is_misconfigured(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Linux")

        assert windows_users.run_all_users_schedule() == windows_users.EXIT_MISCONFIG

    def test_non_system_is_misconfigured(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Windows")
        monkeypatch.setattr(windows_users, "is_running_as_system", lambda: False)

        assert windows_users.run_all_users_schedule() == windows_users.EXIT_MISCONFIG

    def test_runs_only_logged_on_users_with_dropped_tokens(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        alice = self._profile("S-1-12-1-1-2-3-4", "alice")
        bob = self._profile("S-1-5-21-1-2-3-1001", "bob")
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Windows")
        monkeypatch.setattr(windows_users, "is_running_as_system", lambda: True)
        monkeypatch.setattr(
            windows_users,
            "enumerate_real_user_profiles",
            lambda: [alice, bob],
        )
        monkeypatch.setattr(
            windows_users,
            "active_session_sids",
            lambda: {alice.sid: 7},
        )
        launches: list[tuple[int, list[str], int]] = []

        def launch(session_id: int, argv: list[str], timeout: int) -> int:
            launches.append((session_id, argv, timeout))
            return 0

        monkeypatch.setattr(windows_users, "launch_argv_as_user", launch)

        code = windows_users.run_all_users_schedule(timeout=42)

        assert code == 0
        assert launches == [(7, [windows_users.sys.executable, "schedule"], 42)]

    def test_user_failures_are_isolated_and_aggregated(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        profiles = [
            self._profile("S-1-5-21-1-2-3-1001", "alice"),
            self._profile("S-1-5-21-1-2-3-1002", "bob"),
            self._profile("S-1-5-21-1-2-3-1003", "carol"),
        ]
        monkeypatch.setattr(windows_users.platform, "system", lambda: "Windows")
        monkeypatch.setattr(windows_users, "is_running_as_system", lambda: True)
        monkeypatch.setattr(
            windows_users,
            "enumerate_real_user_profiles",
            lambda: profiles,
        )
        monkeypatch.setattr(
            windows_users,
            "active_session_sids",
            lambda: {profile.sid: index for index, profile in enumerate(profiles, 1)},
        )
        launched: list[int] = []

        def launch(session_id: int, argv: list[str], timeout: int) -> int:
            del argv, timeout
            launched.append(session_id)
            if session_id == 2:
                raise OSError("token launch failed")
            return 1 if session_id == 1 else 0

        monkeypatch.setattr(windows_users, "launch_argv_as_user", launch)

        assert windows_users.run_all_users_schedule() == 1
        assert launched == [1, 2, 3]


class TestRegistryGating:
    def test_privileged_context_makes_skill_sync_not_due(self):
        run = _run(privileged=True, managed=_CONFIGURED)

        run.client_cls.assert_not_called()
        run.sync.assert_not_called()
        run.checkin.assert_not_called()
        run.disabled.assert_not_called()

    def test_no_managed_host_not_due(self):
        run = _run(managed={"org_api_key": "rl_org_key"})

        run.client_cls.assert_not_called()
        run.sync.assert_not_called()
        run.disabled.assert_not_called()

    def test_no_key_not_due(self):
        run = _run(managed={"host": _HOST})

        run.client_cls.assert_not_called()
        run.sync.assert_not_called()
        run.disabled.assert_not_called()

    def test_gated_task_run_never_called(self):
        run_fn = Mock(name="run_fn")
        task = ScheduledTask(name="t", should_run=lambda managed: False, run=run_fn)
        with (
            patch.object(schedule_mod, "_TASKS", (task,)),
            patch.object(schedule_mod, "read_managed_config", return_value={}),
        ):
            schedule()
        run_fn.assert_not_called()

    def test_managed_config_read_failure_swallowed(self):
        run_fn = Mock(name="run_fn")
        task = ScheduledTask(name="t", should_run=lambda managed: True, run=run_fn)
        with (
            patch.object(schedule_mod, "_TASKS", (task,)),
            patch.object(
                schedule_mod,
                "read_managed_config",
                side_effect=RuntimeError("plist exploded"),
            ),
        ):
            schedule()  # no raise
        run_fn.assert_not_called()


class TestUvToolCleanup:
    def test_cleanup_task_is_last(self):
        assert schedule_mod._TASKS[-1].name == "uv_tool_cleanup"

    def test_marker_and_privileged_context_gate_cleanup(self):
        with (
            patch.object(schedule_mod, "_privileged_sync_context", return_value=False),
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=True),
        ):
            assert schedule_mod._uv_tool_cleanup_should_run(_CONFIGURED) is False

        with (
            patch.object(schedule_mod, "_privileged_sync_context", return_value=True),
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=False),
        ):
            assert schedule_mod._uv_tool_cleanup_should_run(_CONFIGURED) is False

    def test_unconfigured_cleanup_is_not_due(self):
        with (
            patch.object(schedule_mod, "_privileged_sync_context", return_value=False),
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=False),
            patch.dict(
                "os.environ",
                {
                    "RUNLAYER_API_KEY": "",
                    "RUNLAYER_SKILL_SYNC_API_KEY": "",
                },
            ),
        ):
            assert schedule_mod._uv_tool_cleanup_should_run({"host": _HOST}) is False

    def test_linux_env_key_makes_cleanup_due(self):
        with (
            patch.object(schedule_mod, "_privileged_sync_context", return_value=False),
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=False),
            patch.dict("os.environ", {"RUNLAYER_API_KEY": "rl_org_linux"}),
        ):
            assert schedule_mod._uv_tool_cleanup_should_run({"host": _HOST}) is True

    def test_user_key_does_not_make_cleanup_due(self):
        with (
            patch.object(schedule_mod, "_privileged_sync_context", return_value=False),
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=False),
            patch.dict(
                "os.environ",
                {
                    "RUNLAYER_API_KEY": "rl_user_key",
                    "RUNLAYER_SKILL_SYNC_API_KEY": "",
                },
            ),
        ):
            assert (
                schedule_mod._uv_tool_cleanup_should_run(
                    {"host": _HOST, "org_api_key": "rl_user_managed"}
                )
                is False
            )

    def test_user_key_does_not_mask_later_org_key(self):
        with patch.dict(
            "os.environ",
            {
                "RUNLAYER_API_KEY": "rl_org_linux",
                "RUNLAYER_SKILL_SYNC_API_KEY": "",
            },
        ):
            assert (
                schedule_mod._resolve_ai_watch_config_secret_for(
                    {"host": _HOST, "org_api_key": "rl_user_managed"}
                )
                == "rl_org_linux"
            )

    @pytest.mark.parametrize("enabled", [False, True])
    def test_backend_setting_controls_cleanup_and_marker(self, enabled: bool):
        client = Mock()
        client.get_aiwatch_config.return_value = {"remove_uv_tool": enabled}
        with (
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=False),
            patch.object(schedule_mod, "RunlayerClient", return_value=client),
            patch.object(
                schedule_mod, "cleanup_uv_tool", return_value=False
            ) as cleanup,
            patch.object(schedule_mod, "write_uv_tool_removed_marker") as write_marker,
        ):
            schedule_mod._run_uv_tool_cleanup(_CONFIGURED)

        if enabled:
            cleanup.assert_called_once_with()
            write_marker.assert_called_once_with()
        else:
            cleanup.assert_not_called()
            write_marker.assert_not_called()

    def test_unsupported_backend_does_not_mark_complete(self):
        client = Mock()
        client.get_aiwatch_config.return_value = None
        with (
            patch.object(schedule_mod, "uv_tool_cleanup_completed", return_value=False),
            patch.object(schedule_mod, "RunlayerClient", return_value=client),
            patch.object(schedule_mod, "cleanup_uv_tool") as cleanup,
            patch.object(schedule_mod, "write_uv_tool_removed_marker") as write_marker,
        ):
            schedule_mod._run_uv_tool_cleanup(_CONFIGURED)

        cleanup.assert_not_called()
        write_marker.assert_not_called()


class TestTaskIsolation:
    def test_first_task_raising_does_not_stop_the_second(self):
        first = Mock(name="first", side_effect=RuntimeError("boom"))
        second = Mock(name="second")
        tasks = (
            ScheduledTask(name="a", should_run=lambda managed: True, run=first),
            ScheduledTask(name="b", should_run=lambda managed: True, run=second),
        )
        with (
            patch.object(schedule_mod, "_TASKS", tasks),
            patch.object(schedule_mod, "read_managed_config", return_value={}),
        ):
            schedule()  # no raise
        first.assert_called_once()
        second.assert_called_once()

    def test_raising_gate_does_not_stop_the_next_task(self):
        def _bad_gate(managed):
            raise RuntimeError("gate boom")

        second = Mock(name="second")
        tasks = (
            ScheduledTask(name="a", should_run=_bad_gate, run=Mock()),
            ScheduledTask(name="b", should_run=lambda managed: True, run=second),
        )
        with (
            patch.object(schedule_mod, "_TASKS", tasks),
            patch.object(schedule_mod, "read_managed_config", return_value={}),
        ):
            schedule()
        second.assert_called_once()

    def test_tasks_receive_the_shared_managed_snapshot(self):
        seen: list[dict] = []
        task = ScheduledTask(name="t", should_run=lambda managed: True, run=seen.append)
        with (
            patch.object(schedule_mod, "_TASKS", (task,)),
            patch.object(
                schedule_mod, "read_managed_config", return_value={"host": _HOST}
            ),
        ):
            schedule()
        assert seen == [{"host": _HOST}]


class TestSkillSyncDisabledCheckin:
    def test_sync_skills_false_emits_disabled_checkin_and_no_sync(self):
        run = _run(managed={**_CONFIGURED, "sync_skills": False})

        run.disabled.assert_called_once()
        assert run.disabled.call_args.args[0] is run.client
        assert run.disabled.call_args.kwargs["tools"] == []
        run.sync.assert_not_called()
        run.checkin.assert_not_called()

    def test_disabled_checkin_failure_swallowed(self):
        run = _run(
            managed={**_CONFIGURED, "sync_skills": False},
            disabled_side_effect=RuntimeError("offline"),
        )

        run.disabled.assert_called_once()  # the raising path actually ran
        run.sync.assert_not_called()


class TestSkillSyncHappyPath:
    def test_sync_and_checkin_with_org_key(self):
        run = _run(managed=_CONFIGURED, report=ds.SyncReport(installed=["a"]))

        run.client_cls.assert_called_once_with(hostname=_HOST, secret="rl_org_key")
        assert run.sync.call_args.args[0] is run.client
        assert run.sync.call_args.kwargs["device_id"] == "device-1"
        run.checkin.assert_called_once()
        assert run.checkin.call_args.args[0] is run.client
        assert run.checkin.call_args.kwargs["report"].installed == ["a"]
        run.disabled.assert_not_called()

    def test_dedicated_sync_key_beats_org_key(self):
        run = _run(managed=_CONFIGURED, sync_key="rl_org_sync", report=ds.SyncReport())

        run.client_cls.assert_called_once_with(hostname=_HOST, secret="rl_org_sync")

    def test_snapshot_dedicated_key_resolves_without_second_mdm_read(self):
        """A snapshot carrying only the dedicated key must resolve from the
        snapshot itself — a second MDM disk read lets gate and run diverge
        if the plist changes mid-tick."""
        managed = {"host": _HOST, "skill_sync_org_api_key": "rl_sync_key"}
        with patch.dict("os.environ", {"RUNLAYER_SKILL_SYNC_API_KEY": ""}):
            secret = schedule_mod._resolve_skill_sync_secret_for(managed)
        assert secret == "rl_sync_key"

    def test_managed_username_forwarded(self):
        run = _run(
            managed={**_CONFIGURED, "username": "mdm-user"}, report=ds.SyncReport()
        )

        assert run.sync.call_args.kwargs["username"] == "mdm-user"


class TestSkillSyncFailureTolerance:
    def test_keep_state_no_checkin(self):
        run = _run(managed=_CONFIGURED, report=None)

        run.checkin.assert_not_called()
        run.disabled.assert_not_called()

    def test_sync_raising_is_swallowed(self):
        run = _run(managed=_CONFIGURED, sync_side_effect=RuntimeError("boom"))

        run.checkin.assert_not_called()

    def test_checkin_network_failure_swallowed(self):
        run = _run(
            managed=_CONFIGURED,
            report=ds.SyncReport(),
            checkin_side_effect=RuntimeError("offline"),
        )

        run.checkin.assert_called_once()
