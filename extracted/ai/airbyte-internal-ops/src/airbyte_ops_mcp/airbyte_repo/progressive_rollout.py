# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Progressive rollout configuration utilities for Airbyte connectors.

A connector's `releases.rolloutConfiguration` has two independent parts:

- *Configuration* (the "how"): `defaultRolloutMode` plus `autopilotConfig`
  (`autoStart`, `autoPromoteStages`, `strategy`). This is the persistent,
  connector-level setup written the first time autopilot is turned on.
- *The toggle* (the "whether"): the `enableProgressiveRollout` boolean, which
  is what actually turns automatic progressive rollout on or off.

`bump_connector_version` in `bump_version.py` also writes the toggle per
release: RC bumps set it `true`, and `promote` clears it to `false` — except
for connectors whose `defaultRolloutMode` is `autopilot`, where the flag is
left `true` so autopilot stays on across GA promotion.

This module provides:

- `extract_ga_version`, used during the promote flow.
- `enable_autopilot_rollout`, which clobbers `defaultRolloutMode: autopilot`,
  fills in any absent `autopilotConfig` defaults, and sets
  `enableProgressiveRollout: true`.
- `disable_autopilot_rollout`, which only sets `enableProgressiveRollout:
  false`, leaving `defaultRolloutMode` and `autopilotConfig` intact so the
  configuration is retained (inert) for a lossless re-enable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from airbyte_connector_models.metadata.v0.connector_metadata_definition_v0 import (
    ConnectorMetadataDefinitionV0DataConnectorReleasesRolloutConfigurationAutopilotConfigStrategy as AutopilotConfigStrategy,
)

from airbyte_ops_mcp.airbyte_repo._yaml_helpers import (
    load_metadata_yaml,
    write_metadata_yaml,
)
from airbyte_ops_mcp.airbyte_repo.bump_version import (
    AUTOPILOT_ROLLOUT_MODE,
    MANUAL_ROLLOUT_MODE,
    get_connector_path,
    set_progressive_rollout_flag,
)
from airbyte_ops_mcp.airbyte_repo.list_connectors import METADATA_FILE_NAME

# `AUTOPILOT_ROLLOUT_MODE` / `MANUAL_ROLLOUT_MODE` are defined in `bump_version`
# (the lowest-level rollout module, to avoid a circular import) and re-exported
# here since this module is their primary consumer. Autopilot is the only
# actively-supported rollout mode; the others are being deprecated, so
# "enabling rollouts" for a connector implies autopilot.
__all__ = [
    "AUTOPILOT_ROLLOUT_MODE",
    "MANUAL_ROLLOUT_MODE",
    "DisableAutopilotResult",
    "EnableAutopilotResult",
    "disable_autopilot_rollout",
    "enable_autopilot_rollout",
    "extract_ga_version",
    "is_autopilot_rollout_enabled",
]

# Allowed `autopilotConfig.strategy` values, sourced from the type-safe
# `AutopilotConfigStrategy` enum generated from the connector metadata schema
# (airbyte-connector-models) so they cannot drift from the schema. `"default"`
# is a server-side alias for `"fast"`; callers should prefer the explicit
# `"fast"`.
VALID_STRATEGIES: tuple[str, ...] = tuple(s.value for s in AutopilotConfigStrategy)

# Default strategy when the caller does not specify one. `"fast"` is the
# explicit spelling of the server-side `"default"` alias.
DEFAULT_STRATEGY = AutopilotConfigStrategy.fast.value


def extract_ga_version(rc_version: str) -> str:
    """Extract the GA version from a version string.

    Strips known pre-release suffixes:
    - RC versions (e.g., `1.0.0-rc.1`) → `1.0.0`
    - Preview versions (e.g., `1.0.0-preview.1`) → `1.0.0`

    GA versions without a pre-release suffix are returned as-is.

    Args:
        rc_version: Version string (e.g., "1.0.0-rc.1", "1.0.0-preview.1",
            or "1.0.0")

    Returns:
        GA version string (e.g., "1.0.0")
    """
    if "-rc." in rc_version:
        return rc_version.split("-rc.")[0]
    if "-preview." in rc_version:
        return rc_version.split("-preview.")[0]
    return rc_version


def is_autopilot_rollout_enabled(data: dict) -> bool:
    """Return `True` if a connector's metadata has autopilot rollout fully enabled.

    "Enabled" here means both parts of `releases.rolloutConfiguration` are set
    the way `enable_autopilot_rollout` leaves them:

    - `defaultRolloutMode: autopilot` (the *configuration*), and
    - `enableProgressiveRollout: true` (the *toggle* that actually turns
      automatic progressive rollout on).

    A connector missing either part — or with no `releases.rolloutConfiguration`
    at all — is considered not enabled and returns `False`. `data` is the parsed
    `data` mapping from a connector's `metadata.yaml`.
    """
    releases = data.get("releases")
    if not isinstance(releases, dict):
        return False

    rollout_config = releases.get("rolloutConfiguration")
    if not isinstance(rollout_config, dict):
        return False

    return rollout_config.get("defaultRolloutMode") == AUTOPILOT_ROLLOUT_MODE and bool(
        rollout_config.get("enableProgressiveRollout")
    )


@dataclass
class EnableAutopilotResult:
    """Result of enabling autopilot rollout mode on a connector."""

    connector: str
    modified: bool
    dry_run: bool
    default_rollout_mode: str
    progressive_rollout_enabled: bool
    strategy: str
    auto_start: bool
    auto_promote_stages: bool
    metadata_path: str


@dataclass
class _ResolvedAutopilotConfig:
    """The `autopilotConfig` values written, plus whether anything changed."""

    changed: bool
    strategy: str
    auto_start: bool
    auto_promote_stages: bool


def _set_autopilot_config(
    data: dict,
    *,
    strategy: str | None,
    auto_start: bool | None,
    auto_promote_stages: bool | None,
) -> _ResolvedAutopilotConfig:
    """Set autopilot rollout mode + config in a parsed metadata `data` dict.

    Mutates `data` in place under `releases.rolloutConfiguration`, preserving
    any existing keys (and ruamel formatting) on the surrounding maps.

    Each `autopilotConfig` field is resolved as: the explicit argument if one
    was passed (not `None`), else the existing value already in the metadata,
    else the module default. In other words, defaults only fill in fields that
    are absent — present settings are never overwritten unless the caller passes
    an explicit override. `defaultRolloutMode` is always set to `autopilot`.

    Returns the resolved values and whether any value was changed.
    """
    releases = data.get("releases")
    if not isinstance(releases, dict):
        releases = {}
        data["releases"] = releases

    rollout_config = releases.get("rolloutConfiguration")
    if not isinstance(rollout_config, dict):
        rollout_config = {}
        releases["rolloutConfiguration"] = rollout_config

    changed = False

    if rollout_config.get("defaultRolloutMode") != AUTOPILOT_ROLLOUT_MODE:
        rollout_config["defaultRolloutMode"] = AUTOPILOT_ROLLOUT_MODE
        changed = True

    autopilot_config = rollout_config.get("autopilotConfig")
    if not isinstance(autopilot_config, dict):
        autopilot_config = {}
        rollout_config["autopilotConfig"] = autopilot_config

    defaults: dict[str, object] = {
        "autoStart": True,
        "autoPromoteStages": True,
        "strategy": DEFAULT_STRATEGY,
    }
    overrides: dict[str, object | None] = {
        "autoStart": auto_start,
        "autoPromoteStages": auto_promote_stages,
        "strategy": strategy,
    }
    for key, override in overrides.items():
        if override is not None:
            resolved = override
        elif key in autopilot_config:
            resolved = autopilot_config[key]
        else:
            resolved = defaults[key]

        if autopilot_config.get(key) != resolved or key not in autopilot_config:
            autopilot_config[key] = resolved
            changed = True

    return _ResolvedAutopilotConfig(
        changed=changed,
        strategy=autopilot_config["strategy"],
        auto_start=autopilot_config["autoStart"],
        auto_promote_stages=autopilot_config["autoPromoteStages"],
    )


def enable_autopilot_rollout(
    repo_path: str | Path,
    connector_name: str,
    *,
    strategy: str | None = None,
    auto_start: bool | None = None,
    auto_promote_stages: bool | None = None,
    dry_run: bool = False,
) -> EnableAutopilotResult:
    """Enable autopilot rollout mode in a connector's `metadata.yaml`.

    Enabling does two things:

    - Always sets `releases.rolloutConfiguration.defaultRolloutMode: autopilot`
      (this is what "enable" means) and fills in `autopilotConfig`
      (`autoStart`, `autoPromoteStages`, `strategy`).
    - Sets the `enableProgressiveRollout` toggle to `true`, which is what
      actually turns automatic progressive rollout on.

    Each `autopilotConfig` field is resolved as: the explicit argument if one
    was passed (not `None`), else the value already present in the metadata,
    else the module default (`strategy=fast`, `autoStart=True`,
    `autoPromoteStages=True`). Defaults only fill in fields that are absent, so
    `autopilotConfig` settings already present on the connector are never
    clobbered (only `defaultRolloutMode` is unconditionally set).

    `enableProgressiveRollout` is also toggled per-release by
    `bump_connector_version` (RC bumps set it `true`; `promote` clears it,
    except for autopilot connectors). Enabling here simply guarantees it is on.

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g. `source-github`).
        strategy: Explicit autopilot pacing strategy override. One of `fast`,
            `slow`, `default`. `None` keeps any existing value or the default.
        auto_start: Explicit `autopilotConfig.autoStart` override, or `None`.
        auto_promote_stages: Explicit `autopilotConfig.autoPromoteStages`
            override, or `None`.
        dry_run: When `True`, compute changes without writing the file.

    Returns:
        An `EnableAutopilotResult` describing the applied configuration.

    Raises:
        ConnectorNotFoundError: If the connector directory does not exist.
        FileNotFoundError: If the connector has no `metadata.yaml`.
        ValueError: If `strategy` is not one of the allowed values.
    """
    if strategy is not None and strategy not in VALID_STRATEGIES:
        allowed = ", ".join(repr(s) for s in VALID_STRATEGIES)
        raise ValueError(
            f"Unknown autopilot strategy: {strategy!r}. Must be one of {allowed}."
        )

    connector_path = get_connector_path(repo_path, connector_name)
    metadata_file = connector_path / METADATA_FILE_NAME
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

    metadata = load_metadata_yaml(metadata_file)
    data = metadata.get("data")
    if not isinstance(data, dict):
        data = {}
        metadata["data"] = data

    resolved = _set_autopilot_config(
        data,
        strategy=strategy,
        auto_start=auto_start,
        auto_promote_stages=auto_promote_stages,
    )
    flag_changed = set_progressive_rollout_flag(data, enabled=True)
    changed = resolved.changed or flag_changed

    if changed and not dry_run:
        write_metadata_yaml(metadata, metadata_file)

    return EnableAutopilotResult(
        connector=connector_name,
        modified=changed,
        dry_run=dry_run,
        default_rollout_mode=AUTOPILOT_ROLLOUT_MODE,
        progressive_rollout_enabled=True,
        strategy=resolved.strategy,
        auto_start=resolved.auto_start,
        auto_promote_stages=resolved.auto_promote_stages,
        metadata_path=str(metadata_file),
    )


@dataclass
class DisableAutopilotResult:
    """Result of disabling autopilot rollout mode on a connector."""

    connector: str
    modified: bool
    dry_run: bool
    progressive_rollout_enabled: bool
    metadata_path: str


def _disable_progressive_rollout(data: dict) -> bool:
    """Set `enableProgressiveRollout: false` on an existing `rolloutConfiguration`.

    Only touches connectors that already have a `releases.rolloutConfiguration`
    map with the flag currently enabled; disabling never creates rollout
    configuration where none exists and is a no-op when the flag is already off
    or absent. `defaultRolloutMode` and `autopilotConfig` are left untouched, so
    the configuration is retained (inert) and re-enabling is lossless.

    Returns `True` if any value was changed.
    """
    releases = data.get("releases")
    if not isinstance(releases, dict):
        return False

    rollout_config = releases.get("rolloutConfiguration")
    if not isinstance(rollout_config, dict):
        return False

    if not rollout_config.get("enableProgressiveRollout"):
        return False

    return set_progressive_rollout_flag(data, enabled=False)


def disable_autopilot_rollout(
    repo_path: str | Path,
    connector_name: str,
    *,
    dry_run: bool = False,
) -> DisableAutopilotResult:
    """Disable autopilot rollout for a connector in its `metadata.yaml`.

    Only sets `releases.rolloutConfiguration.enableProgressiveRollout: false` —
    the toggle that turns automatic progressive rollout off. `defaultRolloutMode`
    and any `autopilotConfig` are deliberately left untouched, so the connector's
    configuration is retained (inert) and re-enabling is lossless. Only
    connectors that already have progressive rollout enabled are affected; a
    connector with no rollout config, or with the flag already off, is a no-op
    (`modified=False`).

    Args:
        repo_path: Path to the Airbyte monorepo.
        connector_name: Technical name of the connector (e.g. `source-github`).
        dry_run: When `True`, compute changes without writing the file.

    Returns:
        A `DisableAutopilotResult` describing the applied configuration.

    Raises:
        ConnectorNotFoundError: If the connector directory does not exist.
        FileNotFoundError: If the connector has no `metadata.yaml`.
    """
    connector_path = get_connector_path(repo_path, connector_name)
    metadata_file = connector_path / METADATA_FILE_NAME
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")

    metadata = load_metadata_yaml(metadata_file)
    data = metadata.get("data")
    modified = _disable_progressive_rollout(data) if isinstance(data, dict) else False

    if modified and not dry_run:
        write_metadata_yaml(metadata, metadata_file)

    return DisableAutopilotResult(
        connector=connector_name,
        modified=modified,
        dry_run=dry_run,
        progressive_rollout_enabled=False,
        metadata_path=str(metadata_file),
    )
