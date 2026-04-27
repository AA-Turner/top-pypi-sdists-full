"""Config hierarchy inspection service.

The hierarchy view is an aggregation layer. Config provenance comes from
``config_explanation`` and setting metadata/current values come from
``config_registry`` so this command does not drift from the explanation/help
surfaces.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config_editor import _SENSITIVE_FIELDS, LAYER_ORDER, get_field
from .config_explanation import ConfigExplanationContext, list_sources
from .config_overlays import flatten_to_dot_paths
from .config_registry import attach_current_values, get_config_setting, list_config_settings

_LAYER_ORDER = (*LAYER_ORDER, "cli flags")
_KEY_SETTING_PATHS = (
    "ai.model",
    "ai.base_url",
    "safety.approval_mode",
    "safety.read_only",
    "safety.allowed_tools",
    "safety.denied_tools",
    "cli.builtin_tools",
    "cli.max_tool_iterations",
    "project.name",
)


@dataclass(frozen=True)
class ConfigHierarchyLayer:
    """One config layer in merge precedence order."""

    name: str
    precedence: int
    active: bool
    source: str | None = None
    key_count: int = 0
    winning_key_count: int = 0
    enforced_key_count: int = 0
    keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConfigHierarchyItem:
    """Named item attached to the config hierarchy."""

    name: str
    kind: str
    source: str | None = None
    detail: str | None = None


@dataclass(frozen=True)
class ConfigHierarchy:
    """Structured config hierarchy result."""

    layers: tuple[ConfigHierarchyLayer, ...]
    enforced_fields: tuple[str, ...] = ()
    required_fields: tuple[ConfigHierarchyItem, ...] = ()
    key_settings: tuple[ConfigHierarchyItem, ...] = ()
    references: tuple[ConfigHierarchyItem, ...] = ()
    skills: tuple[ConfigHierarchyItem, ...] = ()
    mcp_servers: tuple[ConfigHierarchyItem, ...] = ()
    tools: tuple[ConfigHierarchyItem, ...] = ()
    final_key_count: int = 0


def build_config_hierarchy(
    *,
    context: ConfigExplanationContext,
    include_keys: bool = False,
) -> ConfigHierarchy:
    """Build a structured view from explanation context and registry metadata."""
    sources = list_sources(context)
    source_layers = {row["layer"]: row for row in sources["layers"]}
    final_flat = _redact_flat(_flatten_config_object(context.config))
    enforced = set(context.enforced_fields)

    layers: list[ConfigHierarchyLayer] = []
    for precedence, layer_name in enumerate(_LAYER_ORDER):
        raw = context.layer_raws.get(layer_name, {})
        if layer_name == "default":
            flat = {k: v for k, v in final_flat.items() if k not in context.source_map and k not in enforced}
        elif layer_name == "cli flags":
            flat = {}
        else:
            flat = _redact_flat(flatten_to_dot_paths(raw)) if raw else {}

        winning = sum(
            1 for key in flat if (key in enforced and layer_name == "team") or context.source_map.get(key) == layer_name
        )
        source = _layer_source(layer_name, context)
        if source is None and layer_name in source_layers and source_layers[layer_name]["field_count"]:
            source = layer_name

        layers.append(
            ConfigHierarchyLayer(
                name=layer_name,
                precedence=precedence,
                active=bool(flat) or layer_name == "default",
                source=source,
                key_count=len(flat),
                winning_key_count=winning,
                enforced_key_count=sum(1 for key in flat if key in enforced),
                keys=tuple(sorted(flat)) if include_keys else (),
            )
        )

    return ConfigHierarchy(
        layers=tuple(layers),
        enforced_fields=tuple(sorted(enforced)),
        required_fields=_collect_required_fields(context),
        key_settings=_collect_key_settings(context),
        references=_collect_instruction_references(context),
        skills=_collect_skills(context),
        mcp_servers=_collect_mcp_servers(context.config),
        tools=_collect_tools(context.config),
        final_key_count=len(final_flat),
    )


def hierarchy_to_dict(hierarchy: ConfigHierarchy) -> dict[str, Any]:
    """Serialize hierarchy data for JSON output."""
    return asdict(hierarchy)


def _flatten_config_object(config: Any) -> dict[str, Any]:
    try:
        return flatten_to_dot_paths(asdict(config))
    except TypeError:
        return flatten_to_dot_paths(config if isinstance(config, dict) else {})


def _redact_flat(flat: dict[str, Any]) -> dict[str, Any]:
    return {key: "***" if key in _SENSITIVE_FIELDS and value else value for key, value in flat.items()}


def _layer_source(layer_name: str, context: ConfigExplanationContext) -> str | None:
    if layer_name == "pack" and context.pack_merge and context.pack_merge.contributions:
        packs = sorted({c.pack_label for c in context.pack_merge.contributions if c.pack_label})
        return ", ".join(packs) if packs else "attached packs"
    if layer_name == "space" and context.active_space:
        return str(context.active_space.get("source_file") or context.active_space.get("name") or "active space")
    if layer_name == "project" and context.working_dir:
        return str(Path(context.working_dir))
    if layer_name == "env var" and context.layer_raws.get(layer_name):
        return "AI_CHAT_*"
    return None


def _collect_required_fields(context: ConfigExplanationContext) -> tuple[ConfigHierarchyItem, ...]:
    items: list[ConfigHierarchyItem] = []
    for layer_name in ("team", "project"):
        required = context.layer_raws.get(layer_name, {}).get("required", [])
        if not isinstance(required, list):
            continue
        for entry in required:
            if isinstance(entry, dict):
                path = str(entry.get("path") or "")
                description = str(entry.get("description") or "")
            else:
                path = str(entry)
                description = ""
            if not path:
                continue
            status = _required_status(path, context)
            detail = status if not description else f"{status}; {description}"
            items.append(ConfigHierarchyItem(name=path, kind="required", source=layer_name, detail=detail))
    return tuple(items)


def _required_status(path: str, context: ConfigExplanationContext) -> str:
    try:
        current = get_field(context.config, path, context.source_map, context.enforced_fields)
    except (AttributeError, TypeError, ValueError):
        return "missing"
    return "configured" if current.effective_value not in (None, "", [], {}) else "missing"


def _collect_key_settings(context: ConfigExplanationContext) -> tuple[ConfigHierarchyItem, ...]:
    entries = [entry for path in _KEY_SETTING_PATHS if (entry := get_config_setting(path))]
    if not entries:
        entries = list_config_settings()[:8]
    results = attach_current_values(entries, context.config, context.source_map, context.enforced_fields)
    items: list[ConfigHierarchyItem] = []
    for result in results:
        current = result.current
        if current is None:
            continue
        value = current.effective_value
        detail = f"{_format_value(value)} from {current.source_layer}"
        if current.is_enforced:
            detail += " (enforced)"
        items.append(
            ConfigHierarchyItem(
                name=result.entry.dot_path,
                kind="setting",
                source=current.source_layer,
                detail=detail,
            )
        )
    return tuple(items)


def _collect_instruction_references(context: ConfigExplanationContext) -> tuple[ConfigHierarchyItem, ...]:
    items: list[ConfigHierarchyItem] = []
    try:
        from ..cli.instructions import discover_conventions

        discovered = discover_conventions(context.working_dir)
        if discovered.path is not None:
            items.append(
                ConfigHierarchyItem(
                    name=str(discovered.path),
                    kind="instruction",
                    source=discovered.source,
                    detail=f"{discovered.estimated_tokens} tokens",
                )
            )
    except Exception:
        pass

    refs = getattr(context.config, "references", None)
    if refs is None:
        return tuple(items)
    for kind in ("instructions", "rules"):
        values = getattr(refs, kind, None) or []
        if not isinstance(values, list):
            continue
        for value in values:
            path = Path(str(value))
            detail = _file_detail(path)
            items.append(
                ConfigHierarchyItem(name=str(value), kind=kind.removesuffix("s"), source="config", detail=detail)
            )
    return tuple(items)


def _collect_skills(context: ConfigExplanationContext) -> tuple[ConfigHierarchyItem, ...]:
    refs = getattr(context.config, "references", None)
    reference_paths = getattr(refs, "skills", None) or []
    items: list[ConfigHierarchyItem] = []
    try:
        from ..cli.skills import SkillRegistry

        registry = SkillRegistry()
        for skill in registry.load(context.working_dir):
            items.append(
                ConfigHierarchyItem(
                    name=skill.name,
                    kind="skill",
                    source=skill.source,
                    detail=_skill_detail(skill),
                )
            )
        if isinstance(reference_paths, list):
            registry.load_from_references([str(path) for path in reference_paths])
            for skill in registry.list_skills():
                if skill.source == "reference":
                    items.append(
                        ConfigHierarchyItem(
                            name=skill.name,
                            kind="skill",
                            source="reference",
                            detail=_skill_detail(skill),
                        )
                    )
    except Exception:
        if isinstance(reference_paths, list):
            for value in reference_paths:
                items.append(
                    ConfigHierarchyItem(
                        name=str(value),
                        kind="skill",
                        source="config",
                        detail=_file_detail(Path(str(value))),
                    )
                )
    return tuple(_dedupe_items(items))


def _collect_mcp_servers(config: Any) -> tuple[ConfigHierarchyItem, ...]:
    items: list[ConfigHierarchyItem] = []
    for server in getattr(config, "mcp_servers", []) or []:
        name = str(getattr(server, "name", "") or "(unnamed)")
        transport = str(getattr(server, "transport", "") or "unknown")
        enabled = getattr(server, "enabled", True)
        status = "configured" if enabled else "disabled"
        detail = f"{status}; {transport}; tools unknown until connected"
        items.append(ConfigHierarchyItem(name=name, kind="mcp_server", source="config", detail=detail))
    return tuple(items)


def _collect_tools(config: Any) -> tuple[ConfigHierarchyItem, ...]:
    cli = getattr(config, "cli", None)
    safety = getattr(config, "safety", None)
    builtin_tools = getattr(cli, "builtin_tools", True) if cli is not None else True
    tool_count = 0
    if builtin_tools:
        try:
            from ..config import _BUILTIN_TOOL_DESCRIPTIONS

            tool_count = len(_BUILTIN_TOOL_DESCRIPTIONS)
        except Exception:
            tool_count = 0
    mcp_count = len(getattr(config, "mcp_servers", []) or [])
    approval_mode = getattr(safety, "approval_mode", None)
    read_only = getattr(safety, "read_only", None)
    allowed = getattr(safety, "allowed_tools", None) or []
    denied = getattr(safety, "denied_tools", None) or []
    return (
        ConfigHierarchyItem(
            name="builtin_tools",
            kind="tool_set",
            source="config",
            detail=f"{'enabled' if builtin_tools else 'disabled'}; {tool_count} tools",
        ),
        ConfigHierarchyItem(
            name="mcp_tools",
            kind="tool_set",
            source="config",
            detail=f"{mcp_count} configured servers; tool count known after connection",
        ),
        ConfigHierarchyItem(
            name="approval_mode",
            kind="tool_policy",
            source="safety",
            detail=str(approval_mode) if approval_mode else "default",
        ),
        ConfigHierarchyItem(
            name="tool_filters",
            kind="tool_policy",
            source="safety",
            detail=f"read_only={bool(read_only)}; allowed={len(allowed)}; denied={len(denied)}",
        ),
    )


def _format_value(value: Any) -> str:
    if isinstance(value, (list, tuple, set)):
        return "[" + ", ".join(str(v) for v in list(value)[:5]) + (", ..." if len(value) > 5 else "") + "]"
    text = str(value)
    return text if len(text) <= 80 else text[:77] + "..."


def _file_detail(path: Path) -> str:
    if not path.exists():
        return "missing"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return "unreadable"
    try:
        from ..cli.instructions import estimate_tokens

        return f"loaded; {estimate_tokens(text)} tokens"
    except Exception:
        return "loaded"


def _skill_detail(skill: Any) -> str | None:
    parts = []
    policy = getattr(skill, "policy", None)
    if policy is not None and str(policy):
        parts.append(str(policy))
    resource_count = getattr(skill, "resource_count", 0)
    if resource_count:
        parts.append(f"{resource_count} resources")
    return "; ".join(parts) if parts else None


def _dedupe_items(items: list[ConfigHierarchyItem]) -> list[ConfigHierarchyItem]:
    seen: set[tuple[str, str, str | None]] = set()
    result: list[ConfigHierarchyItem] = []
    for item in items:
        key = (item.kind, item.name, item.source)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
