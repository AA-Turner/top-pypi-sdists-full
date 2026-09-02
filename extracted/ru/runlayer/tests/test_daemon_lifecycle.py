"""Daemon supervisor reconciliation for the hourly MDM tick."""

from __future__ import annotations

import subprocess
from pathlib import Path

from runlayer_cli.hook_install import daemon_lifecycle


def _completed(command: list[str], returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(command, returncode, "", "")


def _set_frozen_windows_runtime(monkeypatch) -> None:
    executable = r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.setattr(daemon_lifecycle.sys, "frozen", True, raising=False)
    monkeypatch.setattr(daemon_lifecycle.sys, "executable", executable)
    monkeypatch.setenv("ProgramFiles", r"C:\Program Files")
    monkeypatch.setenv("ProgramW6432", r"C:\Program Files")


def test_embedded_launchagent_matches_packaged_asset() -> None:
    packaged = (
        Path(__file__).parent.parent
        / "packaging"
        / "macos"
        / "com.runlayer.aiwatch.daemon.plist"
    )

    assert packaged.read_bytes() == daemon_lifecycle.MACOS_AGENT_BYTES


def test_macos_ensure_rewrites_and_bootstraps_missing_agent(
    monkeypatch,
    tmp_path,
) -> None:
    agent_path = tmp_path / "Library/LaunchAgents/daemon.plist"
    home = tmp_path / "Users/alex"
    home.mkdir(parents=True)
    commands: list[list[str]] = []

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command, 1 if "print" in command else 0)

    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_AGENT_PATH", agent_path)
    monkeypatch.setattr(daemon_lifecycle, "find_console_user_home", lambda: home)
    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)
    monkeypatch.setattr(daemon_lifecycle.os, "chown", lambda *_args: None)
    monkeypatch.setattr(
        daemon_lifecycle,
        "probe_daemon",
        lambda *_args: (_ for _ in ()).throw(AssertionError("gate is off")),
    )

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert result.changed
    assert agent_path.read_bytes() == daemon_lifecycle.MACOS_AGENT_BYTES
    assert [command[1] for command in commands] == ["print", "bootstrap"]


def test_macos_ensure_scan_unit_bootstraps_unloaded_agent(
    monkeypatch,
    tmp_path,
) -> None:
    scan_agent_path = tmp_path / "Library/LaunchAgents/com.runlayer.aiwatch.plist"
    scan_agent_path.parent.mkdir(parents=True)
    scan_agent_path.write_text("packaged scan agent")
    home = tmp_path / "Users/alex"
    home.mkdir(parents=True)
    commands: list[list[str]] = []

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command, 1 if "print" in command else 0)

    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_SCAN_AGENT_PATH", scan_agent_path)
    monkeypatch.setattr(daemon_lifecycle, "find_console_user_home", lambda: home)
    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_scan_unit()

    assert result.ok
    assert result.changed
    assert commands == [
        [
            "/bin/launchctl",
            "print",
            f"gui/{home.stat().st_uid}/com.runlayer.aiwatch",
        ],
        [
            "/bin/launchctl",
            "bootstrap",
            f"gui/{home.stat().st_uid}",
            str(scan_agent_path),
        ],
    ]


def test_macos_ensure_kickstarts_unhealthy_gated_daemon(
    monkeypatch,
    tmp_path,
) -> None:
    agent_path = tmp_path / "daemon.plist"
    agent_path.write_bytes(daemon_lifecycle.MACOS_AGENT_BYTES)
    home = tmp_path / "alex"
    home.mkdir()
    probes = iter(
        [
            None,
            None,
            {
                "status": "ok",
                "version": daemon_lifecycle.protocol_version(),
            },
        ]
    )
    commands: list[list[str]] = []

    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_AGENT_PATH", agent_path)
    monkeypatch.setattr(daemon_lifecycle, "find_console_user_home", lambda: home)
    monkeypatch.setattr(
        daemon_lifecycle,
        "probe_daemon",
        lambda *_args: next(probes),
    )
    monkeypatch.setattr(daemon_lifecycle.time, "sleep", lambda _seconds: None)

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    assert any("kickstart" in command for command in commands)


def test_macos_ensure_retries_probe_before_kill_restart(
    monkeypatch,
    tmp_path,
) -> None:
    agent_path = tmp_path / "daemon.plist"
    agent_path.write_bytes(daemon_lifecycle.MACOS_AGENT_BYTES)
    home = tmp_path / "alex"
    home.mkdir()
    probes = iter(
        [
            None,
            {
                "status": "ok",
                "version": daemon_lifecycle.protocol_version(),
            },
        ]
    )
    commands: list[list[str]] = []
    sleeps: list[float] = []

    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_AGENT_PATH", agent_path)
    monkeypatch.setattr(daemon_lifecycle, "find_console_user_home", lambda: home)
    monkeypatch.setattr(
        daemon_lifecycle,
        "probe_daemon",
        lambda *_args: next(probes),
    )
    monkeypatch.setattr(daemon_lifecycle.time, "sleep", sleeps.append)

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert not result.changed
    assert sleeps == [0.5]
    assert not any("kickstart" in command for command in commands)


def test_macos_ensure_does_not_kickstart_draining_daemon(
    monkeypatch,
    tmp_path,
) -> None:
    agent_path = tmp_path / "daemon.plist"
    agent_path.write_bytes(daemon_lifecycle.MACOS_AGENT_BYTES)
    home = tmp_path / "alex"
    home.mkdir()
    commands: list[list[str]] = []

    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_AGENT_PATH", agent_path)
    monkeypatch.setattr(daemon_lifecycle, "find_console_user_home", lambda: home)
    monkeypatch.setattr(
        daemon_lifecycle,
        "probe_daemon",
        lambda *_args: {"status": "restarting"},
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert not result.changed
    assert not any("kickstart" in command for command in commands)


def test_macos_check_accepts_draining_daemon(
    monkeypatch,
    tmp_path,
) -> None:
    agent_path = tmp_path / "daemon.plist"
    agent_path.write_bytes(daemon_lifecycle.MACOS_AGENT_BYTES)
    home = tmp_path / "alex"
    home.mkdir()

    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_AGENT_PATH", agent_path)
    monkeypatch.setattr(daemon_lifecycle, "find_console_user_home", lambda: home)
    monkeypatch.setattr(
        daemon_lifecycle,
        "probe_daemon",
        lambda *_args: {"status": "restarting"},
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "_run_command",
        lambda command: _completed(command),
    )

    result = daemon_lifecycle.check_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert not result.changed


def test_macos_check_reports_stale_plist_without_mutation(
    monkeypatch,
    tmp_path,
) -> None:
    agent_path = tmp_path / "daemon.plist"
    agent_path.write_text("stale")
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(daemon_lifecycle, "MACOS_AGENT_PATH", agent_path)
    monkeypatch.setattr(
        daemon_lifecycle,
        "_run_command",
        lambda _command: (_ for _ in ()).throw(AssertionError("must not mutate")),
    )

    result = daemon_lifecycle.check_daemon_unit({})

    assert not result.ok
    assert "stale" in result.detail


def test_windows_ensure_removes_running_service_when_daemon_gate_closed(
    monkeypatch,
) -> None:
    commands: list[list[str]] = []
    stop_waits: list[float] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: (_ for _ in ()).throw(AssertionError("must not query config")),
    )

    def wait_for_state(
        expected: int | None,
        *,
        timeout: float = 15.0,
        absent_is_success: bool = False,
    ) -> bool:
        assert expected == daemon_lifecycle.SERVICE_STOPPED
        assert absent_is_success
        stop_waits.append(timeout)
        return True

    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service_state",
        wait_for_state,
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert result.changed
    assert result.detail == "gate closed; Windows service removed"
    assert commands == [
        ["sc.exe", "stop", daemon_lifecycle.SERVICE_NAME],
        ["sc.exe", "delete", daemon_lifecycle.SERVICE_NAME],
    ]
    assert stop_waits == [
        daemon_lifecycle.WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS,
    ]


def test_windows_ensure_accepts_service_deleted_while_stopping(monkeypatch) -> None:
    query_calls = 0
    commands: list[list[str]] = []
    monotonic_values = iter([0.0, 0.0, 36.0])
    _set_frozen_windows_runtime(monkeypatch)

    def query_state() -> int | None:
        nonlocal query_calls
        query_calls += 1
        if query_calls == 1:
            return daemon_lifecycle.SERVICE_RUNNING
        return None

    monkeypatch.setattr(daemon_lifecycle, "query_service_state", query_state)
    monkeypatch.setattr(
        daemon_lifecycle.time,
        "monotonic",
        lambda: next(monotonic_values),
    )
    monkeypatch.setattr(daemon_lifecycle.time, "sleep", lambda _seconds: None)

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert result.changed
    assert commands == [
        ["sc.exe", "stop", daemon_lifecycle.SERVICE_NAME],
        ["sc.exe", "delete", daemon_lifecycle.SERVICE_NAME],
    ]


def test_windows_ensure_is_noop_when_gate_closed_service_absent(
    monkeypatch,
) -> None:
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(daemon_lifecycle, "query_service_state", lambda: None)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: (_ for _ in ()).throw(AssertionError("must not query config")),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "_run_command",
        lambda _command: (_ for _ in ()).throw(AssertionError("must not mutate")),
    )

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert not result.changed
    assert result.detail == "gate closed; Windows service absent"


def test_windows_ensure_deletes_stopped_service_without_stopping(
    monkeypatch,
) -> None:
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_STOPPED,
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert result.changed
    assert commands == [["sc.exe", "delete", daemon_lifecycle.SERVICE_NAME]]


def test_windows_ensure_accepts_concurrent_delete_when_gate_closed(
    monkeypatch,
) -> None:
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_STOPPED,
    )

    for error in (1060, 1072):
        monkeypatch.setattr(
            daemon_lifecycle,
            "_run_command",
            lambda command, error=error: _completed(command, error),
        )

        result = daemon_lifecycle.ensure_daemon_unit(
            {"org_api_key": "rl_org_test", "daemon_enabled": False}
        )

        assert result.ok, error
        assert result.changed, error
        assert result.detail == "gate closed; Windows service removed"


def test_windows_ensure_reports_stop_timeout_when_gate_closed(monkeypatch) -> None:
    commands: list[list[str]] = []
    monotonic_values = iter([0.0, 0.0, 36.0])
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle.time,
        "monotonic",
        lambda: next(monotonic_values),
    )
    monkeypatch.setattr(daemon_lifecycle.time, "sleep", lambda _seconds: None)

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert not result.ok
    assert result.changed
    assert result.detail == "gate closed; Windows service removal failed: sc.exe stop"
    assert commands == [["sc.exe", "stop", daemon_lifecycle.SERVICE_NAME]]


def test_windows_ensure_recreates_configures_and_starts_service(monkeypatch) -> None:
    states = iter([None, 1, daemon_lifecycle.SERVICE_RUNNING])
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    verbs = [command[1] for command in commands]
    assert verbs == ["create", "description", "failure", "failureflag", "start"]
    create = commands[0]
    assert create[create.index("binPath=") + 1] == (
        '"C:\\Program Files\\Runlayer\\AIWatch\\aiwatch.exe" daemon-service'
    )


def test_windows_ensure_accepts_concurrent_service_create(monkeypatch) -> None:
    states = iter(
        [
            None,
            daemon_lifecycle.SERVICE_STOPPED,
            daemon_lifecycle.SERVICE_RUNNING,
        ]
    )
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        if command[1] == "create":
            return subprocess.CompletedProcess(
                command,
                1073,
                "[SC] CreateService FEHLER:\n",
                "",
            )
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    assert [command[1] for command in commands] == [
        "create",
        "description",
        "failure",
        "failureflag",
        "start",
    ]


def test_windows_ensure_is_noop_when_service_is_running(monkeypatch) -> None:
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path()
        ),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "_run_command",
        lambda _command: (_ for _ in ()).throw(AssertionError("no repair expected")),
    )

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert not result.changed


def test_windows_ensure_repairs_start_type_drift(monkeypatch) -> None:
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path(),
            start_type=3,
        ),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    assert commands == [
        [
            "sc.exe",
            "config",
            daemon_lifecycle.SERVICE_NAME,
            "start=",
            daemon_lifecycle.SERVICE_START_TYPE,
        ]
    ]


def test_windows_ensure_restarts_running_service_when_requested(monkeypatch) -> None:
    states = iter(
        [
            daemon_lifecycle.SERVICE_RUNNING,
            daemon_lifecycle.SERVICE_STOPPED,
            daemon_lifecycle.SERVICE_RUNNING,
        ]
    )
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path()
        ),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True},
        restart_windows_service=True,
    )

    assert result.ok
    assert result.changed
    assert [command[1] for command in commands] == ["stop", "start"]


def test_windows_gate_flip_restart_waits_through_service_stop_window(
    monkeypatch,
) -> None:
    clock = 0.0
    stop_requested = False
    start_requested = False
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)

    def query_state() -> int:
        if start_requested:
            return daemon_lifecycle.SERVICE_RUNNING
        if stop_requested:
            if clock >= 30.2:
                return daemon_lifecycle.SERVICE_STOPPED
            return 3  # SERVICE_STOP_PENDING
        return daemon_lifecycle.SERVICE_RUNNING

    def run(command: list[str]) -> subprocess.CompletedProcess:
        nonlocal start_requested, stop_requested
        commands.append(command)
        if command[1] == "stop":
            stop_requested = True
        elif command[1] == "start":
            start_requested = True
        return _completed(command)

    def sleep(delay: float) -> None:
        nonlocal clock
        clock += delay

    monkeypatch.setattr(daemon_lifecycle, "query_service_state", query_state)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path()
        ),
    )
    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)
    monkeypatch.setattr(daemon_lifecycle.time, "monotonic", lambda: clock)
    monkeypatch.setattr(daemon_lifecycle.time, "sleep", sleep)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True},
        restart_windows_service=True,
    )

    assert result.ok
    assert [command[1] for command in commands] == ["stop", "start"]


def test_windows_gate_flip_restart_retries_start_with_full_budget(
    monkeypatch,
) -> None:
    commands: list[list[str]] = []
    running_waits: list[float] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path()
        ),
    )

    def wait_for_state(expected: int | None, *, timeout: float = 15.0) -> bool:
        assert expected == daemon_lifecycle.SERVICE_STOPPED
        assert timeout == daemon_lifecycle.WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS
        return True

    def wait_for_running(*, timeout: float) -> bool:
        running_waits.append(timeout)
        return len(running_waits) == 2

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service_state",
        wait_for_state,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service",
        wait_for_running,
    )
    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True},
        restart_windows_service=True,
    )

    assert result.ok
    assert result.changed
    assert [command[1] for command in commands] == ["stop", "start", "start"]
    assert running_waits == [
        daemon_lifecycle.WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS,
        daemon_lifecycle.WINDOWS_GATE_FLIP_STOP_TIMEOUT_SECONDS,
    ]


def test_windows_gate_flip_restart_reports_start_failure(
    monkeypatch,
) -> None:
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path()
        ),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service_state",
        lambda _expected, **_kwargs: True,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service",
        lambda *, timeout: False,
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True},
        restart_windows_service=True,
    )

    assert not result.ok
    assert result.changed
    assert result.detail == "Windows service gate-flip restart failed: sc.exe start"
    assert [command[1] for command in commands] == ["stop", "start", "start"]


def test_windows_ensure_starts_stopped_service_when_config_is_unavailable(
    monkeypatch,
) -> None:
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_STOPPED,
    )
    monkeypatch.setattr(daemon_lifecycle, "query_service_config", lambda: None)
    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service",
        lambda: True,
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert not result.ok
    assert result.changed
    assert result.detail == "Windows service config unavailable"
    assert commands == [["sc.exe", "start", daemon_lifecycle.SERVICE_NAME]]


def test_windows_ensure_recreates_service_when_binary_path_drifted(
    monkeypatch,
) -> None:
    states = iter(
        [
            daemon_lifecycle.SERVICE_RUNNING,
            daemon_lifecycle.SERVICE_STOPPED,
            None,
            daemon_lifecycle.SERVICE_STOPPED,
            daemon_lifecycle.SERVICE_RUNNING,
        ]
    )
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path='"C:\\stale\\aiwatch.exe" daemon-service'
        ),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    assert [command[1] for command in commands] == [
        "stop",
        "delete",
        "create",
        "description",
        "failure",
        "failureflag",
        "start",
    ]


def test_windows_ensure_does_not_repoint_service_from_staged_binary(
    monkeypatch,
) -> None:
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle.sys,
        "executable",
        r"C:\Windows\Temp\aiwatch-stage\aiwatch.exe",
    )
    monkeypatch.setenv("ProgramFiles", r"C:\Program Files")
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path='"C:\\stale\\aiwatch.exe" daemon-service'
        ),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert not result.changed
    assert result.detail == (
        "not the canonical install; skipping Windows service repair"
    )
    assert commands == []


def test_windows_canonical_guard_resolves_short_executable_path(monkeypatch) -> None:
    canonical = r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle.sys,
        "executable",
        r"C:\PROGRA~1\Runlayer\AIWatch\aiwatch.exe",
    )
    monkeypatch.setattr(daemon_lifecycle.os.path, "realpath", lambda _path: canonical)

    assert daemon_lifecycle._running_from_canonical_windows_install()


def test_windows_canonical_executable_prefers_programw6432(monkeypatch) -> None:
    monkeypatch.setenv("ProgramFiles", r"C:\Program Files (x86)")
    monkeypatch.setenv("ProgramW6432", r"C:\Program Files")

    assert daemon_lifecycle._canonical_windows_executable() == (
        r"C:\Program Files\Runlayer\AIWatch\aiwatch.exe"
    )


def test_windows_ensure_reports_missing_program_files_environment(monkeypatch) -> None:
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.delenv("ProgramFiles")
    monkeypatch.delenv("ProgramW6432", raising=False)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert not result.ok
    assert not result.changed
    assert result.detail == (
        "Windows service repair requires ProgramW6432 or ProgramFiles"
    )


def test_windows_ensure_recreates_while_deleted_service_remains_queryable(
    monkeypatch,
) -> None:
    states = iter(
        [
            daemon_lifecycle.SERVICE_RUNNING,
            daemon_lifecycle.SERVICE_STOPPED,
        ]
    )
    waited_for: list[int | None] = []
    commands: list[list[str]] = []
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path='"C:\\stale\\aiwatch.exe" daemon-service'
        ),
    )

    def wait_for_state(expected: int | None, **_kwargs) -> bool:
        waited_for.append(expected)
        return expected is not None

    def run(command: list[str]) -> subprocess.CompletedProcess:
        commands.append(command)
        return _completed(command)

    monkeypatch.setattr(
        daemon_lifecycle,
        "_wait_for_windows_service_state",
        wait_for_state,
    )
    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    assert waited_for == [
        daemon_lifecycle.SERVICE_STOPPED,
        daemon_lifecycle.SERVICE_RUNNING,
    ]
    assert [command[1] for command in commands] == [
        "stop",
        "delete",
        "create",
        "description",
        "failure",
        "failureflag",
        "start",
    ]


def test_windows_ensure_accepts_concurrent_stop_and_delete(monkeypatch) -> None:
    states = iter(
        [
            daemon_lifecycle.SERVICE_RUNNING,
            daemon_lifecycle.SERVICE_STOPPED,
            None,
            daemon_lifecycle.SERVICE_STOPPED,
            daemon_lifecycle.SERVICE_RUNNING,
        ]
    )
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path='"C:\\stale\\aiwatch.exe" daemon-service'
        ),
    )

    def run(command: list[str]) -> subprocess.CompletedProcess:
        returncode = 1 if command[1] in {"stop", "delete"} else 0
        return _completed(command, returncode)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed


def test_windows_ensure_retries_create_when_service_marked_for_delete(
    monkeypatch,
) -> None:
    states = iter(
        [
            daemon_lifecycle.SERVICE_RUNNING,
            daemon_lifecycle.SERVICE_STOPPED,
            None,
            daemon_lifecycle.SERVICE_STOPPED,
            daemon_lifecycle.SERVICE_RUNNING,
        ]
    )
    commands: list[list[str]] = []
    create_attempts = 0
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: next(states),
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path='"C:\\stale\\aiwatch.exe" daemon-service'
        ),
    )
    monkeypatch.setattr(daemon_lifecycle.time, "sleep", lambda _seconds: None)

    def run(command: list[str]) -> subprocess.CompletedProcess:
        nonlocal create_attempts
        commands.append(command)
        if command[1] == "create":
            create_attempts += 1
            if create_attempts == 1:
                return subprocess.CompletedProcess(
                    command,
                    1072,
                    "[SC] CreateService FEHLER:\n",
                    "",
                )
        return _completed(command)

    monkeypatch.setattr(daemon_lifecycle, "_run_command", run)

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert result.ok
    assert result.changed
    assert [command[1] for command in commands] == [
        "stop",
        "delete",
        "create",
        "create",
        "description",
        "failure",
        "failureflag",
        "start",
    ]


def test_windows_error_code_match_requires_sc_failed_shape() -> None:
    command = ["sc.exe", "create", daemon_lifecycle.SERVICE_NAME]

    assert daemon_lifecycle._command_output_reports_error(
        subprocess.CompletedProcess(
            command,
            1072,
            "[SC] CreateService FEHLER:\n",
            "",
        ),
        1072,
    )
    assert daemon_lifecycle._command_output_reports_error(
        subprocess.CompletedProcess(
            command,
            1,
            "[SC] CreateService FAILED 1072:\n",
            "",
        ),
        1072,
    )
    assert not daemon_lifecycle._command_output_reports_error(
        subprocess.CompletedProcess(
            command,
            1,
            "diagnostic record 1072 was unrelated\n",
            "",
        ),
        1072,
    )


def test_run_command_replaces_undecodable_output(monkeypatch) -> None:
    def run(command, **kwargs):
        assert kwargs["errors"] == "replace"
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(daemon_lifecycle.subprocess, "run", run)

    assert daemon_lifecycle._run_command(["sc.exe", "query"]).returncode == 0


def test_windows_ensure_does_not_register_unfrozen_python(monkeypatch) -> None:
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.delattr(daemon_lifecycle.sys, "frozen", raising=False)
    monkeypatch.setattr(daemon_lifecycle, "query_service_state", lambda: None)
    monkeypatch.setattr(
        daemon_lifecycle,
        "_run_command",
        lambda _command: (_ for _ in ()).throw(AssertionError("must not register")),
    )

    result = daemon_lifecycle.ensure_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert not result.ok
    assert "frozen" in result.detail


def test_windows_check_accepts_absent_service_when_gate_closed(monkeypatch) -> None:
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.setattr(daemon_lifecycle, "query_service_state", lambda: None)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: (_ for _ in ()).throw(AssertionError("must not query config")),
    )

    result = daemon_lifecycle.check_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert result.ok
    assert not result.changed
    assert result.detail == "gate closed; Windows service absent"


def test_windows_check_reports_present_service_when_gate_closed(monkeypatch) -> None:
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: (_ for _ in ()).throw(AssertionError("must not query config")),
    )

    result = daemon_lifecycle.check_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": False}
    )

    assert not result.ok
    assert not result.changed
    assert result.detail == "Windows service present while daemon gate closed"


def test_windows_check_reports_stopped_service(monkeypatch) -> None:
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.setattr(daemon_lifecycle, "query_service_state", lambda: 1)

    result = daemon_lifecycle.check_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert not result.ok
    assert "state=1" in result.detail


def test_windows_check_reports_scm_query_error(monkeypatch) -> None:
    monkeypatch.setattr(daemon_lifecycle.platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: (_ for _ in ()).throw(OSError(5, "OpenServiceW failed")),
    )

    result = daemon_lifecycle.check_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert not result.ok
    assert "SCM query failed" in result.detail
    assert "OpenServiceW failed" in result.detail


def test_windows_check_reports_start_type_drift(monkeypatch) -> None:
    _set_frozen_windows_runtime(monkeypatch)
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_state",
        lambda: daemon_lifecycle.SERVICE_RUNNING,
    )
    monkeypatch.setattr(
        daemon_lifecycle,
        "query_service_config",
        lambda: daemon_lifecycle.ServiceConfig(
            binary_path=daemon_lifecycle._expected_windows_binary_path(),
            start_type=3,
        ),
    )

    result = daemon_lifecycle.check_daemon_unit(
        {"org_api_key": "rl_org_test", "daemon_enabled": True}
    )

    assert not result.ok
    assert result.detail == "Windows service start type drifted"
