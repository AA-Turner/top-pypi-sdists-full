"""Validated backend contract for binary update targets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast


MAX_INSTALLER_SIZE_BYTES = 512 * 1024 * 1024
SUPPORTED_ARTIFACT_FORMATS = frozenset({"deb", "msi", "pkg", "rpm"})


@dataclass(frozen=True)
class Artifact:
    platform: str
    arch: str
    filename: str
    sha256: str
    size_bytes: int
    format: str
    variant: str | None = None


@dataclass(frozen=True)
class TargetRelease:
    version: str
    artifacts: tuple[Artifact, ...]


class UpdateContractError(RuntimeError):
    """The backend returned an invalid or ambiguous update contract."""


def _required_string(mapping: dict[str, object], field: str) -> str:
    value = mapping.get(field)
    if not isinstance(value, str) or not value:
        raise UpdateContractError(f"Update target {field!r} must be a non-empty string")
    return value


def _parse_artifact(raw: object) -> Artifact:
    if not isinstance(raw, dict):
        raise UpdateContractError("Update target artifact must be an object")
    artifact_data = cast(dict[str, object], raw)
    size_bytes = artifact_data.get("size_bytes")
    if isinstance(size_bytes, bool) or not isinstance(size_bytes, int):
        raise UpdateContractError("Update target size_bytes must be an integer")
    artifact_format = _required_string(artifact_data, "format")
    if artifact_format not in SUPPORTED_ARTIFACT_FORMATS:
        raise UpdateContractError(
            f"Update target format {artifact_format!r} is not supported"
        )
    variant = artifact_data.get("variant")
    if variant is not None and (not isinstance(variant, str) or not variant):
        raise UpdateContractError(
            "Update target variant must be a non-empty string when present"
        )
    artifact = Artifact(
        platform=_required_string(artifact_data, "platform"),
        arch=_required_string(artifact_data, "arch"),
        filename=_required_string(artifact_data, "filename"),
        sha256=_required_string(artifact_data, "sha256").lower(),
        size_bytes=size_bytes,
        format=artifact_format,
        variant=variant,
    )
    if (
        artifact.filename in {".", ".."}
        or Path(artifact.filename).name != artifact.filename
        or "/" in artifact.filename
        or "\\" in artifact.filename
    ):
        raise UpdateContractError("Update target filename must be a basename")
    if len(artifact.sha256) != 64:
        raise UpdateContractError(
            "Update target sha256 must be a 64-character hex digest"
        )
    try:
        int(artifact.sha256, 16)
    except ValueError as exc:
        raise UpdateContractError("Update target sha256 must be hexadecimal") from exc
    if artifact.size_bytes < 0:
        raise UpdateContractError("Update target size_bytes must not be negative")
    if artifact.size_bytes > MAX_INSTALLER_SIZE_BYTES:
        raise UpdateContractError(
            "Update target size_bytes exceeds the maximum installer size"
        )
    return artifact


def parse_target(payload: object, package: str) -> TargetRelease | None:
    """Extract one package's resolved target from the collection response."""
    if not isinstance(payload, dict):
        raise UpdateContractError("Binary package response must contain a data list")
    payload_data = cast(dict[str, object], payload)
    rows = payload_data.get("data")
    if not isinstance(rows, list):
        raise UpdateContractError("Binary package response must contain a data list")
    package_rows: list[dict[str, object]] = []
    for raw_row in rows:
        if not isinstance(raw_row, dict):
            continue
        row = cast(dict[str, object], raw_row)
        if row.get("package") == package:
            package_rows.append(row)
    if len(package_rows) != 1:
        raise UpdateContractError(
            f"Expected exactly one binary package row for {package!r}; "
            f"found {len(package_rows)}"
        )
    package_row = package_rows[0]
    if "resolved_target" not in package_row:
        raise UpdateContractError("Binary package row must contain resolved_target")
    raw_target = package_row["resolved_target"]
    if raw_target is None:
        return None
    if not isinstance(raw_target, dict):
        raise UpdateContractError("resolved_target must be an object or null")
    target_data = cast(dict[str, object], raw_target)
    raw_artifacts = target_data.get("artifacts")
    if not isinstance(raw_artifacts, list):
        raise UpdateContractError("resolved_target artifacts must be a list")
    return TargetRelease(
        version=_required_string(target_data, "version"),
        artifacts=tuple(_parse_artifact(raw) for raw in raw_artifacts),
    )
