"""Windows MSI replacement tests."""

import json
from pathlib import Path
from typing import cast

import pytest

from runlayer_cli.installer_common import (
    InstallerExecutionError,
    InstallerVerificationError,
    UnsupportedInstallerError,
)
from runlayer_cli.windows_installer import WindowsMsiInstaller
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


def _installer(runner: RecordingRunner) -> WindowsMsiInstaller:
    return WindowsMsiInstaller(
        upgrade_code=AIWATCH_UPGRADE_CODE,
        product_name=AIWATCH_PRODUCT_NAME,
        runner=runner,
        powershell_executable="powershell.exe",
        msiexec_executable="msiexec.exe",
    )


def test_major_upgrades_related_product_with_verified_target(tmp_path: Path) -> None:
    value = artifact("windows", "msi", "aiwatch-2.0.0-win-x64.msi")
    path = artifact_path(tmp_path, value)
    product_code = "{12345678-90AB-CDEF-1234-567890ABCDEF}"
    runner = RecordingRunner(
        result(stdout=authenticode_payload()),
        result(stdout=json.dumps(product_code)),
        result(),
    )

    _installer(runner).verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    assert runner.calls[2][0] == [
        "msiexec.exe",
        "/i",
        str(path.resolve()),
        "/qn",
        "/norestart",
    ]
    assert not any("/x" in argv for argv, _ in runner.calls)
    assert_argv_without_shell(runner)


def test_arbitrary_target_uses_transactional_major_upgrade(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RUNLAYER_API_KEY", "secret-runlayer")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret-aws")
    monkeypatch.setenv("GITHUB_TOKEN", "secret-github")
    monkeypatch.setenv("PSModulePath", r"C:\Users\attacker\Modules")
    monkeypatch.setenv("COMPlus_Profiler", "{attacker-profiler}")
    value = artifact("windows", "msi", "aiwatch-1.0.0-win-x64.msi")
    path = artifact_path(tmp_path, value)
    product_code = "{12345678-90AB-CDEF-1234-567890ABCDEF}"
    runner = RecordingRunner(
        result(stdout=authenticode_payload(product_version="1.0.0")),
        result(stdout=json.dumps(product_code)),
        result(),
    )

    _installer(runner).verify_and_install(
        path,
        artifact=value,
        from_version="2.0.0",
        to_version="1.0.0",
    )

    discovery_script = runner.calls[1][0][-1]
    assert "$PSModuleAutoLoadingPreference = 'None'" in discovery_script
    assert "Microsoft.PowerShell.Core\\Import-Module" in discovery_script
    assert "Microsoft.PowerShell.Utility\\ConvertTo-Json" in discovery_script
    assert "New-Object" not in discovery_script
    discovery_env = cast(dict[str, str], runner.calls[1][1]["env"])
    assert discovery_env == {
        "ComSpec": r"C:\Windows\System32\cmd.exe",
        "PATH": (
            r"C:\Windows\System32;"
            r"C:\Windows\System32\WindowsPowerShell\v1.0"
        ),
        "PSModulePath": r"C:\Windows\System32\WindowsPowerShell\v1.0\Modules",
        "SystemRoot": r"C:\Windows",
        "TEMP": r"C:\Windows\Temp",
        "TMP": r"C:\Windows\Temp",
        "WINDIR": r"C:\Windows",
        "RUNLAYER_MSI_UPGRADE_CODE": AIWATCH_UPGRADE_CODE,
    }
    installer_env = {
        key: value
        for key, value in discovery_env.items()
        if key != "RUNLAYER_MSI_UPGRADE_CODE"
    }
    assert runner.calls[2][0] == [
        "msiexec.exe",
        "/i",
        str(path.resolve()),
        "/qn",
        "/norestart",
    ]
    assert runner.calls[2][1]["env"] == installer_env
    for argv, kwargs in runner.calls:
        command = "\n".join(argv)
        environment = cast(dict[str, str], kwargs["env"])
        for secret in ("secret-runlayer", "secret-aws", "secret-github"):
            assert secret not in command
            assert secret not in environment.values()


@pytest.mark.parametrize(
    ("product_version", "template", "message"),
    [
        ("1.9.0", "x64;1033", "version"),
        ("2.0.0", "Arm64;1033", "architecture"),
    ],
)
def test_target_metadata_mismatch_aborts_before_uninstall(
    tmp_path: Path,
    product_version: str,
    template: str,
    message: str,
) -> None:
    value = artifact("windows", "msi", "aiwatch-2.0.0-win-x64.msi")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(
            stdout=authenticode_payload(
                product_version=product_version,
                template=template,
            )
        )
    )

    with pytest.raises(InstallerVerificationError, match=message):
        _installer(runner).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 1


@pytest.mark.parametrize("reboot_success_code", [1641, 3010])
def test_accepts_msi_success_with_reboot_codes(
    tmp_path: Path,
    reboot_success_code: int,
) -> None:
    value = artifact("windows", "msi", "aiwatch-target-win-x64.msi")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout=authenticode_payload()),
        result(stdout=json.dumps("{12345678-90AB-CDEF-1234-567890ABCDEF}")),
        result(returncode=reboot_success_code),
    )

    _installer(runner).verify_and_install(
        path,
        artifact=value,
        from_version="anything",
        to_version="2.0.0",
    )

    assert len(runner.calls) == 3


def test_rejects_ambiguous_related_products_before_replacement(
    tmp_path: Path,
) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout=authenticode_payload(product_version="1.0.0")),
        result(
            stdout=json.dumps(
                [
                    "{12345678-90AB-CDEF-1234-567890ABCDEF}",
                    "{AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE}",
                ]
            )
        ),
    )

    with pytest.raises(InstallerExecutionError, match="exactly one"):
        _installer(runner).verify_and_install(
            path,
            artifact=value,
            from_version="2.0.0",
            to_version="1.0.0",
        )

    assert len(runner.calls) == 2


def test_product_discovery_requires_zero_exit(tmp_path: Path) -> None:
    value = artifact("windows", "msi", "aiwatch.msi")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout=authenticode_payload()),
        result(returncode=3010),
    )

    with pytest.raises(InstallerExecutionError, match="3010"):
        _installer(runner).verify_and_install(
            path,
            artifact=value,
            from_version="installed",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 2


def test_rejects_non_native_format(tmp_path: Path) -> None:
    value = artifact("windows", "intunewin", "aiwatch.intunewin")
    path = artifact_path(tmp_path, value)

    with pytest.raises(UnsupportedInstallerError):
        _installer(RecordingRunner()).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )
