"""Windows MSI signing identity, product, version, and architecture verifier."""

from __future__ import annotations

import ctypes
import json
import ntpath
import os
from dataclasses import dataclass
from pathlib import Path

from runlayer_cli import regex_safe
from runlayer_cli.installer_common import (
    CommandRunner,
    InstallerExecutionError,
    InstallerVerificationError,
    default_command_runner,
    run_checked,
    windows_installer_environment,
)

WINDOWS_SIGNER_IDENTITY_EKU_OID = (
    "1.3.6.1.4.1.311.97.321483706.169062785.441198005.491085472"
)

_GUID_PATTERN = regex_safe.compile(
    r"^\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}$"
)
_OID_PATTERN = regex_safe.compile(r"^\d+(?:\.\d+)+$")

_AUTHENTICODE_SCRIPT = (
    "$ErrorActionPreference = 'Stop'; "
    "$PSModuleAutoLoadingPreference = 'None'; "
    "$securityModulePath = [System.IO.Path]::Combine($PSHOME, 'Modules', "
    "'Microsoft.PowerShell.Security', 'Microsoft.PowerShell.Security.psd1'); "
    "$utilityModulePath = [System.IO.Path]::Combine($PSHOME, 'Modules', "
    "'Microsoft.PowerShell.Utility', 'Microsoft.PowerShell.Utility.psd1'); "
    "Microsoft.PowerShell.Core\\Import-Module -Name $securityModulePath "
    "-Force -ErrorAction Stop; "
    "Microsoft.PowerShell.Core\\Import-Module -Name $utilityModulePath "
    "-Force -ErrorAction Stop; "
    "$signature = Microsoft.PowerShell.Security\\Get-AuthenticodeSignature "
    "-LiteralPath $env:RUNLAYER_INSTALLER_PATH; "
    "$certificate = $signature.SignerCertificate; "
    "$signerName = $null; $issuerName = $null; $ekuOids = @(); "
    "if ($null -ne $certificate) { "
    "$signerName = $certificate.GetNameInfo("
    "[System.Security.Cryptography.X509Certificates.X509NameType]::SimpleName, "
    "$false); "
    "$issuerName = $certificate.GetNameInfo("
    "[System.Security.Cryptography.X509Certificates.X509NameType]::SimpleName, "
    "$true); "
    "$ekuExtension = $null; foreach ($extension in $certificate.Extensions) { "
    "if ($extension.Oid.Value -eq '2.5.29.37') { "
    "$ekuExtension = $extension; break } }; "
    "if ($null -ne $ekuExtension) { "
    "$parsedEku = [System.Security.Cryptography.X509Certificates."
    "X509EnhancedKeyUsageExtension]::new($ekuExtension, $ekuExtension.Critical); "
    "foreach ($oid in $parsedEku.EnhancedKeyUsages) { "
    "$ekuOids += [string]$oid.Value } } }; "
    "if ([string]$signature.Status -ne 'Valid' -or "
    "$ekuOids -notcontains $env:RUNLAYER_EXPECTED_SIGNER_IDENTITY_EKU) { "
    "throw 'Authenticode identity does not match the expected Runlayer signer' }; "
    "$installerType = [type]::GetTypeFromProgID("
    "'WindowsInstaller.Installer', $true); "
    "$installer = [System.Activator]::CreateInstance($installerType); "
    "$database = $installer.OpenDatabase($env:RUNLAYER_INSTALLER_PATH, 0); "
    '$view = $database.OpenView("SELECT ``Value`` FROM ``Property`` '
    "WHERE ``Property`` = 'UpgradeCode'\"); "
    "$view.Execute(); $record = $view.Fetch(); $msiUpgradeCode = $null; "
    "if ($null -ne $record) { $msiUpgradeCode = [string]$record.StringData(1) }; "
    '$view = $database.OpenView("SELECT ``Value`` FROM ``Property`` '
    "WHERE ``Property`` = 'ProductName'\"); "
    "$view.Execute(); $record = $view.Fetch(); $msiProductName = $null; "
    "if ($null -ne $record) { $msiProductName = [string]$record.StringData(1) }; "
    '$view = $database.OpenView("SELECT ``Value`` FROM ``Property`` '
    "WHERE ``Property`` = 'ProductVersion'\"); "
    "$view.Execute(); $record = $view.Fetch(); $msiProductVersion = $null; "
    "if ($null -ne $record) { "
    "$msiProductVersion = [string]$record.StringData(1) }; "
    '$view = $database.OpenView("SELECT ``Value`` FROM ``Property`` '
    "WHERE ``Property`` = 'RUNLAYER_SELF_UPDATE_READY'\"); "
    "$view.Execute(); $record = $view.Fetch(); $msiSelfUpdateReady = $null; "
    "if ($null -ne $record) { "
    "$msiSelfUpdateReady = [string]$record.StringData(1) }; "
    "$summary = $database.SummaryInformation(0); "
    "$msiTemplate = [string]$summary.Property(7); "
    "$payload = [pscustomobject]@{ Status = [string]$signature.Status; "
    "SignerName = $signerName; IssuerName = $issuerName; "
    "EnhancedKeyUsageOids = @($ekuOids); MsiUpgradeCode = $msiUpgradeCode; "
    "MsiProductName = $msiProductName; MsiProductVersion = $msiProductVersion; "
    "MsiTemplate = $msiTemplate; "
    "MsiSelfUpdateReady = $msiSelfUpdateReady }; "
    "Microsoft.PowerShell.Utility\\ConvertTo-Json "
    "-InputObject $payload -Compress"
)
_RELATED_PRODUCTS_SCRIPT = (
    "$ErrorActionPreference = 'Stop'; "
    "$PSModuleAutoLoadingPreference = 'None'; "
    "$utilityModulePath = [System.IO.Path]::Combine($PSHOME, 'Modules', "
    "'Microsoft.PowerShell.Utility', 'Microsoft.PowerShell.Utility.psd1'); "
    "Microsoft.PowerShell.Core\\Import-Module -Name $utilityModulePath "
    "-Force -ErrorAction Stop; "
    "$installerType = [type]::GetTypeFromProgID("
    "'WindowsInstaller.Installer', $true); "
    "$installer = [System.Activator]::CreateInstance($installerType); "
    "$products = @($installer.RelatedProducts($env:RUNLAYER_MSI_UPGRADE_CODE)); "
    "Microsoft.PowerShell.Utility\\ConvertTo-Json "
    "-Compress -InputObject $products"
)


@dataclass(frozen=True)
class WindowsSignerIdentity:
    """Stable Azure Trusted Signing identity independent of rotating leaf certs."""

    identity_eku_oid: str = WINDOWS_SIGNER_IDENTITY_EKU_OID


def normalize_guid(value: str, *, field: str) -> str:
    normalized = value.strip().upper()
    if not normalized.startswith("{"):
        normalized = "{" + normalized + "}"
    if _GUID_PATTERN.fullmatch(normalized) is None:
        raise ValueError(f"{field} must be a Windows Installer GUID")
    return normalized


def windows_system_directory() -> str:
    """Resolve System32 without trusting the inherited process environment."""
    if os.name != "nt":
        return r"C:\Windows\System32"
    buffer = ctypes.create_unicode_buffer(32768)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    get_system_directory = kernel32.GetSystemDirectoryW
    get_system_directory.argtypes = [ctypes.c_wchar_p, ctypes.c_uint]
    get_system_directory.restype = ctypes.c_uint
    length = get_system_directory(buffer, len(buffer))
    if length == 0 or length >= len(buffer):
        raise InstallerExecutionError("Could not resolve Windows system directory")
    return buffer.value


def default_windows_executable(filename: str) -> str:
    return ntpath.join(windows_system_directory(), filename)


class WindowsMsiVerifier:
    """Verify the signer identity, product family, target version, and architecture."""

    def __init__(
        self,
        *,
        upgrade_code: str,
        product_name: str,
        signer_identity: WindowsSignerIdentity | None = None,
        runner: CommandRunner = default_command_runner,
        powershell_executable: str | None = None,
    ) -> None:
        self._signer_identity = signer_identity or WindowsSignerIdentity()
        if _OID_PATTERN.fullmatch(self._signer_identity.identity_eku_oid) is None:
            raise ValueError("Windows signer identity EKU must be a dotted OID")
        self.upgrade_code = normalize_guid(upgrade_code, field="upgrade_code")
        if not product_name.strip():
            raise ValueError("Windows MSI ProductName is required")
        self.product_name = product_name
        self._runner = runner
        self.system_directory = windows_system_directory()
        self._powershell = powershell_executable or default_windows_executable(
            r"WindowsPowerShell\v1.0\powershell.exe"
        )

    def powershell_command(self, script: str) -> list[str]:
        return [
            self._powershell,
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            script,
        ]

    def require_related_product(self) -> None:
        result = run_checked(
            self._runner,
            self.powershell_command(_RELATED_PRODUCTS_SCRIPT),
            verification=False,
            env=windows_installer_environment(
                self.system_directory,
                RUNLAYER_MSI_UPGRADE_CODE=self.upgrade_code,
            ),
        )
        try:
            payload = json.loads(result.stdout or "[]")
        except json.JSONDecodeError as exc:
            raise InstallerExecutionError(
                "Windows Installer returned invalid related-product output"
            ) from exc
        if isinstance(payload, str):
            products = [payload]
        elif isinstance(payload, list) and all(
            isinstance(product, str) for product in payload
        ):
            products = payload
        else:
            products = []
        if len(products) != 1:
            raise InstallerExecutionError(
                "Expected exactly one installed MSI related to the package UpgradeCode"
            )
        try:
            normalize_guid(products[0], field="product_code")
        except ValueError as exc:
            raise InstallerExecutionError(
                "Windows Installer returned an invalid related product code"
            ) from exc

    def verify(
        self,
        path: Path,
        *,
        expected_version: str,
        expected_arch: str,
    ) -> None:
        if not expected_version:
            raise ValueError("Expected Windows MSI version is required")
        normalized_expected_arch = expected_arch.strip().casefold()
        if normalized_expected_arch not in {"x64", "arm64"}:
            raise ValueError("Expected Windows MSI architecture is unsupported")
        result = run_checked(
            self._runner,
            self.powershell_command(_AUTHENTICODE_SCRIPT),
            verification=True,
            env=windows_installer_environment(
                self.system_directory,
                RUNLAYER_INSTALLER_PATH=str(path),
                RUNLAYER_EXPECTED_SIGNER_IDENTITY_EKU=(
                    self._signer_identity.identity_eku_oid
                ),
            ),
        )
        try:
            payload = json.loads(result.stdout)
        except (json.JSONDecodeError, TypeError) as exc:
            raise InstallerVerificationError(
                "Get-AuthenticodeSignature returned invalid output"
            ) from exc
        if not isinstance(payload, dict) or payload.get("Status") != "Valid":
            raise InstallerVerificationError(
                "Windows MSI Authenticode status is not Valid"
            )
        raw_eku_oids = payload.get("EnhancedKeyUsageOids")
        if isinstance(raw_eku_oids, str):
            eku_oids = [raw_eku_oids]
        elif isinstance(raw_eku_oids, list) and all(
            isinstance(oid, str) for oid in raw_eku_oids
        ):
            eku_oids = raw_eku_oids
        else:
            eku_oids = []
        if self._signer_identity.identity_eku_oid not in eku_oids:
            raise InstallerVerificationError(
                "Windows MSI signer is missing the pinned Azure identity EKU"
            )
        raw_upgrade_code = payload.get("MsiUpgradeCode")
        if not isinstance(raw_upgrade_code, str):
            raise InstallerVerificationError(
                "Windows MSI is missing its package UpgradeCode"
            )
        try:
            msi_upgrade_code = normalize_guid(raw_upgrade_code, field="MSI UpgradeCode")
        except ValueError as exc:
            raise InstallerVerificationError(
                "Windows MSI contains an invalid package UpgradeCode"
            ) from exc
        if msi_upgrade_code != self.upgrade_code:
            raise InstallerVerificationError(
                "Windows MSI UpgradeCode does not match the requested product"
            )
        msi_product_name = payload.get("MsiProductName")
        if not isinstance(msi_product_name, str):
            raise InstallerVerificationError(
                "Windows MSI is missing its embedded ProductName"
            )
        if msi_product_name != self.product_name:
            raise InstallerVerificationError(
                "Windows MSI ProductName does not match the requested distribution"
            )
        product_version = payload.get("MsiProductVersion")
        if product_version != expected_version:
            raise InstallerVerificationError(
                "Windows MSI embedded version does not match the backend target version"
            )
        if payload.get("MsiSelfUpdateReady") != "1":
            raise InstallerVerificationError(
                "Windows MSI does not support the required self-update handoff"
            )
        raw_template = payload.get("MsiTemplate")
        if not isinstance(raw_template, str):
            raise InstallerVerificationError(
                "Windows MSI is missing its embedded architecture"
            )
        embedded_arch = raw_template.partition(";")[0].strip().casefold()
        if embedded_arch != normalized_expected_arch:
            raise InstallerVerificationError(
                "Windows MSI embedded architecture does not match the requested "
                "architecture"
            )
