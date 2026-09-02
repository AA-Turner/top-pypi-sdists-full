"""Epic-tree configuration loading from agdt-config.json."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from agentic_devtools.config import DEFAULT_ISSUE_ADAPTER, VALID_ISSUE_ADAPTERS, load_repo_config

from .errors import ConfigError

# Hard maximum depth allowed by the schema (epic=0, feature=1, subtask=2)
_ABSOLUTE_MAX_DEPTH = 3

_DEFAULT_ISSUE_TYPES: dict[int, str] = {
    0: "Epic",
    1: "Feature",
    2: "Subtask",
}

_DEFAULT_LABELS: dict[int, list[str]] = {
    0: ["epic"],
    1: ["feature"],
    2: ["subtask"],
}


def _copy_depth_label_map(source: dict[int, list[str]]) -> dict[int, list[str]]:
    """Return an independent copy of a depth->labels map."""
    return {depth: list(labels) for depth, labels in source.items()}


@dataclass(frozen=True)
class EpicTreeConfig:
    """Configuration for epic-tree validation and normalization.

    Loaded from ``agdt-config.json["epicTree"]`` or constructed with defaults.
    """

    max_depth: int = _ABSOLUTE_MAX_DEPTH
    allowed_labels: dict[int, list[str]] = field(default_factory=dict)
    allowed_issue_types: dict[int, list[str]] = field(default_factory=dict)
    required_body_sections: dict[int, list[str]] = field(default_factory=dict)
    default_labels: dict[int, list[str]] = field(default_factory=lambda: _copy_depth_label_map(_DEFAULT_LABELS))
    default_issue_types: dict[int, str] = field(default_factory=lambda: dict(_DEFAULT_ISSUE_TYPES))
    provider: str = DEFAULT_ISSUE_ADAPTER

    @classmethod
    def from_config_file(cls, repo_path: Path | str) -> EpicTreeConfig:
        """Load configuration from the repository's agdt-config.json.

        This is a convenience factory that delegates to :func:`load_epic_tree_config`.
        The *repo_path* argument is the repository root path; the method resolves
        ``.github/agdt-config.json`` internally.  Falls back to built-in defaults
        when the file is missing or the ``epicTree`` key is absent.

        Args:
            repo_path: Path to the repository root directory.

        Returns:
            An :class:`EpicTreeConfig` instance.

        Raises:
            ConfigError: If the config file exists but contains invalid values.
        """
        return load_epic_tree_config(repo_path)


def load_epic_tree_config(
    repo_path: Path | str | None = None,
    *,
    provider: str | None = None,
) -> EpicTreeConfig:
    """Load epic-tree configuration from the repository's agdt-config.json.

    Args:
        repo_path: Path to the repository root. If None, returns defaults.
        provider: Optional explicit provider name override.  When supplied and
            non-empty, it selects the matching ``issueManagement`` block
            instead of resolving the active provider from
            ``platform.issue_adapter``.  When ``None`` the active provider is
            resolved from config as before.

    Returns:
        An :class:`EpicTreeConfig` instance.

    Raises:
        ConfigError: If the configuration contains invalid values.
    """
    if provider is not None and not isinstance(provider, str):
        raise ConfigError("<argument>", "provider", f"must be a string, got {type(provider).__name__!r}")
    if repo_path is None:
        if provider is not None and provider.strip():
            normalized = provider.strip().lower()
            if normalized not in VALID_ISSUE_ADAPTERS:
                raise ConfigError(
                    "<argument>",
                    "provider",
                    f"unsupported provider {normalized!r}; valid values: {sorted(VALID_ISSUE_ADAPTERS)}",
                )
            return EpicTreeConfig(provider=normalized)
        return EpicTreeConfig()

    repo_path = Path(repo_path)
    config_file = str(repo_path / ".github" / "agdt-config.json")
    raw_config = load_repo_config(str(repo_path))

    if provider is not None and provider.strip():
        provider = provider.strip().lower()
        if provider not in VALID_ISSUE_ADAPTERS:
            raise ConfigError(
                config_file,
                "provider",
                f"unsupported provider {provider!r}; valid values: {sorted(VALID_ISSUE_ADAPTERS)}",
            )
    else:
        provider = _resolve_active_provider(raw_config)

    # Check for issueManagement section with provider-specific block.
    issue_mgmt = raw_config.get("issueManagement")
    if isinstance(issue_mgmt, dict):
        provider_block = issue_mgmt.get(provider)
        if isinstance(provider_block, dict):
            return _load_with_issue_management(provider_block, raw_config, config_file, provider)

    # Fallback: epicTree-only path (backward compatible).
    epic_tree_section = raw_config.get("epicTree")
    if not epic_tree_section or not isinstance(epic_tree_section, dict):
        return EpicTreeConfig(provider=provider)

    config = _parse_epic_tree_config(epic_tree_section, config_file)
    return EpicTreeConfig(
        max_depth=config.max_depth,
        allowed_labels=config.allowed_labels,
        allowed_issue_types=config.allowed_issue_types,
        required_body_sections=config.required_body_sections,
        default_labels=config.default_labels,
        default_issue_types=config.default_issue_types,
        provider=provider,
    )


def _parse_epic_tree_config(section: dict, config_file: str) -> EpicTreeConfig:
    """Parse and validate the epicTree section of agdt-config.json."""
    max_depth = section.get("maxDepth", _ABSOLUTE_MAX_DEPTH)
    if not isinstance(max_depth, int) or max_depth < 1:
        raise ConfigError(config_file, "epicTree.maxDepth", "must be a positive integer")
    if max_depth > _ABSOLUTE_MAX_DEPTH:
        raise ConfigError(
            config_file,
            "epicTree.maxDepth",
            f"must be <= {_ABSOLUTE_MAX_DEPTH} (schema supports epic/feature/subtask only)",
        )

    allowed_labels = _parse_depth_keyed_list(section.get("allowedLabels", {}), config_file, "epicTree.allowedLabels")
    allowed_issue_types = _parse_depth_keyed_list(
        section.get("allowedIssueTypes", {}), config_file, "epicTree.allowedIssueTypes"
    )
    required_body_sections = _parse_depth_keyed_list(
        section.get("requiredBodySections", {}), config_file, "epicTree.requiredBodySections"
    )
    default_labels = _parse_depth_keyed_list(section.get("defaultLabels", {}), config_file, "epicTree.defaultLabels")
    if not default_labels:
        default_labels = _copy_depth_label_map(_DEFAULT_LABELS)

    default_issue_types = _parse_depth_keyed_string(
        section.get("defaultIssueTypes", {}), config_file, "epicTree.defaultIssueTypes"
    )
    if not default_issue_types:
        default_issue_types = dict(_DEFAULT_ISSUE_TYPES)

    return EpicTreeConfig(
        max_depth=max_depth,
        allowed_labels=allowed_labels,
        allowed_issue_types=allowed_issue_types,
        required_body_sections=required_body_sections,
        default_labels=default_labels,
        default_issue_types=default_issue_types,
    )


def _parse_depth_keyed_list(
    raw: dict | object,
    config_file: str,
    field_name: str,
) -> dict[int, list[str]]:
    """Parse a depth-keyed dict of string lists (e.g. {"0": ["epic"], "1": ["feature"]})."""
    if not isinstance(raw, dict):
        return {}
    result: dict[int, list[str]] = {}
    for key, value in raw.items():
        try:
            depth = int(key)
        except (ValueError, TypeError):
            raise ConfigError(config_file, field_name, f"depth key '{key}' must be a numeric string")
        if depth < 0 or depth >= _ABSOLUTE_MAX_DEPTH:
            raise ConfigError(
                config_file,
                field_name,
                f"depth key '{key}' is out of range; supported depths are 0..{_ABSOLUTE_MAX_DEPTH - 1}",
            )
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise ConfigError(config_file, field_name, f"values for depth '{key}' must be a list of strings")
        result[depth] = value
    return result


def _parse_depth_keyed_string(
    raw: dict | object,
    config_file: str,
    field_name: str,
) -> dict[int, str]:
    """Parse a depth-keyed dict of strings (e.g. {"0": "Epic", "1": "Feature"})."""
    if not isinstance(raw, dict):
        return {}
    result: dict[int, str] = {}
    for key, value in raw.items():
        try:
            depth = int(key)
        except (ValueError, TypeError):
            raise ConfigError(config_file, field_name, f"depth key '{key}' must be a numeric string")
        if depth < 0 or depth >= _ABSOLUTE_MAX_DEPTH:
            raise ConfigError(
                config_file,
                field_name,
                f"depth key '{key}' is out of range; supported depths are 0..{_ABSOLUTE_MAX_DEPTH - 1}",
            )
        if not isinstance(value, str):
            raise ConfigError(config_file, field_name, f"value for depth '{key}' must be a string")
        result[depth] = value
    return result


def _resolve_active_provider(raw_config: dict) -> str:
    """Resolve the active issue adapter from the raw config dict.

    Mirrors the ``issue_adapter`` normalization in ``load_platform_config()``
    but operates on the already-loaded config dict to avoid a second I/O round-trip.

    Args:
        raw_config: Parsed JSON dict from agdt-config.json.

    Returns:
        A concrete provider string from ``VALID_ISSUE_ADAPTERS``.
    """
    platform = raw_config.get("platform")
    if not isinstance(platform, dict):
        return DEFAULT_ISSUE_ADAPTER
    issue_adapter = platform.get("issue_adapter")
    if not isinstance(issue_adapter, str) or issue_adapter not in VALID_ISSUE_ADAPTERS:
        return DEFAULT_ISSUE_ADAPTER
    return issue_adapter


def _parse_issue_management_section(
    section: dict,
    config_file: str,
    provider: str,
) -> dict:
    """Parse and validate an issueManagement.<provider> block.

    Returns a dict with snake_case keys mirroring ``EpicTreeConfig`` field names:
    ``allowed_labels``, ``allowed_issue_types``, ``required_body_sections``,
    ``default_labels``, ``default_issue_types``, and optionally ``max_depth``.

    Raises:
        ConfigError: If the section contains malformed values.
    """
    prefix = f"issueManagement.{provider}"
    result: dict = {}

    # Parse maxDepth (optional override).
    raw_max_depth = section.get("maxDepth")
    if raw_max_depth is not None:
        if isinstance(raw_max_depth, bool) or not isinstance(raw_max_depth, int) or raw_max_depth < 1:
            raise ConfigError(config_file, f"{prefix}.maxDepth", "must be a positive integer")
        if raw_max_depth > _ABSOLUTE_MAX_DEPTH:
            raise ConfigError(
                config_file,
                f"{prefix}.maxDepth",
                f"must be <= {_ABSOLUTE_MAX_DEPTH} (schema supports epic/feature/subtask only)",
            )
        result["max_depth"] = raw_max_depth

    # Parse depth-keyed list fields; store under snake_case keys matching EpicTreeConfig.
    _list_field_map = [
        ("allowedLabels", "allowed_labels"),
        ("allowedIssueTypes", "allowed_issue_types"),
        ("requiredBodySections", "required_body_sections"),
        ("defaultLabels", "default_labels"),
    ]
    for json_name, snake_name in _list_field_map:
        raw_field = section.get(json_name)
        if raw_field is None:
            continue
        if not isinstance(raw_field, dict):
            raise ConfigError(config_file, f"{prefix}.{json_name}", "must be an object with depth keys")
        result[snake_name] = _parse_depth_keyed_list(raw_field, config_file, f"{prefix}.{json_name}")

    # Parse defaultIssueTypes (depth-keyed string map); store under snake_case key.
    raw_dit = section.get("defaultIssueTypes")
    if raw_dit is not None:
        if not isinstance(raw_dit, dict):
            raise ConfigError(config_file, f"{prefix}.defaultIssueTypes", "must be an object with depth keys")
        result["default_issue_types"] = _parse_depth_keyed_string(raw_dit, config_file, f"{prefix}.defaultIssueTypes")

    return result


def _merge_depth_keyed_maps(
    high: dict[int, list[str]],
    low: dict[int, list[str]],
) -> dict[int, list[str]]:
    """Merge two depth-keyed list maps with per-key precedence.

    For each depth key present in *high*, the *high* value wins (full replacement).
    Keys only in *low* are preserved.

    Args:
        high: Higher-precedence depth-keyed map.
        low: Lower-precedence depth-keyed map.

    Returns:
        Merged depth-keyed map.
    """
    merged = dict(low)
    merged.update(high)
    return merged


def _merge_depth_keyed_string_maps(
    high: dict[int, str],
    low: dict[int, str],
) -> dict[int, str]:
    """Merge two depth-keyed string maps with per-key precedence.

    For each depth key present in *high*, the *high* value wins.
    Keys only in *low* are preserved.

    Args:
        high: Higher-precedence depth-keyed map.
        low: Lower-precedence depth-keyed map.

    Returns:
        Merged depth-keyed map.
    """
    merged = dict(low)
    merged.update(high)
    return merged


def _load_with_issue_management(
    provider_block: dict,
    raw_config: dict,
    config_file: str,
    provider: str,
) -> EpicTreeConfig:
    """Load config with issueManagement section merged over epicTree.

    Precedence (highest to lowest):
        issueManagement.<provider> → epicTree → built-in defaults
    """
    im_parsed = _parse_issue_management_section(provider_block, config_file, provider)

    # Parse epicTree section as the base (lower precedence).
    epic_tree_section = raw_config.get("epicTree")
    if isinstance(epic_tree_section, dict):
        base = _parse_epic_tree_config(epic_tree_section, config_file)
    else:
        base = EpicTreeConfig()

    # Resolve effective maxDepth: provider override wins.
    max_depth = im_parsed.get("max_depth", base.max_depth)

    # Merge depth-keyed list fields.
    allowed_labels = _merge_depth_keyed_maps(im_parsed.get("allowed_labels", {}), base.allowed_labels)
    allowed_issue_types = _merge_depth_keyed_maps(im_parsed.get("allowed_issue_types", {}), base.allowed_issue_types)
    required_body_sections = _merge_depth_keyed_maps(
        im_parsed.get("required_body_sections", {}), base.required_body_sections
    )
    default_labels = _merge_depth_keyed_maps(im_parsed.get("default_labels", {}), base.default_labels)

    # Merge depth-keyed string fields.
    default_issue_types = _merge_depth_keyed_string_maps(
        im_parsed.get("default_issue_types", {}), base.default_issue_types
    )

    # Validate issueManagement-provided depth keys against effective maxDepth.
    # Keys inherited from epicTree/defaults are silently truncated.
    # field_name uses JSON spelling for error-message clarity.
    im_list_fields = [
        ("allowedLabels", im_parsed.get("allowed_labels", {})),
        ("allowedIssueTypes", im_parsed.get("allowed_issue_types", {})),
        ("requiredBodySections", im_parsed.get("required_body_sections", {})),
        ("defaultLabels", im_parsed.get("default_labels", {})),
    ]
    for field_name, im_map in im_list_fields:
        for depth_key in im_map:
            if depth_key >= max_depth:
                raise ConfigError(
                    config_file,
                    f"issueManagement.{provider}.{field_name}",
                    f"depth key '{depth_key}' exceeds effective maxDepth ({max_depth})",
                )
    im_dit = im_parsed.get("default_issue_types", {})
    for depth_key in im_dit:
        if depth_key >= max_depth:
            raise ConfigError(
                config_file,
                f"issueManagement.{provider}.defaultIssueTypes",
                f"depth key '{depth_key}' exceeds effective maxDepth ({max_depth})",
            )

    # Truncate merged maps to effective maxDepth (remove inherited keys out of range).
    allowed_labels = {k: v for k, v in allowed_labels.items() if k < max_depth}
    allowed_issue_types = {k: v for k, v in allowed_issue_types.items() if k < max_depth}
    required_body_sections = {k: v for k, v in required_body_sections.items() if k < max_depth}
    default_labels = {k: v for k, v in default_labels.items() if k < max_depth}
    default_issue_types = {k: v for k, v in default_issue_types.items() if k < max_depth}

    return EpicTreeConfig(
        max_depth=max_depth,
        allowed_labels=allowed_labels,
        allowed_issue_types=allowed_issue_types,
        required_body_sections=required_body_sections,
        default_labels=default_labels,
        default_issue_types=default_issue_types,
        provider=provider,
    )
