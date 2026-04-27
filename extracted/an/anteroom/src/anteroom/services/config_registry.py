"""Config setting registry and deterministic search helpers.

The registry is intentionally data-oriented: CLI, REPL, API, and future
visualization commands can ask one service for known fields, plain-language
help, valid values, and optional current values without scraping docs.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from .config_editor import _SENSITIVE_FIELDS, ConfigFieldInfo, get_field, list_settable_fields

_REDACTED = "***"
_SETTABLE_SCOPES = ("personal", "space", "project")


@dataclass(frozen=True)
class ConfigSettingEntry:
    """Structured help metadata for one config setting."""

    dot_path: str
    field_type: str
    description: str
    section: str
    source: str = "core"
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    settable_scopes: tuple[str, ...] = _SETTABLE_SCOPES
    sensitive: bool = False
    default: Any = None
    allowed_values: tuple[str, ...] | None = None
    min_val: int | float | None = None
    max_val: int | float | None = None


@dataclass(frozen=True)
class ConfigSettingValue:
    """Current value metadata for one registry entry."""

    effective_value: Any
    source_layer: str
    is_enforced: bool


@dataclass(frozen=True)
class ConfigSearchResult:
    """A ranked config setting search hit."""

    entry: ConfigSettingEntry
    score: int
    current: ConfigSettingValue | None = None
    matched: tuple[str, ...] = field(default_factory=tuple)


_CURATED: dict[str, dict[str, Any]] = {
    "ai.base_url": {
        "description": "OpenAI-compatible API endpoint used for chat completions.",
        "aliases": ("endpoint", "api url", "provider url"),
        "tags": ("ai", "provider", "connection"),
    },
    "ai.model": {
        "description": "Default chat model used when a session does not override the model.",
        "aliases": ("llm", "chat model", "model name"),
        "tags": ("ai", "model", "provider"),
    },
    "ai.api_key": {
        "description": "Secret token for the configured AI provider.",
        "aliases": ("token", "secret", "provider key"),
        "tags": ("ai", "auth", "secret"),
    },
    "ai.api_key_command": {
        "description": "Command that prints an AI provider token at runtime.",
        "aliases": ("token command", "secret command"),
        "tags": ("ai", "auth", "secret"),
    },
    "ai.allowed_models": {
        "description": "Optional allowlist of model names users may select.",
        "aliases": ("model allowlist", "allowed llms"),
        "tags": ("ai", "model", "policy"),
    },
    "ai.allowed_domains": {
        "description": "Optional allowlist of outbound provider domains.",
        "aliases": ("egress", "domain allowlist"),
        "tags": ("ai", "network", "policy"),
    },
    "safety.approval_mode": {
        "description": "Controls when tool calls require user approval.",
        "aliases": ("approvals", "permission mode", "ask mode"),
        "tags": ("safety", "permissions", "tools"),
    },
    "safety.read_only": {
        "description": "Restricts the session to read-only tools.",
        "aliases": ("readonly", "no writes"),
        "tags": ("safety", "permissions", "tools"),
    },
    "safety.allowed_tools": {
        "description": "Tools that can run without prompting for approval.",
        "aliases": ("preapproved tools", "allow tools"),
        "tags": ("safety", "permissions", "tools"),
    },
    "safety.denied_tools": {
        "description": "Tools that are always blocked.",
        "aliases": ("blocked tools", "forbid tools"),
        "tags": ("safety", "permissions", "tools"),
    },
    "safety.sensitive_paths": {
        "description": "Path patterns that require extra care before tool access.",
        "aliases": ("protected paths", "secret paths"),
        "tags": ("safety", "files", "policy"),
    },
    "cli.builtin_tools": {
        "description": "Enables Anteroom's built-in local tools.",
        "aliases": ("tools enabled", "local tools"),
        "tags": ("cli", "tools"),
    },
    "cli.max_tool_iterations": {
        "description": "Maximum number of tool iterations allowed in one assistant turn.",
        "aliases": ("tool loop limit", "max tool calls"),
        "tags": ("cli", "tools", "limits"),
    },
    "cli.context_warn_tokens": {
        "description": "Token count at which the CLI warns that context is getting large.",
        "aliases": ("context warning", "token warning"),
        "tags": ("cli", "context", "tokens"),
    },
    "cli.context_auto_compact_tokens": {
        "description": "Token count at which automatic compaction may begin.",
        "aliases": ("auto compact", "context compaction"),
        "tags": ("cli", "context", "tokens"),
    },
    "embeddings.enabled": {
        "description": "Enables embeddings for knowledge retrieval.",
        "aliases": ("rag embeddings", "knowledge embeddings"),
        "tags": ("embeddings", "knowledge", "rag"),
    },
    "embeddings.provider": {
        "description": "Selects local or API-backed embedding generation.",
        "aliases": ("embedding backend",),
        "tags": ("embeddings", "knowledge", "rag"),
    },
    "embeddings.model": {
        "description": "Embedding model used by the configured provider.",
        "aliases": ("embedding model",),
        "tags": ("embeddings", "knowledge", "rag"),
    },
    "rag.enabled": {
        "description": "Enables retrieval-augmented context from indexed sources.",
        "aliases": ("knowledge retrieval", "search context"),
        "tags": ("rag", "knowledge"),
    },
    "rag.max_chunks": {
        "description": "Maximum retrieved knowledge chunks added to a turn.",
        "aliases": ("retrieval chunks",),
        "tags": ("rag", "knowledge", "limits"),
    },
    "project.name": {
        "description": "Human-friendly project name shown in project-aware surfaces.",
        "aliases": ("repo name", "workspace name"),
        "tags": ("project", "metadata"),
    },
    "team_config_path": {
        "description": "Path to a team config file that can set or enforce shared values.",
        "aliases": ("team config", "org config"),
        "tags": ("team", "policy"),
    },
    "pack_sources": {
        "description": "Configured sources for finding and installing packs.",
        "aliases": ("pack registries",),
        "tags": ("packs", "artifacts"),
    },
    "workflow.enabled": {
        "description": "Enables workflow automation features.",
        "aliases": ("automation",),
        "tags": ("workflow", "automation"),
    },
    "hooks": {
        "description": "Tool lifecycle hook configuration.",
        "aliases": ("tool hooks", "pre tool", "post tool"),
        "tags": ("hooks", "tools"),
    },
}

_SECTION_LABELS: dict[str, str] = {
    "ai": "AI provider and generation",
    "app": "Web server",
    "audit": "Audit logging",
    "cli": "CLI behavior",
    "codebase_index": "Codebase indexing",
    "compaction": "Context compaction",
    "embeddings": "Embeddings",
    "feedback": "Feedback reporting",
    "identity": "Identity",
    "memory": "Memory",
    "project": "Project metadata",
    "proxy": "Proxy",
    "rag": "Knowledge retrieval",
    "references": "Reference artifacts",
    "reranker": "Retrieval reranking",
    "safety": "Safety and permissions",
    "session": "Session limits",
    "storage": "Storage",
    "trusted_proxy": "Trusted proxy",
    "workflow": "Workflow automation",
}


def _section_for(dot_path: str) -> str:
    return dot_path.split(".", 1)[0]


def _default_description(dot_path: str) -> str:
    section = _section_for(dot_path)
    key = dot_path.split(".")[-1].replace("_", " ")
    label = _SECTION_LABELS.get(section, section.replace("_", " ").title())
    return f"{label} setting for {key}."


def _field_to_entry(info: ConfigFieldInfo) -> ConfigSettingEntry:
    data = _CURATED.get(info.dot_path, {})
    section = _section_for(info.dot_path)
    default_tags = tuple(dict.fromkeys((section, *info.dot_path.replace("_", " ").split("."))))
    tags = tuple(dict.fromkeys((*data.get("tags", ()), *default_tags)))
    return ConfigSettingEntry(
        dot_path=info.dot_path,
        field_type=info.field_type,
        description=data.get("description") or _default_description(info.dot_path),
        section=section,
        aliases=tuple(data.get("aliases", ())),
        tags=tags,
        sensitive=info.dot_path in _SENSITIVE_FIELDS,
        default=info.default,
        allowed_values=info.allowed_values,
        min_val=info.min_val,
        max_val=info.max_val,
    )


def list_config_settings(*, include_sensitive: bool = False) -> list[ConfigSettingEntry]:
    """Return registry entries for every known settable config field."""
    return [
        _field_to_entry(info)
        for info in list_settable_fields(include_sensitive=True)
        if include_sensitive or info.dot_path not in _SENSITIVE_FIELDS
    ]


def get_config_setting(dot_path: str, *, include_sensitive: bool = False) -> ConfigSettingEntry | None:
    """Return one registry entry by dot path."""
    for entry in list_config_settings(include_sensitive=include_sensitive):
        if entry.dot_path == dot_path:
            return entry
    return None


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(t for t in re.split(r"[^a-z0-9]+", text.lower()) if t)


def search_config_settings(
    query: str,
    *,
    include_sensitive: bool = False,
    limit: int | None = None,
) -> list[ConfigSearchResult]:
    """Search config settings by dot path, alias, tag, and description."""
    needle = query.strip().lower()
    entries = list_config_settings(include_sensitive=include_sensitive)
    if not needle:
        hits = [ConfigSearchResult(entry=e, score=1, matched=("all",)) for e in entries]
        return hits[:limit] if limit else hits

    query_tokens = _tokens(needle)
    results: list[ConfigSearchResult] = []
    for entry in entries:
        haystacks = {
            "dot_path": entry.dot_path.lower(),
            "section": entry.section.lower(),
            "aliases": " ".join(entry.aliases).lower(),
            "tags": " ".join(entry.tags).lower(),
            "description": entry.description.lower(),
        }
        score = 0
        matched: list[str] = []

        if needle == haystacks["dot_path"]:
            score += 1000
            matched.append("dot_path")
        elif haystacks["dot_path"].startswith(needle):
            score += 600
            matched.append("dot_path")
        elif needle in haystacks["dot_path"]:
            score += 300
            matched.append("dot_path")

        for name, text in haystacks.items():
            if name == "dot_path":
                continue
            if needle and needle in text:
                score += {"aliases": 160, "tags": 120, "section": 100, "description": 60}[name]
                matched.append(name)

        for token in query_tokens:
            if token in _tokens(entry.dot_path.replace(".", " ")):
                score += 80
            if token in entry.tags:
                score += 50
            if any(token in alias.lower() for alias in entry.aliases):
                score += 45
            if token in _tokens(entry.description):
                score += 20

        if score:
            results.append(ConfigSearchResult(entry=entry, score=score, matched=tuple(dict.fromkeys(matched))))

    results.sort(key=lambda r: (-r.score, r.entry.dot_path))
    return results[:limit] if limit else results


def attach_current_values(
    entries: list[ConfigSettingEntry],
    config: Any,
    source_map: dict[str, str],
    enforced_fields: list[str],
    *,
    redact_sensitive: bool = True,
) -> list[ConfigSearchResult]:
    """Attach effective value/source metadata to registry entries."""
    results: list[ConfigSearchResult] = []
    for entry in entries:
        value: Any = None
        source = "default"
        enforced = entry.dot_path in enforced_fields
        if entry.sensitive and redact_sensitive:
            value = _REDACTED
            source = "team (enforced)" if enforced else source_map.get(entry.dot_path, "default")
        else:
            try:
                current = get_field(config, entry.dot_path, source_map, enforced_fields)
                value = current.effective_value
                source = current.source_layer
                enforced = current.is_enforced
            except (AttributeError, TypeError, ValueError):
                flat = _flatten_config(config)
                value = flat.get(entry.dot_path)
                source = "team (enforced)" if enforced else source_map.get(entry.dot_path, "default")
        results.append(
            ConfigSearchResult(
                entry=entry,
                score=0,
                current=ConfigSettingValue(effective_value=value, source_layer=source, is_enforced=enforced),
            )
        )
    return results


def _flatten_config(config: Any) -> dict[str, Any]:
    from .config_overlays import flatten_to_dot_paths

    try:
        return flatten_to_dot_paths(asdict(config))
    except TypeError:
        return flatten_to_dot_paths(config if isinstance(config, dict) else {})


def setting_to_dict(
    entry: ConfigSettingEntry,
    *,
    current: ConfigSettingValue | None = None,
) -> dict[str, Any]:
    """Serialize a setting entry for JSON APIs."""
    data = asdict(entry)
    data["allowed_values"] = list(entry.allowed_values) if entry.allowed_values else None
    data["aliases"] = list(entry.aliases)
    data["tags"] = list(entry.tags)
    data["settable_scopes"] = list(entry.settable_scopes)
    if current is not None:
        data["current"] = asdict(current)
    return data
