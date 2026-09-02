"""Backend-authoritative orchestration for frozen binary updates.

The backend owns version policy. This module compares the resolved target to
the installed version for equality and hands a verified download to a platform
installer. Imports from the original public module remain compatible.
"""

from __future__ import annotations

from collections.abc import Callable
import json
import sys
import tempfile
import time
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from typing import Protocol

import structlog

from runlayer_cli import regex_safe
from runlayer_cli.update_contract import (
    MAX_INSTALLER_SIZE_BYTES as MAX_INSTALLER_SIZE_BYTES,
)
from runlayer_cli.update_contract import (
    Artifact as Artifact,
)
from runlayer_cli.update_contract import (
    TargetRelease as TargetRelease,
)
from runlayer_cli.update_contract import (
    UpdateContractError as UpdateContractError,
)
from runlayer_cli.update_source import (
    SUPPORTED_PACKAGES as SUPPORTED_PACKAGES,
)
from runlayer_cli.update_source import (
    ArtifactVerificationError as ArtifactVerificationError,
)
from runlayer_cli.update_source import (
    BackendUpdateSource as BackendUpdateSource,
)
from runlayer_cli.update_source import (
    UpdateSource as UpdateSource,
)

logger = structlog.get_logger(__name__)
_LOCAL_INSTALLER_FILENAMES = {
    "deb": "installer.deb",
    "msi": "installer.msi",
    "pkg": "installer.pkg",
    "rpm": "installer.rpm",
}
_OUTCOME_MARKER_MAX_AGE_SECONDS = 24 * 60 * 60

__all__ = [
    "Artifact",
    "ArtifactSelectionError",
    "ArtifactVerificationError",
    "BackendUpdateSource",
    "InstallDisposition",
    "InstallTarget",
    "MAX_INSTALLER_SIZE_BYTES",
    "PlatformInstaller",
    "SUPPORTED_PACKAGES",
    "TargetRelease",
    "TargetVersionError",
    "UpdateContractError",
    "UpdateResult",
    "UpdateSource",
    "UpdateStatus",
    "check_and_update",
]


@dataclass(frozen=True)
class InstallTarget:
    platform: str
    arch: str
    format: str
    variant: str | None = None


class InstallDisposition(str, Enum):
    APPLIED = "applied"
    SCHEDULED = "scheduled"


class UpdateStatus(str, Enum):
    NOT_FROZEN = "not_frozen"
    NO_TARGET = "no_target"
    TARGET_BELOW_MINIMUM = "target_below_minimum"
    UP_TO_DATE = "up_to_date"
    SCHEDULED = "scheduled"
    UPDATED = "updated"


@dataclass(frozen=True)
class UpdateResult:
    status: UpdateStatus
    from_version: str
    to_version: str | None = None
    artifact_filename: str | None = None


class PlatformInstaller(Protocol):
    def verify_and_install(
        self,
        artifact_path: Path,
        *,
        artifact: Artifact,
        from_version: str,
        to_version: str,
    ) -> InstallDisposition:
        """Verify vendor identity, then invoke the OS-native installer."""
        ...


class ArtifactSelectionError(RuntimeError):
    """The resolved release has no unambiguous artifact for this device."""


class TargetVersionError(RuntimeError):
    """The resolved release is incompatible with this update entrypoint."""


@dataclass(frozen=True)
class _PendingUpdateOutcome:
    from_version: str
    to_version: str
    scheduled_at: float


def _read_outcome_marker(path: Path) -> _PendingUpdateOutcome:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("outcome marker must be an object")
    from_version = payload.get("from_version")
    to_version = payload.get("to_version")
    scheduled_at = payload.get("scheduled_at")
    if (
        not isinstance(from_version, str)
        or not from_version
        or not isinstance(to_version, str)
        or not to_version
        or isinstance(scheduled_at, bool)
        or not isinstance(scheduled_at, int | float)
    ):
        raise ValueError("outcome marker has invalid fields")
    return _PendingUpdateOutcome(
        from_version=from_version,
        to_version=to_version,
        scheduled_at=float(scheduled_at),
    )


def _consume_outcome_marker(
    path: Path,
    *,
    package: str,
    installed_version: str,
    install_target: InstallTarget,
    clock: Callable[[], float],
) -> None:
    try:
        pending = _read_outcome_marker(path)
    except FileNotFoundError:
        return
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        logger.warning(
            "binary_update_outcome_marker_invalid",
            package=package,
            error=str(exc),
        )
        try:
            path.unlink(missing_ok=True)
        except OSError as unlink_exc:
            logger.warning(
                "binary_update_outcome_marker_clear_failed",
                package=package,
                error=str(unlink_exc),
            )
        return

    try:
        path.unlink()
    except OSError as exc:
        logger.warning(
            "binary_update_outcome_marker_clear_failed",
            package=package,
            error=str(exc),
        )
        return

    if clock() - pending.scheduled_at > _OUTCOME_MARKER_MAX_AGE_SECONDS:
        return

    fields = {
        "package": package,
        "from_version": pending.from_version,
        "to_version": pending.to_version,
        "installed_version": installed_version,
        "platform": install_target.platform,
        "arch": install_target.arch,
        "format": install_target.format,
        "variant": install_target.variant,
    }
    if installed_version == pending.to_version:
        logger.info("binary_update_verified", **fields)
    elif installed_version == pending.from_version:
        logger.warning("binary_update_rollback_suspected", **fields)


def _write_outcome_marker(
    path: Path,
    *,
    from_version: str,
    to_version: str,
    scheduled_at: float,
) -> None:
    payload = {
        "from_version": from_version,
        "scheduled_at": scheduled_at,
        "to_version": to_version,
    }
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            json.dump(payload, temp_file, sort_keys=True)
            temp_file.write("\n")
            temp_path = Path(temp_file.name)
        temp_path.replace(path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


_SEMVER_RE = regex_safe.compile(
    r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


def _version_floor_key(version: str) -> tuple[int, int, int, int]:
    match = _SEMVER_RE.fullmatch(version)
    if match is None:
        raise TargetVersionError(
            f"Backend-selected version {version!r} is not a semantic version"
        )
    major, minor, patch = (int(part) for part in match.groups()[:3])
    is_stable = int(match.group(4) is None)
    return major, minor, patch, is_stable


def _select_artifact(
    target: TargetRelease, install_target: InstallTarget
) -> Artifact | None:
    """Pick the one matching artifact; None means a variant device saw none.

    A variant-marked device must never install a non-matching artifact. An old
    backend ignores the variant query param and serves standard artifacts, so a
    zero-match variant lookup is the expected quiet no-op rather than an error.
    """
    matches = [
        artifact
        for artifact in target.artifacts
        if (
            artifact.platform == install_target.platform
            and artifact.arch == install_target.arch
            and artifact.format == install_target.format
            and artifact.variant == install_target.variant
        )
    ]
    if len(matches) == 0 and install_target.variant is not None:
        return None
    if len(matches) != 1:
        slot = (
            f"{install_target.platform}/{install_target.arch}/{install_target.format}"
        )
        if install_target.variant is not None:
            slot += f" (variant={install_target.variant})"
        raise ArtifactSelectionError(
            f"Expected exactly one installer for {slot}; found {len(matches)}"
        )
    return matches[0]


def check_and_update(
    *,
    package: str,
    installed_version: str,
    installer: PlatformInstaller,
    install_target: InstallTarget,
    source: UpdateSource | None = None,
    host: str | None = None,
    org_api_key: str | None = None,
    frozen: bool | None = None,
    minimum_target_version: str | None = None,
    outcome_marker_path: Path | None = None,
    clock: Callable[[], float] = time.time,
) -> UpdateResult:
    """Apply the backend-resolved version when running as a frozen binary."""
    is_frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    if not is_frozen:
        return UpdateResult(
            status=UpdateStatus.NOT_FROZEN,
            from_version=installed_version,
        )
    if outcome_marker_path is not None:
        _consume_outcome_marker(
            outcome_marker_path,
            package=package,
            installed_version=installed_version,
            install_target=install_target,
            clock=clock,
        )
    target_version: str | None = None
    try:
        if source is None:
            if host is None or org_api_key is None:
                raise ValueError("host and org_api_key are required")
            source = BackendUpdateSource(host=host, org_api_key=org_api_key)
        target = source.fetch_target(package, variant=install_target.variant)
        if target is None:
            return UpdateResult(
                status=UpdateStatus.NO_TARGET,
                from_version=installed_version,
            )
        target_version = target.version
        if target.version == installed_version:
            return UpdateResult(
                status=UpdateStatus.UP_TO_DATE,
                from_version=installed_version,
                to_version=target.version,
            )
        if minimum_target_version is not None and _version_floor_key(
            target.version
        ) < _version_floor_key(minimum_target_version):
            logger.info(
                "binary_update_target_below_minimum",
                package=package,
                from_version=installed_version,
                to_version=target.version,
                minimum_target_version=minimum_target_version,
            )
            return UpdateResult(
                status=UpdateStatus.TARGET_BELOW_MINIMUM,
                from_version=installed_version,
                to_version=target.version,
            )
        log_fields = {
            "package": package,
            "from_version": installed_version,
            "to_version": target.version,
            "platform": install_target.platform,
            "arch": install_target.arch,
            "format": install_target.format,
            "variant": install_target.variant,
        }
        artifact = _select_artifact(target, install_target)
        if artifact is None:
            logger.info("binary_update_no_variant_target", **log_fields)
            return UpdateResult(
                status=UpdateStatus.NO_TARGET,
                from_version=installed_version,
            )
        logger.info("binary_update_attempt", **log_fields)
        local_filename = _LOCAL_INSTALLER_FILENAMES.get(artifact.format)
        if local_filename is None:
            raise ArtifactSelectionError(
                f"Unsupported installer format {artifact.format!r}"
            )
        local_artifact = replace(artifact, filename=local_filename)
        with tempfile.TemporaryDirectory(prefix="runlayer-update-") as temp_dir:
            artifact_path = Path(temp_dir) / local_filename
            source.download(package, target.version, artifact, artifact_path)
            disposition = installer.verify_and_install(
                artifact_path,
                artifact=local_artifact,
                from_version=installed_version,
                to_version=target.version,
            )
        if disposition is InstallDisposition.SCHEDULED:
            status = UpdateStatus.SCHEDULED
            logger.info("binary_update_scheduled", **log_fields)
            if outcome_marker_path is not None:
                try:
                    _write_outcome_marker(
                        outcome_marker_path,
                        from_version=installed_version,
                        to_version=target.version,
                        scheduled_at=clock(),
                    )
                except OSError as exc:
                    logger.warning(
                        "binary_update_outcome_marker_write_failed",
                        **log_fields,
                        error=str(exc),
                    )
        elif disposition is InstallDisposition.APPLIED:
            status = UpdateStatus.UPDATED
            logger.info("binary_update_success", **log_fields)
        else:
            raise RuntimeError("Native installer returned an invalid disposition")
        return UpdateResult(
            status=status,
            from_version=installed_version,
            to_version=target.version,
            artifact_filename=artifact.filename,
        )
    except Exception as exc:
        logger.error(
            "binary_update_failure",
            package=package,
            from_version=installed_version,
            to_version=target_version,
            platform=install_target.platform,
            arch=install_target.arch,
            format=install_target.format,
            variant=install_target.variant,
            error=str(exc),
        )
        raise
