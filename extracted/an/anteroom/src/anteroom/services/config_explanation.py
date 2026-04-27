"""Effective config explanations and write guidance.

This module sits above ``config_editor`` and ``config_overlays``.  It does not
resolve config independently; callers provide the already-merged ``AppConfig``
and this service reconstructs raw contributing layers for explanations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config_editor import (
    _SAFE_DOT_PATH,
    _SENSITIVE_FIELDS,
    LAYER_ORDER,
    _find_field_info,
    _read_yaml,
    build_full_source_map,
    check_write_allowed,
    collect_env_overrides,
    get_field,
)
from .config_overlays import (
    PackOverlayContribution,
    PackOverlayMergeResult,
    collect_pack_overlay_artifacts,
    flatten_to_dot_paths,
    merge_pack_overlays_with_provenance,
)

WRITABLE_SCOPES = ("personal", "space", "project")


@dataclass(frozen=True)
class ConfigLayerValue:
    """A configured value from one layer of the config stack."""

    layer: str
    value: Any
    wins: bool = False
    redacted: bool = False


@dataclass(frozen=True)
class ConfigExplanationContext:
    """Inputs needed to explain effective config state."""

    config: Any
    source_map: dict[str, str]
    enforced_fields: list[str]
    layer_raws: dict[str, dict[str, Any]] = field(default_factory=dict)
    pack_merge: PackOverlayMergeResult | None = None
    active_space: dict[str, Any] | None = None
    working_dir: str | None = None


@dataclass(frozen=True)
class ConfigExplanation:
    """Explanation of a single config dot-path."""

    dot_path: str
    effective_value: Any
    display_value: Any
    source_layer: str
    is_enforced: bool
    is_sensitive: bool
    field_info: Any | None = None
    layer_values: list[ConfigLayerValue] = field(default_factory=list)
    pack_contributions: list[PackOverlayContribution] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-safe representation with sensitive values redacted."""
        return {
            "dot_path": self.dot_path,
            "effective_value": self.display_value,
            "source_layer": self.source_layer,
            "is_enforced": self.is_enforced,
            "is_sensitive": self.is_sensitive,
            "field_info": asdict(self.field_info) if self.field_info else None,
            "layer_values": [asdict(v) for v in self.layer_values],
            "pack_contributions": [_redacted_contribution(c, self.is_sensitive) for c in self.pack_contributions],
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class WritePlan:
    """Dry-run result for setting a config value."""

    dot_path: str
    desired_value: Any
    requested_scope: str | None
    recommended_scope: str | None
    can_write: bool
    would_be_effective: bool
    reason: str | None = None
    blocking_layers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_explanation_context(
    config: Any,
    enforced_fields: list[str] | None = None,
    *,
    db: Any = None,
    active_space: dict[str, Any] | None = None,
    working_dir: str | Path | None = None,
    team_config_path: Path | None = None,
) -> ConfigExplanationContext:
    """Build an explanation context from the same raw layers runtime uses."""
    from ..config import _get_config_path
    from .project_config import discover_project_config
    from .team_config import discover_team_config, load_team_config

    wd = str(working_dir or Path.cwd())
    enforced = list(enforced_fields or [])

    team_raw: dict[str, Any] = {}
    team_path = discover_team_config(cli_path=team_config_path, cwd=wd)
    if team_path:
        try:
            team_raw, loaded_enforced = load_team_config(team_path, interactive=False)
            if not enforced:
                enforced = loaded_enforced
        except Exception:
            team_raw = {}

    personal_raw = _read_yaml(_get_config_path())

    pack_raw: dict[str, Any] = {}
    pack_merge: PackOverlayMergeResult | None = None
    try:
        if db is not None:
            from .pack_attachments import (
                get_active_pack_ids,
                get_active_pack_ids_for_space,
                get_attachment_priorities,
                list_attachments,
            )

            space_id = active_space.get("id") if active_space else None
            active_ids = (
                get_active_pack_ids_for_space(db, space_id, project_path=wd)
                if space_id
                else get_active_pack_ids(db, project_path=wd)
            )
            if active_ids:
                artifacts = collect_pack_overlay_artifacts(db, active_ids)
                priorities = get_attachment_priorities(db, active_ids)
                attachments = {
                    f"{row.get('namespace')}/{row.get('name')}": row
                    for row in list_attachments(db, project_path=wd, space_id=space_id)
                }
                pack_merge = merge_pack_overlays_with_provenance(artifacts, priorities, attachments)
                pack_raw = pack_merge.merged
    except Exception:
        pack_raw = {}
        pack_merge = None

    space_raw: dict[str, Any] = {}
    if active_space and active_space.get("source_file"):
        sp_path = Path(active_space["source_file"])
        if sp_path.exists():
            try:
                from .spaces import parse_space_file

                space_raw = parse_space_file(sp_path).config or {}
            except Exception:
                space_raw = {}

    project_raw: dict[str, Any] = {}
    project_raw_for_sources: dict[str, Any] = {}
    proj_path = discover_project_config(wd)
    if proj_path:
        project_raw_for_sources = _read_yaml(proj_path)
        project_raw = dict(project_raw_for_sources)
        project_raw.pop("required", None)

    env_overrides = collect_env_overrides()
    layer_raws = {
        "team": team_raw,
        "pack": pack_raw,
        "personal": personal_raw,
        "space": space_raw,
        "project": project_raw_for_sources,
        "env var": env_overrides,
    }
    source_map = build_full_source_map(
        team_raw=team_raw,
        pack_raw=pack_raw,
        personal_raw=personal_raw,
        space_raw=space_raw,
        project_raw=project_raw,
        env_overrides=env_overrides,
    )
    return ConfigExplanationContext(
        config=config,
        source_map=source_map,
        enforced_fields=enforced,
        layer_raws=layer_raws,
        pack_merge=pack_merge,
        active_space=active_space,
        working_dir=wd,
    )


def explain_setting(dot_path: str, context: ConfigExplanationContext) -> ConfigExplanation:
    """Explain the effective value and provenance for one config dot-path."""
    if not _SAFE_DOT_PATH.match(dot_path):
        raise ValueError(f"Invalid config path: {dot_path!r}")

    is_sensitive = dot_path in _SENSITIVE_FIELDS
    field_value = get_field(
        context.config,
        dot_path,
        context.source_map,
        context.enforced_fields,
        layer_raws=context.layer_raws,
    )

    layer_values: list[ConfigLayerValue] = []
    for layer in LAYER_ORDER:
        if layer == "default":
            continue
        flat = flatten_to_dot_paths(context.layer_raws.get(layer, {}))
        if dot_path in flat:
            layer_values.append(
                ConfigLayerValue(
                    layer=layer,
                    value=_redact(dot_path, flat[dot_path]),
                    wins=field_value.source_layer == layer,
                    redacted=is_sensitive,
                )
            )

    pack_contributions = [
        c for c in (context.pack_merge.contributions if context.pack_merge else []) if c.dot_path == dot_path
    ]

    notes: list[str] = []
    if field_value.is_enforced:
        notes.append("Team enforcement prevents lower-precedence or runtime overrides.")
    if pack_contributions and field_value.source_layer != "pack":
        notes.append(f"The pack-layer value is overridden by {field_value.source_layer}.")
    if not layer_values and field_value.source_layer == "default":
        notes.append("No configured layer sets this field; the effective value comes from defaults.")

    return ConfigExplanation(
        dot_path=dot_path,
        effective_value=field_value.effective_value,
        display_value=_redact(dot_path, field_value.effective_value),
        source_layer=field_value.source_layer,
        is_enforced=field_value.is_enforced,
        is_sensitive=is_sensitive,
        field_info=field_value.field_info,
        layer_values=layer_values,
        pack_contributions=pack_contributions,
        notes=notes,
    )


def list_sources(context: ConfigExplanationContext) -> dict[str, Any]:
    """Return structured source/layer data for tooling consumers."""
    layers: list[dict[str, Any]] = []
    for layer in LAYER_ORDER:
        if layer == "default":
            continue
        raw = context.layer_raws.get(layer, {})
        flat = flatten_to_dot_paths(raw)
        layers.append(
            {
                "layer": layer,
                "configured_fields": sorted(flat),
                "field_count": len(flat),
            }
        )
    return {
        "layers": layers,
        "enforced_fields": sorted(context.enforced_fields),
        "pack_contributions": [
            _redacted_contribution(c, c.dot_path in _SENSITIVE_FIELDS)
            for c in (context.pack_merge.contributions if context.pack_merge else [])
        ],
        "pack_conflicts": list(context.pack_merge.conflicts if context.pack_merge else []),
    }


def recommend_write_scope(
    dot_path: str,
    desired_value: Any,
    context: ConfigExplanationContext,
    *,
    requested_scope: str | None = None,
) -> WritePlan:
    """Recommend a writable scope and report whether it would take effect."""
    parsed_value = _redact(dot_path, desired_value)
    allowed, reason = check_write_allowed(dot_path, context.enforced_fields)
    if not allowed:
        return WritePlan(dot_path, parsed_value, requested_scope, None, False, False, reason=reason)

    if _find_field_info(dot_path) is None:
        return WritePlan(
            dot_path,
            parsed_value,
            requested_scope,
            None,
            False,
            False,
            reason=f"'{dot_path}' is not a known settable config field",
        )

    if requested_scope is not None and requested_scope not in WRITABLE_SCOPES:
        return WritePlan(
            dot_path,
            parsed_value,
            requested_scope,
            None,
            False,
            False,
            reason="scope must be personal, space, or project",
        )

    flat_layers = {layer: flatten_to_dot_paths(raw) for layer, raw in context.layer_raws.items()}
    if dot_path in flat_layers.get("env var", {}):
        return WritePlan(
            dot_path,
            parsed_value,
            requested_scope,
            "env var",
            False,
            False,
            reason="An environment variable currently overrides persistent config for this field",
            blocking_layers=["env var"],
        )

    available_scopes = ["personal", "project"]
    if context.active_space and context.active_space.get("source_file"):
        available_scopes.insert(1, "space")

    scope = requested_scope or _smallest_effective_scope(dot_path, flat_layers, available_scopes)
    blockers = _higher_persistent_layers(dot_path, flat_layers, scope)
    if blockers:
        recommended = _smallest_effective_scope(dot_path, flat_layers, available_scopes)
        return WritePlan(
            dot_path,
            parsed_value,
            requested_scope,
            recommended,
            True,
            False,
            reason=f"{scope} config would be overridden by {', '.join(blockers)}",
            blocking_layers=blockers,
        )

    return WritePlan(dot_path, parsed_value, requested_scope, scope, True, True)


def plan_set(
    dot_path: str,
    desired_value: Any,
    context: ConfigExplanationContext,
    *,
    scope: str | None = None,
) -> WritePlan:
    """Alias for write-planning callers."""
    return recommend_write_scope(dot_path, desired_value, context, requested_scope=scope)


def format_explanation(explanation: ConfigExplanation) -> str:
    """Render a compact human-readable explanation."""
    lines = [
        f"{explanation.dot_path}",
        f"  Effective: {explanation.display_value!r}",
        f"  Source:    {explanation.source_layer}",
    ]
    if explanation.field_info:
        lines.append(f"  Type:      {explanation.field_info.field_type}")
        if explanation.field_info.allowed_values:
            lines.append(f"  Allowed:   {', '.join(explanation.field_info.allowed_values)}")
    if explanation.layer_values:
        lines.append("  Configured values:")
        for layer_value in explanation.layer_values:
            marker = " (wins)" if layer_value.wins else ""
            lines.append(f"    - {layer_value.layer}: {layer_value.value!r}{marker}")
    if explanation.pack_contributions:
        lines.append("  Pack contributions:")
        for contribution in explanation.pack_contributions:
            marker = (
                "wins pack layer" if contribution.wins_pack_layer else f"overridden by {contribution.overridden_by}"
            )
            lines.append(
                f"    - {contribution.pack_label} priority {contribution.priority}: "
                f"{_redact(explanation.dot_path, contribution.value)!r} ({marker})"
            )
    for note in explanation.notes:
        lines.append(f"  Note:      {note}")
    return "\n".join(lines)


def format_write_plan(plan: WritePlan) -> str:
    """Render concise write guidance."""
    if not plan.can_write:
        return f"Cannot change {plan.dot_path}: {plan.reason}"
    if plan.would_be_effective:
        return f"Change {plan.dot_path} in {plan.recommended_scope} config for this value to take effect."
    return f"Changing {plan.dot_path} there would not take effect: {plan.reason}."


def _smallest_effective_scope(
    dot_path: str,
    flat_layers: dict[str, dict[str, Any]],
    available_scopes: list[str],
) -> str:
    for scope in available_scopes:
        if not _higher_persistent_layers(dot_path, flat_layers, scope):
            return scope
    return available_scopes[-1]


def _higher_persistent_layers(dot_path: str, flat_layers: dict[str, dict[str, Any]], scope: str) -> list[str]:
    precedence = {"personal": 0, "space": 1, "project": 2}
    scope_rank = precedence.get(scope, -1)
    blockers: list[str] = []
    for layer, rank in precedence.items():
        if rank > scope_rank and dot_path in flat_layers.get(layer, {}):
            blockers.append(layer)
    return blockers


def _redact(dot_path: str, value: Any) -> Any:
    if dot_path in _SENSITIVE_FIELDS and value not in (None, ""):
        return "***"
    return value


def _redacted_contribution(contribution: PackOverlayContribution, sensitive: bool) -> dict[str, Any]:
    data = asdict(contribution)
    if sensitive and data.get("value") not in (None, ""):
        data["value"] = "***"
    return data
