"""macOS package verification and installation."""

from __future__ import annotations

import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from pathlib import Path
from typing import TypedDict

from runlayer_cli import regex_safe
from runlayer_cli.installer_common import (
    CommandRunner,
    InstallerVerificationError,
    combined_output,
    default_command_runner,
    posix_installer_environment,
    run_checked,
    validate_artifact,
)
from runlayer_cli.updater import Artifact, InstallDisposition

MACOS_DEVELOPER_TEAM_ID = "AF2M8HC7A2"


class _PackageMetadata(TypedDict):
    identifiers: frozenset[str]
    versions: frozenset[str]
    architectures: frozenset[str]


def _read_package_metadata(
    path: Path,
    runner: CommandRunner,
    env: Mapping[str, str],
) -> _PackageMetadata:
    """Expand a verified product archive and read signed package metadata."""
    with tempfile.TemporaryDirectory(prefix="runlayer-pkg-identity-") as temp_dir:
        expanded = Path(temp_dir) / "expanded"
        run_checked(
            runner,
            ["/usr/sbin/pkgutil", "--expand", str(path), str(expanded)],
            verification=True,
            env=env,
        )
        try:
            package_roots = [
                ET.parse(package_info).getroot()
                for package_info in expanded.rglob("PackageInfo")
            ]
            distribution = ET.parse(expanded / "Distribution").getroot()
        except (OSError, ET.ParseError) as exc:
            raise InstallerVerificationError(
                "macOS package identity metadata is invalid"
            ) from exc
        options = distribution.find("options")
        architecture_value = (
            options.get("hostArchitectures") if options is not None else None
        )
        if (
            not package_roots
            or any(
                not root.get("identifier") or not root.get("version")
                for root in package_roots
            )
            or not architecture_value
        ):
            raise InstallerVerificationError(
                "macOS package identity metadata is invalid"
            )
        architectures = frozenset(
            value
            # STDLIB_WS, not `\s`: RE2's is ASCII-only, so an NBSP between
            # tokens would yield one unsplit member and fail the identity check.
            for value in regex_safe.split(
                rf"[{regex_safe.STDLIB_WS_BODY},]+", architecture_value
            )
            if value
        )
        if not architectures:
            raise InstallerVerificationError(
                "macOS package identity metadata is invalid"
            )
        return {
            "identifiers": frozenset(
                root.get("identifier", "") for root in package_roots
            ),
            "versions": frozenset(root.get("version", "") for root in package_roots),
            "architectures": architectures,
        }


class MacOSPackageInstaller:
    """Verify Developer ID + notarization, then install a macOS package."""

    def __init__(
        self,
        *,
        package_id: str,
        runner: CommandRunner = default_command_runner,
    ) -> None:
        if not package_id:
            raise ValueError("macOS package identifier is required")
        self._package_id = package_id
        self._runner = runner

    def verify_and_install(
        self,
        artifact_path: Path,
        *,
        artifact: Artifact,
        from_version: str,
        to_version: str,
    ) -> InstallDisposition:
        del from_version
        path = validate_artifact(
            artifact_path,
            artifact,
            platform="macos",
            formats=("pkg",),
        )
        env = posix_installer_environment()
        signature = run_checked(
            self._runner,
            ["/usr/sbin/pkgutil", "--check-signature", str(path)],
            verification=True,
            env=env,
        )
        signature_output = combined_output(signature)
        # pkgutil's Status prose varies by macOS release. Its successful exit
        # plus the exact leaf below pins the team; spctl then proves notarization.
        expected_leaf = regex_safe.search(
            rf"(?m)^\s*1\.\s+Developer ID Installer:[^\r\n]*"
            rf"\({regex_safe.escape(MACOS_DEVELOPER_TEAM_ID)}\)\s*$",
            signature_output,
        )
        if expected_leaf is None:
            raise InstallerVerificationError(
                "macOS package is not signed by the Runlayer Developer ID Installer "
                f"team {MACOS_DEVELOPER_TEAM_ID}"
            )

        assessment = run_checked(
            self._runner,
            [
                "/usr/sbin/spctl",
                "--assess",
                "--type",
                "install",
                "--verbose=4",
                str(path),
            ],
            verification=True,
            env=env,
        )
        if (
            regex_safe.search(
                r"(?im)^\s*source=Notarized Developer ID\s*$",
                combined_output(assessment),
            )
            is None
        ):
            raise InstallerVerificationError(
                "macOS package did not pass a notarized Developer ID assessment"
            )

        metadata = _read_package_metadata(path, self._runner, env)
        if metadata["identifiers"] != {self._package_id}:
            raise InstallerVerificationError(
                "macOS package component identifier does not match the requested product"
            )
        if metadata["versions"] != {to_version}:
            raise InstallerVerificationError(
                "macOS package version does not match the backend-selected version"
            )
        if metadata["architectures"] != {artifact.arch}:
            raise InstallerVerificationError(
                "macOS package architecture does not match the requested target"
            )

        run_checked(
            self._runner,
            ["/usr/sbin/installer", "-pkg", str(path), "-target", "/"],
            verification=False,
            env=env,
        )
        return InstallDisposition.APPLIED
