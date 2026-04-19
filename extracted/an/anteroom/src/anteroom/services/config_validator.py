"""Config validation: type-check, range-check, and error collection for YAML configs.

Validates raw YAML dicts against the known config schema before they are
parsed into dataclass objects.  Collects all errors rather than failing on
the first, so users can fix everything in one pass.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ConfigError:
    """A single config validation error."""

    path: str  # dot-separated config path (e.g. "ai.request_timeout")
    message: str
    severity: str = "error"  # "error" or "warning"

    def __str__(self) -> str:
        prefix = "warning" if self.severity == "warning" else "error"
        return f"[{prefix}] {self.path}: {self.message}"


@dataclass
class ValidationResult:
    """Result of validating a config dict."""

    errors: list[ConfigError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not any(e.severity == "error" for e in self.errors)

    @property
    def has_warnings(self) -> bool:
        return any(e.severity == "warning" for e in self.errors)

    def format_errors(self) -> str:
        if not self.errors:
            return ""
        lines = []
        errs = [e for e in self.errors if e.severity == "error"]
        warns = [e for e in self.errors if e.severity == "warning"]
        if errs:
            lines.append(f"{len(errs)} config error(s):")
            for e in errs:
                lines.append(f"  - {e.path}: {e.message}")
        if warns:
            lines.append(f"{len(warns)} config warning(s):")
            for w in warns:
                lines.append(f"  - {w.path}: {w.message}")
        return "\n".join(lines)


# Schema definition: maps dot-paths to their expected types and constraints.
# Each entry is (type, min, max, allowed_values, required).
# None means "no constraint" for that field.

_BOOL_VALUES = {"true", "false", "0", "1", "yes", "no"}

# Known top-level keys
_KNOWN_TOP_LEVEL = {
    "ai",
    "app",
    "mcp_servers",
    "mcp_tool_warning_threshold",
    "shared_databases",
    "databases",
    "cli",
    "identity",
    "embeddings",
    "safety",
    "proxy",
    "team_config_path",
    "enforce",
    "required",
    "references",
    "storage",
    "rag",
    "reranker",
    "codebase_index",
    "session",
    "rate_limit",
    "audit",
    "memory",
    "compliance",
    "trusted_proxy",
    "workflow",
    "pack_sources",
}

# Known keys per section
_KNOWN_KEYS: dict[str, set[str]] = {
    "ai": {
        "base_url",
        "api_key",
        "model",
        "system_prompt",
        "verify_ssl",
        "api_key_command",
        "request_timeout",
        "connect_timeout",
        "write_timeout",
        "pool_timeout",
        "first_token_timeout",
        "chunk_stall_timeout",
        "retry_max_attempts",
        "retry_backoff_base",
        "narration_cadence",
        "max_tools",
        "temperature",
        "top_p",
        "seed",
        "allowed_domains",
        "allowed_models",
        "block_localhost_api",
        "provider",
        "max_output_tokens",
        "model_family_aliases",
    },
    "app": {"host", "port", "data_dir", "tls"},
    "cli": {
        "builtin_tools",
        "max_tool_iterations",
        "context_warn_tokens",
        "context_auto_compact_tokens",
        # Legacy key — accepted as a deprecated alias for compaction.preserve_tail.
        "compact_preserve_tail",
        "tool_dedup",
        "retry_delay",
        "max_retries",
        "esc_hint_delay",
        "stall_display_threshold",
        "stall_warning_threshold",
        "stall_throughput_threshold",
        "tool_output_max_chars",
        "tool_replay_max_chars",
        "file_reference_max_chars",
        "model_context_window",
        "planning",
        "usage",
    },
    "cli.planning": {"enabled", "auto_threshold_tools", "auto_mode"},
    "cli.usage": {"week_days", "month_days", "model_costs", "budgets"},
    "cli.usage.budgets": {
        "enabled",
        "max_tokens_per_request",
        "max_tokens_per_conversation",
        "max_tokens_per_day",
        "warn_threshold_percent",
        "action_on_exceed",
    },
    "embeddings": {
        "enabled",
        "provider",
        "model",
        "dimensions",
        "local_model",
        "base_url",
        "api_key",
        "api_key_command",
        "cache_dir",
    },
    "safety": {
        "enabled",
        "approval_mode",
        "approval_timeout",
        "bash",
        "write_file",
        "custom_patterns",
        "sensitive_paths",
        "allowed_tools",
        "denied_tools",
        "tool_tiers",
        "read_only",
        "subagent",
        "tool_rate_limit",
        "dlp",
        "prompt_injection",
        "output_filter",
        "bypass_immune_paths",
    },
    "safety.dlp": {
        "enabled",
        "scan_output",
        "scan_input",
        "action",
        "patterns",
        "custom_patterns",
        "redaction_string",
        "log_detections",
    },
    "safety.prompt_injection": {
        "enabled",
        "action",
        "canary_length",
        "detect_encoding_attacks",
        "detect_instruction_override",
        "heuristic_threshold",
        "log_detections",
    },
    "safety.output_filter": {
        "enabled",
        "system_prompt_leak_detection",
        "leak_threshold",
        "custom_patterns",
        "action",
        "redaction_string",
        "log_detections",
    },
    "safety.tool_rate_limit": {
        "max_calls_per_minute",
        "max_calls_per_conversation",
        "max_consecutive_failures",
        "action",
    },
    "safety.subagent": {
        "max_concurrent",
        "max_total",
        "max_depth",
        "max_iterations",
        "timeout",
        "max_output_chars",
        "max_prompt_chars",
    },
    "workflow": {
        "enabled",
        "approval_mode",
        "max_review_rounds",
        "max_iterations",
        "step_timeout",
        "heartbeat_interval",
        "stale_threshold",
        "approval_timeout",
        "registry_enabled",
        "registry_heartbeat_interval",
        "budget",
        "credentials",
        "executor_enabled",
        "executor_poll_interval",
        "max_concurrent_runs",
        "scheduler_enabled",
        "min_schedule_interval",
        "watch_buffer_lines",
        "transcript",
    },
    "workflow.budget": {
        "max_duration_seconds",
        "max_steps",
        "max_tokens",
    },
    "workflow.transcript": {
        "enabled",
        "max_assistant_chars",
        "max_tool_output_chars",
        "max_stdout_chars",
        "max_stderr_chars",
    },
    "proxy": {"enabled", "allowed_origins"},
    "storage": {
        "retention_days",
        "retention_check_interval",
        "purge_attachments",
        "purge_embeddings",
        "encrypt_at_rest",
        "encryption_kdf",
    },
    "identity": {"user_id", "display_name", "public_key", "private_key"},
    "references": {"instructions", "rules", "skills"},
    "compaction": {
        "preserve_tail",
        "compact_rehydrate",
        "compact_rehydrate_max_files",
        "compact_rehydrate_max_errors",
    },
    "rag": {
        "enabled",
        "max_chunks",
        "max_tokens",
        "similarity_threshold",
        "include_sources",
        "include_conversations",
        "exclude_current",
        "retrieval_mode",
    },
    "reranker": {
        "enabled",
        "provider",
        "model",
        "top_k",
        "score_threshold",
        "candidate_multiplier",
        "cache_dir",
    },
    "codebase_index": {"enabled", "map_tokens", "languages", "exclude_dirs"},
    "session": {
        "store",
        "max_concurrent_sessions",
        "idle_timeout",
        "absolute_timeout",
        "allowed_ips",
        "log_session_events",
    },
    "audit": {
        "enabled",
        "log_path",
        "tamper_protection",
        "rotation",
        "rotate_size_bytes",
        "retention_days",
        "redact_content",
        "events",
    },
    "compliance": {"rules"},
    "memory": {"promotion", "retention"},
    "trusted_proxy": {"enabled", "trusted_cidrs", "header"},
}

# Int fields: (section_path, key, min, max, default)
_INT_FIELDS: list[tuple[str, str, int, int, int]] = [
    ("ai", "request_timeout", 10, 600, 120),
    ("ai", "connect_timeout", 1, 30, 5),
    ("ai", "write_timeout", 5, 120, 30),
    ("ai", "pool_timeout", 1, 60, 10),
    ("ai", "first_token_timeout", 5, 120, 30),
    ("ai", "chunk_stall_timeout", 10, 600, 30),
    ("ai", "retry_max_attempts", 0, 10, 3),
    ("ai", "narration_cadence", 0, 100, 8),
    ("ai", "max_tools", 0, 1000, 128),
    ("app", "port", 1, 65535, 8080),
    ("cli", "max_tool_iterations", 1, 200, 50),
    ("cli", "context_warn_tokens", 1000, 1_000_000, 80_000),
    ("cli", "context_auto_compact_tokens", 1000, 1_000_000, 100_000),
    ("cli", "max_retries", 0, 10, 3),
    ("compaction", "preserve_tail", 0, 200, 6),
    ("compaction", "compact_rehydrate_max_files", 0, 200, 20),
    ("compaction", "compact_rehydrate_max_errors", 0, 50, 5),
    ("cli", "tool_output_max_chars", 100, 100_000, 2000),
    ("cli", "tool_replay_max_chars", 100, 100_000, 2000),
    ("cli", "file_reference_max_chars", 1000, 10_000_000, 100_000),
    ("cli", "model_context_window", 1000, 2_000_000, 128_000),
    ("cli.planning", "auto_threshold_tools", 0, 200, 15),
    ("cli.usage", "week_days", 1, 365, 7),
    ("cli.usage", "month_days", 1, 365, 30),
    ("cli.usage.budgets", "max_tokens_per_request", 0, 100_000_000, 0),
    ("cli.usage.budgets", "max_tokens_per_conversation", 0, 100_000_000, 0),
    ("cli.usage.budgets", "max_tokens_per_day", 0, 100_000_000, 0),
    ("cli.usage.budgets", "warn_threshold_percent", 0, 100, 80),
    ("safety", "approval_timeout", 10, 600, 120),
    ("safety.tool_rate_limit", "max_calls_per_minute", 0, 100_000, 0),
    ("safety.tool_rate_limit", "max_calls_per_conversation", 0, 100_000, 0),
    ("safety.tool_rate_limit", "max_consecutive_failures", 0, 1000, 5),
    ("safety.subagent", "max_concurrent", 1, 20, 5),
    ("safety.subagent", "max_total", 1, 50, 10),
    ("safety.subagent", "max_depth", 1, 10, 3),
    ("safety.subagent", "max_iterations", 1, 100, 15),
    ("safety.subagent", "timeout", 10, 600, 120),
    ("safety.subagent", "max_output_chars", 100, 100_000, 4000),
    ("safety.subagent", "max_prompt_chars", 100, 100_000, 32_000),
    ("storage", "retention_days", 0, 36500, 0),
    ("storage", "retention_check_interval", 60, 86400, 3600),
    ("safety.prompt_injection", "canary_length", 8, 64, 16),
    ("workflow", "max_review_rounds", 1, 100, 2),
    ("workflow", "max_iterations", 1, 100, 30),
    ("workflow", "step_timeout", 10, 3600, 300),
    ("workflow", "heartbeat_interval", 5, 300, 30),
    ("workflow", "stale_threshold", 10, 600, 60),
    ("workflow", "approval_timeout", 10, 3600, 300),
    ("workflow", "registry_heartbeat_interval", 5, 300, 30),
    ("workflow", "executor_poll_interval", 1, 60, 5),
    ("workflow", "max_concurrent_runs", 1, 20, 3),
    ("workflow", "min_schedule_interval", 60, 86400, 60),
    ("workflow", "watch_buffer_lines", 1, 1000, 50),
    ("workflow.budget", "max_duration_seconds", 0, 86400, 0),
    ("workflow.budget", "max_steps", 0, 10000, 0),
    ("workflow.budget", "max_tokens", 0, 100_000_000, 0),
    ("workflow.transcript", "max_assistant_chars", 0, 1_000_000, 4000),
    ("workflow.transcript", "max_tool_output_chars", 0, 1_000_000, 2000),
    ("workflow.transcript", "max_stdout_chars", 0, 1_000_000, 4000),
    ("workflow.transcript", "max_stderr_chars", 0, 1_000_000, 4000),
]

# Float fields: (section_path, key, min, max, default)
_FLOAT_FIELDS: list[tuple[str, str, float, float, float]] = [
    ("ai", "retry_backoff_base", 0.1, 30.0, 1.0),
    ("ai", "temperature", 0.0, 2.0, 1.0),
    ("ai", "top_p", 0.0, 1.0, 1.0),
    ("cli", "retry_delay", 1.0, 60.0, 5.0),
    ("cli", "esc_hint_delay", 0.0, 60.0, 8.0),
    ("cli", "stall_display_threshold", 1.0, 120.0, 5.0),
    ("cli", "stall_warning_threshold", 1.0, 300.0, 15.0),
    ("cli", "stall_throughput_threshold", 0.0, 1000.0, 30.0),
    ("safety.prompt_injection", "heuristic_threshold", 0.0, 1.0, 0.7),
]

# Enum fields: (section_path, key, allowed_values)
_ENUM_FIELDS: list[tuple[str, str, set[str]]] = [
    ("safety", "approval_mode", {"auto", "ask_for_dangerous", "ask_for_writes", "ask"}),
    ("workflow", "approval_mode", {"auto", "ask_for_dangerous", "ask_for_writes", "ask"}),
    ("cli.planning", "auto_mode", {"off", "suggest", "auto"}),
    ("cli.usage.budgets", "action_on_exceed", {"block", "warn"}),
    ("safety.tool_rate_limit", "action", {"block", "warn"}),
    ("safety.dlp", "action", {"redact", "block", "warn"}),
    ("safety.prompt_injection", "action", {"block", "warn", "log"}),
    ("safety.output_filter", "action", {"warn", "block", "redact"}),
    ("embeddings", "provider", {"local", "api"}),
    ("storage", "encryption_kdf", {"hkdf-sha256"}),
]

# MCP server known keys
_MCP_SERVER_KEYS = {
    "name",
    "transport",
    "command",
    "args",
    "url",
    "env",
    "timeout",
    "tools_include",
    "tools_exclude",
    "trust_level",
    "enabled",
}


def _get_section(raw: dict[str, Any], section_path: str) -> dict[str, Any] | None:
    """Navigate to a nested section by dot-path. Returns None if missing."""
    parts = section_path.split(".")
    current: Any = raw
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current if isinstance(current, dict) else None


def validate_config(raw: dict[str, Any]) -> ValidationResult:
    """Validate a raw config dict against the known schema.

    Returns a ValidationResult with all errors and warnings collected.
    Does not modify the input dict.
    """
    result = ValidationResult()

    if not isinstance(raw, dict):
        result.errors.append(ConfigError(path="<root>", message="config must be a YAML mapping"))
        return result

    # Check for unknown top-level keys
    for key in raw:
        if key not in _KNOWN_TOP_LEVEL:
            result.errors.append(
                ConfigError(
                    path=key,
                    message=f"unknown config key '{key}'",
                    severity="warning",
                )
            )

    # Check unknown keys within known sections
    for section_path, known_keys in _KNOWN_KEYS.items():
        section = _get_section(raw, section_path)
        if section is None:
            continue
        for key in section:
            if key not in known_keys:
                result.errors.append(
                    ConfigError(
                        path=f"{section_path}.{key}",
                        message=f"unknown config key '{key}'",
                        severity="warning",
                    )
                )

    # Validate section types
    _check_section_type(raw, "ai", dict, result)
    _check_section_type(raw, "app", dict, result)
    _check_section_type(raw, "cli", dict, result)
    _check_section_type(raw, "embeddings", dict, result)
    _check_section_type(raw, "safety", dict, result)
    _check_section_type(raw, "proxy", dict, result)
    _check_section_type(raw, "storage", dict, result)
    _check_section_type(raw, "identity", dict, result)
    _check_section_type(raw, "rag", dict, result)
    _check_section_type(raw, "reranker", dict, result)
    _check_section_type(raw, "codebase_index", dict, result)
    _check_section_type(raw, "session", dict, result)
    _check_section_type(raw, "audit", dict, result)
    _check_section_type(raw, "memory", dict, result)
    _check_section_type(raw, "compliance", dict, result)
    _check_section_type(raw, "trusted_proxy", dict, result)
    _check_section_type(raw, "mcp_servers", list, result)

    # Validate int fields
    for section_path, key, lo, hi, default in _INT_FIELDS:
        section = _get_section(raw, section_path)
        if section is None or key not in section:
            continue
        val = section[key]
        if not _is_numeric(val):
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"expected integer, got {type(val).__name__}: {val!r} (will use default {default})",
                    severity="warning",
                )
            )
            continue
        try:
            int_val = int(val)
        except (ValueError, TypeError):
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"cannot convert to integer: {val!r} (will use default {default})",
                    severity="warning",
                )
            )
            continue
        if int_val < lo or int_val > hi:
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"value {int_val} out of range [{lo}, {hi}] (will be clamped)",
                    severity="warning",
                )
            )

    # Validate float fields
    for section_path, key, lo, hi, default in _FLOAT_FIELDS:  # type: ignore[assignment]
        section = _get_section(raw, section_path)
        if section is None or key not in section:
            continue
        val = section[key]
        if not _is_numeric(val):
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"expected number, got {type(val).__name__}: {val!r} (will use default {default})",
                    severity="warning",
                )
            )
            continue
        try:
            float_val = float(val)
        except (ValueError, TypeError):
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"cannot convert to float: {val!r} (will use default {default})",
                    severity="warning",
                )
            )
            continue
        if float_val < lo or float_val > hi:
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"value {float_val} out of range [{lo}, {hi}] (will be clamped)",
                    severity="warning",
                )
            )

    # Validate enum fields
    for section_path, key, allowed in _ENUM_FIELDS:
        section = _get_section(raw, section_path)
        if section is None or key not in section:
            continue
        val = str(section[key]).lower().strip()
        if val not in allowed:
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"invalid value '{val}'; must be one of: {', '.join(sorted(allowed))} (will use default)",
                    severity="warning",
                )
            )

    # Validate bool fields
    for section_path, key in [
        ("ai", "verify_ssl"),
        ("ai", "block_localhost_api"),
        ("app", "tls"),
        ("cli", "builtin_tools"),
        ("cli", "tool_dedup"),
        ("cli.planning", "enabled"),
        ("embeddings", "enabled"),
        ("safety", "enabled"),
        ("safety", "read_only"),
        ("proxy", "enabled"),
        ("storage", "purge_attachments"),
        ("storage", "purge_embeddings"),
        ("storage", "encrypt_at_rest"),
        ("safety.prompt_injection", "enabled"),
        ("safety.prompt_injection", "detect_encoding_attacks"),
        ("safety.prompt_injection", "detect_instruction_override"),
        ("safety.prompt_injection", "log_detections"),
    ]:
        section = _get_section(raw, section_path)
        if section is None or key not in section:
            continue
        val = section[key]
        if isinstance(val, bool):
            continue
        if isinstance(val, str) and val.lower() in _BOOL_VALUES:
            continue
        if isinstance(val, int) and val in (0, 1):
            continue
        result.errors.append(
            ConfigError(
                path=f"{section_path}.{key}",
                message=f"expected boolean, got: {val!r}",
                severity="warning",
            )
        )

    # Validate list fields
    for section_path, key in [
        ("safety", "custom_patterns"),
        ("safety", "sensitive_paths"),
        ("safety", "allowed_tools"),
        ("safety", "denied_tools"),
        ("safety", "bypass_immune_paths"),
        ("proxy", "allowed_origins"),
        ("ai", "allowed_domains"),
        ("ai", "allowed_models"),
    ]:
        section = _get_section(raw, section_path)
        if section is None or key not in section:
            continue
        val = section[key]
        if not isinstance(val, list):
            result.errors.append(
                ConfigError(
                    path=f"{section_path}.{key}",
                    message=f"expected list, got {type(val).__name__} (will use empty list)",
                    severity="warning",
                )
            )

    # Validate trusted_proxy config
    tp_section = _get_section(raw, "trusted_proxy")
    if tp_section is not None:
        tp_enabled = tp_section.get("enabled")
        if tp_enabled is not None:
            if not isinstance(tp_enabled, bool):
                if not (isinstance(tp_enabled, str) and tp_enabled.lower() in _BOOL_VALUES):
                    if not (isinstance(tp_enabled, int) and tp_enabled in (0, 1)):
                        result.errors.append(
                            ConfigError(
                                path="trusted_proxy.enabled",
                                message=f"expected boolean, got: {tp_enabled!r}",
                                severity="warning",
                            )
                        )
        tp_cidrs = tp_section.get("trusted_cidrs")
        if tp_cidrs is not None:
            if not isinstance(tp_cidrs, list):
                result.errors.append(
                    ConfigError(
                        path="trusted_proxy.trusted_cidrs",
                        message=f"expected list, got {type(tp_cidrs).__name__}",
                    )
                )
            else:
                import ipaddress

                for i, entry in enumerate(tp_cidrs):
                    try:
                        ipaddress.ip_network(str(entry), strict=False)
                    except ValueError:
                        result.errors.append(
                            ConfigError(
                                path=f"trusted_proxy.trusted_cidrs[{i}]",
                                message=f"invalid CIDR: {entry!r}",
                            )
                        )
        tp_header = tp_section.get("header")
        if tp_header is not None:
            if not isinstance(tp_header, str) or not tp_header.strip():
                result.errors.append(
                    ConfigError(
                        path="trusted_proxy.header",
                        message="header must be a non-empty string",
                    )
                )

    # Validate mcp_servers entries
    mcp_servers = raw.get("mcp_servers")
    if isinstance(mcp_servers, list):
        for i, srv in enumerate(mcp_servers):
            prefix = f"mcp_servers[{i}]"
            if not isinstance(srv, dict):
                result.errors.append(
                    ConfigError(
                        path=prefix,
                        message="MCP server entry must be a mapping",
                    )
                )
                continue
            if "name" not in srv:
                result.errors.append(
                    ConfigError(
                        path=prefix,
                        message="MCP server entry missing required 'name' field",
                    )
                )
            # Items with enabled: false will be filtered out during parsing,
            # so skip transport/command/url checks.  Partial overlay entries
            # are also valid — they exist to overlay fields (like env vars)
            # onto a team-defined server via named-list merge.  We detect a
            # partial overlay when the entry has no explicit transport AND
            # no command AND no url — i.e. it only carries overlay fields.
            is_disabled = srv.get("enabled") is False
            is_partial_overlay = "transport" not in srv and not srv.get("command") and not srv.get("url")
            transport = srv.get("transport", "stdio")
            if transport not in ("stdio", "sse"):
                result.errors.append(
                    ConfigError(
                        path=f"{prefix}.transport",
                        message=f"invalid transport '{transport}'; must be 'stdio' or 'sse'",
                    )
                )
            if not is_disabled and not is_partial_overlay:
                if transport == "stdio" and not srv.get("command"):
                    result.errors.append(
                        ConfigError(
                            path=f"{prefix}.command",
                            message="stdio transport requires 'command' field",
                        )
                    )
                if transport == "sse" and not srv.get("url"):
                    result.errors.append(
                        ConfigError(
                            path=f"{prefix}.url",
                            message="sse transport requires 'url' field",
                        )
                    )
            for key in srv:
                if key not in _MCP_SERVER_KEYS:
                    result.errors.append(
                        ConfigError(
                            path=f"{prefix}.{key}",
                            message=f"unknown MCP server key '{key}'",
                            severity="warning",
                        )
                    )
            if srv.get("tools_include") and srv.get("tools_exclude"):
                result.errors.append(
                    ConfigError(
                        path=f"{prefix}",
                        message="cannot set both 'tools_include' and 'tools_exclude'; include takes precedence",
                        severity="warning",
                    )
                )
            trust = srv.get("trust_level")
            if trust is not None and trust not in ("trusted", "untrusted"):
                result.errors.append(
                    ConfigError(
                        path=f"{prefix}.trust_level",
                        message=f"invalid trust_level '{trust}'; must be 'trusted' or 'untrusted'",
                        severity="error",
                    )
                )

    # Validate workflow credentials
    workflow_section = _get_section(raw, "workflow")
    if workflow_section is not None:
        creds = workflow_section.get("credentials")
        if creds is not None:
            if not isinstance(creds, list):
                result.errors.append(
                    ConfigError(
                        path="workflow.credentials",
                        message=f"expected list, got {type(creds).__name__}",
                        severity="error",
                    )
                )
            else:
                for i, cred in enumerate(creds):
                    prefix = f"workflow.credentials[{i}]"
                    if not isinstance(cred, dict):
                        result.errors.append(ConfigError(path=prefix, message="credential entry must be a mapping"))
                        continue
                    if not cred.get("name"):
                        result.errors.append(
                            ConfigError(path=f"{prefix}.name", message="credential entry missing required 'name' field")
                        )
                    if not cred.get("env_var") and not cred.get("command"):
                        result.errors.append(
                            ConfigError(
                                path=prefix,
                                message="credential must have either 'env_var' or 'command'",
                                severity="warning",
                            )
                        )
                    if cred.get("env_var") and cred.get("command"):
                        result.errors.append(
                            ConfigError(
                                path=prefix,
                                message="credential should have only one of 'env_var' or 'command'",
                                severity="warning",
                            )
                        )

    # Validate proxy origins format
    proxy = raw.get("proxy", {})
    if isinstance(proxy, dict):
        origins = proxy.get("allowed_origins", [])
        if isinstance(origins, list):
            for i, origin in enumerate(origins):
                origin_str = str(origin).rstrip("/")
                if origin_str == "*":
                    result.errors.append(
                        ConfigError(
                            path=f"proxy.allowed_origins[{i}]",
                            message="wildcard '*' is not allowed for proxy origins (will be ignored)",
                            severity="warning",
                        )
                    )
                elif not origin_str.startswith(("http://", "https://")):
                    result.errors.append(
                        ConfigError(
                            path=f"proxy.allowed_origins[{i}]",
                            message=f"origin must start with http:// or https://: '{origin_str}' (will be ignored)",
                            severity="warning",
                        )
                    )

    return result


def _check_section_type(
    raw: dict[str, Any],
    key: str,
    expected_type: type,
    result: ValidationResult,
) -> None:
    """Check that a top-level key, if present, is the expected type."""
    if key not in raw:
        return
    val = raw[key]
    if not isinstance(val, expected_type):
        result.errors.append(
            ConfigError(
                path=key,
                message=f"expected {expected_type.__name__}, got {type(val).__name__}",
            )
        )


def _is_numeric(val: Any) -> bool:
    """Check if a value is numeric (int, float, or numeric string)."""
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return True
    if isinstance(val, str):
        try:
            float(val)
            return True
        except ValueError:
            return False
    return False
