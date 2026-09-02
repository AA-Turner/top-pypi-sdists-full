"""Windows MSI signer and product verification tests."""

from pathlib import Path
from typing import cast

import pytest

from runlayer_cli.installer_common import InstallerVerificationError
from runlayer_cli.windows_installer_verifier import (
    WINDOWS_SIGNER_IDENTITY_EKU_OID,
    WindowsMsiVerifier,
    WindowsSignerIdentity,
    default_windows_executable,
)
from tests.platform_installer_helpers import (
    RecordingRunner,
    artifact,
    artifact_path,
    assert_argv_without_shell,
    result,
)
from tests.windows_installer_helpers import (
    AIWATCH_PRODUCT_NAME,
    AIWATCH_UPGRADE_CODE,
    authenticode_payload,
)


TARGET_VERSION = "2.0.0"
TARGET_ARCH = "x64"


def test_signer_identity_defaults_to_durable_identity_validation_eku() -> None:
    assert WindowsSignerIdentity() == WindowsSignerIdentity(
        identity_eku_oid=("1.3.6.1.4.1.311.97.321483706.169062785.441198005.491085472"),
    )


def test_accepts_rotated_certificate_names_with_pinned_identity_eku(
    tmp_path: Path,
) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                signer_name="Renamed Runlayer Signer",
                issuer_name="Rotated Microsoft Artifact Signing CA",
            )
        )
    )
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    verifier.verify(
        path,
        expected_version=TARGET_VERSION,
        expected_arch=TARGET_ARCH,
    )


def test_pins_signer_identity_product_and_target_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RUNLAYER_API_KEY", "secret-runlayer")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret-aws")
    monkeypatch.setenv("GITHUB_TOKEN", "secret-github")
    monkeypatch.setenv("PSModulePath", r"C:\Users\attacker\Modules")
    monkeypatch.setenv("COMPlus_Profiler", "{attacker-profiler}")
    value = artifact("windows", "msi", "aiwatch-2.0.0-win-x64.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(result(stdout=authenticode_payload()))
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    verifier.verify(
        path,
        expected_version=TARGET_VERSION,
        expected_arch=TARGET_ARCH,
    )

    script = runner.calls[0][0][-1]
    assert "$PSModuleAutoLoadingPreference = 'None'" in script
    assert (
        "Microsoft.PowerShell.Security', 'Microsoft.PowerShell.Security.psd1'" in script
    )
    assert (
        "Microsoft.PowerShell.Utility', 'Microsoft.PowerShell.Utility.psd1'" in script
    )
    assert script.count("Microsoft.PowerShell.Core\\Import-Module") == 2
    assert "Microsoft.PowerShell.Security\\Get-AuthenticodeSignature" in script
    assert "WHERE ``Property`` = 'ProductName'" in script
    assert "MsiProductName" in script
    assert "MsiProductVersion" in script
    assert "MsiTemplate" in script
    assert "RUNLAYER_SELF_UPDATE_READY" in script
    assert "MsiSelfUpdateReady" in script
    signature_env = cast(dict[str, str], runner.calls[0][1]["env"])
    assert signature_env == {
        "ComSpec": r"C:\Windows\System32\cmd.exe",
        "PATH": (
            r"C:\Windows\System32;"
            r"C:\Windows\System32\WindowsPowerShell\v1.0"
        ),
        "PSModulePath": (r"C:\Windows\System32\WindowsPowerShell\v1.0\Modules"),
        "SystemRoot": r"C:\Windows",
        "TEMP": r"C:\Windows\Temp",
        "TMP": r"C:\Windows\Temp",
        "WINDIR": r"C:\Windows",
        "RUNLAYER_INSTALLER_PATH": str(path),
        "RUNLAYER_EXPECTED_SIGNER_IDENTITY_EKU": WINDOWS_SIGNER_IDENTITY_EKU_OID,
    }
    assert_argv_without_shell(runner)


def test_default_executable_ignores_inherited_systemroot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SystemRoot", r"C:\Users\attacker\Windows")

    executable = default_windows_executable(r"WindowsPowerShell\v1.0\powershell.exe")

    assert executable.casefold().endswith(
        r"\system32\windowspowershell\v1.0\powershell.exe"
    )
    assert "attacker" not in executable.casefold()


@pytest.mark.parametrize(
    ("status", "eku_oids", "message"),
    [
        (
            "NotSigned",
            [WINDOWS_SIGNER_IDENTITY_EKU_OID],
            "status",
        ),
        (
            "Valid",
            ["1.3.6.1.5.5.7.3.3"],
            "identity EKU",
        ),
    ],
)
def test_rejects_wrong_authenticode_identity(
    tmp_path: Path,
    status: str,
    eku_oids: list[str],
    message: str,
) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                status=status,
                eku_oids=eku_oids,
            )
        )
    )
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    with pytest.raises(InstallerVerificationError, match=message):
        verifier.verify(
            path,
            expected_version=TARGET_VERSION,
            expected_arch=TARGET_ARCH,
        )

    assert len(runner.calls) == 1


def test_rejects_other_runlayer_product(tmp_path: Path) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                upgrade_code="{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}"
            )
        )
    )
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    with pytest.raises(InstallerVerificationError, match="requested product"):
        verifier.verify(
            path,
            expected_version=TARGET_VERSION,
            expected_arch=TARGET_ARCH,
        )


def test_rejects_other_distribution_with_shared_upgrade_code(tmp_path: Path) -> None:
    value = artifact("windows", "msi", "runlayer-desktop.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                upgrade_code="{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}",
                product_name="Runlayer CLI",
            )
        )
    )
    verifier = WindowsMsiVerifier(
        upgrade_code="{9F4B2E71-3C8A-4D5E-A1B2-6E7F8091C2D3}",
        product_name="Runlayer",
        runner=runner,
        powershell_executable="powershell.exe",
    )

    with pytest.raises(InstallerVerificationError, match="ProductName"):
        verifier.verify(
            path,
            expected_version=TARGET_VERSION,
            expected_arch=TARGET_ARCH,
        )


@pytest.mark.parametrize(
    ("product_version", "template", "message"),
    [
        ("1.9.0", "x64;1033", "version"),
        ("2.0.0", "Arm64;1033", "architecture"),
        ("2.0.0", "", "architecture"),
    ],
)
def test_rejects_wrong_target_metadata(
    tmp_path: Path,
    product_version: str,
    template: str,
    message: str,
) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                product_version=product_version,
                template=template,
            )
        )
    )
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    with pytest.raises(InstallerVerificationError, match=message):
        verifier.verify(
            path,
            expected_version=TARGET_VERSION,
            expected_arch=TARGET_ARCH,
        )


def test_rejects_msi_without_self_update_handoff(tmp_path: Path) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(result(stdout=authenticode_payload(self_update_ready="")))
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    with pytest.raises(InstallerVerificationError, match="self-update handoff"):
        verifier.verify(
            path,
            expected_version=TARGET_VERSION,
            expected_arch=TARGET_ARCH,
        )


def test_signer_identity_can_be_overridden_for_identity_rotation(
    tmp_path: Path,
) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    identity = WindowsSignerIdentity(
        identity_eku_oid="1.2.3.4.5",
    )
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                eku_oids=[identity.identity_eku_oid],
            )
        )
    )
    verifier = WindowsMsiVerifier(
        signer_identity=identity,
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    verifier.verify(
        path,
        expected_version=TARGET_VERSION,
        expected_arch=TARGET_ARCH,
    )


def test_signature_requires_zero_exit(tmp_path: Path) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value).resolve()
    runner = RecordingRunner(result(returncode=3010))
    verifier = WindowsMsiVerifier(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
    )

    with pytest.raises(InstallerVerificationError, match="3010"):
        verifier.verify(
            path,
            expected_version=TARGET_VERSION,
            expected_arch=TARGET_ARCH,
        )
