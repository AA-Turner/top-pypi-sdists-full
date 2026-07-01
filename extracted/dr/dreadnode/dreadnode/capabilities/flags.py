"""
Capability flag definitions, validation, and resolution — v1 spec.

See specs/capabilities/flags.md for the canonical rules (CAP-FLAG-*).
"""

import os
import re
import typing as t
from dataclasses import dataclass
from pathlib import Path

FLAG_NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
MAX_FLAGS = 16
_VALID_FLAG_FIELDS = {"description", "default"}
_TRUTHY = {"1", "true", "on"}
_FALSY = {"0", "false", "off"}


@dataclass
class FlagDef:
    """Author-declared flag from capability.yaml."""

    name: str
    description: str
    default: bool = False


@dataclass
class ResolvedFlag:
    """Effective flag state after merging the four-layer override stack."""

    name: str
    description: str
    default: bool
    effective: bool
    source: t.Literal["default", "binding", "env", "cli"]


# ============================================================================
# Validation (CAP-FLAG-001 through CAP-FLAG-005)
# ============================================================================


def validate_flags_block(
    raw: dict[str, t.Any] | None,
    manifest_path: Path,
) -> list[FlagDef]:
    """Validate the top-level ``flags`` block and return parsed definitions.

    Returns an empty list when *raw* is None or ``{}``.
    """
    if raw is None or (isinstance(raw, dict) and not raw):
        return []

    if not isinstance(raw, dict):
        raise ValueError(f"'flags' must be a mapping in {manifest_path} [CAP-FLAG-001]")  # noqa: TRY004

    if len(raw) > MAX_FLAGS:
        raise ValueError(
            f"Capability declares {len(raw)} flags, maximum is {MAX_FLAGS} "
            f"in {manifest_path} [CAP-FLAG-005]"
        )

    defs: list[FlagDef] = []
    for name, entry in raw.items():
        if not isinstance(name, str) or not FLAG_NAME_PATTERN.match(name):
            raise ValueError(
                f"Flag name {name!r} must match [a-z0-9]([a-z0-9-]*[a-z0-9])? "
                f"in {manifest_path} [CAP-FLAG-001]"
            )
        if not isinstance(entry, dict):
            raise ValueError(f"Flag '{name}' must be a mapping in {manifest_path} [CAP-FLAG-001]")  # noqa: TRY004
        unknown = set(entry.keys()) - _VALID_FLAG_FIELDS
        if unknown:
            raise ValueError(
                f"Flag '{name}' has unknown fields {unknown} in {manifest_path} [CAP-FLAG-004]"
            )
        if (
            "description" not in entry
            or not isinstance(entry["description"], str)
            or not entry["description"].strip()
        ):
            raise ValueError(
                f"Flag '{name}' requires a non-empty 'description' "
                f"in {manifest_path} [CAP-FLAG-002]"
            )
        default = entry.get("default", False)
        if not isinstance(default, bool):
            raise ValueError(  # noqa: TRY004
                f"Flag '{name}' default must be a boolean in {manifest_path} [CAP-FLAG-002]"
            )
        defs.append(FlagDef(name=name, description=entry["description"], default=default))

    return defs


# ============================================================================
# when: predicate validation (CAP-FLAG-010 through CAP-FLAG-013, CAP-FLAG-080)
# ============================================================================


def validate_when(
    when: t.Any,
    declared_flags: set[str],
    component_name: str,
    manifest_path: Path,
    *,
    source: str = "inline",
    component_kind: str = "MCP server",
) -> list[str] | None:
    """Validate a ``when`` predicate on a gate-eligible component (MCP server or worker).

    Returns the validated flag-name list, or None for "always load".
    """
    if source == "file" and when is not None:
        raise ValueError(
            f"{component_kind} '{component_name}' loaded from file must not have 'when' "
            f"in {manifest_path} [CAP-FLAG-010]"
        )

    if when is None:
        return None

    if not isinstance(when, list):
        raise ValueError(  # noqa: TRY004
            f"{component_kind} '{component_name}' 'when' must be a list of flag names "
            f"in {manifest_path} [CAP-FLAG-080]"
        )

    if len(when) == 0:
        raise ValueError(
            f"{component_kind} '{component_name}' 'when' must not be empty "
            f"in {manifest_path} [CAP-FLAG-080]"
        )

    validated: list[str] = []
    for flag_name in when:
        if not isinstance(flag_name, str):
            raise ValueError(  # noqa: TRY004
                f"{component_kind} '{component_name}' 'when' entries must be strings "
                f"in {manifest_path} [CAP-FLAG-080]"
            )
        if flag_name not in declared_flags:
            raise ValueError(
                f"{component_kind} '{component_name}' references undeclared flag '{flag_name}' "
                f"in {manifest_path} [CAP-FLAG-012]"
            )
        validated.append(flag_name)

    return validated


# ============================================================================
# Env var naming (CAP-FLAG-020 through CAP-FLAG-024)
# ============================================================================


def _to_upper_snake(name: str) -> str:
    """Convert a kebab-case name to UPPER_SNAKE_CASE."""
    return name.upper().replace("-", "_")


def flag_to_env_name(capability_name: str, flag_name: str) -> str:
    """Convention env var injected into MCP subprocesses and tool imports (CAP-FLAG-021)."""
    return f"CAPABILITY_FLAG__{_to_upper_snake(capability_name)}__{_to_upper_snake(flag_name)}"


def override_env_name(capability_name: str, flag_name: str) -> str:
    """User-facing override env var (CAP-FLAG-032)."""
    return f"DREADNODE_CAPABILITY_FLAG__{_to_upper_snake(capability_name)}__{_to_upper_snake(flag_name)}"


# ============================================================================
# Resolution (CAP-FLAG-030 through CAP-FLAG-034)
# ============================================================================


def resolve_flags(
    flag_defs: list[FlagDef],
    persisted: dict[str, bool] | None = None,
    env_overrides: dict[str, bool] | None = None,
    cli_overrides: dict[str, bool] | None = None,
) -> list[ResolvedFlag]:
    """Resolve effective state for each declared flag via the four-layer stack."""
    persisted = persisted if isinstance(persisted, dict) else {}
    env_overrides = env_overrides if isinstance(env_overrides, dict) else {}
    cli_overrides = cli_overrides if isinstance(cli_overrides, dict) else {}

    results: list[ResolvedFlag] = []
    for flag in flag_defs:
        effective = flag.default
        source: t.Literal["default", "binding", "env", "cli"] = "default"

        if flag.name in persisted and isinstance(persisted[flag.name], bool):
            effective = persisted[flag.name]
            source = "binding"

        if flag.name in env_overrides and isinstance(env_overrides[flag.name], bool):
            effective = env_overrides[flag.name]
            source = "env"

        if flag.name in cli_overrides and isinstance(cli_overrides[flag.name], bool):
            effective = cli_overrides[flag.name]
            source = "cli"

        results.append(
            ResolvedFlag(
                name=flag.name,
                description=flag.description,
                default=flag.default,
                effective=effective,
                source=source,
            )
        )
    return results


def read_env_overrides(
    capability_name: str,
    flag_defs: list[FlagDef],
) -> dict[str, bool]:
    """Read ``DREADNODE_CAPABILITY_FLAG__*`` overrides from ``os.environ`` (CAP-FLAG-032)."""
    from loguru import logger

    overrides: dict[str, bool] = {}
    for flag in flag_defs:
        env_name = override_env_name(capability_name, flag.name)
        raw = os.environ.get(env_name)
        if raw is None:
            continue
        low = raw.strip().lower()
        if low in _TRUTHY:
            overrides[flag.name] = True
        elif low in _FALSY:
            overrides[flag.name] = False
        else:
            logger.warning(
                "Ignoring invalid value for {}: {!r} (expected 1/true/on or 0/false/off)",
                env_name,
                raw,
            )
    return overrides


def parse_cli_flags(raw: list[str] | None) -> dict[str, dict[str, bool]]:
    """Parse ``--capability-flag capability.flag=true|false`` values (CAP-FLAG-033)."""
    from loguru import logger

    if not raw:
        return {}

    result: dict[str, dict[str, bool]] = {}
    for item in raw:
        if "=" not in item:
            logger.warning(
                "Ignoring malformed --capability-flag: {!r} (expected cap.flag=bool)", item
            )
            continue
        path, value_str = item.split("=", 1)
        if "." not in path:
            logger.warning(
                "Ignoring malformed --capability-flag: {!r} (expected cap.flag=bool)", item
            )
            continue
        cap_name, flag_name = path.split(".", 1)
        if "." in flag_name:
            logger.warning("Ignoring malformed --capability-flag: {!r} (extra dots in path)", item)
            continue
        low = value_str.strip().lower()
        if low in _TRUTHY:
            result.setdefault(cap_name, {})[flag_name] = True
        elif low in _FALSY:
            result.setdefault(cap_name, {})[flag_name] = False
        else:
            logger.warning(
                "Ignoring invalid --capability-flag value: {!r} (expected true/false)",
                item,
            )
    return result


# ============================================================================
# when: predicate evaluation (CAP-FLAG-011, CAP-FLAG-014)
# ============================================================================


def evaluate_when(
    when: list[str] | None,
    resolved: list[ResolvedFlag],
) -> bool:
    """Evaluate a ``when`` predicate against resolved flag state.

    Returns True if the component should be loaded (CAP-FLAG-011).
    """
    if when is None:
        return True
    effective = {f.name: f.effective for f in resolved}
    return any(effective.get(name, False) for name in when)
