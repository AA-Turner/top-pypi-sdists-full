import os
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Keep these tests independent of a developer's local .env. Importing main loads
# .env, and OAuth 2.1 mode changes tool schemas at decoration time.
os.environ["MCP_ENABLE_OAUTH21"] = "false"
os.environ["WORKSPACE_MCP_STATELESS_MODE"] = "false"

import main
import core.server as server_module

TERMINAL = SimpleNamespace(isatty=lambda: True)
PIPE = SimpleNamespace(isatty=lambda: False)


@pytest.mark.parametrize("stdin", [TERMINAL, PIPE, None])
def test_resolve_transport_flag_wins(monkeypatch, stdin):
    monkeypatch.setenv("WORKSPACE_MCP_TRANSPORT", "streamable-http")
    monkeypatch.setattr(sys, "stdin", stdin)

    assert main.resolve_transport("stdio") == ("stdio", "flag")


def test_resolve_transport_env_beats_terminal(monkeypatch):
    monkeypatch.setenv("WORKSPACE_MCP_TRANSPORT", " STDIO ")
    monkeypatch.setattr(sys, "stdin", TERMINAL)

    assert main.resolve_transport(None) == ("stdio", "env")


def test_resolve_transport_rejects_invalid_env(monkeypatch, capsys):
    monkeypatch.setenv("WORKSPACE_MCP_TRANSPORT", "sse")

    with pytest.raises(SystemExit) as exc:
        main.resolve_transport(None)

    assert exc.value.code == 1
    assert "invalid WORKSPACE_MCP_TRANSPORT 'sse'" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("stdin", "expected"),
    [
        (TERMINAL, ("streamable-http", "terminal")),
        (PIPE, ("stdio", "client")),
        (None, ("stdio", "client")),
    ],
)
def test_resolve_transport_detects_launch_context(monkeypatch, stdin, expected):
    monkeypatch.delenv("WORKSPACE_MCP_TRANSPORT", raising=False)
    monkeypatch.setattr(sys, "stdin", stdin)

    assert main.resolve_transport(None) == expected


@pytest.fixture
def oauth21_calls(monkeypatch):
    """Unset the OAuth 2.1 flag and record the config side effects instead of running them."""
    calls = []
    monkeypatch.delenv("MCP_ENABLE_OAUTH21", raising=False)
    monkeypatch.delenv("MCP_SINGLE_USER_MODE", raising=False)
    monkeypatch.setattr(main, "is_service_account_enabled", lambda: False)
    monkeypatch.setattr(main, "is_trust_gateway_identity", lambda: False)
    monkeypatch.setattr(main, "reload_oauth_config", lambda: calls.append("reload"))
    monkeypatch.setattr(
        main, "refresh_server_instructions", lambda: calls.append("instructions")
    )
    return calls


def test_oauth21_defaults_on_for_streamable_http(oauth21_calls):
    assert main.resolve_oauth21_default("streamable-http", single_user=False)
    assert os.environ["MCP_ENABLE_OAUTH21"] == "true"
    assert oauth21_calls == ["reload", "instructions"]


def test_oauth21_default_leaves_stdio_alone(oauth21_calls):
    assert not main.resolve_oauth21_default("stdio", single_user=False)
    assert "MCP_ENABLE_OAUTH21" not in os.environ
    assert oauth21_calls == []


@pytest.mark.parametrize("value", ["false", "0", "true"])
def test_oauth21_default_respects_explicit_value(monkeypatch, oauth21_calls, value):
    monkeypatch.setenv("MCP_ENABLE_OAUTH21", value)

    assert not main.resolve_oauth21_default("streamable-http", single_user=False)
    assert os.environ["MCP_ENABLE_OAUTH21"] == value
    assert oauth21_calls == []


@pytest.mark.parametrize(
    ("single_user", "env", "service_account", "gateway"),
    [
        (True, {}, False, False),
        (False, {"MCP_SINGLE_USER_MODE": "1"}, False, False),
        (False, {}, True, False),
        (False, {}, False, True),
    ],
    ids=["single-user-flag", "single-user-env", "service-account", "trusted-gateway"],
)
def test_oauth21_default_skips_incompatible_modes(
    monkeypatch, oauth21_calls, single_user, env, service_account, gateway
):
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(main, "is_service_account_enabled", lambda: service_account)
    monkeypatch.setattr(main, "is_trust_gateway_identity", lambda: gateway)

    assert not main.resolve_oauth21_default("streamable-http", single_user)
    assert "MCP_ENABLE_OAUTH21" not in os.environ
    assert oauth21_calls == []


def test_server_instructions_drop_default_account_under_oauth21(monkeypatch):
    monkeypatch.setattr(server_module, "USER_GOOGLE_EMAIL", "user@example.com")
    monkeypatch.setattr(server_module, "is_trust_gateway_identity", lambda: False)
    monkeypatch.setattr(server_module, "is_oauth21_enabled", lambda: False)
    assert "user@example.com" in server_module.build_server_instructions()

    monkeypatch.setattr(server_module, "is_oauth21_enabled", lambda: True)
    monkeypatch.setattr(server_module.server, "instructions", "stale")
    server_module.refresh_server_instructions()

    assert server_module.build_server_instructions() is None
    assert server_module.server.instructions is None
