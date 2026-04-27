"""Tests for config.py env var overrides and load_config branches.

Covers missed lines concentrated in:
- Lines 40-96: build_runtime_context
- Lines 913-968: AI timeout/retry env var loading
- Lines 996-1000: allowed_domains env var
- Lines 1048-1049: port fallback
- Lines 1096-1117: shared_databases / databases keys
- Lines 1130-1181: cli config section
- Lines 1199-1270, 1284-1305: usage / budget config
- Lines 1386-1464: safety / bash sandbox config
- Lines 1473-1826+: load_config branches (proxy, storage, session, audit, etc.)
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from anteroom.config import AppConfig, build_runtime_context, load_config

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_config(path: Path, data: dict) -> Path:
    cfg_file = path / "config.yaml"
    cfg_file.write_text(yaml.dump(data))
    return cfg_file


_MINIMAL_AI = {"ai": {"base_url": "https://api.example.com", "api_key": "sk-test"}}


def _minimal(tmp_path: Path, extra: dict | None = None) -> Path:
    data: dict = dict(_MINIMAL_AI)
    if extra:
        data = {**data, **extra}
    return _write_config(tmp_path, data)


class TestDiagnosticsConfig:
    def test_diagnostics_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)

        assert config.diagnostics.error_log_enabled is True
        assert config.diagnostics.log_path == ""
        assert config.diagnostics.log_successful_debug_turns is False
        assert config.diagnostics.redact_content is True
        assert config.diagnostics.retention_days == 14
        assert config.diagnostics.max_entry_bytes == 32_768

    def test_diagnostics_yaml_values_are_loaded(self, tmp_path: Path) -> None:
        cfg = _minimal(
            tmp_path,
            {
                "diagnostics": {
                    "error_log_enabled": False,
                    "log_path": "/tmp/anteroom-diagnostics",
                    "log_successful_debug_turns": True,
                    "redact_content": False,
                    "retention_days": 30,
                    "rotate_size_bytes": 2_000_000,
                    "max_entry_bytes": 64_000,
                    "max_log_dir_bytes": 20_000_000,
                }
            },
        )
        config, _ = load_config(cfg)

        assert config.diagnostics.error_log_enabled is False
        assert config.diagnostics.log_path == "/tmp/anteroom-diagnostics"
        assert config.diagnostics.log_successful_debug_turns is True
        assert config.diagnostics.redact_content is False
        assert config.diagnostics.retention_days == 30
        assert config.diagnostics.rotate_size_bytes == 2_000_000
        assert config.diagnostics.max_entry_bytes == 64_000
        assert config.diagnostics.max_log_dir_bytes == 20_000_000

    def test_diagnostics_env_values_are_loaded(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_ERROR_LOG_ENABLED", "false")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_LOG_PATH", "/tmp/diag-env")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_LOG_SUCCESSFUL_DEBUG_TURNS", "true")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_REDACT_CONTENT", "false")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_RETENTION_DAYS", "21")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_ROTATE_SIZE_BYTES", "3000000")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_MAX_ENTRY_BYTES", "65000")
        monkeypatch.setenv("AI_CHAT_DIAGNOSTICS_MAX_LOG_DIR_BYTES", "30000000")
        cfg = _minimal(tmp_path)

        config, _ = load_config(cfg)

        assert config.diagnostics.error_log_enabled is False
        assert config.diagnostics.log_path == "/tmp/diag-env"
        assert config.diagnostics.log_successful_debug_turns is True
        assert config.diagnostics.redact_content is False
        assert config.diagnostics.retention_days == 21
        assert config.diagnostics.rotate_size_bytes == 3_000_000
        assert config.diagnostics.max_entry_bytes == 65_000
        assert config.diagnostics.max_log_dir_bytes == 30_000_000

    def test_diagnostics_invalid_values_fall_back_and_clamp(self, tmp_path: Path) -> None:
        cfg = _minimal(
            tmp_path,
            {
                "diagnostics": {
                    "retention_days": "bad",
                    "rotate_size_bytes": 1,
                    "max_entry_bytes": 1,
                    "max_log_dir_bytes": 1,
                }
            },
        )
        config, _ = load_config(cfg)

        assert config.diagnostics.retention_days == 14
        assert config.diagnostics.rotate_size_bytes == 65_536
        assert config.diagnostics.max_entry_bytes == 1_024
        assert config.diagnostics.max_log_dir_bytes == 65_536


# ---------------------------------------------------------------------------
# build_runtime_context (lines 44-118)
# ---------------------------------------------------------------------------


class TestBuildRuntimeContext:
    def test_basic_web_interface(self) -> None:
        ctx = build_runtime_context(model="gpt-4")
        assert "<anteroom_context>" in ctx
        assert "Web UI" in ctx
        assert "gpt-4" in ctx
        assert "</anteroom_context>" in ctx

    def test_version_matches_package_version(self) -> None:
        from anteroom import __version__

        ctx = build_runtime_context(model="gpt-4")
        assert f"v{__version__}" in ctx

    def test_cli_interface(self) -> None:
        ctx = build_runtime_context(model="gpt-4o", interface="cli")
        assert "CLI REPL" in ctx
        assert "CLI:" in ctx

    def test_builtin_tools_listed(self) -> None:
        ctx = build_runtime_context(model="gpt-4", builtin_tools=["read_file", "bash"])
        assert "Available tools:" in ctx
        assert "read_file:" in ctx
        assert "bash:" in ctx

    def test_unknown_builtin_tool_no_description(self) -> None:
        ctx = build_runtime_context(model="gpt-4", builtin_tools=["mystery_tool"])
        assert "mystery_tool" in ctx
        assert "mystery_tool:" not in ctx  # no colon+space since no description

    def test_mcp_servers_listed(self) -> None:
        ctx = build_runtime_context(
            model="gpt-4",
            mcp_servers={
                "my-server": {"status": "connected", "tool_count": 3, "tools": [{"name": "do_thing"}]},
            },
        )
        assert "MCP servers:" in ctx
        assert "my-server: connected (3 tools)" in ctx
        assert "do_thing" in ctx

    def test_mcp_server_not_connected_tools_not_listed(self) -> None:
        ctx = build_runtime_context(
            model="gpt-4",
            mcp_servers={
                "my-server": {"status": "disconnected", "tool_count": 0},
            },
        )
        assert "disconnected" in ctx
        assert "Available tools:" not in ctx

    def test_mcp_tools_as_string_names(self) -> None:
        ctx = build_runtime_context(
            model="gpt-4",
            mcp_servers={
                "srv": {"status": "connected", "tool_count": 1, "tools": ["plain_tool_name"]},
            },
        )
        assert "plain_tool_name" in ctx

    def test_working_dir_shown_for_cli(self) -> None:
        ctx = build_runtime_context(model="gpt-4", interface="cli", working_dir="/tmp/project")
        assert "Working directory: /tmp/project" in ctx

    def test_working_dir_not_shown_for_web(self) -> None:
        ctx = build_runtime_context(model="gpt-4", interface="web", working_dir="/tmp/project")
        assert "Working directory" not in ctx

    def test_tls_shown_for_web(self) -> None:
        ctx = build_runtime_context(model="gpt-4", interface="web", tls_enabled=True)
        assert "TLS: enabled" in ctx

    def test_tls_disabled_for_web(self) -> None:
        ctx = build_runtime_context(model="gpt-4", interface="web", tls_enabled=False)
        assert "TLS: disabled" in ctx

    def test_tls_not_shown_for_cli(self) -> None:
        ctx = build_runtime_context(model="gpt-4", interface="cli", tls_enabled=True)
        assert "TLS:" not in ctx


# ---------------------------------------------------------------------------
# AI timeout env var overrides (lines 911-968)
# ---------------------------------------------------------------------------


class TestAITimeoutEnvVars:
    def test_request_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_REQUEST_TIMEOUT", "300")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.request_timeout == 300

    def test_request_timeout_clamped_max(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_REQUEST_TIMEOUT", "9999")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.request_timeout == 600

    def test_request_timeout_clamped_min(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_REQUEST_TIMEOUT", "1")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.request_timeout == 10

    def test_request_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_REQUEST_TIMEOUT", "notanumber")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.request_timeout == 120

    def test_connect_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_CONNECT_TIMEOUT", "10")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.connect_timeout == 10

    def test_connect_timeout_clamped_max(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_CONNECT_TIMEOUT", "999")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.connect_timeout == 30

    def test_connect_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_CONNECT_TIMEOUT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.connect_timeout == 5

    def test_write_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_WRITE_TIMEOUT", "60")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.write_timeout == 60

    def test_write_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_WRITE_TIMEOUT", "x")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.write_timeout == 30

    def test_pool_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_POOL_TIMEOUT", "30")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.pool_timeout == 30

    def test_pool_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_POOL_TIMEOUT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.pool_timeout == 10

    def test_first_token_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_FIRST_TOKEN_TIMEOUT", "45")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.first_token_timeout == 45

    def test_first_token_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_FIRST_TOKEN_TIMEOUT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.first_token_timeout == 30

    def test_chunk_stall_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_CHUNK_STALL_TIMEOUT", "60")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.chunk_stall_timeout == 60

    def test_chunk_stall_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_CHUNK_STALL_TIMEOUT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.chunk_stall_timeout == 30

    def test_retry_max_attempts_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RETRY_MAX_ATTEMPTS", "5")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.retry_max_attempts == 5

    def test_retry_max_attempts_clamped_max(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RETRY_MAX_ATTEMPTS", "999")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.retry_max_attempts == 10

    def test_retry_max_attempts_clamped_min(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RETRY_MAX_ATTEMPTS", "-5")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.retry_max_attempts == 0

    def test_retry_max_attempts_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RETRY_MAX_ATTEMPTS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.retry_max_attempts == 3

    def test_retry_backoff_base_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RETRY_BACKOFF_BASE", "2.5")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.retry_backoff_base == 2.5

    def test_retry_backoff_base_clamped_min(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RETRY_BACKOFF_BASE", "0.0")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.retry_backoff_base == 0.1

    def test_retry_backoff_base_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "https://api.example.com", "api_key": "sk-test", "retry_backoff_base": "notanumber"}},
        )
        config, _ = load_config(cfg)
        assert config.ai.retry_backoff_base == 1.0

    def test_max_tools_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MAX_TOOLS", "64")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.max_tools == 64

    def test_max_tools_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MAX_TOOLS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.max_tools == 128

    def test_verify_ssl_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_VERIFY_SSL", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.verify_ssl is False

    def test_verify_ssl_env_var_true(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_VERIFY_SSL", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.verify_ssl is True

    def test_verify_ssl_env_var_zero(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_VERIFY_SSL", "0")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.verify_ssl is False


# ---------------------------------------------------------------------------
# allowed_domains and block_localhost_api (lines 994-1003)
# ---------------------------------------------------------------------------


class TestAllowedDomainsEnvVar:
    def test_allowed_domains_env_var_comma_separated(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_ALLOWED_DOMAINS", "api.example.com,other.example.com")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.allowed_domains == ["api.example.com", "other.example.com"]

    def test_allowed_domains_env_var_overrides_yaml(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_ALLOWED_DOMAINS", "env-domain.com")
        cfg = _write_config(
            tmp_path,
            {
                "ai": {
                    "base_url": "https://api.example.com",
                    "api_key": "sk-test",
                    "allowed_domains": ["yaml-domain.com"],
                }
            },
        )
        config, _ = load_config(cfg)
        assert config.ai.allowed_domains == ["env-domain.com"]

    def test_allowed_domains_yaml_when_no_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AI_CHAT_ALLOWED_DOMAINS", raising=False)
        cfg = _write_config(
            tmp_path,
            {
                "ai": {
                    "base_url": "https://api.example.com",
                    "api_key": "sk-test",
                    "allowed_domains": ["yaml-domain.com"],
                }
            },
        )
        config, _ = load_config(cfg)
        assert config.ai.allowed_domains == ["yaml-domain.com"]

    def test_allowed_domains_non_list_yaml_ignored(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AI_CHAT_ALLOWED_DOMAINS", raising=False)
        cfg = _write_config(
            tmp_path,
            {
                "ai": {
                    "base_url": "https://api.example.com",
                    "api_key": "sk-test",
                    "allowed_domains": "notalist",
                }
            },
        )
        config, _ = load_config(cfg)
        assert config.ai.allowed_domains == []

    def test_block_localhost_api_env_var_true(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BLOCK_LOCALHOST_API", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.block_localhost_api is True

    def test_block_localhost_api_default_false(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.ai.block_localhost_api is False


# ---------------------------------------------------------------------------
# Port env var and invalid port (lines 1045-1050)
# ---------------------------------------------------------------------------


class TestPortConfig:
    def test_port_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_PORT", "9090")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.app.port == 9090

    def test_port_invalid_env_var_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_PORT", "notaport")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.app.port == 8080

    def test_port_yaml_overrides_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_PORT", "9999")
        cfg = _write_config(
            tmp_path, {"ai": {"base_url": "https://api.example.com", "api_key": "sk-test"}, "app": {"port": 7777}}
        )
        config, _ = load_config(cfg)
        assert config.app.port == 7777

    def test_port_clamped_max(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "https://api.example.com", "api_key": "sk-test"}, "app": {"port": 99999}},
        )
        config, _ = load_config(cfg)
        assert config.app.port == 65535


# ---------------------------------------------------------------------------
# MCP server disabled flag (line 1062)
# ---------------------------------------------------------------------------


class TestMcpServerDisabled:
    def test_disabled_mcp_server_skipped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "https://api.example.com", "api_key": "sk-test"},
                "mcp_servers": [
                    {"name": "active-server", "transport": "stdio", "command": "npx"},
                    {"name": "disabled-server", "transport": "stdio", "command": "npx", "enabled": False},
                ],
            },
        )
        config, _ = load_config(cfg)
        names = [s.name for s in config.mcp_servers]
        assert "active-server" in names
        assert "disabled-server" not in names


# ---------------------------------------------------------------------------
# Shared databases (lines 1099-1123)
# ---------------------------------------------------------------------------


class TestSharedDatabasesConfig:
    def test_shared_databases_parsed(self, tmp_path: Path) -> None:
        db_path = str(tmp_path / "shared.db")
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "https://api.example.com", "api_key": "sk-test"},
                "shared_databases": [{"name": "team-db", "path": db_path, "passphrase_hash": "abc123"}],
            },
        )
        config, _ = load_config(cfg)
        assert len(config.shared_databases) == 1
        assert config.shared_databases[0].name == "team-db"
        assert config.shared_databases[0].passphrase_hash == "abc123"

    def test_disabled_shared_database_skipped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "https://api.example.com", "api_key": "sk-test"},
                "shared_databases": [
                    {"name": "active-db", "path": "/tmp/active.db"},
                    {"name": "disabled-db", "path": "/tmp/disabled.db", "enabled": False},
                ],
            },
        )
        config, _ = load_config(cfg)
        names = [db.name for db in config.shared_databases]
        assert "active-db" in names
        assert "disabled-db" not in names

    def test_databases_key_skips_personal(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "https://api.example.com", "api_key": "sk-test"},
                "databases": {
                    "personal": {"path": "/tmp/personal.db"},
                    "team": {"path": "/tmp/team.db"},
                },
            },
        )
        config, _ = load_config(cfg)
        names = [db.name for db in config.shared_databases]
        assert "personal" not in names
        assert "team" in names


# ---------------------------------------------------------------------------
# CLI config section (lines 1133-1177)
# ---------------------------------------------------------------------------


class TestCliConfig:
    def test_context_warn_tokens_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"context_warn_tokens": 50000}},
        )
        config, _ = load_config(cfg)
        assert config.cli.context_warn_tokens == 50000

    def test_context_warn_tokens_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"context_warn_tokens": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.context_warn_tokens == 80_000

    def test_context_auto_compact_tokens_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"context_auto_compact_tokens": 75000}},
        )
        config, _ = load_config(cfg)
        assert config.cli.context_auto_compact_tokens == 75000

    def test_context_auto_compact_tokens_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"context_auto_compact_tokens": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.context_auto_compact_tokens == 100_000

    def test_context_thresholds_derive_for_smaller_model_window(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"model_context_window": 32_000}},
        )
        config, _ = load_config(cfg)

        assert config.cli.context_warn_tokens == 17_440
        assert config.compaction.summary_trigger_token_count == 19_532
        assert config.cli.context_auto_compact_tokens == 21_765

    def test_explicit_context_thresholds_override_derived_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {
                    "model_context_window": 32_000,
                    "context_warn_tokens": 12_000,
                    "context_auto_compact_tokens": 14_000,
                },
                "compaction": {"summary_trigger_token_count": 13_000},
            },
        )
        config, _ = load_config(cfg)

        assert config.cli.context_warn_tokens == 12_000
        assert config.compaction.summary_trigger_token_count == 13_000
        assert config.cli.context_auto_compact_tokens == 14_000

    def test_context_threshold_env_overrides_are_honored(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MODEL_CONTEXT_WINDOW", "40_000")
        monkeypatch.setenv("AI_CHAT_CONTEXT_RESERVED_OUTPUT_TOKENS", "4_000")
        monkeypatch.setenv("AI_CHAT_CONTEXT_WARN_BUFFER_TOKENS", "8_000")
        monkeypatch.setenv("AI_CHAT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS", "4_000")
        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_BUFFER_TOKENS", "6_000")
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})

        config, _ = load_config(cfg)

        assert config.cli.context_reserved_output_tokens == 4_000
        assert config.cli.context_warn_tokens == 28_000
        assert config.compaction.summary_trigger_token_count == 30_000
        assert config.cli.context_auto_compact_tokens == 32_000

    def test_legacy_context_threshold_env_overrides_are_honored(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("AI_CHAT_CONTEXT_WARN_TOKENS", "11_000")
        monkeypatch.setenv("AI_CHAT_CONTEXT_AUTO_COMPACT_TOKENS", "12_000")
        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_TOKEN_COUNT", "13_000")
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})

        config, _ = load_config(cfg)

        assert config.cli.context_warn_tokens == 11_000
        assert config.cli.context_auto_compact_tokens == 12_000
        assert config.compaction.summary_trigger_token_count == 13_000

    def test_retry_delay_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"retry_delay": 10.0}},
        )
        config, _ = load_config(cfg)
        assert config.cli.retry_delay == 10.0

    def test_retry_delay_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"retry_delay": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.retry_delay == 5.0

    def test_max_retries_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"max_retries": 5}},
        )
        config, _ = load_config(cfg)
        assert config.cli.max_retries == 5

    def test_max_retries_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"max_retries": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.max_retries == 3

    def test_esc_hint_delay_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"esc_hint_delay": 1.5}},
        )
        config, _ = load_config(cfg)
        assert config.cli.esc_hint_delay == 1.5

    def test_esc_hint_delay_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"esc_hint_delay": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.esc_hint_delay == 8.0

    def test_tool_output_max_chars_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"tool_output_max_chars": 500}},
        )
        config, _ = load_config(cfg)
        assert config.cli.tool_output_max_chars == 500

    def test_tool_output_max_chars_default(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.tool_output_max_chars == 10_000

    def test_tool_output_max_chars_clamped_min(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"tool_output_max_chars": 10}},
        )
        config, _ = load_config(cfg)
        assert config.cli.tool_output_max_chars == 100

    def test_tool_output_max_chars_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"tool_output_max_chars": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.tool_output_max_chars == 10_000

    def test_update_check_message_default(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.update_check_message == (
            "Update available: {current} -> {latest} -- pip install --upgrade anteroom"
        )

    def test_update_check_message_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"update_check_message": "Install {latest}; current {current}"},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.update_check_message == "Install {latest}; current {current}"

    def test_update_check_message_from_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        monkeypatch.setenv("AI_CHAT_UPDATE_CHECK_MESSAGE", "Ask IT for {latest}")
        config, _ = load_config(cfg)
        assert config.cli.update_check_message == "Ask IT for {latest}"

    def test_tool_replay_max_chars_default(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.tool_replay_max_chars == 10_000

    def test_tool_replay_max_chars_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"tool_replay_max_chars": 750}},
        )
        config, _ = load_config(cfg)
        assert config.cli.tool_replay_max_chars == 750

    def test_tool_replay_max_chars_from_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        monkeypatch.setenv("AI_CHAT_TOOL_REPLAY_MAX_CHARS", "900")
        config, _ = load_config(cfg)
        assert config.cli.tool_replay_max_chars == 900

    def test_tool_replay_max_chars_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"tool_replay_max_chars": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.tool_replay_max_chars == 10_000

    def test_show_attribution_footer_default_true(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.show_attribution_footer is True

    def test_show_attribution_footer_disabled_via_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"show_attribution_footer": False}},
        )
        config, _ = load_config(cfg)
        assert config.cli.show_attribution_footer is False

    def test_show_attribution_footer_env_overrides_yaml(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """AI_CHAT_SHOW_ATTRIBUTION_FOOTER overrides YAML — matches docs promise (#923)."""
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"show_attribution_footer": True}},
        )
        for val in ("false", "0", "no", "FALSE"):
            monkeypatch.setenv("AI_CHAT_SHOW_ATTRIBUTION_FOOTER", val)
            config, _ = load_config(cfg)
            assert config.cli.show_attribution_footer is False, f"expected False for env={val!r}"

    def test_show_attribution_footer_env_truthy(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"show_attribution_footer": False}},
        )
        monkeypatch.setenv("AI_CHAT_SHOW_ATTRIBUTION_FOOTER", "true")
        config, _ = load_config(cfg)
        assert config.cli.show_attribution_footer is True

    def test_file_reference_max_chars_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"file_reference_max_chars": 50000}},
        )
        config, _ = load_config(cfg)
        assert config.cli.file_reference_max_chars == 50000

    def test_model_context_window_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"model_context_window": 200000}},
        )
        config, _ = load_config(cfg)
        assert config.cli.model_context_window == 200000

    def test_model_context_window_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"model_context_window": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.model_context_window == 128_000

    def test_stall_display_threshold_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"stall_display_threshold": 10.0}},
        )
        config, _ = load_config(cfg)
        assert config.cli.stall_display_threshold == 10.0

    def test_stall_display_threshold_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"stall_display_threshold": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.stall_display_threshold == 5.0

    def test_stall_warning_threshold_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"stall_warning_threshold": 20.0}},
        )
        config, _ = load_config(cfg)
        assert config.cli.stall_warning_threshold == 20.0

    def test_stall_warning_threshold_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"stall_warning_threshold": "bad"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.stall_warning_threshold == 15.0

    def test_planning_not_a_dict_falls_back_to_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"planning": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.planning.enabled is True

    def test_skills_auto_invoke_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"skills": {"auto_invoke": False}}},
        )
        config, _ = load_config(cfg)
        assert config.cli.skills.auto_invoke is False

    def test_skills_not_a_dict_uses_default(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"skills": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.skills.auto_invoke is True

    # --- cli.hierarchy config (#1370) ---

    def test_hierarchy_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.show_timestamps is False
        assert config.cli.hierarchy.turn_separator_char == "\u2500"
        assert config.cli.hierarchy.code_block_language_label is True

    def test_hierarchy_show_timestamps_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"hierarchy": {"show_timestamps": True}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.show_timestamps is True

    def test_hierarchy_turn_separator_char_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"hierarchy": {"turn_separator_char": "="}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.turn_separator_char == "="

    def test_hierarchy_code_block_language_label_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"hierarchy": {"code_block_language_label": False}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.code_block_language_label is False

    def test_hierarchy_not_a_dict_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"hierarchy": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.show_timestamps is False
        assert config.cli.hierarchy.turn_separator_char == "\u2500"
        assert config.cli.hierarchy.code_block_language_label is True

    def test_hierarchy_show_timestamps_env_overrides_yaml(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"hierarchy": {"show_timestamps": False}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_HIERARCHY_SHOW_TIMESTAMPS", "true")
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.show_timestamps is True

    def test_hierarchy_turn_separator_char_env_overrides_yaml(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"hierarchy": {"turn_separator_char": "-"}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_HIERARCHY_TURN_SEPARATOR_CHAR", "*")
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.turn_separator_char == "*"

    def test_hierarchy_code_block_language_label_env_overrides_yaml(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"hierarchy": {"code_block_language_label": True}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_HIERARCHY_CODE_BLOCK_LANGUAGE_LABEL", "false")
        config, _ = load_config(cfg)
        assert config.cli.hierarchy.code_block_language_label is False

    # --- cli.streaming config (#1365) ---

    def test_streaming_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.streaming.enabled is False
        assert config.cli.streaming.refresh_hz == 20.0
        assert config.cli.streaming.live_in_exec_mode is False
        assert config.cli.streaming.code_fence_container is True

    def test_streaming_enabled_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"enabled": False}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.streaming.enabled is False

    def test_streaming_refresh_hz_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"refresh_hz": 30.0}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.streaming.refresh_hz == 30.0

    def test_streaming_refresh_hz_clamped_high(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"refresh_hz": 500.0}},
            },
        )
        with caplog.at_level("WARNING", logger="anteroom.config"):
            config, _ = load_config(cfg)
        assert config.cli.streaming.refresh_hz == 60.0
        assert any("refresh_hz" in r.message for r in caplog.records)

    def test_streaming_refresh_hz_clamped_low(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"refresh_hz": 0.0}},
            },
        )
        with caplog.at_level("WARNING", logger="anteroom.config"):
            config, _ = load_config(cfg)
        assert config.cli.streaming.refresh_hz == 1.0
        assert any("refresh_hz" in r.message for r in caplog.records)

    def test_streaming_live_in_exec_mode_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"live_in_exec_mode": True}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.streaming.live_in_exec_mode is True

    def test_streaming_code_fence_container_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"code_fence_container": False}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.streaming.code_fence_container is False

    def test_streaming_not_a_dict_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"streaming": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.streaming.enabled is False
        assert config.cli.streaming.refresh_hz == 20.0
        assert config.cli.streaming.live_in_exec_mode is False
        assert config.cli.streaming.code_fence_container is True

    def test_streaming_env_override_enabled(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"enabled": True}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_STREAMING_ENABLED", "false")
        config, _ = load_config(cfg)
        assert config.cli.streaming.enabled is False

    def test_streaming_env_override_enables_from_default_off(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        monkeypatch.setenv("AI_CHAT_CLI_STREAMING_ENABLED", "true")
        config, _ = load_config(cfg)
        assert config.cli.streaming.enabled is True

    def test_streaming_env_override_refresh_hz(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"refresh_hz": 20.0}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_STREAMING_REFRESH_HZ", "45.0")
        config, _ = load_config(cfg)
        assert config.cli.streaming.refresh_hz == 45.0

    def test_streaming_env_override_live_in_exec_mode(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"live_in_exec_mode": False}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_STREAMING_LIVE_IN_EXEC_MODE", "true")
        config, _ = load_config(cfg)
        assert config.cli.streaming.live_in_exec_mode is True

    def test_streaming_env_override_code_fence_container(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"streaming": {"code_fence_container": True}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_STREAMING_CODE_FENCE_CONTAINER", "false")
        config, _ = load_config(cfg)
        assert config.cli.streaming.code_fence_container is False

    # --- cli.live_tools config (#1364) ---

    def test_live_tools_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.live_tools.show_args_in_verbose is True
        assert config.cli.live_tools.show_metric_suffix is True
        assert config.cli.live_tools.metric_max_chars == 40

    def test_live_tools_show_args_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"show_args_in_verbose": False}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.live_tools.show_args_in_verbose is False

    def test_live_tools_show_metric_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"show_metric_suffix": False}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.live_tools.show_metric_suffix is False

    def test_live_tools_metric_max_chars_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"metric_max_chars": 80}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.live_tools.metric_max_chars == 80

    def test_live_tools_metric_max_chars_clamped_low(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"metric_max_chars": 0}},
            },
        )
        with caplog.at_level("WARNING", logger="anteroom.config"):
            config, _ = load_config(cfg)
        assert config.cli.live_tools.metric_max_chars == 1
        assert any("metric_max_chars" in r.message for r in caplog.records)

    def test_live_tools_metric_max_chars_clamped_high(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"metric_max_chars": 9999}},
            },
        )
        with caplog.at_level("WARNING", logger="anteroom.config"):
            config, _ = load_config(cfg)
        assert config.cli.live_tools.metric_max_chars == 200
        assert any("metric_max_chars" in r.message for r in caplog.records)

    def test_live_tools_not_a_dict_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"live_tools": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.live_tools.show_args_in_verbose is True
        assert config.cli.live_tools.show_metric_suffix is True
        assert config.cli.live_tools.metric_max_chars == 40

    def test_live_tools_env_override_show_args(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"show_args_in_verbose": True}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_LIVE_TOOLS_SHOW_ARGS_IN_VERBOSE", "false")
        config, _ = load_config(cfg)
        assert config.cli.live_tools.show_args_in_verbose is False

    def test_live_tools_env_override_show_metric(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"show_metric_suffix": True}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_LIVE_TOOLS_SHOW_METRIC_SUFFIX", "false")
        config, _ = load_config(cfg)
        assert config.cli.live_tools.show_metric_suffix is False

    def test_live_tools_env_override_metric_max_chars(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"live_tools": {"metric_max_chars": 40}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_LIVE_TOOLS_METRIC_MAX_CHARS", "60")
        config, _ = load_config(cfg)
        assert config.cli.live_tools.metric_max_chars == 60

    # --- cli.density config (#1367) ---

    def test_density_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(tmp_path, {"ai": {"base_url": "http://t", "api_key": "k"}})
        config, _ = load_config(cfg)
        assert config.cli.density.mode == "normal"
        assert config.cli.density.collapse_repeats is True
        assert config.cli.density.diff_context_lines == 3
        assert config.cli.density.head_lines == 3
        assert config.cli.density.tail_lines == 2

    def test_density_mode_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"mode": "compact"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.density.mode == "compact"

    def test_density_mode_invalid_falls_back_to_normal(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"mode": "bogus"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.density.mode == "normal"

    def test_density_collapse_repeats_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"collapse_repeats": False}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.density.collapse_repeats is False

    def test_density_diff_context_lines_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"diff_context_lines": 5}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.density.diff_context_lines == 5

    def test_density_head_tail_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"head_lines": 6, "tail_lines": 4}},
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.density.head_lines == 6
        assert config.cli.density.tail_lines == 4

    def test_density_not_a_dict_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"density": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.density.mode == "normal"
        assert config.cli.density.collapse_repeats is True
        assert config.cli.density.diff_context_lines == 3
        assert config.cli.density.head_lines == 3
        assert config.cli.density.tail_lines == 2

    def test_density_env_override_mode(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"mode": "normal"}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_DENSITY_MODE", "compact")
        config, _ = load_config(cfg)
        assert config.cli.density.mode == "compact"

    def test_density_env_override_collapse_repeats(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"collapse_repeats": True}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_DENSITY_COLLAPSE_REPEATS", "false")
        config, _ = load_config(cfg)
        assert config.cli.density.collapse_repeats is False

    def test_density_env_override_diff_context_lines(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"diff_context_lines": 3}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_DENSITY_DIFF_CONTEXT_LINES", "7")
        config, _ = load_config(cfg)
        assert config.cli.density.diff_context_lines == 7

    def test_density_env_override_head_lines(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"head_lines": 3}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_DENSITY_HEAD_LINES", "8")
        config, _ = load_config(cfg)
        assert config.cli.density.head_lines == 8

    def test_density_env_override_tail_lines(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"density": {"tail_lines": 2}},
            },
        )
        monkeypatch.setenv("AI_CHAT_CLI_DENSITY_TAIL_LINES", "9")
        config, _ = load_config(cfg)
        assert config.cli.density.tail_lines == 9

    def test_density_int_clamped_non_negative(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {
                    "density": {
                        "diff_context_lines": -4,
                        "head_lines": -1,
                        "tail_lines": -1,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert config.cli.density.diff_context_lines == 0
        assert config.cli.density.head_lines == 0
        assert config.cli.density.tail_lines == 0


# ---------------------------------------------------------------------------
# Usage config (lines 1199-1224)
# ---------------------------------------------------------------------------


class TestUsageConfig:
    def test_usage_week_days_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": {"week_days": 14}}},
        )
        config, _ = load_config(cfg)
        assert config.cli.usage.week_days == 14

    def test_usage_week_days_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": {"week_days": "bad"}}},
        )
        config, _ = load_config(cfg)
        assert config.cli.usage.week_days == 7

    def test_usage_month_days_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": {"month_days": 60}}},
        )
        config, _ = load_config(cfg)
        assert config.cli.usage.month_days == 60

    def test_usage_month_days_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": {"month_days": "bad"}}},
        )
        config, _ = load_config(cfg)
        assert config.cli.usage.month_days == 30

    def test_usage_model_costs_merged(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {"usage": {"model_costs": {"my-model": {"input": 0.001, "output": 0.002}}}},
            },
        )
        config, _ = load_config(cfg)
        assert "my-model" in config.cli.usage.model_costs
        assert config.cli.usage.model_costs["my-model"]["input"] == 0.001

    def test_usage_model_costs_not_a_dict_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": {"model_costs": "notadict"}}},
        )
        config, _ = load_config(cfg)
        assert isinstance(config.cli.usage.model_costs, dict)

    def test_usage_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": "notadict"}},
        )
        config, _ = load_config(cfg)
        assert config.cli.usage.week_days == 7


# ---------------------------------------------------------------------------
# Budget config (lines 1226-1301)
# ---------------------------------------------------------------------------


class TestBudgetConfig:
    def test_budget_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.enabled is True

    def test_budget_disabled_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.enabled is False

    def test_budget_max_per_request_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_MAX_TOKENS_PER_REQUEST", "5000")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.max_tokens_per_request == 5000

    def test_budget_max_per_request_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_MAX_TOKENS_PER_REQUEST", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.max_tokens_per_request == 0

    def test_budget_max_per_conversation_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_MAX_TOKENS_PER_CONVERSATION", "50000")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.max_tokens_per_conversation == 50000

    def test_budget_max_per_day_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_MAX_TOKENS_PER_DAY", "1000000")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.max_tokens_per_day == 1000000

    def test_budget_warn_threshold_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_WARN_THRESHOLD_PERCENT", "90")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.warn_threshold_percent == 90

    def test_budget_warn_threshold_clamped_max(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_WARN_THRESHOLD_PERCENT", "200")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.warn_threshold_percent == 100

    def test_budget_warn_threshold_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_WARN_THRESHOLD_PERCENT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.warn_threshold_percent == 80

    def test_budget_action_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_ACTION_ON_EXCEED", "warn")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.action_on_exceed == "warn"

    def test_budget_action_invalid_falls_back_to_block(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BUDGET_ACTION_ON_EXCEED", "garbage")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.action_on_exceed == "block"

    def test_budget_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "cli": {
                    "usage": {
                        "budgets": {
                            "enabled": True,
                            "max_tokens_per_request": 2000,
                            "max_tokens_per_conversation": 20000,
                            "max_tokens_per_day": 100000,
                            "warn_threshold_percent": 75,
                            "action_on_exceed": "warn",
                        }
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        b = config.cli.usage.budgets
        assert b.enabled is True
        assert b.max_tokens_per_request == 2000
        assert b.max_tokens_per_conversation == 20000
        assert b.max_tokens_per_day == 100000
        assert b.warn_threshold_percent == 75
        assert b.action_on_exceed == "warn"

    def test_budgets_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "cli": {"usage": {"budgets": "notadict"}}},
        )
        config, _ = load_config(cfg)
        assert config.cli.usage.budgets.enabled is False


# ---------------------------------------------------------------------------
# Safety config (lines 1376-1478)
# ---------------------------------------------------------------------------


class TestSafetyConfig:
    def test_safety_enabled_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.enabled is True

    def test_safety_enabled_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SAFETY_ENABLED", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.enabled is False

    def test_safety_approval_mode_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SAFETY_APPROVAL_MODE", "auto")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.approval_mode == "auto"

    def test_safety_approval_mode_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"approval_mode": "ask"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.approval_mode == "ask"

    def test_read_only_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_READ_ONLY", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.read_only is True

    def test_read_only_default_false(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.read_only is False

    def test_safety_allowed_tools_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"allowed_tools": ["bash", "read_file"]},
            },
        )
        config, _ = load_config(cfg)
        assert "bash" in config.safety.allowed_tools
        assert "read_file" in config.safety.allowed_tools

    def test_safety_allowed_tools_not_list_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"allowed_tools": "notalist"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.allowed_tools == []

    def test_safety_denied_tools_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"denied_tools": ["run_agent"]},
            },
        )
        config, _ = load_config(cfg)
        assert "run_agent" in config.safety.denied_tools

    def test_safety_tool_tiers_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"tool_tiers": {"bash": "READ"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.tool_tiers.get("bash") == "READ"

    def test_safety_tool_tiers_not_dict_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"tool_tiers": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.tool_tiers == {}

    def test_safety_custom_patterns_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"custom_patterns": ["rm -rf", "sudo"]},
            },
        )
        config, _ = load_config(cfg)
        assert "rm -rf" in config.safety.custom_patterns

    def test_safety_sensitive_paths_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"sensitive_paths": ["/etc/passwd"]},
            },
        )
        config, _ = load_config(cfg)
        assert "/etc/passwd" in config.safety.sensitive_paths


# ---------------------------------------------------------------------------
# Bash sandbox config (lines 1384-1453)
# ---------------------------------------------------------------------------


class TestBashSandboxConfig:
    def test_bash_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_TIMEOUT", "60")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.timeout == 60

    def test_bash_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_TIMEOUT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.timeout == 120

    def test_bash_max_output_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_MAX_OUTPUT", "50000")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.max_output_chars == 50000

    def test_bash_blocked_paths_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_BLOCKED_PATHS", "/etc,/root")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert "/etc" in config.safety.bash.blocked_paths
        assert "/root" in config.safety.bash.blocked_paths

    def test_bash_blocked_commands_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_BLOCKED_COMMANDS", "curl,wget")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert "curl" in config.safety.bash.blocked_commands
        assert "wget" in config.safety.bash.blocked_commands

    def test_bash_allowed_paths_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_ALLOWED_PATHS", "/tmp,/home/user")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert "/tmp" in config.safety.bash.allowed_paths

    def test_bash_allow_network_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_ALLOW_NETWORK", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.allow_network is False

    def test_bash_allow_package_install_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_ALLOW_PACKAGE_INSTALL", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.allow_package_install is False

    def test_bash_log_all_commands_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_LOG_ALL_COMMANDS", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.log_all_commands is True

    def test_bash_blocked_paths_from_yaml_list(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AI_CHAT_BASH_BLOCKED_PATHS", raising=False)
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"bash": {"blocked_paths": ["/etc", "/var"]}},
            },
        )
        config, _ = load_config(cfg)
        assert "/etc" in config.safety.bash.blocked_paths
        assert "/var" in config.safety.bash.blocked_paths

    def test_bash_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"bash": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.bash.timeout == 120

    def test_sandbox_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_SANDBOX_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.enabled is True

    def test_sandbox_enabled_none_when_not_set(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AI_CHAT_BASH_SANDBOX_ENABLED", raising=False)
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.enabled is None

    def test_sandbox_max_memory_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_SANDBOX_MAX_MEMORY_MB", "1024")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.max_memory_mb == 1024

    def test_sandbox_cpu_time_limit_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_SANDBOX_CPU_TIME_LIMIT", "30")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.cpu_time_limit == 30

    def test_sandbox_cpu_time_limit_none_when_not_set(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AI_CHAT_BASH_SANDBOX_CPU_TIME_LIMIT", raising=False)
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.cpu_time_limit is None

    def test_sandbox_cpu_time_limit_invalid_returns_none(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_BASH_SANDBOX_CPU_TIME_LIMIT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.cpu_time_limit is None

    def test_sandbox_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"bash": {"sandbox": "notadict"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.bash.sandbox.max_memory_mb == 512


# ---------------------------------------------------------------------------
# Subagent config (lines 1480-1499)
# ---------------------------------------------------------------------------


class TestSubagentConfig:
    def test_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        sa = config.safety.subagent
        assert sa.max_concurrent == 5
        assert sa.max_total == 10
        assert sa.max_depth == 3
        assert sa.max_iterations == 15
        assert sa.timeout == 120

    def test_custom_values(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "subagent": {
                        "max_concurrent": 3,
                        "max_total": 20,
                        "max_depth": 2,
                        "max_iterations": 10,
                        "timeout": 60,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        sa = config.safety.subagent
        assert sa.max_concurrent == 3
        assert sa.max_total == 20
        assert sa.max_depth == 2
        assert sa.max_iterations == 10
        assert sa.timeout == 60

    def test_invalid_values_clamped_to_bounds(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"subagent": {"max_concurrent": 999, "max_depth": 0}},
            },
        )
        config, _ = load_config(cfg)
        sa = config.safety.subagent
        assert sa.max_concurrent == 20
        assert sa.max_depth == 1

    def test_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"subagent": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.subagent.max_concurrent == 5


# ---------------------------------------------------------------------------
# Workflow config
# ---------------------------------------------------------------------------


class TestWorkflowConfig:
    def test_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        workflow = config.workflow
        assert workflow.approval_mode == "ask_for_dangerous"
        assert workflow.max_iterations == 30
        assert workflow.executor_enabled is False
        assert workflow.executor_poll_interval == 5
        assert workflow.max_concurrent_runs == 3
        assert workflow.scheduler_enabled is True
        assert workflow.min_schedule_interval == 60
        assert workflow.watch_buffer_lines == 50
        assert workflow.transcript.enabled is True
        assert workflow.transcript.max_assistant_chars == 4000

    def test_custom_values(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "workflow": {
                    "approval_mode": "ask_for_writes",
                    "max_iterations": 45,
                    "executor_enabled": True,
                    "executor_poll_interval": 9,
                    "max_concurrent_runs": 7,
                    "scheduler_enabled": False,
                    "min_schedule_interval": 120,
                    "watch_buffer_lines": 120,
                    "transcript": {
                        "enabled": False,
                        "max_assistant_chars": 1234,
                        "max_tool_output_chars": 2345,
                        "max_stdout_chars": 3456,
                        "max_stderr_chars": 4567,
                    },
                },
            },
        )
        config, _ = load_config(cfg)
        workflow = config.workflow
        assert workflow.approval_mode == "ask_for_writes"
        assert workflow.max_iterations == 45
        assert workflow.executor_enabled is True
        assert workflow.executor_poll_interval == 9
        assert workflow.max_concurrent_runs == 7
        assert workflow.scheduler_enabled is False
        assert workflow.min_schedule_interval == 120
        assert workflow.watch_buffer_lines == 120
        assert workflow.transcript.enabled is False
        assert workflow.transcript.max_assistant_chars == 1234
        assert workflow.transcript.max_tool_output_chars == 2345
        assert workflow.transcript.max_stdout_chars == 3456
        assert workflow.transcript.max_stderr_chars == 4567

    def test_invalid_values_clamped_to_bounds(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "workflow": {
                    "max_iterations": 999,
                    "executor_poll_interval": 0,
                    "max_concurrent_runs": 0,
                    "min_schedule_interval": 10,
                    "watch_buffer_lines": 0,
                },
            },
        )
        config, _ = load_config(cfg)
        workflow = config.workflow
        assert workflow.max_iterations == 100
        assert workflow.executor_poll_interval == 1
        assert workflow.max_concurrent_runs == 1
        assert workflow.min_schedule_interval == 60
        assert workflow.watch_buffer_lines == 1


# ---------------------------------------------------------------------------
# Tool rate limit config (lines 1501-1521)
# ---------------------------------------------------------------------------


class TestToolRateLimitConfig:
    def test_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        trl = config.safety.tool_rate_limit
        assert trl.max_calls_per_minute == 0
        assert trl.max_calls_per_conversation == 0
        assert trl.max_consecutive_failures == 5
        assert trl.action == "block"

    def test_custom_values_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "tool_rate_limit": {
                        "max_calls_per_minute": 60,
                        "max_calls_per_conversation": 500,
                        "max_consecutive_failures": 3,
                        "action": "warn",
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        trl = config.safety.tool_rate_limit
        assert trl.max_calls_per_minute == 60
        assert trl.max_calls_per_conversation == 500
        assert trl.max_consecutive_failures == 3
        assert trl.action == "warn"

    def test_invalid_action_falls_back_to_block(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"tool_rate_limit": {"action": "garbage"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.tool_rate_limit.action == "block"

    def test_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"tool_rate_limit": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.tool_rate_limit.max_calls_per_minute == 0


# ---------------------------------------------------------------------------
# DLP config (lines 1523-1572)
# ---------------------------------------------------------------------------


class TestDlpConfig:
    def test_dlp_disabled_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.dlp.enabled is False

    def test_dlp_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_DLP_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.dlp.enabled is True

    def test_dlp_action_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_DLP_ACTION", "block")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.dlp.action == "block"

    def test_dlp_action_invalid_falls_back_to_redact(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_DLP_ACTION", "garbage")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.dlp.action == "redact"

    def test_dlp_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "dlp": {
                        "enabled": True,
                        "scan_output": False,
                        "scan_input": True,
                        "action": "warn",
                        "redaction_string": "[BLOCKED]",
                        "log_detections": False,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        dlp = config.safety.dlp
        assert dlp.enabled is True
        assert dlp.scan_output is False
        assert dlp.scan_input is True
        assert dlp.action == "warn"
        assert dlp.redaction_string == "[BLOCKED]"
        assert dlp.log_detections is False

    def test_dlp_patterns_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "dlp": {
                        "patterns": [
                            {"name": "ssn", "pattern": r"\d{3}-\d{2}-\d{4}", "description": "Social Security"},
                        ]
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert len(config.safety.dlp.patterns) == 1
        assert config.safety.dlp.patterns[0].name == "ssn"

    def test_dlp_invalid_patterns_skipped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "dlp": {
                        "patterns": [
                            {"name": "valid", "pattern": r"\d+"},
                            {"name": "", "pattern": r"\d+"},  # missing name
                            {"name": "nopat"},  # missing pattern
                            "notadict",
                        ]
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert len(config.safety.dlp.patterns) == 1

    def test_dlp_custom_patterns_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "dlp": {
                        "custom_patterns": [
                            {"name": "employee-id", "pattern": r"EMP\d{6}"},
                        ]
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert len(config.safety.dlp.custom_patterns) == 1
        assert config.safety.dlp.custom_patterns[0].name == "employee-id"

    def test_dlp_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"dlp": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.dlp.enabled is False


# ---------------------------------------------------------------------------
# Output filter config (lines 1574-1614)
# ---------------------------------------------------------------------------


class TestOutputFilterConfig:
    def test_output_filter_disabled_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.output_filter.enabled is False

    def test_output_filter_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_OUTPUT_FILTER_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.output_filter.enabled is True

    def test_output_filter_action_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_OUTPUT_FILTER_ACTION", "block")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.output_filter.action == "block"

    def test_output_filter_action_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_OUTPUT_FILTER_ACTION", "garbage")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.safety.output_filter.action == "warn"

    def test_output_filter_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "output_filter": {
                        "enabled": True,
                        "system_prompt_leak_detection": False,
                        "leak_threshold": 0.7,
                        "action": "redact",
                        "redaction_string": "[REMOVED]",
                        "log_detections": False,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        of = config.safety.output_filter
        assert of.enabled is True
        assert of.system_prompt_leak_detection is False
        assert of.leak_threshold == 0.7
        assert of.action == "redact"
        assert of.redaction_string == "[REMOVED]"
        assert of.log_detections is False

    def test_output_filter_leak_threshold_clamped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"output_filter": {"leak_threshold": 999.0}},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.output_filter.leak_threshold == 1.0

    def test_output_filter_leak_threshold_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"output_filter": {"leak_threshold": "bad"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.output_filter.leak_threshold == 0.4

    def test_output_filter_custom_patterns(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {
                    "output_filter": {
                        "custom_patterns": [
                            {"name": "secret-key", "pattern": r"sk-[a-z0-9]{32}"},
                        ]
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert len(config.safety.output_filter.custom_patterns) == 1
        assert config.safety.output_filter.custom_patterns[0].name == "secret-key"

    def test_output_filter_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "safety": {"output_filter": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.safety.output_filter.enabled is False


# ---------------------------------------------------------------------------
# RAG config (lines 1634-1670)
# ---------------------------------------------------------------------------


class TestRagConfig:
    def test_rag_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.enabled is True
        assert config.rag.max_chunks == 10
        assert config.rag.max_tokens == 2000
        assert config.rag.similarity_threshold == 0.5

    def test_rag_enabled_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_ENABLED", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.enabled is False

    def test_rag_max_chunks_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_MAX_CHUNKS", "20")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.max_chunks == 20

    def test_rag_max_chunks_clamped_max(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_MAX_CHUNKS", "999")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.max_chunks == 50

    def test_rag_max_chunks_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_MAX_CHUNKS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.max_chunks == 10

    def test_rag_max_tokens_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_MAX_TOKENS", "5000")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.max_tokens == 5000

    def test_rag_max_tokens_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_MAX_TOKENS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.max_tokens == 2000

    def test_rag_similarity_threshold_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_SIMILARITY_THRESHOLD", "0.8")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.similarity_threshold == 0.8

    def test_rag_similarity_threshold_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_SIMILARITY_THRESHOLD", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.similarity_threshold == 0.5

    def test_rag_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "rag": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)

    def test_rag_include_exclude_flags(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "rag": {"include_sources": False, "include_conversations": False, "exclude_current": False},
            },
        )
        config, _ = load_config(cfg)
        assert config.rag.include_sources is False
        assert config.rag.include_conversations is False
        assert config.rag.exclude_current is False

    def test_rag_retrieval_mode_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.retrieval_mode == "dense"

    def test_rag_retrieval_mode_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "rag": {"retrieval_mode": "hybrid"},
            },
        )
        config, _ = load_config(cfg)
        assert config.rag.retrieval_mode == "hybrid"

    def test_rag_retrieval_mode_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_RETRIEVAL_MODE", "keyword")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.retrieval_mode == "keyword"

    def test_rag_retrieval_mode_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "rag": {"retrieval_mode": "bogus"},
            },
        )
        config, _ = load_config(cfg)
        assert config.rag.retrieval_mode == "dense"

    def test_rag_show_status_default_true(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.show_status is True

    def test_rag_show_status_yaml_false(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "rag": {"show_status": False},
            },
        )
        config, _ = load_config(cfg)
        assert config.rag.show_status is False

    def test_rag_show_status_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RAG_SHOW_STATUS", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rag.show_status is False


# ---------------------------------------------------------------------------
# Reranker config
# ---------------------------------------------------------------------------


class TestRerankerConfig:
    def test_reranker_auto_detect_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.reranker.enabled is None

    def test_reranker_enabled_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"enabled": True, "model": "custom/model", "top_k": 10},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.enabled is True
        assert config.reranker.model == "custom/model"
        assert config.reranker.top_k == 10

    def test_reranker_disabled_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"enabled": False},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.enabled is False

    def test_reranker_env_var_enabled(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RERANKER_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.reranker.enabled is True

    def test_reranker_top_k_clamped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"top_k": 100},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.top_k == 50  # clamped to max

    def test_reranker_score_threshold_not_clamped(self, tmp_path: Path) -> None:
        """Cross-encoder scores are unbounded logits; threshold must not be clamped."""
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"score_threshold": 5.0},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.score_threshold == 5.0

    def test_reranker_negative_score_threshold(self, tmp_path: Path) -> None:
        """Negative thresholds are valid for cross-encoder logits."""
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"score_threshold": -2.5},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.score_threshold == -2.5

    def test_reranker_invalid_provider_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"provider": "bogus"},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.provider == "local"

    def test_reranker_candidate_multiplier_clamped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"candidate_multiplier": 50},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.candidate_multiplier == 10

    def test_reranker_cache_dir_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "reranker": {"cache_dir": "/vendored/reranker"},
            },
        )
        config, _ = load_config(cfg)
        assert config.reranker.cache_dir == "/vendored/reranker"

    def test_reranker_cache_dir_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RERANKER_CACHE_DIR", "/env/reranker")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.reranker.cache_dir == "/env/reranker"

    def test_reranker_cache_dir_default_empty(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.reranker.cache_dir == ""


# ---------------------------------------------------------------------------
# Embeddings cache_dir config
# ---------------------------------------------------------------------------


class TestEmbeddingsCacheDirConfig:
    def test_embeddings_cache_dir_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "embeddings": {"cache_dir": "/vendored/embeddings"},
            },
        )
        config, _ = load_config(cfg)
        assert config.embeddings.cache_dir == "/vendored/embeddings"

    def test_embeddings_cache_dir_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_EMBEDDINGS_CACHE_DIR", "/env/embeddings")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.embeddings.cache_dir == "/env/embeddings"

    def test_embeddings_cache_dir_default_empty(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.embeddings.cache_dir == ""


# ---------------------------------------------------------------------------
# Proxy config (lines 1672-1694)
# ---------------------------------------------------------------------------


class TestProxyConfig:
    def test_proxy_disabled_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.proxy.enabled is False

    def test_proxy_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_PROXY_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.proxy.enabled is True

    def test_proxy_allowed_origins_valid(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "proxy": {
                    "enabled": True,
                    "allowed_origins": ["https://app.example.com", "https://other.example.com"],
                },
            },
        )
        config, _ = load_config(cfg)
        assert "https://app.example.com" in config.proxy.allowed_origins
        assert "https://other.example.com" in config.proxy.allowed_origins

    def test_proxy_wildcard_origin_rejected(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "proxy": {"enabled": True, "allowed_origins": ["*", "https://valid.example.com"]},
            },
        )
        config, _ = load_config(cfg)
        assert "*" not in config.proxy.allowed_origins
        assert "https://valid.example.com" in config.proxy.allowed_origins

    def test_proxy_non_http_origin_rejected(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "proxy": {"allowed_origins": ["ftp://bad.example.com", "https://good.example.com"]},
            },
        )
        config, _ = load_config(cfg)
        assert "ftp://bad.example.com" not in config.proxy.allowed_origins

    def test_proxy_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "proxy": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)

    def test_proxy_origins_not_a_list_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "proxy": {"allowed_origins": "notalist"},
            },
        )
        config, _ = load_config(cfg)
        assert config.proxy.allowed_origins == []


# ---------------------------------------------------------------------------
# Storage config (lines 1706-1743)
# ---------------------------------------------------------------------------


class TestStorageConfig:
    def test_storage_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.retention_days == 0
        assert config.storage.encrypt_at_rest is False

    def test_storage_retention_days_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_RETENTION_DAYS", "90")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.retention_days == 90

    def test_storage_retention_days_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_RETENTION_DAYS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.retention_days == 0

    def test_storage_check_interval_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_CHECK_INTERVAL", "7200")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.retention_check_interval == 7200

    def test_storage_check_interval_clamped_min(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_CHECK_INTERVAL", "10")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.retention_check_interval == 60

    def test_storage_purge_attachments_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_PURGE_ATTACHMENTS", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.purge_attachments is False

    def test_storage_purge_embeddings_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_PURGE_EMBEDDINGS", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.purge_embeddings is False

    def test_storage_encrypt_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_STORAGE_ENCRYPT", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.storage.encrypt_at_rest is True

    def test_storage_encryption_kdf_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "storage": {"encryption_kdf": "md5-oops"},
            },
        )
        config, _ = load_config(cfg)
        assert config.storage.encryption_kdf == "hkdf-sha256"

    def test_storage_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "storage": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)


# ---------------------------------------------------------------------------
# Session config (lines 1745-1801)
# ---------------------------------------------------------------------------


class TestSessionConfig:
    def test_session_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.store == "memory"
        assert config.session.max_concurrent_sessions == 0
        assert config.session.idle_timeout == 1800
        assert config.session.absolute_timeout == 43200

    def test_session_store_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_STORE", "sqlite")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.store == "sqlite"

    def test_session_store_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_STORE", "redis")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.store == "memory"

    def test_session_max_concurrent_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_MAX_CONCURRENT", "5")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.max_concurrent_sessions == 5

    def test_session_max_concurrent_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_MAX_CONCURRENT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.max_concurrent_sessions == 0

    def test_session_idle_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_IDLE_TIMEOUT", "3600")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.idle_timeout == 3600

    def test_session_idle_timeout_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_IDLE_TIMEOUT", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.idle_timeout == 1800

    def test_session_absolute_timeout_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_ABSOLUTE_TIMEOUT", "86400")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.session.absolute_timeout == 86400

    def test_session_allowed_ips_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_ALLOWED_IPS", "192.168.1.0/24,10.0.0.1")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert "192.168.1.0/24" in config.session.allowed_ips
        assert "10.0.0.1" in config.session.allowed_ips

    def test_session_allowed_ips_yaml_takes_precedence_over_env(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("AI_CHAT_SESSION_ALLOWED_IPS", "10.0.0.1")
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "session": {"allowed_ips": ["192.168.1.1"]},
            },
        )
        config, _ = load_config(cfg)
        assert "192.168.1.1" in config.session.allowed_ips
        assert "10.0.0.1" not in config.session.allowed_ips

    def test_session_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "session": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)


# ---------------------------------------------------------------------------
# Audit config (lines 1803-1846)
# ---------------------------------------------------------------------------


class TestAuditConfig:
    def test_audit_disabled_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.enabled is False

    def test_audit_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.enabled is True

    def test_audit_log_path_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_LOG_PATH", "/var/log/anteroom/audit.jsonl")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.log_path == "/var/log/anteroom/audit.jsonl"

    def test_audit_tamper_protection_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_TAMPER_PROTECTION", "none")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.tamper_protection == "none"

    def test_audit_tamper_protection_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_TAMPER_PROTECTION", "sha256")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.tamper_protection == "hmac"

    def test_audit_rotation_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {"rotation": "weekly"},
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.rotation == "daily"

    def test_audit_rotate_size_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {"rotate_size_bytes": 20_000_000},
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.rotate_size_bytes == 20_000_000

    def test_audit_rotate_size_clamped_min(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {"rotate_size_bytes": 100},
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.rotate_size_bytes == 1_048_576

    def test_audit_rotate_size_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {"rotate_size_bytes": "bad"},
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.rotate_size_bytes == 10_485_760

    def test_audit_retention_days_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_RETENTION_DAYS", "30")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.retention_days == 30

    def test_audit_retention_days_invalid_falls_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_RETENTION_DAYS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.retention_days == 90

    def test_audit_redact_content_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_AUDIT_REDACT_CONTENT", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.audit.redact_content is False

    def test_audit_events_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {
                    "events": {
                        "auth": False,
                        "tool_calls": True,
                        "dlp": False,
                        "output_filter": True,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.events["auth"] is False
        assert config.audit.events["tool_calls"] is True
        assert config.audit.events["dlp"] is False

    def test_audit_events_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {"events": "notadict"},
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.events["auth"] is True

    def test_audit_events_workflow_memory_subagent_governable(self, tmp_path: Path) -> None:
        """Operators must be able to disable workflow/memory/subagent categories via YAML (#1459)."""
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "audit": {
                    "events": {
                        "workflow": False,
                        "memory": False,
                        "subagent": False,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        assert config.audit.events["workflow"] is False
        assert config.audit.events["memory"] is False
        assert config.audit.events["subagent"] is False
        # Defaults for unspecified categories
        assert config.audit.events["auth"] is True
        assert config.audit.events["tool_calls"] is True

    def test_audit_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "audit": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)


# ---------------------------------------------------------------------------
# Codebase index config (lines 1848-1864)
# ---------------------------------------------------------------------------


class TestCodebaseIndexConfig:
    def test_ci_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.codebase_index.enabled is True
        assert config.codebase_index.map_tokens == 1000

    def test_ci_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "codebase_index": {
                    "enabled": False,
                    "map_tokens": 500,
                    "languages": ["python", "javascript"],
                    "exclude_dirs": ["node_modules", ".git"],
                },
            },
        )
        config, _ = load_config(cfg)
        assert config.codebase_index.enabled is False
        assert config.codebase_index.map_tokens == 500
        assert "python" in config.codebase_index.languages
        assert "node_modules" in config.codebase_index.exclude_dirs

    def test_ci_languages_not_a_list_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "codebase_index": {"languages": "notalist"},
            },
        )
        config, _ = load_config(cfg)
        assert config.codebase_index.languages == []

    def test_ci_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "codebase_index": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)


# ---------------------------------------------------------------------------
# Memory promotion config (#920)
# ---------------------------------------------------------------------------


class TestMemoryPromotionConfig:
    def test_memory_promotion_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        p = config.memory.promotion
        assert p.default_review_state == "candidate"
        assert p.local_auto_approve is False
        assert p.agent_proposals_enabled is True
        assert p.max_lineage_entries == 50
        assert p.max_candidates_per_conversation == 10
        assert p.max_reject_reason_chars == 500

    def test_memory_promotion_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {
                    "promotion": {
                        "default_review_state": "pending_review",
                        "local_auto_approve": True,
                        "agent_proposals_enabled": False,
                        "max_lineage_entries": 25,
                        "max_candidates_per_conversation": 3,
                        "max_reject_reason_chars": 120,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        p = config.memory.promotion
        assert p.default_review_state == "pending_review"
        assert p.local_auto_approve is True
        assert p.agent_proposals_enabled is False
        assert p.max_lineage_entries == 25
        assert p.max_candidates_per_conversation == 3
        assert p.max_reject_reason_chars == 120

    def test_memory_promotion_invalid_review_state_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"promotion": {"default_review_state": "nope"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.memory.promotion.default_review_state == "candidate"

    def test_memory_promotion_local_auto_approve_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_LOCAL_AUTO_APPROVE", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.local_auto_approve is True

    def test_memory_promotion_local_auto_approve_env_var_false(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_LOCAL_AUTO_APPROVE", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.local_auto_approve is False

    def test_memory_promotion_agent_proposals_env_var_false(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_AGENT_PROPOSALS_ENABLED", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.agent_proposals_enabled is False

    def test_memory_promotion_max_candidates_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_MAX_CANDIDATES_PER_CONVERSATION", "4")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.max_candidates_per_conversation == 4

    def test_memory_promotion_max_lineage_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_MAX_LINEAGE_ENTRIES", "17")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.max_lineage_entries == 17

    def test_memory_promotion_max_reject_reason_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_MAX_REJECT_REASON_CHARS", "200")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.max_reject_reason_chars == 200

    def test_memory_promotion_max_candidates_invalid_falls_back(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_PROMOTION_MAX_CANDIDATES_PER_CONVERSATION", "garbage")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.promotion.max_candidates_per_conversation == 10

    def test_memory_promotion_zero_or_negative_caps_clamped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {
                    "promotion": {
                        "max_lineage_entries": 0,
                        "max_candidates_per_conversation": -5,
                        "max_reject_reason_chars": 0,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        p = config.memory.promotion
        # clamp is 1 (ensures the pipeline never runs with an un-bounded cap)
        assert p.max_lineage_entries == 1
        assert p.max_candidates_per_conversation == 1
        assert p.max_reject_reason_chars == 1


# ---------------------------------------------------------------------------
# Memory retention config (#625)
# ---------------------------------------------------------------------------


class TestMemoryRetentionConfig:
    def test_memory_retention_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        r = config.memory.retention
        assert r.enabled is False
        assert r.max_age_days is None
        assert r.idle_days is None
        assert r.min_age_days == 1
        assert r.purge_statuses == ["rejected"]
        assert r.respect_pins is True

    def test_memory_retention_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {
                    "retention": {
                        "enabled": True,
                        "max_age_days": 90,
                        "idle_days": 30,
                        "min_age_days": 3,
                        "purge_statuses": ["rejected", "archived"],
                        "respect_pins": False,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        r = config.memory.retention
        assert r.enabled is True
        assert r.max_age_days == 90
        assert r.idle_days == 30
        assert r.min_age_days == 3
        assert r.purge_statuses == ["rejected", "archived"]
        assert r.respect_pins is False

    def test_memory_retention_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_RETENTION_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.retention.enabled is True

    def test_memory_retention_max_age_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_RETENTION_MAX_AGE_DAYS", "120")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.retention.max_age_days == 120

    def test_memory_retention_idle_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_RETENTION_IDLE_DAYS", "45")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.retention.idle_days == 45

    def test_memory_retention_min_age_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_RETENTION_MIN_AGE_DAYS", "7")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.retention.min_age_days == 7

    def test_memory_retention_respect_pins_env_var_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_RETENTION_RESPECT_PINS", "false")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.retention.respect_pins is False

    def test_memory_retention_purge_statuses_env_var_csv(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_RETENTION_PURGE_STATUSES", "rejected,archived")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.retention.purge_statuses == ["rejected", "archived"]

    def test_memory_retention_invalid_max_age_falls_back_to_none(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"retention": {"max_age_days": "bad"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.memory.retention.max_age_days is None

    def test_memory_retention_zero_or_negative_max_age_disables(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"retention": {"max_age_days": 0}},
            },
        )
        config, _ = load_config(cfg)
        assert config.memory.retention.max_age_days is None

    def test_memory_retention_invalid_status_filtered_out(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"retention": {"purge_statuses": ["rejected", "deleted", "archived"]}},
            },
        )
        config, _ = load_config(cfg)
        # "deleted" is not a valid memory status — dropped; remaining pair kept.
        assert config.memory.retention.purge_statuses == ["rejected", "archived"]

    def test_memory_retention_empty_status_list_falls_back_to_default(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"retention": {"purge_statuses": []}},
            },
        )
        config, _ = load_config(cfg)
        assert config.memory.retention.purge_statuses == ["rejected"]


# ---------------------------------------------------------------------------
# Memory auto-propose config (#1454)
# ---------------------------------------------------------------------------


class TestMemoryAutoProposeConfig:
    def test_auto_propose_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        ap = config.memory.auto_propose
        assert ap.enabled is False
        assert ap.max_candidates_per_turn == 1
        assert ap.categories == ["preference", "project_fact", "decision", "workflow_hint"]
        assert ap.min_confidence == 0.8
        assert ap.notify_inline is True
        assert ap.cooldown_turns == 5

    def test_auto_propose_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {
                    "auto_propose": {
                        "enabled": True,
                        "max_candidates_per_turn": 3,
                        "categories": ["preference", "decision"],
                        "min_confidence": 0.5,
                        "notify_inline": False,
                        "cooldown_turns": 10,
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        ap = config.memory.auto_propose
        assert ap.enabled is True
        assert ap.max_candidates_per_turn == 3
        assert ap.categories == ["preference", "decision"]
        assert ap.min_confidence == 0.5
        assert ap.notify_inline is False
        assert ap.cooldown_turns == 10

    def test_auto_propose_enabled_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_AUTO_PROPOSE_ENABLED", "true")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.auto_propose.enabled is True

    def test_auto_propose_max_per_turn_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_AUTO_PROPOSE_MAX_CANDIDATES_PER_TURN", "4")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.auto_propose.max_candidates_per_turn == 4

    def test_auto_propose_min_confidence_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_AUTO_PROPOSE_MIN_CONFIDENCE", "0.65")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.auto_propose.min_confidence == 0.65

    def test_auto_propose_categories_env_var_csv(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_MEMORY_AUTO_PROPOSE_CATEGORIES", "preference,decision")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.memory.auto_propose.categories == ["preference", "decision"]

    def test_auto_propose_categories_invalid_filtered(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {
                    "auto_propose": {
                        "categories": ["preference", "garbage", "another_invalid"],
                    }
                },
            },
        )
        config, _ = load_config(cfg)
        # Invalid categories silently dropped; valid ones survive.
        assert config.memory.auto_propose.categories == ["preference"]

    def test_auto_propose_categories_all_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"auto_propose": {"categories": ["bogus"]}},
            },
        )
        config, _ = load_config(cfg)
        # All-invalid input falls back to the full default category list.
        assert config.memory.auto_propose.categories == [
            "preference",
            "project_fact",
            "decision",
            "workflow_hint",
        ]

    def test_auto_propose_min_confidence_clamped(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"auto_propose": {"min_confidence": 1.7}},
            },
        )
        config, _ = load_config(cfg)
        assert config.memory.auto_propose.min_confidence == 1.0

    def test_auto_propose_max_per_turn_clamped_to_one(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"auto_propose": {"max_candidates_per_turn": 0}},
            },
        )
        config, _ = load_config(cfg)
        # Floor of 1 — never run with zero cap (would still produce overhead).
        assert config.memory.auto_propose.max_candidates_per_turn == 1

    def test_auto_propose_invalid_min_confidence_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "memory": {"auto_propose": {"min_confidence": "garbage"}},
            },
        )
        config, _ = load_config(cfg)
        assert config.memory.auto_propose.min_confidence == 0.8


# ---------------------------------------------------------------------------
# Compliance config (lines 1866-1896)
# ---------------------------------------------------------------------------


class TestComplianceConfig:
    def test_compliance_empty_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.compliance.rules == []

    def test_compliance_rules_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "compliance": {
                    "rules": [
                        {"field": "safety.approval_mode", "must_be": "ask", "message": "Must use ask mode"},
                    ]
                },
            },
        )
        config, _ = load_config(cfg)
        assert len(config.compliance.rules) == 1
        assert config.compliance.rules[0].field == "safety.approval_mode"

    def test_compliance_rules_skip_invalid_entries(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "compliance": {
                    "rules": [
                        {"field": "valid.field", "must_be": "value"},
                        {"field": "", "must_be": "value"},  # empty field ignored
                        "notadict",  # not a dict, ignored
                    ]
                },
            },
        )
        config, _ = load_config(cfg)
        assert len(config.compliance.rules) == 1

    def test_compliance_must_match_compiled(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "compliance": {
                    "rules": [
                        {"field": "ai.model", "must_match": r"^gpt-4.*", "message": "Must use GPT-4"},
                    ]
                },
            },
        )
        config, _ = load_config(cfg)
        rule = config.compliance.rules[0]
        assert rule.must_match == r"^gpt-4.*"
        assert rule._compiled_pattern is not None

    def test_compliance_invalid_regex_compiled_is_none(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "compliance": {
                    "rules": [
                        {"field": "ai.model", "must_match": r"[invalid", "message": "Bad regex"},
                    ]
                },
            },
        )
        config, _ = load_config(cfg)
        rule = config.compliance.rules[0]
        assert rule._compiled_pattern is None

    def test_compliance_not_a_dict_rejected_by_validator(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "compliance": "notadict"},
        )
        with pytest.raises(ValueError, match="expected dict"):
            load_config(cfg)


# ---------------------------------------------------------------------------
# Pack sources config (lines 1898-1918)
# ---------------------------------------------------------------------------


class TestPackSourcesConfig:
    def test_pack_sources_empty_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.pack_sources == []

    def test_pack_sources_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "pack_sources": [
                    {"url": "https://github.com/org/packs.git", "branch": "main", "refresh_interval": 60},
                ],
            },
        )
        config, _ = load_config(cfg)
        assert len(config.pack_sources) == 1
        assert config.pack_sources[0].url == "https://github.com/org/packs.git"
        assert config.pack_sources[0].branch == "main"
        assert config.pack_sources[0].refresh_interval == 60

    def test_pack_sources_skips_entries_without_url(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "pack_sources": [
                    {"url": "https://github.com/org/packs.git"},
                    {"branch": "main"},  # no url
                    "notadict",
                ],
            },
        )
        config, _ = load_config(cfg)
        assert len(config.pack_sources) == 1

    def test_pack_sources_refresh_interval_invalid_falls_back(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "pack_sources": [{"url": "https://github.com/org/packs.git", "refresh_interval": "bad"}],
            },
        )
        config, _ = load_config(cfg)
        assert config.pack_sources[0].refresh_interval == 30

    def test_pack_sources_not_a_list_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "pack_sources": "notalist",
            },
        )
        config, _ = load_config(cfg)
        assert config.pack_sources == []


# ---------------------------------------------------------------------------
# References config (lines 1696-1704)
# ---------------------------------------------------------------------------


class TestReferencesConfig:
    def test_references_empty_by_default(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.references.instructions == []
        assert config.references.rules == []
        assert config.references.skills == []

    def test_references_from_yaml(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "references": {
                    "instructions": ["/path/to/instructions.md"],
                    "rules": ["/path/to/rules.md"],
                    "skills": ["/path/to/skills.yaml"],
                },
            },
        )
        config, _ = load_config(cfg)
        assert "/path/to/instructions.md" in config.references.instructions
        assert "/path/to/rules.md" in config.references.rules
        assert "/path/to/skills.yaml" in config.references.skills

    def test_references_non_string_entries_ignored(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {
                "ai": {"base_url": "http://t", "api_key": "k"},
                "references": {
                    "instructions": ["valid.md", 123, None, ""],
                },
            },
        )
        config, _ = load_config(cfg)
        # Non-string entries filtered; surviving path resolved to absolute
        assert len(config.references.instructions) == 1
        assert Path(config.references.instructions[0]).is_absolute()

    def test_references_not_a_dict_uses_defaults(self, tmp_path: Path) -> None:
        cfg = _write_config(
            tmp_path,
            {"ai": {"base_url": "http://t", "api_key": "k"}, "references": "notadict"},
        )
        config, _ = load_config(cfg)
        assert config.references.instructions == []


# ---------------------------------------------------------------------------
# Space config layer in load_config (lines 861-864)
# ---------------------------------------------------------------------------


class TestSpaceConfigLayer:
    def test_space_config_overlays_raw(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        space_config = {"safety": {"approval_mode": "auto"}}
        config, _ = load_config(cfg, space_config=space_config)
        assert config.safety.approval_mode == "auto"

    def test_space_config_none_ignored(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg, space_config=None)
        assert isinstance(config, AppConfig)

    def test_space_config_not_dict_ignored(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg, space_config="notadict")  # type: ignore[arg-type]
        assert isinstance(config, AppConfig)


# ---------------------------------------------------------------------------
# api_key_command fallback (no api_key but has api_key_command)
# ---------------------------------------------------------------------------


class TestApiKeyCommand:
    def test_api_key_command_accepted_without_api_key(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AI_CHAT_API_KEY", raising=False)
        cfg = _write_config(
            tmp_path,
            {
                "ai": {
                    "base_url": "https://api.example.com",
                    "api_key_command": "echo sk-from-cmd",
                }
            },
        )
        config, _ = load_config(cfg)
        assert config.ai.api_key_command == "echo sk-from-cmd"
        assert config.ai.api_key == ""

    def test_api_key_command_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_API_KEY_COMMAND", "vault read secret/key")
        monkeypatch.delenv("AI_CHAT_API_KEY", raising=False)
        cfg = _write_config(tmp_path, {"ai": {"base_url": "https://api.example.com"}})
        config, _ = load_config(cfg)
        assert config.ai.api_key_command == "vault read secret/key"


class TestServerConfig:
    def test_server_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.server.max_upload_mb == 50

    def test_server_max_upload_mb_from_yaml(self, tmp_path: Path) -> None:
        raw = {"ai": {"base_url": "http://t", "api_key": "k"}, "server": {"max_upload_mb": 200}}
        cfg = _write_config(tmp_path, raw)
        config, _ = load_config(cfg)
        assert config.server.max_upload_mb == 200

    def test_server_max_upload_mb_from_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = _minimal(tmp_path)
        monkeypatch.setenv("AI_CHAT_SERVER_MAX_UPLOAD_MB", "100")
        config, _ = load_config(cfg)
        assert config.server.max_upload_mb == 100

    def test_server_max_upload_mb_clamped_to_minimum(self, tmp_path: Path) -> None:
        raw = {"ai": {"base_url": "http://t", "api_key": "k"}, "server": {"max_upload_mb": 0}}
        cfg = _write_config(tmp_path, raw)
        config, _ = load_config(cfg)
        assert config.server.max_upload_mb == 1

    def test_server_max_upload_mb_clamped_to_maximum(self, tmp_path: Path) -> None:
        raw = {"ai": {"base_url": "http://t", "api_key": "k"}, "server": {"max_upload_mb": 9999}}
        cfg = _write_config(tmp_path, raw)
        config, _ = load_config(cfg)
        assert config.server.max_upload_mb == 1000

    def test_server_max_upload_mb_invalid_falls_back(self, tmp_path: Path) -> None:
        raw = {"ai": {"base_url": "http://t", "api_key": "k"}, "server": {"max_upload_mb": "notanint"}}
        cfg = _write_config(tmp_path, raw)
        config, _ = load_config(cfg)
        assert config.server.max_upload_mb == 50


class TestRateLimitConfig:
    def test_rate_limit_defaults(self, tmp_path: Path) -> None:
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rate_limit.max_requests == 120
        assert config.rate_limit.window_seconds == 60
        assert config.rate_limit.exempt_paths == ["/api/events"]
        assert config.rate_limit.sse_retry_ms == 5000

    def test_rate_limit_from_yaml(self, tmp_path: Path) -> None:
        cfg = _minimal(
            tmp_path,
            extra={
                "rate_limit": {
                    "max_requests": 60,
                    "window_seconds": 30,
                    "exempt_paths": ["/api/events", "/health"],
                    "sse_retry_ms": 10000,
                }
            },
        )
        config, _ = load_config(cfg)
        assert config.rate_limit.max_requests == 60
        assert config.rate_limit.window_seconds == 30
        assert config.rate_limit.exempt_paths == ["/api/events", "/health"]
        assert config.rate_limit.sse_retry_ms == 10000

    def test_rate_limit_env_vars(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_MAX_REQUESTS", "200")
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_WINDOW_SECONDS", "120")
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_SSE_RETRY_MS", "8000")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rate_limit.max_requests == 200
        assert config.rate_limit.window_seconds == 120
        assert config.rate_limit.sse_retry_ms == 8000

    def test_rate_limit_exempt_paths_env_var(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_EXEMPT_PATHS", "/api/events,/health")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rate_limit.exempt_paths == ["/api/events", "/health"]

    def test_rate_limit_invalid_values_fall_back(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_MAX_REQUESTS", "bad")
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_WINDOW_SECONDS", "bad")
        monkeypatch.setenv("AI_CHAT_RATE_LIMIT_SSE_RETRY_MS", "bad")
        cfg = _minimal(tmp_path)
        config, _ = load_config(cfg)
        assert config.rate_limit.max_requests == 120
        assert config.rate_limit.window_seconds == 60
        assert config.rate_limit.sse_retry_ms == 5000

    def test_rate_limit_clamped_to_minimum(self, tmp_path: Path) -> None:
        cfg = _minimal(
            tmp_path,
            extra={
                "rate_limit": {
                    "max_requests": 0,
                    "window_seconds": -5,
                    "sse_retry_ms": 10,
                }
            },
        )
        config, _ = load_config(cfg)
        assert config.rate_limit.max_requests >= 1
        assert config.rate_limit.window_seconds >= 1
        assert config.rate_limit.sse_retry_ms >= 100
