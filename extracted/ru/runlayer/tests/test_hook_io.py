"""Request-scoped hook IO and relay client reuse."""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from threading import Barrier

import httpx
import pytest

from runlayer_cli import flow_trace
from runlayer_cli.hook import (
    clients,
    copilot_cli_mcp_lookup,
    dispatch,
    hook_io,
    mcp_lookup,
    relay,
)
from runlayer_cli.hook.clients import Client
from runlayer_cli.mdm_config import AIWatchMode


@pytest.fixture(autouse=True)
def _reset_shared_state():
    relay.set_shared_http_client_provider(None)
    relay.set_credential_cache(None)
    relay.set_deferred_event_sender(None)
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()
    yield
    relay.set_shared_http_client_provider(None)
    relay.set_credential_cache(None)
    relay.set_deferred_event_sender(None)
    flow_trace.disable_flow_tracing()
    flow_trace.reset_flow()


def _run_hook(request_io: hook_io.HookIO) -> int | str | None:
    with hook_io.scoped(request_io):
        try:
            dispatch.run_hook()
        except SystemExit as exc:
            return exc.code
    return None


def test_run_hook_in_thread_uses_injected_request_io(monkeypatch):
    stdout = StringIO()
    stderr = StringIO()
    looked_up_from: list[str] = []

    def missing_server(_server_name: str, cwd: str):
        looked_up_from.append(cwd)
        return None

    monkeypatch.setattr(dispatch, "lookup_mcp_server", missing_server)
    monkeypatch.setattr(dispatch, "silence_hook_logging", lambda: None)
    monkeypatch.setattr(dispatch.flow_spool, "spool_append", lambda *_: None)
    monkeypatch.setenv("RUNLAYER_HOOK_CLIENT", "cursor")
    monkeypatch.setenv("HOOK_EVENT_NAME", "UnknownEvent")
    monkeypatch.setattr(sys, "stdin", StringIO("not request input"))
    monkeypatch.setattr(sys, "argv", ["aiwatch", "--mode", "monitor"])

    request_io = hook_io.HookIO(
        stdin_text=json.dumps(
            {
                "tool_name": "mcp__missing__search",
                "tool_input": {"query": "test"},
            }
        ),
        stdout=stdout,
        stderr=stderr,
        env={
            "RUNLAYER_HOOK_CLIENT": "claude_code",
            "HOOK_EVENT_NAME": "PreToolUse",
        },
        cwd="/request/workspace",
        argv=["aiwatch", "--mode", "enforce"],
    )

    with ThreadPoolExecutor(max_workers=1) as executor:
        exit_code = executor.submit(_run_hook, request_io).result()

    response = json.loads(stdout.getvalue())
    assert exit_code == 0
    assert stderr.getvalue() == ""
    assert looked_up_from == ["/request/workspace"]
    assert response["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
    assert response["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_consumed_stdin_failure_denies_without_rereading_stream(monkeypatch):
    stdout = StringIO()
    stderr = StringIO()

    class UnreadableStdin:
        def read(self) -> str:
            raise AssertionError("hook re-read an already consumed stdin stream")

    monkeypatch.setattr(dispatch, "silence_hook_logging", lambda: None)
    monkeypatch.setattr(dispatch.flow_spool, "spool_append", lambda *_: None)
    monkeypatch.setattr(sys, "stdin", UnreadableStdin())

    request_io = hook_io.HookIO(
        stdin_error=OSError("interrupted mid-read"),
        stdout=stdout,
        stderr=stderr,
        env={
            "RUNLAYER_HOOK_CLIENT": "claude_code",
            "HOOK_EVENT_NAME": "PreToolUse",
        },
        argv=["aiwatch", "--mode", "enforce"],
    )

    exit_code = _run_hook(request_io)

    response = json.loads(stdout.getvalue())
    assert exit_code == 0
    assert response["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_concurrent_run_hook_contexts_do_not_cross_contaminate(monkeypatch):
    rendezvous = Barrier(2)
    monkeypatch.setattr(dispatch, "silence_hook_logging", lambda: None)
    monkeypatch.setattr(dispatch.flow_spool, "spool_append", lambda *_: None)
    monkeypatch.setattr(dispatch, "forward_event", lambda *_, **__: None)
    monkeypatch.setattr(
        dispatch,
        "forward_tool_lifecycle",
        lambda *_, **__: rendezvous.wait(timeout=5),
    )
    monkeypatch.setenv("RUNLAYER_HOOK_CLIENT", "claude_code")
    monkeypatch.setenv("HOOK_EVENT_NAME", "UnknownEvent")

    cursor_stdout = StringIO()
    cursor_stderr = StringIO()
    hermes_stdout = StringIO()
    hermes_stderr = StringIO()
    payload = json.dumps(
        {
            "tool_name": "Read",
            "tool_input": {"file_path": "README.md"},
        }
    )
    cursor_io = hook_io.HookIO(
        stdin_text=payload,
        stdout=cursor_stdout,
        stderr=cursor_stderr,
        env={
            "RUNLAYER_HOOK_CLIENT": "cursor",
            "HOOK_EVENT_NAME": "PreToolUse",
        },
        argv=["aiwatch", "--mode", "monitor"],
    )
    hermes_io = hook_io.HookIO(
        stdin_text=payload,
        stdout=hermes_stdout,
        stderr=hermes_stderr,
        env={
            "RUNLAYER_HOOK_CLIENT": "hermes",
            "HOOK_EVENT_NAME": "preToolUse",
        },
        argv=["aiwatch", "--mode", "monitor"],
    )

    with ThreadPoolExecutor(max_workers=2) as executor:
        cursor_result = executor.submit(_run_hook, cursor_io)
        hermes_result = executor.submit(_run_hook, hermes_io)
        assert cursor_result.result() is None
        assert hermes_result.result() is None

    assert cursor_stdout.getvalue() == '{"permission":"allow"}'
    assert hermes_stdout.getvalue() == "{}"
    assert cursor_stderr.getvalue() == ""
    assert hermes_stderr.getvalue() == ""


def test_hook_io_falls_through_to_process_defaults(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", StringIO("process stdin"))
    monkeypatch.setattr(sys, "argv", ["process", "--flag"])
    monkeypatch.setattr(hook_io.os, "getcwd", lambda: "/process/cwd")
    monkeypatch.setenv("PROCESS_ONLY", "process value")

    assert hook_io.read_stdin() == "process stdin"
    assert hook_io.getenv("PROCESS_ONLY") == "process value"
    assert hook_io.getcwd() == "/process/cwd"
    assert hook_io.argv() == ["process", "--flag"]
    hook_io.write_stdout("process stdout")
    hook_io.write_stderr("process stderr")

    captured = capsys.readouterr()
    assert captured.out == "process stdout"
    assert captured.err == "process stderr"

    stdout = StringIO()
    stderr = StringIO()
    with hook_io.scoped(
        hook_io.HookIO(
            stdin_text="request stdin",
            stdout=stdout,
            stderr=stderr,
            env={"REQUEST_ONLY": "request value"},
            cwd="/request/cwd",
            argv=["request", "--other"],
        )
    ):
        assert hook_io.read_stdin() == "request stdin"
        assert hook_io.getenv("REQUEST_ONLY") == "request value"
        assert hook_io.getenv("PROCESS_ONLY") == "process value"
        assert hook_io.getcwd() == "/request/cwd"
        assert hook_io.argv() == ["request", "--other"]
        hook_io.write_stdout("request stdout")
        hook_io.write_stderr("request stderr")

    assert stdout.getvalue() == "request stdout"
    assert stderr.getvalue() == "request stderr"


def test_abspath_anchors_relative_paths_at_request_cwd(monkeypatch):
    monkeypatch.setattr(hook_io.os, "getcwd", lambda: "/process/cwd")

    assert hook_io.abspath("hooks/aiwatch") == "/process/cwd/hooks/aiwatch"
    assert hook_io.abspath("/absolute/aiwatch") == "/absolute/aiwatch"

    with hook_io.scoped(hook_io.HookIO(cwd="/request/cwd")):
        assert hook_io.abspath("hooks/aiwatch") == "/request/cwd/hooks/aiwatch"
        assert hook_io.abspath("/absolute/aiwatch") == "/absolute/aiwatch"


def test_client_detection_anchors_relative_argv0_at_request_cwd(monkeypatch, tmp_path):
    monkeypatch.delenv("RUNLAYER_HOOK_CLIENT", raising=False)
    monkeypatch.delenv("CURSOR_VERSION", raising=False)
    hook_dir = tmp_path / ".cursor" / "hooks"
    hook_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)

    with hook_io.scoped(hook_io.HookIO(cwd=str(hook_dir), argv=["aiwatch"])):
        assert clients.detect_client() is Client.CURSOR
        assert clients.should_noop_for_cursor(Client.CURSOR) is False


def test_env_relocated_hook_home_anchors_at_request_cwd(monkeypatch, tmp_path):
    """A relative ``COPILOT_HOME`` is relative to the request cwd, not the daemon's."""
    monkeypatch.delenv("RUNLAYER_HOOK_CLIENT", raising=False)
    monkeypatch.delenv("CURSOR_VERSION", raising=False)
    project = tmp_path / "project"
    project.mkdir()
    hook_dir = tmp_path / "copilot-home" / "hooks"
    hook_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)

    with hook_io.scoped(
        hook_io.HookIO(
            cwd=str(project),
            argv=[str(hook_dir / "aiwatch")],
            env={"COPILOT_HOME": "../copilot-home"},
        )
    ):
        assert clients.detect_client() is Client.GITHUB_COPILOT_CLI


def test_resolve_mode_reads_config_beside_request_relative_argv0(monkeypatch, tmp_path):
    config_dir = tmp_path / "hooks"
    config_dir.mkdir()
    (config_dir / "runlayer-config.json").write_text(
        json.dumps({"enforcement": False}), encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)

    with hook_io.scoped(hook_io.HookIO(cwd=str(config_dir), argv=["aiwatch"])):
        assert dispatch._resolve_mode() is AIWatchMode.MONITOR


def test_copilot_mcp_lookup_uses_request_cwd_when_payload_omits_cwd(
    monkeypatch, tmp_path
):
    project = tmp_path / "project"
    project.mkdir()
    (project / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"acme": {"command": "acme-server"}}}),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    with hook_io.scoped(hook_io.HookIO(cwd=str(project))):
        resolved = (
            copilot_cli_mcp_lookup.resolve_github_copilot_cli_mcp_source_from_payload(
                "acme-search",
                {"tool_name": "acme-search", "tool_input": {}},
                home_path=tmp_path / "home",
            )
        )

    assert resolved is not None
    assert resolved[0] == "acme"
    assert resolved[1] == {"command": "acme-server"}


def test_copilot_mcp_lookup_honors_request_env_copilot_home(monkeypatch, tmp_path):
    monkeypatch.delenv("COPILOT_HOME", raising=False)
    copilot_home = tmp_path / "copilot-home"
    copilot_home.mkdir()
    (copilot_home / "mcp-config.json").write_text(
        json.dumps({"mcpServers": {"acme": {"command": "acme-server"}}}),
        encoding="utf-8",
    )
    project = tmp_path / "project"
    project.mkdir()

    with hook_io.scoped(
        hook_io.HookIO(cwd=str(project), env={"COPILOT_HOME": str(copilot_home)})
    ):
        server = copilot_cli_mcp_lookup.lookup_github_copilot_cli_mcp_server(
            "acme",
            str(project),
            home_path=tmp_path / "home",
        )
        plugins_base = (
            copilot_cli_mcp_lookup._github_copilot_cli_installed_plugins_base(
                tmp_path / "home"
            )
        )

    assert server == {"command": "acme-server"}
    assert plugins_base == copilot_home / "installed-plugins"


def test_relative_copilot_home_anchors_at_request_cwd(monkeypatch, tmp_path):
    """A relative ``COPILOT_HOME`` resolves against the request cwd, not the daemon's."""
    monkeypatch.delenv("COPILOT_HOME", raising=False)
    copilot_home = tmp_path / "copilot-home"
    copilot_home.mkdir()
    (copilot_home / "mcp-config.json").write_text(
        json.dumps({"mcpServers": {"acme": {"command": "acme-server"}}}),
        encoding="utf-8",
    )
    project = tmp_path / "project"
    project.mkdir()
    daemon_cwd = tmp_path / "daemon-cwd"
    daemon_cwd.mkdir()
    monkeypatch.chdir(daemon_cwd)

    with hook_io.scoped(
        hook_io.HookIO(cwd=str(project), env={"COPILOT_HOME": "../copilot-home"})
    ):
        server = copilot_cli_mcp_lookup.lookup_github_copilot_cli_mcp_server(
            "acme",
            str(project),
            home_path=tmp_path / "home",
        )
        plugins_base = (
            copilot_cli_mcp_lookup._github_copilot_cli_installed_plugins_base(
                tmp_path / "home"
            )
        )

    assert server == {"command": "acme-server"}
    assert plugins_base == copilot_home / "installed-plugins"


def test_copilot_session_mcp_config_honors_request_env(monkeypatch):
    for (
        env_var
    ) in copilot_cli_mcp_lookup._GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG_ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)

    request_env = {
        "COPILOT_ADDITIONAL_MCP_CONFIG": json.dumps(
            {"mcpServers": {"acme": {"command": "acme-server"}}}
        )
    }
    with hook_io.scoped(hook_io.HookIO(env=request_env)):
        assert (
            copilot_cli_mcp_lookup.github_copilot_cli_has_session_mcp_config() is True
        )
        resolved = copilot_cli_mcp_lookup.resolve_github_copilot_cli_mcp_tool(
            "acme-search",
            "/project",
        )

    assert resolved == ("acme", {"command": "acme-server"})


def test_cline_mcp_settings_honor_request_env_cline_dir(monkeypatch, tmp_path):
    monkeypatch.delenv("CLINE_DIR", raising=False)
    cline_dir = tmp_path / "cline"
    settings_dir = cline_dir / "data" / "settings"
    settings_dir.mkdir(parents=True)
    (settings_dir / "cline_mcp_settings.json").write_text(
        json.dumps({"mcpServers": {"acme": {"command": "acme-server"}}}),
        encoding="utf-8",
    )

    with hook_io.scoped(hook_io.HookIO(env={"CLINE_DIR": str(cline_dir)})):
        resolved = mcp_lookup.resolve_cline_cli_mcp_tool("acme__search")

    assert resolved == ("acme", {"command": "acme-server"})


def test_relative_cline_dir_anchors_at_request_cwd(monkeypatch, tmp_path):
    monkeypatch.delenv("CLINE_DIR", raising=False)
    cline_dir = tmp_path / "cline"
    settings_dir = cline_dir / "data" / "settings"
    settings_dir.mkdir(parents=True)
    (settings_dir / "cline_mcp_settings.json").write_text(
        json.dumps({"mcpServers": {"acme": {"command": "acme-server"}}}),
        encoding="utf-8",
    )
    daemon_cwd = tmp_path / "daemon-cwd"
    daemon_cwd.mkdir()
    monkeypatch.chdir(daemon_cwd)

    with hook_io.scoped(hook_io.HookIO(cwd=str(tmp_path), env={"CLINE_DIR": "cline"})):
        resolved = mcp_lookup.resolve_cline_cli_mcp_tool("acme__search")

    assert resolved == ("acme", {"command": "acme-server"})


def test_windows_mcp_config_paths_honor_request_env(monkeypatch):
    monkeypatch.setenv("APPDATA", r"C:\process\AppData")
    monkeypatch.setenv("PROGRAMFILES", r"C:\Process Files")
    monkeypatch.setattr(mcp_lookup.platform, "system", lambda: "Windows")

    with hook_io.scoped(
        hook_io.HookIO(
            env={
                "APPDATA": r"C:\request\AppData",
                "PROGRAMFILES": r"C:\Request Files",
            }
        )
    ):
        vscode_paths = mcp_lookup._vscode_mcp_config_paths("/project")
        goose_paths = mcp_lookup._goose_mcp_config_paths()
        managed_path = mcp_lookup._claude_managed_mcp_config_path()

    assert any(r"C:\request\AppData" in str(path) for path in vscode_paths)
    assert any(r"C:\request\AppData" in str(path) for path in goose_paths)
    assert r"C:\Request Files" in str(managed_path)


def test_shared_http_client_provider_reuses_non_closing_client(monkeypatch):
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, text='{"ok":true}')

    client = httpx.Client(transport=httpx.MockTransport(handle))
    provided: list[httpx.Client] = []

    def provide() -> httpx.Client:
        provided.append(client)
        return client

    monkeypatch.setattr(relay, "_maybe_attach_device", lambda payload: payload)
    relay.set_shared_http_client_provider(provide)
    try:
        relay._post(
            "https://api.example.com",
            "rl_user_test",
            "{}",
            target="enforce",
        )
        relay._post(
            "https://api.example.com",
            "rl_user_test",
            "{}",
            target="enforce",
        )

        assert len(requests) == 2
        assert provided == [client, client]
        assert not client.is_closed
    finally:
        client.close()


def test_default_relay_path_constructs_client_per_post(monkeypatch):
    clients: list[httpx.Client] = []
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(200, text='{"ok":true}')
    )

    def make_client(**_kwargs) -> httpx.Client:
        client = httpx.Client(transport=transport)
        clients.append(client)
        return client

    monkeypatch.setattr(relay, "_maybe_attach_device", lambda payload: payload)
    monkeypatch.setattr(relay, "http_client", make_client)

    relay._post(
        "https://api.example.com",
        "rl_user_test",
        "{}",
        target="enforce",
    )
    relay._post(
        "https://api.example.com",
        "rl_user_test",
        "{}",
        target="enforce",
    )

    assert len(clients) == 2
    assert clients[0] is not clients[1]
    assert all(client.is_closed for client in clients)
