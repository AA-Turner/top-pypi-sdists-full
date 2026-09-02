"""Public facade and host detection for OS-native self-update installers."""

from __future__ import annotations

from collections.abc import Callable, Mapping
import os
from pathlib import Path
import platform as platform_module

from runlayer_cli.installer_common import CommandRunner as CommandRunner
from runlayer_cli.installer_common import (
    InstallerExecutionError as InstallerExecutionError,
)
from runlayer_cli.installer_common import (
    InstallerVerificationError as InstallerVerificationError,
)
from runlayer_cli.installer_common import (
    UnsupportedInstallerError as UnsupportedInstallerError,
)
from runlayer_cli.daemon.windows_scm import SERVICE_NAME as AIWATCH_SERVICE_NAME
from runlayer_cli.installer_common import default_command_runner
from runlayer_cli.linux_installer import LinuxPackageInstaller as LinuxPackageInstaller
from runlayer_cli.macos_installer import MacOSPackageInstaller as MacOSPackageInstaller
from runlayer_cli.product import PRODUCT_DISPLAY_NAMES
from runlayer_cli.updater import Artifact, InstallDisposition, InstallTarget
from runlayer_cli.windows_installer import WindowsMsiInstaller as WindowsMsiInstaller
from runlayer_cli.windows_installer_verifier import (
    WINDOWS_SIGNER_IDENTITY_EKU_OID as WINDOWS_SIGNER_IDENTITY_EKU_OID,
)
from runlayer_cli.windows_installer_verifier import (
    WindowsSignerIdentity as WindowsSignerIdentity,
)
from runlayer_cli.windows_update_handoff import (
    WindowsUpdateHandoffInstaller as WindowsUpdateHandoffInstaller,
)
from runlayer_cli.windows_update_handoff import windows_update_outcome_marker_path


MACOS_PACKAGE_ID_BY_PACKAGE = {
    "ai-watch": "com.runlayer.aiwatch",
    "cli": "com.runlayer.cli",
    "desktop": "com.runlayer.desktop",
}
LINUX_PACKAGE_NAME_BY_PACKAGE = {
    "ai-watch": "runlayer-aiwatch",
    "cli": "runlayer",
}
WINDOWS_UPGRADE_CODE_BY_PACKAGE = {
    "ai-watch": "{E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C}",
    "cli": "{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}",
    "desktop": "{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}",
}
WINDOWS_PRODUCT_NAME_BY_PACKAGE = {
    "ai-watch": "Runlayer AI Watch",
    **PRODUCT_DISPLAY_NAMES,
}
DEBIAN_DISTRO_IDS = frozenset(
    {"debian", "kali", "linuxmint", "pop", "raspbian", "ubuntu"}
)
RPM_DISTRO_IDS = frozenset(
    {
        "almalinux",
        "amzn",
        "centos",
        "fedora",
        "ol",
        "opensuse",
        "opensuse-leap",
        "rhel",
        "rocky",
        "sles",
        "suse",
    }
)
WINDOWS_HANDOFF_TASK_BY_PACKAGE = {
    "ai-watch": "AIWatchUpdateHandoff",
    "cli": "CLIUpdateHandoff",
    "desktop": "CLIUpdateHandoff",
}
WINDOWS_STAGED_FILENAME_BY_PACKAGE = {
    "ai-watch": "aiwatch-update.msi",
    "cli": "runlayer-update.msi",
    "desktop": "runlayer-desktop-update.msi",
}
WINDOWS_PROCESS_NAME_BY_PACKAGE = {
    "ai-watch": "aiwatch",
    "cli": "runlayer",
    "desktop": "runlayer",
}
WINDOWS_INSTALL_DIRECTORY_BY_PACKAGE = {
    "ai-watch": r"C:\Program Files\Runlayer\AIWatch",
    "cli": r"C:\Program Files\Runlayer\CLI",
    "desktop": r"C:\Program Files\Runlayer\CLI",
}
WINDOWS_QUIESCE_TASKS_BY_PACKAGE = {
    "ai-watch": ("AIWatchScan", "AIWatchHooks"),
    "cli": ("CLISchedule",),
    "desktop": ("CLISchedule",),
}
WINDOWS_QUIESCE_SERVICES_BY_PACKAGE = {
    "ai-watch": (AIWATCH_SERVICE_NAME,),
    "cli": (),
    "desktop": (),
}


def _normalized_arch(system: str, machine: str) -> str:
    normalized = machine.casefold().replace("-", "_")
    if normalized in {"amd64", "x86_64"}:
        return "x64" if system == "windows" else "x86_64"
    if normalized in {"aarch64", "arm64"}:
        return "arm64"
    raise UnsupportedInstallerError(f"Unsupported native architecture: {machine!r}")


def _linux_format_from_os_release(
    linux_os_release: Callable[[], Mapping[str, str]],
) -> str | None:
    try:
        os_release = linux_os_release()
    except OSError:
        os_release = {}
    distro_ids = {
        value.casefold()
        for key in ("ID", "ID_LIKE")
        for value in os_release.get(key, "").split()
    }
    is_debian_family = bool(distro_ids & DEBIAN_DISTRO_IDS)
    is_rpm_family = bool(distro_ids & RPM_DISTRO_IDS)
    format_: str | None = None
    if is_debian_family != is_rpm_family:
        format_ = "deb" if is_debian_family else "rpm"
    return format_


def native_install_target(
    *,
    system: str | None = None,
    machine: str | None = None,
    linux_format: str | None = None,
    executable_exists: Callable[[str], bool] = os.path.isfile,
    linux_os_release: Callable[[], Mapping[str, str]] = (
        platform_module.freedesktop_os_release
    ),
) -> InstallTarget:
    """Return the platform/arch/format slot for the current native host."""
    detected_system = (system or platform_module.system()).casefold()
    detected_machine = machine or platform_module.machine()
    if detected_system == "darwin":
        platform = "macos"
        format_ = "pkg"
    elif detected_system == "windows":
        platform = "windows"
        format_ = "msi"
    elif detected_system == "linux":
        platform = "linux"
        if linux_format is not None:
            format_ = linux_format
        else:
            has_dpkg = executable_exists("/usr/bin/dpkg")
            has_rpm = executable_exists("/usr/bin/rpm")
            if not has_dpkg and not has_rpm:
                raise UnsupportedInstallerError(
                    "Linux self-update requires a native package manager; "
                    "found neither dpkg nor rpm"
                )
            if has_dpkg and has_rpm:
                format_ = _linux_format_from_os_release(linux_os_release)
                if format_ is None:
                    raise UnsupportedInstallerError(
                        "Linux self-update found both dpkg and rpm, but the distro "
                        "family could not be determined from /etc/os-release"
                    )
            else:
                format_ = "deb" if has_dpkg else "rpm"
        if format_ not in {"deb", "rpm"}:
            raise UnsupportedInstallerError(
                f"Unsupported Linux installer format: {format_!r}"
            )
    else:
        raise UnsupportedInstallerError(
            f"Unsupported native operating system: {detected_system!r}"
        )
    return InstallTarget(
        platform=platform,
        arch=_normalized_arch(platform, detected_machine),
        format=format_,
    )


class NativePlatformInstaller:
    """PlatformInstaller facade sharing one InstallTarget with updater selection."""

    def __init__(
        self,
        package: str,
        *,
        target: InstallTarget | None = None,
        windows_signer_identity: WindowsSignerIdentity | None = None,
        runner: CommandRunner = default_command_runner,
        powershell_executable: str | None = None,
        msiexec_executable: str | None = None,
    ) -> None:
        if package not in WINDOWS_UPGRADE_CODE_BY_PACKAGE:
            raise ValueError(f"Unsupported binary package: {package!r}")
        self.target = target or native_install_target()
        self.outcome_marker_path: Path | None = None
        if self.target.platform == "macos":
            self._delegate = MacOSPackageInstaller(
                package_id=MACOS_PACKAGE_ID_BY_PACKAGE[package],
                runner=runner,
            )
        elif self.target.platform == "linux":
            if package not in LINUX_PACKAGE_NAME_BY_PACKAGE:
                raise UnsupportedInstallerError(
                    f"No Linux installer exists for binary package: {package!r}"
                )
            self._delegate = LinuxPackageInstaller(
                package_name=LINUX_PACKAGE_NAME_BY_PACKAGE[package],
                runner=runner,
            )
        elif self.target.platform == "windows":
            windows_delegate = WindowsUpdateHandoffInstaller(
                upgrade_code=WINDOWS_UPGRADE_CODE_BY_PACKAGE[package],
                product_name=WINDOWS_PRODUCT_NAME_BY_PACKAGE[package],
                task_name=WINDOWS_HANDOFF_TASK_BY_PACKAGE[package],
                staged_filename=WINDOWS_STAGED_FILENAME_BY_PACKAGE[package],
                process_name=WINDOWS_PROCESS_NAME_BY_PACKAGE[package],
                product_install_directory=WINDOWS_INSTALL_DIRECTORY_BY_PACKAGE[package],
                quiesce_task_names=WINDOWS_QUIESCE_TASKS_BY_PACKAGE[package],
                quiesce_service_names=WINDOWS_QUIESCE_SERVICES_BY_PACKAGE[package],
                signer_identity=windows_signer_identity,
                runner=runner,
                powershell_executable=powershell_executable,
                msiexec_executable=msiexec_executable,
            )
            self._delegate = windows_delegate
            self.outcome_marker_path = windows_update_outcome_marker_path(
                WINDOWS_STAGED_FILENAME_BY_PACKAGE[package]
            )
        else:
            raise UnsupportedInstallerError(
                f"Unsupported native platform: {self.target.platform!r}"
            )

    def verify_and_install(
        self,
        artifact_path: Path,
        *,
        artifact: Artifact,
        from_version: str,
        to_version: str,
    ) -> InstallDisposition:
        artifact_target = InstallTarget(
            platform=artifact.platform,
            arch=artifact.arch,
            format=artifact.format,
            variant=artifact.variant,
        )
        if artifact_target != self.target:
            raise UnsupportedInstallerError(
                f"Artifact slot {artifact_target} does not match native slot {self.target}"
            )
        return self._delegate.verify_and_install(
            artifact_path,
            artifact=artifact,
            from_version=from_version,
            to_version=to_version,
        )
