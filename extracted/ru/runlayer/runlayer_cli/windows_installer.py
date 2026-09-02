"""Synchronous Windows MSI replacement primitive retained for direct callers."""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.installer_common import (
    CommandRunner,
    default_command_runner,
    run_checked,
    validate_artifact,
    windows_installer_environment,
)
from runlayer_cli.updater import Artifact, InstallDisposition
from runlayer_cli.windows_installer_verifier import (
    WindowsMsiVerifier,
    WindowsSignerIdentity,
    default_windows_executable,
)


_MSI_SUCCESS_CODES = frozenset({0, 1641, 3010})


class WindowsMsiInstaller:
    """Verify a pinned Authenticode signer, then replace the installed MSI."""

    def __init__(
        self,
        *,
        upgrade_code: str,
        product_name: str,
        signer_identity: WindowsSignerIdentity | None = None,
        runner: CommandRunner = default_command_runner,
        powershell_executable: str | None = None,
        msiexec_executable: str | None = None,
    ) -> None:
        self._runner = runner
        self._verifier = WindowsMsiVerifier(
            upgrade_code=upgrade_code,
            product_name=product_name,
            signer_identity=signer_identity,
            runner=runner,
            powershell_executable=powershell_executable,
        )
        self._msiexec = msiexec_executable or default_windows_executable("msiexec.exe")
        self._environment = windows_installer_environment(
            self._verifier.system_directory
        )

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
            platform="windows",
            formats=("msi",),
        )
        self._verifier.verify(
            path,
            expected_version=to_version,
            expected_arch=artifact.arch,
        )
        self._verifier.require_related_product()
        run_checked(
            self._runner,
            [
                self._msiexec,
                "/i",
                str(path),
                "/qn",
                "/norestart",
            ],
            verification=False,
            allowed_returncodes=_MSI_SUCCESS_CODES,
            env=self._environment,
        )
        return InstallDisposition.APPLIED
