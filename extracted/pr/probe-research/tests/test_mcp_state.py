"""One honest MCP answer per coding agent (`Capabilities.mcp_state`).

"MCP on" used to mean "plugin installed and CLI signed in": a daemon profile
that carries no MCP read as on, Kimi's un-logged-in OAuth MCP read as on, and
pi always read as off. The state now comes from each agent's registry row
(`mcp` kind -> one credential resolver), so a new harness gets it by declaring
its row, and this file fails when a kind has no resolver.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import capabilities as caps_mod
from probe.cli import kimi_config, pi_config
from probe.cli.capabilities import (
    DAEMON_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
    Capabilities,
    McpCheck,
    McpCredential,
    McpState,
)
from probe.harness import get_registry
from probe.harness import registry as reg


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))
    monkeypatch.setenv("KIMI_CODE_HOME", str(tmp_path / "kimi"))
    for name in ("PROBE_MCP_TOKEN", "PROBE_AGENT", "CLAUDECODE", "CODEX_THREAD_ID"):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / "home").mkdir()
    monkeypatch.chdir(tmp_path / "home")
    # The process-wide token verdict never leaks between tests.
    monkeypatch.setattr(caps_mod, "_MCP_TOKEN_VERDICT", None)
    return tmp_path


def _config_token(isolate, token: str | None) -> None:
    path = isolate / "probe" / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    ctx = {"base_url": "https://api.research.prbe.ai"}
    if token:
        ctx["mcp_token"] = token
    path.write_text(json.dumps({"current_context": "default", "contexts": {"default": ctx}}))


def test_every_registry_mcp_kind_has_a_resolver():
    kinds = {h.mcp for h in get_registry().all() if h.mcp is not None}
    assert kinds <= set(caps_mod.MCP_RESOLVERS), kinds - set(caps_mod.MCP_RESOLVERS)
    assert set(reg.MCP_KINDS) == set(caps_mod.MCP_RESOLVERS)


def test_a_registry_row_naming_an_unknown_mcp_kind_is_refused():
    doc = json.loads((Path(reg.__file__).parent / "harnesses.json").read_text())
    rows = doc["harnesses"] if isinstance(doc, dict) else doc
    bad = dict(rows[1], id="smoke_agent", mcp="smoke-signals")
    with pytest.raises(reg.RegistryError):
        reg.load(extra=[bad])


def _caps(**kw) -> Capabilities:
    base = dict(agent_source="claude_code", mcp_kind=reg.MCP_PLUGIN_FILE, tracking_plugin_installed=True,
                logged_in_as="a@b.c", mcp_check=McpCheck(McpCredential.PRESENT))
    base.update(kw)
    return Capabilities(**base)


@pytest.mark.parametrize(
    ("kw", "state", "words"),
    [
        ({}, McpState.ON, "on"),
        ({"mcp_kind": None}, McpState.NOT_OFFERED, "not offered for this agent"),
        ({"tracking_plugin_installed": False}, McpState.NOT_INSTALLED, "off: not installed"),
        ({"tracking_plugin_installed": False, "plugins_verified": False}, McpState.UNKNOWN,
         "unknown: the agent's plugin list could not be read"),
        ({"mcp_check": McpCheck(McpCredential.MISSING)}, McpState.LOGIN_NEEDED,
         "login needed: run `probe wizard`"),
        ({"mcp_check": McpCheck(McpCredential.REJECTED)}, McpState.LOGIN_NEEDED,
         "login needed: token rejected; run `probe wizard`"),
        ({"mcp_check": McpCheck(McpCredential.UNKNOWN, what="x unreadable")}, McpState.UNKNOWN, "unknown: x unreadable"),
        # MCP is about MCP: no CLI sign-in does not make a working MCP "off".
        ({"logged_in_as": None}, McpState.ON, "on"),
    ],
)
def test_state_precedence_and_words(kw, state, words):
    caps = _caps(**kw)
    assert caps.mcp_state == state
    assert caps.mcp_status() == words


def test_the_daemon_profile_reads_as_the_daemon_not_as_on(monkeypatch):
    """The daemon plugin carries no MCP; it read "MCP on" before."""
    monkeypatch.setattr(caps_mod, "tracking_plugin_name", lambda source=None: DAEMON_PLUGIN_NAME)
    caps = _caps(mcp_check=McpCheck(McpCredential.MISSING))
    assert caps.mcp_state == McpState.DAEMON
    assert caps.mcp_status() == "off: the daemon reads for this agent"
    monkeypatch.setattr(caps_mod, "tracking_plugin_name", lambda source=None: TRACKING_PLUGIN_NAME)
    assert caps.mcp_state == McpState.LOGIN_NEEDED


def test_pi_is_never_unknown_for_an_absent_entry():
    """pi's plugin answer is a settings read (verified=False by design)."""
    caps = _caps(agent_source="pi", mcp_kind=reg.MCP_EXTENSION_BRIDGE, tracking_plugin_installed=False,
                 plugins_verified=False)
    assert caps.mcp_state == McpState.NOT_INSTALLED


def test_the_cli_token_resolves_env_first_like_the_helper(isolate, monkeypatch):
    _config_token(isolate, "from-config")
    assert caps_mod.cli_mcp_token() == "from-config"
    monkeypatch.setenv("PROBE_MCP_TOKEN", "from-env")
    assert caps_mod.cli_mcp_token() == "from-env"
    helper = (Path(caps_mod.__file__).parents[3] / "plugins" / "probe-research" / "bin" / "probe-mcp-headers").read_text()
    assert helper.index("PROBE_MCP_TOKEN") < helper.index("mcp_token")


@pytest.mark.parametrize("token", [None, "tok"])
def test_claude_code_needs_the_read_token(isolate, token):
    _config_token(isolate, token)
    kind, check = caps_mod.check_mcp("claude_code")
    assert kind == reg.MCP_PLUGIN_FILE
    assert check.credential == (McpCredential.PRESENT if token else McpCredential.MISSING)


@pytest.mark.parametrize(("auth", "expected"), [(True, McpCredential.PRESENT), (False, McpCredential.MISSING),
                                                 (None, McpCredential.UNKNOWN)])
def test_codex_reuses_its_mcp_list_answer(auth, expected):
    assert caps_mod.check_mcp("codex", codex_auth=auth)[1].credential == expected


def test_pi_names_pi_mcp_adapter_when_it_serves_the_mcp(isolate):
    _config_token(isolate, "tok")
    assert caps_mod.check_mcp("pi")[1].credential == McpCredential.PRESENT
    settings = isolate / "pi-agent" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(json.dumps({"packages": ["npm:pi-mcp-adapter@1.2.3", pi_config.MIRROR_GIT_SOURCE]}))
    check = caps_mod.check_mcp("pi")[1]
    assert check.credential == McpCredential.UNKNOWN
    assert "pi-mcp-adapter" in check.what


@pytest.mark.parametrize("source", ["npm:pi-mcp-adapter", "git:github.com/x/pi-mcp-adapter.git#main",
                                    "https://github.com/x/pi-mcp-adapter"])
def test_adapter_detection_matches_the_extensions_identity(isolate, source):
    settings = isolate / "pi-agent" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(json.dumps({"packages": [source]}))
    assert pi_config.mcp_adapter_installed() is True


def _kimi_record(isolate, header: str | None) -> None:
    root = isolate / "kimi" / "plugins" / "managed" / "probe-research@9.9.9"
    (root / ".kimi-plugin").mkdir(parents=True)
    server = {"url": "https://mcp.research.prbe.ai/mcp"}
    if header is None:
        server["auth"] = "oauth"
    else:
        server["headers"] = {"Authorization": header}
    (root / ".kimi-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research", "mcpServers": {"probe-research": server}}))
    (isolate / "kimi" / "plugins" / "installed.json").write_text(json.dumps(
        {"version": 1, "plugins": [{"id": "probe-research", "root": str(root), "source": "local-path", "enabled": True}]}))


@pytest.mark.parametrize(
    ("header", "expected"),
    [("Bearer tok", McpCredential.PRESENT), ("Bearer old", McpCredential.MISSING), (None, McpCredential.MISSING)],
)
def test_kimi_needs_the_held_token_in_its_installed_manifest(isolate, header, expected):
    _config_token(isolate, "tok")
    _kimi_record(isolate, header)
    assert caps_mod.check_mcp("kimi_code")[1].credential == expected


def test_an_unreadable_kimi_record_is_unknown_never_on(isolate):
    _config_token(isolate, "tok")
    check = caps_mod.check_mcp("kimi_code")[1]
    assert check.credential == McpCredential.UNKNOWN and check.what
    assert kimi_config.MCP_SERVER_KEY == "probe-research"


def test_cursor_is_not_offered():
    assert caps_mod.check_mcp("cursor") == (None, None)


# --- a token the API refuses (plan T4) --------------------------------------


@pytest.fixture()
def refused(isolate, monkeypatch):
    _config_token(isolate, "tok")
    import importlib

    cli_main = importlib.import_module("probe.cli.main")

    monkeypatch.setattr(cli_main, "_verify", lambda token, base_url: ("rejected", None))
    assert caps_mod.refresh_mcp_token_verdict() == "rejected"
    return None


def test_a_refused_token_reads_login_needed_and_names_the_reason(refused):
    check = caps_mod.check_mcp("claude_code")[1]
    assert check.credential == McpCredential.REJECTED
    assert _caps(mcp_check=check).mcp_status() == "login needed: token rejected; run `probe wizard`"


def test_codex_on_its_own_oauth_login_is_not_the_refused_token(refused, monkeypatch):
    from probe.cli import codex_config

    monkeypatch.setattr(codex_config, "configured_bearer", lambda name: None)
    assert caps_mod.check_mcp("codex", codex_auth=True)[1].credential == McpCredential.PRESENT
    monkeypatch.setattr(codex_config, "configured_bearer", lambda name: "tok")
    assert caps_mod.check_mcp("codex", codex_auth=True)[1].credential == McpCredential.REJECTED


def test_the_wizard_re_authorizes_a_refused_token(refused):
    """Presence used to count as held, so `probe wizard` was a no-op."""
    from probe.cli import setup as wizard

    caps = _caps(mcp_token_held=True)
    selection = wizard.Selection(tracking=True, capture=False, auto_update=False, agent_rules=False)
    assert "mcp" in wizard.needs_authorization(caps, selection)


def test_a_rotated_token_is_not_still_refused(refused, isolate):
    _config_token(isolate, "new-tok")
    assert caps_mod.mcp_token_rejected() is False


def test_no_token_asks_nothing(isolate, monkeypatch):
    import importlib

    cli_main = importlib.import_module("probe.cli.main")

    monkeypatch.setattr(cli_main, "_verify", lambda *a: pytest.fail("asked the API with no token"))
    assert caps_mod.refresh_mcp_token_verdict() is None


# --- what the screens print (plan T6) ---------------------------------------


def test_the_wizard_header_prints_each_agents_mcp_answer(monkeypatch):
    from probe.cli import setup as wizard

    monkeypatch.setattr(caps_mod, "tracking_plugin_name", lambda source=None: TRACKING_PLUGIN_NAME)
    lines = wizard.describe_state({
        "claude_code": _caps(),
        "kimi_code": _caps(agent_source="kimi_code", mcp_kind=reg.MCP_PLUGIN_MANIFEST,
                           mcp_check=McpCheck(McpCredential.MISSING)),
        "pi": _caps(agent_source="pi", mcp_kind=reg.MCP_EXTENSION_BRIDGE, tracking_plugin_installed=False),
        "cursor": _caps(agent_source="cursor", mcp_kind=None),
    })
    text = "\n".join(lines)
    assert "MCP on " in text
    assert "MCP login needed " in text
    assert "MCP not installed " in text
    assert "MCP not offered " in text


def test_the_wizard_header_shows_only_installed_agents(monkeypatch):
    """Richard 2026-10-05: "only show the harness if its actually detected as
    installed on the device"."""
    from probe.cli import setup as wizard

    monkeypatch.setattr(caps_mod, "tracking_plugin_name", lambda source=None: TRACKING_PLUGIN_NAME)
    caps = {"claude_code": _caps(), "pi": _caps(agent_source="pi", mcp_kind=reg.MCP_EXTENSION_BRIDGE)}
    lines = wizard.describe_state(caps, installed=("claude_code",))
    assert lines[0].strip().startswith("Claude Code") and lines[1] == ""
    none = wizard.describe_state(caps, installed=())
    assert "none found on this device" in none[0]
    assert any("Account" in line for line in none), "device rows stay without agents"


def test_every_installable_agent_has_a_logo():
    from probe.cli import setup as wizard

    for harness in get_registry().installable():
        logo = wizard.agent_logo(harness.id)
        assert logo and logo.startswith(b"\x89PNG"), harness.id
    assert set(wizard._MCP_WORDS) == set(McpState)


def test_a_terminal_that_draws_images_gets_logos_and_hover_names(monkeypatch):
    """Richard 2026-10-06: the real logos, and the name on hover. Kitty replies
    are switched off (q=2): a reply lands on stdin, where the menu reads keys."""
    from probe.cli import setup as wizard
    from probe.cli import tui

    monkeypatch.setattr(caps_mod, "tracking_plugin_name", lambda source=None: TRACKING_PLUGIN_NAME)
    caps = {"claude_code": _caps(), "codex": _caps(agent_source="codex")}
    rows = wizard.describe_state(caps, images=tui.ImageProtocol.KITTY)[:2]
    assert [row.hover for row in rows] == ["Claude Code", "Codex"]
    assert not any("Claude Code" in row or "Codex" in row for row in rows), "the logo replaces the name"
    for row in rows:
        (column, escape), = row.escapes
        assert escape.startswith("\x1b7") and escape.endswith("\x1b8") and "q=2" in escape



def test_doctor_prints_the_mcp_answer(monkeypatch):
    from probe.cli import doctor

    monkeypatch.setattr(caps_mod, "tracking_plugin_name", lambda source=None: DAEMON_PLUGIN_NAME)
    text = doctor.render(_caps())
    assert "off: the daemon reads for this agent" in text



@pytest.mark.parametrize("verdict", ["ok", "unreachable"])
def test_only_a_refusal_re_authorizes(isolate, monkeypatch, verdict):
    """An unreachable API is not a refused token: no browser approval for it."""
    import importlib

    from probe.cli import setup as wizard

    _config_token(isolate, "tok")
    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(cli_main, "_verify", lambda token, base_url: (verdict, None))
    assert caps_mod.refresh_mcp_token_verdict() == verdict
    selection = wizard.Selection(tracking=True, capture=False, auto_update=False, agent_rules=False)
    assert "mcp" not in wizard.needs_authorization(_caps(mcp_token_held=True), selection)
    assert caps_mod.check_mcp("claude_code")[1].credential == McpCredential.PRESENT


def test_a_codex_bearer_the_device_has_replaced_is_a_login_needed(monkeypatch):
    """`codex mcp list` answers bearer_token for a dead header too."""
    from probe.cli import setup as wizard

    monkeypatch.setattr(wizard, "codex_mcp_token_drifted", lambda: True)
    assert caps_mod.check_mcp("codex", codex_auth=True)[1].credential == McpCredential.MISSING


def test_pi_with_its_extension_filtered_out_is_not_on(isolate):
    _config_token(isolate, "tok")
    settings = isolate / "pi-agent" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(json.dumps({"packages": [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": []}]}))
    check = caps_mod.check_mcp("pi")[1]
    assert check.credential == McpCredential.UNKNOWN and "extension" in check.what


@pytest.mark.parametrize("source", ["npm:@x/pi-mcp-adapter", "npm:pi-mcp-adapter-fork", "git:github.com/x/other.git"])
def test_adapter_look_alikes_are_not_the_adapter(isolate, source):
    settings = isolate / "pi-agent" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(json.dumps({"packages": [source]}))
    assert pi_config.mcp_adapter_installed() is False


def test_the_adapter_counts_in_the_project_scope_and_as_a_local_path(isolate):
    local = isolate / "adapter-checkout"
    local.mkdir()
    (local / "package.json").write_text(json.dumps({"name": "pi-mcp-adapter"}))
    project = isolate / "home" / ".pi" / "settings.json"
    project.parent.mkdir(parents=True)
    project.write_text(json.dumps({"packages": [str(local)]}))
    assert pi_config.mcp_adapter_installed() is False  # global only
    assert pi_config.mcp_adapter_installed(cwd=isolate / "home") is True


def test_kimi_on_another_deployment_never_gets_the_token(isolate):
    """A self-hosted device's read token must not be sent to the hosted MCP."""
    path = isolate / "probe" / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"current_context": "default", "contexts": {"default": {
        "base_url": "https://probe.selfhosted.example", "mcp_token": "tok"}}}))
    _kimi_record(isolate, None)
    root = next((isolate / "kimi" / "plugins" / "managed").glob("probe-research@*"))
    server = json.loads((root / ".kimi-plugin" / "plugin.json").read_text())["mcpServers"]["probe-research"]
    server["url"] = "https://mcp.research.prbe.ai/mcp"
    (root / ".kimi-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research", "mcpServers": {"probe-research": server}}))
    assert kimi_config.write_mcp_bearer(root, "tok") is False
    assert "headers" not in json.loads((root / ".kimi-plugin" / "plugin.json").read_text())["mcpServers"]["probe-research"]
    assert caps_mod.check_mcp("kimi_code")[1].credential == McpCredential.UNKNOWN


def test_logout_takes_the_token_out_of_every_kimi_copy(isolate):
    _config_token(isolate, "tok")
    _kimi_record(isolate, None)
    managed = isolate / "kimi" / "plugins" / "managed"
    old = managed / "probe-research@9.9.8"
    (old / ".kimi-plugin").mkdir(parents=True)
    (old / ".kimi-plugin" / "plugin.json").write_text(json.dumps({"name": "probe-research", "mcpServers": {
        "probe-research": {"url": "https://mcp.research.prbe.ai/mcp", "headers": {"Authorization": "Bearer stale"}}}}))
    for root in managed.glob("probe-research@*"):
        server = json.loads((root / ".kimi-plugin" / "plugin.json").read_text())
        server["mcpServers"]["probe-research"]["url"] = "https://mcp.research.prbe.ai/mcp"
        (root / ".kimi-plugin" / "plugin.json").write_text(json.dumps(server))
    assert kimi_config.sync_mcp_bearer()  # the recorded copy gets the token
    _config_token(isolate, None)  # logout cleared the config
    kimi_config.sync_mcp_bearer()
    for root in managed.glob("probe-research@*"):
        server = json.loads((root / ".kimi-plugin" / "plugin.json").read_text())["mcpServers"]["probe-research"]
        assert server.get("auth") == "oauth" and "headers" not in server, root


def test_a_token_only_in_the_shell_is_never_written_to_kimis_manifest(isolate, monkeypatch):
    _config_token(isolate, None)
    monkeypatch.setenv("PROBE_MCP_TOKEN", "env-only")
    _kimi_record(isolate, None)
    kimi_config.sync_mcp_bearer()
    root = next((isolate / "kimi" / "plugins" / "managed").glob("probe-research@*"))
    assert "env-only" not in (root / ".kimi-plugin" / "plugin.json").read_text()
