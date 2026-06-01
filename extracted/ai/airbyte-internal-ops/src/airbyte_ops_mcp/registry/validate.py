# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Metadata validation for connector version artifacts.

This module provides validators that check connector metadata for correctness
before publishing. Validators are designed to be run:

1. After `artifacts generate` (to catch issues before uploading).
2. Before `artifacts publish` (as a pre-flight gate).

Each validator is a callable that accepts raw metadata (`dict`) and an
options object, returning a `(passed, error_message)` tuple.
"""

from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass, field
from typing import Any

import semver

from airbyte_ops_mcp.registry._constants import ALLOW_GA_PROGRESSIVE_ROLLOUT

logger = logging.getLogger(__name__)

# Source-declarative-manifest is exempt from breaking-change checks.
_SOURCE_DECLARATIVE_MANIFEST_DEFINITION_ID = "64a2f99c-542f-4af8-9a6f-355f1217b436"


# ---------------------------------------------------------------------------
# Options & result models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ValidateOptions:
    """Options that influence which validators run and how."""

    docs_path: str | None = None
    """Path to the connector's documentation file (for `validate_docs_path_exists`)."""

    is_prerelease: bool = False
    """Whether this is a pre-release build (skips version-decrement checks)."""


@dataclass
class ValidationResult:
    """Aggregate result from running all validators."""

    passed: bool = True
    errors: list[str] = field(default_factory=list)
    validators_run: int = 0

    def add_error(self, message: str) -> None:
        self.passed = False
        self.errors.append(message)


# ---------------------------------------------------------------------------
# Individual validators
# ---------------------------------------------------------------------------


def validate_all_tags_are_keyvalue_pairs(
    metadata_data: dict[str, Any],
    _opts: ValidateOptions,
) -> tuple[bool, str | None]:
    """All tags must be `KEY:VALUE` pairs."""
    tags = metadata_data.get("tags", [])
    for tag in tags:
        if ":" not in str(tag):
            return False, f"Tag '{tag}' is not of the form KEY:VALUE."
    return True, None


def validate_at_least_one_language_tag(
    metadata_data: dict[str, Any],
    _opts: ValidateOptions,
) -> tuple[bool, str | None]:
    """At least one tag must be `language:<LANG>`."""
    tags = metadata_data.get("tags", [])
    if not any(str(t).startswith("language:") for t in tags):
        return False, "At least one tag must be of the form language:<LANG>."
    return True, None


def _is_major_version(version: str) -> bool:
    """Return True if *version* is `N.0.0` where N > 0 (no pre-release)."""
    try:
        sv = semver.Version.parse(version)
    except ValueError:
        return False
    return sv.major > 0 and sv.minor == 0 and sv.patch == 0 and sv.prerelease is None


def validate_major_version_bump_has_breaking_change_entry(
    metadata_data: dict[str, Any],
    _opts: ValidateOptions,
) -> tuple[bool, str | None]:
    """Major version bumps (N.0.0) must have a `breakingChanges` entry."""
    image_tag = metadata_data.get("dockerImageTag", "")
    if not image_tag or not _is_major_version(image_tag):
        return True, None

    # source-declarative-manifest is exempt.
    if (
        str(metadata_data.get("definitionId", ""))
        == _SOURCE_DECLARATIVE_MANIFEST_DEFINITION_ID
    ):
        return True, None

    releases = metadata_data.get("releases")
    if not releases:
        return (
            False,
            f"Major version bump ({image_tag}) requires a 'releases' property with 'breakingChanges' entries.",
        )

    breaking_changes = (
        releases.get("breakingChanges") if isinstance(releases, dict) else None
    )
    if breaking_changes is None or image_tag not in breaking_changes:
        return (
            False,
            f"Major version {image_tag} requires a 'releases.breakingChanges' entry.",
        )

    return True, None


def validate_docs_path_exists(
    _metadata_data: dict[str, Any],
    opts: ValidateOptions,
) -> tuple[bool, str | None]:
    """The documentation file must exist on disk."""
    if opts.docs_path is None:
        # Cannot check without a path — skip silently.
        return True, None
    if not pathlib.Path(opts.docs_path).exists():
        return False, f"Documentation file not found: {opts.docs_path}."
    return True, None


def validate_pypi_only_for_python(
    metadata_data: dict[str, Any],
    _opts: ValidateOptions,
) -> tuple[bool, str | None]:
    """PyPI publishing requires a `language:python` or `language:low-code` tag."""
    pypi_enabled = (
        (metadata_data.get("remoteRegistries") or {})
        .get("pypi", {})
        .get("enabled", False)
    )
    if not pypi_enabled:
        return True, None

    tags = metadata_data.get("tags", [])
    if "language:python" not in tags and "language:low-code" not in tags:
        return (
            False,
            "PyPI publishing enabled but connector lacks a python/low-code language tag.",
        )
    return True, None


def _is_release_candidate(version: str) -> bool:
    try:
        sv = semver.Version.parse(version)
    except ValueError:
        return False
    return sv.prerelease is not None and "rc" in sv.prerelease


def _is_major_rc(version: str) -> bool:
    if not _is_release_candidate(version):
        return False
    try:
        sv = semver.Version.parse(version)
    except ValueError:
        return False
    return sv.major > 0 and sv.minor == 0 and sv.patch == 0


def validate_version_and_progressive_rollout_configuration(
    metadata_data: dict[str, Any],
    opts: ValidateOptions,
) -> tuple[bool, str | None]:
    """Validate version vs progressive rollout configuration.

    RC versions (`-rc.N`) require `enableProgressiveRollout` to be set.
    GA versions with `enableProgressiveRollout` are gated behind the
    `ALLOW_GA_PROGRESSIVE_ROLLOUT` flag (default `False`).
    """
    if opts.is_prerelease:
        return True, None

    docker_image_tag = metadata_data.get("dockerImageTag")
    if not docker_image_tag:
        return False, "The dockerImageTag field is not set."

    try:
        # Validate semver upfront so invalid tags are rejected.
        semver.Version.parse(docker_image_tag)

        is_major_rc = _is_major_rc(docker_image_tag)
        is_rc = _is_release_candidate(docker_image_tag)

        rollout_cfg = (metadata_data.get("releases") or {}).get(
            "rolloutConfiguration", {}
        )
        enabled_progressive = (
            rollout_cfg.get("enableProgressiveRollout") if rollout_cfg else None
        )

        if is_major_rc:
            return (
                False,
                "Release candidates for major versions (with breaking changes) are not allowed.",
            )

        if is_rc and enabled_progressive is None:
            return (
                False,
                "RC version requires releases.rolloutConfiguration.enableProgressiveRollout.",
            )

        # GA versions with enableProgressiveRollout=true are gated behind
        # the ALLOW_GA_PROGRESSIVE_ROLLOUT flag.  When the flag is False
        # (the default), the pre-#623 behaviour is preserved: only RC
        # versions may set this field.
        # Tracking issue: https://github.com/airbytehq/airbyte-ops-mcp/issues/646
        if (
            not ALLOW_GA_PROGRESSIVE_ROLLOUT
            and enabled_progressive is True
            and not is_rc
        ):
            return (
                False,
                "GA progressive rollout is not yet enabled. "
                "The enableProgressiveRollout flag requires an RC version suffix.",
            )
    except ValueError:
        return False, f"Invalid semver version: {docker_image_tag}."

    return True, None


# ---------------------------------------------------------------------------
# Validator registry
# ---------------------------------------------------------------------------

#: Validators to run before publishing artifacts.
PRE_PUBLISH_VALIDATORS = [
    validate_all_tags_are_keyvalue_pairs,
    validate_at_least_one_language_tag,
    validate_major_version_bump_has_breaking_change_entry,
    validate_docs_path_exists,
    validate_pypi_only_for_python,
    validate_version_and_progressive_rollout_configuration,
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_metadata(
    metadata_data: dict[str, Any],
    opts: ValidateOptions | None = None,
) -> ValidationResult:
    """Run all pre-publish validators against raw `metadata.data`.

    Args:
        metadata_data: The `data` section of a parsed `metadata.yaml`.
        opts: Options influencing validation behaviour.

    Returns:
        A `ValidationResult` with aggregate pass/fail and error list.
    """
    if opts is None:
        opts = ValidateOptions()

    result = ValidationResult()

    for validator in PRE_PUBLISH_VALIDATORS:
        result.validators_run += 1
        logger.info("Running validator: %s", validator.__name__)
        passed, error = validator(metadata_data, opts)
        if not passed and error:
            logger.error("Validation failed: %s", error)
            result.add_error(error)

    return result
