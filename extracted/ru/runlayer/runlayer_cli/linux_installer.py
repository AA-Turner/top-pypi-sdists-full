"""Linux package verification and installation."""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.installer_common import (
    CommandRunner,
    InstallerVerificationError,
    UnsupportedInstallerError,
    default_command_runner,
    posix_installer_environment,
    run_checked,
    validate_artifact,
)
from runlayer_cli.updater import Artifact, InstallDisposition


_PACKAGE_ARCHITECTURES = {
    "deb": {"arm64": "arm64", "x86_64": "amd64"},
    "rpm": {"arm64": "aarch64", "x86_64": "x86_64"},
}


class LinuxPackageInstaller:
    """Install checksum-verified Linux packages with the native package tool."""

    def __init__(
        self,
        *,
        package_name: str,
        runner: CommandRunner = default_command_runner,
    ) -> None:
        if not package_name:
            raise ValueError("Linux package name is required")
        self._package_name = package_name
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
            platform="linux",
            formats=("deb", "rpm"),
        )
        try:
            expected_arch = _PACKAGE_ARCHITECTURES[artifact.format][artifact.arch]
        except KeyError as exc:
            raise UnsupportedInstallerError(
                f"Unsupported Linux package architecture: {artifact.arch}"
            ) from exc
        if artifact.format == "deb":
            env = posix_installer_environment(DEBIAN_FRONTEND="noninteractive")
            identity = run_checked(
                self._runner,
                ["/usr/bin/dpkg-deb", "--field", str(path), "Package"],
                verification=True,
                env=env,
            )
            version_argv = [
                "/usr/bin/dpkg-deb",
                "--field",
                str(path),
                "Version",
            ]
            architecture_argv = [
                "/usr/bin/dpkg-deb",
                "--field",
                str(path),
                "Architecture",
            ]
            argv = [
                "/usr/bin/dpkg",
                "--force-confdef",
                "--force-confold",
                "--install",
                str(path),
            ]
        else:
            env = posix_installer_environment()
            identity = run_checked(
                self._runner,
                [
                    "/usr/bin/rpm",
                    "--query",
                    "--package",
                    "--queryformat",
                    "%{NAME}",
                    str(path),
                ],
                verification=True,
                env=env,
            )
            version_argv = [
                "/usr/bin/rpm",
                "--query",
                "--package",
                "--queryformat",
                "%{VERSION}",
                str(path),
            ]
            architecture_argv = [
                "/usr/bin/rpm",
                "--query",
                "--package",
                "--queryformat",
                "%{ARCH}",
                str(path),
            ]
            argv = ["/usr/bin/rpm", "-U", "--oldpackage", str(path)]
        if identity.stdout.strip() != self._package_name:
            raise InstallerVerificationError(
                "Linux package name does not match the requested product"
            )
        version = run_checked(
            self._runner,
            version_argv,
            verification=True,
            env=env,
        )
        if version.stdout.strip() != to_version:
            raise InstallerVerificationError(
                "Linux package does not match the backend-selected version"
            )
        architecture = run_checked(
            self._runner,
            architecture_argv,
            verification=True,
            env=env,
        )
        if architecture.stdout.strip() != expected_arch:
            raise InstallerVerificationError(
                "Linux package architecture does not match the requested target"
            )
        run_checked(self._runner, argv, verification=False, env=env)
        return InstallDisposition.APPLIED
