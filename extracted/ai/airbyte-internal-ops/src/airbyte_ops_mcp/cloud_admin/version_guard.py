# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Existing-pin guard for connector version overrides.

Prevents accidentally overwriting existing version pins when pinning connectors.
An existing pin at any scope (actor, workspace, or organization) indicates that
someone (a human, a rollout, or a breaking-change migration) intentionally set
the version — overwriting it without awareness could break customer syncs or
interfere with ongoing operations.

Two independent checks are enforced:

1. **Existing-pin check** — blocks overwriting any existing pin.  Can be
   bypassed with `force=True`.
2. **Major-version check** — blocks pinning across a major-version boundary
   (e.g. v2 -> v3).  This is a *hard* blocker with **no override** because
   major-version bumps in Airbyte connectors indicate breaking changes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import semver

from airbyte_ops_mcp.cloud_admin.api_client import (
    _get_scoped_configuration_context,
    _ScopeType,
)

logger = logging.getLogger(__name__)


@dataclass
class PinGuardResult:
    """Result of an existing-pin guard check.

    Attributes:
        error_msg: If set, the operation should be blocked with this message.
    """

    error_msg: str | None = None

    @property
    def blocked(self) -> bool:
        return self.error_msg is not None


def check_existing_pins(
    *,
    scopes: list[tuple[_ScopeType, str, str]],
    actor_definition_id: str,
    config_api_root: str,
    access_token: str,
    target_version: str,
    force: bool,
) -> PinGuardResult:
    """Check scoped configurations for an existing pin and validate the override.

    Iterates through *scopes* in precedence order (actor > workspace > org)
    and stops at the first pin found.

    Args:
        scopes: Ordered list of `(scope_type_enum, scope_id, scope_label)`
            tuples to check.
        actor_definition_id: Connector definition UUID.
        config_api_root: Config API root URL.
        access_token: Pre-authenticated bearer token.
        target_version: The version string being pinned to.
        force: Whether the caller is forcing the override.

    Returns:
        A `PinGuardResult` with `error_msg` set when the operation
        should be blocked.
    """
    for scope_type_enum, scope_id, scope_label in scopes:
        existing_config = _get_scoped_configuration_context(
            actor_definition_id=actor_definition_id,
            scope_type=scope_type_enum,
            scope_id=scope_id,
            config_api_root=config_api_root,
            access_token=access_token,
        )
        if not existing_config:
            continue

        existing_scope = existing_config.get("scope_type", scope_label)
        existing_version = existing_config.get("value_name")

        # Check 1: existing-pin guard (bypassable with force=True)
        error_msg = _validate_not_already_pinned(
            is_pinned=True,
            pinned_version=existing_version,
            pin_scope=existing_scope,
            force=force,
            target_version=target_version,
        )
        if error_msg:
            return PinGuardResult(error_msg=error_msg)

        # Check 2: major-version hard blocker (NOT bypassable, even with force)
        if existing_version:
            major_error = _check_major_version_crossing(
                existing_pinned_version=existing_version,
                target_version=target_version,
            )
            if major_error:
                return PinGuardResult(error_msg=major_error)

        return PinGuardResult()

    return PinGuardResult()


def _validate_not_already_pinned(
    *,
    is_pinned: bool,
    pinned_version: str | None = None,
    pin_scope: str | None = None,
    force: bool,
    target_version: str | None = None,
) -> str | None:
    """Check if a connector is already pinned and block the override unless forced.

    This guard prevents accidentally overwriting an existing version pin.
    Existing pins may have been set by rollouts, breaking-change migrations,
    or other operators — overwriting them without awareness is dangerous.

    `force=True` bypasses this check only.  Major-version crossings are
    enforced separately by `_check_major_version_crossing` and cannot be
    overridden.

    Args:
        is_pinned: Whether the connector already has a version pin applied.
        pinned_version: The current pinned version string, if known.
        pin_scope: The scope of the existing pin (e.g., `"actor"`,
            `"workspace"`, `"organization"`), if known.
        force: If `True`, allow overwriting the existing pin.
        target_version: The version being pinned to, used for major-version
            crossing detection in the error message.

    Returns:
        An error message string if the override is blocked, or `None` if allowed.
    """
    if force:
        return None

    if not is_pinned:
        return None

    parts = ["Version override rejected: this connector is already pinned"]
    if pinned_version:
        parts.append(f"to version {pinned_version}")
    if pin_scope:
        parts.append(f"at {pin_scope} scope")
    parts.append(
        "— overwriting an existing pin may interfere with an ongoing rollout, "
        "a breaking-change migration, or another operator's work. "
        "Use force=True to override."
    )

    error_msg = " ".join(parts)

    # Append major-version crossing note if applicable
    if target_version and pinned_version:
        crossing_msg = _check_major_version_crossing(
            existing_pinned_version=pinned_version,
            target_version=target_version,
        )
        if crossing_msg:
            error_msg = (
                f"{error_msg} NOTE: Even with force=True, this operation "
                f"would still be blocked because it crosses a major version "
                f"boundary (see below). {crossing_msg}"
            )

    return error_msg


def _check_major_version_crossing(
    *,
    existing_pinned_version: str | None,
    target_version: str,
) -> str | None:
    """Return an error string if the override crosses a major version boundary.

    This is a **hard blocker** — major-version crossings are never allowed,
    even with `force=True`.  Major-version bumps in Airbyte connectors
    indicate breaking changes (schema, config, or state format changes),
    and the correct path is to advance the actor to the new major version
    through the normal upgrade/migration process before pinning.

    Args:
        existing_pinned_version: The version string of the existing pin,
            or `None` if unknown.
        target_version: The target version string being pinned to.

    Returns:
        An error string if a major-version boundary is crossed,
        or `None` if no crossing is detected or versions cannot be parsed.
    """
    if not existing_pinned_version:
        return None

    try:
        existing = semver.Version.parse(existing_pinned_version)
    except ValueError:
        logger.debug(
            "Cannot parse existing pinned version '%s' as semver; "
            "skipping major-version crossing check.",
            existing_pinned_version,
        )
        return None

    try:
        target = semver.Version.parse(target_version)
    except ValueError:
        logger.debug(
            "Cannot parse target version '%s' as semver; "
            "skipping major-version crossing check.",
            target_version,
        )
        return None

    if existing.major != target.major:
        return (
            f"Version override blocked: this operation crosses a major version "
            f"boundary (v{existing.major} -> v{target.major}). Major version "
            f"bumps in Airbyte connectors indicate breaking changes (schema "
            f"changes, config changes, state format changes). This check "
            f"cannot be overridden — advance the actor to the target major "
            f"version through the normal upgrade/migration process first."
        )

    return None
