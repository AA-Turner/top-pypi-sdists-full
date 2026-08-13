"""Tests for determine_agent, driven primarily by upstream testcases.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from detect_agent import KNOWN_AGENTS, determine_agent
from detect_agent import _evaluate as evaluate_mod

_TESTCASES_PATH = Path(__file__).with_name("testcases.json")
_TESTCASES: list[dict[str, Any]] = json.loads(_TESTCASES_PATH.read_text(encoding="utf-8"))

# Env vars cleared between tests so cases don't leak into each other.
_AGENT_ENV_VARS = (
    "AI_AGENT",
    "PI_CODING_AGENT",
    "CURSOR_TRACE_ID",
    "CURSOR_AGENT",
    "CURSOR_EXTENSION_HOST_ROLE",
    "KIMI_PLUGIN_ROOT",
    "GROK_PLUGIN_ROOT",
    "GROK_PLUGIN_DATA",
    "GEMINI_CLI",
    "CLINE_ACTIVE",
    "CODEX_SANDBOX",
    "CODEX_CI",
    "CODEX_THREAD_ID",
    "CODEX_SANDBOX_NETWORK_DISABLED",
    "ANTIGRAVITY_AGENT",
    "ANTIGRAVITY_CLI_ALIAS",
    "AUGMENT_AGENT",
    "OPENCODE_CLIENT",
    "OPENCODE",
    "GOOSE_PROVIDER",
    "JUNIE_DATA",
    "JUNIE_SHIM_PATH",
    "CLAUDECODE",
    "CLAUDE_CODE",
    "CLAUDE_CODE_IS_COWORK",
    "REPL_ID",
    "COPILOT_MODEL",
    "COPILOT_ALLOW_ALL",
    "COPILOT_GITHUB_TOKEN",
    "TERM_PROGRAM",
    "OPENCLAW_SHELL",
    "PATH",
)


@pytest.fixture(autouse=True)
def _clear_agent_env(monkeypatch: pytest.MonkeyPatch):
    for key in _AGENT_ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    # Neutral PATH so Pi's env_matches cannot fire accidentally from the host.
    monkeypatch.setenv("PATH", "/usr/bin")
    monkeypatch.setattr(evaluate_mod, "is_tty_fn", lambda: True)
    monkeypatch.setattr(evaluate_mod, "path_exists_fn", lambda _path: False)
    yield


def _expected_name(tc: dict[str, Any]) -> str | None:
    if "expectedName" in tc:
        return tc["expectedName"]
    key = tc.get("expectedAgentKey")
    if key is None:
        return None
    return KNOWN_AGENTS[key]


@pytest.mark.parametrize("tc", _TESTCASES, ids=[tc["name"] for tc in _TESTCASES])
def test_upstream_testcase(tc: dict[str, Any], monkeypatch: pytest.MonkeyPatch):
    for key, value in tc.get("env", {}).items():
        monkeypatch.setenv(key, value)

    if tc.get("tty") is not None:
        monkeypatch.setattr(evaluate_mod, "is_tty_fn", lambda: bool(tc["tty"]))

    files = set(tc.get("files") or [])
    if files:
        monkeypatch.setattr(evaluate_mod, "path_exists_fn", lambda path: path in files)

    result = determine_agent()
    expected_name = _expected_name(tc)

    if tc["expectedIsAgent"]:
        assert result == {"is_agent": True, "agent": {"name": expected_name}}
    else:
        assert result == {"is_agent": False, "agent": None}


class TestPythonPortExtensions:
    """Behavior kept for Python-port compatibility / extra coverage."""

    def test_pi_coding_agent_set_detects_pi(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("PI_CODING_AGENT", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["PI"]}}

    def test_ai_agent_github_copilot_cli_is_emitted_verbatim(self, monkeypatch: pytest.MonkeyPatch):
        # Upstream emits AI_AGENT values verbatim (no alias rewriting).
        monkeypatch.setenv("AI_AGENT", "github-copilot-cli")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": "github-copilot-cli"}}

    def test_ai_agent_v0(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("AI_AGENT", "v0")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": "v0"}}


class TestNewUpstreamAgents:
    """Coverage for agents added upstream after the initial JSON testcases."""

    def test_cline_active_detects_cline(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("CLINE_ACTIVE", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CLINE"]}}

    def test_openclaw_shell_detects_openclaw(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("OPENCLAW_SHELL", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["OPENCLAW"]}}

    def test_codex_sandbox_network_disabled_detects_codex(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("CODEX_SANDBOX_NETWORK_DISABLED", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CODEX"]}}

    def test_antigravity_cli_alias_detects_antigravity(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("ANTIGRAVITY_CLI_ALIAS", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["ANTIGRAVITY"]}}


class TestEvaluateCondition:
    """Unit tests for condition leaves/combinators."""

    def test_env_set_true(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("SOME_VAR", "1")
        assert evaluate_mod.evaluate_condition({"type": "env_set", "name": "SOME_VAR"})

    def test_env_set_false_when_empty(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("SOME_VAR", "")
        assert not evaluate_mod.evaluate_condition({"type": "env_set", "name": "SOME_VAR"})

    def test_env_value_match(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("ROLE", "agent-exec")
        assert evaluate_mod.evaluate_condition(
            {"type": "env_value", "name": "ROLE", "value": "agent-exec"}
        )

    def test_env_matches_and_malformed_pattern(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("PATH", "/home/me/.pi/agent/bin")
        assert evaluate_mod.evaluate_condition(
            {"type": "env_matches", "name": "PATH", "pattern": r"\.pi[\\/]agent"}
        )
        assert not evaluate_mod.evaluate_condition(
            {"type": "env_matches", "name": "PATH", "pattern": "("}
        )

    def test_any_of_and_all_of(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("A", "1")
        assert evaluate_mod.evaluate_condition(
            {
                "type": "anyOf",
                "conditions": [
                    {"type": "env_set", "name": "MISSING"},
                    {"type": "env_set", "name": "A"},
                ],
            }
        )
        assert not evaluate_mod.evaluate_condition(
            {
                "type": "allOf",
                "conditions": [
                    {"type": "env_set", "name": "A"},
                    {"type": "env_set", "name": "MISSING"},
                ],
            }
        )

    def test_unknown_condition_type_is_false(self):
        assert not evaluate_mod.evaluate_condition({"type": "not-a-real-type"})
