"""Operator-facing daemon status health check."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from runlayer_cli.daemon import status


def test_status_is_healthy_only_when_daemon_and_supervisor_are_running(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(status, "protocol_version", lambda: "1.2.3")
    monkeypatch.setattr(
        status,
        "probe_daemon",
        lambda: {"status": "ok", "version": "1.2.3"},
    )
    monkeypatch.setattr(status, "supervisor_is_running", lambda: True)
    monkeypatch.setattr(status.sys, "platform", "darwin")

    assert status.run_status() == 0
    assert capsys.readouterr().out == (
        "daemon: running (version 1.2.3)\nlaunch-agent: running\n"
    )


def test_linux_status_reports_unsupported_and_succeeds(monkeypatch, capsys) -> None:
    monkeypatch.setattr(status.sys, "platform", "linux")
    monkeypatch.setattr(
        status,
        "probe_daemon",
        lambda: (_ for _ in ()).throw(AssertionError("must not probe on Linux")),
    )

    assert status.run_status() == 0
    assert capsys.readouterr().out == "daemon: not supported on this platform\n"


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        (None, "daemon: unavailable"),
        ({"status": "restarting"}, "daemon: restarting"),
        (
            {"status": "ok", "version": "1.2.2"},
            "daemon: version mismatch (running 1.2.2, expected 1.2.3)",
        ),
    ],
)
def test_status_reports_unavailable_or_stale_daemon(
    monkeypatch,
    capsys,
    response,
    expected,
) -> None:
    monkeypatch.setattr(status, "protocol_version", lambda: "1.2.3")
    monkeypatch.setattr(status, "probe_daemon", lambda: response)
    monkeypatch.setattr(status, "supervisor_is_running", lambda: True)
    monkeypatch.setattr(status.sys, "platform", "win32")

    assert status.run_status() == 1
    assert expected in capsys.readouterr().out


def test_macos_supervisor_query_uses_current_gui_domain(monkeypatch) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr(status.sys, "platform", "darwin")
    monkeypatch.setattr(status.os, "getuid", lambda: 501)

    def run(command, **_kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout="")

    monkeypatch.setattr(status.subprocess, "run", run)

    assert status.supervisor_is_running()
    assert calls == [
        [
            "/bin/launchctl",
            "print",
            "gui/501/com.runlayer.aiwatch.daemon",
        ]
    ]


def test_root_macos_status_targets_console_user(
    monkeypatch,
    capsys,
    tmp_path,
) -> None:
    home = tmp_path / "alex"
    home.mkdir()
    uid = home.stat().st_uid
    endpoints: list[str | None] = []
    commands: list[list[str]] = []
    monkeypatch.setattr(status.sys, "platform", "darwin")
    monkeypatch.setattr(status, "_is_elevated", lambda: True)
    monkeypatch.setattr(status, "find_console_user_home", lambda: home)
    monkeypatch.setattr(status, "protocol_version", lambda: "1.2.3")

    def probe(endpoint=None):
        endpoints.append(endpoint)
        return {"status": "ok", "version": "1.2.3"}

    def run(command, **_kwargs):
        commands.append(command)
        return SimpleNamespace(returncode=0, stdout="")

    monkeypatch.setattr(status, "probe_daemon", probe)
    monkeypatch.setattr(status.subprocess, "run", run)

    assert status.run_status() == 0
    assert endpoints == [
        str(home / "Library" / "Application Support" / "Runlayer" / "aiwatch.sock")
    ]
    assert commands[0][2] == f"gui/{uid}/com.runlayer.aiwatch.daemon"
    assert "hint:" not in capsys.readouterr().out


def test_elevated_windows_unavailable_daemon_prints_user_hint(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(status.sys, "platform", "win32")
    monkeypatch.setattr(status, "_is_elevated", lambda: True)
    monkeypatch.setattr(status, "probe_daemon", lambda: None)
    monkeypatch.setattr(status, "supervisor_is_running", lambda: True)

    assert status.run_status() == 1
    assert (
        "hint: if you are not the logged-in user, re-run as them\n"
        in capsys.readouterr().out
    )


def test_elevated_windows_stale_daemon_does_not_print_user_hint(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(status.sys, "platform", "win32")
    monkeypatch.setattr(status, "_is_elevated", lambda: True)
    monkeypatch.setattr(status, "protocol_version", lambda: "1.2.3")
    monkeypatch.setattr(
        status,
        "probe_daemon",
        lambda: {"status": "ok", "version": "1.2.2"},
    )
    monkeypatch.setattr(status, "supervisor_is_running", lambda: True)

    assert status.run_status() == 1
    assert "run as the logged-in user" not in capsys.readouterr().out


def test_windows_status_reports_scm_access_error(monkeypatch, capsys) -> None:
    monkeypatch.setattr(status.sys, "platform", "win32")
    monkeypatch.setattr(status, "_is_elevated", lambda: False)
    monkeypatch.setattr(status, "probe_daemon", lambda: None)
    monkeypatch.setattr(
        status,
        "query_service_state",
        lambda: (_ for _ in ()).throw(OSError(5, "OpenServiceW failed")),
    )

    assert status.run_status() == 1
    assert "service: unavailable ([Errno 5] OpenServiceW failed)" in (
        capsys.readouterr().out
    )


@pytest.mark.parametrize(
    ("state", "running"),
    [(status.SERVICE_RUNNING, True), (1, False), (None, False)],
)
def test_windows_supervisor_query_checks_scm_running_state(
    monkeypatch,
    state,
    running,
) -> None:
    monkeypatch.setattr(status.sys, "platform", "win32")
    monkeypatch.setattr(
        status,
        "query_service_state",
        lambda: state,
    )

    assert status.supervisor_is_running() is running
