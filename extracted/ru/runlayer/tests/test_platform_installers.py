"""Native installer host detection and dispatch tests."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

from runlayer_cli import platform_installers
from runlayer_cli.linux_installer import LinuxPackageInstaller
from runlayer_cli.macos_installer import MacOSPackageInstaller
from runlayer_cli.platform_installers import (
    NativePlatformInstaller,
    UnsupportedInstallerError,
    native_install_target,
)
from runlayer_cli.updater import InstallTarget
from runlayer_cli.windows_installer import WindowsMsiInstaller
from runlayer_cli.windows_installer_verifier import (
    WINDOWS_SIGNER_IDENTITY_EKU_OID,
    WindowsSignerIdentity,
)
from tests.platform_installer_helpers import (
    RecordingRunner,
    artifact,
    artifact_path,
    result,
)


@pytest.mark.parametrize(
    ("system", "machine", "linux_format", "expected"),
    [
        ("Darwin", "arm64", None, InstallTarget("macos", "arm64", "pkg")),
        ("Darwin", "x86_64", None, InstallTarget("macos", "x86_64", "pkg")),
        ("Windows", "AMD64", None, InstallTarget("windows", "x64", "msi")),
        ("Linux", "x86_64", "deb", InstallTarget("linux", "x86_64", "deb")),
        ("Linux", "AMD64", "rpm", InstallTarget("linux", "x86_64", "rpm")),
    ],
)
def test_native_install_target_normalizes_platform_arch_and_format(
    system: str,
    machine: str,
    linux_format: str | None,
    expected: InstallTarget,
) -> None:
    assert (
        native_install_target(
            system=system,
            machine=machine,
            linux_format=linux_format,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("available", "expected_format"),
    [
        ({"/usr/bin/dpkg"}, "deb"),
        ({"/usr/bin/rpm"}, "rpm"),
    ],
)
def test_linux_target_detects_one_native_package_manager(
    available: set[str],
    expected_format: str,
) -> None:
    target = native_install_target(
        system="Linux",
        machine="x86_64",
        executable_exists=available.__contains__,
    )

    assert target == InstallTarget("linux", "x86_64", expected_format)


@pytest.mark.parametrize(
    ("os_release", "expected_format"),
    [
        ({"ID": "ubuntu", "ID_LIKE": "debian"}, "deb"),
        ({"ID": "rocky", "ID_LIKE": "rhel centos fedora"}, "rpm"),
    ],
)
def test_linux_target_uses_distro_family_when_both_package_managers_exist(
    os_release: dict[str, str],
    expected_format: str,
) -> None:
    target = native_install_target(
        system="Linux",
        machine="x86_64",
        executable_exists={"/usr/bin/dpkg", "/usr/bin/rpm"}.__contains__,
        linux_os_release=lambda: os_release,
    )

    assert target == InstallTarget("linux", "x86_64", expected_format)


def test_linux_target_rejects_ambiguous_distro_with_both_package_managers() -> None:
    with pytest.raises(
        UnsupportedInstallerError,
        match="both dpkg and rpm.*distro family",
    ):
        native_install_target(
            system="Linux",
            machine="x86_64",
            executable_exists={"/usr/bin/dpkg", "/usr/bin/rpm"}.__contains__,
            linux_os_release=lambda: {"ID": "unknown"},
        )


def test_linux_target_requires_a_native_package_manager() -> None:
    with pytest.raises(UnsupportedInstallerError, match="neither dpkg nor rpm"):
        native_install_target(
            system="Linux",
            machine="x86_64",
            executable_exists=set().__contains__,
        )


def test_native_platform_installer_dispatches_using_same_target(tmp_path: Path) -> None:
    target = InstallTarget("linux", "x86_64", "deb")
    value = artifact("linux", "deb", "runlayer_2.0.0_amd64.deb")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout="runlayer\n"),
        result(stdout="2.0.0\n"),
        result(stdout="amd64\n"),
        result(),
    )
    installer = NativePlatformInstaller("cli", target=target, runner=runner)

    installer.verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    assert runner.calls[0][0] == [
        "/usr/bin/dpkg-deb",
        "--field",
        str(path.resolve()),
        "Package",
    ]
    assert runner.calls[1][0] == [
        "/usr/bin/dpkg-deb",
        "--field",
        str(path.resolve()),
        "Version",
    ]
    assert runner.calls[2][0] == [
        "/usr/bin/dpkg-deb",
        "--field",
        str(path.resolve()),
        "Architecture",
    ]
    assert runner.calls[3][0] == [
        "/usr/bin/dpkg",
        "--force-confdef",
        "--force-confold",
        "--install",
        str(path.resolve()),
    ]
    env = cast(dict[str, str], runner.calls[3][1]["env"])
    assert env["DEBIAN_FRONTEND"] == "noninteractive"


def test_native_windows_installer_uses_stable_identity_defaults() -> None:
    installer = NativePlatformInstaller(
        "ai-watch",
        target=InstallTarget("windows", "x64", "msi"),
    )

    assert installer.target == InstallTarget("windows", "x64", "msi")


@pytest.mark.parametrize(
    ("package", "expected_product_name"),
    [
        ("ai-watch", "Runlayer AI Watch"),
        ("cli", "Runlayer CLI"),
        ("desktop", "Runlayer"),
    ],
)
def test_native_windows_installer_passes_expected_product_name(
    monkeypatch: pytest.MonkeyPatch,
    package: str,
    expected_product_name: str,
) -> None:
    captured: dict[str, object] = {}

    class RecordingHandoff:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

    monkeypatch.setattr(
        platform_installers,
        "WindowsUpdateHandoffInstaller",
        RecordingHandoff,
    )

    NativePlatformInstaller(package, target=InstallTarget("windows", "x64", "msi"))

    assert captured["product_name"] == expected_product_name


@pytest.mark.parametrize(
    ("package", "target", "delegate_name", "identity_key", "expected_identity"),
    [
        (
            "ai-watch",
            InstallTarget("macos", "arm64", "pkg"),
            "MacOSPackageInstaller",
            "package_id",
            "com.runlayer.aiwatch",
        ),
        (
            "cli",
            InstallTarget("macos", "arm64", "pkg"),
            "MacOSPackageInstaller",
            "package_id",
            "com.runlayer.cli",
        ),
        (
            "desktop",
            InstallTarget("macos", "arm64", "pkg"),
            "MacOSPackageInstaller",
            "package_id",
            "com.runlayer.desktop",
        ),
        (
            "ai-watch",
            InstallTarget("linux", "x86_64", "deb"),
            "LinuxPackageInstaller",
            "package_name",
            "runlayer-aiwatch",
        ),
        (
            "cli",
            InstallTarget("linux", "x86_64", "deb"),
            "LinuxPackageInstaller",
            "package_name",
            "runlayer",
        ),
        (
            "ai-watch",
            InstallTarget("windows", "x64", "msi"),
            "WindowsUpdateHandoffInstaller",
            "upgrade_code",
            "{E3A2F1C0-7B4D-4E9A-8C6F-1D2E3F4A5B6C}",
        ),
        (
            "cli",
            InstallTarget("windows", "x64", "msi"),
            "WindowsUpdateHandoffInstaller",
            "upgrade_code",
            "{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}",
        ),
        (
            "desktop",
            InstallTarget("windows", "x64", "msi"),
            "WindowsUpdateHandoffInstaller",
            "upgrade_code",
            "{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}",
        ),
    ],
)
def test_native_installer_passes_exact_product_identity_to_delegate(
    monkeypatch: pytest.MonkeyPatch,
    package: str,
    target: InstallTarget,
    delegate_name: str,
    identity_key: str,
    expected_identity: str,
) -> None:
    captured: dict[str, object] = {}

    class RecordingDelegate:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

    monkeypatch.setattr(platform_installers, delegate_name, RecordingDelegate)

    NativePlatformInstaller(package, target=target)

    assert captured[identity_key] == expected_identity


def test_desktop_windows_installer_reuses_exclusive_cli_install_layout() -> None:
    assert (
        platform_installers.WINDOWS_UPGRADE_CODE_BY_PACKAGE["desktop"]
        == platform_installers.WINDOWS_UPGRADE_CODE_BY_PACKAGE["cli"]
    )
    assert (
        platform_installers.WINDOWS_INSTALL_DIRECTORY_BY_PACKAGE["desktop"]
        == platform_installers.WINDOWS_INSTALL_DIRECTORY_BY_PACKAGE["cli"]
    )
    assert (
        platform_installers.WINDOWS_HANDOFF_TASK_BY_PACKAGE["desktop"]
        == "CLIUpdateHandoff"
    )
    assert (
        platform_installers.WINDOWS_STAGED_FILENAME_BY_PACKAGE["desktop"]
        == "runlayer-desktop-update.msi"
    )
    assert platform_installers.WINDOWS_QUIESCE_TASKS_BY_PACKAGE["desktop"] == (
        "CLISchedule",
    )


def test_desktop_has_no_linux_installer() -> None:
    with pytest.raises(UnsupportedInstallerError, match="No Linux installer"):
        NativePlatformInstaller(
            "desktop",
            target=InstallTarget("linux", "x86_64", "deb"),
        )


def test_public_facade_preserves_os_specific_imports() -> None:
    assert platform_installers.MacOSPackageInstaller is MacOSPackageInstaller
    assert platform_installers.LinuxPackageInstaller is LinuxPackageInstaller
    assert platform_installers.WindowsMsiInstaller is WindowsMsiInstaller
    assert platform_installers.WindowsSignerIdentity is WindowsSignerIdentity
    assert (
        platform_installers.WINDOWS_SIGNER_IDENTITY_EKU_OID
        == WINDOWS_SIGNER_IDENTITY_EKU_OID
    )


def test_native_installer_rejects_artifact_outside_detected_slot(
    tmp_path: Path,
) -> None:
    value = artifact("linux", "rpm", "runlayer.rpm")
    path = artifact_path(tmp_path, value)
    installer = NativePlatformInstaller(
        "cli",
        target=InstallTarget("linux", "x86_64", "deb"),
        runner=RecordingRunner(),
    )

    with pytest.raises(UnsupportedInstallerError, match="does not match native slot"):
        installer.verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )


@pytest.mark.parametrize(
    ("target_variant", "artifact_variant"),
    [(None, "glibc2.17"), ("glibc2.17", None), ("glibc2.17", "glibc2.28")],
)
def test_native_installer_rejects_artifact_with_mismatched_variant(
    tmp_path: Path,
    target_variant: str | None,
    artifact_variant: str | None,
) -> None:
    value = replace(artifact("linux", "deb", "runlayer.deb"), variant=artifact_variant)
    path = artifact_path(tmp_path, value)
    installer = NativePlatformInstaller(
        "cli",
        target=InstallTarget("linux", "x86_64", "deb", variant=target_variant),
        runner=RecordingRunner(),
    )

    with pytest.raises(UnsupportedInstallerError, match="does not match native slot"):
        installer.verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )
