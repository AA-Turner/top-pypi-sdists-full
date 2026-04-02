"""Tests for plato.utils.pypi_index and install command index ordering."""

from __future__ import annotations

from plato.agents.runtime.install import build_agent_install_command, build_editable_sdk_install_command
from plato.utils.pypi_index import plato_token_simple_index, redact_pypi_token_credential


def test_redact_pypi_token_credential_strips_secret():
    raw = "uv pip install --index-url 'https://__token__:pk_secret_abc@plato.so/api/v2/pypi/pypi-store/simple/'"
    redacted = redact_pypi_token_credential(raw)
    assert "pk_secret_abc" not in redacted
    assert "__token__:***@plato.so" in redacted


def test_plato_token_simple_index_uses_env_key(monkeypatch):
    monkeypatch.setenv("PLATO_API_KEY", "pk_from_env")
    url = plato_token_simple_index("pypi-store")
    assert "pk_from_env" in url
    assert redact_pypi_token_credential(url) == "https://__token__:***@plato.so/api/v2/pypi/pypi-store/simple/"


class TestAgentInstallCommandIndexOrder:
    """Ensure agent install uses first-match index strategy with correct priority.

    Agents index must be --index (checked first) so agent packages take
    priority over any public PyPI name collision. pypi-store must be
    --default-index (fallback for SDK + public deps). unsafe-best-match
    must NOT be used — it queries all indices for all packages.
    """

    def test_agents_index_checked_before_pypi_store(self, monkeypatch):
        monkeypatch.setenv("PLATO_API_KEY", "pk_test")
        cmd = build_agent_install_command("claude-code", "3.0.22")
        # pypi-store must be --default-index (fallback), agents must be --index (checked first).
        # Parse flags properly to avoid substring collision (--default-index contains --index).
        import re

        default_idx = re.search(r"--default-index\s+(\S+)", cmd)
        idx = re.search(r"(?<!default-)--index\s+(\S+)", cmd)
        assert default_idx is not None, "--default-index not found"
        assert idx is not None, "--index not found"
        assert "pypi-store" in default_idx.group(1)
        assert "agents" in idx.group(1)

    def test_no_unsafe_best_match(self, monkeypatch):
        monkeypatch.setenv("PLATO_API_KEY", "pk_test")
        cmd = build_agent_install_command("claude-code", "3.0.22")
        assert "unsafe-best-match" not in cmd

    def test_no_extra_index_url(self, monkeypatch):
        monkeypatch.setenv("PLATO_API_KEY", "pk_test")
        cmd = build_agent_install_command("claude-code", "3.0.22")
        assert "--extra-index-url" not in cmd


def test_build_editable_sdk_install_command_includes_sdk_and_agent(monkeypatch):
    monkeypatch.setenv("PLATO_API_KEY", "pk_test")
    cmd = build_editable_sdk_install_command("claude-code", "3.1.4")
    assert "uv tool install -e /sdk --python 3.12" in cmd
    assert "--with 'claude-code==3.1.4'" in cmd
    assert "--default-index" in cmd
    assert "--index" in cmd
