"""Thin aiwatch entrypoint routes daemon-first hooks without losing fallback stdin."""

from __future__ import annotations

import io
import time

import pytest

from runlayer_cli import aiwatch, command_metrics, flow_trace
from runlayer_cli.daemon import server, status as daemon_status, windows_service
from runlayer_cli.hook import daemon_client, dispatch, hook_io
from runlayer_cli.hook.daemon_protocol import CLIENT_START_ENV


def test_daemon_served_hook_writes_captured_streams_and_exit(
    monkeypatch, capsys
) -> None:
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)
    monkeypatch.setattr(
        daemon_client,
        "try_daemon_hook",
        lambda stdin, **_kwargs: {
            "stdout": f"out:{stdin}",
            "stderr": "daemon stderr",
            "exit_code": 2,
        },
    )
    monkeypatch.setattr(
        aiwatch,
        "_inject_truststore",
        lambda: (_ for _ in ()).throw(AssertionError("served path imported TLS")),
    )
    monkeypatch.setattr(aiwatch.sys, "stdin", io.StringIO("request"))

    with pytest.raises(SystemExit, match="2"):
        aiwatch._run_hook_daemon_first()

    captured = capsys.readouterr()
    assert captured.out == "out:request"
    assert captured.err == "daemon stderr"


def test_daemon_failure_replays_consumed_stdin_to_inline_hook(
    monkeypatch, capsys
) -> None:
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)
    monkeypatch.setattr(
        daemon_client,
        "try_daemon_hook",
        lambda _stdin, **_kwargs: None,
    )
    monkeypatch.setattr(aiwatch, "_inject_truststore", lambda: None)
    monkeypatch.setattr(aiwatch.sys, "stdin", io.StringIO("request"))

    def run_hook() -> None:
        assert hook_io.is_daemon_fallback()
        hook_io.write_stdout(hook_io.read_stdin())

    monkeypatch.setattr(dispatch, "run_hook", run_hook)

    aiwatch._run_hook_daemon_first()

    assert capsys.readouterr().out == "request"


def test_stdin_read_failure_does_not_replay_partial_stream(monkeypatch) -> None:
    class FlakyStdin:
        def __init__(self) -> None:
            self.reads = 0

        def read(self) -> str:
            self.reads += 1
            if self.reads == 1:
                raise OSError("interrupted mid-read")
            return "truncated-remainder"

    stdin = FlakyStdin()
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)
    monkeypatch.setattr(
        daemon_client,
        "try_daemon_hook",
        lambda *_args, **_kwargs: pytest.fail("daemon called without stdin"),
    )
    monkeypatch.setattr(aiwatch, "_inject_truststore", lambda: None)
    monkeypatch.setattr(aiwatch.sys, "stdin", stdin)

    def run_hook() -> None:
        hook_io.read_stdin()

    monkeypatch.setattr(dispatch, "run_hook", run_hook)

    with pytest.raises(OSError, match="interrupted mid-read"):
        aiwatch._run_hook_daemon_first()

    assert stdin.reads == 1


def test_client_start_ms_prefers_shim_env_over_import_stamp(monkeypatch) -> None:
    monkeypatch.setenv(CLIENT_START_ENV, "1723500000123")

    assert aiwatch._client_start_ms() == 1723500000123


@pytest.mark.parametrize("env_value", [None, "", "not-a-number", "0", "-3"])
def test_client_start_ms_falls_back_to_import_stamp(monkeypatch, env_value) -> None:
    if env_value is None:
        monkeypatch.delenv(CLIENT_START_ENV, raising=False)
    else:
        monkeypatch.setenv(CLIENT_START_ENV, env_value)

    assert aiwatch._client_start_ms() == aiwatch._CLIENT_START_MS


def test_daemon_request_carries_client_start_ms(monkeypatch, capsys) -> None:
    seen: dict[str, int | None] = {}
    monkeypatch.setenv(CLIENT_START_ENV, "1723500000123")
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)

    def fake_try_daemon_hook(stdin, *, client_start_ms=None, _gate_checked=False):
        seen["client_start_ms"] = client_start_ms
        return {"stdout": "", "stderr": "", "exit_code": 0}

    monkeypatch.setattr(daemon_client, "try_daemon_hook", fake_try_daemon_hook)
    monkeypatch.setattr(aiwatch.sys, "stdin", io.StringIO("request"))

    with pytest.raises(SystemExit, match="0"):
        aiwatch._run_hook_daemon_first()

    assert seen["client_start_ms"] == 1723500000123


def test_inline_hook_sees_client_start_ms(monkeypatch) -> None:
    monkeypatch.delenv(CLIENT_START_ENV, raising=False)
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: False)
    monkeypatch.setattr(aiwatch, "_inject_truststore", lambda: None)
    seen: dict[str, int | None] = {}

    def run_hook() -> None:
        seen["client_start_ms"] = hook_io.client_start_ms()

    monkeypatch.setattr(dispatch, "run_hook", run_hook)

    aiwatch._run_hook_daemon_first()

    assert seen["client_start_ms"] == aiwatch._CLIENT_START_MS


@pytest.fixture
def flow_summaries():
    summaries: list[dict] = []
    flow_trace.enable_flow_tracing(summaries.append)
    yield summaries
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


def test_record_startup_ms_reports_elapsed_wall_time(flow_summaries) -> None:
    recent = int(time.time() * 1000) - 25
    with hook_io.scoped(hook_io.HookIO(client_start_ms=recent)):
        with flow_trace.flow("cli.hook_pre_tool"):
            dispatch._record_startup_ms()

    assert 25 <= flow_summaries[0]["startup_ms"] <= 60_000


def test_record_startup_ms_clamps_stale_stamp_to_ceiling(flow_summaries) -> None:
    with hook_io.scoped(hook_io.HookIO(client_start_ms=1)):
        with flow_trace.flow("cli.hook_pre_tool"):
            dispatch._record_startup_ms()

    assert flow_summaries[0]["startup_ms"] == 60_000.0


def test_record_startup_ms_clamps_future_stamp_to_zero(flow_summaries) -> None:
    future = int(time.time() * 1000) + 120_000
    with hook_io.scoped(hook_io.HookIO(client_start_ms=future)):
        with flow_trace.flow("cli.hook_pre_tool"):
            dispatch._record_startup_ms()

    assert flow_summaries[0]["startup_ms"] == 0.0


def test_record_startup_ms_without_stamp_omits_summary_field(flow_summaries) -> None:
    with flow_trace.flow("cli.hook_pre_tool"):
        dispatch._record_startup_ms()

    assert "startup_ms" not in flow_summaries[0]


def test_daemon_subcommand_dispatches_before_typer(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(aiwatch.sys, "argv", ["aiwatch", "daemon"])
    monkeypatch.setattr(
        aiwatch, "_inject_truststore", lambda: calls.append("truststore")
    )
    monkeypatch.setattr(
        aiwatch,
        "_apply_managed_config",
        lambda: calls.append("managed"),
    )
    monkeypatch.setattr(
        command_metrics,
        "run_with_command_metrics",
        lambda command: (calls.append("metrics"), command()),
    )
    monkeypatch.setattr(server, "run_daemon", lambda: calls.append("daemon"))

    aiwatch.main()

    assert calls == ["truststore", "managed", "metrics", "daemon"]


def test_daemon_status_dispatches_without_starting_daemon(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(aiwatch.sys, "argv", ["aiwatch", "daemon", "status"])
    monkeypatch.setattr(
        aiwatch,
        "_inject_truststore",
        lambda: calls.append("truststore"),
    )
    monkeypatch.setattr(
        daemon_status,
        "run_status",
        lambda: calls.append("status") or 0,
    )
    monkeypatch.setattr(
        server,
        "run_daemon",
        lambda: calls.append("daemon"),
    )

    with pytest.raises(SystemExit) as exc_info:
        aiwatch.main()

    assert exc_info.value.code == 0
    assert calls == ["status"]


def test_daemon_help_prints_usage_without_starting_daemon(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(aiwatch.sys, "argv", ["aiwatch", "daemon", "--help"])
    monkeypatch.setattr(
        aiwatch,
        "_inject_truststore",
        lambda: (_ for _ in ()).throw(AssertionError("daemon must not start")),
    )

    with pytest.raises(SystemExit) as exc_info:
        aiwatch.main()

    assert exc_info.value.code == 0
    assert capsys.readouterr().err == "Usage: aiwatch daemon [status]\n"


def test_daemon_unknown_action_exits_without_starting_daemon(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(aiwatch.sys, "argv", ["aiwatch", "daemon", "bogus"])
    monkeypatch.setattr(
        aiwatch,
        "_inject_truststore",
        lambda: (_ for _ in ()).throw(AssertionError("daemon must not start")),
    )

    with pytest.raises(SystemExit) as exc_info:
        aiwatch.main()

    assert exc_info.value.code == 2
    assert capsys.readouterr().err == "Usage: aiwatch daemon [status]\n"


def test_daemon_service_subcommand_dispatches_without_cli_dependencies(
    monkeypatch,
) -> None:
    calls: list[str] = []
    monkeypatch.setattr(aiwatch.sys, "argv", ["aiwatch.exe", "daemon-service"])
    monkeypatch.setattr(
        aiwatch,
        "_inject_truststore",
        lambda: calls.append("truststore"),
    )
    monkeypatch.setattr(
        windows_service,
        "run_service",
        lambda: calls.append("service") or 0,
    )

    aiwatch.main()

    assert calls == ["service"]


def test_daemon_service_failure_becomes_process_exit(monkeypatch) -> None:
    monkeypatch.setattr(aiwatch.sys, "argv", ["aiwatch.exe", "daemon-service"])
    monkeypatch.setattr(windows_service, "run_service", lambda: 1)

    with pytest.raises(SystemExit, match="1"):
        aiwatch.main()
